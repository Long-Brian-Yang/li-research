#!/usr/bin/env python3
"""Draw standardized material-specific workflows for the Material Review.

The diagrams are intentionally schematic: they connect the literature
benchmark to the model, MD protocol, analyses and bounded conclusion without
encoding scheduler, seed or fit-window details.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "materials" / "figures"

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica", "sans-serif"],
        "font.size": 8,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
    }
)


WORKFLOWS = {
    "Li3YCl6": {
        "title": "Li₃YCl₆ — crystalline transport benchmark",
        "subtitle": "From experimental reference to a controlled three-model MD comparison",
        "accent": "#2F6B9A",
        "nodes": [
            ("Literature benchmark", "Asano et al. (2018)\nExperimental chloride SSE\nRoom-temperature transport"),
            ("Structure and models", "Explicit Li/Y ordering\n2 × 2 × 2 supercell\n240 atoms; three NNPs"),
            ("MD protocol", "400–1000 K; NVT\n1 fs; 50 ps equilibration\n500 ps production"),
            ("Analysis", "Li MSD and D(T)\nArrhenius Eₐ\nConditional σNE"),
            ("Bounded conclusion", "Thermal trend reproduced\nAbsolute transport is\nstrongly model dependent"),
        ],
    },
    "LiNbOCl4": {
        "title": "LiNbOCl₄ — crystalline oxyhalide benchmark",
        "subtitle": "Testing transfer of the same workflow to mixed O²⁻/Cl⁻ chemistry",
        "accent": "#3B7F78",
        "nodes": [
            ("Literature benchmark", "Tanaka et al. (2023)\n10.4 mS cm⁻¹ at room T\nExperimental Eₐ = 0.240 eV"),
            ("Structure and models", "Periodic oxyhalide model\n224 atoms; 32 Li\nMACE / SevenNet / M3GNet"),
            ("MD protocol", "600–1200 K; NVT\n1 fs; 50 ps equilibration\n500 ps production"),
            ("Analysis", "Li MSD and D(T)\nln(σNET) Arrhenius plot\n300 K extrapolation"),
            ("Bounded conclusion", "Experimental slope included\nModel ordering differs\nfrom Li₃YCl₆"),
        ],
    },
    "LZOC": {
        "title": "Li₁.₇₅ZrCl₄.₇₅O₀.₅ — amorphous AIMD comparison",
        "subtitle": "The oxychloride main line links experimental relevance to matched-temperature AIMD",
        "accent": "#4A6FA5",
        "nodes": [
            ("Literature benchmark", "Hu et al. (2023): experiment\nHussain et al. (2024): AIMD\n340 / 360 / 380 K"),
            ("Structure and model", "Integer occupancy model\n192 atoms; periodic glass\nPretrained NEP89"),
            ("MD protocol", "340 / 360 / 380 K\nNVT Nosé–Hoover chain\n2 fs; 300 ps production"),
            ("Analysis", "Li and framework MSD\nD(T), RDF and CN\nDisplacement distributions"),
            ("Bounded conclusion", "NEP89 D below AIMD\nLocal geometry persists\nMechanism not yet unique"),
        ],
    },
    "LSZC": {
        "title": "0.5Li₂SO₄–ZrCl₄ — experiment–structure–MLIP comparison",
        "subtitle": "A sulfate-containing glass tests transport and local structure simultaneously",
        "accent": "#8A6A35",
        "nodes": [
            ("Literature benchmark", "Tang et al. (2026)\nExperiment + scattering\nAIMD and tuned MACE"),
            ("Structure and model", "Cluster-based packing\nLi₃₂Zr₃₂Cl₁₂₈S₁₆O₆₄\n272 atoms; NEP89"),
            ("MD protocol", "320 / 330 / 340 / 350 K\n50 ps NVT equilibration\n300 ps NVT production"),
            ("Analysis", "MSD, D(T), σNE and Eₐ\nRDF and coordination\nLi–O environment / mobility"),
            ("Bounded conclusion", "Sulfate motif retained\nTransport fit is literature-close\nLong-range diffusion limited"),
        ],
    },
    "Li3PS4": {
        "title": "Li₃PS₄ glass — sulfide transferability test",
        "subtitle": "Moving beyond oxychlorides tests whether structural and transport agreement persist",
        "accent": "#7965A8",
        "nodes": [
            ("Literature benchmark", "Mirmira et al. (2021)\nExperimental glass\nChen et al. (2025): DeePMD"),
            ("Structure and model", "Author-data precursor\nLi₁₉₂P₆₄S₂₅₆; 512 atoms\nMelt–quench with NEP89"),
            ("MD protocol", "300 / 500 / 700 / 900 K\n50 ps NPT equilibration\n200 ps NVT production"),
            ("Analysis", "Li MSD and D(T)\nLi–S / P–S RDF and CN\nFramework motion"),
            ("Bounded conclusion", "Local motifs partly retained\nTransport magnitude differs\nDedicated work remains"),
        ],
    },
    "LiPON": {
        "title": "LiPON — phosphate–oxynitride applicability limit",
        "subtitle": "A chemically constrained network provides the most stringent pretrained-potential test",
        "accent": "#9A5B63",
        "nodes": [
            ("Literature benchmark", "Lacivita et al. (2018)\nNeutron / IR + AIMD\nSeth et al. (2025): NequIP"),
            ("Structure and model", "Li₄₇P₁₆O₅₆N₅\n124 atoms; Preparation B\nApical + bridging N"),
            ("MD protocol", "600 / 900 / 1200 / 1500 K\n50 ps equilibration\n300–600 ps production"),
            ("Analysis", "MSD, D(T), σNE and Eₐ\nP–O / P–N / Li RDF\nNetwork-topology checks"),
            ("Bounded conclusion", "Thermal trend reproduced\nD strongly overestimated\nTransferability limit exposed"),
        ],
    },
}


BOX_FILLS = ["#EAF2F8", "#EEF3F4", "#F5F5F3", "#EEF4EE", "#F6F0EA"]
STAGE_LABELS = ["Literature", "Structure", "MD protocol", "Analysis", "Conclusion"]


def draw_workflow(key: str, spec: dict[str, object]) -> None:
    fig, ax = plt.subplots(figsize=(11.8, 3.55), constrained_layout=False)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    accent = str(spec["accent"])
    ax.add_patch(
        FancyBboxPatch(
            (0.02, 0.83),
            0.96,
            0.11,
            boxstyle="round,pad=0.008,rounding_size=0.018",
            facecolor=accent,
            edgecolor=accent,
            linewidth=0,
        )
    )
    ax.text(0.04, 0.885, str(spec["title"]), color="white", fontsize=13.2, fontweight="bold", va="center")
    ax.text(0.04, 0.785, str(spec["subtitle"]), color="#39434A", fontsize=8.8, va="center")

    left = 0.025
    gap = 0.018
    width = (0.95 - 4 * gap) / 5
    bottom = 0.13
    height = 0.55

    for idx, (_, body) in enumerate(spec["nodes"], start=1):
        x = left + (idx - 1) * (width + gap)
        ax.add_patch(
            FancyBboxPatch(
                (x, bottom),
                width,
                height,
                boxstyle="round,pad=0.010,rounding_size=0.018",
                facecolor=BOX_FILLS[idx - 1],
                edgecolor="#AEB8BE",
                linewidth=0.9,
            )
        )
        ax.add_patch(
            FancyBboxPatch(
                (x + 0.012, bottom + height - 0.093),
                0.035,
                0.060,
                boxstyle="round,pad=0.004,rounding_size=0.010",
                facecolor=accent,
                edgecolor=accent,
                linewidth=0,
            )
        )
        ax.text(x + 0.0295, bottom + height - 0.063, str(idx), color="white", fontsize=8.2,
                fontweight="bold", ha="center", va="center")
        ax.text(x + 0.057, bottom + height - 0.063, STAGE_LABELS[idx - 1], color="#1E2A31", fontsize=8.4,
                fontweight="bold", va="center")
        ax.plot([x + 0.015, x + width - 0.015], [bottom + height - 0.118] * 2,
                color="#C8D0D4", linewidth=0.7)
        ax.text(x + width / 2, bottom + 0.245, body, color="#2D3940", fontsize=7.75,
                ha="center", va="center", linespacing=1.45)

        if idx < 5:
            start = (x + width + 0.002, bottom + height / 2)
            end = (x + width + gap - 0.002, bottom + height / 2)
            ax.add_patch(
                FancyArrowPatch(
                    start,
                    end,
                    arrowstyle="-|>",
                    mutation_scale=10,
                    linewidth=1.25,
                    color=accent,
                    shrinkA=0,
                    shrinkB=0,
                )
            )

    stem = OUT / f"material_workflow_{key}"
    for suffix, kwargs in {
        ".png": {"dpi": 300},
        ".pdf": {},
        ".svg": {},
    }.items():
        path = stem.with_suffix(suffix)
        fig.savefig(path, bbox_inches="tight", pad_inches=0.04, **kwargs)
        if suffix == ".svg":
            path.write_text("\n".join(line.rstrip() for line in path.read_text().splitlines()) + "\n")
    plt.close(fig)


def update_manifest() -> None:
    manifest_path = OUT / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {"assets": []}
    manifest["assets"] = [
        item for item in manifest.get("assets", [])
        if not str(item.get("file", "")).startswith("material_workflow_")
    ]
    for key in WORKFLOWS:
        for suffix in (".png", ".pdf", ".svg"):
            path = OUT / f"material_workflow_{key}{suffix}"
            manifest["assets"].append(
                {
                    "file": path.name,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "source": "scripts/structures/plot_material_workflows.py",
                }
            )
    manifest["figure_groups"] = len(
        {Path(item["file"]).stem for item in manifest["assets"]}
    )
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for key, spec in WORKFLOWS.items():
        draw_workflow(key, spec)
    update_manifest()


if __name__ == "__main__":
    main()
