# Historical technical notes removed from the main narrative

These are historical records, not current task status. Current scientific conclusions are maintained in Material Review.

The existing NEP 700/800/900 K extensions (8665996/8665995/8665994) have now been analysed separately from production. Each contains 1000 finite thermo records at 0.05 ps. No additional run was submitted.

**New production submitted (8677465.1–2):** 320 K proceeds from the completed 50 ps NVT restart to 300 ps NVT production. At 350 K, the additional NPT still showed a 2.06% density decrease between its two 25 ps halves; use its final-25-ps mean volume (8720.237 Å³), preserve fractional positions and velocities, equilibrate 50 ps NVT, then run 300 ps NVT production. Both retain 272 atoms, NEP89, 0.5 fs and MTTK `tperiod 200`. These are project settings, not a claim of exact paper reproduction. The 350 K branch is exploratory fixed-volume transport: the NPT density drift is unresolved and the extra NVT stage does not prove equilibrium density. Runs stop on numerical/output failure; physical convergence remains to be checked. Submission is confirmed; results are pending. Previous results remain separate.

**Next stage submitted: 8677026.1–2.** Task 1: 320 K, 50 ps NVT at the arithmetic mean volume over the preceding NPT's last 50 ps (8138.512 Å³). The endpoint cell and coordinates were scaled isotropically by 1.009478; species, fractional positions and velocities were preserved. Task 2: 350 K, 50 ps NPT at 1 bar from its preceding restart, without cell adjustment. Both retain 272 atoms, NEP89, 0.5 fs and 100 fs thermostat coupling (NPT barostat 1000 fs). Both stop for review; 300 ps production has not been submitted.

Jobs 8676678.1–2 completed 150 ps NPT after the 10 ps ramp. Comparing the last two consecutive 25 ps means:

**Submission history (now completed), 15 September 2026:** array **8676678.1–2**, respectively 320/350 K. Both branches start from the same documented 272-atom, 400 K mother structure: 10 ps NPT ramp, then **150 ps NPT at 1 bar**, timestep 0.5 fs, MTTK coupling periods 100/1000 fs, one GPU per task. The jobs stop for late-block density/energy review. Mean-volume NVT equilibration and **300 ps NVT production per temperature** are planned only after that review; they are not yet submitted. Existing results below remain unchanged.

**Completed analysis:** all four tasks 8676216.1–4 completed 300 ps production. Downloaded trajectories were checked for 272 atoms, unchanged element order, a fixed cell, 3000 frames at 0.1 ps, and finite thermo records. FFT MSD was checked against direct displacement averages. The primary 20–80 ps fit was fixed before inspecting the results, matching the existing 400 K analysis; no temperature or replica was replaced.

**a:** Li MSD and20–80 ps fit; **b:** framework MSD, including substantial Cl motion; **c:** raw PE per atom and5 ps means; **d:** four consecutive50 ps blocks, each fitted at5–20 ps lag. Block estimates and the full-trajectory fit use different windows and are not interchangeable error bars.200 ps production8676040.3 is complete; apparent transport coexists with residual relaxation.

|LSZC|272: Li32Zr32Cl128S16O64|400 K pilot and 320/330/340/350 K, 300 ps array8676216 analysed|Sulfate retained, but Zr environment/density and the temperature trend differ from reference|

|Li₃PS₄|512: Li192P64S256|300/500/700/900 K200 ps production analysed, array8675738|Transport differs from reference;300 K plateau and900 K host motion remain|
