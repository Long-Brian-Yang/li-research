# Structures and representative trajectories

This directory links the material-review conclusions to inspectable atomic structures and trajectories. The XYZ trajectories are uniformly sampled exports for visualization and provenance; all numerical analyses used the complete source trajectories listed in `manifest.json`.

本目录将综述中的主要结论与可检查的初始结构、代表轨迹对应起来。XYZ 为等时间间隔抽帧后的展示与溯源文件；MSD、扩散系数、RDF、配位及热力学分析仍使用 `manifest.json` 中记录的完整原始轨迹。

## Contents

|System|Evidence|Model / role|Temperature (K)|Files|
|---|---|---|---:|---|
|Li72Y24Cl144|Initial/analysis structure|initial_structure|—|[initial_structure.xyz](crystalline/Li3YCl6/initial_structure.xyz)|
|Li48Nb48Cl192O48|Initial/analysis structure|initial_structure|—|[initial_structure.xyz](crystalline/LiNbOCl4/initial_structure.xyz)|
|Li42Zr24Cl114O12|Initial/analysis structure|common_300K_structure|—|[common_300K_structure.xyz](amorphous/MACE_NEP_benchmark/common_300K_structure.xyz)|
|Li42Zr24Cl114O12|Initial/analysis structure|construction_initial|—|[construction_initial.xyz](amorphous/LZOC/construction_initial.xyz)|
|Li42Zr24Cl114O12|Initial/analysis structure|analysis_start|—|[analysis_start.xyz](amorphous/LZOC/analysis_start.xyz)|
|Li32Zr32Cl128O64S16|Initial/analysis structure|construction_relaxed|—|[construction_relaxed.xyz](amorphous/LSZC/construction_relaxed.xyz)|
|Li32Zr32Cl128O64S16|Initial/analysis structure|analysis_start|—|[analysis_start.xyz](amorphous/LSZC/analysis_start.xyz)|
|Li192P64S256|Initial/analysis structure|construction_initial|—|[construction_initial.xyz](amorphous/Li3PS4/construction_initial.xyz)|
|Li192P64S256|Initial/analysis structure|analysis_start|—|[analysis_start.xyz](amorphous/Li3PS4/analysis_start.xyz)|
|Li47N5O56P16|Initial/analysis structure|construction_initial|—|[construction_initial.xyz](amorphous/LiPON/construction_initial.xyz)|
|Li47N5O56P16|Initial/analysis structure|analysis_start|—|[analysis_start.xyz](amorphous/LiPON/analysis_start.xyz)|
|Li3YCl6|Representative trajectory|MACE-MPA-0 / production|600|[MACE_600K_representative_part01.xyz](crystalline/Li3YCl6/MACE_600K_representative_part01.xyz)|
|Li3YCl6|Representative trajectory|SevenNet-nano / production|600|[SevenNet_600K_representative_part01.xyz](crystalline/Li3YCl6/SevenNet_600K_representative_part01.xyz)|
|Li3YCl6|Representative trajectory|M3GNet GPU / production|600|[M3GNet_600K_representative_part01.xyz](crystalline/Li3YCl6/M3GNet_600K_representative_part01.xyz)|
|LiNbOCl4|Representative trajectory|MACE-MPA-0 / production|800|[MACE_800K_representative_part01.xyz](crystalline/LiNbOCl4/MACE_800K_representative_part01.xyz)|
|LiNbOCl4|Representative trajectory|SevenNet-nano / production|800|[SevenNet_800K_representative_part01.xyz](crystalline/LiNbOCl4/SevenNet_800K_representative_part01.xyz)|
|LiNbOCl4|Representative trajectory|M3GNet GPU / production|800|[M3GNet_800K_representative_part01.xyz](crystalline/LiNbOCl4/M3GNet_800K_representative_part01.xyz)|
|Li1.75ZrCl4.75O0.5|Representative trajectory|MACE-MPA-0 / NPT equilibration and volume response|600|[MACE_600K_NPT_volume_part01.xyz](amorphous/MACE_NEP_benchmark/MACE_600K_NPT_volume_part01.xyz)|
|Li1.75ZrCl4.75O0.5|Representative trajectory|NEP89 / NPT equilibration and volume response|600|[NEP89_600K_NPT_volume_part01.xyz](amorphous/MACE_NEP_benchmark/NEP89_600K_NPT_volume_part01.xyz)|
|Li1.75ZrCl4.75O0.5|Representative trajectory|MACE-MPA-0 / NVT production|600|[MACE_600K_NVT_representative_part01.xyz](amorphous/MACE_NEP_benchmark/MACE_600K_NVT_representative_part01.xyz)|
|Li1.75ZrCl4.75O0.5|Representative trajectory|NEP89 / NVT production|600|[NEP89_600K_NVT_representative_part01.xyz](amorphous/MACE_NEP_benchmark/NEP89_600K_NVT_representative_part01.xyz)|
|Li1.75ZrCl4.75O0.5|Representative trajectory|NEP89 / NVT production|340|[NEP89_340K_representative_part01.xyz](amorphous/LZOC/NEP89_340K_representative_part01.xyz)|
|Li1.75ZrCl4.75O0.5|Representative trajectory|NEP89 / NVT production|360|[NEP89_360K_representative_part01.xyz](amorphous/LZOC/NEP89_360K_representative_part01.xyz)|
|Li1.75ZrCl4.75O0.5|Representative trajectory|NEP89 / NVT production|380|[NEP89_380K_representative_part01.xyz](amorphous/LZOC/NEP89_380K_representative_part01.xyz)|
|0.5Li2SO4-ZrCl4|Representative trajectory|NEP89 / NVT production|320|[NEP89_320K_representative_part01.xyz](amorphous/LSZC/NEP89_320K_representative_part01.xyz)|
|0.5Li2SO4-ZrCl4|Representative trajectory|NEP89 / NVT production|330|[NEP89_330K_representative_part01.xyz](amorphous/LSZC/NEP89_330K_representative_part01.xyz)|
|0.5Li2SO4-ZrCl4|Representative trajectory|NEP89 / NVT production|340|[NEP89_340K_representative_part01.xyz](amorphous/LSZC/NEP89_340K_representative_part01.xyz)|
|0.5Li2SO4-ZrCl4|Representative trajectory|NEP89 / NVT production|350|[NEP89_350K_representative_part01.xyz](amorphous/LSZC/NEP89_350K_representative_part01.xyz)|
|Li3PS4|Representative trajectory|NEP89 / NVT production|300|[NEP89_300K_representative_part01.xyz](amorphous/Li3PS4/NEP89_300K_representative_part01.xyz)|
|Li3PS4|Representative trajectory|NEP89 / NVT production|500|[NEP89_500K_representative_part01.xyz](amorphous/Li3PS4/NEP89_500K_representative_part01.xyz)|
|Li3PS4|Representative trajectory|NEP89 / NVT production|700|[NEP89_700K_representative_part01.xyz](amorphous/Li3PS4/NEP89_700K_representative_part01.xyz)|
|Li3PS4|Representative trajectory|NEP89 / NVT production|900|[NEP89_900K_representative_part01.xyz](amorphous/Li3PS4/NEP89_900K_representative_part01.xyz)|
|LiPON|Representative trajectory|NEP89 / NVT production|600|[NEP89_600K_representative_part01.xyz](amorphous/LiPON/NEP89_600K_representative_part01.xyz)|
|LiPON|Representative trajectory|NEP89 / NVT production|900|[NEP89_900K_representative_part01.xyz](amorphous/LiPON/NEP89_900K_representative_part01.xyz)|
|LiPON|Representative trajectory|NEP89 / NVT production|1200|[NEP89_1200K_representative_part01.xyz](amorphous/LiPON/NEP89_1200K_representative_part01.xyz)|
|LiPON|Representative trajectory|NEP89 / NVT production|1500|[NEP89_1500K_representative_part01.xyz](amorphous/LiPON/NEP89_1500K_representative_part01.xyz)|

## Interpretation

- `source_frame_indices` and `time_ps` in `manifest.json` give the exact mapping from every exported frame to its complete source trajectory.
- Every XYZ retains the periodic cell and includes material, model, temperature, phase, source-frame index and relative time in its extended-XYZ metadata.
- SHA-256 values cover both the complete local source and each exported XYZ file.
- These exports are evidence and visualization files, not replacements for the full trajectories used in quantitative analysis.
