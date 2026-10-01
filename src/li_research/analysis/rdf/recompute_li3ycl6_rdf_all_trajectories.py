"""Recompute 600 K Li3YCl6 RDFs from every available matched production run.

No individual trajectory is chosen by its numerical result. Every discovered
50 ps-equilibration/500 ps-production source is exported, with the per-model
mean shown separately. The historical source tree contains MACE runs; current
model-specific trees are searched for every model.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import MDAnalysis as mda
from MDAnalysis.analysis.rdf import InterRDF
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
RUN_ROOT = ROOT / "runs/md"
MODEL_DIRS = {
    "MACE-MPA-0": "mace_mpa0_medium",
    "SevenNet-nano": "sevennet_nano_55",
    "M3GNet": "m3gnet_matgl_gpu",
}
PAIRS = {"Li-Cl": ("1", "3"), "Y-Cl": ("2", "3"), "Cl-Cl": ("3", "3")}
COLORS = {"MACE-MPA-0": "#1f77b4", "SevenNet-nano": "#2ca02c", "M3GNet": "#d62728"}
OUT = ROOT / "results/midterm_Li3YCl6_MACE_M3GNet/plots"


def discover(model: str) -> list[Path]:
    current = RUN_ROOT / MODEL_DIRS[model] / "Li3YCl6_03_2x2x2" / "600K"
    paths = set(current.glob("replica_*/*/trajectory.lammpstrj"))
    if model == "MACE-MPA-0":
        history = RUN_ROOT / "history/md_runs"
        paths.update(history.glob("*50ps_eq_500ps*/Li3YCl6_03/Li3YCl6_03_600K_prod.lammpstrj"))
    return sorted(path for path in paths if path.is_file())


def rdf(path: Path, atom_types: tuple[str, str]) -> tuple[np.ndarray, np.ndarray]:
    universe = mda.Universe(str(path), format="LAMMPSDUMP")
    first, second = (universe.select_atoms(f"type {value}") for value in atom_types)
    analysis = InterRDF(first, second, nbins=120, range=(0.0, 6.0), norm="rdf")
    analysis.run(start=50, stop=universe.trajectory.n_frames, step=1)
    return np.asarray(analysis.results.bins), np.asarray(analysis.results.rdf)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    all_curves = {}
    for model in MODEL_DIRS:
        paths = discover(model)
        if not paths:
            raise FileNotFoundError(f"No 600 K production trajectory found for {model}")
        all_curves[model] = {pair: [rdf(path, types) for path in paths] for pair, types in PAIRS.items()}

    for pair in PAIRS:
        fig, ax = plt.subplots(figsize=(8.8, 5.8667), dpi=180)
        for model, pair_curves in all_curves.items():
            curves = pair_curves[pair]
            radii = curves[0][0]
            values = np.asarray([curve[1] for curve in curves])
            for curve in values:
                ax.plot(radii, curve, lw=1.2, color=COLORS[model], alpha=0.28)
            mean = values.mean(axis=0)
            ax.plot(radii, mean, lw=3.0, color=COLORS[model], label=f"{model} (n={len(curves)})")
            np.savetxt(
                OUT / f"Li3YCl6_{pair.replace('-', '')}_RDF_600K_{model.replace('-', '_')}_all.csv",
                np.column_stack([radii, values.mean(axis=0), values.std(axis=0, ddof=1) if len(values) > 1 else np.zeros(len(radii))]),
                delimiter=",", header="r_A,g_r_mean,g_r_sample_sd", comments="",
            )
        ax.set_title(f"Li$_3$YCl$_6$ — {pair} RDF at 600 K", fontsize=22, pad=12)
        ax.set_xlabel("Distance r (Å)", fontsize=19)
        ax.set_ylabel("g(r)", fontsize=19)
        ax.tick_params(labelsize=15, width=1.5, length=6)
        for spine in ax.spines.values():
            spine.set_linewidth(1.5)
        ax.grid(True, alpha=0.22)
        ax.legend(fontsize=13, loc="upper right", frameon=False)
        fig.tight_layout()
        fig.savefig(OUT / f"Li3YCl6_{pair.replace('-', '')}_RDF_600K_all_models_all_runs.png")
        plt.close(fig)


if __name__ == "__main__":
    main()
