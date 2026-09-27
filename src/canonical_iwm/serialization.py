"""Frozen schema_v1 vector ordering and serialization helpers."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

POSE_ORDER = ("x_m", "y_m", "z_m", "rx_rad", "ry_rad", "rz_rad")
TWIST_ORDER = ("vx_m_s", "vy_m_s", "vz_m_s", "wx_rad_s", "wy_rad_s", "wz_rad_s")
WRENCH_ORDER = ("Fx_N", "Fy_N", "Fz_N", "Mx_Nm", "My_Nm", "Mz_Nm")
ACTION_ORDER = ("dx_m", "dy_m", "dz_m", "drx_rad", "dry_rad", "drz_rad")
ACTIVE_NORMAL_FORCE_EPSILON_N = 1e-4


def vector6(value, *, name: str = "vector6") -> np.ndarray:
    result = np.asarray(value, dtype=float)
    if result.shape != (6,) or not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must contain exactly six finite numbers")
    return result


def pose_vector6(position_task_m, rotation_task_tcp) -> np.ndarray:
    from .transforms import matrix_to_rotation_vector

    position = np.asarray(position_task_m, dtype=float)
    if position.shape != (3,):
        raise ValueError("position must have shape (3,)")
    return np.r_[position, matrix_to_rotation_vector(rotation_task_tcp)]


def twist_vector6(linear_task_m_s, angular_task_rad_s) -> np.ndarray:
    return vector6(np.r_[linear_task_m_s, angular_task_rad_s], name="tcp_twist_task")


def wrench_vector6(force_task_n, moment_at_tcp_task_nm) -> np.ndarray:
    return vector6(np.r_[force_task_n, moment_at_tcp_task_nm], name="wrench_task_at_tcp")


def action_vector6(delta_position_task_m, delta_rotation_task_rad) -> np.ndarray:
    return vector6(np.r_[delta_position_task_m, delta_rotation_task_rad], name="action_delta_tcp_task")


def in_contact(normal_forces_n) -> bool:
    return any(float(value) > ACTIVE_NORMAL_FORCE_EPSILON_N for value in normal_forces_n)


def json_ready(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"cannot JSON-encode {type(value).__name__}")


def dumps(value, **kwargs) -> str:
    return json.dumps(value, default=json_ready, **kwargs)
