import numpy as np

from canonical_iwm.frames import T_task_tcp, T_world_tcp_from_eef, relative_pose_serialization
from canonical_iwm.transforms import compose, inverse, make_transform, rotation_vector_to_matrix


def test_se3_inverse_and_compose():
    transform = make_transform(rotation_vector_to_matrix([0.1, -0.2, 0.3]), [0.4, 0.5, -0.6])
    np.testing.assert_allclose(compose(transform, inverse(transform)), np.eye(4), atol=1e-12)


def test_eef_to_semantic_tcp():
    eef = make_transform(translation=[1, 2, 3])
    offset = make_transform(translation=[0, 0, 0.08])
    np.testing.assert_allclose(T_world_tcp_from_eef(eef, offset)[:3, 3], [1, 2, 3.08])


def test_task_relative_pose_and_rotvec_roundtrip():
    task = make_transform(rotation_vector_to_matrix([0, 0, np.pi / 2]), [1, 0, 0])
    tcp = compose(task, make_transform(rotation_vector_to_matrix([0.2, 0, 0]), [0.1, 0.2, 0.3]))
    relative = T_task_tcp(task, tcp)
    np.testing.assert_allclose(relative[:3, 3], [0.1, 0.2, 0.3], atol=1e-12)
    np.testing.assert_allclose(relative_pose_serialization(task, tcp), [0.1, 0.2, 0.3, 0.2, 0, 0], atol=1e-12)
