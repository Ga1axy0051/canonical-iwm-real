# Real-robot bring-up

1. Integrate one backend using `RobotAdapter`; separately implement measured
   state, target state, stop, watchdog, and protective-stop reporting.
2. Calibrate payload/CoM and semantic `T_eef_tcp` using the actual installed
   tool. The historical 80 mm simulator offset is not a hardware calibration.
3. Define and physically mark the right-handed task frame. Validate axes with
   read-only measurements.
4. Validate free-space wrench baseline and then a technician-applied light push.
5. Run zero action, then 0.25 mm, 0.5 mm, and 1 mm free-space tests, one stage at
   a time. Review requested vs actual/orthogonal motion and joint state logs.
6. Identify compliance from paired known-force/known-displacement samples.
7. Consider a very light single-axis contact only after the safety checklist and
   native stop path have passed.

`--execute` grants only the named script operation. It never grants permission
to weaken safety limits, create autonomous hard contact, or run insertion.
