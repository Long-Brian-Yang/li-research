"""Regenerate the LiNbOCl4 publication Arrhenius panel from the selected data."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[4]
T = np.array([600., 800., 1000., 1200.])
x = 1000.0 / T
kb = 8.617333262e-5
series = [
    ("MACE-MPA-0", [2.2414064884e-6, 1.0327468841e-5, 2.2000042187e-5, 4.9955242087e-5], "#1f77b4"),
    ("SevenNet-nano", [2.1931432164e-6, 1.3022182835e-5, 3.0074905262e-5, 7.5903962406e-5], "#2ca02c"),
    ("M3GNet GPU", [1.9143993123e-7, 3.4931969439e-7, 2.5821102699e-6, 9.0673258084e-6], "#d62728"),
]
fig, ax = plt.subplots(figsize=(8.8, 5.8667), dpi=180)
for name, vals, color in series:
    y = np.log(vals)
    m, b = np.polyfit(x, y, 1)
    ea = -m * 1000.0 * kb
    xx = np.linspace(x.min(), x.max(), 200)
    ax.plot(xx, m * xx + b, color=color, lw=3.4, label=fr"{name} ($E_a={ea:.3f}\,\mathrm{{eV}}$)")
    ax.scatter(x, y, color=color, s=82, zorder=3)
    x300 = 1000.0 / 300.0
    ax.plot([x.max(), x300], [m*x.max()+b, m*x300+b], color=color, lw=3.4, ls="--")
ax.set_title(r"LiNbOCl$_4$ — Arrhenius analysis of Li-ion transport", fontsize=22, pad=12)
ax.set_xlabel(r"1000/T (K$^{-1}$)", fontsize=19)
ax.set_ylabel(r"$\ln[D\;(\mathrm{cm^2\,s^{-1}})]$", fontsize=19)
ax.tick_params(labelsize=15, width=1.5, length=6)
for spine in ax.spines.values(): spine.set_linewidth(1.5)
ax.grid(True, alpha=0.23)
ax.legend(fontsize=13, loc="upper right", frameon=False)
fig.tight_layout()
for out in [ROOT / "results/publication_all_materials/arrhenius/LiNbOCl4_Arrhenius_all_models.png"]:
    out.parent.mkdir(parents=True, exist_ok=True); fig.savefig(out)
    print(out)
