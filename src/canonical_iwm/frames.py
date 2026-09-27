"""Canonical task-frame and semantic-TCP relationships."""

from __future__ import annotations

import numpy as np

from .transforms import compose, relative_transform, transform_to_pose_vector


def T_task_tcp(T_world_task, T_world_tcp) -> np.ndarray:
    return relative_transform(T_world_task, T_world_tcp)


def T_world_tcp_from_eef(T_world_eef, T_eef_tcp) -> np.ndarray:
    """Map an end-effector pose to the calibrated semantic interaction point."""
    return compose(T_world_eef, T_eef_tcp)


def relative_pose_serialization(T_world_task, T_world_tcp) -> np.ndarray:
    return transform_to_pose_vector(T_task_tcp(T_world_task, T_world_tcp))


def rotate_twist_world_to_task(twist_world, T_world_task) -> np.ndarray:
    twist = np.asarray(twist_world, dtype=float)
    if twist.shape != (6,):
        raise ValueError("twist must have shape (6,)")
    rotation_task_world = np.asarray(T_world_task, dtype=float)[:3, :3].T
    return np.r_[rotation_task_world @ twist[:3], rotation_task_world @ twist[3:]]
