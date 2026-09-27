#!/usr/bin/env python3
"""Read-only task-frame sanity check by default."""

import argparse
import numpy as np

from _common import add_mode_arguments, make_adapter
from canonical_iwm.frames import T_task_tcp


def main():
    parser = argparse.ArgumentParser(); add_mode_arguments(parser)
    args = parser.parse_args()
    adapter = make_adapter(args); adapter.connect()
    try:
        pose = adapter.get_tcp_pose_world()
        relative = T_task_tcp(np.eye(4), pose)
        print("DRY RUN/read-only task frame. T_task_tcp=", relative.tolist())
    finally: adapter.disconnect()
    return 0


if __name__ == "__main__": raise SystemExit(main())
