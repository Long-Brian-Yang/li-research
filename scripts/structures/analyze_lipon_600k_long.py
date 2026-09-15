"""Analyse the two completed 600 K, 600 ps LiPON trajectories."""
from collections import Counter
from pathlib import Path
import csv
import json

import numpy as np
from ase.io import iread, read

from analyze_lipon_transport import MASS, rdf_and_coordination
from analyze_lzoc_production import fit_msd, unwrap, window_msd

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/amorphous_review_20260915"
SOURCE = BASE / "source/LiPON_transport_long"
OUT = BASE / "LiPON_transport_long"
WINDOWS = ((20, 100), (20, 150), (50, 150), (50, 200), (100, 250), (100, 300))


def analyse(replica):
    run = SOURCE / f"bulk_transport_600K_R{replica}_600ps_8680487"
    prod = run / "production"
    assert (run / "completed.txt").exists()
    start = read(prod / "model.xyz")
    frames = list(iread(prod / "dump.xyz"))
    assert len(frames) == 6000
    symbols = np.asarray(start.get_chemical_symbols())
    assert Counter(symbols) == Counter(Li=47, P=16, O=56, N=5)
    assert all(np.allclose(frame.cell, start.cell, atol=1e-7, rtol=0) for frame in frames)
    positions = np.asarray([start.positions] + [frame.positions for frame in frames])
    unwrapped = unwrap(positions, start.cell.array)
    masses = np.asarray([MASS[s] for s in symbols])
    corrected = unwrapped - np.average(unwrapped, axis=1, weights=masses)[:, None, :]
    lag = np.arange(6001) * 0.1
    msd = {s: window_msd(corrected[:, symbols == s]) for s in ("Li", "P", "O", "N")}
    fits = [fit_msd(lag, msd["Li"], lo, hi) for lo, hi in WINDOWS]
    thermo = np.loadtxt(prod / "thermo.out")
    assert thermo.shape == (12000, 18) and np.isfinite(thermo).all()
    quarter = len(thermo) // 4
    structure = rdf_and_coordination(frames, symbols, range(5400, 6000, 20))
    block_rows = []
    # Independent 150 ps blocks, fitted over 20--100 ps within each block.
    for block in range(4):
        segment = corrected[block * 1500:(block + 1) * 1500 + 1, symbols == "Li"]
        segment_lag = np.arange(1501) * 0.1
        segment_msd = window_msd(segment)
        fit = fit_msd(segment_lag, segment_msd, 20, 100)
        block_rows.append({"replica": replica, "block": block + 1, **fit})
    np.savetxt(
        OUT / f"600K_R{replica}_MSD.csv",
        np.column_stack([lag] + [msd[s] for s in ("Li", "P", "O", "N")]),
        delimiter=",", header="lag_ps,Li_A2,P_A2,O_A2,N_A2", comments="",
    )
    return {
        "replica": replica,
        "fits": fits,
        "block_fits": block_rows,
        "mean_temperature_K": float(thermo[:, 0].mean()),
        "PE_last_minus_first_quarter_meV_atom": float(
            (thermo[-quarter:, 2].mean() - thermo[:quarter, 2].mean()) / 124 * 1000
        ),
        "minimum_NN_A": structure["minimum_NN_A"],
        "Li_MSD_100ps_A2": float(msd["Li"][1000]),
        "Li_MSD_300ps_A2": float(msd["Li"][3000]),
        "framework_max_MSD_100ps_A2": float(max(msd[s][1000] for s in ("P", "O", "N"))),
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [analyse(replica) for replica in (4, 5)]
    with (OUT / "600K_long_fit_windows.csv").open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["replica", "lo_ps", "hi_ps", "D_cm2_s", "R2", "alpha"])
        for row in rows:
            for fit in row["fits"]:
                writer.writerow([row["replica"], fit["lo_ps"], fit["hi_ps"], fit["D_cm2_s"], fit["R2"], fit["alpha"]])
    with (OUT / "600K_long_blocks.csv").open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["replica", "block", "lo_ps", "hi_ps", "D_cm2_s", "R2", "alpha"])
        for row in rows:
            for fit in row["block_fits"]:
                writer.writerow([row["replica"], fit["block"], fit["lo_ps"], fit["hi_ps"], fit["D_cm2_s"], fit["R2"], fit["alpha"]])
    (OUT / "analysis.json").write_text(json.dumps(rows, indent=2) + "\n")
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
