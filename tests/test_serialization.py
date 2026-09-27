import hashlib
import json
from pathlib import Path

import jsonschema
import numpy as np

from canonical_iwm.serialization import ACTION_ORDER, POSE_ORDER, TWIST_ORDER, WRENCH_ORDER, action_vector6, pose_vector6
from canonical_iwm.transforms import rotation_vector_to_matrix

ROOT = Path(__file__).resolve().parents[1]


def test_frozen_schema_is_byte_identical():
    assert hashlib.sha256((ROOT / "configs/schema_v1.json").read_bytes()).hexdigest() == "7da0a541741de01d7f3487db6790208adfe77dd053a3a2dd52ddd8512c1956dd"


def test_ordering_and_rotation_vector_serialization():
    assert POSE_ORDER == ("x_m", "y_m", "z_m", "rx_rad", "ry_rad", "rz_rad")
    assert TWIST_ORDER[0] == "vx_m_s" and WRENCH_ORDER[-1] == "Mz_Nm" and ACTION_ORDER[0] == "dx_m"
    np.testing.assert_allclose(pose_vector6([1, 2, 3], rotation_vector_to_matrix([0.1, -0.2, 0.3])), [1, 2, 3, 0.1, -0.2, 0.3], atol=1e-12)


def test_schema_round_trip():
    state = {"t": 0.0, "T_task_TCP": [0] * 6, "tcp_twist_task": [0] * 6, "wrench_task_at_tcp": [0] * 6, "in_contact": False}
    candidate = {"action_delta_tcp_task": action_vector6([0.00025, 0, 0], [0, 0, 0]).tolist(), "horizon_s": 0.1, "samples": [state], "consequences": {"peak_lateral_force_N": 0, "force_impulse_Ns": 0, "insertion_progress_m": 0, "contact_release": True}}
    payload = {"schema_version": "canonical_iwm.branch.v1", "units": {"angular_velocity": "rad/s", "force": "N", "linear_velocity": "m/s", "position": "m", "rotation": "rad", "time": "s", "torque": "N*m"}, "frames": {"task_frame": "hole_center_z_out", "tcp_frame": "semantic_peg_tip", "wrench_expression": "task_frame", "wrench_reference": "tcp_origin"}, "metadata": {"robot_identity": "ur5", "controller_contract_id": "test"}, "branch_state": state, "candidates": [candidate] * 8}
    encoded = json.loads(json.dumps(payload))
    jsonschema.validate(encoded, json.loads((ROOT / "configs/schema_v1.json").read_text()))
