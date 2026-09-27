import numpy as np

from canonical_iwm.locality import LocalityLimits, calibrate_locality, validate_local_candidate
from canonical_iwm.transforms import make_transform


def fk(q):
    return make_transform(translation=[q[0], 0, 0])


def test_locality_validator_accepts_coherent_candidate():
    jacobian = np.zeros((6, 2)); jacobian[0, 0] = 1
    result = validate_local_candidate(np.zeros(2), [0.001, 0], [-1, -1], [1, 1], jacobian, [0.001, 0, 0, 0, 0, 0], fk, make_transform(translation=[0.001, 0, 0]), 0.1, LocalityLimits(0.01, 0.01, 0.1))
    assert result.accepted


def test_locality_validator_rejects_limits_and_wrong_direction():
    jacobian = np.zeros((6, 1)); jacobian[0, 0] = 1
    result = validate_local_candidate([0], [-0.2], [-0.1], [0.1], jacobian, [0.1, 0, 0, 0, 0, 0], lambda q: make_transform(translation=[q[0], 0, 0]), make_transform(translation=[0.1, 0, 0]), 0.1, LocalityLimits(1, 1, 10))
    assert not result.accepted and not result.checks["joint_limits"] and not result.checks["task_direction"]


def test_locality_calibration_is_robot_data_driven():
    limits = calibrate_locality([[0.01, 0], [0, 0.02]], 0.1, margin=2)
    assert np.isclose(limits.max_joint_delta_l2_rad, 0.04)
