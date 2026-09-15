# LZOC / LSZC analysis package — 2026-09-15

- [日本語：図・結果表・説明](report_ja.md)
- [English: figures, tables and interpretation](report_en.md)
- [Numerical summary and input SHA256](summary.json)
- [Reproducible analysis script](../../../scripts/structures/finish_amorphous_analysis.py)

10 figure families, each in PNG/PDF/SVG. CSV files contain the plotted numerical data except framework MSD curves, which are reproducible from the script and retained trajectories. Raw input data are unchanged. No formal Ea or 300 K extrapolation is claimed.

QA: all 10 PNG figures visually inspected for legibility and clipping. Periodic coordination, block fitting, FFT/direct MSD agreement, unwrapping and unit-conversion tests checked. The 200 ps framework-MSD tail has few time origins and is not used to infer transport. Pressure/energy panels use individual y-axis ranges.
