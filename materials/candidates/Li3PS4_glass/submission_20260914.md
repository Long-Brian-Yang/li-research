# Submission record

SGE accepted job **8670632**, `lips_nep89_trial`, group `tgj-26ICP`, one `gpu_1` slot, maximum walltime 1 hour.

Preparation target: 512 atoms, 611 ps total (1 ps smoke + 10 ps heating + 100 ps melt + 480 ps quench + 20 ps relaxation diagnostic). No production or Arrhenius analysis is included.

Remote output: `/gs/fs/tgj-26ICP/uf03782/yang/li-research/runs/amorphous/Li3PS4/nep89/preparation_8670632`.

Submission acceptance does not mean completion or validated amorphous structure. Source and potential provenance are recorded in the run directory. The heating and final relaxation duration, cell size and thermostat/barostat settings are project choices documented in README.md.

Live verification: qstat showed `r` on r22n1; `stages_completed.txt` confirmed smoke and heating completed, and melt directory was active. Full preparation was not yet complete at this check.
