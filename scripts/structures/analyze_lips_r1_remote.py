"""Remote post-processing for completed Li3PS4 R1 GPUMD trajectories.

The raw trajectories remain on TSUBAME.  This script writes only compact CSV
tables and a JSON summary suitable for local plotting and report integration.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np
from ase.io import iread, read
from scipy.stats import linregress


TEMPERATURES = (300, 500, 700, 900)
WINDOWS = ((5, 20), (10, 40), (20, 80), (40, 100), (50, 150))
MASS = {"Li": 6.94, "P": 30.973761998, "S": 32.06}


def window_msd(positions: np.ndarray) -> np.ndarray:
    """Return the time-origin-averaged MSD for shape (time, atom, xyz)."""
    x = np.asarray(positions, dtype=float)
    x = x - x[0]
    n = len(x)
    f = np.fft.rfft(x, n=2 * n, axis=0)
    corr = np.fft.irfft(f * f.conjugate(), n=2 * n, axis=0)[:n].sum(axis=(1, 2))
    squared_sum = np.r_[0.0, np.cumsum((x * x).sum(axis=(1, 2)))]
    lag = np.arange(n)
    msd = (
        squared_sum[n - lag]
        + squared_sum[n]
        - squared_sum[lag]
        - 2.0 * corr
    ) / ((n - lag) * x.shape[1])
    msd[0] = 0.0
    return msd


def unwrap(positions: np.ndarray, cell: np.ndarray) -> np.ndarray:
    fractional = positions @ np.linalg.inv(cell)
    delta = np.diff(fractional, axis=0)
    delta -= np.round(delta)
    return np.concatenate([positions[:1], positions[:1] + np.cumsum(delta @ cell, axis=0)])


def fit_msd(time_ps: np.ndarray, msd_a2: np.ndarray, lo: float, hi: float) -> dict:
    mask = (time_ps >= lo) & (time_ps <= hi)
    fit = linregress(time_ps[mask], msd_a2[mask])
    positive = mask & (time_ps > 0) & (msd_a2 > 0)
    alpha = linregress(np.log(time_ps[positive]), np.log(msd_a2[positive])).slope
    return {
        "lo_ps": lo,
        "hi_ps": hi,
        "D_cm2_s": float(fit.slope / 6.0e4),
        "R2": float(fit.rvalue**2),
        "alpha": float(alpha),
        "intercept_A2": float(fit.intercept),
    }


def p_centered_angles(vectors: np.ndarray) -> np.ndarray:
    """Return all unique angles between P-to-S neighbour vectors in degrees."""
    vectors = np.asarray(vectors, dtype=float)
    if len(vectors) < 2:
        return np.empty(0)
    unit = vectors / np.linalg.norm(vectors, axis=1)[:, None]
    i, j = np.triu_indices(len(unit), 1)
    cosine = np.clip(np.sum(unit[i] * unit[j], axis=1), -1.0, 1.0)
    return np.degrees(np.arccos(cosine))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def frame_structure(atoms, symbols: np.ndarray, edges: np.ndarray) -> tuple:
    distances = atoms.get_all_distances(mic=True)
    np.fill_diagonal(distances, np.inf)
    volume = atoms.get_volume()
    shell = 4.0 * np.pi / 3.0 * np.diff(edges**3)
    rdf = []
    coordination = []
    for first, second, cutoff in (("Li", "S", 3.2), ("P", "S", 2.6)):
        selected = distances[np.ix_(symbols == first, symbols == second)]
        n_first = int(np.sum(symbols == first))
        n_second = int(np.sum(symbols == second))
        rdf.append(np.histogram(selected, edges)[0] * volume / (n_first * n_second * shell))
        coordination.append(float(np.mean(np.sum(selected < cutoff, axis=1))))

    p_indices = np.flatnonzero(symbols == "P")
    s_indices = np.flatnonzero(symbols == "S")
    p_coordination = []
    angles = []
    for p_index in p_indices:
        vectors = atoms.get_distances(p_index, s_indices, mic=True, vector=True)
        neighbours = vectors[np.linalg.norm(vectors, axis=1) < 2.6]
        p_coordination.append(len(neighbours))
        angles.extend(p_centered_angles(neighbours))
    return (
        np.asarray(rdf),
        np.asarray(coordination),
        np.asarray(p_coordination),
        np.asarray(angles),
        float(np.min(distances)),
    )


def analyse_temperature(run_dir: Path, output: Path, temperature: int) -> dict:
    assert (run_dir / "completed.txt").exists()
    production = run_dir / "production"
    model = read(production / "model.xyz")
    symbols = np.asarray(model.get_chemical_symbols())
    assert Counter(symbols) == Counter(Li=192, P=64, S=256)
    frames = list(iread(production / "dump.xyz"))
    assert len(frames) == 2000
    assert all(np.array_equal(symbols, frame.get_chemical_symbols()) for frame in frames)
    assert all(np.allclose(model.cell.array, frame.cell.array, atol=1e-7) for frame in frames)

    times = np.asarray([frame.info["Time"] for frame in frames]) / 1000.0
    np.testing.assert_allclose(times, np.arange(1, 2001) * 0.1, atol=1e-7)
    positions = np.asarray([model.positions] + [frame.positions for frame in frames])
    unwrapped = unwrap(positions, model.cell.array)
    masses = np.asarray([MASS[element] for element in symbols])
    com = np.average(unwrapped, axis=1, weights=masses)
    corrected = unwrapped - com[:, None, :]
    time_ps = np.arange(2001) * 0.1
    msd = {element: window_msd(corrected[:, symbols == element]) for element in ("Li", "P", "S")}
    for lag in (10, 200, 800):
        direct = np.mean(
            np.sum(
                (corrected[lag:, symbols == "Li"] - corrected[:-lag, symbols == "Li"]) ** 2,
                axis=2,
            )
        )
        np.testing.assert_allclose(msd["Li"][lag], direct, atol=1e-7)

    fits = [fit_msd(time_ps, msd["Li"], *window) for window in WINDOWS]
    np.savetxt(
        output / f"{temperature}K_MSD.csv",
        np.column_stack([time_ps, msd["Li"], msd["P"], msd["S"]]),
        delimiter=",",
        header="lag_ps,Li_A2,P_A2,S_A2",
        comments="",
    )

    edges = np.arange(0.0, 5.0001, 0.05)
    radius = (edges[:-1] + edges[1:]) / 2.0
    angle_edges = np.arange(60.0, 180.0001, 2.0)
    angle_centres = (angle_edges[:-1] + angle_edges[1:]) / 2.0
    structure = {}
    for label, indices in (
        ("early", range(0, 500, 25)),
        ("late", range(1500, 2000, 25)),
    ):
        rdf_values = []
        coordination_values = []
        p_cn_values = []
        angle_values = []
        minimum_distances = []
        for index in indices:
            rdf, coordination, p_cn, angles, minimum = frame_structure(
                frames[index], symbols, edges
            )
            rdf_values.append(rdf)
            coordination_values.append(coordination)
            p_cn_values.extend(p_cn)
            angle_values.extend(angles)
            minimum_distances.append(minimum)
        rdf_mean = np.mean(rdf_values, axis=0)
        angle_hist, _ = np.histogram(angle_values, angle_edges, density=True)
        np.savetxt(
            output / f"{temperature}K_{label}_structure.csv",
            np.column_stack([radius, rdf_mean.T]),
            delimiter=",",
            header="r_A,Li_S_g_r,P_S_g_r",
            comments="",
        )
        np.savetxt(
            output / f"{temperature}K_{label}_angles.csv",
            np.column_stack([angle_centres, angle_hist]),
            delimiter=",",
            header="angle_deg,S_P_S_density",
            comments="",
        )
        p_cn_values = np.asarray(p_cn_values)
        structure[label] = {
            "CN_Li_S": float(np.mean(np.asarray(coordination_values)[:, 0])),
            "CN_P_S": float(np.mean(np.asarray(coordination_values)[:, 1])),
            "P_four_S_fraction": float(np.mean(p_cn_values == 4)),
            "S_P_S_mean_deg": float(np.mean(angle_values)),
            "minimum_pair_A": float(np.min(minimum_distances)),
            "sampled_frames": len(list(indices)),
        }

    stages = {}
    expected_rows = {"ramp": 200, "equil": 1000, "production": 4000}
    for stage, expected in expected_rows.items():
        thermo = np.loadtxt(run_dir / stage / "thermo.out")
        assert thermo.shape == (expected, 18) and np.isfinite(thermo).all()
        volume = np.linalg.det(thermo[:, 9:].reshape(-1, 3, 3))
        density = model.get_masses().sum() * 1.6605390666 / volume
        quarter = expected // 4
        stages[stage] = {
            "mean_T_K": float(np.mean(thermo[:, 0])),
            "mean_P_GPa": float(np.mean(thermo[:, 3:6])),
            "mean_density_g_cm3": float(np.mean(density)),
            "density_last_minus_first_percent": float(
                (np.mean(density[-quarter:]) / np.mean(density[:quarter]) - 1.0) * 100.0
            ),
            "PE_last_minus_first_meV_atom": float(
                (np.mean(thermo[-quarter:, 2]) - np.mean(thermo[:quarter, 2]))
                / len(model)
                * 1000.0
            ),
        }

    return {
        "temperature_K": temperature,
        "n_atoms": len(model),
        "n_production_frames": len(frames),
        "production_duration_ps": float(time_ps[-1]),
        "fits": fits,
        "MSD80_A2": {element: float(values[800]) for element, values in msd.items()},
        "MSD150_A2": {element: float(values[1500]) for element, values in msd.items()},
        "structure": structure,
        "stages": stages,
        "max_COM_displacement_A": float(np.max(np.linalg.norm(com - com[0], axis=1))),
        "source_sha256": {
            "model.xyz": sha256(production / "model.xyz"),
            "dump.xyz": sha256(production / "dump.xyz"),
            "thermo.out": sha256(production / "thermo.out"),
        },
    }


def run(root: Path, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    results = {}
    for temperature in TEMPERATURES:
        run_dir = root / f"r1_transport_{temperature}K_8679199"
        results[str(temperature)] = analyse_temperature(run_dir, output, temperature)
        print(f"analysed {temperature} K", flush=True)

    with (output / "fit_windows.csv").open("w") as handle:
        handle.write("T_K,lo_ps,hi_ps,D_cm2_s,R2,alpha,intercept_A2\n")
        for temperature in TEMPERATURES:
            for fit in results[str(temperature)]["fits"]:
                handle.write(
                    f"{temperature},{fit['lo_ps']},{fit['hi_ps']},{fit['D_cm2_s']:.12e},"
                    f"{fit['R2']:.9f},{fit['alpha']:.9f},{fit['intercept_A2']:.12e}\n"
                )

    selected = []
    for temperature in TEMPERATURES:
        selected.append(results[str(temperature)]["fits"][2])
    high_temperature = np.asarray(TEMPERATURES[1:], dtype=float)
    high_d = np.asarray([selected[index]["D_cm2_s"] for index in range(1, 4)])
    arrhenius = linregress(1.0 / high_temperature, np.log(high_d))
    summary = {
        "definition": "time-origin averaged, whole-system COM-corrected species MSD",
        "selected_common_window_ps": [20, 80],
        "results": results,
        "high_temperature_diagnostic": {
            "range_K": [500, 700, 900],
            "Ea_eV": float(-arrhenius.slope * 8.617333262145e-5),
            "R2": float(arrhenius.rvalue**2),
            "status": "diagnostic; 300 K excluded and no room-temperature extrapolation",
        },
    }
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    run(arguments.root, arguments.output)


if __name__ == "__main__":
    main()
