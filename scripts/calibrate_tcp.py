#!/usr/bin/env python3
"""Estimate/check an EEF-to-semantic-TCP transform from offline samples."""

import argparse
import json

import numpy as np

from _common import add_mode_arguments


def main():
    parser = argparse.ArgumentParser()
    add_mode_arguments(parser)
    parser.add_argument("--samples", help="JSON containing repeated T_eef_tcp 4x4 samples")
    args = parser.parse_args()
    if not args.samples:
        print("DRY RUN: collect pivot/caliper samples; semantic TCP is the physical interaction point.")
        return 0
    samples = np.asarray(json.load(open(args.samples, encoding="utf-8")), float)
    if samples.ndim != 3 or samples.shape[1:] != (4, 4):
        raise SystemExit("samples must have shape (n,4,4)")
    translations = samples[:, :3, 3]
    result = {"translation_m": np.mean(translations, axis=0).tolist(), "translation_std_m": np.std(translations, axis=0).tolist(), "rotation_note": "rotation averaging intentionally requires robot-specific calibration review"}
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__": raise SystemExit(main())
