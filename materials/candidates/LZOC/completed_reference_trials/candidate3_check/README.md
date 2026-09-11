# Candidate 3 structural screening — 2026-09-11

## Decision

Retain candidate 3 for further equilibration, but do not label it a validated,
fully equilibrated amorphous structure or use this preparation trajectory for
formal transport fitting. No new MD job was submitted during this check.

## Evidence

Source: TSUBAME job 8631935.3, downloaded `source_3/candidate.lammpstrj`,
`candidate.log` and `initial_minimized.data`. SHA256 fingerprints are in
[diagnostics.json](diagnostics.json). All 1,101 frames span 0–55 ps, with unique
IDs 1–192, fixed type/element mapping and Li42Zr24O12Cl114 composition.

Last 5 ps thermo samples (mean ± frame standard deviation, not uncertainty):

| Quantity | Result |
|---|---|
| Temperature | 299.08 ± 18.38 K |
| Density | 1.93176 ± 0.02695 g/cm³ |
| Potential energy, whole cell | −912.1966 ± 0.4869 eV |
| Potential-energy fitted slope | −0.1261 eV/ps, or −0.657 meV/atom/ps |

The short late window still shows relaxation: the energy slope corresponds to
about −0.63 eV across 5 ps. This is not proof of a statistically significant
long-term drift, nor an energy-conservation test in NPT. It is insufficient to
declare equilibration. The previously reported 1.98326 g/cm³ is the final-frame
cell density, not this temporal mean.

## Local structure and initial-order retention

21 frames sampled every 0.25 ps over 50–55 ps were used for RDF. ASE triclinic
minimum-image distances, explicit spherical shell volumes and finite-count
normalization were used; identical-atom self distances were excluded. Partial
RDF normalization is N_A(N_B−delta_AB)/V. Bin width 0.05 Å, rmax 4.5 Å,
below half the cell height for every analyzed frame. No smoothing applied.
See [RDF data](rdf.csv). Main sampled peaks: Li–Cl 2.375 Å, Li–O 1.975 Å,
Zr–Cl 2.425 Å, Zr–O 1.975 Å, Cl–Cl 3.575 Å. The high Zr–O peak must not
be interpreted as excessive coordination: O is dilute and the peak is narrow.
The sampled minimum pair distance is 1.769 Å; no zero-distance overlaps occur.

Unweighted reciprocal intensities I(h)=|sum exp(2 pi i h.s)|²/N were evaluated
for Cl and Zr separately. Initial-cell reciprocal vectors with indices −8…8,
one member of each ±h pair, and q=1…5 Å⁻¹ were searched. The strongest ten
initial reflections were followed at identical fractional hkl in each changing
cell. Their summed mean intensity retained 12.6% (Cl) and 7.6% (Zr) of the
initial value. This supports substantial loss of initial periodic order.
It is NOT a crystalline fraction, and does not exclude new ordered motifs,
small crystallites, thermal attenuation or finite-size effects.

RDF only extends to 4.5 Å, so it cannot by itself establish long-range disorder.
The combined evidence supports a substantially disordered candidate, not a
certified fully amorphous material. No experimental density was assumed.

## Next step

Use this same structure for additional equilibration, rather than adding more
candidate structures. Assess density and energy in successive time blocks
before beginning production. Target production temperature remains to be set.

Reproduce from repository root:
`PYTHONPATH=/tmp/lzoc_reference_ase_20260911 python3 scripts/structures/check_lzoc_candidate3.py`
The temporary environment path is local; otherwise install ASE and NumPy in an
analysis environment. The source trajectory is local/TSUBAME, not on GitHub.

Method reference: [ASE RDF documentation](https://docs.ase-lib.org/_modules/ase/geometry/rdf.html).
The installed ASE 3.26 partial-RDF helper uses a different normalization; this
analysis therefore uses explicit pair-count normalization instead of that helper.
