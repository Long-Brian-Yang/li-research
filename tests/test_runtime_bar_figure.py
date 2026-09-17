import sys
import unittest
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts/structures"))


class RuntimeBarFigureTests(unittest.TestCase):
    def test_runtime_panel_is_paired_horizontal_bar_chart(self):
        from curate_overview_figures import plot_runtime_bars

        timing = np.array([
            [600.0, 14830.478, 544.344],
            [700.0, 18019.970, 502.105],
            [800.0, 14485.452, 501.880],
            [900.0, 18975.057, 497.137],
        ])
        fig, ax = plt.subplots()
        plot_runtime_bars(ax, timing)

        self.assertEqual(len(ax.patches), 8)
        self.assertEqual(ax.get_xscale(), "log")
        self.assertEqual(ax.get_xlabel(), "Whole-job runtime (min)")
        self.assertEqual(ax.get_ylabel(), "Temperature (K)")
        self.assertEqual(len(ax.texts), 8)
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        right_edge = ax.get_window_extent(renderer).x1
        for label in ax.texts:
            self.assertLessEqual(label.get_window_extent(renderer).x1, right_edge - 2)
        plt.close(fig)


if __name__ == "__main__":
    unittest.main()
