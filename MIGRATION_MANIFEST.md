# Migration manifest and audit

The complete `canonical_iwm/` tree was inventoried: 609 files (84 Python, 206
JSON, 109 logs, 66 Markdown, 37 figures, 101 bytecode files, and supporting
files). All Python files were classified by dependency/import and purpose; the
frozen schema, required reports, controllers, tests, and relevant Phase 1/1.5,
2C, and 2D sources were read in detail. Phase 2E–2I were inspected for reusable
symbols and numerical utilities, not copied as experiment directories.

## Audit table

| Original file/category | Purpose | Real-robot reusable? | Decision | Reason / destination |
|---|---|---:|---|---|
| `configs/schema_v1.json` | Frozen branch schema | Yes | KEEP | Byte-for-byte at `configs/schema_v1.json`; SHA-256 retained |
| `reports/canonical_serialization_v1.md` | Exact vector/frame semantics | Yes | REFACTOR | Semantics in README, docs, and `serialization.py` |
| `reports/canonical_serialization_v1.json` | Machine-readable ordering | Yes | KEEP | Byte-for-byte at `configs/canonical_serialization_v1.json` |
| `controllers/canonical_serialization_v1.py` | Vector serialization and principal rotvec | Yes | REFACTOR | Split across `serialization.py` and `transforms.py` |
| `tests/test_canonical_serialization_v1.py` | Schema hash/order/evidence tests | Yes | REFACTOR | Portable hash/order/round-trip tests; raw evidence dependency removed |
| `controllers/canonical_tcp_controller.py` | Full-pose target, local IK/FK/Jacobian guards | Partly | REFACTOR | Generic action, transform, locality, and controller modules; Lula removed |
| `tests/test_canonical_tcp_controller.py` | Task delta, TCP inverse, task-direction tests | Yes | REFACTOR | `test_actions.py`, `test_frames.py`, `test_locality.py` |
| `reports/ur5_controller_contract_v2.json` | UR5 simulator controller evidence | Concept only | REFACTOR | Frame/action/locality lessons documented; asset/gains/thresholds dropped |
| `reports/franka_controller_contract_v2.json` | Franka equilibrium-target evidence | Concept only | REFACTOR | Configurable `equilibrium_preserving_target`; hardware recalibration warning |
| `reports/canonical_iwm_phase1_ur5_control.md` | Initial UR5 controller evidence | Concept only | REFACTOR | Historical lesson captured in adapter/controller docs |
| `reports/canonical_iwm_phase1_5_contract_audit.md` | Canonical contract/serialization audit | Yes | REFACTOR | Frozen semantics and validation tests |
| `reports/canonical_iwm_phase1_5_repaired.md` | Repaired canonical UR5 evidence | Concept only | REFACTOR | Full-pose/task-direction/local branch ideas only |
| `scripts/phase1_5_contract_audit.py` | Simulator canonical state/wrench audit | Partly | REIMPLEMENT | Simulator access dropped; generic frame/wrench/logging code added |
| `reports/canonical_iwm_phase2c_controller_repair.md` | Franka control repair | Concept only | REFACTOR | Measured-vs-equilibrium target semantics retained |
| `scripts/franka_phase2c_equilibrium_repair.py` | Simulator Franka repair experiment | No as code | DROP | Isaac/asset/drive operations are not a real backend |
| `reports/canonical_iwm_phase2d_force_canonicalization.md` | Wrench sign/frame/reference validation | Yes | REIMPLEMENT | `wrench.py`, tests, and manual validation script |
| `scripts/analyze_phase2d_force_canonicalization.py` | Force canonicalization analysis | Partly | REIMPLEMENT | Small explicit wrench math replaces report-bound analysis |
| `scripts/cross_robot_task_compliance.py` | Fit `delta_x = C_x F` and `pinv(C_x)` | Yes, fit only | REFACTOR | Offline `compliance.py`; Isaac force application removed |
| `reports/phase2d_task_compliance*.json` | Large simulation compliance evidence | No | DROP | Not hardware calibration and too large for toolkit |
| `scripts/phase2d_isolated_branching.py` | Simulator branch execution | No | DROP | Isaac contact/action stack not promoted |
| `scripts/phase2d_isolated_contact_sweep.py` | Simulator contact sweeps | No | DROP | No automatic hardware contact sweep |
| `phase2e/locality/run_l0_l3_tournament.py` | Locality/FK coherence experiments | Concept only | REFACTOR | Generic calibrated locality validator; no fixed thresholds |
| `phase2e/branching/*` | Loaded-contact branches | No | DROP | Simulation experiment stack |
| `phase2e/replay/*` | Simulator replay/root-cause lanes | No | DROP | No real-robot dependency |
| `phase2f/controllers/c5_c6_free_space_identification.py` | Compliance/stiffness identification | Partly | REFACTOR | Offline fitting and guarded manual protocol; drive tuning dropped |
| `phase2f/controllers/c5_c6_c5_r4_v0_v1.py` | Simulator controller comparison | No | DROP | Contact/controller tournament not hardware-ready |
| `phase2f/semantics/*` | Simulator action-semantics screen | Concept only | REFACTOR | Task-space action tests retained; raw runs dropped |
| `phase2g/g5/bounded_velocity_qp.py` | Bounded velocity QP prototype | Not yet | DROP | Phase 2G contact path unresolved; no hardware controller promotion |
| `phase2g/g6/numerical_audit_runtime.py` | Numerical safety diagnostics | Concept only | REFACTOR | Finite/bounds checks incorporated without simulator runtime |
| `phase2h/h3/audit_fk_target_mismatch.py` | FK/target mismatch diagnosis | Concept only | REFACTOR | Measured/target separation and FK residual checks retained |
| `phase2h/h4/run_velocity_drive_g4.py` | Simulator hybrid velocity drive | No | DROP | PhysX/drive/contact-specific and unresolved |
| `phase2i/ik/run_local_differential_actions.py` | Local differential IK diagnostic | Concept only | REFACTOR | Bounded residual and local direction validation only |
| `phase2i/i3`–`i7` | Impact/contact/drive diagnostics | No | DROP | Explicitly diagnostic, not validated for real control |
| `reports/canonical_iwm_status.md` | Authoritative research status | Yes as warning | REFACTOR | Exclusions recorded in sim-to-real notes/status |
| `robots/`, `envs/`, `tasks/`, `models/` | Simulation/research stack | No | DROP | Learned model and simulator runtime intentionally absent |

## Major exclusions

- Phase 12 and all later unrelated experiment material
- raw JSON evidence, large logs, and figures
- GPU/explicit PhysX experiments and server-only launch scripts
- Phase 2G/2H/2I impact, mounted-tool collision, and post-impact debugging
- USD assets and simulator asset URLs
- Isaac Sim, OmniGibson, `omni`, `pxr`, and PhysX-specific APIs
- learned models, checkpoints, training data, and ordinal-transfer experiments

No original source or evidence file was modified or deleted.
