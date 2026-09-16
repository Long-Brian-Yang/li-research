import importlib.util
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "structures" / "analyze_lszc_endpoints.py"


def load_module():
    sys.path.insert(0, str(SCRIPT.parent))
    spec = importlib.util.spec_from_file_location("analyze_lszc_endpoints", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_local_structure_uses_same_four_temperature_representatives_as_transport():
    module = load_module()

    assert module.TEMPERATURES == (320, 330, 340, 350)
    assert module.PRIMARY_SERIES == {320: 2, 330: 2, 340: 2, 350: 1}


def test_rdf_figure_contains_four_temperature_series_in_every_panel():
    module = load_module()
    radius = np.linspace(1.0, 5.0, 10)
    rdf_by_temperature = {
        temperature: np.column_stack(
            [radius] + [np.full_like(radius, index + temperature / 1000) for index in range(4)]
        )
        for temperature in module.TEMPERATURES
    }

    fig = module.build_rdf_figure(rdf_by_temperature)

    assert len(fig.axes) == 4
    for axis in fig.axes:
        assert len(axis.lines) == 4
        assert [line.get_label() for line in axis.lines] == [
            "320 K",
            "330 K",
            "340 K",
            "350 K",
        ]
    plt.close(fig)


def test_report_references_four_temperature_rdf_asset():
    script = SCRIPT.read_text()
    assert "19_LSZC_four_temperature_RDF" in script
    for language in ("ja", "en"):
        review = (ROOT / f"docs/materials/materials_overview_{language}.md").read_text()
        assert "figures/19_LSZC_four_temperature_RDF.png" in review
