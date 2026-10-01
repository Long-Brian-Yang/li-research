from pathlib import Path
import importlib.util


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src/li_research/analysis/lammps/plot_linboocl4_msd_three_models.py"


def load_module():
    spec = importlib.util.spec_from_file_location("plot_linboocl4_msd", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_linboocl4_triptych_matches_li3ycl6_canvas_proportions():
    module = load_module()
    assert module.FIGSIZE == (18.0, 6.2)
    assert module.DPI == 300
    assert module.OUTPUT_PNGS == (
        ROOT / "results/publication_all_materials/main/LiNbOCl4_MSD_4T_all_models.png",
        ROOT / "docs/materials/figures/02_LiNbOCl4_three_model_MSD.png",
    )


def test_linboocl4_triptych_has_three_models_and_four_temperatures():
    module = load_module()
    assert tuple(module.SOURCES) == ("MACE-MPA-0", "SevenNet-nano", "M3GNet GPU")
    assert module.TEMPERATURES == (600, 800, 1000, 1200)
    assert all(isinstance(directory, str) for directory in module.SOURCES.values())


def test_linboocl4_discovers_all_completed_replica_msd_files():
    module = load_module()
    for directory in module.SOURCES.values():
        for temperature in module.TEMPERATURES:
            paths = module.discover_tracks(directory, temperature)
            assert len(paths) >= 3
            assert paths == sorted(paths)
            assert all(path.is_file() and path.name == "msd_li.dat" for path in paths)


def test_linboocl4_figure_plots_every_discovered_track():
    module = load_module()
    fig = module.build_figure()
    try:
        for ax, directory in zip(fig.axes, module.SOURCES.values()):
            expected = sum(len(module.discover_tracks(directory, t)) for t in module.TEMPERATURES)
            assert len(ax.lines) == expected + len(module.TEMPERATURES)
    finally:
        import matplotlib.pyplot as plt
        plt.close(fig)


def test_linboocl4_transport_analysis_includes_every_track_and_groups_by_seed():
    import sys
    sys.path.insert(0, str(ROOT / "src"))
    from li_research.analysis.lammps.linboocl4_all_replicas import (
        MODELS, TEMPERATURES, collect_tracks, discover_tracks, summarize_by_seed,
    )

    tracks = collect_tracks()
    expected = sum(len(discover_tracks(directory, temperature))
                   for directory in MODELS.values() for temperature in TEMPERATURES)
    assert len(tracks) == expected == 41
    summary = summarize_by_seed(tracks)
    assert summary[("SevenNet-nano", 600)]["execution_count"] == 5
    assert summary[("SevenNet-nano", 600)]["seed_count"] == 3
    assert summary[("M3GNet GPU", 800)]["execution_count"] == 6
    assert summary[("M3GNet GPU", 800)]["seed_count"] == 6


def test_linboocl4_arrhenius_pipeline_has_no_hardcoded_selected_diffusion_values():
    source = (ROOT / "src/li_research/analysis/arrhenius/plot_linboocl4_arrhenius.py").read_text()
    assert "collect_tracks()" in source
    assert "summarize_by_seed" in source
    assert "2.2414064884e-6" not in source
    assert "selected real-trajectory combination" not in source


def test_linboocl4_arrhenius_legend_uses_correct_1000_over_temperature_scale():
    import sys
    sys.path.insert(0, str(ROOT / "src"))
    from li_research.analysis.arrhenius.plot_linboocl4_arrhenius import (
        build_figure, build_transport_summary,
    )
    import matplotlib.pyplot as plt

    _, summary = build_transport_summary()
    fig, _ = build_figure(summary)
    try:
        labels = [text.get_text() for text in fig.axes[0].get_legend().get_texts()]
        assert "0.310\\,\\mathrm{eV}" in labels[0]
    finally:
        plt.close(fig)
