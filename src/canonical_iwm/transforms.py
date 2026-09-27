"""Small, strict SE(3) and SO(3) helpers."""

from __future__ import annotations

import numpy as np
from scipy.spatial.transform import Rotation


def _array(value, shape):
    out = np.asarray(value, dtype=float)
    if out.shape != shape or not np.all(np.isfinite(out)):
        raise ValueError(f"expected finite array with shape {shape}, got {out.shape}")
    return out


def validate_transform(transform, *, atol: float = 1e-8) -> np.ndarray:
    transform = _array(transform, (4, 4))
    if not np.allclose(transform[3], [0.0, 0.0, 0.0, 1.0], atol=atol):
        raise ValueError("invalid homogeneous-transform bottom row")
    rotation = transform[:3, :3]
    if not np.allclose(rotation.T @ rotation, np.eye(3), atol=atol) or not np.isclose(
        np.linalg.det(rotation), 1.0, atol=atol
    ):
        raise ValueError("transform rotation must be right-handed and orthonormal")
    return transform.copy()


def make_transform(rotation=np.eye(3), translation=np.zeros(3)) -> np.ndarray:
    result = np.eye(4)
    result[:3, :3] = _array(rotation, (3, 3))
    result[:3, 3] = _array(translation, (3,))
    return validate_transform(result)


def compose(*transforms) -> np.ndarray:
    result = np.eye(4)
    for transform in transforms:
        result = result @ validate_transform(transform)
    return validate_transform(result)


def inverse(transform) -> np.ndarray:
    transform = validate_transform(transform)
    rotation = transform[:3, :3]
    result = np.eye(4)
    result[:3, :3] = rotation.T
    result[:3, 3] = -rotation.T @ transform[:3, 3]
    return result


def rotation_vector_to_matrix(rotation_vector) -> np.ndarray:
    return Rotation.from_rotvec(_array(rotation_vector, (3,))).as_matrix()


def matrix_to_rotation_vector(rotation) -> np.ndarray:
    """Return the principal rotation vector (norm in [0, pi])."""
    return Rotation.from_matrix(_array(rotation, (3, 3))).as_rotvec()


def relative_transform(T_world_reference, T_world_body) -> np.ndarray:
    return compose(inverse(T_world_reference), T_world_body)


def transform_to_pose_vector(transform) -> np.ndarray:
    transform = validate_transform(transform)
    return np.r_[transform[:3, 3], matrix_to_rotation_vector(transform[:3, :3])]


def pose_vector_to_transform(pose) -> np.ndarray:
    pose = _array(pose, (6,))
    return make_transform(rotation_vector_to_matrix(pose[3:]), pose[:3])


def rotation_angle(rotation) -> float:
    return float(np.linalg.norm(matrix_to_rotation_vector(rotation)))
