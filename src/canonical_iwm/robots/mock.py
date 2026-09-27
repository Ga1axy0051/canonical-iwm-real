"""Deterministic no-hardware adapter for every bring-up script."""

from __future__ import annotations

import numpy as np

from .base import AdapterCapabilities, RobotAdapter
from ..transforms import validate_transform


class MockRobotAdapter(RobotAdapter):
    capabilities = AdapterCapabilities(
        joint_state=True,
        tcp_pose=True,
        tcp_twist=True,
        joint_effort=True,
        wrench=True,
        jacobian=True,
        position_target=True,
        joint_position_command=True,
        cartesian_pose_command=True,
        protective_stop=True,
    )

    def __init__(self, joint_count: int = 6):
        if joint_count <= 0:
            raise ValueError("joint_count must be positive")
        self._connected = False
        self._q = np.zeros(joint_count)
        self._qdot = np.zeros(joint_count)
        self._effort = np.zeros(joint_count)
        self._target = np.zeros(joint_count)
        self._pose = np.eye(4)
        self._twist = np.zeros(6)
        self._wrench = np.zeros(6)
        self._stopped = False

    def connect(self): self._connected = True
    def disconnect(self): self._connected = False
    def is_connected(self): return self._connected

    def _require(self):
        if not self._connected:
            raise RuntimeError("mock robot is not connected")

    def get_joint_positions(self): self._require(); return self._q.copy()
    def get_joint_velocities(self): self._require(); return self._qdot.copy()
    def get_tcp_pose_world(self): self._require(); return self._pose.copy()
    def get_tcp_twist_world(self): self._require(); return self._twist.copy()
    def get_joint_torques_or_efforts(self): self._require(); return self._effort.copy()
    def get_wrench_world_or_sensor(self): self._require(); return self._wrench.copy()
    def get_jacobian(self): self._require(); return np.zeros((6, self._q.size))
    def get_position_target_if_available(self): self._require(); return self._target.copy()

    def command_joint_position_target(self, target):
        self._require()
        target = np.asarray(target, float)
        if target.shape != self._q.shape or not np.all(np.isfinite(target)):
            raise ValueError("invalid joint target")
        self._target = target.copy()
        self._q = target.copy()

    def command_cartesian_pose(self, target_world):
        self._require()
        self._pose = validate_transform(target_world)

    def stop_motion(self): self._twist[:] = 0.0
    def protective_stop_status(self): return self._stopped

    def set_measured_wrench(self, wrench):
        wrench = np.asarray(wrench, float)
        if wrench.shape != (6,): raise ValueError("wrench must have shape (6,)")
        self._wrench = wrench.copy()

    def set_protective_stop(self, stopped=True): self._stopped = bool(stopped)
