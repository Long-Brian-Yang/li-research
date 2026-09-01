"""Recompute Li3YCl6 RDFs from selected 600 K LAMMPS trajectories.

Uses MDAnalysis' periodic-boundary-aware InterRDF on the production part of
each trajectory (frames 50--500), avoiding the old sparse histogram workflow.
LAMMPS atom types are 1=Li, 2=Y, 3=Cl.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import MDAnalysis as mda
from MDAnalysis.analysis.rdf import InterRDF
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
TRAJECTORIES = {
    # Use the original smooth 600 K MACE production trajectory that defined
    # the midterm two-model RDF baseline; SevenNet is added to that baseline.
    "MACE-MPA-0": ROOT / "runs/md/history/md_runs/selected_600K_50ps_eq_500ps_20260823_054114/Li3YCl6_03/Li3YCl6_03_600K_prod.lammpstrj",
    "SevenNet-nano": ROOT / "runs/md/sevennet_nano_55/Li3YCl6_03_2x2x2/600K/replica_2/8477949.8_20260824_185237/trajectory.lammpstrj",
    "M3GNet": ROOT / "runs/md/m3gnet_matgl_gpu/Li3YCl6_03_2x2x2/600K/replica_2/8486065.2_20260825_050347/trajectory.lammpstrj",
}
PAIRS = {"Li-Cl": ("1", "3"), "Y-Cl": ("2", "3"), "Cl-Cl": ("3", "3")}
COLORS = {"MACE-MPA-0": "#1f77b4", "SevenNet-nano": "#2ca02c", "M3GNet": "#d62728"}
OUT = ROOT / "results/midterm_Li3YCl6_MACE_M3GNet/plots"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for pair_name, (a_type, b_type) in PAIRS.items():
        fig, ax = plt.subplots(figsize=(8.8, 5.8667), dpi=180)
        for model, path in TRAJECTORIES.items():
            u = mda.Universe(str(path), format="LAMMPSDUMP")
            ag1 = u.select_atoms(f"type {a_type}")
            ag2 = u.select_atoms(f"type {b_type}")
            rdf = InterRDF(ag1, ag2, nbins=120, range=(0.0, 6.0), norm="rdf")
            rdf.run(start=50, stop=u.trajectory.n_frames, step=1)
            ax.plot(rdf.results.bins, rdf.results.rdf, lw=3.4, color=COLORS[model], label=model)
            np.savetxt(OUT / f"Li3YCl6_{pair_name.replace('-', '')}_RDF_600K_{model.replace('-', '_')}.csv",
                       np.column_stack([rdf.results.bins, rdf.results.rdf]), delimiter=",", header="r_A,g_r", comments="")
        ax.set_title(f"Li$_3$YCl$_6$ — {pair_name} RDF at 600 K", fontsize=22, pad=12)
        ax.set_xlabel("Distance r (Å)", fontsize=19)
        ax.set_ylabel("g(r)", fontsize=19)
        ax.tick_params(labelsize=15, width=1.5, length=6)
        for spine in ax.spines.values():
            spine.set_linewidth(1.5)
        ax.grid(True, alpha=0.22)
        ax.legend(fontsize=13, loc="upper right", frameon=False)
        fig.tight_layout()
        fig.savefig(OUT / f"Li3YCl6_{pair_name.replace('-', '')}_RDF_600K_all_models.png")
        plt.close(fig)


if __name__ == "__main__":
    main()
