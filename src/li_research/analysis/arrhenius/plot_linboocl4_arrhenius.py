"""Regenerate LiNbOCl4 Arrhenius figures from all stored replica MSD tracks.

Each track uses the common 20--500 ps MSD fit. Executions with the same
initial-velocity seed are averaged within that seed, then distinct seeds are
averaged equally at each temperature. No trajectory is ranked or selected by
its transport value or agreement with experiment.
"""
from pathlib import Path
import csv
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))
from li_research.analysis.lammps.linboocl4_all_replicas import (
    FIT_WINDOW_PS, MODELS, TEMPERATURES, collect_tracks, summarize_by_seed,
)


KB_EV = 8.617333262e-5
KB_J = 1.380649e-23
ELEMENTARY_CHARGE = 1.602176634e-19
N_LI = 32
VOLUME_A3 = 5127.4186488
MODEL_COLORS = {
    "MACE-MPA-0": "#1f77b4",
    "SevenNet-nano": "#2ca02c",
    "M3GNet GPU": "#d62728",
}
EXPERIMENTAL_EA = 0.240  # eV; Tanaka et al., DOI 10.1002/anie.202217581
EXPERIMENTAL_SIGMA_300 = 10.4e-3  # S/cm


def sigma_ne(diffusion_cm2_s: float, temperature: float) -> float:
    number_density_cm3 = N_LI / (VOLUME_A3 * 1.0e-24)
    return number_density_cm3 * ELEMENTARY_CHARGE**2 * diffusion_cm2_s / (KB_J * temperature)


def build_transport_summary():
    tracks = collect_tracks()
    grouped = summarize_by_seed(tracks)
    summary = {}
    for model in MODELS:
        d_means = np.asarray([grouped[(model, t)]["D_mean_cm2_s"] for t in TEMPERATURES])
        x = 1.0 / np.asarray(TEMPERATURES, dtype=float)
        y = np.log(d_means)
        slope, intercept = np.polyfit(x, y, 1)
        predicted = slope * x + intercept
        r2 = 1.0 - np.sum((y - predicted) ** 2) / np.sum((y - y.mean()) ** 2)
        ea = -slope * KB_EV
        d300 = float(np.exp(intercept + slope / 300.0))
        summary[model] = {
            "Ea_eV": float(ea), "R2": float(r2), "D300_cm2_s": d300,
            "D_by_temperature": {t: grouped[(model, t)] for t in TEMPERATURES},
        }
    return tracks, summary


def write_source_data(tracks, summary) -> None:
    output = ROOT / "results/publication_all_materials/supplementary/source_data"
    output.mkdir(parents=True, exist_ok=True)
    with (output / "LiNbOCl4_trajectory_diffusion.csv").open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["model", "T_K", "velocity_seed", "D_cm2_s", "trajectory"])
        writer.writerows((row.model, row.temperature_K, row.seed, row.diffusion_cm2_s,
                          row.path.relative_to(ROOT).as_posix()) for row in tracks)

    summary_path = output / "LiNbOCl4_D_Ea_summary.csv"
    with summary_path.open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["model", "Ea_eV", "R2", "D300_cm2_s", "D600", "D800", "D1000", "D1200",
                         "temperatures_K", "replica_policy", "seed_counts", "execution_counts", "fit_window_ps"])
        for model, result in summary.items():
            per_t = result["D_by_temperature"]
            writer.writerow([model, result["Ea_eV"], result["R2"], result["D300_cm2_s"],
                             *[per_t[t]["D_mean_cm2_s"] for t in TEMPERATURES],
                             ",".join(map(str, TEMPERATURES)),
                             "all completed executions; grouped by velocity seed",
                             ",".join(str(per_t[t]["seed_count"]) for t in TEMPERATURES),
                             ",".join(str(per_t[t]["execution_count"]) for t in TEMPERATURES),
                             f"{FIT_WINDOW_PS[0]:g}-{FIT_WINDOW_PS[1]:g}"])


def build_figure(summary):
    temperature = np.asarray(TEMPERATURES, dtype=float)
    x = 1000.0 / temperature
    fig, ax = plt.subplots(figsize=(8.8, 5.8667), dpi=180)
    source_rows = []
    for model, result in summary.items():
        d_values = np.asarray([result["D_by_temperature"][t]["D_mean_cm2_s"] for t in TEMPERATURES])
        sigma_values = np.asarray([sigma_ne(d, t) for d, t in zip(d_values, temperature)])
        y = np.log(sigma_values * temperature)
        slope, intercept = np.polyfit(x, y, 1)
        ea_from_sigma = -slope * 1000.0 * KB_EV
        xx = np.linspace(x.min(), x.max(), 200)
        color = MODEL_COLORS[model]
        ax.plot(xx, slope * xx + intercept, color=color, lw=3.4)
        ax.scatter(x, y, color=color, s=82, zorder=3,
                   label=fr"{model} ($E_a={ea_from_sigma:.3f}\,\mathrm{{eV}}$)")
        x300 = 1000.0 / 300.0
        y300 = slope * x300 + intercept
        ax.plot([x.max(), x300], [slope * x.max() + intercept, y300], color=color, lw=3.4, ls="--")
        ax.plot(x300, y300, marker="o", ms=9, mfc="white", mec=color, mew=2.0)
        for t, d, sigma, y_value in zip(TEMPERATURES, d_values, sigma_values, y):
            stats = result["D_by_temperature"][t]
            source_rows.append((model, t, d, sigma, y_value, stats["seed_count"],
                                stats["execution_count"], stats["D_sample_sd_cm2_s"]))

    x300 = 1000.0 / 300.0
    y300_exp = np.log(EXPERIMENTAL_SIGMA_300 * 300.0)
    xx = np.linspace(x.min(), x300, 250)
    y_exp = y300_exp - (EXPERIMENTAL_EA / KB_EV) * (xx / 1000.0 - 1.0 / 300.0)
    ax.plot(xx, y_exp, color="#111111", lw=3.4, ls=":",
            label=fr"Experiment ($E_a={EXPERIMENTAL_EA:.3f}\,\mathrm{{eV}}$)")
    ax.plot(x300, y300_exp, marker="s", ms=9, mfc="white", mec="#111111", mew=2.0)
    ax.set_title(r"LiNbOCl$_4$ — Arrhenius analysis of Li-ion transport", fontsize=22, pad=12)
    ax.set_xlabel(r"1000/T (K$^{-1}$)", fontsize=19)
    ax.set_ylabel(r"$\ln[\sigma_{\mathrm{NE}}T\;(\mathrm{S\,cm^{-1}\,K})]$", fontsize=19)
    ax.tick_params(labelsize=15, width=1.5, length=6)
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)
    ax.grid(True, alpha=0.23)
    ax.legend(fontsize=13, loc="upper right", frameon=False,
              borderpad=0.35, labelspacing=0.45, handlelength=2.6)
    fig.tight_layout()
    return fig, source_rows


def main() -> None:
    tracks, summary = build_transport_summary()
    write_source_data(tracks, summary)
    fig, source_rows = build_figure(summary)
    output_stems = [
        ROOT / "results/publication_all_materials/arrhenius/LiNbOCl4_Arrhenius_all_models",
        ROOT / "docs/materials/figures/04_LiNbOCl4_Arrhenius",
    ]
    for stem in output_stems:
        stem.parent.mkdir(parents=True, exist_ok=True)
        for suffix in (".png", ".pdf", ".svg"):
            path = stem.with_suffix(suffix)
            fig.savefig(path, dpi=300 if suffix == ".png" else None)
            if suffix == ".svg":
                path.write_text("\n".join(line.rstrip() for line in path.read_text().splitlines()) + "\n")
            print(path)

    source_path = ROOT / "results/publication_all_materials/supplementary/source_data/LiNbOCl4_Arrhenius_plot_data.csv"
    with source_path.open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["series", "T_K", "D_cm2_s_mean", "sigma_NE_S_cm", "ln_sigmaT",
                         "velocity_seed_count", "execution_count", "D_sample_sd_cm2_s"])
        writer.writerows(source_rows)
        writer.writerow(["Experiment", 300.0, "", EXPERIMENTAL_SIGMA_300, np.log(EXPERIMENTAL_SIGMA_300 * 300.0), "", "", ""])
    plt.close(fig)
    print("Analysis summary:")
    for model, result in summary.items():
        print(model, f"Ea={result['Ea_eV']:.4f} eV", f"R2={result['R2']:.4f}",
              f"D300={result['D300_cm2_s']:.4e} cm^2/s")
    print(f"Included {len(tracks)} completed MSD execution tracks across all model/temperature groups")


if __name__ == "__main__":
    main()
