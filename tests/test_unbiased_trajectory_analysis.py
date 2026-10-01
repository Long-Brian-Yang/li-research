from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def test_lzoc_posthoc_selectors_are_not_shipped_as_analysis_tools():
    assert not (ROOT / "scripts/structures/select_lzoc_representatives.py").exists()
    assert not (ROOT / "scripts/structures/preview_lzoc_closest.py").exists()


def test_cross_material_plots_do_not_consume_target_selected_series():
    for name in (
        "plot_amorphous_arrhenius_comparisons.py",
        "curate_overview_figures.py",
        "plot_literature_correspondence.py",
    ):
        path = ROOT / "scripts/structures" / name
        source = path.read_text()
        assert "target_informed_summary" not in source
        assert "lzoc_report_selection" not in source
        assert "representatives.json" not in source


def test_crystal_msd_plot_never_rescales_one_model_to_reference_endpoints():
    path = ROOT / "src/li_research/analysis/lammps/plot_li3ycl6_msd_three_models.py"
    source = path.read_text()
    assert "mace_reference_endpoints" not in source
    assert "target / msd[-1]" not in source
    assert "plot_selected_msd_three_models.py" not in source


def test_evidence_package_includes_every_available_transport_repeat():
    sys.path.insert(0, str(ROOT / "scripts/structures"))
    from build_material_evidence_package import trajectory_specs

    specs = trajectory_specs()
    ids = {item["id"] for item in specs}
    for temperature in (320, 330, 340, 350):
        for replica in ("R1", "R2"):
            assert f"LSZC_{temperature}K_{replica}" in ids
    for temperature in (600, 900, 1200, 1500):
        for replica in ("R1", "R2", "R3"):
            assert f"LiPON_{temperature}K_{replica}" in ids
    for temperature in (340, 360):
        for replica in ("R1", "R2"):
            assert f"LZOC_{temperature}K_{replica}" in ids
    assert all("representative" not in item["stem"] for item in specs)
