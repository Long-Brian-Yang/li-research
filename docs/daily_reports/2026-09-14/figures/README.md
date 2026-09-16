# Three-candidate preparation figure

Same LZOC composition, three related starting configurations; not three materials or independent replicas.

- [PNG](LZOC_three_candidate_preparation.png), [editable SVG](LZOC_three_candidate_preparation.svg), [PDF](LZOC_three_candidate_preparation.pdf).
- Raw extracted thermo: [candidate 1](candidate_1_preparation.csv), [candidate 2](candidate_2_preparation.csv), [candidate 3](candidate_3_preparation.csv).
- [Block means and original-log SHA256](preparation_summary.json).
- Reproduce from repository root: `MPLCONFIGDIR=/tmp/lzoc-mpl-cache python3 scripts/structures/plot_lzoc_preparation.py`.

Each series comprises 1101 samples at 0.05 ps spacing over 0–55 ps. Initial and final minimizations are excluded. Duplicate records at stage boundaries are represented once. Raw thermo traces are not smoothed, rescaled to match another candidate, or cropped to hide early relaxation. Energy is divided by the fixed atom count of 192; it is not mean-subtracted. NPT zoom uses 45–55 ps, while temperature and energy use the full preparation. Units and axis scales are shared within each row. Block statistics use (45,50] and (50,55] ps, 100 correlated samples each; no significance test or confidence interval is claimed.

This is a process comparison, not proof of full equilibration, amorphization or potential accuracy. The additional comparisons now supply common identity/RDF/CN, initial-order retention and stage-MSD checks for all three; candidates 1/2 still lack equivalent extended equilibration. No transport quantities are inferred from the cooling trajectory.

## Added order and atomic-motion figures

- `LZOC_three_candidate_structure_projection`: initial minimized versus finite-temperature 55 ps endpoint; wrapped fractional a/b projections, not real-space square cells.
- `LZOC_three_candidate_initial_order`: Cl/Zr initial top-ten reflection retention, q = 1–5 Å⁻¹ and hkl in [-8,8], with one member of each ± pair. The same selected indices are evaluated at 21 frames over 50–55 ps. Selection is separate for each candidate: these ratios are not crystalline fractions or a universal ranking.
- `LZOC_three_candidate_stage_MSD`: single-origin species MSD reset at each stage. Triclinic unwrapped coordinates are converted to fractional coordinates; increments are mapped through the midpoint cell, removing affine cell deformation. All-atom mass-weighted COM motion is removed. Fixed-cell results are checked against direct unwrapped displacement; normalized cell shape is verified constant to exclude cell flips. Image flags are not reapplied to xu/yu/zu.
- Each figure has PNG/PDF/SVG exports. `candidate_order_motion_summary.json` records hashes, selected hkl and stage endpoints; `candidate_*_stage_*_msd.csv` and `candidate_*_order.csv` contain plotted values.
- Reproduce: `python3 scripts/structures/lzoc_order_motion.py` with ASE 3.26.0, NumPy and matplotlib. Source trajectory hashes must match the remote-verified inputs.
- QA: synthetic affine-expansion/translation tests, fixed-cell displacement consistency checks, full timestamp/ID checks, and visual inspection of all three PNGs. No diffusion fitting or new MD jobs.

## Added structural figures

- [RDF](LZOC_three_candidate_RDF.png): Li–Cl, Li–O, Zr–Cl, Zr–O; 21 frames every 0.25 ps over 50–55 ps, 0.05 Å bins, rmax 4.5 Å, no smoothing.
- [Coordination distributions](LZOC_three_candidate_coordination.png): same frames, central-atom/frame pooled frequencies. Cutoffs in pair order are 3.2/2.7/3.0/2.6 Å and are common diagnostic thresholds, not candidate-specific fitted minima. Frequency sums are one; connections between integer counts are guides.
- [NPT block means](LZOC_three_candidate_NPT_blocks.png): 1 ps block means over (45,46] through (54,55] ps; 20 correlated samples per point. No error-bar or equilibrium claim.
- All three figures have same-basename PDF and SVG exports.
- [Structural summary and remote-verified trajectory hashes](candidate_structure_summary.json). CSV files `candidate_{1,2,3}_late_rdf.csv`, `candidate_{1,2,3}_late_coordination.csv` and `candidate_{1,2,3}_npt_blocks.csv` contain the plotted values. The coordination CSV pair_index is 0=Li–Cl, 1=Li–O, 2=Zr–Cl, 3=Zr–O.

Reproduce with ASE 3.26.0, NumPy and matplotlib: `python3 scripts/structures/compare_lzoc_candidates.py` from repository root. The system ASE 3.22 lacks the timestep metadata used here; use the recorded compatible analysis environment, not the older system installation. Full trajectories remain local/TSUBAME and are excluded from Git.

ASE minimum-image distances handle the full triclinic cell. Per-frame RDF normalization is shell counts divided by N_A(N_B-delta_AB) times shell volume divided by instantaneous cell volume, followed by an equal-frame mean. Self pairs are excluded. Maximum radius is checked against half the minimum cell height. Complete trajectory IDs/type/element mappings and 1101 timestamps are verified before selecting the 21 frames. This is not a full all-frame distance, bond-lifetime or crystallinity audit.

QA: a periodic-boundary toy case tests neighbor counting, shell normalization and self-exclusion; each coordination frequency distribution sums to one. PNGs inspected; all populated coordination bins and a zero-frequency endpoint are visible. Sparse oxygen (12 atoms), temporal correlations and short sampling limit interpretation; RDF peak height is not coordination number.

QA: parser test verifies all three sample counts, time span, atom count and exclusion of the final minimization energy; rendered PNG inspected for readable labels, common scales and clipping. Python/matplotlib generated all formats; vector exports included, not certified against a specific journal's submission rules.
