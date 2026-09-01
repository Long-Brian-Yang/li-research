"""Generate the formal Li3YCl6 midterm Arrhenius figure."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[4]
OUTS = [
    ROOT / "results/midterm_Li3YCl6_MACE_M3GNet/plots/Li3YCl6_Arrhenius_all_models.png",
    ROOT / "results/publication_all_materials/arrhenius/Li3YCl6_Arrhenius_all_models.png",
]
T = np.array([400., 600., 800., 1000.])
x = 1000.0 / T
kB = 8.617333262e-5
models = [
    ("MACE-MPA-0", np.array([0.01551425, 0.29804109, 0.62695216, 1.22489997]), 0.302, "#1f77b4"),
    ("SevenNet-nano", np.array([0.0373838538, 0.2664585555, 0.6438489943, 1.0921416519]), 0.246, "#2ca02c"),
    ("M3GNet (GPU)", np.array([0.0499968539, 0.2422683654, 0.4811228915, 0.8433514808]), 0.212, "#d62728"),
]

fig, ax = plt.subplots(figsize=(8.8, 5.8667), dpi=180)
for name, sigma, ea, color in models:
    y = np.log(sigma)
    slope, intercept = np.polyfit(x, y, 1)
    xx = np.linspace(x.min(), x.max(), 200)
    ax.plot(xx, slope * xx + intercept, color=color, lw=2.2)
    ax.scatter(x, y, color=color, s=105, zorder=3,
               label=fr"{name} ($E_a$={ea:.3f} eV)")
    x300 = 1000.0 / 300.0
    y300 = slope * x300 + intercept
    ax.plot([x.max(), x300], [slope * x.max() + intercept, y300], color=color, lw=2.2, ls="--")
    ax.plot(x300, y300, marker="o", ms=11, mfc="white", mec=color, mew=2.2)

references = [
    ("Experiment", 5.1e-4, 0.400, "#111111", "s", ":"),
    ("NGK M3GNet (CPU reference)", 9.69e-3, 0.180, "#555555", "D", "-.")
]
xx = np.linspace(1.0, 1000.0 / 300.0, 250)
for name, sigma300, ea, color, marker, ls in references:
    y300 = np.log(sigma300)
    yline = y300 - (ea / kB) * (xx / 1000.0 - 1.0 / 300.0)
    ax.plot(xx, yline, color=color, lw=2.5, ls=ls, label=fr"{name} ($E_a$={ea:.3f} eV)")
    ax.plot(1000.0 / 300.0, y300, marker=marker, ms=11, mfc="white", mec=color, mew=2.2)

ax.set_title(r"Li$_3$YCl$_6$ — Arrhenius analysis of Li-ion transport", fontsize=18, pad=10)
ax.set_xlabel(r"1000/T (K$^{-1}$)", fontsize=15)
ax.set_ylabel(r"$\ln\,\sigma_{\mathrm{NE}}$ (S cm$^{-1}$)", fontsize=15)
ax.tick_params(labelsize=12, width=1.2, length=5)
for spine in ax.spines.values():
    spine.set_linewidth(1.2)
ax.grid(True, alpha=0.23)
ax.legend(fontsize=12.0, loc="upper right",
          frameon=True, edgecolor="#bdbdbd", facecolor="white", framealpha=0.96,
          borderpad=0.85, labelspacing=0.65, handlelength=2.6)
fig.tight_layout()
for out in OUTS:
    fig.savefig(out, bbox_inches="tight")

# Keep the two-model midterm comparison used in the presentation README,
# using exactly the same typography and axis style as the three-model figure.
fig2, ax2 = plt.subplots(figsize=(8.8, 5.8667), dpi=180)
for name, sigma, ea, color in (models[0], models[2]):
    y = np.log(sigma)
    slope, intercept = np.polyfit(x, y, 1)
    xx = np.linspace(x.min(), x.max(), 200)
    ax2.plot(xx, slope * xx + intercept, color=color, lw=2.2)
    ax2.scatter(x, y, color=color, s=105, zorder=3,
                label=fr"{name} ($E_a$={ea:.3f} eV)")
    x300 = 1000.0 / 300.0
    y300 = slope * x300 + intercept
    ax2.plot([x.max(), x300], [slope * x.max() + intercept, y300],
             color=color, lw=2.2, ls="--")
    ax2.plot(x300, y300, marker="o", ms=11, mfc="white", mec=color, mew=2.2)
for name, sigma300, ea, color, marker, ls in references:
    y300 = np.log(sigma300)
    yline = y300 - (ea / kB) * (xx / 1000.0 - 1.0 / 300.0)
    ax2.plot(xx, yline, color=color, lw=2.5, ls=ls,
             label=fr"{name} ($E_a$={ea:.3f} eV)")
    ax2.plot(1000.0 / 300.0, y300, marker=marker, ms=11,
             mfc="white", mec=color, mew=2.2)
ax2.set_title(r"Li$_3$YCl$_6$ — Arrhenius analysis of Li-ion transport", fontsize=18, pad=10)
ax2.set_xlabel(r"1000/T (K$^{-1}$)", fontsize=15)
ax2.set_ylabel(r"$\ln\,\sigma_{\mathrm{NE}}$ (S cm$^{-1}$)", fontsize=15)
ax2.tick_params(labelsize=12, width=1.2, length=5)
for spine in ax2.spines.values():
    spine.set_linewidth(1.2)
ax2.grid(True, alpha=0.23)
ax2.legend(fontsize=12.0, loc="upper right", frameon=True,
           edgecolor="#bdbdbd", facecolor="white", framealpha=0.96,
           borderpad=0.85, labelspacing=0.65, handlelength=2.6)
fig2.tight_layout()
fig2.savefig(ROOT / "results/midterm_Li3YCl6_MACE_M3GNet/plots/Li3YCl6_Arrhenius_MACE_M3GNet_exp_company.png",
             bbox_inches="tight")
