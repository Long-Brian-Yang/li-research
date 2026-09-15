# Li3PS4 / LiPON preparation validation — 2026-09-14

## Decision

**Exploratory candidates only; neither is yet validated for quantitative transport predictions.** Li3PS4 has stronger evidence of loss of initial order and approximately stationary final thermodynamics. LiPON has substantial residual tension and persistent short N–N contacts; do not advance it directly to production. No new production job was submitted.

## Original evidence

TSUBAME root: `/gs/fs/tgj-26ICP/uf03782/yang/li-research/runs/amorphous`.
- Li3PS4: `Li3PS4/nep89/preparation_8670632`, 512 atoms, NPT preparation, final 300 K/20 ps.
- LiPON: `LiPON/nep89/preparation_8670667`, 124 atoms, NVT preparation, final 250 K/20 ps.
Local copies under `source/`; per-file SHA256 hashes in `structural_thermo_summary.json`. Species/order preserved within each trajectory. All final thermo series contain the expected 400 records. Raw simulations were not edited.

## Thermodynamic checks

Mean ± time-series sample SD over final 20 ps; SD is NOT uncertainty of the mean. Four consecutive non-overlapping 5 ps blocks were also compared. They remain potentially correlated and are too few to certify equilibrium.

| Quantity | Li3PS4 | LiPON |
|---|---:|---:|
| Temperature / K | 298.66 ± 10.76 | 248.24 ± 17.80 |
| Mean hydrostatic pressure / GPa | −0.00012 ± 0.18229 | −2.80025 ± 0.52874 |
| Density / g cm−3 | 2.21305 ± 0.00973 | 2.33792 (fixed cell) |
| Last minus first 5 ps density / g cm−3 | +0.00123 | 0 by construction |
| Last minus first 5 ps PE / eV atom−1 | −0.000070 | −0.001591 |
| PE linear slope / eV atom−1 ps−1 | −0.0000199 | −0.0001076 |

Li3PS4 late density varies little between these blocks. Its increase from the initial 1.85326 to 2.21305 g/cm3 is NOT itself proof of experimental realism. LiPON maintains the imposed volume; flat density is not evidence of mechanical equilibration. Its persistent negative pressure requires attention before treating it as an ambient-pressure material. Potential-energy slopes here are thermostatted relaxation trends, not NVE energy-conservation errors.

## Local structure and residual order

ASE periodic minimum-image distances, with self pairs removed; RDF shell normalization uses the instantaneous cell volume. RDF sampling uses the last 10 ps (10 Li3PS4 frames / 100 LiPON frames at their native output intervals), bin width 0.05 A, maximum radius below half the shortest cell length. No smoothing was applied. Results are in each material's `rdf.csv`.

| Screening result | Li3PS4 | LiPON |
|---|---:|---:|
| Mean P–S CN, cutoff 2.6 A | 4.000 | — |
| Mean P–O / P–N CN, cutoff 2.1 A | — | 3.6875 / 0.4375 |
| Initial P reciprocal-order score | 0.7230 | 0.9190 |
| Late score at the same initial reciprocal modes | 0.0346 | 0.2047 |
| Melt P endpoint MIC displacement squared / A2 | 109.57 | 1.43 |
| Minimum pair distance in final 20 ps / A | 1.902 | 1.255 |

Order score: normalized squared coherent amplitude `abs(mean(exp(2*pi*i*h·fractional_P)))^2`; select the initial top 20 modes from integer h,k,l in −4…4 excluding 000, and evaluate exactly those modes in final frames. This is a finite-cell initial-order persistence screen, NOT experimental S(Q), a universal crystallinity fraction or proof that all possible new crystalline order is absent. Finite-size baselines differ (64 vs 16 P atoms), so do not compare scores as absolute crystallinity percentages across materials.

The P-S tetrahedral coordination is retained while initial P order is strongly reduced in Li3PS4. This supports, but does not alone certify, a glass-like candidate. LiPON loses some order but its phosphorus framework moves comparatively little during the short melt. Further structural verification is needed, not an assumption that 10 ps melted it fully under NEP89.

LiPON also exhibits a persistent N–N distance below 1.6 A throughout the sampled final relaxation. A short N–N contact cannot simply be labelled thermal noise; possible bonding/reconstruction requires chemical/DFT checking. N–P coordination fractions at 2.1 A are 60% one-neighbor and 40% two-neighbor. These geometric counts alone do not establish chemically correct N speciation, especially in the presence of N–N contacts. Cutoff sensitivity and larger/independent sampling remain open.

Endpoint MIC displacement is only a bounded motion diagnostic, measured from the first to last dumped melt frame. It is NOT an unwrapped multi-origin MSD or diffusion coefficient; multiple cell crossings are not counted.

Final candidate CIFs are saved per material, labelled candidates rather than validated glasses.

## DFT force screening

Calorine 3.5 CPUNEP evaluated the exact NEP89 weight file used on TSUBAME. Maximum component difference versus a saved GPUMD force frame: 5.47e−5 eV/A (Li3PS4), 7.82e−5 eV/A (LiPON). This checks evaluation consistency, NOT agreement with DFT.

| Public reference sample | Frames | Component MAE / eV A−1 | Component RMSE / eV A−1 |
|---|---:|---:|---:|
| Li24P8S32, CP2K 3000 K AIMD | 12 | 0.2363 | 0.3335 |
| Li50P16O62N2, VASP AIMD | 12 | 0.2791 | 0.4301 |

Fixed evenly spaced sampling, chosen before errors were computed. Per-frame/per-element results, reference RMS scales and hashes are in `DFT_force_samples.csv` and `force_validation.json`. `DFT_NEP_samples.xyz` retains exact sampled coordinates and both force arrays. MAE averages absolute Cartesian-component errors; RMSE is the square root of their mean square. Do not compare these MAEs directly to another model's reported test error on a different dataset.

Important limits:
- Li3PS4 has the correct stoichiometry but these are high-temperature CP2K/PBE-D3 configurations, not the final 300 K glass. DFT-method differences from the NEP training target can contribute to discrepancies.
- LiPON available AIMD subset has Li50P16O62N2, NOT our Li47P16O56N5. It tests a related composition only; no matching DFT labels for the current candidate were obtained.
- These nonzero errors, particularly on framework P (MAE 0.447 / 0.632 eV/A respectively), do not support assuming transferable DFT accuracy. The small sample is a screen, not a converged benchmark or formal rejection threshold.

## Sources and reproducibility

- LiPS author revision `552d32c1f800cc51776a3d8c055399c29f521c31`, `data.init/init_data/beta-Li3PS4/3000K/deepmd/Li24P8S32/{box,coord,force,type,type_map}.raw`: https://github.com/OxideGlassGroupAAU/LiPS . Paper: https://doi.org/10.1038/s41467-025-56322-x .
- LiPON author revision `1818171dc4423404dc292c51f7593a7366a6599f`, Complete_dataset.7z / MD_structures; selected global frames 6000…10999 at 12 evenly spaced indices: https://github.com/sai-mat-group/ann-lipon . Paper: https://doi.org/10.1021/acsmaterialsau.4c00117 .
- Scripts: `scripts/structures/validate_amorphous_trials.py`, `scripts/structures/check_nep_dft.py`; test `tests/test_amorphous_validation.py`.
- Isolated runtime `/tmp/amorphous-validation-env` (ASE, NumPy, Calorine); source downloads `/tmp/lipon_complete.7z`, `/tmp/lips_force.raw`, model `/tmp/nep89_validation.txt`. Temporary downloads must be reacquired at pinned URLs if removed; saved sampled xyz supports independent force reevaluation.

## Next decision

Retain Li3PS4 as the more promising exploratory candidate, but validate low-temperature/same-state force accuracy and experimental structure/density before quantitative transport claims. Hold LiPON production; investigate N–N reconstruction and fixed-volume residual stress, ideally with matching-composition DFT or the published reference potential. Blindly extending MD is not a substitute for potential validation.
