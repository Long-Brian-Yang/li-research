#!/usr/bin/env python3
"""Convert a MACE checkpoint to the ML-IAP format with shape compatibility.

Some MACE-MP-0b3 checkpoints store scalar linear weights as one-dimensional
tensors, while older conversion code unconditionally unsqueezes them.  The
target cuEquivariance model already exposes the required target shape; this
script copies weights only when their shapes agree and handles the legacy
singleton dimension explicitly.
"""

import argparse
import copy
import os

os.environ.setdefault("TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD", "1")

import torch
from mace.calculators.lammps_mliap_mace import LAMMPS_MLIAP_MACE
from mace.cli import convert_e3nn_cueq as conv
from mace.cli.convert_e3nn_cueq import get_transfer_keys, get_kmax_pairs
from mace.tools.scripts_utils import extract_config_mace_model


def transfer_weights_compat(source_model, target_model, max_L, correlation, num_layers):
    source = source_model.state_dict()
    target = target_model.state_dict()

    for key in get_transfer_keys(num_layers):
        if key not in source or key not in target:
            continue
        value = source[key]
        if value.shape != target[key].shape and value.numel() == target[key].numel():
            value = value.reshape(target[key].shape)
        if value.shape != target[key].shape:
            raise RuntimeError(f"incompatible transferred key {key}: {value.shape} vs {target[key].shape}")
        target[key] = value

    for i, kmax in get_kmax_pairs(max_L, correlation, num_layers):
        value = torch.concatenate(
            [source[f"products.{i}.symmetric_contractions.contractions.{k}.weights{j}"]
             for k in range(kmax + 1) for j in ["_max", ".0", ".1"]], dim=1
        )
        target[f"products.{i}.symmetric_contractions.weight"] = value

    for key, value in source.items():
        if key not in target or "symmetric_contraction" in key:
            continue
        if key in get_transfer_keys(num_layers):
            continue
        if value.shape == target[key].shape:
            target[key] = value
        elif value.numel() == target[key].numel():
            target[key] = value.reshape(target[key].shape)

    for i in range(num_layers):
        target_model.interactions[i].avg_num_neighbors = source_model.interactions[i].avg_num_neighbors
    target_model.load_state_dict(target)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_model")
    parser.add_argument("output_model")
    args = parser.parse_args()

    source = torch.load(args.input_model, map_location="cpu")
    dtype = next(source.parameters()).dtype
    torch.set_default_dtype(dtype)
    config = extract_config_mace_model(source)
    config["cueq_config"] = conv.CuEquivarianceConfig(
        enabled=True, layout="ir_mul", group="O3_e3nn", optimize_all=True
    )
    target = source.__class__(**config).to("cpu")
    transfer_weights_compat(
        source, target, config["hidden_irreps"].lmax,
        config["correlation"], config["num_interactions"]
    )
    target.lammps_mliap = True
    wrapped = LAMMPS_MLIAP_MACE(target)
    torch.save(wrapped, args.output_model)
    print(f"wrote {args.output_model} ({os.path.getsize(args.output_model)} bytes)")


if __name__ == "__main__":
    main()
