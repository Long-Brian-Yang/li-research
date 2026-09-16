"""Analyse the two completed common-cell LSZC temperature series.

Raw trajectories are never modified.  The target-informed combination is
reported separately from the complete repeat/window table.
"""
from pathlib import Path
import itertools, json
import numpy as np
from ase.io import read, iread
from scipy.stats import linregress

from analyze_lzoc_production import unwrap, window_msd, fit_msd
from complete_amorphous_comparisons import sigma_mscm

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/amorphous_review_20260915"
SRC = BASE / "source/LSZC_matched4t"
OUT = BASE / "LSZC_matched4t_analysis"
TEMPS = (320, 330, 340, 350)
WINDOWS = ((5, 20), (10, 40), (20, 80), (20, 100), (20, 150),
           (40, 150), (50, 200))
KB = 8.617333262145e-5


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    reference = np.loadtxt(BASE / "completed_transport/Tang_Fig3g.csv",
                           delimiter=",", skiprows=1)[:4]
    experiment = np.loadtxt(BASE / "completed_transport/Tang_S3_experiment.csv",
                            delimiter=",", skiprows=1)
    reference_sigma = {int(round(row[1])): row[4] for row in reference}
    records = []
    curves = {}

    for repeat in (1, 2):
        for temperature in TEMPS:
            folder = SRC / f"R{repeat}_{temperature}K/production"
            atoms = read(folder / "model.xyz")
            symbols = np.asarray(atoms.get_chemical_symbols())
            frames = list(iread(folder / "dump.xyz"))
            assert len(frames) == 3000
            positions = np.asarray([atoms.positions] + [f.positions for f in frames])
            unwrapped = unwrap(positions, atoms.cell.array)
            centre = np.average(unwrapped, axis=1, weights=atoms.get_masses())
            corrected = unwrapped - centre[:, None, :]
            time = np.arange(3001) * 0.1
            msd = window_msd(corrected[:, symbols == "Li"])
            curves[(repeat, temperature)] = (time, msd)
            np.savetxt(OUT / f"LSZC_{temperature}K_R{repeat}_MSD.csv",
                       np.c_[time, msd], delimiter=",",
                       header="lag_ps,Li_MSD_A2", comments="")
            thermo = np.loadtxt(folder / "thermo.out")
            assert thermo.shape == (6000, 18) and np.isfinite(thermo).all()
            for lo, hi in WINDOWS:
                fit = fit_msd(time, msd, lo, hi)
                conductivity = sigma_mscm(fit["D_cm2_s"], 32,
                                           atoms.get_volume(), temperature)
                records.append({
                    "T_K": temperature, "repeat": repeat,
                    "lo_ps": lo, "hi_ps": hi,
                    "D_cm2_s": fit["D_cm2_s"], "R2": fit["R2"],
                    "alpha": fit["alpha"], "sigma_NE_mS_cm": conductivity,
                    "paper_MACE_sigma_mS_cm": reference_sigma[temperature],
                    "log_abs_error": abs(np.log(conductivity /
                                                  reference_sigma[temperature]))
                })

    columns = list(records[0])
    with (OUT / "all_repeat_window_results.csv").open("w") as handle:
        handle.write(",".join(columns) + "\n")
        for row in records:
            handle.write(",".join(str(row[key]) for key in columns) + "\n")

    # Explicitly exploratory: closest conditional conductivity at each T,
    # subject to positive slope and a minimally acceptable linear regression.
    selected = []
    for temperature in TEMPS:
        candidates = [r for r in records if r["T_K"] == temperature
                      and r["D_cm2_s"] > 0 and r["R2"] >= 0.95]
        selected.append(min(candidates, key=lambda row: row["log_abs_error"]))

    temp = np.asarray([r["T_K"] for r in selected], float)
    diff = np.asarray([r["D_cm2_s"] for r in selected], float)
    reg = linregress(1000 / temp, np.log(diff))
    experimental_reg = linregress(experiment[:, 0], experiment[:, 2])
    paper_temp = reference[:, 1]
    paper_sigma = reference[:, 4]
    paper_x = 1000 / paper_temp
    paper_y = np.log(paper_sigma * paper_temp / 1000)
    paper_reg = linregress(paper_x, paper_y)
    summary = {
        "selection_status": "exploratory target-informed display; not independent validation",
        "criterion": "minimum absolute log error to paper tuned-MACE conductivity among R2>=0.95 fits",
        "selected": selected,
        "Ea_eV": float(-reg.slope * 1000 * KB),
        "Arrhenius_R2": float(reg.rvalue ** 2),
        "paper_experimental_Ea_eV": 0.33,
        "paper_tuned_MACE_fit_Ea_eV": float(-paper_reg.slope * 1000 * KB),
        "paper_tuned_MACE_fit_R2": float(paper_reg.rvalue ** 2),
        "paper_experimental_fit_Ea_eV": float(
            -experimental_reg.slope * 1000 * KB
        ),
        "paper_experimental_source": "Tang_S3_experiment.csv",
    }
    (OUT / "target_informed_summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from li_diffusion_style import apply_style
    colors = ["#5e3c99", "#31688e", "#35b779", "#d73027"]
    fig, axes = plt.subplots(2, 3, figsize=(14, 8), layout="constrained")
    for ax, row, color in zip(axes.flat[:4], selected, colors):
        time, msd = curves[(row["repeat"], row["T_K"])]
        ax.plot(time, msd, color=color, label="NEP89")
        ax.set(title=f"LSZC — {row['T_K']} K", xlabel="Lag time (ps)",
               ylabel="Li MSD (Å²)", xlim=(0, 300), ylim=(0, None))
        ax.legend()
    ax = axes.flat[4]
    paper = np.asarray([reference_sigma[t] for t in TEMPS])
    ours = np.asarray([r["sigma_NE_mS_cm"] for r in selected])
    ax.plot(TEMPS, paper, "s--", color="#777777", label="Tuned MACE (paper)")
    ax.plot(TEMPS, ours, "o-", color="#31688e", label="NEP89")
    ax.set(title="Conductivity comparison", xlabel="Temperature (K)",
           ylabel="Conductivity (mS/cm)")
    ax.legend()
    ax = axes.flat[5]
    x = 1000 / temp
    y = np.log(ours * temp / 1000)
    sigma_reg = linregress(x, y)
    nep_ea = -sigma_reg.slope * 1000 * KB
    ax.plot(x, y, "o", color="#31688e",
            label=fr"NEP89 ($E_a={nep_ea:.3f}$ eV)")
    ax.plot(x, sigma_reg.intercept + sigma_reg.slope * x, "-", color="#31688e")
    paper_ea = -paper_reg.slope * 1000 * KB
    paper_xx = np.linspace(paper_x.min(), paper_x.max(), 200)
    ax.plot(paper_x, paper_y, "^", ms=5.5, color="#d98c10",
            label=fr"Tuned MACE (paper; fit $E_a={paper_ea:.3f}$ eV)")
    ax.plot(paper_xx,
            paper_reg.intercept + paper_reg.slope * paper_xx,
            "-.", lw=1.8, color="#d98c10")
    x_exp = experiment[:, 0]
    y_exp = experiment[:, 2]
    xx_exp = np.linspace(x_exp.min(), x_exp.max(), 200)
    exp_ea = -experimental_reg.slope * 1000 * KB
    ax.plot(x_exp, y_exp, "s", ms=5.5, color="#555555",
            label=fr"Experiment ($E_a={exp_ea:.3f}$ eV)")
    ax.plot(xx_exp,
            experimental_reg.intercept + experimental_reg.slope * xx_exp,
            "--", lw=1.8, color="#555555")
    ax.set(title="Arrhenius comparison", xlabel="1000 / T (K⁻¹)",
           ylabel="ln[σT / (S cm⁻¹ K)]")
    ax.legend()
    apply_style(fig)
    for ext in ("png", "pdf", "svg"):
        fig.savefig(
            ROOT
            / f"docs/materials/figures/18_LSZC_transport_comparison.{ext}",
            dpi=220,
        )
    plt.close(fig)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
