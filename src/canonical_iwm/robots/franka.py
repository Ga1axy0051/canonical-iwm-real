"""Franka Panda adapter skeleton; preserves equilibrium-target distinction."""

from .base import AdapterCapabilities, RobotAdapter


class FrankaAdapter(RobotAdapter):
    capabilities = AdapterCapabilities()

    def __init__(self, backend=None):
        self.backend = backend

    def connect(self):
        raise NotImplementedError("Franka backend not configured; integrate validated libfranka/franka_ros backend")

    def disconnect(self): pass
    def is_connected(self): return False
    def stop_motion(self): raise NotImplementedError("Franka stop path requires a validated backend")
    def protective_stop_status(self): return True

    def get_equilibrium_or_position_target(self):
        raise NotImplementedError("backend must explicitly expose the controller equilibrium target")
