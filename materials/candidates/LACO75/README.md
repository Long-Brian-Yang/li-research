# LACO75 NEP89 / GPUMD preflight — 2026-09-14

Status: **not submitted**. No LACO75 structure or MD result has been generated.

## Scope and reference

User requested a NEP/GPUMD trial of LiAlCl2.5O0.75 following the experimental/AIMD reference:
Dai et al., *Inorganic glass electrolytes with polymer-like viscoelasticity*, Nature Energy 8, 1221–1228 (2023), https://doi.org/10.1038/s41560-023-01356-y.

This would be an evaluation of NEP89 against the reference, not AIMD itself. Prior LZOC structures and protocols must not be reused as LACO75.

## Verified

- Main-text Methods: LiAlCl4-derived oxygen substitution; 600 K for 30 ps with 1 fs steps; cooling to 300 K; subsequent 300 K NVT AIMD for 160 ps for LiAlCl2.5O0.75. Cooling duration/rate is not specified in the cited passage.
- Supplementary PDF: 31 pages inspected by text extraction; no coordinate tables or embedded files found. Publisher lists this PDF, five videos and a phase-equilibria text file, not an explicit CIF/POSCAR dataset.
- Supplementary Fig. 6 compares experimental neutron PDF with a mixture of 89 wt% amorphous LACO75 and 11 wt% LiCl. A pure-cell partial RDF is not directly this experimental total PDF.
- Supplementary Note 5 compares a simulated high-temperature activation energy of 0.30 eV with experiment 0.33 eV; this does not authorize tuning simulated results to those values.

Sources: [main text](https://www.iop.cas.cn/xwzx/kydt/202310/P020231011410324732599.pdf), [supplementary PDF](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41560-023-01356-y/MediaObjects/41560_2023_1356_MOESM1_ESM.pdf).
Downloaded supplement SHA256: `c208620179837699c8be10e2defebd06e706b8a839273e282c2f67b6ea1e9ae5`.

## Runtime preflight

Read-only SSH checks confirmed:

- Executable: `/gs/fs/tgj-26ICP/uf03782/yang/li-research/engines/gpumd/source/src/gpumd`
- Model: `/gs/fs/tgj-26ICP/uf03782/yang/li-research/models/nep89/nep/nep89_20250409/nep89_20250409.txt`
- Model header: `nep4_zbl`, 89 elements including Li/Al/O/Cl. Element coverage is not validation for this material.

## Required before a reference-matched run

1. Traceable atomic coordinates, composition, cell dimensions/density and replacement pattern (or explicit approval for independently constructed exploratory inputs).
2. Cooling schedule and thermostat settings (or a clearly labelled, approved project protocol).
3. Small diagnostic run with model/input hashes and archived parameters; physical checks before production.

No qsub was invoked. No existing environment, simulation or result was modified. The next decision is to obtain the original inputs or explicitly authorize an independently constructed exploratory model; these are different scopes.
