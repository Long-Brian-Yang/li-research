from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/structures/analyze_lszc_matched_repeats.py"
FIGURE_STEM = "18_LSZC_transport_comparison"


def test_lszc_primary_figure_uses_cache_safe_four_temperature_name():
    script = SCRIPT.read_text()
    assert "TEMPS = (320, 330, 340, 350)" in script
    assert "REPEATS = (1, 2)" in script
    assert "for repeat in REPEATS" in script
    assert "selected_replica" not in script
    assert "target_informed" not in script
    assert "log_abs_error" not in script
    assert f'{FIGURE_STEM}.{{ext}}' in script


def test_lszc_endpoints_include_both_repeats_without_primary_series_map():
    script = (ROOT / "scripts/structures/analyze_lszc_endpoints.py").read_text()
    assert "PRIMARY_SERIES" not in script
    assert "REPEATS=(1,2)" in script
    assert "for repeat in REPEATS" in script
    assert "for T in TEMPERATURES:" in script


def test_material_reviews_embed_the_four_temperature_figure():
    for language in ("ja", "en"):
        review = (ROOT / f"docs/materials/materials_overview_{language}.md").read_text()
        assert f"figures/{FIGURE_STEM}.png" in review
        assert "figures/18_LSZC_transport.png" not in review


def test_four_temperature_figure_exports_exist():
    for suffix in ("png", "pdf", "svg"):
        assert (ROOT / f"docs/materials/figures/{FIGURE_STEM}.{suffix}").is_file()
