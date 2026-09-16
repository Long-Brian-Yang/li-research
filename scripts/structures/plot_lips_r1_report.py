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


def normalize_angle_density(angle_values):
    area = np.trapezoid(angle_values[:, 1], angle_values[:, 0])
    assert np.isfinite(area) and area > 0
    return angle_values[:, 1] / area


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


def style_figure(fig):
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
        legend = axis.get_legend()
        if legend:
            legend.get_frame().set_visible(False)
            for label in legend.get_texts():
                label.set_fontsize(11.5)


def finish(fig, name):
    style_figure(fig)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    fig.canvas.draw()
    for extension in ("png", "pdf", "svg"):
        path = OUTPUT / f"{name}.{extension}"
        fig.savefig(path, dpi=300, bbox_inches="tight")
        if extension == "svg":
            path.write_text("\n".join(line.rstrip() for line in path.read_text().splitlines()) + "\n")
    plt.close(fig)


def build_reference_figure(temperatures, model_d, reference_d, framework):
    """Build the report-width Li diffusion and host-framework comparison."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.65), layout="constrained")
    axes[0].plot(
        temperatures,
        model_d,
        "o-",
        color=BLUE,
        label="NEP89",
    )
    axes[0].plot(
        temperatures,
        reference_d,
        "s--",
        color=GRAY,
        label="Chen et al. (2025), DeePMD",
    )
    axes[0].set(
        title="Li-ion self-diffusion",
        xlabel="Temperature (K)",
        ylabel=r"$D_{\mathrm{Li}}$ (cm$^2$ s$^{-1}$)",
        yscale="log",
        xticks=temperatures,
        xlim=(270, 930),
    )
    axes[0].legend(loc="upper left")

    for index, (element, color, style) in enumerate((("P", BLUE, "--"), ("S", RED, "-"))):
        axes[1].plot(
            temperatures,
            framework[:, index],
            marker="o",
            color=color,
            linestyle=style,
            label=element,
        )
    axes[1].set(
        title="Host-framework displacement at 80 ps",
        xlabel="Temperature (K)",
        ylabel=r"MSD at 80 ps ($\mathrm{\AA^2}$)",
        yscale="log",
        xticks=temperatures,
        xlim=(270, 930),
    )
    axes[1].legend(loc="upper left")
    return fig


def build_structure_figure(rdf, reference_rdf, angles, reference_angles):
    """Build local-structure panels with legends in curve-free regions."""
    reference_angle_density = normalize_angle_density(reference_angles)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.65), layout="constrained")
    axes[0].plot(rdf[:, 0], rdf[:, 1], color=BLUE, label="NEP89 (this work)")
    axes[0].plot(
        reference_rdf[:, 0],
        reference_rdf[:, 1],
        color=RED,
        linestyle="--",
        label="Chen et al., DeePMD",
    )
    axes[0].set(title="Li–S radial distribution", xlabel="r (Å)", ylabel="g(r)", xlim=(0, 5))
    axes[1].plot(angles[:, 0], angles[:, 1], color=BLUE, label="NEP89 (this work)")
    axes[1].plot(
        reference_angles[:, 0],
        reference_angle_density,
        color=RED,
        linestyle="--",
        label="Chen et al., DeePMD",
    )
    axes[1].set(
        title="S–P–S angle distribution",
        xlabel="Angle (°)",
        ylabel="Probability density (degree⁻¹)",
        xlim=(60, 160),
    )
    for axis in axes:
        axis.legend(loc="upper left")
    return fig


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

    fig = build_reference_figure(TEMPERATURES, model_d, reference_d, framework)
    finish(fig, "06_LPS_transport_framework")

    r1_rdf = load_csv(DATA / "300K_late_structure.csv")
    chen_rdf = load_reference_csv(REFERENCE / "Chen2025_Fig._1e.csv", (0, 2))
    r1_angle = load_csv(DATA / "300K_late_angles.csv")
    chen_angle = load_reference_csv(REFERENCE / "Chen2025_Fig._1f.csv", (0, 2))
    fig = build_structure_figure(r1_rdf, chen_rdf, r1_angle, chen_angle)
    finish(fig, "07_LPS_structural_comparison")

    plot_summary = {
        "figure_conclusion": "R1 retains local PS4 geometry, while its finite-time apparent Li diffusion remains above the Chen 2025 glass reference across 300–900 K.",
        "archetype": "quantitative grid",
        "exports": ["05_LPS_MSD", "06_LPS_transport_framework", "07_LPS_structural_comparison"],
        "reference_comparison": comparison.tolist(),
        "sources_sha256": {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in [DATA / "summary.json", REFERENCE / "Chen2025_Fig._3a.csv", REFERENCE / "Chen2025_Fig._1e.csv", REFERENCE / "Chen2025_Fig._1f.csv"]
        },
    }
    (DATA / "plot_summary.json").write_text(json.dumps(plot_summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
