# GPUMD + NEP89 Direction 2 results

This directory contains the GPUMD/NEP89 screening runs for Direction 2:
Li₃YCl₆ and LiNbOCl₄. The 400 K screening and the new 300 K long run are kept
separate so that temperature and supercell effects are not mixed.

## Folder layout

```text
simulation/gpumd_nep89/
├── figures/
│   ├── 400K_baseline/       # original 400 K figures
│   ├── 300K_2x2x4_gpumdkit/ # official GPUMDkit plots (primary)
│   └── 300K_2x2x4_custom_diagnostic/ # supplementary analysis plots
├── results/
│   └── 300K_2x2x4/
│       ├── summary_300K_2x2x4.csv
│       ├── *_msd_300K.csv
│       └── job_8439212/      # local raw trajectory archive; not committed
└── analyze_300K_2x2x4.py
```

The raw 300 K trajectories are approximately 192 MB and remain in the local
results archive/TSUBAME output rather than being committed to GitHub. The
derived CSV files, figures, script, and interpretation are version-controlled.

## 1. Completed production run

TSUBAME job `8439212` completed with `exit_status=0` and `failed=0`. The job
used GPUMD 5.0 and NEP89, one GPU, 1 fs timestep, 300 K Langevin NVT, 100 ps
equilibration, and 1 ns production. Coordinates and thermo data were written
every 1 ps.

| System | Cell | Atoms | Replicas |
|---|---:|---:|---:|
| Li₃YCl₆ | 2×2×4 | 480 | 3 |
| LiNbOCl₄ | 2×2×2 | 128 | 1 |

Li₃YCl₆ 2×2×4 cells were made by repeating the previously relaxed 2×2×2
candidates along (c). They passed the 1,000-step smoke test, but were not
independently full-relaxed after the repeat operation.

## 2. New 300 K transport analysis

The primary analysis uses the official GPUMDkit `msd.out` files, calculates the
three-dimensional Li-only MSD, and fits the 100–300 ps lag window. The
100–200 ps, 200–500 ps, and 100–500 ps alternatives are retained for sensitivity
analysis in [`window_sensitivity_300K_2x2x4.csv`](results/300K_2x2x4/window_sensitivity_300K_2x2x4.csv).
The primary fit window, (R^2), and Nernst–Einstein estimate are stored in
[`summary_300K_2x2x4.csv`](results/300K_2x2x4/summary_300K_2x2x4.csv).

| Material / replica | Mean T (K) | (D_{Li}) (cm² s⁻¹) | (R^2) | (sigma_{NE}) (mS cm⁻¹) |
|---|---:|---:|---:|---:|
| Li₃YCl₆_01 | 298.71 | 3.04×10⁻⁸ | 1.000 | 0.0246 |
| Li₃YCl₆_02 | 298.67 | 2.61×10⁻⁷ | 1.000 | 0.2148 |
| Li₃YCl₆_03 | 300.77 | 2.98×10⁻⁸ | 0.969 | 0.0244 |
| LiNbOCl₄ | 298.84 | 6.02×10⁻⁸ | 0.995 | 0.0208 |

The Li₃YCl₆ replica mean is
(D=(1.10\pm1.35)\times10^{-7}) cm² s⁻¹ and
(sigma_{NE}=0.088\pm0.110) mS cm⁻¹ (sample standard deviation across
three replicas). The large relative replica spread means that the mean is a
screening result, not a converged material constant. LiNbOCl₄ has only one
replica and therefore has no replica-based error bar.

### Compact analysis trajectories

The full all-atom `dump.xyz` files are kept in the local/TSUBAME archive and
are not committed to GitHub. For reproducible MSD re-analysis, Li-only
unwrapped trajectories are exported as CSV:

- [`Li₃YCl₆_01 Li positions`](results/300K_2x2x4/Li3YCl6_01_Li_unwrapped_300K.csv)
- [`Li₃YCl₆_02 Li positions`](results/300K_2x2x4/Li3YCl6_02_Li_unwrapped_300K.csv)
- [`Li₃YCl₆_03 Li positions`](results/300K_2x2x4/Li3YCl6_03_Li_unwrapped_300K.csv)
- [`LiNbOCl₄ Li positions`](results/300K_2x2x4/LiNbOCl4_Li_unwrapped_300K.csv)

Each CSV contains `frame`, `time_ps`, `li_index`, and unwrapped Cartesian
coordinates in Å. These files are analysis products, not replacements for the
original all-atom trajectories.

### Statistical uncertainty versus experimental discrepancy

These are two different quantities:

1. **Simulation statistical uncertainty:** the Li₃YCl₆ replica standard
   deviation is 0.110 mS cm⁻¹, larger than its 0.088 mS cm⁻¹ mean (relative
   spread ≈124.9%). LiNbOCl₄ has one replica, so no independent replica error
   can be calculated. Window sensitivity is reported separately rather than
   treated as an independent replica error bar.
2. **Discrepancy from experiment:** the Li₃YCl₆ paper reports a value above
   1 mS cm⁻¹, so the simulation mean is at least 91.6% below the lower bound
   and at least 11.9× smaller. LiNbOCl₄ gives 0.0185 mS cm⁻¹ versus 10.4
   mS cm⁻¹, a 99.80% shortfall (about 500× smaller).

The papers do not provide a directly usable experimental standard deviation in
the current project record. Therefore a combined z-score or formal confidence
interval against experiment cannot be claimed. The percentages above are
benchmark discrepancies, not experimental measurement errors. The dominant
causes to test are the NEP89 potential, explicit ordering, 300 K sampling time,
and the difference between ideal-crystal σ<sub>NE</sub> and pressed-powder EIS.

### Scientific interpretation

At 300 K, NEP89 predicts much lower mobility than the earlier 400 K screening:

- Li₃YCl₆: approximately (0.02–0.21) mS cm⁻¹ by (sigma_{NE}), versus
  the reported room-temperature experimental benchmark above 1 mS cm⁻¹.
- LiNbOCl₄: approximately (0.021) mS cm⁻¹ by (sigma_{NE}), versus the
  reported experimental value near 10.4 mS cm⁻¹.

This is not evidence that the materials are experimentally non-conducting. The
calculation uses one explicit ordered crystal, a generic NEP89 potential, and
tracer/Nernst–Einstein transport; the experiments use disordered pressed
powders and EIS total conductivity. The discrepancy is a diagnostic signal
that the model, ordering, potential, and finite 1 ns sampling must be checked
before any quantitative claim.

## 3. Official GPUMDkit figures

The primary 300 K plots were regenerated with the official GPUMDkit v1.5.6
workflow on TSUBAME. For each trajectory, GPUMDkit was run as:

```bash
gpumdkit.sh -calc msd dump_unwrapped.xyz Li 1000 500
gpumdkit.sh -plt msd save
gpumdkit.sh -plt thermo save
```

The input trajectory is the GPUMD dump converted to an unwrapped extXYZ by
[`prepare_gpumdkit_unwrapped.py`](prepare_gpumdkit_unwrapped.py). The 1 ps
sampling interval and 500 ps maximum lag are explicit in the command.

- [Li₃YCl₆ replica 1 MSD](figures/300K_2x2x4_gpumdkit/Li3YCl6_01/msd.png) · [thermo](figures/300K_2x2x4_gpumdkit/Li3YCl6_01/thermo.png)
- [Li₃YCl₆ replica 2 MSD](figures/300K_2x2x4_gpumdkit/Li3YCl6_02/msd.png) · [thermo](figures/300K_2x2x4_gpumdkit/Li3YCl6_02/thermo.png)
- [Li₃YCl₆ replica 3 MSD](figures/300K_2x2x4_gpumdkit/Li3YCl6_03/msd.png) · [thermo](figures/300K_2x2x4_gpumdkit/Li3YCl6_03/thermo.png)
- [LiNbOCl₄ MSD](figures/300K_2x2x4_gpumdkit/LiNbOCl4/msd.png) · [thermo](figures/300K_2x2x4_gpumdkit/LiNbOCl4/thermo.png)

The corresponding GPUMDkit `msd.out` and `average_results.txt` files are kept
under [`results/300K_2x2x4_gpumdkit/`](results/300K_2x2x4_gpumdkit/). The
previous custom diagnostic figures are retained separately under
[`figures/300K_2x2x4_custom_diagnostic/`](figures/300K_2x2x4_custom_diagnostic/)
and are not used as the primary GPUMDkit result.

GPUMDkit's `sdc` and `msd_sdc` commands were intentionally not run: they require
a valid GPUMD `sdc.out` from a heat-current/Green–Kubo calculation. A tracer
MSD cannot be relabeled as an SDC, so no SDC figure is reported here.

### Original 400 K baseline figures

The original plots are preserved without overwriting them in
[`figures/400K_baseline/`](figures/400K_baseline/). They correspond to the
short 400 K job `8439066` (10 ps equilibration + 100 ps production), not the
new 300 K 2×2×4 run.

## 4. Method and limitations

For each trajectory, Li positions are unwrapped in fractional coordinates with
the complete triclinic cell. The three-dimensional Einstein estimate is

\[
D_{Li}=\frac{1}{6}\frac{d\,\mathrm{MSD}}{dt}.
\]

The reported conductivity is

\[
\sigma_{NE}=\frac{n_{Li}q^2D_{Li}}{k_BT},
\]

which ignores distinct Li–Li correlations. It is not identical to a collective
Green–Kubo conductivity or to pressed-powder EIS. The current analysis also
does not yet provide a Haven ratio, DFT force validation, or an independently
relaxed 2×2×4 cell.

## 5. Next checks

1. Repeat Li₃YCl₆ with at least one additional potential or DFT short
   trajectory to test NEP89 forces and barriers.
2. Extend Li₃YCl₆ to 3–5 ns if block uncertainty remains large.
3. Add two LiNbOCl₄ replicas before assigning an uncertainty interval.
4. Compare 2×2×4 and 2×2×2 using identical analysis and temperature.
5. Add collective charge-current/Green–Kubo conductivity if supported by the
   available trajectory workflow.

The official-output window analysis is [`analyze_gpumdkit_windows.py`](analyze_gpumdkit_windows.py).
The coordinate conversion helper is [`prepare_gpumdkit_unwrapped.py`](prepare_gpumdkit_unwrapped.py).
