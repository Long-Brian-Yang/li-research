#!/usr/bin/env python3
"""Create compact reference-cell/supercell structure views for the daily report."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from ase.io import read

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

CASES = [
    (
        "Li₃YCl₆ model 03",
        ROOT / "structures/ordered/Li3YCl6/2x2x2/model_03/Li3YCl6_ordered_03_2x2x2.cif",
        ROOT / "structures/ordered/Li3YCl6/2x2x4/model_03/Li3YCl6_ordered_03_2x2x4.cif",
        "reference ordered cell (2×2×2)",
        "production supercell (2×2×4)",
    ),
    (
        "LiNbOCl₄",
        ROOT / "structures/reference/photo_reconstructed/LiNbOCl4_photo_reconstructed.cif",
        ROOT / "structures/ordered/LiNbOCl4/2x2x3/LiNbOCl4_ordered_2x2x3.cif",
        "screenshot-reconstructed reference cell",
        "ordered follow-up supercell (2×2×3)",
    ),
]

COLORS = {"Li": "#b35cdb", "Y": "#3b82f6", "Nb": "#2563eb", "O": "#e53935", "Cl": "#22a06b"}
SIZES = {"Li": 22, "Y": 58, "Nb": 58, "O": 42, "Cl": 48}


def draw_cell(ax, atoms, origin):
    cell = np.asarray(atoms.cell.array)
    corners = [origin, cell[0], cell[1], cell[2], cell[0] + cell[1], cell[0] + cell[2], cell[1] + cell[2], cell.sum(axis=0)]
    edges = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 4), (2, 6), (3, 5), (3, 6), (4, 7), (5, 7), (6, 7)]
    for i, j in edges:
        ax.plot([corners[i][0], corners[j][0]], [corners[i][1], corners[j][1]], [corners[i][2], corners[j][2]], color="#777777", lw=0.45, alpha=0.65)


def panel(ax, atoms, label):
    positions = atoms.get_positions()
    center = positions.mean(axis=0)
    positions = positions - center
    symbols = atoms.get_chemical_symbols()
    for element in sorted(set(symbols), key=lambda x: list(COLORS).index(x)):
        mask = np.array([s == element for s in symbols])
        ax.scatter(positions[mask, 0], positions[mask, 1], positions[mask, 2], s=SIZES[element], c=COLORS[element], alpha=0.82, edgecolors="white", linewidths=0.25, label=element)
    # Translate cell edges to the same centered coordinate frame.
    old_positions = atoms.get_positions().copy()
    atoms.set_positions(old_positions - center)
    draw_cell(ax, atoms, -center)
    atoms.set_positions(old_positions)
    ax.set_title(f"{label}\n{len(atoms)} atoms", fontsize=10)
    ax.set_xlabel("x (Å)", fontsize=8)
    ax.set_ylabel("y (Å)", fontsize=8)
    ax.set_zlabel("z (Å)", fontsize=8)
    ax.tick_params(labelsize=6)
    ax.view_init(elev=20, azim=35)


fig = plt.figure(figsize=(14, 7.5), dpi=180)
for row, (name, ref_path, super_path, ref_label, super_label) in enumerate(CASES):
    ref = read(ref_path)
    sup = read(super_path)
    ax1 = fig.add_subplot(2, 2, 2 * row + 1, projection="3d")
    ax2 = fig.add_subplot(2, 2, 2 * row + 2, projection="3d")
    panel(ax1, ref, f"{name}: {ref_label}")
    panel(ax2, sup, f"{name}: {super_label}")
    if row == 0:
        handles = [Line2D([0], [0], marker="o", color="w", label=element,
                          markerfacecolor=COLORS[element], markersize=7)
                   for element in ["Li", "Y", "Nb", "O", "Cl"]]
        fig.legend(handles, [h.get_label() for h in handles], loc="lower center",
                   bbox_to_anchor=(0.5, 0.005), ncol=len(handles), frameon=False, fontsize=9)

fig.suptitle("Direction 2: reference cells and MD supercells", fontsize=14, y=0.99)
fig.tight_layout(rect=[0, 0.04, 1, 0.95])
fig.savefig(OUT / "structure_reference_vs_supercell_ja.png", bbox_inches="tight")
print(OUT / "structure_reference_vs_supercell_ja.png")
