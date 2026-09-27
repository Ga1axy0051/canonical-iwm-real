# Canonical IWM real-robot toolkit

This repository is **not** the full Canonical IWM research repository. It is a
small robot-independent extraction for real-robot calibration and cautious
bring-up. It contains canonical frame/state/action utilities, semantic-TCP and
task-frame calibration support, safe controller adapter contracts, offline
compliance measurement, logging, and dry-run-first bring-up scripts.

It does **not** contain a validated cross-embodiment world model, paired
ordinal-transfer model, large training datasets, simulator experiment stacks,
or a production contact/insertion controller. No real robot has been verified
by this extraction.

## Frozen canonical semantics

- `T_task_TCP = [x, y, z, rx, ry, rz]`: metres followed by a principal rotation
  vector in radians.
- `tcp_twist_task = [vx, vy, vz, wx, wy, wz]`: m/s and rad/s in task axes.
- `wrench_task_at_tcp = [Fx, Fy, Fz, Mx, My, Mz]`: environment-on-tool,
  expressed in task axes, with moment referenced about the semantic TCP.
- `action_delta_tcp_task = [dx, dy, dz, drx, dry, drz]`: task-frame translation
  in metres and task-frame rotation vector in radians.

The semantic TCP is the tool interaction point—not automatically the flange,
wrist, gripper origin, or hand origin. `configs/schema_v1.json` is a byte-for-byte
copy of the frozen source schema.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
python scripts/validate_free_space_motion.py --robot mock --dry-run
```

All scripts default to mock/dry-run behavior. A real backend must be integrated,
reviewed, and configured explicitly. A placeholder invocation is:

```bash
ROBOT_IP=<robot-ip> python scripts/validate_free_space_motion.py \
  --robot ur5 --config calibration/private/ur5.json --execute
```

`ROBOT_IP` is shown only as a deployment placeholder; current skeletons do not
consume it. Never put credentials or a real address in tracked example files.
Live stages demand operator confirmations and must not bypass native safety.

Start with [the bring-up guide](docs/REAL_ROBOT_BRINGUP.md) and complete
[the safety checklist](docs/SAFETY_CHECKLIST.md) before integrating motion.
