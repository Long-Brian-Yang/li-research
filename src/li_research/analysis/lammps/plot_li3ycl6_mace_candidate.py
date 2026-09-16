"""Plot the MACE Li3YCl6 candidate four-temperature MSD set."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[4]
RUNS = ROOT / "runs/md"
OUT = ROOT / "results/analysis/Li3YCl6/Li3YCl6_MACE_MSD_400_600_800_1000_selected.png"

FILES = {
    400: RUNS / "mace_mpa0_medium/Li3YCl6_03_2x2x2/400K/replica_3/8477947.3_20260824_151947/msd_li.dat",
    600: RUNS / "mace_mpa0_medium/Li3YCl6_03_2x2x2/600K/replica_3/8477947.9_20260825_003119/msd_li.dat",
    800: RUNS / "mace_mpa0_medium/Li3YCl6_03_2x2x2/800K/replica_2/8477947.14_20260825_083700/msd_li.dat",
    1000: RUNS / "mace_mpa0_medium/Li3YCl6_03_2x2x2/1000K/replica_1/8502119.1_20260826_154501/msd_li.dat",
}


def read_total_msd(path: Path) -> tuple[np.ndarray, np.ndarray]:
    rows = []
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        fields = line.split()
        if len(fields) >= 5:
            rows.append((float(fields[0]) * 0.001, float(fields[4])))
    data = np.asarray(rows)
    return data[:, 0], data[:, 1]


def main() -> None:
    colors = {400: "#4C78A8", 600: "#F2A541", 800: "#59A14F", 1000: "#D1495B"}
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 12,
        "axes.linewidth": 1.2,
        "xtick.direction": "in",
        "ytick.direction": "in",
    })
    fig, ax = plt.subplots(figsize=(7.2, 4.8), dpi=180)
    for temperature in (400, 600, 800, 1000):
        time_ps, msd = read_total_msd(FILES[temperature])
        ax.plot(time_ps, msd, color=colors[temperature], lw=2.2, label=f"{temperature} K")
    ax.set_xlabel("Time (ps)")
    ax.set_ylabel(r"Li MSD ($\mathrm{\AA^2}$)")
    ax.set_title("Li$_3$YCl$_6$ — MACE-MPA-0 MSD")
    ax.grid(True, color="#D9D9D9", lw=0.7, alpha=0.65)
    ax.legend(frameon=False, ncol=4, loc="upper left")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300, bbox_inches="tight")
    print(OUT)


if __name__ == "__main__":
    main()
