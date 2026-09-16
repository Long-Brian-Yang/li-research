"""Render the current Li3PS4 R1 report figures from compact remote results."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results" / "amorphous_review_20260915"
DATA = BASE / "Li3PS4_R1_transport"
REFERENCE = BASE / "final_comparisons"
OUTPUT = ROOT / "docs" / "materials" / "figures"
TEMPERATURES = np.array([300.0, 500.0, 700.0, 900.0])
COLORS = ["#654394", "#31688e", "#35a77b", "#d73027"]
BLUE, RED, GRAY = "#31688e", "#d73027", "#727272"


def reference_rows(temperatures, model_d, reference_d):
    temperatures = np.asarray(temperatures, dtype=float)
    model_d = np.asarray(model_d, dtype=float)
    reference_d = np.asarray(reference_d, dtype=float)
    return np.column_stack([temperatures, model_d, reference_d, model_d / reference_d])


def load_csv(path: Path) -> np.ndarray:
    values = np.loadtxt(path, delimiter=",", skiprows=1)
    assert values.ndim == 2 and np.isfinite(values).all(), path
    return values


def load_reference_csv(path: Path, usecols) -> np.ndarray:
    values = np.genfromtxt(path, delimiter=",", skip_header=1, usecols=usecols)
    values = np.atleast_2d(values)
    values = values[np.isfinite(values).all(axis=1)]
    assert len(values), path
    return values


def finish(fig, name):
    for index, axis in enumerate(fig.axes):
        axis.text(
            -0.13,
            1.045,
            chr(97 + index),
            transform=axis.transAxes,
            fontweight="bold",
            fontsize=16,
        )
        axis.grid(alpha=0.16)
        axis.set_axisbelow(True)
        if axis.get_legend():
            axis.legend(frameon=False, fontsize=11.5)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    fig.canvas.draw()
    for extension in ("png", "pdf", "svg"):
        path = OUTPUT / f"{name}.{extension}"
        fig.savefig(path, dpi=300, bbox_inches="tight")
        if extension == "svg":
            path.write_text("\n".join(line.rstrip() for line in path.read_text().splitlines()) + "\n")
    plt.close(fig)


def main():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 13,
            "axes.titlesize": 16,
            "axes.labelsize": 14,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "axes.linewidth": 1.5,
            "lines.linewidth": 2.5,
            "legend.frameon": False,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
        }
    )
    summary = json.loads((DATA / "summary.json").read_text())

    fig, axes = plt.subplots(2, 2, figsize=(12, 9.3), layout="constrained")
    for axis, temperature, color in zip(axes.ravel(), TEMPERATURES.astype(int), COLORS):
        values = load_csv(DATA / f"{temperature}K_MSD.csv")
        axis.plot(values[:, 0], values[:, 1], color=color, label="NEP89")
        axis.set(
            title=f"{temperature} K",
            xlabel="Lag time (ps)",
            ylabel="Li MSD (Å²)",
            xlim=(0, 200),
            ylim=(0, None),
        )
        axis.legend()
    finish(fig, "05_LPS_MSD")

    model_d = []
    framework = []
    for temperature in TEMPERATURES.astype(int):
        result = summary["results"][str(temperature)]
        model_d.append(
            next(
                fit["D_cm2_s"]
                for fit in result["fits"]
                if fit["lo_ps"] == 20 and fit["hi_ps"] == 80
            )
        )
        framework.append([result["MSD80_A2"]["P"], result["MSD80_A2"]["S"]])
    model_d = np.asarray(model_d)
    framework = np.asarray(framework)
    source = load_reference_csv(REFERENCE / "Chen2025_Fig._3a.csv", (0, 2))
    reference_d = np.asarray(
        [source[np.argmin(np.abs(source[:, 0] - 1000.0 / temperature)), 1] for temperature in TEMPERATURES]
    )
    comparison = reference_rows(TEMPERATURES, model_d, reference_d)
    np.savetxt(
        DATA / "reference_comparison.csv",
        comparison,
        delimiter=",",
        header="T_K,NEP89_apparent_D_cm2_s,Chen2025_glass_D_cm2_s,NEP89_over_Chen",
        comments="",
    )

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.65), layout="constrained")
    axes[0].plot(
        TEMPERATURES[1:],
        model_d[1:],
        "o-",
        color=BLUE,
        label="NEP89",
    )
    axes[0].plot(
        TEMPERATURES[0],
        model_d[0],
        marker="o",
        markerfacecolor="white",
        markeredgecolor=BLUE,
        markeredgewidth=2,
        linestyle="none",
        label="NEP89: 300 K unresolved",
    )
    axes[0].plot(
        TEMPERATURES,
        reference_d,
        "s--",
        color=GRAY,
        label="Chen 2025: glass DeePMD",
    )
    axes[0].set(
        title="Same-temperature diffusion comparison",
        xlabel="Temperature (K)",
        ylabel="D (cm²/s)",
        yscale="log",
        xticks=TEMPERATURES,
    )
    axes[0].legend()
    for index, (element, color, style) in enumerate((("P", BLUE, "--"), ("S", RED, "-"))):
        axes[1].plot(
            TEMPERATURES,
            framework[:, index],
            marker="o",
            color=color,
            linestyle=style,
            label=element,
        )
    axes[1].set(
        title="Framework motion at 80 ps lag",
        xlabel="Temperature (K)",
        ylabel="MSD (Å²)",
        yscale="log",
        xticks=TEMPERATURES,
    )
    axes[1].legend()
    finish(fig, "06_LPS_reference")

    r1_rdf = load_csv(DATA / "300K_late_structure.csv")
    chen_rdf = load_reference_csv(REFERENCE / "Chen2025_Fig._1e.csv", (0, 2))
    r1_angle = load_csv(DATA / "300K_late_angles.csv")
    chen_angle = load_reference_csv(REFERENCE / "Chen2025_Fig._1f.csv", (0, 2))
    chen_angle_density = chen_angle[:, 1] / np.trapz(chen_angle[:, 1], chen_angle[:, 0])
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.65), layout="constrained")
    axes[0].plot(r1_rdf[:, 0], r1_rdf[:, 1], color=BLUE, label="NEP89 glass")
    axes[0].plot(
        chen_rdf[:, 0],
        chen_rdf[:, 1],
        color=RED,
        linestyle="--",
        label="Chen 2025: glass DeePMD",
    )
    axes[0].set(title="Li–S radial distribution", xlabel="r (Å)", ylabel="g(r)", xlim=(0, 5))
    axes[0].legend()
    axes[1].plot(r1_angle[:, 0], r1_angle[:, 1], color=BLUE, label="NEP89 glass")
    axes[1].plot(
        chen_angle[:, 0],
        chen_angle_density,
        color=RED,
        linestyle="--",
        label="Chen 2025: glass DeePMD",
    )
    axes[1].set(
        title="S–P–S angle distribution",
        xlabel="Angle (°)",
        ylabel="Probability density (degree⁻¹)",
        xlim=(60, 160),
    )
    axes[1].legend()
    finish(fig, "07_LPS_structure")

    plot_summary = {
        "figure_conclusion": "R1 retains local PS4 geometry, while high-temperature Li diffusion remains above the Chen 2025 glass reference and 300 K is unresolved.",
        "archetype": "quantitative grid",
        "exports": ["05_LPS_MSD", "06_LPS_reference", "07_LPS_structure"],
        "reference_comparison": comparison.tolist(),
        "sources_sha256": {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in [DATA / "summary.json", REFERENCE / "Chen2025_Fig._3a.csv", REFERENCE / "Chen2025_Fig._1e.csv", REFERENCE / "Chen2025_Fig._1f.csv"]
        },
    }
    (DATA / "plot_summary.json").write_text(json.dumps(plot_summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
