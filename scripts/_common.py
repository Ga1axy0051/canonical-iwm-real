from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from canonical_iwm.robots import FrankaAdapter, MockRobotAdapter, UR5Adapter, XArm6Adapter


def add_mode_arguments(parser):
    parser.add_argument("--robot", choices=("mock", "ur5", "franka", "xarm6"), default="mock")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="plan/read only (default)")
    mode.add_argument("--execute", action="store_true", help="permit guarded commands after confirmations")
    parser.add_argument("--config", type=Path, help="explicit local robot config; required for real execution")


def executing(args) -> bool:
    return bool(args.execute)


def make_adapter(args):
    if args.execute and args.robot != "mock" and args.config is None:
        raise SystemExit("live execution requires --config; no robot IP is accepted implicitly")
    config = json.loads(args.config.read_text()) if args.config else {}
    classes = {"mock": MockRobotAdapter, "ur5": UR5Adapter, "franka": FrankaAdapter, "xarm6": XArm6Adapter}
    return classes[args.robot](**config)


def confirm(text):
    if input(f"{text} Type YES to continue: ").strip() != "YES":
        raise SystemExit("operator declined; no command sent")


def array_text(value):
    return np.array2string(np.asarray(value), precision=7, suppress_small=False)
