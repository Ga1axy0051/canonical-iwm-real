# Robot adapters

`RobotAdapter` deliberately separates measured state (`get_joint_positions`,
`get_tcp_pose_world`) from controller state (`get_position_target_if_available`)
and commands. Unsupported quantities raise a clear capability error.

| Adapter | Candidate future backend | Current state |
|---|---|---|
| UR5 | ROS/ROS2 or RTDE/vendor driver | Skeleton; no API assumed |
| Franka Panda | libfranka or franka_ros/ROS2 | Skeleton; no API assumed |
| xArm6 | UFactory Python SDK or ROS/ROS2 | Skeleton; no API assumed |
| Mock | In-memory deterministic adapter | Implemented for dry runs/tests |

An integration must declare capability flags only after each path is tested.
Backend-specific conversions, timestamps, watchdogs, safety state, wrench sensor
frame/reference, Jacobian ordering, and TCP configuration belong in the adapter,
not in the canonical core.

The Franka research result showed that measured `q` and the controller
equilibrium target can differ. A configurable strategy is provided:

```text
delta_q_action = q_ik - q_measured
q_command = q_equilibrium_target + alpha * delta_q_action
```

This is a **simulation-validated concept; real-hardware recalibration is
required**. Never reset a generic position target to measured `q` merely to
initialize a command.
