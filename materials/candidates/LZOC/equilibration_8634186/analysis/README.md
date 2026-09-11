# Candidate 3: post-equilibration check

Checked 2026-09-11, TSUBAME job 8634186, MACE-MPA-0, 300 K/1 bar NPT.
All 1,001 frames span 0–50 ps at 0.05 ps intervals. Each has 192 unique IDs,
consistent species/type mapping and Li42Zr24O12Cl114 composition. The final
data-file cell and periodic pair distances match the last trajectory frame.

## Assessment

Retain candidate 3 as the working disordered structure. The additional run
supports improved short-term structural stability, not proof of a fully
equilibrated amorphous phase. No production job was submitted during analysis.
There is no clear reason in these diagnostics to generate more candidates.

| Metric | 30–40 ps | 40–50 ps |
|---|---:|---:|
| Mean temperature / K | 298.046 | 300.152 |
| Mean density / g cm−3 | 1.93382 | 1.91753 |
| Mean potential energy / eV, whole cell | −912.33213 | −912.45019 |
| Li–Cl diagnostic coordination | 3.9909 | 4.0261 |
| Zr–Cl diagnostic coordination | 4.6210 | 4.6052 |
| Zr–O diagnostic coordination | 1.1250 | 1.1250 |

Last 20 ps: T=299.10 K, density=1.92566 g/cm³, PE slope=−0.011743 eV/ps
(−0.06116 meV/atom/ps). The preceding preparation's last 5 ps slope was
−0.12614 eV/ps; these are different windows, so the reduction is descriptive,
not a statistical convergence test. Residual aging/relaxation is possible.
The two late density means differ by about 0.85%; density is not monotonically
decreasing over the entire run. Final instantaneous density is 1.91385 g/cm³.

## RDF and order

[rdf_blocks.csv](rdf_blocks.csv) contains unsmoothed RDFs averaged over 21
frames per window at 0.5 ps spacing (40 ps boundary shared). ASE triclinic MIC,
rmax=4.5 Å, bin width=0.05 Å, explicit shell volumes and finite-pair-count
normalization, with self pairs excluded. No input trajectory was altered.
Coordination uses fixed diagnostic cutoffs: Li–Cl 3.2 Å, Li–O 2.7 Å,
Zr–Cl 3.0 Å, Zr–O 2.6 Å, Cl–Cl 4.0 Å. These are NOT optimized RDF minima.

Largest sampled RDF peaks shift by at most 0.10 Å between late windows;
bin maxima are noisy and are not precision bond-length estimates. The sampled
minimum pair distance is 1.734 Å, with no zero-distance overlaps. Broad local
coordination is similar between the windows; Li–O is sparsely sampled.

Using the original preparation's ten strongest initial hkl reflections,
unweighted mean intensity retention is Cl 18.59%→18.87%, Zr 8.09%→7.89%.
Original-order signals remain attenuated and similar between late blocks.
Cl retention is higher than the earlier 12.6% preparation-end diagnostic;
therefore order is not claimed to decrease monotonically. This is not a
crystalline fraction and cannot exclude other/new ordered motifs. A 192-atom
cell and 4.5 Å RDF range cannot establish absence of long-range crystallinity.

## Next step

A temperature-defined exploratory production run can use this candidate after
appropriate equilibration at that target temperature, retaining block checks
for aging. Do not label transport coefficients converged in advance; at 300 K,
200 ps may provide insufficient Li hopping statistics. Temperature selection
and submission remain separate from this completed check.

Full numbers and input fingerprints: [diagnostics.json](diagnostics.json).
Reproduce with ASE/NumPy from repository root:
`python3 scripts/structures/check_lzoc_equilibration.py`.
The script also reads the prior candidate3_check/diagnostics.json for fixed hkl
references. Source trajectories remain local/TSUBAME, not in GitHub.
