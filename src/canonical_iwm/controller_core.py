"""Robot-independent Cartesian planning and equilibrium-target policy."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .actions import CanonicalAction, apply_task_delta
from .transforms import rotation_angle


@dataclass(frozen=True)
class CartesianGuardLimits:
    max_translation_m: float = 0.001
    max_rotation_rad: float = np.deg2rad(0.5)


def bounded_residual(residual, max_norm: float) -> np.ndarray:
    residual = np.asarray(residual, float)
    norm = float(np.linalg.norm(residual))
    if max_norm < 0:
        raise ValueError("max_norm must be nonnegative")
    return residual if norm <= max_norm or norm == 0 else residual * (max_norm / norm)


def equilibrium_preserving_target(q_measured, q_equilibrium_target, q_ik, alpha=1.0) -> np.ndarray:
    """Simulation-validated strategy; recalibrate before real hardware use."""
    measured, equilibrium, ik = map(lambda value: np.asarray(value, float), (q_measured, q_equilibrium_target, q_ik))
    if not (measured.shape == equilibrium.shape == ik.shape) or not 0 <= alpha <= 1:
        raise ValueError("joint vectors must match and alpha must be in [0, 1]")
    return equilibrium + alpha * (ik - measured)


class CanonicalController:
    def __init__(self, adapter, T_world_task, limits=CartesianGuardLimits()):
        self.adapter = adapter
        self.T_world_task = np.asarray(T_world_task, float)
        self.limits = limits

    def plan(self, action: CanonicalAction) -> dict:
        delta = action.action_delta_tcp_task
        checks = {
            "finite": bool(np.all(np.isfinite(delta))),
            "translation_bound": float(np.linalg.norm(delta[:3])) <= self.limits.max_translation_m,
            "rotation_bound": float(np.linalg.norm(delta[3:])) <= self.limits.max_rotation_rad,
            "connected": bool(self.adapter.is_connected()),
            "not_protective_stopped": not bool(self.adapter.protective_stop_status()),
        }
        current = self.adapter.get_tcp_pose_world()
        desired = apply_task_delta(current, self.T_world_task, action)
        return {"accepted": all(checks.values()), "checks": checks, "current_pose": current, "desired_pose": desired}

    def execute(self, action: CanonicalAction, *, dry_run: bool = True) -> dict:
        plan = self.plan(action)
        if not plan["accepted"]:
            return {**plan, "executed": False}
        if not dry_run:
            self.adapter.command_cartesian_pose(plan["desired_pose"])
        return {**plan, "executed": not dry_run}

    def measure_result(self, before_pose, after_pose, action: CanonicalAction) -> dict:
        requested = action.action_delta_tcp_task[:3]
        actual_world = np.asarray(after_pose)[:3, 3] - np.asarray(before_pose)[:3, 3]
        actual_task = self.T_world_task[:3, :3].T @ actual_world
        direction = requested / max(float(np.linalg.norm(requested)), 1e-15)
        along = float(actual_task @ direction) if np.linalg.norm(requested) else 0.0
        return {
            "requested_motion_task_m": requested,
            "actual_motion_task_m": actual_task,
            "along_axis_motion_m": along,
            "orthogonal_motion_m": float(np.linalg.norm(actual_task - along * direction)) if np.linalg.norm(requested) else float(np.linalg.norm(actual_task)),
            "orientation_change_rad": rotation_angle(np.asarray(before_pose)[:3, :3].T @ np.asarray(after_pose)[:3, :3]),
        }
