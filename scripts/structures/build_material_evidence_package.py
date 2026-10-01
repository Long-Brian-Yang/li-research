"""Build compact, provenance-rich structures and trajectory evidence.

The numerical analyses continue to use the complete source trajectories.  This
script exports uniformly sampled, visualization-friendly extended XYZ files so
the structures behind the report remain inspectable on GitHub without adding
multi-gigabyte raw trajectory data to the repository.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import numpy as np
from ase import Atoms
from ase.io import iread, read, write


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "materials/evidence"


def uniform_indices(total_frames: int, target_frames: int) -> list[int]:
    """Return increasing, approximately uniform indices including endpoints."""
    if total_frames < 1 or target_frames < 1:
        raise ValueError("frame counts must be positive")
    count = min(total_frames, target_frames)
    indices = np.rint(np.linspace(0, total_frames - 1, count)).astype(int)
    return np.unique(indices).tolist()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def clean_frame(frame: Atoms, metadata: dict) -> Atoms:
    result = Atoms(
        symbols=frame.get_chemical_symbols(),
        positions=frame.positions,
        cell=frame.cell,
        pbc=frame.pbc,
    )
    result.info.update(metadata)
    return result


def apply_type_symbols(frame: Atoms, type_symbols: dict[int, str]) -> Atoms:
    """Restore element labels when a LAMMPS dump stores only type numbers."""
    result = frame.copy()
    try:
        symbols = [type_symbols[int(number)] for number in frame.numbers]
    except KeyError as error:
        raise ValueError(f"unmapped LAMMPS atom type {error.args[0]}") from error
    result.set_chemical_symbols(symbols)
    return result


def write_xyz_chunks(
    frames,
    selected_indices: list[int],
    output_dir: Path,
    stem: str,
    frame_interval_ps: float,
    max_frames_per_chunk: int,
    common_metadata: dict,
) -> list[dict]:
    """Write selected frames as bounded-size extended-XYZ chunks."""
    output_dir.mkdir(parents=True, exist_ok=True)
    selected = []
    for index in selected_indices:
        metadata = dict(common_metadata)
        metadata.update(
            source_frame_index=int(index),
            relative_time_ps=round(float(index * frame_interval_ps), 12),
        )
        selected.append(clean_frame(frames[index], metadata))

    records = []
    for start in range(0, len(selected), max_frames_per_chunk):
        chunk_frames = selected[start : start + max_frames_per_chunk]
        chunk_indices = selected_indices[start : start + max_frames_per_chunk]
        chunk_number = start // max_frames_per_chunk + 1
        path = output_dir / f"{stem}_part{chunk_number:02d}.xyz"
        write(path, chunk_frames, format="extxyz")
        records.append(
            {
                "file": path.name,
                "atom_count": len(chunk_frames[0]),
                "frame_count": len(chunk_frames),
                "source_frame_indices": [int(i) for i in chunk_indices],
                "time_ps": [round(float(i * frame_interval_ps), 12) for i in chunk_indices],
                "sha256": sha256(path),
                "size_bytes": path.stat().st_size,
            }
        )
    return records


def count_frames(path: Path, fmt: str) -> int:
    marker = b"ITEM: TIMESTEP" if fmt == "lammps-dump-text" else None
    if marker:
        with path.open("rb") as handle:
            return sum(line.startswith(marker) for line in handle)
    with path.open("rb") as handle:
        first = handle.readline()
        atom_count = int(first.strip())
        line_count = 1 + sum(1 for _ in handle)
    frame_lines = atom_count + 2
    if line_count % frame_lines:
        raise ValueError(f"incomplete XYZ frame in {path}")
    return line_count // frame_lines


def read_selected_frames(path: Path, fmt: str, indices: list[int]) -> list[Atoms]:
    selected = set(indices)
    frames = []
    kwargs = {"format": fmt} if fmt else {}
    for index, atoms in enumerate(iread(path, index=":", **kwargs)):
        if index in selected:
            frames.append(atoms)
        if index > indices[-1]:
            break
    if len(frames) != len(indices):
        raise ValueError(f"expected {len(indices)} selected frames from {path}, got {len(frames)}")
    return frames


def export_structure(source: Path, output_dir: Path, name: str, metadata: dict) -> dict:
    atoms = read(source)
    target = output_dir / f"{name}.xyz"
    output_dir.mkdir(parents=True, exist_ok=True)
    frame_metadata = dict(metadata)
    frame_metadata["report_figures"] = "; ".join(metadata["report_figures"])
    write(target, clean_frame(atoms, frame_metadata), format="extxyz")
    return {
        "file": target.name,
        "source": str(source.relative_to(ROOT)),
        "display_name": metadata["display_name"],
        "report_figures": metadata["report_figures"],
        "atom_count": len(atoms),
        "formula": atoms.get_chemical_formula(mode="metal"),
        "sha256": sha256(target),
        "size_bytes": target.stat().st_size,
    }


def export_trajectory(spec: dict) -> dict:
    source = ROOT / spec["source"]
    fmt = spec.get("format", "extxyz")
    total = count_frames(source, fmt)
    indices = uniform_indices(total, spec.get("target_frames", 101))
    frames = read_selected_frames(source, fmt, indices)
    if spec.get("type_symbols"):
        frames = [apply_type_symbols(frame, spec["type_symbols"]) for frame in frames]
    # write_xyz_chunks expects random-access frames; map compact frames to their
    # original indices while preserving source-relative time in the metadata.
    remapped = []
    for source_index, atoms in zip(indices, frames):
        metadata = dict(spec["metadata"])
        metadata.update(
            source_frame_index=int(source_index),
            relative_time_ps=round(float(source_index * spec["frame_interval_ps"]), 12),
        )
        remapped.append(clean_frame(atoms, metadata))
    out = OUTPUT / spec["directory"]
    out.mkdir(parents=True, exist_ok=True)
    records = []
    limit = spec.get("max_frames_per_chunk", 101)
    for start in range(0, len(remapped), limit):
        subset = remapped[start : start + limit]
        subset_indices = indices[start : start + limit]
        number = start // limit + 1
        path = out / f"{spec['stem']}_part{number:02d}.xyz"
        write(path, subset, format="extxyz")
        records.append(
            {
                "file": path.name,
                "atom_count": len(subset[0]),
                "frame_count": len(subset),
                "source_frame_indices": subset_indices,
                "time_ps": [round(float(i * spec["frame_interval_ps"]), 12) for i in subset_indices],
                "sha256": sha256(path),
                "size_bytes": path.stat().st_size,
            }
        )
    return {
        "id": spec["id"],
        "directory": spec["directory"],
        "display_name": spec["display_name"],
        "report_figures": spec["report_figures"],
        "source": spec["source"],
        "source_sha256": sha256(source),
        "source_format": fmt,
        "source_frame_count": total,
        "source_frame_interval_ps": spec["frame_interval_ps"],
        "export_policy": f"{len(indices)} uniformly spaced frames including endpoints",
        "purpose": spec["purpose"],
        "metadata": spec["metadata"],
        "chunks": records,
    }


STRUCTURES = [
    ("crystalline/Li3YCl6", "initial_structure", "structures/ordered/Li3YCl6/2x2x2/model_03/Li3YCl6_ordered_03_2x2x2.cif", {"material": "Li3YCl6", "role": "ordered 2x2x2 simulation input", "display_name": "Li₃YCl₆｜240原子｜2×2×2有序初期構造", "report_figures": ["01_Li3YCl6_three_model_MSD", "03_Li3YCl6_Arrhenius"]}),
    ("crystalline/LiNbOCl4", "initial_structure", "structures/ordered/LiNbOCl4/2x2x3/LiNbOCl4_ordered_2x2x3.cif", {"material": "LiNbOCl4", "role": "ordered 2x2x3 simulation input", "display_name": "LiNbOCl₄｜336原子｜2×2×3有序初期構造", "report_figures": ["02_LiNbOCl4_three_model_MSD", "04_LiNbOCl4_Arrhenius"]}),
    ("amorphous/MACE_NEP_benchmark", "common_300K_structure", "materials/candidates/LZOC/structure_equilibrated_300K.cif", {"material": "Li1.75ZrCl4.75O0.5", "role": "common 300 K benchmark structure", "display_name": "LZOC MACE–NEP比較｜共通300 K初期構造", "report_figures": ["09_MACE_NEP_runtime_density"]}),
    ("amorphous/LZOC", "construction_initial", "materials/candidates/LZOC_Hussain2024/seed_192/initial_structure.cif", {"material": "Li1.75ZrCl4.75O0.5", "role": "literature-aligned construction input", "display_name": "LZOC｜192原子｜文献条件に合わせた構築初期構造", "report_figures": ["01_LZOC_transport", "15_LZOC_RDF", "16_LZOC_coordination"]}),
    ("amorphous/LZOC", "analysis_start", "results/amorphous_review_20260915/source/LZOC300/nhc300_340K_8676684/model.xyz", {"material": "Li1.75ZrCl4.75O0.5", "role": "300 ps transport-series start", "display_name": "LZOC｜NEP89輸送系列の開始構造", "report_figures": ["01_LZOC_transport", "14_LZOC_species_MSD", "15_LZOC_RDF", "16_LZOC_coordination", "17_LZOC_radial_displacement"]}),
    ("amorphous/LSZC", "construction_relaxed", "materials/candidates/LSZC/packed_272/relaxed.cif", {"material": "0.5Li2SO4-ZrCl4", "role": "relaxed 272-atom cluster-packed structure", "display_name": "LSZC｜272原子｜団簇充填後の緩和構造", "report_figures": ["18_LSZC_transport_comparison", "19_LSZC_partial_RDF", "27_LSZC_PDF_and_Zr_coordination"]}),
    ("amorphous/LSZC", "analysis_start", "results/amorphous_review_20260915/source/LSZC_matched4t/R2_320K/production/model.xyz", {"material": "0.5Li2SO4-ZrCl4", "role": "common-cell transport-series start", "display_name": "LSZC｜NEP89共通セル輸送系列の開始構造", "report_figures": ["18_LSZC_transport_comparison", "19_LSZC_partial_RDF", "20_LSZC_coordination_mobility", "27_LSZC_PDF_and_Zr_coordination"]}),
    ("amorphous/Li3PS4", "construction_initial", "materials/candidates/Li3PS4_glass/input/initial.cif", {"material": "Li3PS4", "role": "glass construction input", "display_name": "Li₃PS₄｜512原子｜ガラス構造の構築入力", "report_figures": ["05_Li3PS4_lithium_MSD", "07_Li3PS4_local_structure"]}),
    ("amorphous/Li3PS4", "analysis_start", "results/amorphous_review_20260915/source/Li3PS4_R1_transport/300K/production/model.xyz", {"material": "Li3PS4", "role": "R1 transport-series start", "display_name": "Li₃PS₄｜NEP89輸送系列の開始構造", "report_figures": ["05_Li3PS4_lithium_MSD", "06_Li3PS4_diffusion_framework_MSD", "07_Li3PS4_local_structure", "28_Li3PS4_dynamic_heterogeneity"]}),
    ("amorphous/LiPON", "construction_initial", "materials/candidates/LiPON/input/initial.cif", {"material": "LiPON", "role": "Preparation-B construction input", "display_name": "LiPON｜124原子｜Preparation B構築入力", "report_figures": ["21_LiPON_glass_structure", "22_LiPON_preparation_RDF", "08_LiPON_nitrogen_distance"]}),
    ("amorphous/LiPON", "analysis_start", "results/amorphous_review_20260915/source/LiPON_transport/bulk_transport_600K_8679521/production/model.xyz", {"material": "LiPON", "role": "transport-series start", "display_name": "LiPON｜NEP89輸送系列の開始構造", "report_figures": ["23_LiPON_lithium_MSD", "24_LiPON_transport_comparison", "25_LiPON_temperature_RDF"]}),
]


def report_figures_for(identifier: str) -> list[str]:
    if identifier.startswith("Li3YCl6_"):
        return ["01_Li3YCl6_three_model_MSD", "03_Li3YCl6_Arrhenius"]
    if identifier.startswith("LiNbOCl4_"):
        return ["02_LiNbOCl4_three_model_MSD", "04_LiNbOCl4_Arrhenius"]
    if identifier.startswith("benchmark_"):
        return ["09_MACE_NEP_runtime_density"]
    if identifier.startswith("LZOC_"):
        return ["01_LZOC_transport", "14_LZOC_species_MSD", "15_LZOC_RDF", "16_LZOC_coordination", "17_LZOC_radial_displacement"]
    if identifier.startswith("LSZC_"):
        return ["18_LSZC_transport_comparison", "19_LSZC_partial_RDF", "20_LSZC_coordination_mobility", "27_LSZC_PDF_and_Zr_coordination"]
    if identifier.startswith("Li3PS4_"):
        return ["05_Li3PS4_lithium_MSD", "06_Li3PS4_diffusion_framework_MSD", "07_Li3PS4_local_structure", "28_Li3PS4_dynamic_heterogeneity"]
    if identifier.startswith("LiPON_"):
        return ["23_LiPON_lithium_MSD", "24_LiPON_transport_comparison", "25_LiPON_temperature_RDF"]
    raise ValueError(f"no report mapping for {identifier}")


def trajectory_specs() -> list[dict]:
    specs = []
    display_material = {
        "Li3YCl6": "Li₃YCl₆",
        "LiNbOCl4": "LiNbOCl₄",
        "Li1.75ZrCl4.75O0.5": "Li₁.₇₅ZrCl₄.₇₅O₀.₅",
        "0.5Li2SO4-ZrCl4": "0.5Li₂SO₄–ZrCl₄",
        "Li3PS4": "Li₃PS₄",
        "LiPON": "LiPON",
    }
    display_purpose = {
        "production": "production計算",
        "NVT production": "NVT production計算",
        "NPT equilibration and volume response": "NPT平衡化・体積応答",
    }

    def add(identifier, directory, source, stem, material, model, temperature,
            duration, purpose, fmt="extxyz", target=101, type_symbols=None):
        display_name = f"{display_material[material]}｜{model}｜{temperature} K｜{display_purpose.get(purpose, purpose)}"
        report_figures = report_figures_for(identifier)
        specs.append({
            "id": identifier,
            "directory": directory,
            "display_name": display_name,
            "report_figures": report_figures,
            "source": source,
            "stem": stem,
            "format": fmt,
            "frame_interval_ps": duration,
            "target_frames": target,
            "max_frames_per_chunk": 101,
            "purpose": purpose,
            "type_symbols": type_symbols,
            "metadata": {"material": material, "model": model,
                         "temperature_K": temperature, "phase": purpose,
                         "display_name": display_name,
                         "report_figures": "; ".join(report_figures)},
        })

    # Include every available trajectory for each benchmark condition.
    lyc = {1: "Li", 2: "Y", 3: "Cl"}
    lnco = {1: "Li", 2: "Nb", 3: "O", 4: "Cl"}
    crystal_models = (
        ("mace_mpa0_medium", "MACE-MPA-0", "MACE"),
        ("sevennet_nano_55", "SevenNet-nano", "SevenNet"),
        ("m3gnet_matgl_gpu", "M3GNet GPU", "M3GNet"),
    )
    for formula, temp, material, folder, type_symbols in (
        ("Li3YCl6_03_2x2x2", 600, "Li3YCl6", "crystalline/Li3YCl6", lyc),
        ("LiNbOCl4_2x2x3", 800, "LiNbOCl4", "crystalline/LiNbOCl4", lnco),
    ):
        for model_dir, model_name, short_name in crystal_models:
            root = ROOT / "runs/md" / model_dir / formula / f"{temp}K"
            for source_path in sorted(root.glob("replica_*/*/trajectory.lammpstrj")):
                replica = source_path.parents[1].name
                relative = source_path.relative_to(ROOT).as_posix()
                identifier = f"{material}_{short_name}_{temp}K_{replica}"
                add(identifier, folder, relative,
                    f"{short_name}_{temp}K_{replica}_trajectory_excerpt", material,
                    model_name, temp, 0.1, "production", "lammps-dump-text",
                    type_symbols=type_symbols)

    # The common 600 K MACE/NEP benchmark: NPT volume response and NVT motion.
    add("benchmark_MACE_600K_NPT", "amorphous/MACE_NEP_benchmark", "results/LZOC/analysis_20260912/source/mace/600K_R1/equilibration/trajectory.lammpstrj", "MACE_600K_NPT_volume", "Li1.75ZrCl4.75O0.5", "MACE-MPA-0", 600, 0.1, "NPT equilibration and volume response", "lammps-dump-text")
    add("benchmark_NEP89_600K_NPT", "amorphous/MACE_NEP_benchmark", "results/LZOC/analysis_20260912/source/nep89/equilibration/dump.xyz", "NEP89_600K_NPT_volume", "Li1.75ZrCl4.75O0.5", "NEP89", 600, 0.1, "NPT equilibration and volume response")
    add("benchmark_MACE_600K_NVT_R1", "amorphous/MACE_NEP_benchmark", "results/LZOC/analysis_20260912/source/mace/600K_R1/production/trajectory.lammpstrj", "MACE_600K_NVT_R1_trajectory_excerpt", "Li1.75ZrCl4.75O0.5", "MACE-MPA-0", 600, 0.1, "NVT production", "lammps-dump-text")
    add("benchmark_NEP89_600K_NVT_R1", "amorphous/MACE_NEP_benchmark", "results/LZOC/analysis_20260912/source/nep89/production/dump.xyz", "NEP89_600K_NVT_R1_trajectory_excerpt", "Li1.75ZrCl4.75O0.5", "NEP89", 600, 0.1, "NVT production")

    review = ROOT / "results/amorphous_review_20260915/source"
    lzoc_sources = sorted((review / "LZOC_repeats").glob("*/production/dump.xyz"))
    lzoc_sources += [review / f"LZOC300/nhc300_{temperature}K_8676684/dump.xyz"
                     for temperature in (340, 360, 380)]
    for source_path in lzoc_sources:
        if not source_path.exists():
            continue
        match = re.search(r"(\d+)K(?:_R(\d+))?", str(source_path))
        if not match:
            raise ValueError(f"cannot identify LZOC temperature/repeat from {source_path}")
        temperature = int(match.group(1))
        replica = f"R{match.group(2)}" if match.group(2) else "baseline"
        relative = source_path.relative_to(ROOT).as_posix()
        add(f"LZOC_{temperature}K_{replica}", "amorphous/LZOC", relative,
            f"NEP89_{temperature}K_{replica}_trajectory_excerpt", "Li1.75ZrCl4.75O0.5",
            "NEP89", temperature, 0.1, "NVT production")

    for source_path in sorted((review / "LSZC_matched4t").glob("R*_*K/production/dump.xyz")):
        repeat_dir = source_path.parents[1].name
        replica, temp_label = repeat_dir.split("_")
        temperature = int(temp_label.removesuffix("K"))
        add(f"LSZC_{temperature}K_{replica}", "amorphous/LSZC",
            source_path.relative_to(ROOT).as_posix(),
            f"NEP89_{temperature}K_{replica}_trajectory_excerpt", "0.5Li2SO4-ZrCl4",
            "NEP89", temperature, 0.1, "NVT production")

    for temperature in (300, 500, 700, 900):
        source = f"results/amorphous_review_20260915/source/Li3PS4_R1_transport/{temperature}K/production/dump.xyz"
        add(f"Li3PS4_{temperature}K_R1", "amorphous/Li3PS4", source, f"NEP89_{temperature}K_R1_trajectory_excerpt", "Li3PS4", "NEP89", temperature, 0.1, "NVT production")

    lipon_roots = (review / "LiPON_transport", review / "LiPON_transport_repeats")
    for source_path in sorted(path for folder in lipon_roots
                              for path in folder.glob("*/production/dump.xyz")):
        folder_name = source_path.parents[1].name
        match = re.search(r"(\d+)K(?:_R(\d+))?", folder_name)
        if not match:
            continue
        temperature = int(match.group(1))
        replica = f"R{match.group(2) or 1}"
        add(f"LiPON_{temperature}K_{replica}", "amorphous/LiPON",
            source_path.relative_to(ROOT).as_posix(),
            f"NEP89_{temperature}K_{replica}_trajectory_excerpt", "LiPON", "NEP89",
            temperature, 0.1, "NVT production")
    return specs


def figure_links(names: list[str]) -> str:
    return ", ".join(
        f"[{name}](../../docs/materials/figures/{name}.png)" for name in names
    )


def render_readme(manifest: dict) -> str:
    lines = [
        "# 原子構造と軌跡抜粋",
        "",
        "本ディレクトリは材料レビューと、確認可能な初期構造・完了済み全軌跡の抜粋を対応付けます。XYZは可視化と出典確認のため、各元軌跡から時間軸に沿って等間隔に抽出したものです。MSD、拡散係数、RDF、配位数、熱力学量の定量解析では、`manifest.json` に記載した完全な元軌跡を使用します。",
        "",
        "## 収録内容",
        "",
        "各項目には材料・モデル・温度・計算段階を記載しています。extended XYZのヘッダーにも `display_name` と対応図を埋め込んでいるため、単独でダウンロードした後も識別できます。",
        "",
        "|名称|種別|温度 (K)|対応図|ファイル|",
        "|---|---|---:|---|---|",
    ]
    for item in manifest.get("structures", []):
        path = f"{item['directory']}/{item['file']}"
        lines.append(
            f"|{item['display_name']}|初期・解析構造|—|{figure_links(item['report_figures'])}|[XYZを開く]({path})|"
        )
    for item in manifest.get("trajectories", []):
        metadata = item["metadata"]
        links = ", ".join(
            f"[XYZを開く]({item['directory']}/{chunk['file']})" for chunk in item["chunks"]
        )
        lines.append(
            f"|{item['display_name']}|軌跡抜粋|{metadata['temperature_K']}|{figure_links(item['report_figures'])}|{links}|"
        )
    lines += [
        "",
        "## データの見方",
        "",
        "- `manifest.json` の `source_frame_indices` と `time_ps` から、抜粋フレームと元軌跡の対応を確認できます。",
        "- 各XYZには周期セル、材料、モデル、温度、計算段階、元フレーム番号および相対時刻を保存しています。",
        "- SHA-256は元軌跡と出力XYZの双方について記録しています。",
        "- これらは根拠確認・可視化用の抜粋であり、定量解析に使った全軌跡の代替ではありません。",
        "",
    ]
    return "\n".join(lines)


def build() -> dict:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    structures = []
    for directory, name, source_text, metadata in STRUCTURES:
        source = ROOT / source_text
        record = export_structure(source, OUTPUT / directory, name, metadata)
        record.update(directory=directory, id=f"{directory}/{name}")
        structures.append(record)
    trajectories = [export_trajectory(spec) for spec in trajectory_specs()]
    manifest = {
        "schema_version": 1,
        "description": "材料レビューの構造根拠と、利用可能な全完了軌跡から等間隔抽出した可視化用データ。",
        "analysis_note": "MSD、拡散係数、RDF、配位数、熱力学量の定量解析には、抜粋ではなくmanifest記載の完全な元軌跡を使用。",
        "structures": structures,
        "trajectories": trajectories,
    }
    manifest_path = OUTPUT / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    (OUTPUT / "README.md").write_text(render_readme(manifest))
    return manifest


if __name__ == "__main__":
    result = build()
    print(json.dumps({"structures": len(result["structures"]),
                      "trajectories": len(result["trajectories"])}, indent=2))
