import importlib.util
from pathlib import Path

import numpy as np


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "structures" / "analyze_lips_r1_remote.py"


def load_module():
    spec = importlib.util.spec_from_file_location("analyze_lips_r1_remote", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_window_msd_matches_direct_time_origin_average():
    module = load_module()
    positions = np.array(
        [
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
            [[1.0, 0.0, 0.0], [1.0, 1.0, 0.0]],
            [[2.0, 0.0, 0.0], [1.0, 2.0, 0.0]],
        ]
    )
    expected = np.array([0.0, 1.0, 4.0])
    np.testing.assert_allclose(module.window_msd(positions), expected)


def test_sp_angle_histogram_recovers_tetrahedral_angle():
    module = load_module()
    cos_theta = -1.0 / 3.0
    sin_theta = np.sqrt(1.0 - cos_theta**2)
    vectors = np.array([[1.0, 0.0, 0.0], [cos_theta, sin_theta, 0.0]])
    angles = module.p_centered_angles(vectors)
    np.testing.assert_allclose(angles, [109.47122063449069], rtol=0, atol=1e-10)


def test_reference_rows_preserve_temperature_and_ratio():
    plot_script = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "structures"
        / "plot_lips_r1_report.py"
    )
    spec = importlib.util.spec_from_file_location("plot_lips_r1_report", plot_script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.reference_rows(
        temperatures=np.array([300.0, 500.0]),
        model_d=np.array([2.0e-9, 3.0e-8]),
        reference_d=np.array([1.0e-9, 1.0e-8]),
    )
    np.testing.assert_allclose(rows[:, 0], [300.0, 500.0])
    np.testing.assert_allclose(rows[:, 3], [2.0, 3.0])


def test_reference_loader_ignores_blank_unused_columns(tmp_path):
    plot_script = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "structures"
        / "plot_lips_r1_report.py"
    )
    spec = importlib.util.spec_from_file_location("plot_lips_r1_report", plot_script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    source = tmp_path / "source.csv"
    source.write_text("x,a,b,unused\n1,2,3,\n4,5,6,\n")
    values = module.load_reference_csv(source, (0, 2))
    np.testing.assert_allclose(values, [[1.0, 3.0], [4.0, 6.0]])
