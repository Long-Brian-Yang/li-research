# Materials portfolio — current assessment, 15 September 2026

**Latest continuation:** [Targeted diagnostics 8675392.1–2](targeted_diagnostics_20260915.md) submitted: LSZC400 K20 ps NPT volume relaxation and LZOC380 K80 ps NHC/0.5 fs timestep control. Results pending; earlier no-new-job statements below describe the completed postprocessing stage only.

[Complete latest analysis: 11 new figure families, data, literature comparisons and limits](../../results/amorphous_review_20260915/final_comparisons/report_en.md) · [Japanese](materials_overview_ja.md)

Four amorphous chemical systems, five preparation routes. Legacy and reconstructed LZOC share one composition. No new MD or DFT was submitted during this postprocessing. Numerical completion is distinct from scientific agreement.

[Additional structural analysis](../../results/amorphous_review_20260915/structure_followup/report_en.md): Li₃PS₄ isolated geometric P₁S₄ contains79.7% of P; shared-S components remain despite fourfold local coordination. LSZC Zr-coordination mismatch is not removed by the tested cutoff sweep. These findings qualify the local-agreement statement below; dedicated transport convergence and structural-model validation remain unresolved. No new jobs in this follow-up.

| Material / route | Latest completed work | Result / disposition |
|---|---|---|
| Reconstructed LZOC, 192 atoms | 340/360/380 K: original 200 ps completed; NHC/2 fs controls 8675022.1–3 completed 80 ps each. Matched first-80-ps analysis finished | Settings/window sensitivity remains. No adopted Ea or 300 K extrapolation |
| LSZC, 272 atoms | Independent cluster packing/relaxation, 300 K diagnostic, 100 ps ramp +20 ps at 400 K completed; experimental EXAFS and deposited-geometry comparisons finished | S–O fourfold retained. Zr–O CN1.532 versus EXAFS2.6; density below author geometry. Not yet quantitative reproduction |
| Li₃PS₄, 512 atoms | Preparation completed; final RDF and S–P–S angle distribution compared with Chen2025 numerical source data | Encouraging local agreement; no transport production or Ea established |
| LiPON, 124 atoms | Preparation and 250 K release completed; coordination and contact tracing analysed | N–N1.270–1.347 Å persists. Retain as limitation case, not validated transport model |
| Legacy LZOC candidate3 | Existing MACE/NEP600 K and four-temperature timing report complete | Archived supplementary comparison; no new extension |

Main line: LZOC and LSZC; Li₃PS₄ is a methodological control, LiPON a documented limitation case. Existing crystalline Li₃YCl₆/LiNbOCl₄ benchmarks are not reanalysed in this update. The cancelled Zhou2024 route is not counted as executed. No new materials were added.

Reference anchors: [Hussain2024 AIMD](https://doi.org/10.1038/s41524-024-01346-y), [Hu2023 experiment](https://doi.org/10.1038/s41467-023-39522-1), [Tang2026 LSZC](https://doi.org/10.1038/s41467-026-69737-x), [Chen2025 Li₃PS₄](https://doi.org/10.1038/s41467-025-56322-x), [Seth2025 LiPON](https://doi.org/10.1021/acsmaterialsau.4c00117). See the latest report for per-setting deviations and source distinctions. None of the routes is labelled strict full-protocol AIMD reproduction.

All newly produced figures link to CSV/JSON and scripts; raw trajectories stay local/TSUBAME rather than Git. Source hashes identify analysed versions. The ≤100-point notification requirement is unchanged.

<details>
<summary>Historical snapshots below — superseded by the current table (including old “not pushed” statements)</summary>

## Previous portfolio records

Legacy candidate 3: [completed 600 K MACE/NEP comparison and four-temperature timing figures](../../results/LZOC/legacy_comparison_20260915/report_en.md). Later high-temperature NEP structural/transport analysis is outside this package.

Completed postprocessing (15 September): [LZOC/LSZC report with 10 figure families and result tables](../../results/amorphous_review_20260915/analysis_complete/report_en.md). Existing runs only; no new MD/DFT. Transport convergence is not established. This local update has not been Git pushed.

## Latest execution status (2026-09-15)

LSZC annealing and the three-temperature reconstructed-LZOC production runs have now completed with basic checks: [latest execution record](workflow_execution_20260915.md). Older incomplete/unsubmitted statements below are historical snapshots, not the latest status. No new DFT is planned. This portfolio update has not yet been pushed to GitHub.

LiPON update: fixed-pair N76/108 tracking shows persistent short contact with P coordination changing from one neighbour each to two through quench and both low-temperature diagnostics. [Timeline](../../results/amorphous_review_20260915/LiPON/contact_origin.md). NoDFT will be performed per user instruction; earlierDFT plans are superseded. This candidate is not cleared for production.

Latest: LSZC newly packed272atom job8674265 submitted for300K20psNVT at0.5fs; noDFT planned. Submission confirmed, completion not confirmed. [Settings](../../materials/candidates/LSZC/packed_272/README.md).

LSZC update: independent272atom random cluster packing and fixed-cell NEP position relaxation finished (1380steps; fmax0.04933eV/Å against0.05target). All16S retain four O neighbours. Stress, finite-temperature and glass validation remain pending; no new cluster MD submitted. [Structures and logs](../../materials/candidates/LSZC/packed_272/README.md). This supersedes earlier packing-pending entries below.

Latest structural diagnosis: five finite non-Li geometric components were extracted from LSZC author Data1. Two copies of each plus32Li preserve the272atom composition; packing and relaxation remain outstanding. [Cluster record](../../materials/candidates/LSZC/cluster_library_272/README.md). LiPON's short N–N contact between row indices76/108 first appears between2.2–2.3ps of the2000K hold and persists thereafter. Full diagnostic snapshots are saved; no DFT has been run. [Contact tracing](../../results/amorphous_review_20260915/LiPON/contact_origin.md).

## Authorized continuation (2026-09-15, 10:00 JST)

Submitted reconstructed-LZOC job **8674222**: 300 K fixed-cell 50 ps diagnostic, 0.5 fs timestep, 100 fs MTTK thermostat; retain velocities/cell from cooling8674094. Output: `runs/amorphous/LZOC_Hussain2024/nep89/hold300_8674222/`. Scheduler acceptance verified; completion not yet verified. This is a project diagnostic, not an original-paper step or automatic production. Late-10-ps RDF CSVs were added for LZOC/LSZC/LiPON in the review directory. LSZC is fixed at272atoms by user choice, but SI Fig.20 requires AIMD-derived cluster packing before annealing; the replicated seed is not that reconstruction. Cluster-generation details remain unresolved; no1088atom job added. LiPON remains on chemical-validation hold; no new Li3PS4 DFT/production or legacy-LZOC extension. Pre-submission balance221.99 and deposit7.26points; no Git push.

## Follow-up measurements (2026-09-15)

The three recent diagnostics now have verified completion markers, 20 ps block statistics and periodic coordination checks: [detailed results and data](../../results/amorphous_review_20260915/README.md). Reconstructed LZOC still shows decreasing potential energy. LSZC retains mean S–O coordination 4, but amorphous reconstruction is incomplete. LiPON mean pressure improves to 0.00614 GPa, yet short N–N contacts persist in all 200 frames. Numerical completion is not equilibration or clearance for production. The 09:42 snapshot below is retained as historical context; its missing completion-marker statements are superseded by this check. Existing Li₃PS₄ and legacy LZOC validation was reviewed, not recomputed. LSZC requires an explicit choice between the author's 1088-atom configuration and independently reconstructed small models; no new calculation was submitted.

Updated: 2026-09-15. Queue snapshot: 09:42 JST on that date; this is not a live status display. Earlier daily reports describe their respective observation dates.

## 1. Scope and current status

The amorphous-material programme includes **four chemical systems and five preparation routes**. The legacy candidate 3 and the Hussain 2024 reconstruction have the same LZOC composition and are not two different materials. Including the established crystalline Li₃YCl₆ and LiNbOCl₄ benchmark lines, the project covers six material systems.

The recorded `qstat` query returned no entries for the account. An active research topic is not necessarily a running calculation. Leaving the queue does not establish successful execution or equilibration. The inventory task submitted, cancelled and deleted no jobs.

| Material / route | Size and potential | Work performed | Limitations and next check |
|---|---|---|---|
| LZOC, Li₁.₇₅ZrCl₄.₇₅O₀.₅: legacy candidate 3 | 192 atoms; MACE and NEP89 | Preparation and four-temperature results exist; historical checks record NEP production at 600/700/800/900 K and additional NPT at 700–900 K | Retain as a comparison. Expansion, framework stability and convergence remain unresolved; an available Ea does not validate the result. Hold further long MD |
| Same-composition LZOC: Hussain 2024 reconstruction | 192 atoms; NEP89/GPUMD | Initial 32 ps and high-temperature 100 ps; expected outputs exist for all stages of the 28 ps cooling sequence | Check the cooled structure and residual pressure. The paper's DFT cell optimization was not performed; do not assume an ambient-pressure glass |
| LSZC: 0.5Li₂SO₄–ZrCl₄ | Current model: 272 atoms, NEP89/GPUMD; a 1088-atom short trial is retained | Compression at 300 K, 5 kbar for 12 ps; expected output for pressure release at 300 K, 1 bar for 20 ps | The 272-atom seed replicates crystalline units, not the author's amorphous model. Amorphous reconstruction is incomplete; resolve the structure route before fitting diffusion |
| Amorphous Li₃PS₄ candidate | 512 atoms; NEP89/GPUMD | Completion and preliminary validation records exist for 611 ps of preparation; no formal transport production | Initial order decreases and P–S coordination is retained. Useful as a methodological comparison, but low-temperature structure and potential applicability still require validation |
| LiPON: Li₄₇P₁₆O₅₆N₅ | 124 atoms; NEP89/GPUMD | 43 ps preparation; expected output for 20 ps pressure release at 250 K and 1 bar | Preparation showed residual tensile stress and short N–N contacts. Evaluate the release trial before transport production |

### Existing crystalline benchmarks

MACE/SevenNet/M3GNet figures and results for Li₃YCl₆ and LiNbOCl₄ remain in the [publication directory](../../results/publication_all_materials/). They are crystalline-model comparisons, not interchangeable with the amorphous preparation results. This inventory did not re-audit every crystalline trajectory or reconfirm Ea values.

## 2. Literature basis and explicit deviations

None of these routes should be labelled wholesale as a strict reproduction. However, some preparation parameters do follow the literature. Separate retained steps from project-specific choices.

| Route | Reference | Retained steps and deviations |
|---|---|---|
| Legacy LZOC candidate 3 | Structure source: [Kim 2025](https://doi.org/10.1038/s41467-025-65702-2); experimental context: [Hu 2023](https://doi.org/10.1038/s41467-023-39522-1) | Modified composition, independently selected occupations and a project-designed preparation schedule. Not a reproduction of the author's amorphous configuration. A multiphase experimental sample is not equivalent to one simulated configuration |
| Reconstructed LZOC | [Hussain 2024](https://doi.org/10.1038/s41524-024-01346-y), 96-atom branch on SI p.23 | Retained staged heating/cooling durations; reconstructed 192 atoms from average occupancies; replaced AIMD with NEP. Post-melt relaxation optimizes positions at fixed cell, not the author's DFT position-and-volume optimization |
| LSZC | [Tang 2026](https://doi.org/10.1038/s41467-026-69737-x), SI Fig.20 | Retained 300 K, 5 kbar and 12 ps. The author used fine-tuned MACE and cluster-assembled glass; this trial uses NEP and a replicated seed. Subsequent 1 bar release is a project diagnostic |
| Li₃PS₄ | [Chen 2025](https://doi.org/10.1038/s41467-025-56322-x) | Melting at 1500 K for 100 ps and cooling at 2.5 K/ps follow the paper. NEP replaces DeePMD; replicated training frame, coupling parameters, heating duration and final 20 ps are project choices |
| LiPON | [Seth 2025](https://doi.org/10.1021/acsmaterialsau.4c00117) | Melting at 2000 K for 10 ps and cooling to 250 K at 250 K/ps follow this paper. Independent substitution/removal pattern, NEP, 0.5 fs timestep, heating and final diagnostics are adaptations. This is not the Lacivita 2018 protocol |

Recommended description: **“Exploratory NEP89 evaluation using literature-derived structures and preparation steps.”** Claiming adherence to a literature protocol requires a parameter-by-parameter audit. Changing the potential does not itself reproduce the author's quantitative results.

## 3. Recent job evidence and outstanding checks

TSUBAME data root: `/gs/fs/tgj-26ICP/uf03782/yang/li-research/runs/amorphous/`.

| Job ID | Relative output path | Verified in this inventory | Not established |
|---|---|---|---|
| 8674094 | `LZOC_Hussain2024/nep89/cooling_8674094/` | 40 thermo records each at 1500/1000/500/100 K and 400 at 300 K; consistent with 2/2/2/2/20 ps at 0.05 ps output intervals | Completion-log marker was not obtained; final pressure, RDF, coordination, density and amorphous character were not reanalysed |
| 8674095 | `LSZC/nep89/seed272_release_8674095/` | 400 thermo records, consistent with 20 ps | Full reconstruction, experimental-density comparison and convergence conclusion remain outstanding |
| 8674143 | `LiPON/nep89/release_8674143/` | 400 thermo records, consistent with 20 ps | Completion-log marker was not obtained; improvement in N–N contacts and chemical environments after release is unconfirmed |

Scientific assessments of legacy LZOC and the Li₃PS₄/LiPON preparation runs rely on existing records, not new calculations in this inventory. See the [preliminary structure and force-validation report](../../results/amorphous_validation_20260914/README.md). Numerical completion, glass formation, thermodynamic equilibration and potential accuracy are distinct questions.

## 4. Proposed priorities: consolidate rather than expand

These are planning recommendations, not authorization to submit new calculations.

1. **Main line A: reconstructed LZOC.** Closest to the existing Zr–O–Cl direction. Review cooling outputs, residual pressure, framework rearrangement, coordination and low-temperature order. Diagnose clear anomalies before adding multi-temperature diffusion runs.
2. **Main line B: LSZC.** Author structures and experimental context are available. Compare amorphous Data 2 with the 272-atom seed route and determine whether a defensible small-model reconstruction is possible. Compression/release at 300 K does not replace amorphous preparation.
3. **Methodological comparison: Li₃PS₄.** Validate existing 611 ps results as a sulfide-glass benchmark, without replacing the oxychloride research line. Do not repeat preparation simply to increase the number of tested literature protocols.
4. **Pending diagnosis: LiPON.** Review the current release trial first. Persistent short N–N contacts require potential/chemical-structure checks rather than repeated MD extensions.
5. **Legacy LZOC candidate 3: archived comparison.** Retain structures, trajectories and anomaly analyses; do not delete them or further expand the temperature matrix.

### Before formal diffusion production

- Pin a traceable structure: composition, atom count, source, random seed, structure files and potential hash.
- Record literature setting / actual setting / reason for deviation. Do not silently combine different paper branches.
- Inspect complete logs and temperature, blockwise energy, density and pressure trends. Constant density in NVT does not demonstrate equilibration.
- Check disorder and local chemistry through RDF/structure factor or order metrics, framework motion, coordination and short contacts. Avoid unsupported universal acceptance thresholds.
- Compare with DFT/AIMD or experiments at relevant compositions and conditions. A few related-composition high-temperature force comparisons are only preliminary screening.
- Choose production temperatures and durations only after review. Determine MSD fitting windows from the diffusive regime and sensitivity, not from a desired Ea.
- One structure can support exploratory screening, not uncertainty across independent amorphous configurations. Reassess independent sampling before publication-level generalization.
- Reuse completed data to conserve points. Retain the existing requirement to notify at a balance ≤100; this task did not change monitoring or resource policy.

## 5. Protocols and materials not yet executed

P1 Lacivita 2018, P2 Smith & Siegel 2020, P3 Zhou 2024, P4 Sadowski & Albe 2020 and P5 Bertani & Pedone 2025 **have not been executed as complete protocols from the screenshot**. P1/P2/P3 overlap with existing materials and do not represent five new systems. Zhou's full Methods remain unavailable; Na₃PS₄ has not been started. LiNbCl₆ and LACO75 remain literature/input candidates, not executed material trials.

## 6. Navigation

- [Legacy candidate 3: MACE/NEP timings and selection rationale, with English/Japanese summaries](LZOC/candidate3_mace_nep_comparison.md)

- [Legacy LZOC](../../materials/candidates/LZOC/README.md)
- [Reconstructed LZOC / Hussain 2024](../../materials/candidates/LZOC_Hussain2024/README.md)
- [LSZC](../../materials/candidates/LSZC/README.md)
- [Li₃PS₄](../../materials/candidates/Li3PS4_glass/README.md)
- [LiPON](../../materials/candidates/LiPON/README.md)
- [Chinese overview](materials_overview_zh.md) / [Japanese overview](materials_overview_ja.md)

Check each material README against its actual input scripts for detailed settings. This overview does not overwrite raw data, relabel potentials or modify diffusion results. These Markdown versions were prepared locally; no Git push was performed in this update.

</details>
