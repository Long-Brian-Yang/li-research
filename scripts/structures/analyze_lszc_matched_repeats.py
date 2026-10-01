"""Analyse every LSZC repeat using one common, predeclared MSD fit window."""
from pathlib import Path
import csv
import hashlib
import json

import numpy as np
from ase.io import read, iread
from scipy.stats import linregress

from analyze_lzoc_production import unwrap, window_msd, fit_msd
from complete_amorphous_comparisons import sigma_mscm

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/amorphous_review_20260915"
SRC = BASE / "source/LSZC_matched4t"
OUT = BASE / "LSZC_matched4t_analysis"
FIG = ROOT / "docs/materials/figures"
TEMPS = (320, 330, 340, 350)
REPEATS = (1, 2)
FIT_WINDOW = (20, 80)
KB = 8.617333262145e-5


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    reference = np.loadtxt(BASE / "completed_transport/Tang_Fig3g.csv", delimiter=",", skiprows=1)[:4]
    experiment = np.loadtxt(BASE / "completed_transport/Tang_S3_experiment.csv", delimiter=",", skiprows=1)
    reference_sigma = {int(round(row[1])): float(row[4]) for row in reference}
    records, curves, hashes = [], {}, {}
    for repeat in REPEATS:
        for temperature in TEMPS:
            folder = SRC / f"R{repeat}_{temperature}K/production"
            atoms = read(folder / "model.xyz")
            symbols = np.asarray(atoms.get_chemical_symbols())
            frames = list(iread(folder / "dump.xyz"))
            assert len(frames) == 3000
            assert all(np.array_equal(symbols, f.get_chemical_symbols()) for f in frames)
            assert all(np.allclose(atoms.cell, f.cell, atol=1e-7, rtol=0) for f in frames)
            positions = np.asarray([atoms.positions] + [f.positions for f in frames])
            unwrapped = unwrap(positions, atoms.cell.array)
            centre = np.average(unwrapped, axis=1, weights=atoms.get_masses())
            corrected = unwrapped - centre[:, None, :]
            time = np.arange(3001) * 0.1
            msd = window_msd(corrected[:, symbols == "Li"])
            fit = fit_msd(time, msd, *FIT_WINDOW)
            sigma = sigma_mscm(fit["D_cm2_s"], 32, atoms.get_volume(), temperature)
            curves[(repeat, temperature)] = (time, msd)
            records.append({"T_K": temperature, "repeat": repeat, "lo_ps": FIT_WINDOW[0], "hi_ps": FIT_WINDOW[1],
                            "D_cm2_s": fit["D_cm2_s"], "R2": fit["R2"], "alpha": fit["alpha"],
                            "sigma_NE_mS_cm": sigma, "paper_MACE_sigma_mS_cm": reference_sigma[temperature]})
            np.savetxt(OUT / f"LSZC_{temperature}K_R{repeat}_MSD.csv", np.c_[time, msd], delimiter=",",
                       header="lag_ps,Li_MSD_A2", comments="")
            thermo = np.loadtxt(folder / "thermo.out")
            assert thermo.shape == (6000, 18) and np.isfinite(thermo).all()
            for name in ("model.xyz", "dump.xyz", "thermo.out"):
                path = folder / name
                hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()

    means = []
    for temperature in TEMPS:
        group = [r for r in records if r["T_K"] == temperature]
        sigma = np.asarray([r["sigma_NE_mS_cm"] for r in group])
        diffusion = np.asarray([r["D_cm2_s"] for r in group])
        means.append({"T_K": temperature, "D_mean_cm2_s": float(diffusion.mean()),
                      "D_sample_sd_cm2_s": float(diffusion.std(ddof=1)),
                      "sigma_NE_mean_mS_cm": float(sigma.mean()),
                      "sigma_NE_sample_sd_mS_cm": float(sigma.std(ddof=1)),
                      "paper_MACE_sigma_mS_cm": reference_sigma[temperature]})
    temp = np.asarray(TEMPS, dtype=float)
    mean_sigma = np.asarray([r["sigma_NE_mean_mS_cm"] for r in means])
    reg = linregress(1000 / temp, np.log(mean_sigma * temp / 1000))
    paper_temp, paper_sigma = reference[:, 1], reference[:, 4]
    paper_reg = linregress(1000 / paper_temp, np.log(paper_sigma * paper_temp / 1000))
    exp_reg = linregress(experiment[:, 0], experiment[:, 2])
    summary = {"method": {"replica_policy": "All completed repeats are included; no replica is selected or omitted.",
                          "repeats_per_temperature": list(REPEATS), "common_msd_fit_window_ps": list(FIT_WINDOW),
                          "arrhenius_input": "Per-temperature arithmetic mean of conditional Nernst-Einstein conductivity."},
               "records": records, "temperature_summary": means,
               "Ea_mean_series_eV": float(-reg.slope * 1000 * KB), "Arrhenius_R2": float(reg.rvalue**2),
               "paper_tuned_MACE_fit_Ea_eV": float(-paper_reg.slope * 1000 * KB),
               "paper_experimental_fit_Ea_eV": float(-exp_reg.slope * 1000 * KB), "source_sha256": hashes}
    (OUT / "analysis.json").write_text(json.dumps(summary, indent=2) + "\n")
    with (OUT / "all_repeats.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(records)
    with (OUT / "temperature_summary.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(means[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(means)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from li_diffusion_style import apply_style
    colors = ("#5e3c99", "#31688e", "#35b779", "#d73027")
    fig, axes = plt.subplots(2, 3, figsize=(14, 8), layout="constrained")
    for ax, temperature, color in zip(axes.flat[:4], TEMPS, colors):
        for repeat in REPEATS:
            time, msd = curves[(repeat, temperature)]
            ax.plot(time, msd, color=color, alpha=0.52, linestyle="-" if repeat == 1 else "--", lw=1.8)
        ax.plot([], [], color=color, label="NEP89 (all repeats)")
        ax.set(title=f"LSZC — {temperature} K", xlabel="Lag time (ps)", ylabel="Li MSD (Å²)", xlim=(0, 300), ylim=(0, None))
        ax.legend()
    ax = axes.flat[4]
    ax.errorbar(TEMPS, mean_sigma, yerr=[r["sigma_NE_sample_sd_mS_cm"] for r in means], fmt="o-", capsize=4,
                color="#31688e", label="NEP89 (mean ± sample SD)")
    ax.plot(TEMPS, [reference_sigma[t] for t in TEMPS], "s--", color="#d98c10", label="Tuned MACE (paper)")
    ax.errorbar(experiment[:, 1], np.exp(experiment[:, 2]) * 1000 / experiment[:, 1], fmt="D:", color="#555555", label="Experiment")
    ax.set(title="Ionic conductivity", xlabel="Temperature (K)", ylabel="Conductivity (mS/cm)"); ax.legend()
    ax = axes.flat[5]
    x = 1000 / temp
    y = np.log(mean_sigma * temp / 1000)
    xfit = np.linspace(x.min(), x.max(), 100)
    ea = -reg.slope * 1000 * KB
    ax.plot(x, y, "o", color="#31688e", label=f"NEP89 mean ($E_a={ea:.3f}$ eV)")
    ax.plot(xfit, reg.intercept + reg.slope * xfit, "-", color="#31688e")
    paper_y = np.log(paper_sigma * paper_temp / 1000); paper_x = 1000 / paper_temp
    ax.plot(paper_x, paper_y, "^", color="#d98c10", label=f"Tuned MACE ($E_a={-paper_reg.slope*1000*KB:.3f}$ eV)")
    ax.plot(xfit, paper_reg.intercept + paper_reg.slope * xfit, "-.", color="#d98c10")
    exp_x, exp_y = experiment[:, 0], experiment[:, 2]
    ax.plot(exp_x, exp_y, "D", color="#555555", label=f"Experiment ($E_a={-exp_reg.slope*1000*KB:.3f}$ eV)")
    exp_fit_x = np.linspace(exp_x.min(), exp_x.max(), 100)
    ax.plot(exp_fit_x, exp_reg.intercept + exp_reg.slope * exp_fit_x, "--", color="#555555")
    ax.set(title="Arrhenius comparison", xlabel="1000 / T (K⁻¹)", ylabel="ln[σT / (S cm⁻¹ K)]"); ax.legend()
    apply_style(fig)
    FIG.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf", "svg"):
        fig.savefig(FIG / f"18_LSZC_transport_comparison.{ext}", dpi=220, bbox_inches="tight")
    plt.close(fig)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    run()
