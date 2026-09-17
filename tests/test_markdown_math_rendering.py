import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = (
    ROOT / "docs/materials/materials_overview_en.md",
    ROOT / "docs/materials/materials_overview_ja.md",
)
INLINE_MATH = re.compile(r"(?<!\\)\$(?!\$)(.+?)(?<!\\)\$")
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")


def lines_outside_display_math(text):
    in_display_math = False
    for line_number, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("$$"):
            in_display_math = not in_display_math
            continue
        if not in_display_math:
            yield line_number, line


class MarkdownMathRenderingTests(unittest.TestCase):
    def test_reports_do_not_use_unsupported_angstrom_command(self):
        for report in REPORTS:
            with self.subTest(report=report.name):
                self.assertNotIn(r"\AA", report.read_text())

    def test_japanese_inline_math_is_separated_from_cjk_text(self):
        report = ROOT / "docs/materials/materials_overview_ja.md"
        failures = []
        for line_number, line in lines_outside_display_math(report.read_text()):
            for match in INLINE_MATH.finditer(line):
                left = line[match.start() - 1] if match.start() else ""
                right = line[match.end()] if match.end() < len(line) else ""
                if CJK.fullmatch(left) or CJK.fullmatch(right):
                    failures.append((line_number, match.group(0), left, right))

        self.assertEqual([], failures)


if __name__ == "__main__":
    unittest.main()
