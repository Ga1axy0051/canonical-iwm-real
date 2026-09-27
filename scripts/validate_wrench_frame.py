#!/usr/bin/env python3
"""Manual, non-contact-producing wrench sign/frame validation."""

import argparse
import numpy as np

from _common import add_mode_arguments, confirm, executing, make_adapter


def main():
    parser = argparse.ArgumentParser(); add_mode_arguments(parser); args = parser.parse_args()
    adapter = make_adapter(args); adapter.connect()
    try:
        if not adapter.capabilities.wrench:
            raise SystemExit("adapter does not expose wrench sensing")
        baseline = np.asarray(adapter.get_wrench_world_or_sensor(), float)
        print("Free-space baseline:", baseline.tolist())
        if executing(args):
            confirm("Apply only a light MANUAL push in the documented +task-X direction")
            pushed = np.asarray(adapter.get_wrench_world_or_sensor(), float)
            print("Measured change:", (pushed - baseline).tolist())
            print("Operator must verify environment-on-tool sign and task-frame axis; no autonomous contact was commanded.")
        else:
            print("DRY RUN: no push requested and no motion commanded")
    finally: adapter.disconnect()
    return 0


if __name__ == "__main__": raise SystemExit(main())
