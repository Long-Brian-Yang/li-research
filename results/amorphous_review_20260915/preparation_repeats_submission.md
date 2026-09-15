# Preparation repeats: submission provenance

Submitted 2026-09-15 JST to TSUBAME group tgj-26ICP. Array **8678859.1–4**, maximum two concurrent tasks; gpu_1, one-hour wall limit per task (limit, not runtime estimate). Confirmed tasks1/2 running and3/4 queued after submission.

|Task|Material|Thermal seed|Atoms|Total preparation ps|
|---|---|---|---|---|
|1|Li3PS4|9153101|512|611|
|2|Li3PS4|9153102|512|611|
|3|LiPON|9154101|124|63|
|4|LiPON|9154102|124|63|

Runner: `scripts/structures/submit_preparation_repeats.sh`; dry-run schedules and tests checked before upload and submission. Three tests passed, bash syntax passed. Inputs and potential were hash-verified on TSUBAME before submission and are checked again in each job.

- NEP89 SHA256: `75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1`
- Li3PS4 precursor SHA256: `8976c5ee5a0d89ea15e817c95afef9c4cda4c4dbd5a8980febe1e50831054e48`
- LiPON precursor SHA256: `059d2d5793fd4bfe9dfcc77905b0c8735e3e050737abc6cde0d890d3ac3dd8e7`

Remote root: `/gs/fs/tgj-26ICP/uf03782/yang/li-research`.
Outputs: `runs/amorphous/{Li3PS4,LiPON}/nep89/prep_repeat_R{1,2}_8678859/`.
Each run saves its input, generated stage run.in, executable/potential/input hashes, stage logs, trajectory, thermo and restart. No automatic production, DFT or overwriting of old results.

These are different stochastic thermal histories from the same precursor per material, not different LiPON substitution patterns. Both outcomes must be analysed, including failures. Selection is based on interpretable structure and sampling, not closeness to literature D or conductivity. Main report carries scientific settings; this file retains scheduler provenance.
