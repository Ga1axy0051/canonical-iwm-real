"""xArm6 adapter skeleton; no vendor SDK installation is assumed."""

from .base import AdapterCapabilities, RobotAdapter


class XArm6Adapter(RobotAdapter):
    capabilities = AdapterCapabilities()

    def __init__(self, backend=None):
        self.backend = backend

    def connect(self):
        raise NotImplementedError("xArm6 backend not configured; integrate validated UFactory SDK or ROS backend")

    def disconnect(self): pass
    def is_connected(self): return False
    def stop_motion(self): raise NotImplementedError("xArm6 stop path requires a validated backend")
    def protective_stop_status(self): return True
