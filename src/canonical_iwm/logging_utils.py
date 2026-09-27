"""Append-only JSONL logging for canonical state/action and controller context."""

from __future__ import annotations

import json
from pathlib import Path
from threading import Lock

from .serialization import json_ready


class CanonicalJsonlLogger:
    def __init__(self, path):
        self.path = Path(path)
        self._lock = Lock()

    def append(self, *, state, action=None, controller_context=None, metadata=None):
        row = {
            "state": state.as_dict() if hasattr(state, "as_dict") else state,
            "action_delta_tcp_task": None if action is None else list(action.action_delta_tcp_task),
            "controller_context": controller_context or {},
            "metadata": metadata or {},
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock, self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, default=json_ready, sort_keys=True) + "\n")
