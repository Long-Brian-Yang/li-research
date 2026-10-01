"""Load and summarize every completed LiNbOCl4 transport trajectory.

Repeated executions with the same initial-velocity seed are first averaged
within that seed; distinct seeds are then given equal weight in the
temperature-level estimate. No trajectory is chosen using its MSD or
agreement with a reference value.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import re

import numpy as np


ROOT = Path(__file__).resolve().parents[4]
RUN_ROOT = ROOT / "runs/md"
TEMPERATURES = (600, 800, 1000, 1200)
FIT_WINDOW_PS = (20.0, 500.0)
MODELS = {
    "MACE-MPA-0": "mace_mpa0_medium",
    "SevenNet-nano": "sevennet_nano_55",
    "M3GNet GPU": "m3gnet_matgl_gpu",
}
VELOCITY_SEED = re.compile(r"^\s*velocity\s+all\s+create\s+\S+\s+(\d+)\b", re.MULTILINE)


@dataclass(frozen=True)
class DiffusionTrack:
    model: str
    temperature_K: int
    seed: int
    path: Path
    diffusion_cm2_s: float


def discover_tracks(model_directory: str, temperature: int,
                    run_root: Path = RUN_ROOT) -> list[Path]:
    """Return all stored MSD trajectories for a model and temperature."""
    root = run_root / model_directory / "LiNbOCl4_2x2x3" / f"{temperature}K"
    return sorted(path for path in root.glob("replica_*/*/msd_li.dat") if path.is_file())


def velocity_seed(path: Path) -> int:
    """Read the Maxwell-velocity seed from the matching LAMMPS input."""
    input_path = path.with_name("in.md.lmp")
    if not input_path.is_file():
        raise FileNotFoundError(f"Missing MD input needed to identify trajectory seed: {input_path}")
    match = VELOCITY_SEED.search(input_path.read_text())
    if match is None:
        raise ValueError(f"Cannot determine initial-velocity seed from {input_path}")
    return int(match.group(1))


def diffusion_from_track(path: Path,
                         fit_window_ps: tuple[float, float] = FIT_WINDOW_PS) -> float:
    """Fit 3-D Li MSD and return D in cm^2/s using the fixed common window."""
    data = np.loadtxt(path, comments="#")
    if data.ndim != 2 or data.shape[1] < 5 or not np.isfinite(data[:, [0, 4]]).all():
        raise ValueError(f"Invalid MSD data: {path}")
    time_ps = data[:, 0] * 0.001  # LAMMPS timestep is 1 fs.
    if time_ps[0] > 1e-9 or time_ps[-1] + 1e-9 < fit_window_ps[1]:
        raise ValueError(f"MSD track does not span the common fit interval {fit_window_ps}: {path}")
    mask = (time_ps >= fit_window_ps[0]) & (time_ps <= fit_window_ps[1])
    if np.count_nonzero(mask) < 3:
        raise ValueError(f"Too few MSD samples in fit interval {fit_window_ps}: {path}")
    slope = float(np.polyfit(time_ps[mask], data[mask, 4], 1)[0])
    if not np.isfinite(slope) or slope <= 0:
        raise ValueError(f"Non-positive/non-finite MSD slope in {path}: {slope}")
    return slope / 6.0e4  # (Å^2/ps) / 6 × 10^-4 cm^2/s per Å^2/ps.


def collect_tracks() -> list[DiffusionTrack]:
    """Read each discovered trajectory, failing rather than silently omitting it."""
    tracks: list[DiffusionTrack] = []
    for model, directory in MODELS.items():
        for temperature in TEMPERATURES:
            paths = discover_tracks(directory, temperature)
            if not paths:
                raise FileNotFoundError(f"No completed MSD tracks for {model} at {temperature} K")
            tracks.extend(DiffusionTrack(model, temperature, velocity_seed(path), path,
                                         diffusion_from_track(path)) for path in paths)
    return tracks


def summarize_by_seed(tracks: list[DiffusionTrack]) -> dict[tuple[str, int], dict]:
    """Average executions sharing a seed, then summarize distinct seeds."""
    executions: dict[tuple[str, int, int], list[float]] = defaultdict(list)
    for track in tracks:
        executions[(track.model, track.temperature_K, track.seed)].append(track.diffusion_cm2_s)

    summaries: dict[tuple[str, int], dict] = {}
    for model in MODELS:
        for temperature in TEMPERATURES:
            seed_values = [float(np.mean(values)) for (m, t, _), values in executions.items()
                           if m == model and t == temperature]
            if not seed_values:
                raise ValueError(f"No velocity seeds found for {model} at {temperature} K")
            summaries[(model, temperature)] = {
                "D_mean_cm2_s": float(np.mean(seed_values)),
                "D_sample_sd_cm2_s": float(np.std(seed_values, ddof=1)) if len(seed_values) > 1 else 0.0,
                "seed_count": len(seed_values),
                "execution_count": sum(len(values) for (m, t, _), values in executions.items()
                                        if m == model and t == temperature),
                "seed_D_cm2_s": seed_values,
            }
    return summaries
