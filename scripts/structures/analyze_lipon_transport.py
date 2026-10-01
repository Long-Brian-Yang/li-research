"""Analyse every completed LiPON velocity-seed repeat under one fixed method.

No replica is ranked, omitted, or selected by transport value or literature
agreement. D(T) is summarized from all three repeats at each temperature.
"""
from collections import Counter
from pathlib import Path
import csv
import hashlib
import json

import numpy as np
from ase.io import iread, read
from scipy.stats import linregress

from analyze_lzoc_production import fit_msd, unwrap, window_msd
from li_diffusion_style import apply_style

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/amorphous_review_20260915"
SOURCE = BASE / "source/LiPON_transport"
REPEAT_SOURCE = BASE / "source/LiPON_transport_repeats"
OUT = BASE / "LiPON_transport"
FIG = ROOT / "docs/materials/figures"
TEMPERATURES = (600, 900, 1200, 1500)
REPLICAS = (1, 2, 3)
PRIMARY_WINDOW = (20, 100)
WINDOWS = ((10, 50), (20, 80), PRIMARY_WINDOW, (20, 150), (40, 120),
           (50, 150), (50, 200), (100, 250), (100, 300))
COLORS = ("#5e3c99", "#31688e", "#35b779", "#d73027")
MASS = {"Li": 6.94, "P": 30.973761998, "O": 15.999, "N": 14.007}


def run_dir(temperature, replica):
    if replica == 1:
        return SOURCE / f"bulk_transport_{temperature}K_8679521"
    return REPEAT_SOURCE / f"bulk_transport_{temperature}K_R{replica}_8680013"


def fit_arrhenius(temperatures, diffusion):
    temperatures = np.asarray(temperatures, dtype=float)
    diffusion = np.asarray(diffusion, dtype=float)
    if np.any(diffusion <= 0) or np.any(~np.isfinite(diffusion)):
        raise ValueError("Arrhenius fit requires positive finite diffusivities")
    reg = linregress(1 / temperatures, np.log(diffusion))
    return {"Ea_eV": float(-reg.slope * 8.617333262145e-5),
            "R2": float(reg.rvalue**2), "D0_cm2_s": float(np.exp(reg.intercept)),
            "D_300K_extrapolated_cm2_s": float(np.exp(reg.intercept + reg.slope / 300))}


def rdf_and_coordination(frames, symbols, indices):
    pairs = (("P", "O", 2.1), ("P", "N", 2.1), ("Li", "O", 2.7), ("Li", "N", 2.7))
    edges = np.arange(0, 4.5001, 0.05)
    radii = (edges[:-1] + edges[1:]) / 2
    shell = 4 * np.pi / 3 * np.diff(edges**3)
    rdf, cn, minimum_nn = {f"{a}-{b}": [] for a, b, _ in pairs}, {f"{a}-{b}": [] for a, b, _ in pairs}, []
    for idx in indices:
        atoms = frames[idx]
        d = atoms.get_all_distances(mic=True)
        np.fill_diagonal(d, np.inf)
        nn = d[np.ix_(symbols == "N", symbols == "N")]
        minimum_nn.append(float(nn.min()))
        for a, b, cutoff in pairs:
            z = d[np.ix_(symbols == a, symbols == b)]
            na, nb = np.sum(symbols == a), np.sum(symbols == b)
            norm = na * (nb - int(a == b)) * shell / atoms.get_volume()
            key = f"{a}-{b}"
            rdf[key].append(np.histogram(z, edges)[0] / norm)
            cn[key].append(float((z < cutoff).sum(axis=1).mean()))
    return {"r_A": radii, "rdf": {k: np.mean(v, axis=0) for k, v in rdf.items()},
            "coordination": {k: float(np.mean(v)) for k, v in cn.items()},
            "minimum_NN_A": min(minimum_nn)}


def sigma_ne_mscm(diffusion_cm2_s, n_li, volume_a3, temperature):
    charge, kb = 1.602176634e-19, 1.380649e-23
    density = n_li / (volume_a3 * 1e-30)
    return float(density * charge**2 * diffusion_cm2_s * 1e-4 / (kb * temperature) * 10)


def save_figure(fig, stem):
    import matplotlib.pyplot as plt
    apply_style(fig)
    for ext in ("png", "pdf", "svg"):
        fig.savefig(FIG / f"{stem}.{ext}", dpi=300 if ext == "png" else None, bbox_inches="tight")
    plt.close(fig)


def refresh_figure_manifest(stems):
    manifest_path = FIG / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    indexed = {item["file"]: item for item in manifest["assets"]}
    for stem in stems:
        for ext in ("png", "pdf", "svg"):
            path = FIG / f"{stem}.{ext}"
            record = indexed.get(path.name)
            if record is None:
                record = {"file": path.name}
                manifest["assets"].append(record)
                indexed[path.name] = record
            record["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            record["source"] = "scripts/structures/analyze_lipon_transport.py"
    manifest["figure_groups"] = len({Path(item["file"]).stem for item in manifest["assets"]})
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")


def analyse_one(temperature, replica):
    folder = run_dir(temperature, replica)
    assert (folder / "completed.txt").exists(), folder
    production = folder / "production"
    start = read(production / "model.xyz") if (production / "model.xyz").exists() else read(folder / "equil/restart.xyz")
    symbols = np.asarray(start.get_chemical_symbols())
    assert Counter(symbols) == Counter(Li=47, P=16, O=56, N=5)
    frames = list(iread(production / "dump.xyz"))
    assert len(frames) == 3000
    times = np.asarray([frame.info["Time"] for frame in frames]) / 1000
    np.testing.assert_allclose(times, np.arange(1, 3001) * 0.1, atol=1e-7)
    assert all(np.array_equal(symbols, f.get_chemical_symbols()) for f in frames)
    assert all(np.allclose(start.cell, f.cell, atol=1e-7, rtol=0) for f in frames)
    coordinates = np.asarray([start.positions] + [f.positions for f in frames])
    unwrapped = unwrap(coordinates, start.cell.array)
    mass = np.asarray([MASS[s] for s in symbols])
    corrected = unwrapped - np.average(unwrapped, axis=1, weights=mass)[:, None, :]
    lag = np.arange(3001) * 0.1
    msd = {species: window_msd(corrected[:, symbols == species]) for species in ("Li", "P", "O", "N")}
    fits = [fit_msd(lag, msd["Li"], *window) for window in WINDOWS]
    primary = next(f for f in fits if (f["lo_ps"], f["hi_ps"]) == PRIMARY_WINDOW)
    np.savetxt(OUT / f"{temperature}K_R{replica}_MSD.csv",
               np.column_stack([lag] + [msd[s] for s in ("Li", "P", "O", "N")]),
               delimiter=",", header="lag_ps,Li_A2,P_A2,O_A2,N_A2", comments="")
    thermo = np.loadtxt(production / "thermo.out")
    assert thermo.shape == (6000, 18) and np.isfinite(thermo).all()
    structure = rdf_and_coordination(frames, symbols, range(2700, 3000, 10))
    payload = {"T_K": temperature, "replica": replica, "primary_fit": primary,
               "fit_sensitivity": fits, "sigma_NE_mS_cm": sigma_ne_mscm(primary["D_cm2_s"], 47, start.get_volume(), temperature),
               "volume_A3": float(start.get_volume()), "MSD_100ps_A2": {s: float(v[1000]) for s, v in msd.items()},
               "MSD_300ps_A2": {s: float(v[-1]) for s, v in msd.items()},
               "mean_T_K": float(thermo[:, 0].mean()),
               "PE_last_minus_first_quarter_meV_atom": float((thermo[-1500:, 2].mean() - thermo[:1500, 2].mean()) / 124 * 1000),
               "late_structure": {k: v for k, v in structure.items() if k not in ("r_A", "rdf")}}
    return payload, lag, msd, structure


def run():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    all_results, curves, structure_rows, hashes = {}, {}, {}, {}
    for temperature in TEMPERATURES:
        results, temperature_curves, structures = [], [], []
        for replica in REPLICAS:
            result, lag, msd, structure = analyse_one(temperature, replica)
            results.append(result)
            temperature_curves.append((replica, lag, msd))
            structures.append(structure)
            for file in run_dir(temperature, replica).rglob("*"):
                if file.is_file() and file.name != "dump.xyz":
                    hashes[str(file.relative_to(ROOT))] = hashlib.sha256(file.read_bytes()).hexdigest()
        d_values = np.asarray([r["primary_fit"]["D_cm2_s"] for r in results])
        sigma_values = np.asarray([r["sigma_NE_mS_cm"] for r in results])
        all_results[str(temperature)] = {
            "replicas": results,
            "D_mean_cm2_s": float(d_values.mean()),
            "D_sample_sd_cm2_s": float(d_values.std(ddof=1)),
            "sigma_NE_mean_mS_cm": float(sigma_values.mean()),
            "sigma_NE_sample_sd_mS_cm": float(sigma_values.std(ddof=1)),
            "RDF_late_mean": {key: np.mean([s["rdf"][key] for s in structures], axis=0).tolist() for key in structures[0]["rdf"]},
            "RDF_late_r_A": structures[0]["r_A"].tolist(),
            "coordination_mean": {key: float(np.mean([s["coordination"][key] for s in structures])) for key in structures[0]["coordination"]},
        }
        curves[temperature] = temperature_curves

    aggregate_diffusion = np.asarray([all_results[str(t)]["D_mean_cm2_s"] for t in TEMPERATURES])
    arrhenius = fit_arrhenius(TEMPERATURES, aggregate_diffusion)
    payload = {"method": {"replica_policy": "All completed repeats are included; no replica is selected or omitted.",
                           "replicas_per_temperature": list(REPLICAS), "primary_fit_window_ps": list(PRIMARY_WINDOW),
                           "sensitivity_windows_ps": [list(w) for w in WINDOWS], "trajectory_length_ps": 300,
                           "arrhenius_input": "Arithmetic mean of the three per-temperature D values; uncertainty is shown separately."},
               "temperatures": all_results, "arrhenius_on_mean_D": arrhenius,
               "source_hashes_excluding_large_dumps": hashes}
    (OUT / "analysis.json").write_text(json.dumps(payload, indent=2) + "\n")
    with (OUT / "transport_summary.csv").open("w", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["T_K", "D_mean_cm2_s", "D_sample_sd_cm2_s", "sigma_NE_mean_mS_cm", "sigma_NE_sample_sd_mS_cm"])
        for t in TEMPERATURES:
            r = all_results[str(t)]
            writer.writerow([t, r["D_mean_cm2_s"], r["D_sample_sd_cm2_s"], r["sigma_NE_mean_mS_cm"], r["sigma_NE_sample_sd_mS_cm"]])

    fig, axes = plt.subplots(2, 2, figsize=(10, 8), layout="constrained")
    for ax, t, color in zip(axes.flat, TEMPERATURES, COLORS):
        for replica, lag, msd in curves[t]:
            ax.plot(lag, msd["Li"], color=color, alpha=0.38, lw=1.25)
        ax.plot([], [], color=color, label=f"NEP89, all repeats ({len(REPLICAS)})")
        ax.set(title=f"{t} K", xlabel="Lag time (ps)", ylabel="Li MSD (Å²)", xlim=(0, 300), ylim=(0, None))
        ax.legend(loc="upper left")
    fig.suptitle("LiPON — lithium-ion mean-squared displacement")
    save_figure(fig, "23_LiPON_lithium_MSD")

    fig, ax = plt.subplots(figsize=(8.8, 5.8), layout="constrained")
    ax.errorbar(1000 / np.asarray(TEMPERATURES), aggregate_diffusion,
                yerr=[all_results[str(t)]["D_sample_sd_cm2_s"] for t in TEMPERATURES],
                fmt="o-", capsize=4, color="#31688e", label="NEP89 (mean ± sample SD)")
    ref_t, ref_d = np.asarray([600, 1500]), np.asarray([1.25e-10, 7.5e-9])
    ax.semilogy(1000 / ref_t, ref_d, "s--", color="#777777", label="NequIP (Seth et al.)")
    ax.set(yscale="log", xlabel="1000 / T (K⁻¹)", ylabel="D (cm²/s)", title="Lithium-ion diffusion")
    ax.legend()
    save_figure(fig, "24_LiPON_diffusion_comparison")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.4), layout="constrained")
    axes[0].errorbar(TEMPERATURES, aggregate_diffusion,
                     yerr=[all_results[str(t)]["D_sample_sd_cm2_s"] for t in TEMPERATURES],
                     fmt="o-", capsize=4, color="#31688e", label="NEP89 (all repeats)")
    axes[0].scatter([600, 1500], [1.25e-10, 7.5e-9], marker="s", color="#777777",
                    label="Seth et al. (material-specific NequIP)")
    axes[0].set(yscale="log", xlabel="Temperature (K)", ylabel="D (cm²/s)",
                title="Tracer diffusion")
    axes[0].legend(frameon=False)

    mean_sigma = np.asarray([all_results[str(t)]["sigma_NE_mean_mS_cm"] for t in TEMPERATURES])
    sigma_sd = np.asarray([all_results[str(t)]["sigma_NE_sample_sd_mS_cm"] for t in TEMPERATURES])
    axes[1].errorbar(TEMPERATURES, mean_sigma, yerr=sigma_sd, fmt="o-", capsize=4,
                     color="#31688e", label="NEP89 (conditional $\\sigma_{NE}$)")
    d300 = arrhenius["D_300K_extrapolated_cm2_s"]
    volume_600_mean = np.mean([r["volume_A3"] for r in all_results["600"]["replicas"]])
    sigma300 = sigma_ne_mscm(d300, 47, volume_600_mean, 300)
    axes[1].scatter([300], [sigma300], marker="o", facecolors="none", edgecolors="#31688e",
                    linewidths=2, label="NEP89 (300 K D extrapolation; 600 K density)")
    axes[1].scatter([300], [0.0033], marker="D", color="#111111", label="Bates et al. experiment")
    axes[1].set(yscale="log", xlabel="Temperature (K)", ylabel="Conductivity (mS/cm)",
                title="Conditional conductivity and experiment")
    axes[1].legend(frameon=False, fontsize=9.5)
    fig.suptitle("LiPON — transport comparison")
    save_figure(fig, "24_LiPON_transport_comparison")

    fig, axes = plt.subplots(2, 2, figsize=(11, 8), layout="constrained")
    pair_keys = ("P-O", "P-N", "Li-O", "Li-N")
    for ax, pair in zip(axes.flat, pair_keys):
        for t, color in zip(TEMPERATURES, COLORS):
            item = all_results[str(t)]
            ax.plot(item["RDF_late_r_A"], item["RDF_late_mean"][pair], color=color, label=f"{t} K")
        ax.set(title=f"{pair} radial distribution", xlabel="r (Å)", ylabel="g(r)", xlim=(0.8, 4.5))
        ax.legend(frameon=False)
    fig.suptitle("LiPON — temperature-dependent partial RDF (all repeats)")
    save_figure(fig, "25_LiPON_temperature_RDF")
    refresh_figure_manifest(("23_LiPON_lithium_MSD", "24_LiPON_diffusion_comparison",
                             "24_LiPON_transport_comparison", "25_LiPON_temperature_RDF"))
    print(json.dumps({"D_mean_cm2_s": dict(zip(TEMPERATURES, aggregate_diffusion.tolist())), "arrhenius_on_mean_D": arrhenius}, indent=2))


if __name__ == "__main__":
    run()
