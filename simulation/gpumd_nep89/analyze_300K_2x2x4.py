#!/usr/bin/env python3
"""Analyse and plot the completed 300 K GPUMD trajectories.

The trajectories are GPUMD extended XYZ files.  Li positions are unwrapped in
fractional coordinates, which is required for the skewed Li3YCl6 triclinic
cell.  Figures are written only with matplotlib (the selected figure backend).
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "simulation/gpumd_nep89/results/300K_2x2x4/job_8439212"
OUT = ROOT / "simulation/gpumd_nep89/figures/300K_2x2x4"
TABLE = ROOT / "simulation/gpumd_nep89/results/300K_2x2x4"
OUT.mkdir(parents=True, exist_ok=True)
TABLE.mkdir(parents=True, exist_ok=True)

mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
})

COLORS = {
    "Li3YCl6_01": "#3366A6",
    "Li3YCl6_02": "#5B8DB8",
    "Li3YCl6_03": "#8BB3D4",
    "LiNbOCl4": "#D56B3F",
}


def parse_lattice(comment: str) -> np.ndarray:
    match = re.search(r'Lattice="([^"]+)"', comment)
    if not match:
        raise ValueError("Lattice field not found")
    values = np.fromstring(match.group(1), sep=" ")
    if values.size != 9:
        raise ValueError("Lattice field must contain 9 values")
    return values.reshape(3, 3)


def parse_time(comment: str) -> float:
    match = re.search(r"Time=([0-9eE+.-]+)", comment)
    return float(match.group(1)) if match else np.nan


def read_gpumd_xyz(path: Path):
    """Read species, Cartesian positions and cells from a GPUMD extxyz file."""
    species_frames = []
    position_frames = []
    cells = []
    times = []
    with path.open() as handle:
        while True:
            line = handle.readline()
            if not line:
                break
            n = int(line.strip())
            comment = handle.readline().strip()
            species = []
            positions = np.empty((n, 3), dtype=float)
            for i in range(n):
                fields = handle.readline().split()
                species.append(fields[0])
                positions[i] = [float(x) for x in fields[1:4]]
            if not species_frames:
                species_frames.append(np.array(species))
            position_frames.append(positions)
            cells.append(parse_lattice(comment))
            times.append(parse_time(comment))
    species = species_frames[0]
    positions = np.asarray(position_frames)
    cells = np.asarray(cells)
    times = np.asarray(times)
    if not np.isfinite(times).all():
        times = np.arange(len(times), dtype=float) * 1000.0
    return species, positions, cells, times


def unwrap_fractional(positions: np.ndarray, cells: np.ndarray) -> np.ndarray:
    frac = np.einsum("fai,fij->faj", positions, np.linalg.inv(cells))
    unwrapped = np.empty_like(frac)
    unwrapped[0] = frac[0]
    for frame in range(1, len(frac)):
        delta = frac[frame] - frac[frame - 1]
        delta -= np.rint(delta)
        unwrapped[frame] = unwrapped[frame - 1] + delta
    return np.einsum("fai,fij->faj", unwrapped, cells)


def multi_origin_msd(cart: np.ndarray, max_lag: int | None = None, origin_stride: int = 10):
    nframes = cart.shape[0]
    max_lag = max_lag or nframes // 2
    max_lag = min(max_lag, nframes - 1)
    lags = np.arange(1, max_lag + 1)
    msd_xyz = np.empty((len(lags), 3))
    for j, lag in enumerate(lags):
        origins = np.arange(0, nframes - lag, origin_stride)
        disp = cart[origins + lag] - cart[origins]
        msd_xyz[j] = np.mean(disp * disp, axis=(0, 1))
    return lags, msd_xyz


def slope_fit(time_ps: np.ndarray, msd: np.ndarray, lo_ps: float, hi_ps: float):
    mask = (time_ps >= lo_ps) & (time_ps <= hi_ps)
    coeff = np.polyfit(time_ps[mask], msd[mask], 1)
    pred = np.polyval(coeff, time_ps[mask])
    ss_res = np.sum((msd[mask] - pred) ** 2)
    ss_tot = np.sum((msd[mask] - np.mean(msd[mask])) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
    return float(coeff[0]), float(r2), int(mask.sum())


def thermo(path: Path):
    data = np.loadtxt(path)
    if data.ndim == 1:
        data = data[None, :]
    # GPUMD thermo.out has T, kinetic energy, potential energy, pressure terms,
    # then the nine cell-vector components. The first column is temperature.
    time_ps = np.arange(len(data), dtype=float)
    return time_ps, data[:, 0], data[:, 2]


def sigma_ne(D_cm2_s: float, n_li: int, cell: np.ndarray) -> float:
    volume_cm3 = abs(np.linalg.det(cell)) * 1e-24
    number_density = n_li / volume_cm3
    q = 1.602176634e-19
    k = 1.380649e-23
    return number_density * q * q * D_cm2_s / (k * 300.0) * 1e3 / 100.0


def save_csv(path: Path, header, rows):
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    names = ["Li3YCl6_01", "Li3YCl6_02", "Li3YCl6_03", "LiNbOCl4"]
    records = []
    msd_data = {}
    thermo_data = {}

    for name in names:
        folder = RUN / name
        species, positions, cells, times = read_gpumd_xyz(folder / "dump.xyz")
        li_mask = species == "Li"
        cart = unwrap_fractional(positions[:, li_mask], cells)
        # Keep a compact, analysis-ready trajectory: Li only, unwrapped
        # Cartesian coordinates. The all-atom GPUMD dump remains outside Git.
        li_time_ps = (times - times[0]) / 1000.0
        save_csv(
            TABLE / f"{name}_Li_unwrapped_300K.csv",
            ["frame", "time_ps", "li_index", "x_A", "y_A", "z_A"],
            [
                [frame, li_time_ps[frame], li_index, *cart[frame, li_index]]
                for frame in range(len(cart))
                for li_index in range(cart.shape[1])
            ],
        )
        lags, msd_xyz = multi_origin_msd(cart, max_lag=len(cart) // 2, origin_stride=10)
        dt_ps = np.median(np.diff(times)) / 1000.0
        time_ps = lags * dt_ps
        msd_total = msd_xyz.sum(axis=1)
        # Use the second half of the available multi-origin lag range. This is
        # deliberately reported, not hidden, so the fit can be changed later.
        fit_lo = max(100.0, time_ps[-1] * 0.20)
        fit_hi = time_ps[-1] * 0.90
        slope, r2, nfit = slope_fit(time_ps, msd_total, fit_lo, fit_hi)
        D = slope / 6.0 * 1e-4
        sigma = sigma_ne(D, int(li_mask.sum()), cells[-1])
        block_values = []
        block_edges = np.linspace(fit_lo, fit_hi, 6)
        for left, right in zip(block_edges[:-1], block_edges[1:]):
            try:
                b_slope, _, _ = slope_fit(time_ps, msd_total, left, right)
                block_values.append(b_slope / 6.0 * 1e-4)
            except (TypeError, ValueError):
                pass
        block_std = float(np.std(block_values, ddof=1)) if len(block_values) > 1 else np.nan
        thermo_data[name] = thermo(folder / "thermo.out")
        msd_data[name] = (time_ps, msd_xyz, fit_lo, fit_hi)
        records.append({
            "material": "Li3YCl6" if name.startswith("Li3") else "LiNbOCl4",
            "replica": name,
            "n_frames": len(positions),
            "n_Li": int(li_mask.sum()),
            "fit_lo_ps": fit_lo,
            "fit_hi_ps": fit_hi,
            "msd_slope_A2_ps": slope,
            "r2": r2,
            "D_cm2_s": D,
            "sigma_NE_mS_cm": sigma,
            "block_std_D_cm2_s": block_std,
            "mean_temperature_K": float(np.mean(thermo_data[name][1][-max(1, len(thermo_data[name][1]) // 2):])),
        })

        save_csv(TABLE / f"{name}_msd_300K.csv",
                 ["time_ps", "msd_x_A2", "msd_y_A2", "msd_z_A2", "msd_total_A2"],
                 [[t, *xyz, xyz.sum()] for t, xyz in zip(time_ps, msd_xyz)])

    save_csv(TABLE / "summary_300K_2x2x4.csv", list(records[0].keys()),
             [[r[k] for k in records[0].keys()] for r in records])

    # Hero MSD panel: total MSD with a shaded fit window.
    fig, ax = plt.subplots(figsize=(5.8, 3.7), constrained_layout=True)
    for name in names:
        t, xyz, lo, hi = msd_data[name]
        ax.plot(t, xyz.sum(axis=1), lw=1.5, color=COLORS[name], label=name)
        ax.axvspan(lo, hi, color=COLORS[name], alpha=0.035)
    ax.set(xlabel="Lag time (ps)", ylabel="Li-only MSD (Å²)", title="300 K ML-MD: Li transport")
    ax.legend(ncol=2, fontsize=7)
    fig.savefig(OUT / "msd_total_300K_2x2x4.png", dpi=500)
    fig.savefig(OUT / "msd_total_300K_2x2x4.svg")
    plt.close(fig)

    # Directional MSD panels.
    fig, axes = plt.subplots(1, 3, figsize=(8.0, 2.8), sharex=True, sharey=False, constrained_layout=True)
    for axis, component, label in zip(axes, range(3), "xyz"):
        for name in names:
            t, xyz, _, _ = msd_data[name]
            axis.plot(t, xyz[:, component], lw=1.1, color=COLORS[name], label=name)
        axis.set_title(f"{label}-direction")
        axis.set_xlabel("Lag time (ps)")
        axis.set_ylabel("MSD (Å²)")
    axes[0].legend(fontsize=6, frameon=False)
    fig.savefig(OUT / "msd_directional_300K_2x2x4.png", dpi=500)
    fig.savefig(OUT / "msd_directional_300K_2x2x4.svg")
    plt.close(fig)

    # Temperature panel.
    fig, ax = plt.subplots(figsize=(5.8, 3.2), constrained_layout=True)
    for name in names:
        t, temp, _ = thermo_data[name]
        ax.plot(t, temp, lw=0.9, color=COLORS[name], label=name)
    ax.axhline(300, color="#444444", lw=0.8, ls="--")
    ax.set(xlabel="Thermo sample (1 ps)", ylabel="Temperature (K)", title="Thermostat stability")
    ax.legend(ncol=2, fontsize=7)
    fig.savefig(OUT / "temperature_300K_2x2x4.png", dpi=500)
    fig.savefig(OUT / "temperature_300K_2x2x4.svg")
    plt.close(fig)

    # Compact summary panel with replica-level values.
    d_values = np.array([r["D_cm2_s"] for r in records]) * 1e6
    s_values = np.array([r["sigma_NE_mS_cm"] for r in records])
    fig, axes = plt.subplots(1, 2, figsize=(6.2, 3.0), constrained_layout=True)
    axes[0].bar(np.arange(len(names)), d_values, color=[COLORS[n] for n in names])
    axes[0].set_ylabel(r"$D_{Li}$ ($10^{-6}$ cm$^2$ s$^{-1}$)")
    axes[1].bar(np.arange(len(names)), s_values, color=[COLORS[n] for n in names])
    axes[1].set_ylabel(r"$\sigma_{NE}$ (mS cm$^{-1}$)")
    for axis in axes:
        axis.set_xticks(np.arange(len(names)), names, rotation=35, ha="right", fontsize=7)
    fig.suptitle("Replica-level transport estimates (300 K)")
    fig.savefig(OUT / "transport_summary_300K_2x2x4.png", dpi=500)
    fig.savefig(OUT / "transport_summary_300K_2x2x4.svg")
    plt.close(fig)

    print("material,replica,D_cm2_s,sigma_NE_mS_cm,R2,block_std_D_cm2_s,mean_T_K")
    for r in records:
        print(r["material"], r["replica"], f"{r['D_cm2_s']:.6e}",
              f"{r['sigma_NE_mS_cm']:.4f}", f"{r['r2']:.5f}",
              f"{r['block_std_D_cm2_s']:.3e}", f"{r['mean_temperature_K']:.2f}")


if __name__ == "__main__":
    main()
