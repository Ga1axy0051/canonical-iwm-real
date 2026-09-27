"""Offline local translational compliance identification: delta_x = C_x F."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ComplianceFit:
    C_x_m_per_N: np.ndarray
    K_x_N_per_m: np.ndarray
    compliance_eigenvalues_m_per_N: np.ndarray
    stiffness_eigenvalues_N_per_m: np.ndarray
    condition_number: float
    cross_axis_coupling_ratio: float
    fit_relative_residual: float
    fit_design_rank: int

    def as_dict(self) -> dict:
        return {name: (value.tolist() if isinstance(value, np.ndarray) else value) for name, value in vars(self).items()}


def fit_compliance(forces_task_N, displacements_task_m, *, rcond=1e-12) -> ComplianceFit:
    forces = np.asarray(forces_task_N, dtype=float)
    displacements = np.asarray(displacements_task_m, dtype=float)
    if forces.ndim != 2 or forces.shape[1] != 3 or displacements.shape != forces.shape:
        raise ValueError("forces and displacements must both have shape (n, 3)")
    if forces.shape[0] < 3 or not np.all(np.isfinite(forces)) or not np.all(np.isfinite(displacements)):
        raise ValueError("at least three finite samples are required")
    coefficients, _, rank, _ = np.linalg.lstsq(forces, displacements, rcond=rcond)
    compliance = coefficients.T
    prediction = forces @ compliance.T
    residual = float(np.linalg.norm(displacements - prediction) / max(np.linalg.norm(displacements), 1e-15))
    stiffness = np.linalg.pinv(compliance, rcond=rcond)
    diagonal = np.diag(np.diag(compliance))
    coupling = float(np.linalg.norm(compliance - diagonal) / max(np.linalg.norm(diagonal), 1e-15))
    symmetric_compliance = 0.5 * (compliance + compliance.T)
    symmetric_stiffness = 0.5 * (stiffness + stiffness.T)
    return ComplianceFit(
        C_x_m_per_N=compliance,
        K_x_N_per_m=stiffness,
        compliance_eigenvalues_m_per_N=np.linalg.eigvalsh(symmetric_compliance),
        stiffness_eigenvalues_N_per_m=np.linalg.eigvalsh(symmetric_stiffness),
        condition_number=float(np.linalg.cond(compliance)),
        cross_axis_coupling_ratio=coupling,
        fit_relative_residual=residual,
        fit_design_rank=int(rank),
    )
