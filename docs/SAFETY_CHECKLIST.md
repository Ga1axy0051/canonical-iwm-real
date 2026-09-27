# Hardware safety checklist

Before any live command, verify every item physically and in software:

- [ ] E-stop is physically reachable.
- [ ] Protective stop is verified.
- [ ] Robot speed is reduced.
- [ ] Workspace is cleared.
- [ ] No person is inside the robot workspace.
- [ ] Semantic TCP is calibrated.
- [ ] Payload and center of mass are configured.
- [ ] Tool is mechanically secured.
- [ ] Joint limits are confirmed for the installed system.
- [ ] Software stop is tested.
- [ ] Connection watchdog is tested.
- [ ] Force/torque limits are configured.
- [ ] Logging is active.
- [ ] Dry-run is complete.
- [ ] Free-space 0.25 mm test passed.
- [ ] Free-space 0.5 mm test passed.
- [ ] Free-space 1 mm test passed.
- [ ] Only then is light contact being considered.

Required progression:

```text
free space
  -> light manual wrench validation
  -> very light wall contact
  -> repeatability
  -> compliance identification
  -> only later insertion
```

Any unexpected motion, stale state, watchdog loss, excessive force/torque,
velocity, joint displacement, or protective-stop indication requires immediate
stop and investigation. Never disable or bypass native safety systems.
