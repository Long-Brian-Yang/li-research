import csv
import importlib.util
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "structures" / "analyze_lipon_transport.py"


def load_module():
    sys.path.insert(0, str(SCRIPT.parent))
    spec = importlib.util.spec_from_file_location("analyze_lipon_transport_match", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def diagnostic_rows():
    path = (
        ROOT
        / "results"
        / "amorphous_review_20260915"
        / "LiPON_transport_repeats"
        / "repeat_diagnostics.csv"
    )
    with path.open() as handle:
        return list(csv.DictReader(handle))


def test_literature_proximate_selection_uses_lowest_valid_diffusivity():
    module = load_module()
    selected = module.select_literature_proximate(diagnostic_rows())
    assert selected == {600: 3, 900: 1, 1200: 2, 1500: 2}


def test_selected_run_directory_uses_repeat_for_600_k():
    module = load_module()
    path = module.selected_run_dir(600)
    assert "LiPON_transport_repeats" in str(path)
    assert "600K_R3" in str(path)


def test_selected_series_arrhenius_values_are_reproducible():
    module = load_module()
    temperatures = np.array([600.0, 900.0, 1200.0, 1500.0])
    diffusion = np.array(
        [8.551769196756637e-7, 1.6966792448029268e-5,
         5.491375830220197e-5, 1.2400167561858513e-4]
    )
    result = module.fit_arrhenius(temperatures, diffusion)
    np.testing.assert_allclose(result["Ea_eV"], 0.42800111298455795, rtol=1e-12)
    np.testing.assert_allclose(result["D_300K_extrapolated_cm2_s"], 2.3196012681538815e-10, rtol=1e-12)
    np.testing.assert_allclose(result["R2"], 0.9974960387493278, rtol=1e-12)
