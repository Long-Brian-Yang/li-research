import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DATA = (
    ROOT
    / "results/amorphous_review_20260915/literature_correspondence"
    / "LSZC_Zr_mean_coordination.csv"
)
SVG = ROOT / "docs/materials/figures/27_LSZC_PDF_and_Zr_coordination.svg"


class LszcCoordinationFigureTests(unittest.TestCase):
    def test_main_figure_compares_mean_coordination_across_four_temperatures(self):
        self.assertTrue(SOURCE_DATA.exists(), "mean-coordination source table is missing")
        with SOURCE_DATA.open() as handle:
            rows = list(csv.DictReader(handle))

        self.assertEqual({320, 330, 340, 350}, {int(row["T_K"]) for row in rows})
        self.assertEqual({"Zr-O", "Zr-Cl"}, {row["pair"] for row in rows})
        self.assertEqual(8, len(rows))

        svg = SVG.read_text()
        self.assertIn("Mean Zr-O coordination", svg)
        self.assertIn("Mean Zr-Cl coordination", svg)
        self.assertIn("Temperature (K)", svg)
        self.assertNotIn("Probability", svg)


if __name__ == "__main__":
    unittest.main()
