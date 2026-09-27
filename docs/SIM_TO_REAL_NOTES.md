# Simulation-to-real notes

Reusable concepts are canonical task/TCP frames, task-space action semantics,
wrench reference-point math, FK/Jacobian/locality validation, measured-vs-target
controller state, bounded residual correction, compliance identification, and
canonical logging.

Not promoted to hardware code: explicit GPU PhysX setup, mounted-tool collision
debugging, impact dynamics, post-impact joint velocity models, Phase 2G/2H/2I
contact diagnostics, simulator drive gains, USD assets, or contact controllers.

The historical 80 mm EEF-to-TCP offsets and locality values are evidence from
specific simulated assets. They are examples only. Hardware requires new TCP,
payload/CoM, joint/Cartesian limit, watchdog, stiffness/compliance, and sensor
frame calibration.
