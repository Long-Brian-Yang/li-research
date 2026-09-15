# LSZC common-cell four-temperature rerun

Submitted2026-09-15 JST: TSUBAME array8679150.1–4, group tgj-26ICP, gpu_1,30-minute wall ceiling per task,max2concurrent. Tasks map to320/330/340/350K respectively. This is not a runtime forecast.

Each task: same272atom320Kpreproduction structure and cell, newtarget-temperature velocities,50psNVT+300psNVT. NEP89,0.5fs,MTTK100fsthermal coupling,thermo0.05ps,trajectory0.1ps. No pressure-driven cell change or experimental-density scaling. Seeds9155320/9155330/9155340/9155350.

Input: `materials/candidates/LSZC/production300_inputs/320K.xyz`.
InputSHA256:`d4b29f986d8a6d548f9e6e320ea7b78df263a0bd0849adc78c60a6309c316b03`.
NEPSHA256:`75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1`.
CellV8138.552255Å³, densityabout1.880g/cm³. Inputhashverifiedremote before submission and again byeachjob. No oldcoordinatesoroutputs overwritten.

Runner:`scripts/structures/submit_lszc_matched4t.sh`; tested dry-run schedules,invalidtaskhandling,andbashsyntax. Outputsunder`/gs/fs/tgj-26ICP/uf03782/yang/li-research/runs/amorphous/LSZC/nep89/matched4t_{T}K_8679150/`.

Scientific rationale: old320/350Kcells had different densitiesandnonmonotonic apparentD. This controlledisochoricseries removesdensitychoicefromtemperaturecomparison, notanequilibrium-isobaricreproduction. Pressure,energy,coordination,fullMSDandlocalslopestabilitymustbeassessed. No guaranteedEa;no selecting favourabletemperaturesorclosestpaperD. Existingendpointfiguresremainhistoricalcompletedresultsuntilnewanalysis.
