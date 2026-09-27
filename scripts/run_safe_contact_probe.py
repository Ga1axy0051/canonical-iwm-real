#!/usr/bin/env python3
"""Single-axis, low-speed contact probe shell—not an insertion controller."""

import argparse
import math
import time
import numpy as np

from _common import add_mode_arguments, confirm, executing, make_adapter
from canonical_iwm.actions import CanonicalAction
from canonical_iwm.controller_core import CanonicalController, CartesianGuardLimits


def main():
    parser=argparse.ArgumentParser(); add_mode_arguments(parser)
    parser.add_argument("--confirm-contact-test", action="store_true")
    parser.add_argument("--max-translation-m", type=float, default=0.00025)
    parser.add_argument("--max-speed-mps", type=float, default=0.001)
    parser.add_argument("--max-force-N", type=float, default=3.0)
    parser.add_argument("--max-torque-Nm", type=float, default=0.3)
    parser.add_argument("--timeout-s", type=float, default=2.0)
    args=parser.parse_args(); live=executing(args); adapter=make_adapter(args); adapter.connect()
    try:
        if not live:
            print("DRY RUN ONLY: would perform one +task-X probe with conservative limits", vars(args)); return 0
        if not args.confirm_contact_test: raise SystemExit("live contact requires --confirm-contact-test")
        if args.robot == "mock": raise SystemExit("mock cannot validate a live contact test")
        if not adapter.capabilities.wrench: raise SystemExit("live contact refused: force/torque sensing unavailable")
        if not adapter.capabilities.cartesian_pose_command or not adapter.capabilities.tcp_twist:
            raise SystemExit("live contact refused: guarded Cartesian command/twist capability unavailable")
        values=(args.max_translation_m,args.max_speed_mps,args.max_force_N,args.max_torque_Nm,args.timeout_s)
        if not all(np.isfinite(values)) or not all(value>0 for value in values): raise SystemExit("all probe limits must be finite and positive")
        confirm("Final contact-test confirmation: E-stop reachable, native safety active, workspace clear?")
        def enforce_limits():
            wrench=np.asarray(adapter.get_wrench_world_or_sensor(),float)
            speed=float(np.linalg.norm(np.asarray(adapter.get_tcp_twist_world(),float)[:3]))
            if np.linalg.norm(wrench[:3])>args.max_force_N or np.linalg.norm(wrench[3:])>args.max_torque_Nm or speed>args.max_speed_mps:
                adapter.stop_motion(); raise SystemExit("force/torque/velocity limit exceeded; stopped")
        enforce_limits()
        period_s=0.02; required_s=args.max_translation_m/args.max_speed_mps
        if required_s>args.timeout_s: raise SystemExit("configured speed cannot complete the bounded probe before timeout")
        steps=max(1,math.ceil(required_s/period_s)); step_m=args.max_translation_m/steps
        controller=CanonicalController(adapter,np.eye(4),CartesianGuardLimits(step_m,0.0)); started=time.monotonic(); result=None
        for _ in range(steps):
            if time.monotonic()-started>args.timeout_s: adapter.stop_motion(); raise SystemExit("probe timeout; stopped")
            enforce_limits()
            action=CanonicalAction.from_parts([step_m,0,0],[0,0,0])
            result=controller.execute(action,dry_run=False)
            enforce_limits(); time.sleep(period_s)
        adapter.stop_motion()
        print("single command completed and stop issued", result["checks"])
    finally:
        try: adapter.stop_motion()
        finally: adapter.disconnect()
    return 0


if __name__ == "__main__": raise SystemExit(main())
