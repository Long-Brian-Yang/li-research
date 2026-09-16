import importlib.util
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "structures" / "plot_lips_r1_report.py"
REFERENCE_STEM = "06_Li3PS4_diffusion_framework_MSD"


def load_module():
    spec = importlib.util.spec_from_file_location("plot_lips_r1_report", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_reference_figure_uses_side_by_side_report_layout():
    module = load_module()
    temperatures = np.array([300.0, 500.0, 700.0, 900.0])
    model_d = np.array([5.4e-8, 4.2e-7, 7.9e-6, 3.1e-5])
    reference_d = np.array([1.2e-9, 9.4e-8, 1.5e-6, 9.1e-6])
    framework = np.array([[0.09, 0.15], [0.20, 0.35], [1.0, 2.2], [5.1, 12.2]])

    fig = module.build_reference_figure(temperatures, model_d, reference_d, framework)

    assert len(fig.axes) == 2
    width, height = fig.get_size_inches()
    assert np.allclose([width, height], [12.0, 4.65])
    fig.canvas.draw()
    left_position = fig.axes[0].get_position()
    right_position = fig.axes[1].get_position()
    assert left_position.x1 < right_position.x0
    assert np.isclose(left_position.height, right_position.height, rtol=0.03)
    assert fig.axes[0].get_title() == "Li-ion self-diffusion"
    assert fig.axes[1].get_title() == "Host-framework displacement at 80 ps"
    assert all("comparison" not in axis.get_title().lower() for axis in fig.axes)
    diffusion_lines = {line.get_label(): line for line in fig.axes[0].lines}
    assert np.array_equal(
        diffusion_lines["NEP89"].get_xdata(), [300.0, 500.0, 700.0, 900.0]
    )
    assert all("subdiffusive" not in label.lower() for label in diffusion_lines)
    plt.close(fig)


def test_reference_figure_has_cache_safe_report_name():
    script = SCRIPT.read_text()
    assert f'finish(fig, "{REFERENCE_STEM}")' in script
    for language in ("ja", "en"):
        review = (ROOT / f"docs/materials/materials_overview_{language}.md").read_text()
        assert f"figures/{REFERENCE_STEM}.png" in review


def test_angle_density_is_normalized_with_current_numpy_api():
    module = load_module()
    angles = np.array([[60.0, 1.0], [90.0, 2.0], [120.0, 1.0]])

    density = module.normalize_angle_density(angles)

    assert np.isclose(np.trapezoid(density, angles[:, 0]), 1.0)


def test_structure_figure_uses_non_overlapping_legends_inside_axes():
    module = load_module()
    rdf = np.array([[0.0, 0.0], [2.5, 5.5], [5.0, 1.0]])
    reference_rdf = np.array([[0.0, 0.0], [2.5, 5.8], [5.0, 1.0]])
    angles = np.array([[60.0, 0.0], [110.0, 0.08], [160.0, 0.0]])
    reference_angles = np.array([[60.0, 0.0], [110.0, 0.09], [160.0, 0.0]])

    fig = module.build_structure_figure(rdf, reference_rdf, angles, reference_angles)
    module.style_figure(fig)

    assert len(fig.axes) == 2
    assert all(axis.get_legend() is not None for axis in fig.axes)
    assert all(axis.get_legend()._loc == 2 for axis in fig.axes)
    assert len(fig.legends) == 0
    for axis in fig.axes:
        labels = [text.get_text() for text in axis.get_legend().get_texts()]
        assert "Chen et al., DeePMD" in labels
        assert all("2025" not in label for label in labels)
    plt.close(fig)


def test_structure_figure_has_cache_safe_report_name():
    script = SCRIPT.read_text()
    assert 'finish(fig, "07_Li3PS4_local_structure")' in script
    for language in ("ja", "en"):
        review = (ROOT / f"docs/materials/materials_overview_{language}.md").read_text()
        assert "figures/07_Li3PS4_local_structure.png" in review
