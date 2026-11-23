# Phase 2.2 Baseline Regression Validation Report

**Workspace:** `F:\FOSSEE internship`  
**Repository Baseline:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (branch `dev`)  
**Environment:** `osdagbridge-py312` (Python 3.12.16, OpenCASCADE 7.9.0, OpenSeesPy 3.7.0.1)  
**Execution Timestamp:** 2026-11-16T12:10:37 UTC  
**Execution Mode:** Baseline (`--mode baseline`)  
**Process Exit Code:** `0` (Baseline Manifest Alignment: 14 / 14 Matches)  

---

## 1. Executive Summary

This report documents the official baseline revalidation of the repaired Phase 2.2 regression test harness against the frozen upstream repository `source/OsdagBridge` at commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`.

Under the Phase 2.2 test harness, all tests exercise authentic application entry points, execute finite element grillage analyses in OpenSees, and evaluate code-traceable engineering oracles.

### Primary Results Summary:
- **Total Tests Executed:** 14
- **Baseline Failures (Confirmed Defects):** 11
- **Blocked Tests (Formal Specification Blockers):** 2 (`TC-REG-D02` pending DEC-015, `TC-REG-GEO-SLAB` pending DEC-013)
- **Passing Tests (Environment/Harness Check):** 1 (`TC-REG-CAD-EXPORT-VS-SCREENSHOT`)
- **Manifest Alignment:** **14 / 14 exact matches** (100.0%)
- **Harness Exit Code:** `0` (indicating 100% agreement with `BASELINE_MANIFEST`)
- **Working Tree Integrity:** 100% clean (`source/OsdagBridge` unmodified)

---

## 2. Environment & Provenance Verification

| Property | Value | Audit Verification |
|---|---|---|
| **Python Version** | `3.12.16` | Verified via active conda environment `osdagbridge-py312` |
| **Python Executable** | `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe` | Isolated Miniconda environment |
| **Host OS** | `Windows 11 Build 26300` | 64-bit native Windows |
| **Repository Commit** | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` | Read dynamically from `.git/HEAD` and `.git/refs/heads/dev` |
| **Concrete Module Path** | `.../osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py` | Verified concrete import path |
| **Runner Self SHA-256** | `b817861e662c57e6aa50c918ee8cede79dee0e188995ab3f2f12da3ee7b6852c` | Recorded at start of run |
| **Input Fixture SHA-256** | `31ae62dc08a0de7797aa4ca6451a178fd46cc66bba4c00f7414021336fb10191` | Cryptographic hard-abort match |
| **Output Fixture SHA-256** | `429a3198fc93c157a5bd5ee13c74b95612c3410d35a7be1f246867167991a5ab` | Cryptographic hard-abort match |

---

## 3. Detailed Test-by-Test Baseline Results

| # | Test ID | Defect ID | Baseline Status | Expected Status | Duration (s) | Failure / Observation Reason |
|---|---|---|---|---|---|---|
| 1 | `TC-REG-A01-FACTOR-SCALING` | DEF-01 (Upstream) | **BASELINE_FAIL** | BASELINE_FAIL | 0.144 | ospgrillage ignored load_factor 1.35; force ratio is 1.00000 (expected 1.35000). |
| 2 | `TC-REG-B01-SECTION-PROPERTY-SYNC` | DEF-03 | **BASELINE_FAIL** | BASELINE_FAIL | 0.055 | Dimensions inconsistent: D=1340.0mm != dw(1306.0) + 2*tf(36.0) = 1342.0mm; Solver girder sections retain preliminary sizing: Iz gap ~7.40%, A gap ~10.55%; Analysed deflection 7.82mm deviates from snapped target 7.22mm |
| 3 | `TC-REG-C01-SECTIONAL-STRESS-RANGE` | DEF-07 | **BASELINE_FAIL** | BASELINE_FAIL | 0.085 | Static load case produces false cyclic stress ranges: Path (a) envelope = 125.46 MPa; Path (b) per-LC = 62.73 MPa. Expected 0.0 MPa. |
| 4 | `TC-REG-A02-ULS-COMBINATION-SUM` | DEF-01 / DEF-02 | **BASELINE_FAIL** | BASELINE_FAIL | 24.354 | Solver ignored ULS factors: shears match un-factored 1.0DL+1.0DW (err=72392.5N, vs unfactored=1.16e-07N); Total reaction 1736.6kN does not match factored target 2932.3kN; Crash barrier load omitted from BASIC_1 |
| 5 | `TC-REG-D01-WIND-SPEED-PROPAGATION` | DEF-05 | **BASELINE_FAIL** | BASELINE_FAIL | 0.383 | Wind arguments fell back to defaults (speed=33.0 vs 47.0, height=10.0 vs 15.0, barrier=0.0 vs 1.1, railing=0.0 vs 1.2), yielding Pz = 463.7 N/m2 instead of authentic 1039.6 N/m2. |
| 6 | `TC-REG-D02-TEMPERATURE-PROPAGATION` | DEF-06 | **BLOCKED** | BLOCKED | 0.244 | DEC-015 Pending: Thermal load modeling (IRC 6 Cl. 215) is undecided in project specifications. add_temperature_load() reads unpopulated 'temperature_load_kN_m2' and leaves temperature_load_case as None. |
| 7 | `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS` | DEF-17 | **BASELINE_FAIL** | BASELINE_FAIL | 7.099 | Moving vehicle cases generated 2 (Class A and 70R only); IRC 6 Cl. 204.6 fatigue vehicle missing. |
| 8 | `TC-REG-RPT-EXEC-SUMMARY-STATUS` | DEF-08 | **BASELINE_FAIL** | BASELINE_FAIL | 0.239 | executive_summary() emits literal '\noindent Girder design pass' unconditionally under Key Design Outcomes Summary despite a failing fatigue check (DCR = 1.9746). |
| 9 | `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` | DEF-11 | **BASELINE_FAIL** | BASELINE_FAIL | 0.237 | designer.py:401 sets n_girders = geom.n_l (6), incorrectly counting 2 slab overhang edge lines as structural girders for a 4-girder bridge. |
| 10 | `TC-REG-GEO-SLAB-SECTION-PROPERTIES` | DEF-14 | **BLOCKED** | BLOCKED | 0.004 | DEC-013 Pending: Transverse deck slab representation is undecided in project documentation. Baseline assigns girder/2 (Iz=0.00367 m4), requiring engineering sign-off. |
| 11 | `TC-REG-CAP-STIFFENER-BUCKLING` | DEF-12 | **BASELINE_FAIL** | BASELINE_FAIL | 0.240 | Geometry 1 (Baseline Snapped): capacity 134083.2kN (fails oracle 63.4kN, squash=1918.8kN); Geometry 2 (Alternate Section): capacity 231365.0kN (fails oracle 158.5kN, squash=1909.1kN). |
| 12 | `TC-REG-MAT-DENSITY-CONSISTENCY` | DEF-13 | **BASELINE_FAIL** | BASELINE_FAIL | 2.989 | Self-weight resultant (169.8 kN) matches hardcoded 78.5 kN/m3 (169.8 kN) instead of user-specified density 70.0 kN/m3 (151.4 kN). |
| 13 | `TC-REG-FS-CLEAN-WORKING-TREE` | DEF-10 | **BASELINE_FAIL** | BASELINE_FAIL | 8.060 | Production DB_PATH targets package tree causing package mutation; Database() default constructor creates unanchored weather.sqlite in cwd. |
| 14 | `TC-REG-CAD-EXPORT-VS-SCREENSHOT` | DEF-09 | **PASS** | PASS | 2.775 | Native OCC offscreen Viewer3d.ExportToImage renders opaque 3D geometry (std=20.0, 3 colors). |

---

## 4. Manifest Comparison: Baseline vs Remediation Target

To prevent conflating known defects with blockers, the test runner enforces a two-manifest architecture:

```
+------------------------------------+-------------------+----------------------+
| Test Identifier                    | Baseline Manifest | Remediation Manifest |
+------------------------------------+-------------------+----------------------+
| TC-REG-A01-FACTOR-SCALING          | BASELINE_FAIL     | PASS                 |
| TC-REG-B01-SECTION-PROPERTY-SYNC   | BASELINE_FAIL     | PASS                 |
| TC-REG-C01-SECTIONAL-STRESS-RANGE  | BASELINE_FAIL     | PASS                 |
| TC-REG-A02-ULS-COMBINATION-SUM     | BASELINE_FAIL     | PASS                 |
| TC-REG-D01-WIND-SPEED-PROPAGATION  | BASELINE_FAIL     | PASS                 |
| TC-REG-D02-TEMPERATURE-PROPAGATION | BLOCKED (DEC-015) | BLOCKED (DEC-015)    |
| TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS| BASELINE_FAIL     | PASS                 |
| TC-REG-RPT-EXEC-SUMMARY-STATUS     | BASELINE_FAIL     | PASS                 |
| TC-REG-GEO-GIRDER-COUNT-ALIGNMENT  | BASELINE_FAIL     | PASS                 |
| TC-REG-GEO-SLAB-SECTION-PROPERTIES | BLOCKED (DEC-013) | BLOCKED (DEC-013)    |
| TC-REG-CAP-STIFFENER-BUCKLING      | BASELINE_FAIL     | PASS                 |
| TC-REG-MAT-DENSITY-CONSISTENCY     | BASELINE_FAIL     | PASS                 |
| TC-REG-FS-CLEAN-WORKING-TREE       | BASELINE_FAIL     | PASS                 |
| TC-REG-CAD-EXPORT-VS-SCREENSHOT    | PASS              | PASS                 |
+------------------------------------+-------------------+----------------------+
```

- In **Baseline Mode** (`--mode baseline`), the harness asserts exact identity with `BASELINE_MANIFEST` (11 BASELINE_FAIL, 2 BLOCKED, 1 PASS). Exit code `0` verifies 100% defect capture.
- In **Remediation Mode** (`--mode remediation`), the harness will assert identity with `REMEDIATION_MANIFEST` (12 PASS, 2 BLOCKED), exiting `0` only when all 12 actionable defects are genuinely resolved.

---

## 5. Baseline Evidence Archival

All evidence generated during this baseline run is preserved outside the source repository:
- Summary JSON: `testing/evidence/phase_2_2/baseline/phase_2_2_baseline_summary.json`
- Exit Code: `testing/evidence/phase_2_2/baseline/baseline_exit_code.txt`
- 14 Discrete Test Logs: `testing/evidence/phase_2_2/baseline/TC-REG-*.log`
