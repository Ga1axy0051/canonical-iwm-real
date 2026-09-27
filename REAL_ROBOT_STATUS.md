# Real robot status

No row is hardware-verified. `READY FOR BRINGUP` means the generic toolkit can
support a supervised integration after a backend is implemented; it does not
mean motion-ready.

| Robot | Adapter status | Motion backend | State reading | Cartesian control | Jacobian | Torque/wrench | TCP calibration | Compliance calibration | Contact-ready | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| UR5 | SKELETON | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | ROS/ROS2 or RTDE candidate; no backend selected |
| Franka Panda | SKELETON | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | Preserve measured-vs-equilibrium target distinction |
| xArm6 | SKELETON | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | UFactory SDK or ROS candidate; no approved implementation |

Toolkit/mock status: **READY FOR BRINGUP**. Real-hardware status: **NOT TESTED**.
