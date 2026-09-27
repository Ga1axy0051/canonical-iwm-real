#!/usr/bin/env python3
"""Staged, confirmation-gated free-space micro-motion validation."""

import argparse
import json
import numpy as np

from _common import add_mode_arguments, confirm, executing, make_adapter
from canonical_iwm.actions import CanonicalAction
from canonical_iwm.controller_core import CanonicalController


def main():
    parser = argparse.ArgumentParser(); add_mode_arguments(parser)
    parser.add_argument("--axis", choices=("x", "y", "z"), default="x")
    args = parser.parse_args(); live = executing(args)
    adapter = make_adapter(args); adapter.connect()
    records = []
    try:
        q0 = adapter.get_joint_positions(); pose0 = adapter.get_tcp_pose_world()
        print("Stage 0 PASS: connected and read measured state only")
        print("Stage 1: verify semantic TCP configuration mechanically")
        print("Stage 2: verify task-frame axes against the physical setup")
        controller = CanonicalController(adapter, np.eye(4))
        axis = "xyz".index(args.axis)
        for stage, magnitude in ((3, 0.0), (4, 0.00025), (4, 0.0005), (4, 0.001)):
            if live: confirm(f"Stage {stage}: command {magnitude * 1e3:g} mm in free space; E-stop reachable?")
            delta = np.zeros(6); delta[axis] = magnitude
            action = CanonicalAction(delta)
            before_pose = adapter.get_tcp_pose_world(); before_q = adapter.get_joint_positions()
            result = controller.execute(action, dry_run=not live)
            after_pose = adapter.get_tcp_pose_world(); after_q = adapter.get_joint_positions()
            metrics = controller.measure_result(before_pose, after_pose, action)
            metrics.update({"stage": stage, "executed": result["executed"], "joint_displacement_l2_rad": float(np.linalg.norm(after_q-before_q)), "max_joint_velocity_rad_s": float(np.max(np.abs(adapter.get_joint_velocities()), initial=0.0))})
            records.append(metrics)
        print(json.dumps(records, default=lambda x: x.tolist(), indent=2))
        print("MOCK_DRY_RUN_OK" if args.robot == "mock" and not live else "VALIDATION_SEQUENCE_COMPLETE")
    finally:
        adapter.stop_motion(); adapter.disconnect()
    return 0


if __name__ == "__main__": raise SystemExit(main())
