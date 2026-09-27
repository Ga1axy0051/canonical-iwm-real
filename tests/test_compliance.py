import numpy as np

from canonical_iwm.compliance import fit_compliance


def test_compliance_fit_recovers_matrix():
    compliance = np.array([[1e-5, 2e-6, 0], [0, 2e-5, 1e-6], [0, 0, 3e-5]])
    forces = np.vstack([np.eye(3), -np.eye(3), 2 * np.eye(3), -2 * np.eye(3)])
    fit = fit_compliance(forces, forces @ compliance.T)
    np.testing.assert_allclose(fit.C_x_m_per_N, compliance, atol=1e-15)
    np.testing.assert_allclose(fit.K_x_N_per_m, np.linalg.inv(compliance), rtol=1e-12, atol=1e-9)
    assert fit.fit_relative_residual < 1e-12 and fit.fit_design_rank == 3
