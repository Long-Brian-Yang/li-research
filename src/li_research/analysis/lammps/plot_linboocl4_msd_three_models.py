"""Plot the publication LiNbOCl4 three-model MSD comparison.

The canvas and typography deliberately match the corresponding Li3YCl6
triptych so the two figures render at the same proportion in the material
review.  The trajectories are the sources used by the existing publication
figure; this script changes presentation only.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[4]
FIGSIZE = (18.0, 6.2)
DPI = 300
TEMPERATURES = (600, 800, 1000, 1200)
COLORS = ("#1f77b4", "#2fb47c", "#e3362d", "#8c2d04")

SOURCES = {
    "MACE-MPA-0": (
        ROOT / "runs/md/mace_mpa0_medium/LiNbOCl4_2x2x3/600K/replica_2/8487891.2_20260825_092110/msd_li.dat",
        ROOT / "runs/md/mace_mpa0_medium/LiNbOCl4_2x2x3/800K/replica_1/8487891.4_20260825_133741/msd_li.dat",
        ROOT / "runs/md/mace_mpa0_medium/LiNbOCl4_2x2x3/1000K/replica_3/8487891.9_20260825_182906/msd_li.dat",
        ROOT / "runs/md/mace_mpa0_medium/LiNbOCl4_2x2x3/1200K/replica_3/8487891.12_20260826_000142/msd_li.dat",
    ),
    "SevenNet-nano": (
        ROOT / "runs/md/sevennet_nano_55/LiNbOCl4_2x2x3/600K/replica_1/8487892.1_20260825_092114/msd_li.dat",
        ROOT / "runs/md/sevennet_nano_55/LiNbOCl4_2x2x3/800K/replica_1/8487892.4_20260825_111237/msd_li.dat",
        ROOT / "runs/md/sevennet_nano_55/LiNbOCl4_2x2x3/1000K/replica_3/8487892.9_20260825_133601/msd_li.dat",
        ROOT / "runs/md/sevennet_nano_55/LiNbOCl4_2x2x3/1200K/replica_3/8487892.12_20260825_155204/msd_li.dat",
    ),
    "M3GNet": (
        ROOT / "runs/md/m3gnet_matgl_gpu/LiNbOCl4_2x2x3/600K/replica_2/8487893.2_20260825_092111/msd_li.dat",
        ROOT / "runs/md/m3gnet_matgl_gpu/LiNbOCl4_2x2x3/800K/replica_3/8498445.3_20260826_074330/msd_li.dat",
        ROOT / "runs/md/m3gnet_matgl_gpu/LiNbOCl4_2x2x3/1000K/replica_1/8487893.7_20260825_160954/msd_li.dat",
        ROOT / "runs/md/m3gnet_matgl_gpu/LiNbOCl4_2x2x3/1200K/replica_2/8487893.11_20260825_202445/msd_li.dat",
    ),
}

OUTPUT_PNGS = (
    ROOT / "results/publication_all_materials/main/LiNbOCl4_MSD_4T_all_models.png",
    ROOT / "docs/materials/figures/02_LiNbOCl4_three_model_MSD.png",
)


def load_msd(path: Path) -> tuple[np.ndarray, np.ndarray]:
    data = np.loadtxt(path, comments="#")
    return data[:, 0] * 0.001, data[:, 4]


def build_figure():
    fig, axes = plt.subplots(1, 3, figsize=FIGSIZE, constrained_layout=True)
    for ax, (model, paths) in zip(axes, SOURCES.items()):
        for temperature, path, color in zip(TEMPERATURES, paths, COLORS):
            time_ps, msd = load_msd(path)
            ax.plot(time_ps, msd, color=color, lw=3.0, label=f"{temperature} K")
        ax.set_title(model, fontsize=22, pad=10)
        ax.set_xlabel("Time (ps)", fontsize=19)
        ax.grid(True, alpha=0.25)
        ax.tick_params(labelsize=15)
        ax.legend(frameon=False, fontsize=15, loc="upper left")
        for spine in ax.spines.values():
            spine.set_linewidth(1.8)
            spine.set_color("black")
    axes[0].set_ylabel(r"MSD ($\mathrm{\AA}^2$)", fontsize=19)
    fig.suptitle(r"LiNbOCl$_4$ — lithium-ion diffusion comparison", fontsize=25)
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
