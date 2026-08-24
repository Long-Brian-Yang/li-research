#!/usr/bin/env python3
"""Convert the final LAMMPS relaxation dump to a deterministic GPUMD extxyz."""
from __future__ import annotations

import argparse
from pathlib import Path


def convert(source: Path, target: Path) -> None:
    lines = source.read_text().splitlines()
    i = 0
    while i < len(lines) and not lines[i].startswith("ITEM: TIMESTEP"):
        i += 1
    if i >= len(lines):
        raise ValueError("No LAMMPS dump frame found")
    n = int(lines[i + 3])
    box = lines[i + 5 : i + 8]
    xy = float(box[0].split()[2]) if len(box[0].split()) == 3 else 0.0
    xz = float(box[1].split()[2]) if len(box[1].split()) == 3 else 0.0
    yz = float(box[2].split()[2]) if len(box[2].split()) == 3 else 0.0
    xlo, xhi = map(float, box[0].split()[:2])
    ylo, yhi = map(float, box[1].split()[:2])
    zlo, zhi = map(float, box[2].split()[:2])
    lx, ly, lz = xhi - xlo, yhi - ylo, zhi - zlo
    lattice = f'{lx} {xy} {xz} 0.0 {ly} {yz} 0.0 0.0 {lz}'
    atom_start = i + 9
    rows = []
    symbols = {1: "Li", 2: "Y", 3: "Cl"}
    for row in lines[atom_start : atom_start + n]:
        fields = row.split()
        atom_id, typ = int(fields[0]), int(fields[1])
        rows.append((atom_id, symbols[typ], *(float(v) for v in fields[2:5])))
    rows.sort(key=lambda r: r[0])
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w") as out:
        out.write(f"{n}\n")
        out.write(f'Lattice="{lattice}" Properties=species:S:1:pos:R:3:id:I:1:type:I:1 pbc="T T T"\n')
        for atom_id, symbol, x, y, z in rows:
            out.write(f"{symbol} {x:.10f} {y:.10f} {z:.10f} {atom_id} {symbols_to_type(symbol)}\n")


def symbols_to_type(symbol: str) -> int:
    return {"Li": 1, "Y": 2, "Cl": 3}[symbol]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    args = parser.parse_args()
    convert(args.source, args.target)
