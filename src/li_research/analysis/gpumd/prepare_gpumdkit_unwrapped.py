#!/usr/bin/env python3
"""Prepare unwrapped extxyz input for the official GPUMDkit MSD calculator.

The source GPUMD dump is wrapped and triclinic.  This conversion uses
fractional-coordinate minimum-image increments, then writes the resulting
unwrapped Cartesian coordinates without a cell so GPUMDkit does not apply a
second heuristic unwrap.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np


def lattice(comment: str) -> np.ndarray:
    token = comment.split('Lattice="', 1)[1].split('"', 1)[0]
    return np.fromstring(token, sep=" ").reshape(3, 3)


def convert(source: Path, target: Path):
    target.parent.mkdir(parents=True, exist_ok=True)
    previous_frac = None
    unwrapped_frac = None
    with source.open() as src, target.open("w") as dst:
        frame = 0
        while True:
            line = src.readline()
            if not line:
                break
            n = int(line.strip())
            comment = src.readline().strip()
            symbols = []
            positions = np.empty((n, 3), float)
            for i in range(n):
                fields = src.readline().split()
                symbols.append(fields[0])
                positions[i] = [float(v) for v in fields[1:4]]
            cell = lattice(comment)
            frac = positions @ np.linalg.inv(cell)
            if frame == 0:
                unwrapped_frac = frac.copy()
            else:
                delta = frac - previous_frac
                delta -= np.rint(delta)
                unwrapped_frac = unwrapped_frac + delta
            previous_frac = frac
            unwrapped = unwrapped_frac @ cell
            dst.write(f"{n}\n")
            dst.write("Properties=species:S:1:pos:R:3 pbc=\"F F F\"\n")
            for symbol, xyz in zip(symbols, unwrapped):
                dst.write(f"{symbol} {xyz[0]:.10f} {xyz[1]:.10f} {xyz[2]:.10f}\n")
            frame += 1
    print(f"wrote {frame} frames: {target}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: prepare_gpumdkit_unwrapped.py INPUT.dump.xyz OUTPUT.xyz")
    convert(Path(sys.argv[1]), Path(sys.argv[2]))
