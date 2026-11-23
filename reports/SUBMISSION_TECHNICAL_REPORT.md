# OsdagBridge — Software Testing, Defect Verification and Targeted Remediation

**Composite Plate Girder Bridge module · FOSSEE Internship 2026 Screening Task Report**

| | |
|:--|:--|
| **Candidate** | Subodh Shivmurti Bansode · subodh171011@gmail.com · +91 8459475567 · GitHub `Subodh-17` |
| **Software under test** | OsdagBridge (`github.com/Nidhikhare12/OsdagBridge`), branch `dev`, base commit `d74f56d` |
| **Remediation branches** | `fix/phase-3-engineering-remediation` @ `f555075` (6 commits, Batches 1–3) → follow-up `fix/moving-load-mesh-mapping` @ `bbfe14c` (1 commit, §5.1). The packaged source is `bbfe14c`. All local: not pushed, no PR opened |
| **Environment** | Windows 11, Python 3.12 (conda `osdagbridge-py312`), PySide6, pythonocc-core (OCCT 8.0.1), OpenSeesPy 3.8 |
| **Codes referenced** | IRC:6-2017, IRC:22-2015, IRC:24-2010, IS 800:2007 |
| **Date** | 23 November 2026 |

## At a glance

| Evaluator question | Short answer | Where |
|:--|:--|:--|
| What was tested? | Environment and GUI start-up; one full end-to-end design run (24 m, 4 girders); a 15-test regression suite targeting specific calculation paths; load-distribution and load-factor acceptance suites | §1–§3 |
| Why does it matter? | Several defects change design-critical numbers: a buckling capacity overstated ≈3,384×, a barrier load reduced by 37.5 % in the FE model, load factors silently ignored | §4–§5 |
| How were defects reproduced? | Each defect has a scripted test with an independently derived (hand-calculated) oracle; logs are sealed with HMAC-SHA256 manifests | §3 |
| What was changed? | 5 defects fixed in 6 small commits (3 batches); 1 follow-up commit fixes a regression that Batch 2 introduced into moving-load analysis; 15 other register entries remain open, blocked or latent | §5 |
| What proves the fix? | The same tests flip from `BASELINE_FAIL` to `PASS`. Phase 3 suites: 58/58 (17 + 11 + 5 + 15 + 10). Governance: 27/27 on Windows. Two live GUI design runs on the final code | §5–§6 |
| What remains? | Open defects (e.g. barrier load missing from ULS combinations, section-property desync); no parametric sweep, custom-material or multi-run test campaign was completed | §7–§8 |
| How to reproduce? | Unzip the package, activate the conda environment, run `run_submission_tests.bat` | §9 |

## 1. Scope and approach

The work focused on **calculation correctness** of the composite plate girder module rather than broad UI coverage. It proceeded in three phases:

1. **Environment and baseline run.** Built a reproducible Python 3.12 environment, verified the PySide6 GUI starts with all docks, and executed one complete design (24 m span, 7.5 m carriageway, 0° skew, E 350 steel, M40 deck) through the real `CustomWindow` pipeline.
2. **Defect discovery and regression suite.** Read the analysis, design and reporting code against IRC/IS provisions, wrote a hand-calculated oracle for each suspected defect, and encoded each as a regression test that must fail on the unmodified code.
3. **Targeted remediation.** Fixed five defects with minimal commits and proved each fix with the same tests plus dedicated acceptance suites.

Before filing anything, the upstream tracker (40+ existing issues) was catalogued in `documentation/EXISTING_ISSUES_REGISTER.md` so that new findings could be de-duplicated against known issues (for example #19 and #20 on custom materials).

**Not covered.** The submission does not include a geometric parameter sweep, a custom-material state-retention test, a consecutive three-run GUI test, or BMD/SFD plot verification. These are listed as limitations in §8 rather than claimed.

## 2. End-to-end design run and 3D CAD check

The baseline run completed all 14 pipeline stages in 44.6 s. It produced:

- an output dictionary of about 1,066 top-level keys (3.3 MB snapshot);
- a generated LaTeX/PDF design report;
- a 3D CAD model.

The output dictionary's overall status was **FAIL** (maximum DCR 1.97). The generated report's status table correctly said "Fail", but the narrative directly below it still read "Girder design pass … Deck design pass". This contradiction led to DEF-08.

**3D CAD.** The CAD model was verified **programmatically**. An instrumented re-run found 83 OpenCASCADE shapes: girders, flanges, stiffeners, shear studs, cross-bracing, deck and two crash barriers. Their positions match the design: girders at ±1.05 m and ±3.15 m, barriers at ±4.2 m, length 24.0 m.

The on-screen OpenGL viewport could **not** be captured. `QWidget.grab()` returns a black viewport, as Figure 1 shows. No rendered bridge image is therefore claimed in this report; an offscreen OCC export of a test box (DEF-09 harness check) confirms only that the rendering pipeline works.

![GUI after the end-to-end design run](testing/evidence/phase_1d/01_end_to_end_design_full_window.png)

*Figure 1 – OsdagBridge after the automated 24 m design run. The inputs are locked after the run and the information overlay shows the generated geometry (8.40 m overall width, 2.10 m girder spacing). The CAD viewport is black because the window-grab method cannot capture the OpenGL surface, so this image does not show whether the model was drawn on screen.*

## 3. Regression test design and evidence

The baseline regression suite contains **15 tests** (`TC-REG-*`). On the unmodified code:

- **11** fail as expected, each reproducing a specific defect;
- **3** are blocked pending an engineering decision on the governing provision;
- **1** is a passing harness check.

Three practices make the results trustworthy:

- **Independent oracles.** Expected values are derived by hand from the code provisions, not by calling production helpers. For example, the IS 800 curve-c buckling value of 63.40 kN for the sealed stiffener geometry was calculated independently.
- **Tri-state sensitivity check.** Each actionable test was run against three variants of the code: the baseline (must fail), a correct candidate fix (must pass), and a plausible but wrong "naive" fix (must fail). All **12/12** actionable tests showed the required pattern, which shows the tests discriminate rather than pass trivially.
- **Tamper-evident evidence.** Every official run writes into a fresh directory with a SHA-256 manifest and an HMAC-SHA256 seal. 184 sealed files across six runs verify intact. A separate Windows run launched by the candidate (`bb29f1a4`) reproduced the baseline independently of the automated runs.

## 4. Defect register (20 entries)

| ID | Defect | Severity | Status |
|:--|:--|:--:|:--|
| DEF-01 | Component load factors ignored during grillage load compilation (`osp_grillage.py`) | Critical | **Fixed (Batch 3)** |
| DEF-02 | Crash-barrier SIDL not included in dead-load / ULS combinations | Critical | Open – fix proposed (§7) |
| DEF-03 | Grillage uses preliminary section, not the snapped (designed) plates | Critical | Open |
| DEF-05 | User wind speed / height / terrain not propagated (33 m/s fallback) | High | Open – already reported upstream (#86) |
| DEF-06 | Temperature load not modelled | High | Blocked – already reported upstream (#92) |
| DEF-07 | Fatigue stress range: member-end sign doubling and zero-clamping | Critical | Open – fix proposed (§7) |
| DEF-08 | Executive summary prints a hard-coded "pass" narrative | Medium | **Fixed (Batch 1)** – upstream #65 |
| DEF-09 | Offscreen OCC image export (harness check) | Low | Passes – not an application defect |
| DEF-10 | Weather database created inside the package tree / CWD at runtime | Medium | Open |
| DEF-11 | Designer counts slab-edge lines as girders (6 instead of 4) | Medium | **Fixed (Batch 1)** |
| DEF-12 | Bearing-stiffener web buckling capacity formula | Critical | **Fixed (Batch 1)** |
| DEF-13 | Hard-coded steel and concrete densities | Medium | Open – related upstream #41, #20 |
| DEF-14 | Transverse deck members given steel-girder properties | High | Blocked – modelling decision |
| DEF-17 | No fatigue-vehicle moving-load analysis | Critical | Blocked – provision decision |
| DEF-18 | FE grillage does not conserve applied line/patch loads | Critical | **Fixed (Batch 2)** |
| DEF-19a | Impact factor function always returns 0.10 (truthy string test) | High | Open (latent) |
| DEF-19b | Lane reduction factors indexed per vehicle, not per lane count | Medium | Open (latent) |
| DEF-19c | Impact factor in analysis differs from the one printed in the report | Medium | Open (latent) |
| DEF-20 | Wearing course applied over full deck width, not carriageway | Medium | Open |
| DEF-LATENT-ZP | Transverse coordinate index in `load.py` line-load interpolation | Medium | Open (latent) |

Four entries (DEF-05, -06, -08, -13) overlap issues already on the upstream tracker. They are kept here for their reproduction tests, not claimed as new findings. Full source locations, mechanisms and oracles are in `reports/phase_3/PHASE_3_DEFECT_TRACEABILITY_MATRIX_REV3.md`.

## 5. Remediated defects: baseline, change and proof

| Defect | Baseline evidence (sealed log) | Change (commit) | Proof after fix |
|:--|:--|:--|:--|
| **DEF-12** stiffener buckling | Capacity **214,533.2 kN** vs IS 800 oracle **63.40 kN** (squash limit 1,918.8 kN) | Web-strip radius of gyration r = t<sub>w</sub>/√12, KL = 0.7d, IS 800 buckling curve c (`418fd75`) | Same test: **63.40 kN → PASS**; hand fixture 118.79 kN reproduced |
| **DEF-08** report status | Hard-coded "pass" text; disagreed with actual status in **64 of 74** scenarios | Status derived from component DCRs (`12493c9`) | All 74 scenarios agree → **PASS** |
| **DEF-11** girder count | Designer reports **6** girders for a 4-girder bridge | Count bound to physical girders (`eaba076`) | Count 4 = 4 → **PASS** |
| **DEF-18** load conservation | 313.92 kN barrier load applied as 196.2 kN (**−117.72 kN, −37.5 %**); first end bay dropped; patch corner cells over-counted | Line load = mean intensity × segment length, centroid along the segment, z-index fix, out-of-mesh loads raise an error (`34cd4bf`); corner de-duplication, no list mutation while iterating (`9e0b588`) | Batch 2 suite **17/17**, incl. full-bridge barrier 313.920 kN in equilibrium; residuals ≤ 1.2×10<sup>−10</sup> N |
| **DEF-01** load factors | `TC-REG-A01`: factored/unfactored force ratio **1.00000** (expected 1.35000) | Load factor from `LoadCase.add_load()` carried into point, line, patch and nodal distribution (`f555075`) | Ratio **1.35000 → PASS**; 9/9 factor oracles (incl. mixed, zero, negative and compounded factors) |

**Why these matter.**

- **DEF-12.** With a stiffener specified, the code reported the web-buckling check as passing ("stiffener not needed") on the basis of a capacity about 3,384× too high, so a needed stiffener could be judged unnecessary.
- **DEF-18.** The finite-element model under-loaded the girders: the barrier load, an edge bay and the patch corners were all mishandled.
- **DEF-01.** Partial safety factors of 1.35–1.75 were applied as 1.0, so the affected factored effects were 26–43 % low.

The three defects fixed in Batch 1 were re-run after Batches 2 and 3 and still pass.

### 5.1 Regression introduced by Batch 2, and its fix (separate follow-up commit)

**The regression.** Batch 2 (`34cd4bf`) made any point load outside the mesh raise `ValueError`, instead of being silently dropped. The moving-load generator legitimately places vehicle axles off the deck: vehicles entering or leaving the span, and axles beyond skewed abutments. So on `f555075` **every full design run stopped in `add_live_loads()`**. This was reproduced for the default 24 m, 0° bridge.

The Batch 2 and 3 acceptance suites test the load-distribution functions in isolation, so they did not catch it. It was found on 23 Nov 2026 when the design was re-run in the GUI.

**The fix** is commit `bbfe14c` on `fix/moving-load-mesh-mapping`, parent `f555075`. It is not part of the three formal batches. It changes three things:

- **Vehicle point loads.** During load distribution, vehicle point loads outside the deck contribute zero force, since off-bridge axles do not load the superstructure. Direct calls and line-load points still raise an error.
- **Boundary tolerance.** A 10<sup>−9</sup> tolerance lets points on a cell boundary map to that cell.
- **Point types.** Point, tuple, list and array inputs are all accepted when mapping a point to grid nodes.

**Verification.**

- **New suite.** `test_moving_load_mesh_mapping.py` passes 10/10. It covers fail-closed behaviour by default, interior force conservation, boundary points, live-load generation for 24 m/0°, 30 m/10°, 25 m/10° with median and footpath, and 25 m/−10°, and a vehicle partly on the deck, where only the on-deck axle is applied.
- **Same suite on `f555075`.** 8 of its 10 tests error.
- **Existing suites.** All earlier suites pass on `bbfe14c`.
- **Live GUI runs** on Windows, which completed design:
  - 30 m, 7.5 m carriageway, 10° skew;
  - 25 m, 7.5 m carriageway, 10° skew, with median and single footpath.

  The screenshots are in `evidence/screenshots/live_gui_verification/`. They show the locked inputs and the geometry overlay. As in Figure 1, the window capture shows the OpenGL viewport black, so no rendered model image is claimed.

**Trade-off.** An out-of-mesh *point* load that is not from a vehicle is now also dropped without an error during distribution. This is listed in §8.

## 6. Verification results

| Suite | What it checks | Result |
|:--|:--|:--|
| Batch 1 regression tests | DEF-12, DEF-08, DEF-11 (`TC-REG-*`) | 3/3 PASS, re-confirmed after Batch 3 |
| `test_batch_2_comprehensive.py` | Force, centroid and reaction equilibrium for uniform, partial, trapezoidal, skewed and zero-crossing line loads; patch loads; out-of-mesh handling; full-bridge barrier | **17/17 OK** |
| `test_batch_3_factor_scaling.py` | Factor propagation for every load type, nine analytical oracles, no in-place mutation | **15/15 OK** |
| `test_batch_2_line_loads.py`, `test_batch_2_patch_loads.py` | Focused line and patch cases (overlap in scope with the comprehensive suite) | **11/11**, **5/5 OK** |
| `test_moving_load_mesh_mapping.py` | §5.1 regression fix | **10/10 OK** |
| `test_evidence_governance.py` | Write guards for protected evidence, seal and manifest tamper detection, database and trust-ledger hashes | **27/27 OK** (Windows) |

**Clean-room re-check (23 Nov 2026).** The submission ZIP (source `bbfe14c`) was extracted into an empty directory and the suites were run from it with a fresh user profile, on Linux with Python 3.12 and the project dependencies installed. Imports were confirmed to resolve to the packaged source:

- Phase 3 suites: **58/58**. The Batch 3 suite also re-runs the three Batch 1 regression tests, which all pass.
- Governance: **24 passed, 3 skipped**. The skipped tests are Windows-only process-containment checks.

The 27/27 governance figure is from Windows.

Note that the Batch 3 suite rewrites its three logs in `testing/evidence/phase_3/batch_3/` on each run (new timestamp, same result).

These suites verify the five fixed defects and the evidence controls. They are **not** a full verification of the application.

## 7. Proposed fixes for open defects (not applied, not tested)

**DEF-02 – include barrier SIDL in combinations** (`plategirderbridge.py`, after the barrier/railing/median loads are created):

```diff
     model.create_crash_barrier_load()
     model.create_railing_load()
     model.create_median_load()
+    model.create_sidl_combination(partial_safety_factor=1.0)
     model.create_dead_load_combination()
```

**DEF-07 – fatigue stress range** (`designer.py`): remove the zero-clamp so the range is `max − min` of the section moment. The member-end sign convention must be harmonised first, otherwise the range is still doubled.

**DEF-19a – impact factor** (`irc6_2017.py`): the condition tests a constant string, which is always true. It should test the vehicle type that is passed in. The correct impact provision for steel-composite decks requires an engineering decision before a test oracle can be fixed.

## 8. Limitations

- **Open defects.** 15 of the 20 register entries remain open, blocked or latent. The software should not be used for design until at least DEF-02, DEF-03 and DEF-19 are resolved.
- **Test coverage.** No parametric sweep (span, width, skew), custom-material state-retention test, consecutive three-run GUI test, or BMD/SFD verification was completed. Upstream issues #19 and #20 already report custom-material persistence problems.
- **CAD image capture.** CAD output was checked programmatically, not visually captured (§2, §5.1).
- **Out-of-mesh point loads.** Since `bbfe14c`, out-of-mesh point loads are dropped during distribution, which is correct for off-bridge vehicle axles. A misplaced non-vehicle point load would also be dropped without an error (§5.1).
- **Integration testing.** The Batch 2 regression shows that the function-level acceptance suites do not exercise the full design pipeline. Full-pipeline checks are limited to the live GUI runs and the live-load generation tests in §5.1.
- **Upstream contribution.** Issue drafts for the new findings are in `submission/GITHUB_ISSUE_DRAFTS.md`; at the time of writing they had not been filed. All fixes exist only on the local branch; no pull request has been opened.
- **Single-run baseline.** The end-to-end baseline is one design case (24 m, 0° skew). The DEF-18 equilibrium suite includes skewed-line fixtures, but the full design pipeline was not re-run on skewed bridges.

## 9. How to reproduce

The ZIP contains the application source at `bbfe14c` (the Phase 3 commits plus the §5.1 follow-up), all test suites, sealed evidence and this report. It needs a Python 3.12 environment with OsdagBridge's dependencies. The upstream list is `source/OsdagBridge/environment.yml`; the exact `osdagbridge-py312` setup used here is in `documentation/PHASE_1C_ENVIRONMENT_MIGRATION_REPORT.md`. From the package root:

```bat
conda activate osdagbridge-py312
run_submission_tests.bat
```

The script runs the following, each of which can also be run alone from the package root:

1. `python testing\test_cases\baseline_regression\test_evidence_governance.py`
2. `python -m unittest testing\test_cases\phase_3\test_batch_2_comprehensive.py`
3. `python -m unittest testing\test_cases\phase_3\test_batch_3_factor_scaling.py`
4. `python -m unittest testing\test_cases\phase_3\test_moving_load_mesh_mapping.py`

To open the GUI on the packaged source: `cd source\OsdagBridge\src` then `python -m osdagbridge.desktop`.

**Evidence index.**

| What | Location in the ZIP |
|:--|:--|
| Baseline logs | `testing/evidence/phase_2_13/baseline/` |
| Post-fix logs | `testing/evidence/phase_3/` |
| Live GUI runs on the final code | `evidence/screenshots/live_gui_verification/` |
| Fix patches (7) | `patches/` in the GitHub repository |
| End-to-end run | `testing/evidence/phase_1d/` (input `.osi`/YAML, output dictionary, design report PDF) |
| Batch closure records | `reports/phase_3/` |
| Sample project | `submission/osi/sample_24m_composite_plate_girder.osi` |
