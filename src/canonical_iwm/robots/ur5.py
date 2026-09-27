"""UR5 adapter skeleton; no ROS/RTDE backend is assumed."""

from .base import AdapterCapabilities, RobotAdapter


class UR5Adapter(RobotAdapter):
    capabilities = AdapterCapabilities()

    def __init__(self, backend=None):
        self.backend = backend

    def connect(self):
        raise NotImplementedError("UR5 backend not configured; integrate validated ROS/ROS2 or RTDE driver")

    def disconnect(self): pass
    def is_connected(self): return False
    def stop_motion(self): raise NotImplementedError("UR5 stop path requires a validated backend")
    def protective_stop_status(self): return True
