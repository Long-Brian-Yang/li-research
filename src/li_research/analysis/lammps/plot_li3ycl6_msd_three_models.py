"""Plot raw Li3YCl6 MSD data from every matching stored run per model/temperature."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[4]
RUN_ROOT = ROOT / "runs/md"
OUT = ROOT / "results/midterm_Li3YCl6_MACE_M3GNet/plots/Li3YCl6_MSD_4T_all_models.png"
MODELS = {
    "MACE-MPA-0": "mace_mpa0_medium",
    "SevenNet-nano": "sevennet_nano_55",
    "M3GNet": "m3gnet_matgl_gpu",
}
TEMPERATURES = (400, 600, 800, 1000)
COLORS = ("#482878", "#31688e", "#35b779", "#d73027")


def discover_tracks(model_directory, temperature):
    root = RUN_ROOT / model_directory / "Li3YCl6_03_2x2x2" / f"{temperature}K"
    return sorted(root.glob("replica_*/*/msd_li.dat"))


def main():
    fig, axes = plt.subplots(1, 3, figsize=(18, 6.2), sharey=True, constrained_layout=True)
    global_max = 0.0
    found = 0
    for ax, (model, directory) in zip(axes, MODELS.items()):
        for temperature, color in zip(TEMPERATURES, COLORS):
            files = discover_tracks(directory, temperature)
            if not files:
                continue
            for path in files:
                data = np.loadtxt(path, comments="#")
                if data.ndim != 2 or data.shape[1] < 5 or not np.isfinite(data[:, [0, 4]]).all():
                    raise ValueError(f"Invalid raw MSD data: {path}")
                time_ps = data[:, 0] * 0.001
                msd = data[:, 4]
                ax.plot(time_ps, msd, color=color, lw=1.5, alpha=0.42)
                global_max = max(global_max, float(np.max(msd)))
                found += 1
            ax.plot([], [], color=color, lw=2.5, label=f"{temperature} K")
        ax.set_title(model, fontsize=22, pad=10)
        ax.set_xlabel("Time (ps)", fontsize=19)
        ax.grid(True, alpha=0.25)
        ax.tick_params(labelsize=15)
        ax.legend(frameon=False, fontsize=15, loc="upper left")
        for spine in ax.spines.values():
            spine.set_linewidth(1.8)
            spine.set_color("black")
    if found == 0:
        raise FileNotFoundError(f"No Li3YCl6 MSD files discovered under {RUN_ROOT}")
    axes[0].set_ylabel("MSD (Å²)", fontsize=19)
    upper = np.ceil(global_max * 1.08 / 100.0) * 100.0
    for ax in axes:
        ax.set_ylim(0, upper)
    fig.suptitle("Li₃YCl₆ — lithium-ion mean-squared displacement", fontsize=25)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300, facecolor="white")
    plt.close(fig)
    print(f"Wrote {OUT} from {found} unscaled trajectories")


if __name__ == "__main__":
    main()
