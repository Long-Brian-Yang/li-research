# Direction 2 development documentation

This directory is the single documentation entry point for Direction 2. Each
Markdown file has one role: plans define what to do, protocols define how to do
it, benchmarks record comparable speed tests, and results document scientific
interpretation.

## 1. Plans — research decisions and next steps

- [English calculation plan](plans/direction2_plan_en.md)
- [日本語計算計画](plans/direction2_plan_ja.md)
- [Model alternatives and selection criteria](plans/model_alternatives_direction2.md)

## 2. Protocols — reproducible calculation rules

- [TSUBAME project layout and naming standard](protocols/project_layout.md)

## 3. Benchmarks — standardized model/interface comparison

- [Detailed benchmark comparison and ranking](benchmarks/benchmark_comparison.md)

## 4. Results — scientific interpretation

- [Li₃YCl₆ MACE 500 ps composite diffusion/Arrhenius analysis](results/mace_li3ycl6_arrhenius_500ps.md)

## Update rule

When a calculation condition changes, update the relevant plan and protocol.
When a benchmark is rerun, add the raw run location before changing the
comparison table. Superseded files should be removed if they carry no unique
scientific result; raw run artifacts remain only in their TSUBAME result
directory.
