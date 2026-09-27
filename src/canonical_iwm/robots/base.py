"""Measured-state/command-separated robot interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class UnsupportedCapabilityError(NotImplementedError):
    pass


@dataclass(frozen=True)
class AdapterCapabilities:
    joint_state: bool = False
    tcp_pose: bool = False
    tcp_twist: bool = False
    joint_effort: bool = False
    wrench: bool = False
    jacobian: bool = False
    position_target: bool = False
    joint_position_command: bool = False
    cartesian_pose_command: bool = False
    protective_stop: bool = False


class RobotAdapter(ABC):
    """Hardware-neutral contract. Getters are measurements unless named target."""

    capabilities = AdapterCapabilities()

    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def disconnect(self) -> None: ...

    @abstractmethod
    def is_connected(self) -> bool: ...

    def _unsupported(self, capability):
        raise UnsupportedCapabilityError(f"{type(self).__name__} does not provide {capability}")

    def get_joint_positions(self): self._unsupported("measured joint positions")
    def get_joint_velocities(self): self._unsupported("measured joint velocities")
    def get_tcp_pose_world(self): self._unsupported("measured world TCP pose")
    def get_tcp_twist_world(self): self._unsupported("measured world TCP twist")
    def get_joint_torques_or_efforts(self): self._unsupported("measured joint effort")
    def get_wrench_world_or_sensor(self): self._unsupported("measured wrench")
    def get_jacobian(self): self._unsupported("Jacobian")

    def get_position_target_if_available(self):
        """Controller equilibrium/position target; never substitutes for measured q."""
        self._unsupported("equilibrium or position target")

    def get_equilibrium_or_position_target(self):
        return self.get_position_target_if_available()

    def command_joint_position_target(self, target): self._unsupported("joint-position command")
    def command_cartesian_pose(self, target_world): self._unsupported("Cartesian-pose command")

    @abstractmethod
    def stop_motion(self) -> None: ...

    @abstractmethod
    def protective_stop_status(self) -> bool: ...
