import numpy as np

from canonical_iwm.actions import CanonicalAction
from canonical_iwm.controller_core import CanonicalController, equilibrium_preserving_target
from canonical_iwm.robots import MockRobotAdapter


def test_mock_robot_measured_and_target_state_are_separate_concepts():
    robot = MockRobotAdapter(); robot.connect()
    robot.command_joint_position_target(np.ones(6) * 0.1)
    np.testing.assert_allclose(robot.get_joint_positions(), robot.get_position_target_if_available())
    robot.disconnect()


def test_dry_run_controller_does_not_move():
    robot = MockRobotAdapter(); robot.connect(); before = robot.get_tcp_pose_world()
    result = CanonicalController(robot, np.eye(4)).execute(CanonicalAction.from_parts([0.00025, 0, 0], [0, 0, 0]), dry_run=True)
    assert result["accepted"] and not result["executed"]
    np.testing.assert_allclose(robot.get_tcp_pose_world(), before)


def test_equilibrium_preserving_strategy():
    measured = np.array([1, 2]); equilibrium = np.array([1.1, 1.9]); ik = np.array([1.2, 2.2])
    np.testing.assert_allclose(equilibrium_preserving_target(measured, equilibrium, ik, 0.5), equilibrium + 0.5 * (ik - measured))
