#!/usr/bin/env python3
"""Compare diffusion fits from official GPUMDkit msd.out files."""

from pathlib import Path
import csv
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / "results/gpumd_nep89/300K_2x2x4_gpumdkit"
OUT = ROOT / "results/gpumd_nep89/300K_2x2x4"
N_LI = {"Li3YCl6_01": 144, "Li3YCl6_02": 144, "Li3YCl6_03": 144, "LiNbOCl4": 32}
WINDOWS = [(100.0, 200.0), (100.0, 300.0), (200.0, 500.0), (100.0, 500.0)]


def fit(t, y, lo, hi):
    mask = (t >= lo) & (t <= hi)
    coef = np.polyfit(t[mask], y[mask], 1)
    pred = np.polyval(coef, t[mask])
    r2 = 1.0 - np.sum((y[mask] - pred) ** 2) / np.sum((y[mask] - y[mask].mean()) ** 2)
    return float(coef[0]), float(r2), int(mask.sum())


def sigma_ne(D, n_li, volume_a3, temperature=300.0):
    q = 1.602176634e-19
    k = 1.380649e-23
    density = n_li / (volume_a3 * 1e-24)
    return density * q * q * D / (k * temperature) * 1e3 / 100.0


rows = []
for name, n_li in N_LI.items():
    data = np.loadtxt(BASE / name / "msd.out", comments="#")
    t, total = data[:, 0], data[:, 1:4].sum(axis=1)
    avg = (BASE / name / "average_results.txt").read_text()
    volume_text = next(line.split(":", 1)[1] for line in avg.splitlines() if line.startswith("Volume:"))
    volume = float(volume_text.split()[0])
    for lo, hi in WINDOWS:
        slope, r2, nfit = fit(t, total, lo, hi)
        d = slope / 6.0 * 1e-4
        rows.append({"replica": name, "fit_lo_ps": lo, "fit_hi_ps": hi,
                     "n_fit_points": nfit, "msd_slope_A2_ps": slope, "r2": r2,
                     "D_cm2_s": d, "sigma_NE_mS_cm": sigma_ne(d, n_li, volume)})

with (OUT / "window_sensitivity_300K_2x2x4.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

primary = [r for r in rows if r["fit_lo_ps"] == 100.0 and r["fit_hi_ps"] == 300.0]
with (OUT / "summary_300K_2x2x4.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(primary[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(primary)
