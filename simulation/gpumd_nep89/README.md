# GPUMD + NEP89 Direction 2 results

This directory contains the GPUMD/NEP89 screening runs for Direction 2:
Li₃YCl₆ and LiNbOCl₄. The 400 K screening and the new 300 K long run are kept
separate so that temperature and supercell effects are not mixed.

## Folder layout

```text
simulation/gpumd_nep89/
├── figures/
│   ├── 400K_baseline/       # original 400 K figures
│   └── 300K_2x2x4/          # new 300 K, 1 ns analysis figures
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

The analysis script unwraps positions in fractional coordinates using the full
triclinic cell, calculates Li-only multi-origin MSD, fits the 100–450 ps lag
window, and reports a Nernst–Einstein estimate. The fit window, (R^2), block
standard deviation, and mean temperature are stored in
[`summary_300K_2x2x4.csv`](results/300K_2x2x4/summary_300K_2x2x4.csv).

| Material / replica | Mean T (K) | (D_{Li}) (cm² s⁻¹) | (R^2) | (sigma_{NE}) (mS cm⁻¹) | block σ(D) (cm² s⁻¹) |
|---|---:|---:|---:|---:|---:|
| Li₃YCl₆_01 | 298.71 | 3.04×10⁻⁸ | 0.998 | 0.0246 | 1.62×10⁻⁹ |
| Li₃YCl₆_02 | 298.67 | 2.52×10⁻⁷ | 0.998 | 0.2070 | 2.79×10⁻⁸ |
| Li₃YCl₆_03 | 300.77 | 2.39×10⁻⁸ | 0.974 | 0.0196 | 1.09×10⁻⁸ |
| LiNbOCl₄ | 298.84 | 5.35×10⁻⁸ | 0.986 | 0.0185 | 1.23×10⁻⁸ |

The Li₃YCl₆ replica mean is
(D=(1.02\pm1.30)\times10^{-7}) cm² s⁻¹ and
(sigma_{NE}=0.084\pm0.107) mS cm⁻¹ (sample standard deviation across
three replicas). The large relative replica spread means that the mean is a
screening result, not a converged material constant. LiNbOCl₄ has only one
replica and therefore has no replica-based error bar.

### Scientific interpretation

At 300 K, NEP89 predicts much lower mobility than the earlier 400 K screening:

- Li₃YCl₆: approximately (0.02–0.21) mS cm⁻¹ by (sigma_{NE}), versus
  the reported room-temperature experimental benchmark above 1 mS cm⁻¹.
- LiNbOCl₄: approximately (0.019) mS cm⁻¹ by (sigma_{NE}), versus the
  reported experimental value near 10.4 mS cm⁻¹.

This is not evidence that the materials are experimentally non-conducting. The
calculation uses one explicit ordered crystal, a generic NEP89 potential, and
tracer/Nernst–Einstein transport; the experiments use disordered pressed
powders and EIS total conductivity. The discrepancy is a diagnostic signal
that the model, ordering, potential, and finite 1 ns sampling must be checked
before any quantitative claim.

## 3. Figures

### New 300 K figures

- [Total Li MSD](figures/300K_2x2x4/msd_total_300K_2x2x4.png)
- [Directional Li MSD](figures/300K_2x2x4/msd_directional_300K_2x2x4.png)
- [Thermostat temperature](figures/300K_2x2x4/temperature_300K_2x2x4.png)
- [Transport summary](figures/300K_2x2x4/transport_summary_300K_2x2x4.png)

SVG versions of the four figures are stored beside the PNG files for editable
text and vector export.

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

The analysis script is [`analyze_300K_2x2x4.py`](analyze_300K_2x2x4.py).
