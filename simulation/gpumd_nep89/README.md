# NEP89 + GPUMD: 400 K direction-2 run

Job `8439066` completed on TSUBAME with GPUMD 5.0 and the NEP89 potential. Each structure used a 1 fs timestep, 10 ps NVT equilibration, and 100 ps production at 400 K. Production coordinates were written every 1000 steps (100 frames per structure).

Remote output:

```text
/gs/fs/tgj-26ICP/uf03782/li-research-smoke/gpumd_nep89_smoke/runs_400K_10ps_eq_100ps_prod_20260818_225849/
```

## Preliminary Li MSD analysis

The Li trajectories were unwrapped with the minimum-image convention in fractional coordinates and fitted over the 40--100 ps interval. The diffusion estimate is the 3D Einstein estimate, `D = slope(MSD)/(6)`.

| Structure | Li atoms | MSD at 100 ps (Å²) | D (cm² s⁻¹) | Nernst–Einstein σ at 400 K (mS cm⁻¹) |
|---|---:|---:|---:|---:|
| Li₃YCl₆_01 | 72 | 13.55 | 2.07 × 10⁻⁶ | 125.8 |
| Li₃YCl₆_02 | 72 | 7.10 | 1.08 × 10⁻⁶ | 66.4 |
| Li₃YCl₆_03 | 72 | 11.13 | 1.15 × 10⁻⁶ | 71.0 |
| LiNbOCl₄ | 32 | 6.92 | 7.42 × 10⁻⁷ | 19.2 |

The three Li₃YCl₆ replicas average approximately `1.43 × 10⁻⁶ cm² s⁻¹` over this fit window. The Nernst–Einstein conductivity is an upper-bound-like estimate because it neglects distinct-ion correlation terms; it is not the same as a directly measured or Green–Kubo conductivity.

## Interpretation and limitation

The thermostat temperatures remain near 400 K and all four runs completed without a GPUMD error. However, the predicted Li mobility—especially for Li₃YCl₆—is high compared with the original room-temperature experimental benchmark. These values must therefore be treated as a NEP89 screening result, not as validated material properties. Before using them in a conclusion, compare NEP89 energies/forces and short trajectories against DFT or the MACE runs, and perform a block-size/fit-window uncertainty analysis.
