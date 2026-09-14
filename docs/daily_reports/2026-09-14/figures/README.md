# Three-candidate preparation figure

Same LZOC composition, three related starting configurations; not three materials or independent replicas.

- [PNG](LZOC_three_candidate_preparation.png), [editable SVG](LZOC_three_candidate_preparation.svg), [PDF](LZOC_three_candidate_preparation.pdf).
- Raw extracted thermo: [candidate 1](candidate_1_preparation.csv), [candidate 2](candidate_2_preparation.csv), [candidate 3](candidate_3_preparation.csv).
- [Block means and original-log SHA256](preparation_summary.json).
- Reproduce from repository root: `MPLCONFIGDIR=/tmp/lzoc-mpl-cache python3 scripts/structures/plot_lzoc_preparation.py`.

Each series comprises 1101 samples at 0.05 ps spacing over 0–55 ps. Initial and final minimizations are excluded. Duplicate records at stage boundaries are represented once. Raw thermo traces are not smoothed, rescaled to match another candidate, or cropped to hide early relaxation. Energy is divided by the fixed atom count of 192; it is not mean-subtracted. NPT zoom uses 45–55 ps, while temperature and energy use the full preparation. Units and axis scales are shared within each row. Block statistics use (45,50] and (50,55] ps, 100 correlated samples each; no significance test or confidence interval is claimed.

This is a process comparison, not proof of full equilibration, amorphization or potential accuracy. Candidate 1/2 lack the same documented detailed trajectory/structural and extended equilibration checks as candidate 3. No transport quantities are inferred from the cooling trajectory.

QA: parser test verifies all three sample counts, time span, atom count and exclusion of the final minimization energy; rendered PNG inspected for readable labels, common scales and clipping. Python/matplotlib generated all formats; vector exports included, not certified against a specific journal's submission rules.
