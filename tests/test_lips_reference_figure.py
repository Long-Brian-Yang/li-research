import importlib.util
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "structures" / "plot_lips_r1_report.py"


def load_module():
    spec = importlib.util.spec_from_file_location("plot_lips_r1_report", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_reference_figure_uses_markdown_readable_vertical_layout():
    module = load_module()
    temperatures = np.array([300.0, 500.0, 700.0, 900.0])
    model_d = np.array([5.4e-8, 4.2e-7, 7.9e-6, 3.1e-5])
    reference_d = np.array([1.2e-9, 9.4e-8, 1.5e-6, 9.1e-6])
    framework = np.array([[0.09, 0.15], [0.20, 0.35], [1.0, 2.2], [5.1, 12.2]])

    fig = module.build_reference_figure(temperatures, model_d, reference_d, framework)

    assert len(fig.axes) == 2
    width, height = fig.get_size_inches()
    assert height > width
    assert fig.axes[0].get_title() == "Li-ion self-diffusion"
    assert fig.axes[1].get_title() == "Host-framework displacement at 80 ps"
    assert all("comparison" not in axis.get_title().lower() for axis in fig.axes)
    diffusion_lines = {line.get_label(): line for line in fig.axes[0].lines}
    assert np.array_equal(diffusion_lines["NEP89 (this work)"].get_xdata(), [700.0, 900.0])
    assert np.array_equal(
        diffusion_lines["NEP89 (subdiffusive)"].get_xdata(), [300.0, 500.0]
    )
    plt.close(fig)


def test_angle_density_is_normalized_with_current_numpy_api():
    module = load_module()
    angles = np.array([[60.0, 1.0], [90.0, 2.0], [120.0, 1.0]])

    density = module.normalize_angle_density(angles)

    assert np.isclose(np.trapezoid(density, angles[:, 0]), 1.0)
