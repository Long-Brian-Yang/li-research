# LSZC common-cell four-temperature second velocity repeat

Submitted 2026-09-15 JST as TSUBAME array **8679279.1–4**, corresponding to 320/330/340/350 K. Maximum two concurrent GPU tasks. At verification, 320/330 K were running and 340/350 K queued.

The second series uses the same 272-atom input, cell, NEP89 potential, 0.5 fs timestep, 50 ps NVT equilibration and 300 ps NVT production as the first common-cell series. Only the initialized velocities differ. Seeds are 9157320, 9157330, 9157340 and 9157350.

The original input SHA256 remains `d4b29f986d8a6d548f9e6e320ea7b78df263a0bd0849adc78c60a6309c316b03`; NEP89 SHA256 remains `75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1`.

Outputs: `/gs/fs/tgj-26ICP/uf03782/yang/li-research/runs/amorphous/LSZC/nep89/matched4t_R2_{T}K_8679279/`.

Both repeats must be retained. Representative display may use a structurally and statistically interpretable trajectory, but a formal activation-energy conclusion cannot be assembled by selecting each temperature solely for proximity to the literature value.
