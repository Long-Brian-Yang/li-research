"""Compare all LiPON velocity-seed repeats without target-value selection."""
from collections import Counter
from pathlib import Path
import csv, json
import numpy as np
from ase.io import iread, read

from analyze_lzoc_production import fit_msd, unwrap, window_msd
from analyze_lipon_transport import MASS, rdf_and_coordination

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/amorphous_review_20260915"
OUT = BASE / "LiPON_transport_repeats"
TEMPS = (600, 900, 1200, 1500)
WINDOWS = ((10, 50), (20, 80), (20, 100), (40, 120), (50, 150), (50, 200))


def run_dir(t, rep):
    if rep == 1:
        return BASE / "source/LiPON_transport" / f"bulk_transport_{t}K_8679521"
    return BASE / "source/LiPON_transport_repeats" / f"bulk_transport_{t}K_R{rep}_8680013"


def analyse_one(t, rep):
    base = run_dir(t, rep)
    assert (base / "completed.txt").exists()
    prod = base / "production"
    start = read(prod / "model.xyz") if (prod / "model.xyz").exists() else read(base / "equil/restart.xyz")
    frames = list(iread(prod / "dump.xyz"))
    assert len(frames) == 3000
    symbols = np.asarray(frames[0].get_chemical_symbols())
    assert Counter(symbols) == Counter(Li=47, P=16, O=56, N=5)
    positions = np.asarray([start.positions] + [a.positions for a in frames])
    cell = np.asarray(frames[0].cell)
    assert all(np.allclose(a.cell, cell, atol=1e-7, rtol=0) for a in frames)
    unwrapped = unwrap(positions, cell)
    masses = np.asarray([MASS[s] for s in symbols])
    corrected = unwrapped - np.average(unwrapped, axis=1, weights=masses)[:, None, :]
    lag = np.arange(3001) * 0.1
    msd = {s: window_msd(corrected[:, symbols == s]) for s in ("Li", "P", "O", "N")}
    fits = [fit_msd(lag, msd["Li"], lo, hi) for lo, hi in WINDOWS]
    primary = next(x for x in fits if (x["lo_ps"], x["hi_ps"]) == (20, 100))
    stable = [x for x in fits if (x["lo_ps"], x["hi_ps"]) in ((20, 80), (20, 100), (40, 120))]
    ds = np.asarray([x["D_cm2_s"] for x in stable])
    window_cv = float(np.std(ds, ddof=1) / np.mean(ds)) if np.all(ds > 0) else float("inf")
    thermo = np.loadtxt(prod / "thermo.out")
    assert thermo.shape == (6000, 18) and np.isfinite(thermo).all()
    q = len(thermo) // 4
    pe_drift = float((thermo[-q:, 2].mean() - thermo[:q, 2].mean()) / 124 * 1000)
    late = rdf_and_coordination(frames, symbols, range(2700, 3000, 10))
    fw100 = max(float(msd[s][1000]) for s in ("P", "O", "N"))
    result = {
        "T_K": t, "replica": rep, "D_cm2_s": primary["D_cm2_s"],
        "R2": primary["R2"], "alpha": primary["alpha"], "window_CV": window_cv,
        "Li_MSD100_A2": float(msd["Li"][1000]), "framework_max_MSD100_A2": fw100,
        "framework_to_Li_MSD100": fw100 / float(msd["Li"][1000]),
        "PE_drift_meV_atom": pe_drift, "late_min_NN_A": late["minimum_NN_A"],
        "fits": fits,
    }
    # Predeclared diagnostic ranking: diffusion quality first, then stationary host.
    result["quality_score"] = (
        8 * abs(primary["alpha"] - 1) + 4 * window_cv + 10 * (1 - primary["R2"])
        + 0.02 * abs(pe_drift) + 0.5 * result["framework_to_Li_MSD100"]
        + (5 if late["minimum_NN_A"] < 1.6 else 0)
    )
    np.savetxt(OUT / f"{t}K_R{rep}_MSD.csv", np.column_stack([lag] + [msd[s] for s in ("Li", "P", "O", "N")]),
               delimiter=",", header="lag_ps,Li_A2,P_A2,O_A2,N_A2", comments="")
    return result


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [analyse_one(t, r) for t in TEMPS for r in (1, 2, 3)]
    selected = {}
    for t in TEMPS:
        choices = [x for x in rows if x["T_K"] == t]
        selected[str(t)] = min(choices, key=lambda x: x["quality_score"])["replica"]
    with (OUT / "repeat_diagnostics.csv").open("w", newline="") as f:
        cols = ["T_K", "replica", "D_cm2_s", "R2", "alpha", "window_CV", "Li_MSD100_A2",
                "framework_max_MSD100_A2", "framework_to_Li_MSD100", "PE_drift_meV_atom",
                "late_min_NN_A", "quality_score"]
        w = csv.DictWriter(f, cols, lineterminator="\n"); w.writeheader()
        w.writerows({k: x[k] for k in cols} for x in rows)
    payload = {"selection_rule": "minimum predeclared quality score; no literature D enters score",
               "selected_replica": selected, "results": rows}
    (OUT / "repeat_diagnostics.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"selected_replica": selected,
                      "summary": [{k: x[k] for k in ("T_K", "replica", "D_cm2_s", "R2", "alpha", "window_CV", "framework_max_MSD100_A2", "PE_drift_meV_atom", "late_min_NN_A", "quality_score")} for x in rows]}, indent=2))


if __name__ == "__main__":
    run()
