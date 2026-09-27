"""Canonical measured state, intentionally free of robot identity."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .serialization import vector6


@dataclass(frozen=True)
class CanonicalState:
    t: float
    T_task_TCP: np.ndarray
    tcp_twist_task: np.ndarray
    wrench_task_at_tcp: np.ndarray
    in_contact: bool

    def __post_init__(self):
        if not np.isfinite(self.t):
            raise ValueError("t must be finite")
        object.__setattr__(self, "T_task_TCP", vector6(self.T_task_TCP, name="T_task_TCP"))
        object.__setattr__(self, "tcp_twist_task", vector6(self.tcp_twist_task, name="tcp_twist_task"))
        object.__setattr__(self, "wrench_task_at_tcp", vector6(self.wrench_task_at_tcp, name="wrench_task_at_tcp"))

    def as_dict(self) -> dict:
        return {
            "t": float(self.t),
            "T_task_TCP": self.T_task_TCP.tolist(),
            "tcp_twist_task": self.tcp_twist_task.tolist(),
            "wrench_task_at_tcp": self.wrench_task_at_tcp.tolist(),
            "in_contact": bool(self.in_contact),
        }
