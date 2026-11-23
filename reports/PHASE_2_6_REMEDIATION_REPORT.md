# PHASE 2.6 — Final Regression Suite Remediation Report

**Date:** 2026-11-16  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`, 100% clean)  
**Controlling Document:** `reports/PHASE_2_5_FINAL_INDEPENDENT_GATE_AUDIT.md` (Verdict: `CONDITIONAL ACCEPTANCE`)  
**Python Reference Environment:** `osdagbridge-py312` (Python 3.12.16 on Windows 11 AMD64)  
**Phase 2.6 Test Runner:** `testing\test_cases\baseline_regression\run_all_baseline_tests.py`  
**Phase 2.6 Sensitivity Matrix Runner:** `testing\test_cases\baseline_regression\run_sensitivity_matrix.py`  
**Evidence Root:** `testing\evidence\phase_2_6\`  

---

## 1. Executive Summary & Controlling Audit Absorption

In the Phase 2.5 independent gate audit (`reports/PHASE_2_5_FINAL_INDEPENDENT_GATE_AUDIT.md`), Claude issued a verdict of **CONDITIONAL ACCEPTANCE**. Nine tests were accepted (A01, D01, GEO-COUNT, CAP, CAD, A02, MAT, C01, B01), and three tests were formally blocked pending structural engineering design decisions (D02 under DEC-015, C02 under DEC-018, and GEO-SLAB under DEC-013). However, three tests were **REJECTED**:
1. `TC-REG-EQ-LOAD-CONSERVATION` (DEF-18) — rejected because equal lumping across girders, incorrect spacing, and barrier relocations could pass due to lack of per-barrier centroid checks and transverse tributary load share checks; self-weight was coupled to DEF-13; and literal fallbacks remained;
2. `TC-REG-RPT-EXEC-SUMMARY-STATUS` (DEF-08) — rejected because a candidate checking only G1 and G3 passed; DCR-only failure was untested; non-girder components were not checked; and the summary table was not synchronized with the injected fixture state;
3. `TC-REG-FS-CLEAN-WORKING-TREE` (DEF-10) — rejected because execution wrote `weather.sqlite` into the clean source tree; checks 4 and 5 were redundant path aliases; no real OS-level read-only permissions were enforced; and query outputs were unasserted.

In addition, the audit required:
- Correcting documented bounds and re-labeling deflection in `TC-REG-B01` as internal grillage model consistency;
- Adding a sign-reversal case and element-end envelope to `TC-REG-C01`;
- Deriving applied loads dynamically in `TC-REG-A02`;
- Accessing span via production key `geometry.span` in `TC-REG-MAT`;
- Programmatically generating evidence manifest hashes directly from disk bytes to eliminate any manual transcription errors.

In Phase 2.6, **every mandatory correction identified in §10 of the controlling audit has been resolved in full**. No application source files under `source/OsdagBridge` were modified; the application repository remains frozen at commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`.

### Key Verification Metrics

- **Baseline Regression Suite:**
  - Total Tests Registered: **15**
  - Baseline Failures (True Defects Detected): **11**
  - Passing Checks (Environment Verification): **1** (`TC-REG-CAD-EXPORT-VS-SCREENSHOT`)
  - Blocked (Formal Architectural/Spec Decisions Pending): **3** (`TC-REG-D02`, `TC-REG-C02`, `TC-REG-GEO-SLAB`)
  - Harness Exceptions / Errors: **0**
  - Manifest Alignment: **15 / 15 (100% Exact Match)**
  - Execution Duration: **49.84 s**
  - Summary Hash: `e2bd04069919b3ef826c0a766938fdb4ca9544d1b332f02707223aee41aae441` (12,732 B)
  - Process Exit Code: **0**

- **Sensitivity Matrix Suite (Candidate Mutation Gate):**
  - Total Tests Registered: **15**
  - Actionable Tests Verified: **12 / 12 (100.0%)**
  - Blocked Tests: **3 / 15** (`BLOCKED / NOT DEMONSTRATED`)
  - Overall Actionable Gate Status: **PASSED**
  - Execution Duration: **130.05 s**
  - Summary Hash: `fbaf7f119ec749da76146def6c69442ac927789c6e12883f315af429a9f80d6c` (25,929 B)
  - Process Exit Code: **0**

---

## 2. Technical Remediation of Priority 1–3 Tests

### 2.1 TC-REG-EQ-LOAD-CONSERVATION (DEF-18) — Static Equilibrium Overhaul

#### Defect Background
In `PlateGirderBridge.py` and `analyser.py`, finite element dead load distribution through `ospgrillage` causes severe load imbalance:
- Deck slab (DD) patch load distributes $+3.088\%$ excess force ($1314.375\text{ kN}$ vs $1275.000\text{ kN}$);
- Wearing course (DW) patch load distributes $+3.088\%$ excess force ($252.360\text{ kN}$ vs $244.800\text{ kN}$);
- Crash barrier line loads suffer a $-37.50\%$ shortfall ($196.200\text{ kN}$ vs $313.920\text{ kN}$), and barrier centroids shift longitudinally by $+0.750\text{ m}$.

#### Audit Deficiencies in Phase 2.5
The Phase 2.5 audit identified four flaws:
1. Only the combined barrier centroid was asserted ($\bar{z} = 4.25\text{ m}$), which passed when both barriers were shifted symmetrically or when equal loads were lumped on all girders;
2. No transverse load share distribution was asserted across longitudinal grillage lines;
3. Declared self-weight used hardcoded $78.5\text{ kN/m}^3$ instead of reading `material.girder.density`, coupling EQ to DEF-13;
4. Support reactions were summed with `abs()`, masking directional sign errors;
5. Literal fallbacks were used when keys were missing.

#### Phase 2.6 Remediation
1. **Individual Barrier Centroids:** Asserted separately for each barrier load group:
   - Left barrier: $W_{\text{left}} = 156.960\text{ kN} \pm 0.05\%$, centroid $\bar{x} = 12.000\text{ m} \pm 0.05\text{ m}$, $\bar{z} = 0.250\text{ m} \pm 0.05\text{ m}$.
   - Right barrier: $W_{\text{right}} = 156.960\text{ kN} \pm 0.05\%$, centroid $\bar{x} = 12.000\text{ m} \pm 0.05\text{ m}$, $\bar{z} = 8.250\text{ m} \pm 0.05\text{ m}$.
2. **Transverse Tributary Line Shares:**
   - **Deck Slab (DD) Patch Load:** Transverse tributary widths for the 6 grillage lines ($z = [0.0, 1.05, 3.183, 5.317, 7.45, 8.5]\text{ m}$) are $[0.525, 1.592, 2.133, 2.133, 1.592, 0.525]\text{ m}$, yielding theoretical shares of $[6.18\%, 18.73\%, 25.10\%, 25.10\%, 18.73\%, 6.18\%]$. The test asserts that interior lines receive $25.10\% \pm 1.5\%$ and outer lines receive $6.18\% \pm 1.5\%$.
   - **Crash Barrier Line Loads:** The left barrier at $z = 0.25\text{ m}$ lies between Line 0 ($z=0.0$) and Line 1 ($z=1.05$). By linear tributary lever-arm: Line 0 share is $(1.05 - 0.25) / 1.05 = 76.19\%$, Line 1 share is $0.25 / 1.05 = 23.81\%$, and Lines 2–5 receive $0.0\%$. Symmetrically, the right barrier at $z = 8.25\text{ m}$ allocates $23.81\%$ to Line 4 and $76.19\%$ to Line 5.
3. **Decoupled Self-Weight Derivation:** Declared self-weight is derived directly from `material.girder.density`:
   $$W_{SW} = \sum (A_g) \times \rho_{\text{girder}} \times L_{\text{span}}$$
   Reading `material.girder.density` decouples EQ from DEF-13, preventing false failures.
4. **Algebraic Support Reactions:** Summed without `abs()`:
   $$R_y = \sum_{\text{nodes}} -ops.\text{nodeReaction}(\text{node}, 2)$$
   Verifies that reaction forces genuinely oppose downward gravity loads.
5. **Elimination of Fallbacks:** Missing configuration keys raise explicit exceptions instead of defaulting to hardcoded constants.

#### Sensitivity Verification
- **Candidate (b):** Implements cell-intersection bilinear load distributor and line distributor matching tributary coordinates. Conserves 100% force, longitudinal centroids, per-barrier transverse centroids, and transverse line shares. Outcome: `PASS`.
- **Candidate (c):** Naively redistributes patch loads and lumps barrier loads uniformly across all 6 lines, violating per-barrier centroids ($z=4.25$ instead of $0.25$ and $8.25$) and transverse tributary line shares. Outcome: `BASELINE_FAIL`.
- Sensitivity Gate: **VERIFIED**.

---

### 2.2 TC-REG-RPT-EXEC-SUMMARY-STATUS (DEF-08) — Report Status Multi-Scenario Audit

#### Defect Background
`executive_summary.py` hardcodes `\noindent Girder design pass` in the executive summary narrative of the generated LaTeX report, regardless of whether individual girders or auxiliary bridge components fail.

#### Audit Deficiencies in Phase 2.5
1. Tested only G1 and G3 failure scenarios, permitting a candidate checking only G1 and G3 to pass;
2. DCR-only failure (`status == "PASS"`, `dcr = 1.30`) was omitted;
3. Non-girder components (Cross Bracing, End Diaphragm, Deck Slab) were not verified;
4. Tabular `Overall Design Status` was not verified against the narrative outcome in every scenario;
5. The fixture's `design_results["overall_status"]` was left stale, failing candidates that checked `overall_status`.

#### Phase 2.6 Remediation
1. **Girder-by-Girder Parameterized Loop:** Loops independently over every single girder G1 through G6. In each iteration, only that specific girder fails while all others pass.
2. **DCR-Only Failure Mode:** Tests a scenario where girder status string is erroneously `"PASS"` but utilization exceeds unity (`dcr = 1.30`). The test asserts that the report detects this as a failure.
3. **Auxiliary Component Scenarios:** Tests Cross Bracing (`CB`), End Diaphragm (`ED`), and Deck Slab (`Deck`) failure modes individually and simultaneously.
4. **Table and Narrative Consistency:** In every scenario, asserts agreement between:
   - Key Outcomes narrative text (`Girder design fail` vs `Girder design pass`);
   - Tabular `Overall Design Status` (`Fail` vs `Pass`).
5. **Synchronized Injected State:** In every test scenario, `out["design_results"]["overall_status"]` is synchronized with the scenario verdict (`"FAIL"` if any component fails, `"PASS"` if all pass). This ensures candidates checking `overall_status` pass legitimately on genuine fixes.

#### Sensitivity Verification
- **Candidate (b):** Evaluates all girders G1–G6, auxiliary components, and DCR thresholds, producing matching narrative and table outputs across all scenarios. Outcome: `PASS`.
- **Candidate (c):** Checks only G1 and G3, passing on G1 and G3 but failing when G2, G4, G5, or G6 fails. Outcome: `BASELINE_FAIL`.
- Sensitivity Gate: **VERIFIED**.

---

### 2.3 TC-REG-FS-CLEAN-WORKING-TREE (DEF-10) — Package Sandbox & Immutability Overhaul

#### Defect Background
In baseline `source/OsdagBridge`, `ui_fields_project_location.DB_PATH` is hardcoded relative to `__file__` inside the package tree (`src/osdagbridge/core/data/project_location/weather.sqlite`). In a clean installation where the database is missing, calling `@_with_db` creates an empty `weather.sqlite` directly inside the package source tree. Furthermore, the default `Database()` constructor creates unanchored `weather.sqlite` in `os.getcwd()`. In read-only deployments, write operations crash the application.

#### Audit Deficiencies in Phase 2.5
1. The test executed against the workspace repository, creating `weather.sqlite` in the clean source tree;
2. Checks 4 and 5 were redundant path aliases that did not test distinct behavioral properties;
3. No real OS-level read-only permissions were applied;
4. Query output validity was unasserted.

#### Phase 2.6 Remediation
1. **Isolated Package Copy Sandbox:** The test copies the entire package tree into a temporary directory (`tempfile.mkdtemp`), shielding `source/OsdagBridge` from any file creation or mutation.
2. **Recursive Tree Hashing & Detector Self-Test:**
   - Recursively hashes every file in the package sandbox before and after execution;
   - Performs a detector self-test by placing a probe file in `shapefiles/`, confirming the hashing mechanism detects unexpected filesystem modifications.
3. **Real OS Read-Only Permission Test:**
   - Applies true OS write denial without elevation: `icacls <dir> /deny Everyone:(OI)(CI)W` on Windows, `chmod -R 0555` on POSIX;
   - Verifies that baseline fails with permission denied / read-only error when attempting to create `weather.sqlite` in the package tree;
   - Verifies that candidate fixes handle read-only installations gracefully by redirecting writes to user app data.
4. **Query Assertions:** Asserts that `Database.get_states()` returns `>= 30` states and `Database.get_weather()` returns authentic meteorological data (`max_temp`, `min_temp`, `latitude`, `longitude`).
5. **Alias Removal:** Removed redundant path alias checks.

#### Sensitivity Verification
- **Candidate (b):** Anchors all database operations to user data directories, cleanly passing in read-only package copies without polluting the package tree. Outcome: `PASS`.
- **Candidate (c):** Leaves default `Database()` constructor unanchored, creating files in `os.getcwd()` and failing the sandbox immutability check. Outcome: `BASELINE_FAIL`.
- Sensitivity Gate: **VERIFIED**.

---

## 3. Targeted Refinements of Conditionally Accepted Tests

### 3.1 TC-REG-B01-SECTION-PROPERTY-SYNC (DEF-03)
- **Defect Background:** Solver grillage section properties remain unsynchronized with designed plate girder sections ($I_z$ error $\sim 7.40\%$, $A$ error $\sim 10.55\%$, depth mismatch $1340\text{ mm}$ vs $1342\text{ mm}$).
- **Audit Findings:** The deflection target ($7.218\text{ mm}$) was a calibrated grillage value tied to DEF-14 assumptions and edge beam modeling, while documented bounds conflated 4-girder central Courbon with eccentric loading.
- **Phase 2.6 Corrections:**
  - Corrected Courbon 6-line rigid factor documentation: rigid factor $0.3977 \implies 7.22\text{ mm}$ at outer edge girder, $0.3406 \implies 6.19\text{ mm}$ under load line.
  - Clarified 4-girder Courbon central bound ($4.541\text{ mm}$) vs eccentric bound ($12.71\text{ mm}$) and single-beam upper bound ($18.164\text{ mm}$).
  - Documented transformed concrete deck slab deflection ($6.501\text{ mm}$, DEF-14 / DEC-013).
  - Explicitly labeled the deflection check as an internal grillage model consistency target tied to 6-girder configuration and section synchronization.

### 3.2 TC-REG-C01-SECTIONAL-STRESS-RANGE (DEF-07)
- **Defect Background:** Baseline subtracts minimum static moment from maximum static moment, producing false cyclic stress ranges ($125.46\text{ MPa}$ envelope due to element-end $-Mz_i$ and $+Mz_j$ sign flipping).
- **Audit Findings:** The test lacked a sign-reversal case and element-end envelope check, allowing sign-inconsistent candidates to pass.
- **Phase 2.6 Corrections:**
  - Added a sign-reversal load case transition: hogging ($-500\text{ kNm}$) to sagging ($+1500\text{ kNm}$), producing a true stress range of $\Delta M = 2000\text{ kNm}$ and $\Delta \sigma = 125.45\text{ MPa}$.
  - Verified static zeroing ($\Delta \sigma = 0.00\text{ MPa}$) under static load cases.
  - Verified element-end sign consistency ($-Mz_i$ at end $i$, $+Mz_j$ at end $j$) across both ends.
  - Retained authentic application fatigue capacity ($92.491\text{ MPa}$) and DCR checks.

### 3.3 TC-REG-A02-ULS-COMBINATION-SUM (DEF-01 / DEF-02)
- **Phase 2.6 Corrections:**
  - Applied load resultant ($2802.70\text{ kN} \pm 0.05\%$) derived dynamically from component models rather than asserted as a magic literal.
  - Dynamic reaction superposition target ($2710.16\text{ kN} \pm 0.5\%$) asserted directly against individual load case sums.
  - Removed all silent literal fallbacks.

### 3.4 TC-REG-MAT-DENSITY-CONSISTENCY (DEF-13)
- **Phase 2.6 Corrections:**
  - Span is retrieved directly via production schema key `geometry.span`, with fallback to `bridge.span`.
  - Documented self-weight resultant: $169.82\text{ kN}$ at steel density $78.5\text{ kN/m}^3$ vs $151.43\text{ kN}$ at user density $70.0\text{ kN/m}^3$.

---

## 4. Preservation of Formal Architectural Blockers

The three formal engineering blockers identified in previous audits are preserved as **BLOCKED**:
1. **`TC-REG-D02-TEMPERATURE-PROPAGATION` (DEF-06):** Preserved as `BLOCKED` under **DEC-015**. IRC 6:2017 Cl. 215 thermal modeling (uniform temperature range vs non-linear vertical temperature gradient) remains undecided in project specifications.
2. **`TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS` (DEF-17):** Preserved as `BLOCKED` under **DEC-018**. IRC 6:2017 Cl. 204.6 fatigue vehicle moving load analysis pipeline is absent from `analyser.py` and requires architectural design.
3. **`TC-REG-GEO-SLAB-SECTION-PROPERTIES` (DEF-14):** Preserved as `BLOCKED` under **DEC-013**. Transverse concrete deck slab representation (`girder/2` vs transformed concrete section) remains undecided in specifications.

In `run_sensitivity_matrix.py`, all three blocked tests unconditionally return `BLOCKED / NOT DEMONSTRATED` and are excluded from the actionable verification count.

---

## 5. Evidence Manifest Cryptographic Integrity

To eliminate transcription errors flagged in Phase 2.5 §7:
1. All file sizes and SHA-256 hashes were generated programmatically from disk bytes via `hashlib.sha256()` into `testing/evidence/phase_2_6/hashes/manifest_hashes.json`.
2. `reports/PHASE_2_6_EVIDENCE_MANIFEST.md` was generated directly from `manifest_hashes.json`.
3. Key file hashes:
   - `testing/evidence/phase_2_6/hashes/manifest_hashes.json`: `7f20225cb604186f37120c2ee0e0ecff2409f33ab06b46f103528d51c2ad9dc6` (16,047 B)
   - `reports/PHASE_2_6_EVIDENCE_MANIFEST.md`: `ae7b6d90a9a7f8e1612efe04841feed28568f65fda248989974865431ca86fc1` (16,448 B)
   - `testing/test_cases/baseline_regression/run_all_baseline_tests.py`: `ef5a8151feead5a0b104bc8ec058a1f0c46e6147b2590df280f51f93a140dbf1` (109,078 B)
   - `testing/test_cases/baseline_regression/run_sensitivity_matrix.py`: `d24db269e7079f0097d823c3e4693cff395c0e612266b219042d7ee997c3da04` (48,898 B)
   - `baseline/phase_2_6_baseline_summary.json`: `e2bd04069919b3ef826c0a766938fdb4ca9544d1b332f02707223aee41aae441` (12,732 B)
   - `sensitivity/phase_2_6_sensitivity_matrix_summary.json`: `fbaf7f119ec749da76146def6c69442ac927789c6e12883f315af429a9f80d6c` (25,929 B)

---

## 6. Repository Integrity Verification

| Verification Item | Target Value | Observed Value | Status |
|:---|:---|:---|:---:|
| Git HEAD | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` | **VERIFIED** |
| Git Branch | `dev` | `dev` | **VERIFIED** |
| Working Tree Status | Clean (0 modified, 0 uncommitted) | Clean (0 modified, 0 uncommitted) | **VERIFIED** |
| Phase 3 Branch | None created | None created | **VERIFIED** |
| `Intg_osdag.sqlite` Hash | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` (270,336 B) | **VERIFIED** |
| `weather.sqlite` Hash | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` (180,224 B) | **VERIFIED** |

---

## 7. Conclusion & Next Steps

The Phase 2.6 remediation resolves every outstanding finding from Claude's Phase 2.5 independent audit. The regression suite is mathematically defensible, sensitive to subtle structural errors, completely isolated from the clean application source tree, and cryptographically verified.

**Strict Constraint Adherence:**
- Zero modifications to application source code under `source/OsdagBridge`;
- Zero git commits, pushes, merges, or branch creations;
- Phase 3 remains deferred pending independent audit review and acceptance.
