# Best Arrhenius Temperature/Replica Combinations

These records preserve the best replica combinations selected against the
experimental activation energy.  MSD values were fitted over the 10--90%
production-trajectory window.  Replica selection is a screening result, not
an uncertainty-free ensemble average.

## LiNbOCl4

Experimental reference: `Ea_exp ~= 0.24 eV`.

### MACE-MPA-0 medium (closest combination)

| Temperature | Replica |
|---:|---:|
| 600 K | 2 |
| 800 K | 2 |
| 1000 K | 1 |
| 1200 K | 1 |

- Ea = 0.256 eV
- R2 = 0.968
- Absolute error = 0.016 eV (6.9%)

All 81 one-replica-per-temperature combinations (600/800/1000/1200 K;
3^4 combinations) were enumerated from the latest completed MACE data.  The
next-best combinations are shown below; this makes the selection auditable
instead of reporting only one hand-picked fit.

| Rank | 600 K | 800 K | 1000 K | 1200 K | Ea (eV) | R2 | ΔEa (eV) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | R2 | R2 | R1 | R1 | 0.2565 | 0.9684 | 0.0165 |
| 2 | R2 | R1 | R1 | R1 | 0.2574 | 0.9725 | 0.0174 |
| 3 | R2 | R3 | R1 | R1 | 0.2594 | 0.9749 | 0.0194 |
| 4 | R2 | R2 | R2 | R1 | 0.2743 | 0.9993 | 0.0343 |
| 5 | R2 | R1 | R2 | R1 | 0.2753 | 0.9996 | 0.0353 |
| 6 | R2 | R2 | R3 | R1 | 0.2758 | 0.9988 | 0.0358 |

Rank 1 is the closest to the experimental reference.  Ranks 4--6 have a
higher Arrhenius fit quality, so they are useful sensitivity checks if a more
strictly linear fit is preferred over minimum absolute Ea error.

### SevenNet-nano (closest combination)

| Temperature | Replica |
|---:|---:|
| 600 K | 3 |
| 800 K | 3 |
| 1000 K | 1 |
| 1200 K | 2 |

- Ea = 0.317 eV
- R2 = 0.991
- Absolute error = 0.077 eV (32.1%)

### M3GNet GPU (selected high-linearity combination)

This combination is selected by prioritizing a very high Arrhenius linearity
while retaining a clearly distinguishable activation energy from the
experimental reference. It is not the minimum-error combination.

| Temperature | Replica |
|---:|---:|
| 600 K | 2 |
| 800 K | 3 |
| 1000 K | 1 |
| 1200 K | 3 |

- Ea = 0.3422 eV
- R2 = 0.9996
- Experimental reference: Ea ~= 0.24 eV
- Absolute error = 0.1022 eV (42.6%)

## Li3YCl6

Experimental reference: `Ea_exp ~= 0.40 eV`.

### SevenNet-nano (selected four-temperature combination)

**Current selected record:** this is the combination retained for the present
SevenNet comparison; 500 K is not part of this four-point fit. The experimental
reference is $E_a\approx0.40\ \mathrm{eV}$; this is not the calculated value.

| Temperature | Replica |
|---:|---:|
| 700 K | 3 |
| 800 K | 1 |
| 900 K | 1 |
| 1000 K | 1 |

- Ea = 0.2338 eV
- R2 = 0.9231
- Absolute error = 0.1662 eV (41.6%)

The complete fixed-temperature enumeration (all 81 Replica combinations,
ranked by both (R^2) and (E_a) proximity) is available in
[`sevennet_700_800_900_1000_all_81.md`](sevennet_700_800_900_1000_all_81.md).

The fit is numerically closest among the tested four-temperature combinations,
but its lower R2 means that the 500/600/700/1000 K combination may be a more
stable alternative for reporting.

### MACE-MPA-0 medium (latest completed data)

**正式採用する比較用4点組合せ（current selected result）**

| Temperature | Replica | Diffusion coefficient |
|---:|---:|---:|
| 700 K | R2 | — |
| 800 K | R3 | — |
| 900 K | R1 | — |
| 1000 K | R1 (new rerun) | $4.529\times10^{-5}\ \mathrm{cm^2\,s^{-1}}$ |

- $E_a=0.2763\ \mathrm{eV}$
- $R^2=0.9881$
- This record supersedes the earlier provisional (E_a=0.245\ \mathrm{eV}, R^2=0.962) result.

For a direct comparison with the SevenNet 700/800/900/1000 K selection, the
updated MACE baseline is 700 K/R2, 800 K/R3, 900 K/R1 and 1000 K/R1.  After
replacing the previous 1000 K/R1 value with the new 500 ps rerun, this fit
gives Ea = 0.2763 eV and R2 = 0.9881.  The corresponding 1000 K diffusion
coefficients for the new replicas are 4.529 x 10^-5 (R1) and 4.115 x 10^-5
cm^2/s (R2).  This updated fit supersedes the provisional 0.245 eV result.
The same Arrhenius fit gives (D(300\,\mathrm{K})=2.60\times10^{-8}\,
\mathrm{cm^2\,s^{-1}}).  Using 72 Li ions and the relaxed cell volume
(5439.9 A^3) in the Nernst--Einstein relation gives
\(\sigma_{NE}(300\,\mathrm{K})\approx2.14\,\mathrm{mS\,cm^{-1}}\).
Compared with the experimental 0.51 mS cm^-1 reference, this is about 4.2
times higher (approximately 319% relative error), so it is the same order of
magnitude but not a quantitative match.

The completed MACE set now contains 400, 500, 600, 700, 800, 900 and 1000 K,
with three replicas at each temperature (21 temperature/replica records).
The three 1000 K records were newly extracted directly from the completed
LAMMPS `msd_li.dat` files using the same 50--450 ps (10--90%) fitting window.
Their updated diffusion coefficients are 4.529, 4.115 and 3.034 x 10^-5 cm^2/s
for replicas 1--3, respectively.

Using the experimental reference (E_a\approx0.40\,\mathrm{eV}), all 2,835
four-temperature/replica combinations were enumerated (35 temperature subsets
and (3^4) replica assignments).  The closest combination remains:

| Temperature | Replica |
|---:|---:|
| 400 K | 3 |
| 500 K | 2 |
| 600 K | 1 |
| 700 K | 1 |

- Ea = 0.2961 eV
- R2 = 0.9712
- Absolute error = 0.1039 eV (26.0%)

Including the newly completed 1000 K data, the closest six- and seven-temperature
combinations are:

- Six temperatures: 400 K/R3, 600 K/R3, 700 K/R1, 800 K/R2, 900 K/R1,
  1000 K/R1; Ea = 0.2663 eV, R2 = 0.9883.
- All seven temperatures: 400 K/R3, 500 K/R2, 600 K/R3, 700 K/R1,
  800 K/R2, 900 K/R1, 1000 K/R1; Ea = 0.2537 eV, R2 = 0.9727.

Thus, 1000 K improves the multi-temperature Ea estimate only modestly and
does not bring it to the 0.40 eV experimental value. It is best retained as
a high-temperature sensitivity point rather than used as the sole basis for
claiming agreement.

For comparison, the best five-temperature combination is 400 K/R3, 600 K/R3,
700 K/R1, 800 K/R2 and 900 K/R1, giving Ea = 0.2756 eV and R2 = 0.9922.
The best six-temperature combination (all available temperatures) is
400 K/R3, 500 K/R2, 600 K/R3, 700 K/R1, 800 K/R2 and 900 K/R1, giving
Ea = 0.2630 eV and R2 = 0.9732.

The closest-Ea result is therefore the recommended screening combination;
the five- and six-temperature results should be retained as sensitivity
checks.  None reaches the 0.40 eV experimental reference closely enough to
claim quantitative agreement.
