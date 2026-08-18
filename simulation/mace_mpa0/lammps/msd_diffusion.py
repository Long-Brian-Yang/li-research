#!/usr/bin/env python3
"""Estimate Li self-diffusion from a LAMMPS custom dump.

Expected dump columns are: id type xu yu zu (as written by in.md.*).
The output is a preliminary linear-fit estimate, not a conductivity claim.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np


def read_li_frames(path: Path, li_type: int) -> tuple[np.ndarray, np.ndarray]:
    times: list[float] = []
    frames: list[np.ndarray] = []
    with path.open() as handle:
        while True:
            line = handle.readline()
            if not line:
                break
            if line.strip() != "ITEM: TIMESTEP":
                continue
            timestep = float(handle.readline().strip())
            if handle.readline().strip() != "ITEM: NUMBER OF ATOMS":
                raise ValueError("Unexpected dump format before atom count")
            natoms = int(handle.readline())
            if not handle.readline().startswith("ITEM: BOX BOUNDS"):
                raise ValueError("Expected BOX BOUNDS in dump")
            for _ in range(3):
                handle.readline()
            columns = handle.readline().strip().split()[2:]
            required = {"id", "type", "xu", "yu", "zu"}
            if not required.issubset(columns):
                raise ValueError(f"Dump must contain {sorted(required)}; got {columns}")
            index = {name: columns.index(name) for name in required}
            positions: list[tuple[int, float, float, float]] = []
            for _ in range(natoms):
                fields = handle.readline().split()
                if int(fields[index["type"]]) == li_type:
                    positions.append((int(fields[index["id"]]), float(fields[index["xu"]]), float(fields[index["yu"]]), float(fields[index["zu"]])))
            positions.sort(key=lambda row: row[0])
            if not positions:
                raise ValueError(f"No atoms with type {li_type} found at timestep {timestep}")
            times.append(timestep)
            frames.append(np.asarray([[row[1], row[2], row[3]] for row in positions]))
    if len(frames) < 3:
        raise ValueError("Need at least three frames for a diffusion estimate")
    return np.asarray(times), np.asarray(frames)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dump", type=Path)
    parser.add_argument("--li-type", type=int, default=1)
    parser.add_argument("--timestep-ps", type=float, default=0.001)
    parser.add_argument("--discard-fraction", type=float, default=0.2)
    parser.add_argument("--output", type=Path, default=Path("msd_diffusion.txt"))
    args = parser.parse_args()
    times, xyz = read_li_frames(args.dump, args.li_type)
    origin = xyz[0]
    msd = np.mean(np.sum((xyz - origin[None, :, :]) ** 2, axis=2), axis=1)
    start = min(max(1, int(len(times) * args.discard_fraction)), len(times) - 2)
    t_ps = (times - times[0]) * args.timestep_ps
    slope, intercept = np.polyfit(t_ps[start:], msd[start:], 1)
    D_a2_per_ps = slope / 6.0
    D_cm2_per_s = D_a2_per_ps * 1e-4
    lines = [
        f"frames = {len(times)}",
        f"Li atoms = {xyz.shape[1]}",
        f"fit start frame = {start}",
        f"MSD slope = {slope:.8g} Angstrom^2/ps",
        f"D_self = {D_a2_per_ps:.8g} Angstrom^2/ps",
        f"D_self = {D_cm2_per_s:.8g} cm^2/s",
        "warning = exploratory self-diffusion estimate; no collective conductivity computed",
    ]
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
