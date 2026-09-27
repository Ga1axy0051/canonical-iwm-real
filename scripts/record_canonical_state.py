#!/usr/bin/env python3
"""Record one canonical state sample; dry-run prints without writing."""

import argparse
import time
import numpy as np

from _common import add_mode_arguments, executing, make_adapter
from canonical_iwm.frames import relative_pose_serialization, rotate_twist_world_to_task
from canonical_iwm.logging_utils import CanonicalJsonlLogger
from canonical_iwm.state import CanonicalState


def main():
    parser = argparse.ArgumentParser(); add_mode_arguments(parser); parser.add_argument("--output", default="logs/canonical_state.jsonl"); parser.add_argument("--in-contact", action="store_true", help="explicit externally validated contact label"); args=parser.parse_args()
    adapter=make_adapter(args); adapter.connect(); task=np.eye(4)
    try:
        wrench = adapter.get_wrench_world_or_sensor() if adapter.capabilities.wrench else np.zeros(6)
        state=CanonicalState(time.time(), relative_pose_serialization(task,adapter.get_tcp_pose_world()), rotate_twist_world_to_task(adapter.get_tcp_twist_world(),task), wrench, args.in_contact)
        if executing(args): CanonicalJsonlLogger(args.output).append(state=state)
        print(state.as_dict()); print("written" if executing(args) else "DRY RUN: not written")
    finally: adapter.disconnect()
    return 0


if __name__ == "__main__": raise SystemExit(main())
