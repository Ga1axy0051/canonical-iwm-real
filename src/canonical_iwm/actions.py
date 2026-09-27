"""Canonical task-frame delta actions."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .serialization import action_vector6, vector6
from .transforms import rotation_vector_to_matrix, validate_transform


@dataclass(frozen=True)
class CanonicalAction:
    action_delta_tcp_task: np.ndarray

    def __post_init__(self):
        object.__setattr__(
            self,
            "action_delta_tcp_task",
            vector6(self.action_delta_tcp_task, name="action_delta_tcp_task"),
        )

    @classmethod
    def from_parts(cls, translation_m, rotation_vector_rad):
        return cls(action_vector6(translation_m, rotation_vector_rad))


def apply_task_delta(T_world_tcp, T_world_task, action) -> np.ndarray:
    """Apply translation and rotation expressed in task axes to a TCP pose."""
    current = validate_transform(T_world_tcp)
    task = validate_transform(T_world_task)
    delta = action.action_delta_tcp_task if isinstance(action, CanonicalAction) else vector6(action)
    desired = current.copy()
    desired[:3, 3] += task[:3, :3] @ delta[:3]
    rotation_world = task[:3, :3] @ rotation_vector_to_matrix(delta[3:]) @ task[:3, :3].T
    desired[:3, :3] = rotation_world @ current[:3, :3]
    return validate_transform(desired)
