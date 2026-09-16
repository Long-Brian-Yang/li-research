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
from matplotlib.patches import FancyBboxPatch


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
            ("Literature", "Asano et al. (2018)\nExperiment: chloride SSE\nRT conductivity >1 mS cm⁻¹"),
            ("Model & software", "Explicit Li/Y ordering\n2 × 2 × 2; 240 atoms\nMACE / SevenNet / M3GNet\nLAMMPS; 1 GPU per run"),
            ("MD conditions", "T: 400 / 600 / 800 / 1000 K\nEnsemble: fixed-cell NVT\ndt: 1 fs\nEquil.: 50 ps\nProduction: 500 ps"),
            ("Analysis", "Li MSD → D(T)\nArrhenius fit → Eₐ\n300 K extrapolation\nConditional σNE"),
            ("Conclusion", "Thermal trend reproduced\nAbsolute transport is\nstrongly model dependent"),
        ],
    },
    "LiNbOCl4": {
        "title": "LiNbOCl₄ — crystalline oxyhalide benchmark",
        "subtitle": "Testing transfer of the same workflow to mixed O²⁻/Cl⁻ chemistry",
        "accent": "#3B7F78",
        "nodes": [
            ("Literature", "Tanaka et al. (2023)\nRT σ = 10.4 mS cm⁻¹\nExperimental Eₐ = 0.240 eV"),
            ("Model & software", "Periodic oxyhalide model\n224 atoms; 32 Li\nMACE / SevenNet / M3GNet\nLAMMPS; 1 GPU per run"),
            ("MD conditions", "T: 600 / 800 / 1000 / 1200 K\nEnsemble: fixed-cell NVT\ndt: 1 fs\nEquil.: 50 ps\nProduction: 500 ps"),
            ("Analysis", "Li MSD → D(T)\nln(σNET) vs 1000/T\nArrhenius fit → Eₐ\n300 K extrapolation"),
            ("Conclusion", "Experimental slope included\nModel ordering differs\nfrom Li₃YCl₆"),
        ],
    },
    "LZOC": {
        "title": "Li₁.₇₅ZrCl₄.₇₅O₀.₅ — amorphous AIMD comparison",
        "subtitle": "The oxychloride main line links experimental relevance to matched-temperature AIMD",
        "accent": "#4A6FA5",
        "nodes": [
            ("Literature", "Hu et al. (2023): experiment\nHussain et al. (2024): AIMD\nReference T: 340 / 360 / 380 K"),
            ("Model & software", "Integer-occupancy glass\n192 atoms; periodic cell\nPretrained NEP89\nGPUMD"),
            ("MD conditions", "T: 340 / 360 / 380 K\nEnsemble: fixed-cell NVT\nThermostat: NHC; τT = 100 fs\ndt: 2 fs\nProduction: 300 ps"),
            ("Analysis", "Li / host MSD → D(T)\nRDF and coordination\nRadial displacement\nDirect AIMD D comparison"),
            ("Conclusion", "NEP89 D below AIMD\nLocal geometry persists\nMechanism not yet unique"),
        ],
    },
    "LSZC": {
        "title": "0.5Li₂SO₄–ZrCl₄ — experiment–structure–MLIP comparison",
        "subtitle": "A sulfate-containing glass tests transport and local structure simultaneously",
        "accent": "#8A6A35",
        "nodes": [
            ("Literature", "Tang et al. (2026)\nExperiment + total scattering\nAIMD + tuned MACE\nσ30°C = 1.5 mS cm⁻¹"),
            ("Model & software", "Cluster-packed glass\nLi₃₂Zr₃₂Cl₁₂₈S₁₆O₆₄\n272 atoms; fixed cell\nNEP89 / GPUMD"),
            ("MD conditions", "T: 320 / 330 / 340 / 350 K\nEnsemble: NVT (MTTK)\nτT = 100 fs; dt = 0.5 fs\nEquil.: 50 ps\nProduction: 300 ps"),
            ("Analysis", "MSD → D(T), σNE and Eₐ\nRDF and coordination\nLi–O environment / mobility\nExperiment / tuned-MACE comparison"),
            ("Conclusion", "Sulfate motif retained\nFit can approach literature\nLong-range diffusion limited"),
        ],
    },
    "Li3PS4": {
        "title": "Li₃PS₄ glass — sulfide transferability test",
        "subtitle": "Moving beyond oxychlorides tests whether structural and transport agreement persist",
        "accent": "#7965A8",
        "nodes": [
            ("Literature", "Mirmira et al. (2021): experiment\nChen et al. (2025): DeePMD\nReference T: 300–900 K"),
            ("Model & preparation", "Li₁₉₂P₆₄S₂₅₆; 512 atoms\nNEP89 / GPUMD\n1500 K NPT: 100 ps\nCool 2.5 K ps⁻¹ → 300 K\n300 K hold: 20 ps"),
            ("Transport MD", "T: 300 / 500 / 700 / 900 K\nRamp: 10 ps\nNPT (1 bar): 50 ps\nNVT production: 200 ps\ndt: 0.5 fs"),
            ("Analysis", "Li MSD → D(T)\nLi–S / P–S RDF and CN\nS–P–S angle\nFramework motion"),
            ("Conclusion", "Local motifs partly retained\nTransport magnitude differs\nDedicated work remains"),
        ],
    },
    "LiPON": {
        "title": "LiPON — phosphate–oxynitride applicability limit",
        "subtitle": "A chemically constrained network provides the most stringent pretrained-potential test",
        "accent": "#9A5B63",
        "nodes": [
            ("Literature", "Lacivita et al. (2018)\nNeutron / IR + AIMD\nSeth et al. (2025): NequIP\nBates et al. (1996): experiment"),
            ("Model & preparation", "Li₄₇P₁₆O₅₆N₅; 124 atoms\nPreparation B; NEP89 / GPUMD\n2000 K hold: 10 ps\nQuench → 250 K: 7 ps\n250 K hold + release: 20 + 20 ps"),
            ("Transport MD", "T: 600 / 900 / 1200 / 1500 K\nRamp: 10 ps; NPT: 50 ps\nNVT: 300 ps\n600 K primary run: 600 ps\ndt: 0.5 fs"),
            ("Analysis", "MSD → D(T), σNE and Eₐ\nP–O / P–N / Li RDF\nN topology and contacts\nNequIP / experiment comparison"),
            ("Conclusion", "Thermal trend reproduced\nD strongly overestimated\nTransferability limit exposed"),
        ],
    },
}


BOX_FILLS = ["#EAF2F8", "#EEF3F4", "#F5F5F3", "#EEF4EE", "#F6F0EA"]
def draw_workflow(key: str, spec: dict[str, object]) -> None:
    fig, ax = plt.subplots(figsize=(13.2, 4.25), constrained_layout=False)
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
    bottom = 0.095
    height = 0.61

    for idx, (stage, body) in enumerate(spec["nodes"], start=1):
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
        ax.text(x + 0.057, bottom + height - 0.063, stage, color="#1E2A31", fontsize=8.15,
                fontweight="bold", va="center")
        ax.plot([x + 0.015, x + width - 0.015], [bottom + height - 0.118] * 2,
                color="#C8D0D4", linewidth=0.7)
        ax.text(x + 0.018, bottom + 0.255, body, color="#2D3940", fontsize=7.35,
                ha="left", va="center", linespacing=1.40)

    for idx in range(4):
        x = left + idx * (width + gap)
        ax.text(
            x + width + gap / 2,
            bottom + height / 2,
            "›",
            color=accent,
            fontsize=19,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=20,
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
