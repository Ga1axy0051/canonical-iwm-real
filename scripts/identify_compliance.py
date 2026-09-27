#!/usr/bin/env python3
"""Offline-first translational compliance identification."""

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from _common import add_mode_arguments, executing
from canonical_iwm.compliance import fit_compliance


def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    keys = ("fx_N", "fy_N", "fz_N", "dx_m", "dy_m", "dz_m")
    if not rows or any(key not in rows[0] for key in keys):
        raise SystemExit("CSV columns required: " + ",".join(keys))
    data = np.asarray([[float(row[key]) for key in keys] for row in rows])
    return data[:, :3], data[:, 3:]


def main():
    parser = argparse.ArgumentParser(); add_mode_arguments(parser)
    parser.add_argument("--csv", type=Path); parser.add_argument("--output", type=Path, default=Path("compliance_result.json"))
    args = parser.parse_args()
    if executing(args) and not args.csv:
        raise SystemExit("live mode never applies force automatically; collect technician-applied known perturbations and provide --csv")
    if args.csv:
        forces, displacements = read_csv(args.csv)
    else:
        forces = np.vstack([np.eye(3), -np.eye(3)])
        displacements = forces @ np.diag([1e-5, 2e-5, 3e-5])
        print("DRY RUN: using synthetic offline samples")
    result = fit_compliance(forces, displacements).as_dict()
    print(json.dumps(result, indent=2))
    if args.csv:
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"saved {args.output}")
    return 0


if __name__ == "__main__": raise SystemExit(main())
