import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = {
    "English": ROOT / "docs/materials/materials_overview_en.md",
    "Japanese": ROOT / "docs/materials/materials_overview_ja.md",
}


class CompanyReportToneTests(unittest.TestCase):
    def test_reports_identify_company_facing_scope(self):
        self.assertIn("company-facing technical assessment", REPORTS["English"].read_text())
        self.assertIn("企業向け技術報告", REPORTS["Japanese"].read_text())

    def test_reports_open_with_decision_ready_summary(self):
        english = REPORTS["English"].read_text()
        japanese = REPORTS["Japanese"].read_text()
        self.assertLess(english.index("## Executive summary"), english.index("## Contents"))
        self.assertLess(japanese.index("## エグゼクティブサマリー"), japanese.index("## 目次"))
        self.assertIn("17.2×", english)
        self.assertIn("31.1倍", japanese)

    def test_personal_planning_language_is_absent(self):
        forbidden = {
            "English": (
                "standalone work package",
                "focused status and research plan",
                "We ask",
                "Our comparison",
                "Our composition",
            ),
            "Japanese": (
                "独立した研究計画",
                "独立研究として継続可能",
                "個人的な実施予定",
            ),
        }
        for language, path in REPORTS.items():
            text = path.read_text()
            for phrase in forbidden[language]:
                with self.subTest(language=language, phrase=phrase):
                    self.assertNotIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
