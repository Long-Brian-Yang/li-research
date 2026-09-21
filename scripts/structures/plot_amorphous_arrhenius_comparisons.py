"""Create publication-style Arrhenius comparisons for amorphous materials.

The figures use the same 8.8:5.8667 layout as the crystalline Arrhenius
figures.  Conductivity and diffusion are kept on separate physical scales:
LSZC and LiPON use ln(sigma*T), whereas LZOC and Li3PS4 use ln(D).
No activation energy is assigned to LZOC because neither the displayed NEP89
nor AIMD three-point series supports a stable monotonic Arrhenius fit.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/amorphous_review_20260915"
FIG = ROOT / "docs/materials/figures"
SOURCE = BASE / "literature_correspondence"
KB_EV = 8.617333262e-5
BLUE = "#31688e"
GREEN = "#35a77b"
RED = "#d73027"
BLACK = "#111111"
GRAY = "#666666"


def linear_fit(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    slope, intercept = np.polyfit(x, y, 1)
    predicted = slope * x + intercept
    r2 = 1.0 - np.sum((y - predicted) ** 2) / np.sum((y - y.mean()) ** 2)
    return float(slope), float(intercept), float(r2)


def style(ax: plt.Axes, title: str, ylabel: str) -> None:
    ax.set_title(title, fontsize=22, pad=12)
    ax.set_xlabel(r"1000/T (K$^{-1}$)", fontsize=19)
    ax.set_ylabel(ylabel, fontsize=19)
    ax.tick_params(labelsize=15, width=1.5, length=6)
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)
    ax.grid(True, alpha=0.23)
    ax.legend(fontsize=13, loc="best", frameon=False,
              borderpad=0.35, labelspacing=0.45, handlelength=2.6)


def save(fig: plt.Figure, stem: str) -> list[str]:
    FIG.mkdir(parents=True, exist_ok=True)
    outputs = []
    for suffix in (".png", ".pdf", ".svg"):
        path = FIG / f"{stem}{suffix}"
        fig.savefig(path, dpi=300 if suffix == ".png" else None)
        if suffix == ".svg":
            path.write_text("\n".join(line.rstrip() for line in path.read_text().splitlines()) + "\n")
        outputs.append(str(path.relative_to(ROOT)))
    plt.close(fig)
    return outputs


def write_source(name: str, header: list[str], rows: list[tuple]) -> Path:
    SOURCE.mkdir(parents=True, exist_ok=True)
    path = SOURCE / name
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)
    return path


def plot_lzoc() -> tuple[list[str], Path]:
    selected = json.loads((BASE / "seed_repeats/lzoc_report_selection.json").read_text())["selected"]
    temperature = np.asarray([row["T_K"] for row in selected], float)
    nep = np.asarray([row["D_cm2_s"] for row in selected], float)
    aimd = np.asarray([row["AIMD_D"] for row in selected], float)
    x = 1000.0 / temperature

    fig, ax = plt.subplots(figsize=(8.8, 5.8667), dpi=180)
    order = np.argsort(x)
    ax.plot(x[order], np.log(nep[order]), "o-", color=BLUE, lw=3.4, ms=8,
            label=r"NEP89 ($E_a$ not assigned)")
    ax.plot(x[order], np.log(aimd[order]), "s--", color=BLACK, lw=3.4, ms=8,
            label=r"AIMD ($E_a$ not reported)")
    style(ax, r"LZOC — Li tracer diffusion: Arrhenius coordinates",
          r"$\ln[D\;(mathrm{cm^2\,s^{-1}})]$")
    ax.legend(fontsize=13, loc="lower left", frameon=False)
    fig.tight_layout()
    source = write_source(
        "LZOC_Arrhenius_plot_data.csv",
        ["series", "T_K", "D_cm2_s", "ln_D"],
        [("NEP89", t, d, np.log(d)) for t, d in zip(temperature, nep)]
        + [("Hussain_2024_AIMD", t, d, np.log(d)) for t, d in zip(temperature, aimd)],
    )
    return save(fig, "29_LZOC_Arrhenius_comparison"), source


def plot_lszc() -> tuple[list[str], Path]:
    summary = json.loads((BASE / "LSZC_matched4t_analysis/target_informed_summary.json").read_text())
    selected = summary["selected"]
    temperature = np.asarray([row["T_K"] for row in selected], float)
    sigma_ne = np.asarray([row["sigma_NE_mS_cm"] for row in selected], float) / 1000.0
    x = 1000.0 / temperature
    y = np.log(sigma_ne * temperature)
    slope, intercept, _ = linear_fit(x, y)

    mace_data = np.loadtxt(BASE / "completed_transport/Tang_Fig3g.csv", delimiter=",", skiprows=1)
    mace_data = mace_data[:4]
    exp_data = np.loadtxt(BASE / "completed_transport/Tang_S3_experiment.csv", delimiter=",", skiprows=1)

    fig, ax = plt.subplots(figsize=(8.8, 5.8667), dpi=180)
    xx = np.linspace(min(x.min(), exp_data[:, 0].min()), max(x.max(), exp_data[:, 0].max()), 250)
    ax.plot(xx, slope * xx + intercept, color=BLUE, lw=3.4)
    ax.scatter(x, y, color=BLUE, s=82, zorder=3,
               label=fr"NEP89 ($E_a={summary['Ea_eV']:.3f}$ eV)")
    ax.errorbar(mace_data[:, 0], mace_data[:, 2], yerr=mace_data[:, 3], fmt="s",
                color=GREEN, capsize=3, ms=7,
                label=fr"Tuned MACE ($E_a={summary['paper_tuned_MACE_fit_Ea_eV']:.3f}$ eV)")
    m_mace, b_mace, _ = linear_fit(mace_data[:, 0], mace_data[:, 2])
    ax.plot(xx, m_mace * xx + b_mace, color=GREEN, lw=3.4, ls="--")
    ax.plot(exp_data[:, 0], exp_data[:, 2], "D", color=BLACK, ms=7,
            label=fr"Experiment ($E_a={summary['paper_experimental_Ea_eV']:.3f}$ eV)")
    m_exp, b_exp, _ = linear_fit(exp_data[:, 0], exp_data[:, 2])
    ax.plot(xx, m_exp * xx + b_exp, color=BLACK, lw=3.4, ls=":")
    style(ax, r"LSZC — Arrhenius analysis of Li-ion conductivity",
          r"$\ln[\sigma T\;(mathrm{S\,cm^{-1}\,K})]$")
    fig.tight_layout()

    rows = [("NEP89", t, xx_, yy) for t, xx_, yy in zip(temperature, x, y)]
    rows += [("Tang_2026_tuned_MACE", 1000.0 / row[0], row[0], row[2]) for row in mace_data]
    rows += [("Tang_2026_experiment", 1000.0 / row[0], row[0], row[2]) for row in exp_data]
    source = write_source("LSZC_Arrhenius_plot_data.csv", ["series", "T_K", "1000_over_T_K-1", "ln_sigmaT"], rows)
    return save(fig, "30_LSZC_Arrhenius_comparison"), source


def plot_li3ps4() -> tuple[list[str], Path]:
    data = np.loadtxt(BASE / "Li3PS4_R1_transport/reference_comparison.csv", delimiter=",", skiprows=1)
    temperature, nep, chen = data[:, 0], data[:, 1], data[:, 2]
    x = 1000.0 / temperature
    high = temperature >= 500
    m_nep, b_nep, _ = linear_fit(x[high], np.log(nep[high]))
    ea_nep = -m_nep * KB_EV * 1000.0
    ea_chen = 0.470

    fig, ax = plt.subplots(figsize=(8.8, 5.8667), dpi=180)
    order = np.argsort(x)
    ax.plot(x[order], np.log(nep[order]), "o-", color=BLUE, lw=2.2, ms=8,
            label=fr"NEP89 ($E_a={ea_nep:.3f}$ eV; 500–900 K)")
    xx_nep = np.linspace(x[high].min(), x[high].max(), 200)
    ax.plot(xx_nep, m_nep * xx_nep + b_nep, color=BLUE, lw=3.4)
    ax.plot(x[order], np.log(chen[order]), "s--", color=RED, lw=2.2, ms=8,
            label=fr"Chen DeePMD (reported $E_a={ea_chen:.3f}$ eV)")
    anchor_x = x[temperature.argmax()]
    anchor_y = np.log(chen[temperature.argmax()])
    xx_ref = np.linspace(x.min(), x[high].max(), 200)
    reference_slope = -ea_chen / KB_EV / 1000.0
    ax.plot(xx_ref, anchor_y + reference_slope * (xx_ref - anchor_x),
            color=RED, lw=3.4, ls=":")
    style(ax, r"Li$_3$PS$_4$ — Arrhenius analysis of Li-ion diffusion",
          r"$\ln[D\;(mathrm{cm^2\,s^{-1}})]$")
    ax.legend(fontsize=12.5, loc="lower left", frameon=False)
    fig.tight_layout()
    source = write_source(
        "Li3PS4_Arrhenius_plot_data.csv",
        ["series", "T_K", "D_cm2_s", "ln_D"],
        [("NEP89", t, d, np.log(d)) for t, d in zip(temperature, nep)]
        + [("Chen_2025_DeePMD", t, d, np.log(d)) for t, d in zip(temperature, chen)],
    )
    return save(fig, "31_Li3PS4_Arrhenius_comparison"), source


def plot_lipon() -> tuple[list[str], Path]:
    data = np.loadtxt(BASE / "LiPON_transport/transport_summary.csv", delimiter=",", skiprows=1)
    temperature = data[:, 0]
    sigma_ne = data[:, 4] / 1000.0
    x = 1000.0 / temperature
    y = np.log(sigma_ne * temperature)
    slope, intercept, _ = linear_fit(x, y)
    ea_nep = -slope * KB_EV * 1000.0

    ea_exp = 0.550
    sigma_exp_300 = 2.3e-6
    x300 = 1000.0 / 300.0
    y300 = np.log(sigma_exp_300 * 300.0)
    xx_exp = np.linspace(x.min(), x300, 250)
    y_exp = y300 - (ea_exp / KB_EV) * (xx_exp / 1000.0 - 1.0 / 300.0)

    fig, ax = plt.subplots(figsize=(8.8, 5.8667), dpi=180)
    xx = np.linspace(x.min(), x.max(), 200)
    ax.plot(xx, slope * xx + intercept, color=BLUE, lw=3.4)
    ax.scatter(x, y, color=BLUE, s=82, zorder=3,
               label=fr"NEP89 ($E_a={ea_nep:.3f}$ eV)")
    ax.plot(xx_exp, y_exp, color=BLACK, lw=3.4, ls=":",
            label=fr"Thin-film experiment ($E_a={ea_exp:.3f}$ eV)")
    ax.plot(x300, y300, marker="s", ms=9, mfc="white", mec=BLACK, mew=2.0)
    style(ax, r"LiPON — Arrhenius analysis of Li-ion conductivity",
          r"$\ln[\sigma T\;(mathrm{S\,cm^{-1}\,K})]$")
    fig.tight_layout()
    source = write_source(
        "LiPON_Arrhenius_plot_data.csv",
        ["series", "T_K", "sigma_S_cm", "ln_sigmaT"],
        [("NEP89_conditional_NE", t, s, yy) for t, s, yy in zip(temperature, sigma_ne, y)]
        + [("Bates_1996_experiment_anchor", 300.0, sigma_exp_300, y300)],
    )
    return save(fig, "32_LiPON_Arrhenius_comparison"), source


def main() -> None:
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "none", "pdf.fonttype": 42})
    outputs = []
    sources = []
    for function in (plot_lzoc, plot_lszc, plot_li3ps4, plot_lipon):
        created, source = function()
        outputs.extend(created)
        sources.append(str(source.relative_to(ROOT)))
    inventory = write_source(
        "activation_energy_inventory.csv",
        ["material", "model_Ea_eV", "reference_Ea_eV", "reference_type", "status"],
        [
            ("Li3YCl6", 0.302, 0.400, "experiment", "formal comparison; MACE value shown here"),
            ("LiNbOCl4", 0.313, 0.240, "experiment", "formal comparison; MACE value shown here"),
            ("LZOC", "", "", "Hussain 2024 AIMD D(T)", "no formal Ea assigned"),
            ("LSZC", 0.3508458941, 0.330, "experiment", "formal comparison"),
            ("Li3PS4", 0.4188975679, 0.470, "Chen 2025 DeePMD", "500-900 K comparison"),
            ("LiPON", 0.4280011130, 0.550, "thin-film experiment", "D-based Ea; conductivity-based Ea is 0.415 eV"),
        ],
    )
    sources.append(str(inventory.relative_to(ROOT)))
    provenance = {
        "operation": "Arrhenius-coordinate comparisons; no MD or source-data refitting outside the displayed regressions.",
        "outputs": outputs,
        "sources": sources,
        "sha256": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in outputs + sources},
    }
    (SOURCE / "amorphous_arrhenius_provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    manifest_path = FIG / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    stems = {Path(path).stem for path in outputs}
    manifest["assets"] = [item for item in manifest["assets"] if Path(item["file"]).stem not in stems]
    for path in outputs:
        p = ROOT / path
        manifest["assets"].append({
            "file": p.name,
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            "source": "scripts/structures/plot_amorphous_arrhenius_comparisons.py",
        })
    manifest["figure_groups"] = len({Path(item["file"]).stem for item in manifest["assets"]})
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Created {len(outputs)} figure files and {len(sources)} source tables")


if __name__ == "__main__":
    main()
