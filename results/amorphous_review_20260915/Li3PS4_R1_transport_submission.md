# Li₃PS₄: one reviewed preparation for transport

User requested only one prepared structure for subsequent transport. R1 was designated before transport analysis; R2 is retained without a second transport series.

## Basic review

Source: `runs/amorphous/Li3PS4/nep89/prep_repeat_R1_8678859/relaxation/`.
Reviewed 400 thermo rows and 200 frames across20 ps; composition Li192P64S256 and finite outputs verified. Final100 frames (10 ps) used for periodic contact/coordination check.

|Metric|Result|
|---|---|
|Mean temperature|300.5158 K|
|Mean diagonal pressure|0.002272 GPa|
|First/last10 ps density|2.209611 / 2.205292 g/cm³|
|Last−first10 ps PE|+0.299437 meV/atom|
|P–S CN at2.6 Å|4.000; sampled fourfold fraction1.000|
|Minimum periodic distance in sampled frames|1.902265 Å|

This supports exploratory continuation, not a full equilibrium or accuracy claim.

## Submission

Array **8679199.1–4**, group tgj-26ICP, tasks300/500/700/900 K, max2concurrent, gpu_1,30-minute wall ceiling each. Each10 ps NPT adjustment +50 ps NPT1 bar +200 ps NVT production;0.5 fs,MTTK100/1000 fs. No R2 transport. Retains previous transport schedule for comparison, not exact Chen replication.

Input SHA256: `08f4c4f7a07fab822637dd936dc656b9886fdf238cedcbdae651dea68c325bf6`.
Runner: `scripts/structures/submit_lps_r1_transport.sh`.
Outputs below `/gs/fs/tgj-26ICP/uf03782/yang/li-research/runs/amorphous/Li3PS4/nep89/r1_transport_{T}K_8679199/`.

## Remote analysis result

All four production trajectories were analysed in place on TSUBAME; raw trajectories were not copied into the repository. Compact MSD, RDF, angle, fit-diagnostic and thermodynamic tables are stored in `Li3PS4_R1_transport/`.

Using the common 20–80 ps diagnostic, apparent D is 5.401e-8, 4.209e-7, 7.925e-6 and 3.065e-5 cm2/s at 300, 500, 700 and 900 K. The corresponding log–log exponents are 0.269, 0.535, 0.916 and 0.926; therefore only 700 and 900 K show a clear diffusive regime. A 500–900 K diagnostic gives Ea=0.4189 eV but is not adopted as a definitive activation energy because 500 K remains subdiffusive.

The 300 K late-production Li–S RDF maximum is 2.425 A and the mean S–P–S angle is 109.38 degrees. P remains fourfold coordinated at 300 and 500 K; the late-production fourfold fractions are 99.84% and 98.75% at 700 and 900 K. The current R1 figures replace the earlier preparation in the Material Review; the earlier result remains archived as a preparation-sensitivity control.
New transport not yet analysed. Source structure and old trajectories unchanged.
