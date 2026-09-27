import numpy as np

from canonical_iwm.actions import CanonicalAction, apply_task_delta
from canonical_iwm.transforms import make_transform, rotation_vector_to_matrix


def test_canonical_translation_uses_task_axes_and_preserves_orientation():
    task = make_transform(rotation_vector_to_matrix([0, 0, np.pi / 2]))
    current = make_transform(rotation_vector_to_matrix([0.1, 0.2, 0.3]))
    desired = apply_task_delta(current, task, CanonicalAction.from_parts([0.001, 0, 0], [0, 0, 0]))
    np.testing.assert_allclose(desired[:3, 3], [0, 0.001, 0], atol=1e-12)
    np.testing.assert_allclose(desired[:3, :3], current[:3, :3], atol=1e-12)
