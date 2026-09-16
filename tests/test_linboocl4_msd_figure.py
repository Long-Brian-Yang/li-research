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
    assert tuple(module.SOURCES) == ("MACE-MPA-0", "SevenNet-nano", "M3GNet")
    assert module.TEMPERATURES == (600, 800, 1000, 1200)
    assert all(len(paths) == len(module.TEMPERATURES) for paths in module.SOURCES.values())
