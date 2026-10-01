"""Plot every available LiNbOCl4 MSD trajectory for three models and four temperatures."""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))
from li_research.analysis.lammps.linboocl4_all_replicas import (
    MODELS, TEMPERATURES, discover_tracks,
)


FIGSIZE = (18.0, 6.2)
DPI = 300
SOURCES = MODELS
COLORS = ("#1f77b4", "#2fb47c", "#e3362d", "#8c2d04")
OUTPUT_PNGS = (
    ROOT / "results/publication_all_materials/main/LiNbOCl4_MSD_4T_all_models.png",
    ROOT / "docs/materials/figures/02_LiNbOCl4_three_model_MSD.png",
)


def load_msd(path):
    data = np.loadtxt(path, comments="#")
    if data.ndim != 2 or data.shape[1] < 5 or not np.isfinite(data[:, [0, 4]]).all():
        raise ValueError(f"Invalid MSD data: {path}")
    return data[:, 0] * 0.001, data[:, 4]


def build_figure():
    fig, axes = plt.subplots(1, 3, figsize=FIGSIZE, constrained_layout=True)
    for ax, (model, directory) in zip(axes, SOURCES.items()):
        for temperature, color in zip(TEMPERATURES, COLORS):
            paths = discover_tracks(directory, temperature)
            if not paths:
                raise FileNotFoundError(f"No LiNbOCl4 MSD tracks for {model} at {temperature} K")
            for path in paths:
                time_ps, msd = load_msd(path)
                ax.plot(time_ps, msd, color=color, lw=1.5, alpha=0.40)
            ax.plot([], [], color=color, lw=2.4, label=f"{temperature} K")
        ax.set_title(model, fontsize=22, pad=10)
        ax.set_xlabel("Time (ps)", fontsize=19)
        ax.grid(True, alpha=0.25)
        ax.tick_params(labelsize=15)
        ax.legend(frameon=False, fontsize=15, loc="upper left")
        for spine in ax.spines.values():
            spine.set_linewidth(1.8)
            spine.set_color("black")
    axes[0].set_ylabel(r"MSD ($\mathrm{\AA}^2$)", fontsize=19)
    fig.suptitle(r"LiNbOCl$_4$ — lithium-ion mean-squared displacement", fontsize=25)
    return fig


def main() -> None:
    fig = build_figure()
    for output in OUTPUT_PNGS:
        output.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output, dpi=DPI, facecolor="white")
        print(output)
    plt.close(fig)


if __name__ == "__main__":
    main()
