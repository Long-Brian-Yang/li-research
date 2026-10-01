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


def test_lipon_transport_analysis_has_no_replica_selector():
    source = SCRIPT.read_text()
    assert "SELECTED_REPLICA" not in source
    assert "select_literature_proximate" not in source
    assert "selected_run_dir" not in source
    assert "REPLICAS = (1, 2, 3)" in source
    assert "for replica in REPLICAS" in source
    assert '"replicas": results' in source
    assert '"D_mean_cm2_s": float(d_values.mean())' in source


def test_lipon_repeat_diagnostics_do_not_rank_or_select_replicas():
    source = (SCRIPT.parent / "analyze_lipon_repeats.py").read_text()
    assert "quality_score" not in source
    assert "selected_replica" not in source
    assert "min(choices" not in source
    assert "rows = [analyse_one(t, r) for t in TEMPS for r in (1, 2, 3)]" in source


def test_arrhenius_fit_function_is_reproducible_for_explicit_input():
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
