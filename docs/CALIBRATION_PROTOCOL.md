# Calibration protocol

## Semantic TCP

Calibrate the physical interaction point for the installed tool/end effector.
Record tool identity, mounting, payload, center of mass, method, sample count,
residuals, date, and operator. Reject results that change after remounting.

## Task frame

Record `T_world_task`, origin definition, axis markings, and handedness. For the
historical insertion task, +Z points out of the hole toward the approaching
robot, while +X/+Y are lateral axes. A new task may use a new calibrated frame,
but serialized quantities must retain task-relative semantics.

## Wrench

First measure a free-space baseline. Then use a light manual push in each marked
axis and confirm environment-on-tool sign. Document the sensor frame and source
reference point; shift moments to the semantic TCP before serialization.

## Locality and compliance

Calibrate joint-delta, velocity-equivalent, FK residual, and direction limits per
robot/tool/controller/speed configuration. Do not reuse UR5/Franka simulator
thresholds as universal hardware limits. Fit compliance from symmetric signed
perturbations when practical, subtracting a same-condition zero-load baseline.
