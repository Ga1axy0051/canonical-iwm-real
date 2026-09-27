import numpy as np

from canonical_iwm.transforms import rotation_vector_to_matrix
from canonical_iwm.wrench import shift_moment, transform_wrench, wrench_task_at_tcp


def test_pure_force_and_moment():
    np.testing.assert_allclose(transform_wrench([1, 2, 3], [4, 5, 6], np.eye(3)), [1, 2, 3, 4, 5, 6])


def test_lever_arm_moment_shift():
    np.testing.assert_allclose(shift_moment([0, 0, 0], [0, 1, 0], [1, 0, 0]), [0, 0, 1])


def test_rotation_and_translation():
    rotation = rotation_vector_to_matrix([0, 0, np.pi / 2])
    result = wrench_task_at_tcp([1, 0, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0], rotation)
    np.testing.assert_allclose(result, [0, 1, 0, 0, 0, 0], atol=1e-12)


def test_pure_moment_rotates_without_translation_coupling():
    rotation = rotation_vector_to_matrix([0, 0, np.pi / 2])
    np.testing.assert_allclose(transform_wrench([0, 0, 0], [1, 0, 0], rotation, [5, 4, 3]), [0, 0, 0, 0, 1, 0], atol=1e-12)
