"""Wrench expression and reference-point transformations.

The canonical sign is environment-on-tool; moments are referenced about the
semantic TCP and all six components are expressed in task axes.
"""

from __future__ import annotations

import numpy as np


def _vector(value, name):
    out = np.asarray(value, dtype=float)
    if out.shape != (3,) or not np.all(np.isfinite(out)):
        raise ValueError(f"{name} must have shape (3,) and be finite")
    return out


def rotate_force(force_source, R_target_source) -> np.ndarray:
    rotation = np.asarray(R_target_source, dtype=float)
    if rotation.shape != (3, 3):
        raise ValueError("rotation must have shape (3, 3)")
    return rotation @ _vector(force_source, "force")


def shift_moment(moment_about_source, force, p_source_minus_target) -> np.ndarray:
    """Shift a moment from source point to target point in one frame."""
    return _vector(moment_about_source, "moment") + np.cross(
        _vector(p_source_minus_target, "lever arm"), _vector(force, "force")
    )


def transform_wrench(
    force_source,
    moment_about_source,
    R_target_source,
    p_source_minus_target_source=np.zeros(3),
) -> np.ndarray:
    """Shift in source axes, then express force and moment in target axes."""
    force = _vector(force_source, "force")
    shifted = shift_moment(moment_about_source, force, p_source_minus_target_source)
    rotation = np.asarray(R_target_source, dtype=float)
    return np.r_[rotation @ force, rotation @ shifted]


def wrench_task_at_tcp(
    force_world,
    moment_world_about_contact,
    p_contact_world,
    p_tcp_world,
    R_task_world,
) -> np.ndarray:
    lever = _vector(p_contact_world, "contact point") - _vector(p_tcp_world, "TCP point")
    return transform_wrench(force_world, moment_world_about_contact, R_task_world, lever)
