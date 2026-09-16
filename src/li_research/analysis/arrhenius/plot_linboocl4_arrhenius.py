"""Regenerate the LiNbOCl4 publication Arrhenius panel.

The layout follows the Li3YCl6 panel: model transport is converted to a
conditional Nernst--Einstein conductivity, and the experimental reference is
anchored by the reported 300 K conductivity and activation energy.
"""
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[4]
T = np.array([600., 800., 1000., 1200.])
x = 1000.0 / T
kb_ev = 8.617333262e-5
kb_j = 1.380649e-23
elementary_charge = 1.602176634e-19
n_li = 32
volume_a3 = 5127.4186488
number_density_cm3 = n_li / (volume_a3 * 1.0e-24)
series = [
    ("MACE-MPA-0", [2.2414064884e-6, 1.0327468841e-5, 2.2000042187e-5, 4.9955242087e-5], "#1f77b4"),
    ("SevenNet-nano", [2.1931432164e-6, 1.3022182835e-5, 3.0074905262e-5, 7.5903962406e-5], "#2ca02c"),
    ("M3GNet GPU", [1.9143993123e-7, 3.4931969439e-7, 2.5821102699e-6, 9.0673258084e-6], "#d62728"),
]
experimental_ea = 0.240  # eV; Tanaka et al., DOI: 10.1002/anie.202217581
experimental_sigma_300 = 10.4e-3  # S/cm
fig, ax = plt.subplots(figsize=(8.8, 5.8667), dpi=180)
source_rows = []
for name, vals, color in series:
    diffusion = np.asarray(vals, float)
    sigma_ne = (number_density_cm3 * elementary_charge**2 * diffusion /
                (kb_j * T))
    y = np.log(sigma_ne * T)
    m, b = np.polyfit(x, y, 1)
    ea = -m * 1000.0 * kb_ev
    xx = np.linspace(x.min(), x.max(), 200)
    ax.plot(xx, m * xx + b, color=color, lw=3.4)
    ax.scatter(x, y, color=color, s=82, zorder=3,
               label=fr"{name} ($E_a={ea:.3f}\,\mathrm{{eV}}$)")
    x300 = 1000.0 / 300.0
    y300 = m * x300 + b
    ax.plot([x.max(), x300], [m * x.max() + b, y300],
            color=color, lw=3.4, ls="--")
    ax.plot(x300, y300, marker="o", ms=9, mfc="white",
            mec=color, mew=2.0)
    for temperature, d_value, sigma_value, y_value in zip(
            T, diffusion, sigma_ne, y):
        source_rows.append((name, temperature, d_value, sigma_value, y_value))

# Reconstruct the reported experimental Arrhenius trend from its measured
# room-temperature conductivity and activation energy.  This is a conductivity
# reference, not an experimental tracer-diffusion series.
x300 = 1000.0 / 300.0
y300_exp = np.log(experimental_sigma_300 * 300.0)
xx = np.linspace(x.min(), x300, 250)
y_exp = y300_exp - (experimental_ea / kb_ev) * (xx / 1000.0 - 1.0 / 300.0)
ax.plot(
    xx,
    y_exp,
    color="#111111",
    lw=3.4,
    ls=":",
    label=fr"Experiment ($E_a={experimental_ea:.3f}\,\mathrm{{eV}}$)",
)
ax.plot(x300, y300_exp, marker="s", ms=9, mfc="white",
        mec="#111111", mew=2.0)
ax.set_title(r"LiNbOCl$_4$ — Arrhenius analysis of Li-ion transport", fontsize=22, pad=12)
ax.set_xlabel(r"1000/T (K$^{-1}$)", fontsize=19)
ax.set_ylabel(r"$\ln[\sigma_{\mathrm{NE}}T\;(\mathrm{S\,cm^{-1}\,K})]$", fontsize=19)
ax.tick_params(labelsize=15, width=1.5, length=6)
for spine in ax.spines.values(): spine.set_linewidth(1.5)
ax.grid(True, alpha=0.23)
ax.legend(fontsize=13, loc="upper right", frameon=False,
          borderpad=0.35, labelspacing=0.45, handlelength=2.6)
fig.tight_layout()
output_stems = [
    ROOT / "results/publication_all_materials/arrhenius/LiNbOCl4_Arrhenius_all_models",
    ROOT / "docs/materials/figures/04_LiNbOCl4_Arrhenius",
]
for stem in output_stems:
    stem.parent.mkdir(parents=True, exist_ok=True)
    for suffix in (".png", ".pdf", ".svg"):
        out = stem.with_suffix(suffix)
        fig.savefig(out, dpi=300 if suffix == ".png" else None)
        print(out)

source_csv = ROOT / "results/publication_all_materials/supplementary/source_data/LiNbOCl4_Arrhenius_plot_data.csv"
source_csv.parent.mkdir(parents=True, exist_ok=True)
with source_csv.open("w", newline="") as handle:
    writer = csv.writer(handle, lineterminator="\n")
    writer.writerow(["series", "T_K", "D_cm2_s", "sigma_NE_S_cm", "ln_sigmaT"])
    writer.writerows(source_rows)
    writer.writerow(["Experiment", 300.0, "", experimental_sigma_300,
                     y300_exp])
print(source_csv)
plt.close(fig)
