"""Robot-calibrated local IK/FK safety checks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from .transforms import relative_transform, rotation_angle


@dataclass(frozen=True)
class LocalityLimits:
    max_joint_delta_l2_rad: float
    max_joint_delta_abs_rad: float
    max_velocity_equivalent_rad_s: float
    fk_position_tolerance_m: float = 5e-4
    fk_orientation_tolerance_rad: float = np.deg2rad(0.5)
    min_task_direction_cosine: float = 0.0


@dataclass(frozen=True)
class LocalityResult:
    accepted: bool
    checks: dict[str, bool]
    metrics: dict[str, float]
    reasons: tuple[str, ...]


def task_direction_cosine(jacobian, delta_q, requested_task_delta) -> float:
    realized = np.asarray(jacobian, float) @ np.asarray(delta_q, float)
    requested = np.asarray(requested_task_delta, float)
    denominator = float(np.linalg.norm(realized) * np.linalg.norm(requested))
    return 1.0 if denominator <= 1e-15 else float(np.dot(realized, requested) / denominator)


def validate_local_candidate(
    current_q,
    candidate_q,
    joint_lower,
    joint_upper,
    jacobian,
    requested_task_delta,
    fk_callback: Callable[[np.ndarray], np.ndarray],
    desired_tcp_pose,
    dt_s: float,
    limits: LocalityLimits,
) -> LocalityResult:
    current = np.asarray(current_q, float)
    candidate = np.asarray(candidate_q, float)
    lower = np.asarray(joint_lower, float)
    upper = np.asarray(joint_upper, float)
    if not (current.shape == candidate.shape == lower.shape == upper.shape):
        raise ValueError("all joint vectors must have the same shape")
    if dt_s <= 0:
        raise ValueError("dt_s must be positive")
    delta = candidate - current
    finite = bool(np.all(np.isfinite(candidate)))
    within_limits = bool(finite and np.all(candidate >= lower) and np.all(candidate <= upper))
    l2 = float(np.linalg.norm(delta))
    absolute = float(np.max(np.abs(delta), initial=0.0))
    velocity = absolute / dt_s
    cosine = task_direction_cosine(jacobian, delta, requested_task_delta) if finite else -1.0
    position_error = orientation_error = float("inf")
    if finite:
        residual = relative_transform(fk_callback(candidate), desired_tcp_pose)
        position_error = float(np.linalg.norm(residual[:3, 3]))
        orientation_error = rotation_angle(residual[:3, :3])
    checks = {
        "finite": finite,
        "joint_limits": within_limits,
        "local_l2": l2 <= limits.max_joint_delta_l2_rad,
        "local_absolute": absolute <= limits.max_joint_delta_abs_rad,
        "velocity_equivalent": velocity <= limits.max_velocity_equivalent_rad_s,
        "fk_position": position_error <= limits.fk_position_tolerance_m,
        "fk_orientation": orientation_error <= limits.fk_orientation_tolerance_rad,
        "task_direction": cosine >= limits.min_task_direction_cosine,
    }
    return LocalityResult(
        accepted=all(checks.values()),
        checks=checks,
        metrics={
            "joint_delta_l2_rad": l2,
            "joint_delta_abs_rad": absolute,
            "velocity_equivalent_rad_s": velocity,
            "fk_position_error_m": position_error,
            "fk_orientation_error_rad": orientation_error,
            "task_direction_cosine": cosine,
        },
        reasons=tuple(name for name, passed in checks.items() if not passed),
    )


def calibrate_locality(successful_joint_deltas, dt_s: float, margin: float = 1.5) -> LocalityLimits:
    samples = np.asarray(successful_joint_deltas, float)
    if samples.ndim != 2 or samples.shape[0] < 1 or dt_s <= 0 or margin < 1:
        raise ValueError("provide at least one joint-delta row, positive dt, and margin >= 1")
    return LocalityLimits(
        max_joint_delta_l2_rad=margin * float(np.max(np.linalg.norm(samples, axis=1))),
        max_joint_delta_abs_rad=margin * float(np.max(np.abs(samples))),
        max_velocity_equivalent_rad_s=margin * float(np.max(np.abs(samples))) / dt_s,
    )
