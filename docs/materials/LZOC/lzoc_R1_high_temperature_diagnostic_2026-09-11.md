# LZOC R1 high-temperature screening diagnosis

> Historical record / 历史记录：保留记录当时的设置与判断，不作为实时任务状态。参见 [材料文档索引](README.md)。

Source: TSUBAME `/gs/fs/tgj-26ICP/uf03782/yang/li-research/runs/amorphous/LZOC/mace_mpa0/high_temperature_8631254/replica_1/`.

## Decision

Do not proceed directly to quenching or use this trajectory for production transport properties. The 1500 K, 1 bar, 20 ps NPT screen completed numerically but developed pronounced spatial inhomogeneity and voids. This does not establish a physically valid homogeneous melt. R2 was stopped and R3 cancelled at the user's request; retain their existing files.

## Verified observations

- 256 atoms: Li56 Zr32 O16 Cl152, all retained. Input mapping Li/Zr/O/Cl verified.
- Actual input: metal units, timestep 0.0005 ps, 40000 steps; thermostat damping 0.1 ps, barostat damping 1 ps; isotropic pressure target 1 bar.
- Density independently recomputed from atomic masses and cell volume agrees with log: 2.167293 to 0.864236 g/cm³. Initial density is a construction assumption, not an experimental reference.
- Final volume 17200.704 Å³ versus initial 6859 Å³: 2.508-fold expansion.
- All 401 saved frames examined for O–O distances with minimum-image periodic boundaries: minimum 2.238289 Å; zero frames below the diagnostic threshold 1.9 Å. No recurrence of the original short O–O pair, but this alone does not validate the chemistry.

| Time window (ps) | Mean temperature (K) | Mean pressure (bar) | Mean density (g/cm³) | Density SD (g/cm³) |
|---|---:|---:|---:|---:|
| 0–5 | 1491.23 | 1213.25 | 1.25207 | 0.29475 |
| 5–10 | 1489.38 | -14.91 | 0.99910 | 0.05282 |
| 10–15 | 1503.43 | 14.21 | 1.08885 | 0.06542 |
| 15–20 inclusive | 1495.71 | 163.50 | 1.00399 | 0.08119 |

Windows are left-inclusive/right-exclusive except the last includes 20 ps. These are descriptive statistics, not independent-sample uncertainty estimates.

## Spatial inhomogeneity

Sample a uniform 16×16×16 fractional-coordinate grid in each cubic cell. Compute the nearest atomic-center distance using minimum-image periodic boundaries. This is a geometric void diagnostic, not physical porosity or a bonding classification.

| Time (ps) | Fraction with nearest atom >4 Å | Largest sampled nearest-atom distance (Å) |
|---|---:|---:|
| 0 | 0 | 3.307 |
| 5 | 0.0881 | 5.859 |
| 10 | 0.0388 | 5.429 |
| 15 | 0.0393 | 5.447 |
| 20 | 0.1472 | 7.631 |

The final configuration has substantial empty regions. A phase-separated/clustered or cavitated state is a possible interpretation, not a verified chemical decomposition assignment.

## Mobility screening

Use saved unwrapped coordinates sorted by atom ID. Integrate successive fractional-coordinate increments multiplied by the mean box lengths of the two frames, removing affine expansion. Subtract the final all-atom arithmetic-mean displacement (not a mass-weighted COM correction).

20 ps endpoint displacement RMS: Li 16.276 Å; Zr 14.422 Å; O 12.367 Å; Cl 15.610 Å. These single-origin diagnostics indicate substantial motion of all species; they are NOT Einstein diffusion coefficients. Cluster translation and finite-dump-interval effects remain possible. No transport inference or activation-energy fit is made.

## Unresolved causes and next checkpoint

Units, atom mapping and density arithmetic do not explain the observed expansion. Potential accuracy for high-temperature low-density configurations, the physical suitability of 1500 K at 1 bar, and ML-IAP stress/virial consistency remain unverified. Do not claim the root cause is known.

Recommended next diagnostic: verify pressure/virial against finite-volume energy differences on saved snapshots, then design a single-replica controlled comparison (e.g. fixed-volume high-temperature screening) with the density choice explicitly justified. Fixing the volume cannot itself prove that a melt is physically valid. Do not silently impose pressure or density to produce a desired structure.
