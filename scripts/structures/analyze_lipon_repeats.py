"""Compare completed LiPON NEP89 preparations without transport fitting.

The analysis uses the matched final 20 ps, 250 K, 1 bar release stages of the
original preparation and two independent thermal histories.  It reports
thermodynamics, short contacts, time-averaged partial RDFs, nitrogen site
environments and phosphate coordination motifs.  Distances are geometric
screening definitions, not bond-order assignments.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ase.io import read

from finish_amorphous_analysis import frame_metrics
from li_diffusion_style import apply_style

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/amorphous_review_20260915"
OUT = BASE / "LiPON_repeats_analysis"
FIG = ROOT / "docs/materials/figures"
SOURCES = {
    "Preparation A": BASE / "source/LiPON",
    "Preparation B": BASE / "source/LiPON_repeats/prep_repeat_R1_8678859/release",
    "Preparation C": BASE / "source/LiPON_repeats/prep_repeat_R2_8678859/release",
}
COLORS = {"Preparation A": "#727272", "Preparation B": "#31688e", "Preparation C": "#d73027"}
PAIRS = [("P", "O", 2.1), ("P", "N", 2.1), ("Li", "O", 2.8), ("Li", "N", 2.8)]
EDGES = np.arange(0.0, 4.5001, 0.05)


def save(fig, name):
    apply_style(fig)
    FIG.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf", "svg"):
        p = FIG / f"{name}.{ext}"
        fig.savefig(p, dpi=300, bbox_inches="tight")
        if ext == "svg":
            p.write_text("\n".join(x.rstrip() for x in p.read_text().splitlines()) + "\n")
    plt.close(fig)


def distances(frame):
    symbols = np.asarray(frame.get_chemical_symbols())
    d = frame.get_all_distances(mic=True)
    np.fill_diagonal(d, np.inf)
    return symbols, d


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    records = {}
    rdf = {}
    traces = {}
    n_site = {}
    p_motif = {}

    for label, source in SOURCES.items():
        frames = read(source / "dump.xyz", index=":")
        thermo = np.loadtxt(source / "thermo.out")
        assert len(frames) == 200 and thermo.shape == (400, 18)
        assert np.isfinite(thermo).all() and all(len(x) == 124 for x in frames)
        late = frames[100:]
        mass = frames[0].get_masses().sum()
        volume = np.linalg.det(thermo[:, 9:].reshape(-1, 3, 3))
        density = mass * 1.6605390666 / volume
        pe = thermo[:, 2] / 124
        pressure = thermo[:, 3:6].mean(axis=1)
        time = np.arange(1, 401) * 0.05

        nn = []
        n_counts = []
        motifs = []
        gs = []
        for frame in late:
            symbols, d = distances(frame)
            n_idx = np.flatnonzero(symbols == "N")
            p_idx = np.flatnonzero(symbols == "P")
            o_idx = np.flatnonzero(symbols == "O")
            nn.append(float(d[np.ix_(n_idx, n_idx)].min()))
            n_counts.extend((d[np.ix_(n_idx, p_idx)] < 2.1).sum(axis=1).tolist())
            po = (d[np.ix_(p_idx, o_idx)] < 2.1).sum(axis=1)
            pn = (d[np.ix_(p_idx, n_idx)] < 2.1).sum(axis=1)
            motifs.extend(zip(po.tolist(), pn.tolist()))
            g, _, _ = frame_metrics(frame, PAIRS, EDGES)
            gs.append(g)

        n_counts = np.asarray(n_counts, int)
        motif_keys = [(4, 0), (3, 1), (3, 0), (2, 1), (2, 2)]
        motif_prob = {f"P-O{o}_N{n}": float(np.mean([x == (o, n) for x in motifs])) for o, n in motif_keys}
        motif_prob["Other"] = 1.0 - sum(motif_prob.values())
        site_prob = {str(k): float(np.mean(n_counts == k)) for k in range(4)}

        all_nn = []
        for frame in frames:
            symbols, d = distances(frame)
            n_idx = np.flatnonzero(symbols == "N")
            all_nn.append(float(d[np.ix_(n_idx, n_idx)].min()))
        traces[label] = {"time_ps": time, "pe": pe, "density": density,
                         "frame_time_ps": np.arange(1, 201) * 0.1,
                         "minimum_NN_A": np.asarray(all_nn)}
        rdf[label] = np.mean(gs, axis=0)
        n_site[label] = site_prob
        p_motif[label] = motif_prob
        records[label] = {
            "mean_temperature_K": float(thermo[:, 0].mean()),
            "mean_pressure_GPa": float(pressure.mean()),
            "density_g_cm3": float(density.mean()),
            "density_last5_minus_first5_percent": float((density[-100:].mean() / density[:100].mean() - 1) * 100),
            "PE_last5_minus_first5_meV_atom": float((pe[-100:].mean() - pe[:100].mean()) * 1000),
            "late_NN_min_A": float(min(nn)),
            "late_NN_maximum_of_frame_minima_A": float(max(nn)),
            "fraction_late_frames_NN_below_1p6A": float(np.mean(np.asarray(nn) < 1.6)),
            "N_P_neighbour_fraction": site_prob,
            "P_coordination_motif_fraction": motif_prob,
        }

    # Source tables
    labels = list(SOURCES)
    with (OUT / "summary.csv").open("w") as f:
        f.write("preparation,T_K,P_GPa,rho_g_cm3,rho_change_percent,PE_change_meV_atom,NN_min_A,NN_contact_fraction\n")
        for label in labels:
            r = records[label]
            f.write(f"{label},{r['mean_temperature_K']:.6f},{r['mean_pressure_GPa']:.8f},{r['density_g_cm3']:.8f},{r['density_last5_minus_first5_percent']:.8f},{r['PE_last5_minus_first5_meV_atom']:.8f},{r['late_NN_min_A']:.8f},{r['fraction_late_frames_NN_below_1p6A']:.8f}\n")
    rcentres = (EDGES[:-1] + EDGES[1:]) / 2
    for label in labels:
        np.savetxt(OUT / f"{label}_RDF.csv", np.column_stack([rcentres, *rdf[label]]), delimiter=",", header="r_A,P_O,P_N,Li_O,Li_N", comments="")
    (OUT / "analysis.json").write_text(json.dumps(records, indent=2) + "\n")

    # Figure 1: matched preparation stability and chemically relevant motifs.
    fig, ax = plt.subplots(2, 2, layout="constrained")
    for label in labels:
        x = traces[label]
        ax[0, 0].plot(x["time_ps"], x["density"], color=COLORS[label], label=label)
        ax[0, 1].plot(x["frame_time_ps"], x["minimum_NN_A"], color=COLORS[label], label=label)
    ax[0, 0].set(title="250 K release: density", xlabel="Time (ps)", ylabel="Density (g cm⁻³)")
    ax[0, 1].axhline(1.6, color="#999999", linestyle=":", label="Screening threshold")
    ax[0, 1].set(title="250 K release: closest N–N distance", xlabel="Time (ps)", ylabel="Minimum N–N distance (Å)")
    site_names = ["0 P", "1 P (apical)", "2 P (bridging)", "3 P"]
    xpos = np.arange(4); width = 0.24
    for i, label in enumerate(labels):
        ax[1, 0].bar(xpos + (i - 1) * width, [n_site[label][str(k)] for k in range(4)], width, color=COLORS[label], label=label)
    ax[1, 0].set(title="Nitrogen environments", xlabel="P neighbours within 2.1 Å", ylabel="N atom–frame fraction", xticks=xpos, xticklabels=site_names)
    motif_names = ["PO₄", "PO₃N", "PO₃", "PO₂N", "PO₂N₂", "Other"]
    motif_keys = ["P-O4_N0", "P-O3_N1", "P-O3_N0", "P-O2_N1", "P-O2_N2", "Other"]
    xpos = np.arange(len(motif_names))
    for i, label in enumerate(labels):
        ax[1, 1].bar(xpos + (i - 1) * width, [p_motif[label][k] for k in motif_keys], width, color=COLORS[label], label=label)
    ax[1, 1].set(title="Phosphorus coordination units", xlabel="Geometric P environment (<2.1 Å)", ylabel="P atom–frame fraction", xticks=xpos, xticklabels=motif_names)
    for a in ax.ravel():
        a.legend(frameon=False)
    save(fig, "21_LiPON_preparation_structure")

    # Figure 2: partial RDFs from the matched final 10 ps.
    fig, ax = plt.subplots(2, 2, layout="constrained")
    for j, (u, v, _) in enumerate(PAIRS):
        a = ax.ravel()[j]
        for label in labels:
            a.plot(rcentres, rdf[label][j], color=COLORS[label], label=label)
        a.set(title=f"{u}–{v}", xlabel="r (Å)", ylabel="g(r)", xlim=(1.0, 4.5))
        a.legend(frameon=False)
    save(fig, "22_LiPON_partial_RDF")
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    run()
