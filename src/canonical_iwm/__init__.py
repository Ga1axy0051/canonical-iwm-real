"""Robot-independent canonical task-space utilities for cautious bring-up."""

from .actions import CanonicalAction, apply_task_delta
from .state import CanonicalState

__all__ = ["CanonicalAction", "CanonicalState", "apply_task_delta"]
__version__ = "0.1.0"
