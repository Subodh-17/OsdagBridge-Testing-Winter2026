# Phase 2.8 Final Independent Gate Audit: OsdagBridge Regression Harness (audit only)

| | |
|---|---|
| **Date** | 2026-11-17 |
| **Auditor** | independent QA and structural-verification audit (same auditor as Phases 2.3–2.7) |
| **Repository** | `F:\FOSSEE internship\source\OsdagBridge`, branch `dev`, frozen at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` |
| **Controlling document** | `reports\PHASE_2_7_FINAL_INDEPENDENT_GATE_AUDIT.md` (SHA-256 `a857e6bf…`, unchanged since issue) |

**Material examined**

- **Runners:**
  - `run_all_baseline_tests.py`: 131,324 B, SHA-256 `26c2e9e4…`.
  - `run_sensitivity_matrix.py`: 50,365 B, SHA-256 `35689903…`.
  - Both were read for every changed test. Each function was diffed against Phase 2.7: changed are `test_*` for B01, C01, A02, EQ, RPT and FS, plus `mut_b_fs` and `mut_c_fs`.
- **Reports:** all four Phase 2.8 reports.
- **Preservation records:** the three files under `phase_2_8\preservation\`.
- **Evidence:** all 92 files in `phase_2_8\`, and every manifest of Phases 2.5, 2.6 and 2.7.

**Method**

- Every experiment ran in disposable cloud clones of `d74f56d`:
  - `/tmp/ws28`, run as root;
  - `/tmp/ws28u`, run as an unprivileged user (uid 30033).
- On your machine I only read files and recomputed hashes. The single exception is saving this report.

**Labels:** CONFIRMED means independently reproduced; CONTRADICTED means the evidence disagrees with the claim.

---

## 1. Executive decision

**CONDITIONAL ACCEPTANCE. The harness is substantially improved, but it is not yet independently trustworthy as a whole.**

| Status | Tests |
|---|---|
| ACCEPTED | A01, D01, GEO-COUNT, CAP, CAD (environment/export check only) |
| ACCEPTED WITH LIMITATIONS | **EQ (DEF-18)**, RPT, A02, C01, B01, MAT |
| **REJECTED** | **FS-CLEAN-WORKING-TREE (DEF-10)** |
| BLOCKED | D02 (DEC-015), C02 (DEC-018 / DEF-17), GEO-SLAB (DEC-013) |

The claim that "every finding … has been comprehensively remediated" and that "all historical evidence remains intact" is **CONTRADICTED**:

1. **Evidence (§3).**
   - **New overwrite.** Phase 2.7 evidence was overwritten again during Phase 2.8: `phase_2_7/candidates/tc_reg_eq_load_conservation.log` at 06:15:49 UTC. That was 4.5 minutes *after* the new preservation manifest was written, so the preservation manifest no longer matches disk.
   - **Recoverable logs left marked as overwritten.** Six of the eight "overwritten" Phase 2.6 logs are byte-recoverable, but the forensic report leaves them classed as overwritten.
   - **Inaccurate reporting.** The remediation report names the wrong files and the wrong time window, and quotes summary hashes and sizes that don't exist. The Markdown evidence manifest lists **0 files**.
   - **Missing logs.** The live console transcripts claimed for this phase do not exist.
2. **FS (§4.2)** still misses:
   - writes to `src/` and to the repository root made through package-relative paths;
   - writes into nested working-directory folders;
   - writes from detached child processes, which landed in the real package tree after the test reported PASS.
3. **EQ (§4.1)** now has an independent spatial (distribution) oracle. Its load *magnitudes and positions* are still copied from the application's own load objects, so for those it compares the application against itself.

Phase 3 is **not authorised**. No application source change is recommended.

---

## 2. Reproduction results

**Environment:** a clean clone of `d74f56d` (source aggregate identical to your `src/`, §6) with byte-identical runners. Linux, Python 3.12.16, numpy 2.5.4, openseespy 3.8.0.0, pythonocc-core 8.0.1.2, Xvfb.

**Runs.** Output was captured live, with stdout and stderr redirected separately (`/tmp/p25/live28/`):

| Run | Exit | Duration | stdout / stderr | Result |
|---|---|---|---|---|
| Baseline, root | **1** | 48.4 s | 21,565 / 0 B, no tracebacks | 14/15 manifest match. **FS = BLOCKED** (POSIX root, DEC-023); all other statuses identical to your Windows results. |
| Sensitivity, root | **1** | 29.0 s | 44,765 / 0 B | 11 VERIFIED, 3 BLOCKED, **FS UNVERIFIED** (a/b/c all BLOCKED) |
| FS alone, non-root POSIX (private `TMPDIR`) | — | 1.5 / 1.9 / 0.5 s | — | (a) BASELINE_FAIL, (b) **PASS**, (c) BASELINE_FAIL. Genuine `chmod` read-only. |

- **Exit code 1 as root is correct behaviour.** The root run cannot verify FS, and the harness now says so instead of reporting PASS (Phase 2.7 finding resolved).
- **Your Windows evidence** shows FS (a) BASELINE_FAIL with a genuine `icacls` denial ("Read-only execution denied write … OperationalError"), and (b) PASS.
- **Windows and non-root POSIX behaviour agree.**
- **Side note (environmental, not a harness defect):** a stale root-owned `/tmp/OsdagBridgeAppData` makes candidate (b) fail as non-root with "target directory is not writable". The harness correctly reports that as a failure.
- **Every result comes from the current runners.**
  - The baseline summary's `runner_self_hash` (`26c2e9e4…`) equals the current runner.
  - Per-test outcome lines match your logs.
  - Example values: EQ DD +39.4 kN; A02 1,736.6 vs 2,710.16 kN; C01 three-state range 125.458 MPa; B01 7.239 mm.
- **No artefacts** were created in either clone's repository during the shipped runs (inventory diff empty).

---

## 3. Evidence preservation: forensic verification

### 3.1 The eight Phase 2.6 files

Rehashed against `phase_2_6/hashes/manifest_hashes.json`, which is still the only record of the originals:

| File (phase_2_6/) | Original SHA-256 (2.6 manifest) | Current on disk | Classification |
|---|---|---|---|
| `baseline/tc_reg_eq_load_conservation.log` | `054876a7…` (4,247 B) | `cdcda56b…` (4,359 B) | **Irretrievably lost.** No byte-identical copy exists anywhere under `testing/evidence`. The status, reason excerpt and timestamp survive only in `phase_2_6_baseline_summary.json`. |
| `baseline/tc_reg_fs_clean_working_tree.log` | `cd1e28d7…` (2,028 B) | `ab1ecb30…` (1,987 B) | **Irretrievably lost** (same as above) |
| `candidates/tc_reg_a02_uls_combination_sum.log` | `6b69e668…` | `0fecf557…` | **Original bytes recoverable and verified:** identical to the intact `…_c_naive.log` |
| `candidates/tc_reg_b01_section_property_sync.log` | `8fd719ce…` | `7fe4da64…` | **Recoverable:** = `…_c_naive.log` |
| `candidates/tc_reg_c01_sectional_stress_range.log` | `ff2e7b53…` | `83de7855…` | **Recoverable:** = `…_c_naive.log` |
| `candidates/tc_reg_eq_load_conservation.log` | `0d490c37…` | `40092b80…` | **Recoverable:** = `…_c_naive.log` |
| `candidates/tc_reg_fs_clean_working_tree.log` | `ab361431…` | `c966fe8e…` | **Recoverable:** = `…_c_naive.log` |
| `candidates/tc_reg_rpt_exec_summary_status.log` | `89d3466d…` | `d7ca1f68…` | **Recoverable:** = `…_c_naive.log` |

- **Why six are recoverable.** In each run the unsuffixed candidate log is a copy of the last condition (c). The Phase 2.6 manifest records identical hashes for each pair, and the six `_c_naive.log` files are intact. The forensic report missed this and leaves these six classed as "OVERWRITTEN (Intermediate)".
- **Nothing has been restored on disk.** All eight files still hold the overwritten bytes.
- **`phase_2_6_discrepancy_manifest.json`:**
  - Original and current hashes are correct for all 8 entries (CONFIRMED).
  - **`manifest_size` is `null` for every entry**, even though the Phase 2.6 manifest records each size (4,247 B, 2,028 B, …).
- **`manifest_preservation.json`:**
  - 428 entries, covering Phase 1D and 2.3–2.7 in full.
  - It catalogues **current bytes**, including the eight overwritten Phase 2.6 files, so it is **not** a record of recovered historical content.
  - It already disagrees with disk for one file (§3.2).
- **Remediation report §2.1 is CONTRADICTED on three points:**
  1. It names the eight files as the EQ/FS `_a/_b/_c` logs, which are actually intact.
  2. It dates the overwrite to "16:35–16:47 UTC"; the files' internal timestamps show 18:32:39–18:38:43 UTC.
  3. It says the other files are "100% intact", which §3.2 disproves.

### 3.2 Phase 2.7 evidence was modified during Phase 2.8

- **Phase 2.7:** **92 of 93** files match `phase_2_7/hashes/manifest_hashes.json`. The exception is `candidates/tc_reg_eq_load_conservation.log`:
  - recorded: `9ee3fe4b…`, 4,168 B;
  - now: `8476f053…`, 3,917 B, mtime and internal timestamp 2026-11-17 06:15:49 UTC.
  - The original bytes remain recoverable from `phase_2_7/candidates/tc_reg_eq_load_conservation_c_naive.log`, by the same pairing rule as §3.1.
  - The overwrite happened after `manifest_preservation.json` was written (06:11:10), so that manifest also mismatches here.
  - The claimed scratch isolation (`testing/evidence/scratch/`) exists but is empty. The runners still default to the official `phase_2_8` directories, so nothing in the code enforces scratch isolation.
- **Phases 2.5, 2.4, 2.3 and 1D:** unchanged.

### 3.3 Phase 2.8 evidence itself

| Item | Finding | Status |
|---|---|---|
| Files | 92 = 91 inventoried + `hashes/manifest_hashes.json` | CONFIRMED |
| JSON manifest | 91 of 91 SHA-256 values and sizes match disk | CONFIRMED |
| Markdown manifest (`PHASE_2_8_EVIDENCE_MANIFEST.md`) | The 8 infrastructure rows are correct (runners, fixtures, databases, both manifests). **Sections 2–5 say "Total files: 0" and list nothing.** | **Incomplete** |
| Remediation report hashes | Baseline summary is reported as 13,091 B / `c4b12384…`; actual is **13,686 B / `3fda14ad…`**. Sensitivity summary is reported as 26,532 B / `0229c1ff…`; actual is **27,680 B / `eee98691…`**. Both reported sizes equal the Phase 2.7 sizes. `baseline_exit_code.txt` is reported as `4b227777…`, which is the SHA-256 of the character "4"; the file contains "0" (`5feceb66…`). | **CONTRADICTED** |
| Console and exit codes | **No `console_output.txt`, `stdout`, `stderr` or `shell_exit_code.txt` exists in Phase 2.8.** Only script-written exit codes are present: baseline "0", sensitivity "0\r\n". | **MISSING** (claimed "live stdout/stderr logging") |
| Timeline (UTC) | Runners edited 06:30:34 / 06:30:49. Baseline 06:32:17–06:32:36. Sensitivity and candidates 06:32:50–06:34:06. Manifest 06:34:35. Reports 06:35–06:37. Preservation files 06:10–06:11. Baseline and candidate directories are separate. | CONFIRMED |

---

## 4. Findings by workstream

### 4.1 EQ / DEF-18: **ACCEPTED WITH LIMITATIONS**

**Expected spatial vector (runner lines 1105–1154).** The test builds:

- **Longitudinal tributary lengths** from the actual mesh `nox`: Δx/2 at the end nodes, (xⱼ₊₁ − xⱼ₋₁)/2 in between. For L = 24 m at 1.5 m spacing that is 0.75 m at each end node and 1.5 m elsewhere, summing to 24 m.
- **Transverse tributary widths** from `noz` = [0, 1.05, 3.183, 5.317, 7.45, 8.5]. That gives 0.525, 1.592, 2.133, 2.133, 1.592, 0.525 m, i.e. shares of 6.18, 18.73, 25.10, 25.10, 18.73, 6.18%.
- **Barrier split:** the lever rule between the two bounding lines, giving 76.19 / 23.81% for z = 0.25 m.

**How the vector is checked:**
- Expected nodal force: F = P · (L<sub>trib,x</sub>/L) · share<sub>z</sub>.
- It is compared with the actual nodal commands as Σ|F<sub>act</sub> − F<sub>exp</sub>| / P ≤ 0.5%, for DD, DW and each barrier line.
- For a uniform load this is exactly the consistent nodal vector. That shape is derived **independently from the mesh geometry**. CONFIRMED.

**Probes (`/tmp/p25/probe28a.py`, monkeypatched distributor in the disposable clone):**

| # | Mutation | Result |
|---|---|---|
| E0 | Correct consistent distributor | PASS |
| E1 / E2 | All load on supports / all load at midspan | FAIL ✓ (vector error) |
| E3 | Equal nodal lumping | FAIL ✓ (DD and DW 46.7%) |
| **E4** | **Equal along-span lumping, end nodes not halved** | **FAIL ✓** (was PASS in Phase 2.7) |
| **E5** | **25/50/25 three-point lumping** | **FAIL ✓** (was PASS) |
| **E6 / E7 / E21** | **DW only: equal lumping / supports only / midspan only** | **FAIL ✓** (46.7%, 187.5%, 187.5%) |
| E8 | Barrier +1 node along the span (wrong centroid) | FAIL ✓ (dx +1.453 m) |
| E9 / E10 / E11 | Barrier inboard 0.30 m / ±10% force / 70/30 split | FAIL ✓ |
| E22 | DD transverse shares swapped symmetrically (total and centroid kept) | FAIL ✓ (74.9%) |
| E13 / E14 | DEF-13 fix via module constant / via input density (70) | PASS / **PASS** ✓ (the E14 false failure is resolved) |
| E15–E18 | Spans 30, 36, **12**, 15 m | PASS ✓ (the E17 false failure is resolved) |
| **E12** | Application *defines* the barrier load object at z = 1.00 / 7.50 m | **PASS** ✗ |
| **E19** | Application's DD intensity 20% low (load object) | **PASS** ✗ |
| **E20** | Production constant set to 120 kN/m³: actual and expected move together | **PASS** ✗ |

**Where the expected magnitudes come from**

- **Circular.** Every declared magnitude and position is read from the application's own load objects:
  - SW: `p1.p` × line length;
  - DD and DW: patch extent × `p1.p`;
  - barriers: `p1.p` and `p1.z`.
  - This is "derived from applied load objects" in the report's words: the application output, not the input geometry and material properties.
  - So any error in *what* the application applies (density, deck intensity, barrier position) passes EQ by construction (E12, E19, E20).
- **Scope boundary.**
  - EQ is now a trustworthy test of **distribution and conservation relative to the applied load definitions**.
  - It is not an independent physical oracle for the load magnitudes. MAT covers only girder density.
- **SW** is checked for total force and centroid only, with no nodal vector.

---

### 4.2 FS / DEF-10: **REJECTED**

**Lifecycle (runner lines 2061–2322):**
1. Snapshot the full repository (`source/OsdagBridge`, recursive) and the top level of the working directory.
2. Copy the package to `sandbox_dir/osdagbridge`; write the candidate patch as `sitecustomize.py`.
3. Run production `get_state_list` / `get_weather` with `subprocess.run` and `PYTHONPATH=sandbox_dir`, asserting the results.
4. Run a read-only copy the same way (Windows `icacls` deny; recursive `chmod` for non-root POSIX; **BLOCKED** for root).
5. `time.sleep(0.1)`, then re-snapshot.

**Probes (`/tmp/p25/probe28c*.py`).** Each is candidate (b) plus extra `sitecustomize` code, run as **non-root POSIX** in `/tmp/ws28u`:

| # | Write path (from inside production) | Result | Detected? |
|---|---|---|---|
| G0 | none (candidate b) | PASS | — |
| G1 | nested package directory `…/project_location/shapefiles/_c.tmp` | FAIL | ✓ |
| G6 | `atexit` write into the package after queries return | FAIL | ✓ |
| G8 | non-daemon timer write into the package 0.5 s later | FAIL | ✓ |
| G4 | absolute path into the **real** repository `src/` | FAIL | ✓ but **the file remained in the repository** (detected after pollution) |
| **G2** | `<package>/../weather.sqlite` (= `src/` in a real install) | **PASS** | **✗** |
| **G3** | `<package>/../../.osdag_cache/…` (= repository root in a real install) | **PASS** | **✗** |
| **G5** | nested folder of the working directory (`testing/_cwd_nested.sqlite`) | **PASS**, file left behind | **✗** |
| **G7** | detached child process writes into the **real package** 1 s after the subprocess exits | **PASS**, file appeared in the real package afterwards | **✗** |

**Why these escape:**

| Cause | Effect |
|---|---|
| The sandbox puts the package at `sandbox_dir/osdagbridge`, not `…/src/osdagbridge` | Package-relative parent paths resolve into the unmonitored temporary directory, which is deleted afterwards (G2, G3) |
| The working directory is snapshotted at top level only | Nested writes are missed (G5) |
| The boundary is `subprocess.run` return plus 0.1 s | Grandchild processes are not tracked or awaited (G7) |
| Candidate writes to absolute real-repository paths actually execute | They are detected only after the repository is modified (G4) |

**Credited:**
- Production code really runs from the sandbox.
- Read-only is genuinely exercised for candidates:
  - **Windows** (`icacls`, your evidence);
  - **non-root POSIX** (`chmod`, my run);
  - **root** is reported as **BLOCKED**, not PASS (CONFIRMED).
- The shipped suite writes nothing into the repository.

---

### 4.3 RPT / DEF-08: **ACCEPTED WITH LIMITATIONS**

**What the test asserts (lines 1488–1802):**
- **40 scenarios:** 1 all-pass and 39 single or multi-failure. The single failures are:
  - 24 girder cases (G1–G6 × moment, shear, stiffener, fatigue);
  - 4 DCR-only cases (G4);
  - cross-bracing P1/M1, M2, M3 and P2/M1;
  - end-diaphragm M1, M2, M3;
  - deck moment-only, shear-only and both.
- **Unaffected components** are asserted to remain PASS in every failure scenario.
- **The fixture keeps `overall_status = "PASS"`** throughout.

**Probes (`/tmp/p25/probe28b.py`, source variants of `mut_b_rpt`):**

| Detected (FAIL) ✓ | Not detected (PASS) ✗ |
|---|---|
| ignores stiffener buckling; moment checked only on G1 | DCR-only check applied **only to G4** (R13) |
| CB first member only / last member only / ignores panel P2 / first panel only | deck limit `≥ 1.0` instead of `> 1.0` (no boundary case, R17) |
| ED first member only / last member only / ignores M3 / ignored entirely | |
| deck moment-only; DCR only for shear | |
| **table copied from `overall_status`**; **any failure marks every component FAIL** | |

**Verdict:**
- The final status is now shown to be **derived from component results**: copying the mutable field fails, and fail-all fails. CONFIRMED.
- **Remaining:**
  - DCR-only failures are exercised on one girder only.
  - There is no DCR = 1.0 boundary case.
  - The check names are synthetic.
  - The candidate post-processes the generated text instead of changing the report code path.

---

### 4.4 A02 / DEF-01, DEF-02: **ACCEPTED WITH LIMITATIONS**

**The applied resultant now logged is 2,711.74 kN, not 2,762.14 kN.** Recomputed from what the code reads (lines 784–800):

| Component | Formula | Value |
|---|---|---|
| SW | 0.0901376 × 76.4 × 24 | 165.28 kN |
| DD | 24 × **W<sub>deck</sub> = 8.50** (`bgm.w`, i.e. the model width, **an application output**; input `overall_bridge_width` = 8.4) × 0.25 × 24.5 (input) | 1,249.50 kN |
| DW | 24 × **W<sub>cw</sub> = 7.50** (input `geometry.carriageway_width`) × 0.050 × 24 | 216.00 kN |
| CB | 2 × 24 × 6.54 (production helpers) | 313.92 kN |
| Resultant | 1.35 × 1,728.70 + 1.75 × 216.00 = 2,333.74 + 378.00 | **2,711.74 kN** ✓ |

- **It is still not asserted.** `applied_resultant_ok` does not enter `combination_ok` (line 158 of the function). It is labelled `[INFORMATIONAL]`.
- Probe A1: with the application's steel density set to 120 kN/m³, superposition becomes 2,831.36 kN against 2,711.74 "applied", and the test still **PASSes**.
- **Its closeness to the 2,710.16 kN superposition (0.06%) is coincidental.** The application applies a DW patch 8.5 m wide (252.36 kN), deck concrete at 25 kN/m³ (not the input 24.5), and only 196.2 kN of barrier load (DEF-18). These differences offset each other.
- **Could it be asserted?** Only once the width and density used for each load are pinned to specific input keys. Asserting it today would mix A02 (combination factors) with load-definition and DEF-18 effects. The suite does neither; the earlier requirement remains open.
- **Reaction superposition** (2,710.16 kN ± 0.5%), Vy/Mz factoring and barrier presence remain the mandatory gates.
  - The test function is changed only in its applied-resultant section, and `mut_b_a02` is unchanged.
  - Factor, missing-component and duplicate-component errors in BASIC_1 break the superposition identity (established in Phases 2.4–2.7).
  - Defective reactions are not used as an oracle for the applied resultant.

---

### 4.5 C01 / DEF-07: **ACCEPTED WITH LIMITATIONS**

**What is new:**
- The three-state history +1,500 → −500 → +200 kNm: Δσ = 2,000/15.94 = 125.45 MPa, against |last − first| = 1,300 kNm, which gives 81.55 MPa.
- The shared-node check now uses the **production extractor's** static output (`range_s_env`). It is no longer test-local, though it duplicates the static check.
- All cases pass through the real `_extract_demands_from_analysis_results` (synthetic xarray input).

**Probes (`/tmp/p25/probe28e.py`):**

| Mutation | Result |
|---|---|
| Signed last − first; \|last − first\|; abs-moment range; peak amplitude; raw-sign shared-node envelope | FAIL ✓ |
| One element end not negated; both ends reversed; reversed element order | **PASS** (per-end ranges are sign-invariant; not exercised) |
| **Range from the first two load cases only** | **PASS ✗** (the extremes sit in LC1 and LC2, so LC3 never matters) |

**Capacity, recomputed:**
- f<sub>f</sub> = 92 × (5×10⁶ / 2×10⁶)^(1/3) = **124.863 MPa**.
- f<sub>fd</sub> = 124.863 / 1.35 = **92.491 MPa**, with N<sub>sc</sub> = 2,000,000 used (log).
- DCR = 125.458 / 92.491 = **1.3564** (log 1.3564; the expected value 1.3563 uses 125.450).
- The DCR is still computed in the test, and the stress histories are synthetic.

---

### 4.6 B01 / DEF-03: **ACCEPTED WITH LIMITATIONS**

**Probes (`/tmp/p25/probe28f.py`):**

| Condition | Result |
|---|---|
| Candidate (b) | PASS |
| I<sub>z</sub> × 2 and A × 2 (oversized) | **FAIL ✓** (was PASS in Phase 2.7) |
| I<sub>z</sub> +0.4% | PASS (within ±0.5%) |
| I<sub>z</sub> +0.6% | FAIL ✓ |
| A −0.6% | FAIL ✓ |
| I<sub>z</sub> = 0.00779 with deflection passing | FAIL ✓ |
| D inconsistent by 2 mm | FAIL ✓ |
| Transformed slab (deflection 6.501 mm, out of band) | PASS (informational) ✓ |
| **J × 10** | **PASS** (J and I<sub>y</sub> are not checked) |

**Are the expected values justified?** I recomputed both from the snapped plates (b<sub>f</sub> 410, t<sub>f</sub> 18, d<sub>w</sub> 1,304, t<sub>w</sub> 8 mm):
- A = 2 × 0.41 × 0.018 + 1.304 × 0.008 = **0.025192 m²**.
- I<sub>z</sub> = 1.47826×10⁻³ + 2 × (1.99×10⁻⁷ + 0.00738 × 0.661²) = **7.9276×10⁻³ m⁴**.

Both are correct, but they are **literals for this fixture** (lines 351–352), not derived at run time from the inputs. The deflection target remains model-consistency only.

---

### 4.7 Other tests

- **Unchanged:** A01, D01, GEO-COUNT, CAP, CAD and MAT test functions and their candidates are identical to Phase 2.7 (function diff), so their verdicts stand.
- **CAD** remains an environment/export check only.
- **D02, C02 and GEO-SLAB** are unconditionally BLOCKED and not counted.

---

## 5. Mutation sensitivity matrix (independent)

| Test | Shipped (a) / (b) / (c) | Independent mutants detected | Missed or false failures | Verdict |
|---|---|---|---|---|
| EQ | FAIL / PASS / FAIL | E1–E11, E21, E22; no false failures at 12–36 m or for either DEF-13 fix | E12, E19, E20 (load magnitude/position copied from application) | ACCEPTED WITH LIMITATIONS |
| FS | FAIL / PASS / FAIL (Windows, non-root POSIX); BLOCKED as root | G1, G4 (after pollution), G6, G8 | **G2, G3, G5, G7** | **REJECTED** |
| RPT | FAIL / PASS / FAIL | 15 of 17 variants, including copy-status and fail-all | DCR-only applied to G4 only; ≥ 1.0 boundary | ACCEPTED WITH LIMITATIONS |
| A02 | FAIL / PASS / FAIL | factor, missing and duplicate components via identity | applied resultant not gated (A1 PASS) | ACCEPTED WITH LIMITATIONS |
| C01 | FAIL / PASS / FAIL | order-dependent, abs, amplitude, raw-sign node envelope | first-two-LC-only; per-end sign flips | ACCEPTED WITH LIMITATIONS |
| B01 | FAIL / PASS / FAIL | oversize, undersize ±0.6%, D, hidden-section | J / I<sub>y</sub> errors | ACCEPTED WITH LIMITATIONS |
| A01, D01, GEO-COUNT, CAP, MAT | FAIL / PASS / FAIL | as in earlier phases | as recorded | as in §1 |
| CAD | PASS / PASS / FAIL | blank image | not the application path | ACCEPTED (environment) |
| D02, C02, GEO-SLAB | BLOCKED | — | — | BLOCKED |

"12/12 VERIFIED" reproduces on Windows. As root it is 11 VERIFIED plus FS UNVERIFIED, which is correct.

It demonstrates only that each shipped candidate (b) passes and each candidate (c) fails. It does not establish engineering correctness.

---

## 6. Repository and database integrity

| Check | Result |
|---|---|
| `.git/HEAD` | `ref: refs/heads/dev` → `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` |
| Branches | only `dev` |
| Locks and index | no `*.lock` files; `.git/index` mtime 2026-11-15 12:26:18 UTC (unchanged). The `.git` directory mtime is 06:38:46 UTC (a Git command was run after the reports), with no lasting effect. |
| Tracked source | 282 files under `src/` (CR-normalised). Aggregate SHA-256 `7c9294813b58fb84ecd965643daec240276747d1788b13187c0e0f46c52b024c` on your machine and in a clean checkout: **identical** |
| Untracked or changed since 2026-11-15 14:30 | only the pre-existing untracked `weather.sqlite` (mtime 2026-11-16 05:48:51) |
| Databases | `Intg_osdag.sqlite` `25f978575be64a11…` and `weather.sqlite` `1d767658099bef9d…`: both unchanged |
| This audit | No evidence, report, source or database file on your machine was modified. Both disposable clones were left identical to `d74f56d`; every probe-created file was removed and checked. |

**`source\OsdagBridge` is unchanged on `dev` at the frozen commit.**

---

## 7. Remaining limitations

1. **Evidence:**
   - Phase 2.7 has been overwritten once more.
   - The preservation manifest is already stale.
   - Six recoverable Phase 2.6 originals are neither restored nor recognised.
   - The two Phase 2.6 baseline logs are lost.
   - The Markdown manifest is empty.
   - The remediation report's hashes and sizes are wrong.
   - No live console capture exists.
   - Scratch isolation is not enforced by the code.
2. **FS:**
   - The sandbox layout differs from a real install (G2, G3).
   - The working-directory snapshot is not recursive (G5).
   - Child processes are not awaited (G7).
   - Absolute-path writes are detected only after they pollute the repository.
3. **EQ:** load magnitudes and positions are taken from the application's own load objects (E12, E19, E20). SW has no nodal-vector check.
4. **A02:**
   - The applied resultant is not asserted.
   - The deck width comes from model output.
   - The DW width and deck density differ from what the application applies.
5. **C01:**
   - The extremes sit in the first two states.
   - Per-end sign convention is not exercised.
   - The data is synthetic, and the DCR is computed in the test.
6. **RPT:** DCR-only failures cover one girder; there is no boundary case; the check names are synthetic.
7. **B01:** the expected values are fixture literals, and J / I<sub>y</sub> are unchecked.

---

## 8. Prioritised next steps (test harness and evidence only; no application changes)

1. **Evidence governance.**
   - Stop writes into `phase_2_7/`.
   - Record the Phase 2.7 overwrite.
   - Recover the six Phase 2.6 candidate originals and the Phase 2.7 EQ candidate log from their byte-identical `_c_naive.log` twins, and document the method.
   - Make the runners refuse to write into an existing official phase directory unless an explicit flag is given.
   - Correct the remediation report's hashes, sizes, file list and time window, and populate the Markdown manifest.
   - Capture console output and shell exit status live.
2. **FS.**
   - Mirror the real layout in the sandbox (`sandbox/src/osdagbridge`, plus a sandbox repository root and working directory).
   - Snapshot the sandbox root and the working directory recursively.
   - Run production in its own process group or job object, and wait for every descendant to exit before the final snapshot.
3. **EQ.** Derive the declared intensities and positions from input keys (girder density, deck thickness and density, wearing-course thickness and density, barrier load and offset), so that load *definitions* are also checked independently.
4. **A02.** Pin the widths and densities to explicit input keys and gate the applied resultant, or formally drop that requirement in DECISIONS.md.
5. **C01.** Put the extremes in later load cases (e.g. LC3) and add a cross-end case at a shared node with mixed sign conventions.
6. **RPT.** Run DCR-only failures across girders and add a DCR = 1.0 boundary case.
7. **B01.** Derive the expected A, I<sub>z</sub>, I<sub>y</sub> and J from the snapped plate inputs at run time.

**Final gate:** Phase 3 is **not authorised**. No application source changes are recommended.
