# Extraction report

## Source and scope

- Original source: `open_horizon_pilot/canonical_iwm/` (left unchanged)
- Source tree inventoried: 609 files
- Python source files classified: 84 (18,300 lines total)
- Detailed evidence reviewed: frozen schema/serialization, both v2 controller
  contracts, canonical status, controllers/tests, and relevant Phase 1/1.5/2C/2D
  code; Phase 2E–2I inspected only for generic utilities and exclusion decisions

## Migration result

- Byte-preserved files: 2 (`schema_v1.json` and canonical serialization JSON;
  frozen schema hash retained)
- Robot-independent package modules: 17, including robot adapters
- Operator scripts: 7 plus one private script helper
- Core test files: 7
- Hardware/safety/calibration documents: 5 plus README, status, and manifest

Refactored capabilities include SE(3)/rotation-vector transforms, task/TCP frame
mapping, canonical serialization/state/action types, full wrench rotation and
reference-point shift, locality/FK/Jacobian-direction checks, bounded residuals,
measured-vs-target controller semantics, offline compliance/stiffness fitting,
JSONL logging, and dry-run-first staged scripts.

Excluded categories: Phase 12, raw JSON evidence, figures, large logs, USD
assets, server launch scripts, Isaac/OmniGibson/PhysX dependencies, GPU PhysX
experiments, and Phase 2G/2H/2I collision/impact/post-impact debugging. No world
model, training data, or production contact controller was migrated.

## Validation

- Tests: **18 passed** (`pytest -q`)
- Mock free-space dry run: **PASS** (`MOCK_DRY_RUN_OK`)
- All other operator scripts: mock/dry-run smoke checked
- Python compile check: **PASS**
- Forbidden simulator imports in `src/canonical_iwm/`: none
- Real hardware motion executed: **NO**

## Adapter readiness and TODO

| Robot | Readiness | Remaining work |
|---|---|---|
| UR5 | SKELETON / NOT TESTED | Select ROS/ROS2 or RTDE backend; implement state, watchdog, protective stop, motion/stop, Jacobian and wrench; calibrate TCP/payload/limits/compliance |
| Franka Panda | SKELETON / NOT TESTED | Select libfranka or ROS backend; explicitly expose equilibrium target; validate stop/watchdog and recalibrate equilibrium-offset strategy, TCP/payload/limits/compliance |
| xArm6 | SKELETON / NOT TESTED | Approve UFactory SDK or ROS backend; implement and validate all capability paths; calibrate TCP/payload/limits/compliance |

## GitHub status

**LOCAL_ONLY.** The system had neither `git` nor `gh`; non-root package copies
were used to initialize the repository, rename its branch to `main`, and stage
all files. No Git author name/email is configured and GitHub CLI is not
authenticated, so no identity was invented and no commit/repository/push was
performed. No repository URL exists yet. With normal installed tools, run:

```bash
cd <path-to>/canonical-iwm-real
git config user.name '<your-name>'
git config user.email '<your-email>'
git commit -m "feat: extract real-robot canonical IWM toolkit"
gh auth login
gh auth status
gh repo view canonical-iwm-real
gh repo create canonical-iwm-real --private --source=. --remote=origin --push
```

Run the create command only if `gh repo view` confirms the name does not exist.
If it exists and is unrelated, use a safe private alternate such as
`canonical-iwm-real-robot`. Never use `--public` or force-push.
