# Canonical IWM × Real-Robot Low-Level Controller Integration Audit

## Goal

You are running on the real-robot control computer.

There is already a low-level controller library on this machine that can directly control the robot. We also have a separate research toolkit named:

`canonical-iwm-real`

Your task is **not to move the robot**. Your task is to inspect the existing controller stack, understand exactly what it can do, determine how `canonical-iwm-real` should connect to it, and write a self-contained Markdown audit that can be sent back for the next integration round.

The intended architecture is:

Canonical IWM high-level algorithm
→ RobotAdapter / integration layer
→ existing low-level controller library
→ vendor driver / real-time control
→ real robot

The low-level controller should remain responsible for vendor communication, real-time servo/control, joint/Cartesian command execution, watchdogs, protective stops, native safety, and hardware-specific state acquisition.

The `canonical-iwm-real` layer should handle semantic TCP, task frame, canonical task-space state/action representation, wrench transformation, locality/FK/Jacobian checks, compliance identification, canonical logging, and later cross-embodiment interaction modeling.

The goal is to design the **thinnest safe adapter** between the two.

---

## 0. Hard Safety Rule

During this whole task:

`REAL_HARDWARE_MOTION_EXECUTED = NO`

must remain true.

You may inspect source code, configuration, docs, examples, launch files, logs, recorded data, and read-only ROS topics/services/actions. You may run static tests, mock tests, or read-only state streaming only when the existing lab workflow clearly establishes that it is non-commanding.

Do not:
- issue any joint or Cartesian motion command;
- send hold/zero commands;
- test trajectory execution, impedance, force control, or contact;
- disable/bypass protective stop or vendor safety;
- alter collision/force/workspace limits;
- alter payload/TCP configuration on hardware;
- recover from protective stop;
- start a controller that may implicitly move the robot.

If a call might move hardware and you cannot prove it is read-only, do not run it.

---

## 1. Locate the Existing Controller Stack

Identify the controller repository/library actually used by the lab.

Find:
- repository/library path;
- actual robot currently controlled;
- whether multiple robots are supported;
- known working examples;
- main entry point used in the lab;
- config files;
- communication backend;
- ROS/ROS2/vendor SDK dependencies;
- control frequency;
- whether it has already been used successfully on real hardware.

Report:

CONTROLLER_LIBRARY_PATH =
CONTROLLER_REPOSITORY_NAME =
ACTUAL_ROBOT =
SUPPORTED_ROBOTS =
BACKEND =
ROS_VERSION =
VENDOR_SDK =
LANGUAGE =
CONTROL_RATE =
STATE_RATE =
REAL_TIME_LOOP =
KNOWN_WORKING_ENTRY_POINT =
KNOWN_WORKING_EXAMPLE =
CANONICAL_IWM_REAL_PATH =

If unknown, write `UNKNOWN / NOT FOUND`. Do not guess.

---

## 2. Determine the Hardware Context

We ultimately care about:
- UR5;
- Franka Panda;
- xArm6.

Possible end effectors:
- Robotiq 2F-85;
- ROHAND dexterous hand.

Determine what is actually connected to this PC:

CONNECTED_ROBOT_MODEL =
CONNECTED_END_EFFECTOR =
CONNECTION_METHOD =
HARDWARE_DRIVER =

Do not print private IPs, tokens, credentials, or secrets into the report.

---

## 3. Full Controller API Capability Audit

Trace actual source implementation, not only READMEs.

Audit exact APIs for:

### State
- joint positions q;
- joint velocities qdot;
- measured joint torques;
- commanded torques;
- motor current / effort;
- flange/EEF/TCP pose;
- TCP twist;
- Jacobian;
- mass matrix;
- Coriolis/gravity terms;
- F/T sensor;
- external wrench estimate;
- joint reaction forces;
- controller target/equilibrium state;
- robot mode;
- protective-stop/safety state;
- timestamps and sequence numbers.

### Commands
- joint position;
- joint velocity;
- joint torque;
- joint trajectory;
- Cartesian pose;
- Cartesian velocity/twist;
- Cartesian trajectory;
- Cartesian/joint impedance;
- admittance;
- force control;
- hybrid force-position;
- gripper;
- stop/halt;
- watchdog;
- recovery.

### Configuration
- TCP/tool transform;
- payload/CoM;
- force-sensor calibration;
- control frequency;
- joint/velocity/acceleration/jerk limits;
- workspace limits;
- collision thresholds;
- force/torque thresholds;
- watchdog/command timeout;
- interpolation/smoothing.

Create a table:

| Capability | Exact API / Function | Source File | Input | Output | Unit | Frame | Update Rate | Blocking/Streaming | Known Working Example | Notes |

Use `NOT EXPOSED` or `API EXISTS / HARDWARE STATUS UNKNOWN` where appropriate.

---

## 4. Frame Convention Audit

Determine exact conventions for:
1. world frame;
2. base frame;
3. flange frame;
4. EEF frame;
5. tool frame;
6. TCP frame;
7. F/T sensor frame;
8. any task/user frame.

For every pose API determine whether it returns e.g. `T_base_tcp`, `T_world_tcp`, `T_base_flange`, etc.

Determine rotation representation and quaternion ordering if applicable.

Create:

`canonical-iwm-real/docs/LOW_LEVEL_FRAME_AUDIT.md`

Include a transform-chain diagram:

base → flange → EEF/tool → semantic TCP

Do not modify hardware configuration.

---

## 5. Wrench / Force Convention Audit

For each available wrench source determine:
- physical sensor vs estimate;
- units;
- frame;
- sign;
- moment reference point;
- filtering;
- bias handling;
- gravity compensation;
- update rate.

Explicitly answer whether the wrench is:
- environment-on-tool/robot, or
- robot/tool-on-environment.

The Canonical IWM target convention is:

`wrench_task_at_tcp = [Fx, Fy, Fz, Mx, My, Mz]`

meaning:
- environment-on-tool;
- expressed in task frame;
- moment about semantic TCP.

Document all conversions required.

---

## 6. Timing and Real-Time Architecture

Determine:
- state rate;
- command rate;
- servo rate;
- real-time thread/process;
- communication process;
- Python/C++ boundary;
- command buffering;
- interpolation;
- watchdog behavior;
- command timeout;
- timestamp semantics.

Draw the software architecture and identify the cleanest existing integration boundary.

If there is a hard RT loop, do not put JSON serialization, plotting, disk logging, slow optimization, or high-level learning inference inside it.

---

## 7. Measured State vs Controller Target

Explicitly determine whether the controller distinguishes:

measured q
vs
desired/target/equilibrium q

and

measured TCP
vs
desired TCP.

Report:

MEASURED_Q_API =
TARGET_Q_API =
EQUILIBRIUM_TARGET_EXPOSED = YES / NO
TARGET_PERSISTENCE_BEHAVIOR =

Do not assume `q_target == q_measured`.

This matters because in prior simulation, resetting an internal equilibrium target to measured q itself caused motion.

---

## 8. Inspect `canonical-iwm-real`

Inspect:

`src/canonical_iwm/robots/base.py`

plus existing robot adapters and core modules:
- frames.py
- transforms.py
- wrench.py
- actions.py
- state.py
- locality.py
- controller_core.py
- compliance.py
- serialization.py

Understand the current abstraction before changing anything.

---

## 9. Build the Exact RobotAdapter API Map

Create:

`canonical-iwm-real/docs/CONTROLLER_API_MAP.md`

Map RobotAdapter concepts to exact low-level APIs:

connect()
disconnect()
is_connected()
get_joint_positions()
get_joint_velocities()
get_joint_torques_or_efforts()
get_tcp_pose_world()
get_tcp_twist_world()
get_wrench_world_or_sensor()
get_jacobian()
get_equilibrium_or_position_target()
command_joint_position_target()
command_cartesian_pose()
command_cartesian_velocity()
stop_motion()
protective_stop_status()

Do not force unsupported methods. Add capability flags.

For every mapping record:
- exact controller API;
- units;
- frame conversion;
- blocking/streaming semantics;
- verified/unverified status.

---

## 10. Proposed Adapter Architecture

Design the thinnest adapter:

canonical_iwm
→ robot-specific adapter
→ existing controller library

Do not make the low-level controller depend on Canonical IWM.

The adapter should mainly handle:
- types;
- units;
- frames;
- timestamps;
- capability reporting;
- command construction;
- high-level safety gating;
- canonical logging conversion.

Do not rewrite the controller.

---

## 11. Trace One Canonical Action End-to-End

Without moving hardware, trace:

`action_delta_tcp_task = [0.0005, 0, 0, 0, 0, 0]`

meaning +0.5 mm in task-frame X.

Document:
1. read state;
2. get TCP pose;
3. get `T_world_task`;
4. compute `T_task_tcp`;
5. apply +0.5 mm delta;
6. transform back to robot/base coordinates;
7. convert to controller command representation;
8. apply safety checks;
9. identify the exact API that would receive it;
10. read measured state afterward;
11. compute realized canonical displacement;
12. log state/action/outcome.

Do not execute step 9. Generate a dry-run command object instead.

---

## 12. Trace Wrench End-to-End

Trace:

raw F/T or external wrench
→ original frame
→ semantic TCP reference point
→ task frame
→ Canonical IWM wrench.

Document sign conversion, rotation, moment shift, timestamp handling, filtering, and bias assumptions.

If no wrench is exposed, state this clearly and list available alternatives without inventing an estimator.

---

## 13. TCP / Tool Configuration Plan

Determine how the existing controller handles:
- flange-to-tool;
- tool-to-TCP;
- payload;
- center of mass.

Do not change them.

Design a sanitized config example such as:

```yaml
robot:
  type: ur5
  backend: existing_controller
  address: ${ROBOT_IP}

tool:
  name: canonical_probe
  T_eef_tcp:
    translation_m: [0.0, 0.0, 0.08]
    rotation_rotvec_rad: [0.0, 0.0, 0.0]
```

No private IPs in tracked files.

---

## 14. High-Level Safety Layer Design

Propose checks for:
- connection;
- fresh timestamps;
- finite values;
- robot mode;
- protective stop;
- joint position/velocity/acceleration;
- max Cartesian delta;
- max Cartesian speed;
- max orientation delta;
- workspace bounds;
- command timeout;
- force/torque if available.

Do not invent final numerical limits yet. Read the existing controller/vendor/lab limits and report them.

---

## 15. Read-Only Testing

Only if source inspection proves an interface is read-only, optionally test:
- q;
- qdot;
- TCP pose/twist;
- wrench;
- safety status;
- update rate/timestamps.

Before any connection call, inspect it and verify that it does not enable motion, clear stops, send targets, or enter a motion-producing servo mode.

If uncertain, do not connect.

If no safe read-only test is possible, report:

READ_ONLY_HARDWARE_TEST = NOT RUN
REASON = ...

---

## 16. Static / Mock Integration Test

Using mock or recorded data, validate:
- adapter import;
- state parsing;
- units;
- frame transforms;
- wrench conversion;
- canonical action construction;
- dry-run command generation;
- safety rejection;
- stale-state rejection.

No hardware motion.

---

## 17. First Real-Hardware Bring-Up Plan

Design but do not execute:

Stage A — read-only state streaming for ~30 s.

Stage B — future zero/hold semantics audit. Do not assume resetting target to measured q is safe.

Stage C — future +0.25 mm free-space move at low speed.

Stage D — future -0.25 mm.

Stage E — future ±0.5 mm.

Stage F — future ±1 mm only after prior stages pass.

Stage G — future gentle wrench-sign validation while stationary.

Stage H — future very light wall contact only after explicit human authorization.

No insertion yet.

---

## 18. Real-Time Integration Boundary

Recommend where future high-level components should run:
- candidate-action generation;
- world-model inference;
- receding-horizon selection;
- canonical logging.

Keep them outside hard RT unless the existing architecture explicitly supports them.

Determine the controller’s preferred high-level command type and update rate.

---

## 19. Cross-Embodiment Design Constraint

Keep shared semantics across UR5, Franka, xArm6:

- canonical task state;
- semantic TCP;
- canonical task-space action;
- canonical wrench.

Keep robot-specific details in adapters:

- joint dimension;
- SDK;
- IK backend;
- target/equilibrium semantics;
- native control mode;
- sensor source;
- safety API.

We want invariant high-level task meaning, not identical joint commands.

---

## 20. Lessons From Prior Simulation

Use as design constraints, not as assumptions about hardware:

1. Verify the physical EEF frame; do not trust a named tool frame without checking attachment.
2. Reject remote IK branches; endpoint correctness is not enough.
3. Measured q is not automatically controller equilibrium q.
4. Controller compliance/impedance can strongly change contact force.
5. Safe commanded velocity does not guarantee safe post-impact measured velocity.

Therefore this task remains non-contact and non-motion.

---

## 21. Required Primary Deliverable

Create the main handoff report:

`canonical-iwm-real/docs/REAL_ROBOT_CONTROLLER_INTEGRATION_AUDIT.md`

This file must be self-contained so a future agent can continue without reading this task prompt.

It must include:

1. Executive Summary
2. Controller Stack Overview
3. Hardware Context
4. Exact API Inventory
5. Frame Convention
6. Wrench Convention
7. Timing / Real-Time Architecture
8. Measured vs Target State
9. RobotAdapter Mapping
10. Missing Capabilities
11. Proposed Adapter Implementation
12. Dry-Run +0.5 mm Canonical Action Trace
13. Canonical Wrench Trace
14. Safety Integration
15. Read-Only Test Results
16. First Hardware Bring-Up Plan
17. Main Risks / Unknowns
18. Recommended Next Task

For every important claim, cite evidence by source file and exact class/function, with line ranges where practical.

Use evidence labels:
- VERIFIED
- INFERRED
- UNKNOWN
- NOT TESTED

---

## 22. Supporting Deliverables

Also create:

`canonical-iwm-real/docs/CONTROLLER_API_MAP.md`

`canonical-iwm-real/docs/LOW_LEVEL_FRAME_AUDIT.md`

If useful, create:

`canonical-iwm-real/configs/examples/<robot>_real.yaml`

with sanitized placeholders only.

Optional machine-readable summary:

`canonical-iwm-real/docs/REAL_ROBOT_CONTROLLER_INTEGRATION_AUDIT.json`

Do not fabricate missing values.

---

## 23. Evidence Discipline

Do not write unsupported statements such as “probably base frame”.

If something cannot be verified, say so.

The next round must be able to distinguish:
1. directly verified facts;
2. plausible inference;
3. unresolved unknowns.

---

## 24. Do Not Over-Engineer

Do not:
- rewrite the controller;
- create a second low-level servo architecture;
- introduce ROS if not needed;
- introduce new IPC if the existing API is clean;
- add a learned model;
- add contact control;
- add new IK unless required for integration design.

The task is to understand the existing controller and define the thinnest safe integration layer.

---

## 25. Final Status Classification

Choose one:

`CONTROLLER_INTEGRATION_STATUS = READY_FOR_READ_ONLY`

or

`CONTROLLER_INTEGRATION_STATUS = READY_FOR_FREE_SPACE_BRINGUP`

or

`CONTROLLER_INTEGRATION_STATUS = BLOCKED`

Do not mark free-space-ready merely because a motion API exists.

---

## 26. Final Terminal Output

Print a concise final summary:

CONTROLLER_INTEGRATION_STATUS = ...

Primary audit:
canonical-iwm-real/docs/REAL_ROBOT_CONTROLLER_INTEGRATION_AUDIT.md

Controller API map:
canonical-iwm-real/docs/CONTROLLER_API_MAP.md

Frame audit:
canonical-iwm-real/docs/LOW_LEVEL_FRAME_AUDIT.md

Robot:
...

Existing controller:
...

Control rate:
...

Available measured state:
...

Available commands:
...

Wrench source:
...

Jacobian:
...

TCP/frame convention:
...

Measured-vs-target distinction:
...

Read-only hardware tested:
YES / NO

Real hardware motion executed:
NO

RobotAdapter integration:
READY / PARTIAL / BLOCKED

Main blocker:
...

Recommended next task:
...

The primary audit Markdown is the most important output. It must contain enough exact evidence and context for the next integration round.
