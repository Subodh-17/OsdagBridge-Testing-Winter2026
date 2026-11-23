**Base:** `Nidhikhare12/OsdagBridge`, branch `dev`, commit `d74f56d`
**Module:** `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py` (`add_dead_loads`, about lines 1328–1339) and `analyser.py` (`create_dead_load_combination`)

### What is wrong

The crash-barrier, railing and median load cases are created, but `create_sidl_combination()` is never called before `create_dead_load_combination()`. As a result, the barrier dead load does not enter the dead-load combination or the ULS combinations built from it, such as `BASIC_1`.

This is separate from #143, which is about *which* barrier load value is used. Here the barrier load case exists but never reaches the combinations.

### How to reproduce

Default 24 m design. Sum the support reactions of `BASIC_1` and compare them with the factored sum of the individual load cases.

- The barrier case on its own gives 196.2 kN of reaction. That figure is itself reduced by the line-load issue.
- Its contribution to `BASIC_1` is missing: the expected contribution is 264.9 kN at γ = 1.35, but none is found in the combination.

### Suggested fix (not tested)

```diff
     model.create_crash_barrier_load()
     model.create_railing_load()
     model.create_median_load()
+    model.create_sidl_combination(partial_safety_factor=1.0)
     model.create_dead_load_combination()
```

Afterwards, check that `create_dead_load_combination()` actually picks up the SIDL combination, and that the factor applied is the IRC:6 Table B.2 SIDL factor.
