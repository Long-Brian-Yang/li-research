#!/usr/bin/env python3
"""Analyze Li jump statistics from comparable LAMMPS trajectories.

The first-pass definition is deliberately explicit: a jump is a Li displacement
of >= threshold over one saved frame (1 ps for the supplied trajectories).
Residence time is the interval between successive detected jumps.  This is a
dynamic residence proxy, not a crystallographic site-occupancy measurement.
"""
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "results/midterm_Li3YCl6_MACE_M3GNet/plots/supplementary_priority"
OUT.mkdir(parents=True, exist_ok=True)
TRAJ = {
    "MACE-MPA-0": ROOT / "runs/md/mace_mpa0_medium/Li3YCl6_03_2x2x2/600K/replica_3/8477947.9_20260825_003119/trajectory.lammpstrj",
    "SevenNet-nano": ROOT / "runs/md/sevennet_nano_55/Li3YCl6_03_2x2x2/600K/replica_2/8477949.8_20260824_185237/trajectory.lammpstrj",
    "M3GNet": ROOT / "runs/md/m3gnet_matgl_gpu/Li3YCl6_03_2x2x2/600K/replica_2/8486065.2_20260825_050347/trajectory.lammpstrj",
}
TYPE_LI = 1
FRAME_DT_PS = 1.0
JUMP_THRESHOLD_A = 1.5

def read_dump(path):
    frames, times = [], []
    with path.open() as fh:
        while True:
            line = fh.readline()
            if not line:
                break
            if not line.startswith("ITEM: TIMESTEP"):
                continue
            timestep = int(fh.readline())
            assert fh.readline().startswith("ITEM: NUMBER OF ATOMS")
            n = int(fh.readline())
            assert fh.readline().startswith("ITEM: BOX BOUNDS")
            for _ in range(3): fh.readline()
            header = fh.readline().split()[2:]
            rows = [fh.readline().split() for _ in range(n)]
            idx = {name: i for i, name in enumerate(header)}
            ids = np.array([int(r[idx["id"]]) for r in rows])
            types = np.array([int(r[idx["type"]]) for r in rows])
            order = np.argsort(ids)
            xyz = np.array([[float(r[idx[k]]) for k in ("xu", "yu", "zu")] for r in rows])[order]
            if not frames:
                li = types[order] == TYPE_LI
            frames.append(xyz[li])
            times.append(timestep * 0.001)  # 1 fs timestep -> ps
    return np.asarray(times), np.asarray(frames)

def analyze(times, xyz):
    disp = np.linalg.norm(xyz[1:] - xyz[:-1], axis=2)
    events = disp >= JUMP_THRESHOLD_A
    jump_dist = disp[events]
    n_li = xyz.shape[1]
    duration = times[-1] - times[0]
    freq = events.sum() / (n_li * duration) if duration else np.nan
    waits = []
    for j in range(n_li):
        event_idx = np.flatnonzero(events[:, j])
        if len(event_idx) > 1:
            waits.extend(np.diff(event_idx) * FRAME_DT_PS)
    return jump_dist, float(freq), np.asarray(waits)

def main():
    summaries, all_data = [], {}
    for model, path in TRAJ.items():
        times, xyz = read_dump(path)
        jumps, freq, waits = analyze(times, xyz)
        all_data[model] = (jumps, waits)
        summaries.append({
            "model": model, "n_frames": len(times), "n_li": xyz.shape[1],
            "frame_dt_ps": FRAME_DT_PS, "threshold_A": JUMP_THRESHOLD_A,
            "total_time_ps": times[-1] - times[0], "jump_events": len(jumps),
            "jump_frequency_events_per_Li_ps": freq,
            "mean_jump_distance_A": np.mean(jumps) if len(jumps) else np.nan,
            "median_jump_distance_A": np.median(jumps) if len(jumps) else np.nan,
            "mean_residence_time_ps": np.mean(waits) if len(waits) else np.nan,
            "median_residence_time_ps": np.median(waits) if len(waits) else np.nan,
            "n_residence_intervals": len(waits),
        })
    csv_path = OUT / "Li3YCl6_jump_residence_600K_all_models.csv"
    with csv_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=summaries[0].keys()); writer.writeheader(); writer.writerows(summaries)

    plt.style.use("default")
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.7), constrained_layout=True)
    colors = {"MACE-MPA-0":"#1f77b4", "SevenNet-nano":"#2ca25f", "M3GNet":"#d62728"}
    for model, (jumps, waits) in all_data.items():
        c = colors[model]
        if len(jumps): axes[0].hist(jumps, bins=np.linspace(0, 5, 31), density=True, histtype="step", linewidth=2.2, color=c, label=model)
        s = next(x for x in summaries if x["model"] == model)
        axes[1].bar(model, s["jump_frequency_events_per_Li_ps"], color=c, alpha=0.85)
        if len(waits): axes[2].hist(waits, bins=np.arange(0.5, min(max(waits.max(), 4), 20)+0.5, 1), density=True, histtype="step", linewidth=2.2, color=c, label=model)
    axes[0].set(xlabel="One-frame Li displacement (Å)", ylabel="Probability density", title="Jump-distance distribution")
    axes[1].set(xlabel="Model", ylabel="Events Li$^{-1}$ ps$^{-1}$", title="Jump frequency")
    axes[2].set(xlabel="Residence interval (ps)", ylabel="Probability density", title="Residence-time proxy")
    axes[0].legend(frameon=False, fontsize=10); axes[2].legend(frameon=False, fontsize=10)
    for ax in axes:
        ax.tick_params(labelsize=10); ax.grid(True, alpha=.25); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.suptitle("Li$_3$YCl$_6$ — Li-jump analysis at 600 K", fontsize=16)
    fig.savefig(OUT / "Li3YCl6_jump_residence_600K_all_models.png", dpi=300, facecolor="white")
    print(csv_path); print(OUT / "Li3YCl6_jump_residence_600K_all_models.png")

if __name__ == "__main__": main()
