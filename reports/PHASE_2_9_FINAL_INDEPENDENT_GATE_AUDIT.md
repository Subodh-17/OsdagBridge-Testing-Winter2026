# Phase 2.9 — Final Independent Gate Audit

**Project:** FOSSEE OsdagBridge — baseline regression and sensitivity harness
**Repository:** `source\OsdagBridge`, branch `dev`, frozen baseline `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`
**Auditor:** Claude (independent adversarial auditor)
**Audit date:** 2026-11-17
**Scope:** Phase 2.9 claims in `PHASE_2_9_REMEDIATION_REPORT.md`, `PHASE_2_9_TEST_VALIDATION_MATRIX.md`, `PHASE_2_9_REMAINING_LIMITATIONS.md`, `PHASE_2_9_EVIDENCE_GOVERNANCE_REPORT.md` and `PHASE_2_9_EVIDENCE_MANIFEST.md`, plus `evidence_guard.py`, `test_evidence_governance.py`, `run_all_baseline_tests.py`, `run_sensitivity_matrix.py`, and the Phase 2.9 evidence tree.
**Mode:** Audit only.
- No file in the workspace was edited, apart from this report.
- No source, database, evidence, branch, commit or push was touched.
- All mutations and destructive probes ran in disposable clones: `/tmp/ws29` (root) and `/tmp/ws29u` (non-root user `auditor`, uid 30033).

---

## 1. Executive verdict

**Phase 2.9 is REJECTED as a gate.** Phase 3 is **not** authorised.

The engineering workstreams (EQ, RPT, A02, C01, B01) improved and are each **ACCEPTED WITH LIMITATIONS**. However, three of Phase 2.9's central claims are contradicted by direct evidence.

1. **The guard is fail-open; there is no "fail-closed" governance in the baseline runner.**
   - `run_all_baseline_tests.py` imports a symbol that does not exist (`is_protected_phase_directory`) from `evidence_guard`.
   - The resulting `ImportError` is caught on every OS, and the runner silently installs a no-op `validate_evidence_directory` and a no-op `ProcessLifetimeJob`.
   - Using the official baseline runner, I overwrote a seeded file in a disposable `phase_2_6/baseline`.
   - The real guard, where it is used (the sensitivity runner), is also bypassed by a symlink, a case variant, and reuse of a populated directory.
2. **Process-lifetime containment does not exist.**
   - The FS test runs inside the no-op class.
   - The real class also lacks the interface the runner calls (`__enter__`, `__exit__`, `get_process_count`, `terminate`).
   - A detached SIGTERM-ignoring grandchild, a same-process-group grandchild and an at-exit spawner all passed, then wrote into the real package about 3 s after the verdict.
   - The report's claim of "catching and killing detached grandchild processes (Probe G7)" is false for both the POSIX and the Windows code paths.
3. **Evidence was overwritten again during Phase 2.9, and this was not disclosed.**
   - Four Phase 2.8 candidate logs (`a02`, `eq`, `fs`, `rpt`) were overwritten in place at 10:00:21–10:03:45 on 2026-11-17, after the Phase 2.9 preservation manifest was built (09:38).
   - The remediation report nonetheless states "0 artifacts overwritten or deleted".
   - All four are recoverable from their `_c_naive` twins.

The recovery of the seven logs flagged in Phase 2.8 is genuine and verified byte-for-byte.

"12/12 verified" and runner exit code 0 are **not** evidence of engineering correctness:
- The A02 "independent" resultant agrees to 0.06 % only because component errors of +2.7 %, +5.2 %, −37.5 % and +16.8 % cancel.
- The EQ and A02 oracles use mutually contradictory input interpretations, and both pass the same model.

| Test / workstream | Verdict |
|---|---|
| Evidence recovery (7 logs from Phase 2.6 and 2.7) | **ACCEPTED** |
| Evidence governance (guard, provenance, no-overwrite claim) | **REJECTED** |
| TC-REG-FS (sandbox and process containment) | **REJECTED** (BLOCKED under root on POSIX, which is correct behaviour) |
| TC-REG-EQ (DEF-18 load conservation and input oracle) | **ACCEPTED WITH LIMITATIONS** |
| TC-REG-RPT (executive summary status) | **ACCEPTED WITH LIMITATIONS** |
| TC-REG-A02 (ULS combination) | **ACCEPTED WITH LIMITATIONS**; the applied-resultant sub-assertion is **not trustworthy** |
| TC-REG-C01 (fatigue stress range) | **ACCEPTED WITH LIMITATIONS** |
| TC-REG-B01 (section property sync) | **ACCEPTED WITH LIMITATIONS** |
| Official runner reproduction | **ACCEPTED WITH LIMITATIONS** (runs reproduce; Windows provenance is incomplete) |
| Repository and database integrity | **ACCEPTED** (intact) |
| **Phase 2.9 gate** | **REJECTED — Phase 3 not authorised** |

---

## 2. Reproduction results

### 2.1 Environment fingerprint (independent, Linux)

| Item | Value |
|---|---|
| Python | 3.12.16 |
| Platform | Linux 6.18.44 |
| numpy | 2.5.4 |
| openseespy | 3.8.0.0 |
| pythonocc-core | 8.0.1.2 |
| Display | `xvfb-run -a` |
| Checkout | Disposable clone of `d74f56dd…` plus Phase 2.9 harness files (cloud SHA-256 verified) |
| Source aggregate before and after | `7c9294813b58fb84…` (282 files), unchanged |

Phase 2.9 harness file hashes:

| File | Size | SHA-256 (prefix) |
|---|---|---|
| `evidence_guard.py` | 7,499 B | `ed5b3f47…` |
| `run_all_baseline_tests.py` | 152,503 B | `14a6a264…` (equals the baseline summary's `runner_self_hash`) |
| `run_sensitivity_matrix.py` | 53,393 B | `0fd52e21…` |
| `test_evidence_governance.py` | 3,512 B | `ff5b6a35…` |

### 2.2 Runs (root, `/tmp/ws29`, evidence redirected to a disposable `audit_run/`)

| Runner | Command | Exit | Duration | stdout | stderr | Result |
|---|---|---|---|---|---|---|
| Baseline | `xvfb-run -a python testing/test_cases/baseline_regression/run_all_baseline_tests.py --mode baseline --evidence-dir /tmp/ws29/testing/evidence/audit_run/baseline` | **1** | 30.9 s | 22,471 B | 0 B | 14/15 MATCH; FS **BLOCKED** (root) |
| Sensitivity | `xvfb-run -a python testing/test_cases/baseline_regression/run_sensitivity_matrix.py --evidence-dir …/audit_run/sensitivity --candidates-dir …/audit_run/candidates` | **1** | 42.0 s | 44,765 B | 0 B | 11 VERIFIED, 3 BLOCKED, FS UNVERIFIED |

Observations:
- **Root correctly blocks** the permission-sensitive FS check. The non-zero exit under root is appropriate.
- After the runs, the clone's repository aggregate equalled the baseline, and no artefact was left in the repository tree.
- The Windows evidence reports exit 0, 20.87 s (baseline) and 89.56 s (sensitivity, 12 verified). Console transcripts exist: `baseline/console_output.txt` (47,600 B) and `sensitivity/console_output.txt` (94,050 B), both UTF-16. The exit-code files contain `0`.

### 2.3 Provenance defects in the Windows evidence

1. **The baseline run predates the final guard file.**
   - Baseline evidence timestamps are 10:06:06–10:06:26.
   - `evidence_guard.py` was last modified at **10:07:21**.
   - The guard version that ran was not preserved, and neither runner records the guard's hash.
   - In practice the baseline runner never loaded the real guard (see §4.1), but the evidence cannot prove that.
2. There is no `shell_exit_code` capture separate from the runner-written file.
3. The two platforms disagree: the Windows sensitivity run shows 12 verified, the Linux root run 11 verified plus FS UNVERIFIED. The difference is explained by root BLOCKED, so this is consistent, but "12/12" is platform- and privilege-dependent.

---

## 3. Evidence recovery findings

### 3.1 The seven logs flagged in Phase 2.8: restored and verified individually

Each restored file now matches three things: the original manifest hash, its `_c_naive` twin, and the preservation record in `preservation/evidence_recovery_manifest.json` (status `RESTORED_AND_VERIFIED`).

| Log | Original / restored / twin hash | Overwritten copy preserved | Restored mtime |
|---|---|---|---|
| phase_2_6 `tc_reg_a02` | `6b69e668…` | yes, hash equals the Phase 2.8 observation | twin mtime (11-16 17:41–17:43) |
| phase_2_6 `tc_reg_b01` | `8fd719ce…` | yes | twin mtime |
| phase_2_6 `tc_reg_c01` | `ff2e7b53…` | yes | twin mtime |
| phase_2_6 `tc_reg_eq` | `0d490c37…` | yes | twin mtime |
| phase_2_6 `tc_reg_fs` | `ab361431…` | yes | twin mtime |
| phase_2_6 `tc_reg_rpt` | `89d3466d…` | yes | twin mtime |
| phase_2_7 `tc_reg_eq` | `9ee3fe4b…` | yes | 11-16 18:42:06 (twin) |

Notes:
- The restored files carry their twins' mtimes, not the 09:37 restoration time. The preservation manifest documents the restoration, but the file metadata alone would mislead a later reviewer.
- The two Phase 2.6 **baseline** logs remain mismatched and have no twin. `PHASE_2_6_2_7_RECOVERY_REPORT.md` honestly classifies them as **IRRETRIEVABLY LOST**:
  - `054876a7…` → now `cdcda56b…`
  - `cd1e28d7…` → now `ab1ecb30…`
- Phases 2.5 and 2.7 are otherwise fully intact.

### 3.2 New overwrites during Phase 2.9 (undisclosed)

| Phase 2.8 candidate log | Phase 2.8 manifest hash | Current hash | Overwrite time (11-17) | Recoverable from `_c_naive` twin |
|---|---|---|---|---|
| `tc_reg_a02` | `2a61229c…` | `a6004dd4…` | 10:00–10:04 | yes |
| `tc_reg_eq` | `33d432ce…` | `9ea32ce3…` | 10:00–10:04 | yes |
| `tc_reg_fs` | `efd85cea…` | `5fba8d56…` | 10:00–10:04 | yes |
| `tc_reg_rpt` | `b84e57fb…` | `2e147cec…` | 10:00–10:04 | yes |

- `preservation/manifest_preservation.json` (520 entries, built at 09:38) mismatches disk on exactly these four files.
- These overwrites match a direct call of the test functions with `evidence_dir` pointing at Phase 2.8 (§4.1, probe GP9), or a run of the pre-final harness.
- None of the Phase 2.9 reports discloses them. Remediation report §6 states "0 artifacts overwritten or deleted". The governance report (lines 27, 106, 150) claims `phase_1d`–`phase_2_8` are protected.

### 3.3 Phase 2.9 manifest

- `phase_2_9/hashes/manifest_hashes.json` lists 100 files, and all 100 match disk (path, size, SHA-256).
- The evidence tree holds 101 files: the 100 listed plus the manifest itself.
- The manifest was generated at 10:09:46. No mechanism re-verifies it afterwards, so a later modification is detectable only by a manual re-hash.

---

## 4. Guard mutation matrix

### 4.1 Root cause: the baseline runner never uses the guard

`run_all_baseline_tests.py`, lines 50–61:

```python
try:
    from evidence_guard import validate_evidence_directory, ProcessLifetimeJob, is_protected_phase_directory
except ImportError:
    def validate_evidence_directory(path, allow_active_phase=True):
        return os.path.abspath(path)
    class ProcessLifetimeJob:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def attach_process(self, p): pass
        def get_process_count(self): return 0
        def terminate(self): pass
```

- `is_protected_phase_directory` does not exist in `evidence_guard.py`, so the import **always** fails, on Windows and POSIX alike.
- Verified: `R.validate_evidence_directory.__module__ == "run_all_baseline_tests"`, and it returns OK for a `phase_2_6` path.
- `test_evidence_governance.py` tests only the guard function in isolation. It never exercises either runner, so it cannot detect this.

### 4.2 Matrix

The real guard is `evidence_guard.validate_evidence_directory`; the runners were exercised in a disposable `/tmp/ws29`.

| # | Probe | Entry point | Result | Fail-closed? |
|---|---|---|---|---|
| GP1 | Protected `…/phase_2_6/...` | real guard | `PermissionError` | yes |
| GP2 | Traversal `phase_2_9/../phase_2_6` | real guard | blocked (`normpath`) | yes |
| GP3 | `None` / empty | real guard | `ValueError` | yes |
| GP4 | Symlink `evidence/current → phase_2_8` | real guard | **allowed** (no `realpath`) | **no** |
| GP5 | Case variant `PHASE_2_6` (matters on case-insensitive NTFS) | real guard | **allowed** (case-sensitive substring) | **no** |
| GP6 | Reuse of populated `phase_2_9/sensitivity` | sensitivity runner (`allow_creation=True`) | **allowed** | **no** |
| GP7 | Existing directory with defaults (`allow_existing=True`) | real guard | **allowed** | **no** |
| GP8 | `phase_2_6` path | baseline runner's guard | **allowed** (no-op fallback) | **no** |
| GP9 | Direct test-function call, `evidence_dir=phase_2_8/candidates` | alternate entry point | **wrote into Phase 2.8** | **no** |
| GP10 | Official baseline runner `--evidence-dir …/phase_2_6/baseline` with a seeded "ORIGINAL HISTORICAL BYTES" file | official runner | **seeded file overwritten**; 17 files written | **no** |
| GP11 | No `--evidence-dir` | official baseline runner | writes to default `phase_2_9/baseline` (no refusal) | **no** |
| GP12 | Sensitivity runner through the symlink | official sensitivity runner | **54 candidate logs written into `phase_2_8`** | **no** |
| GP13 | Existing filename / modify file / create after manifest | any | no check, and no post-manifest verification | **no** |
| GP14 | Evidence directory absent | real guard | created (`os.makedirs`) | n/a |

**Conclusion:** the guard is fail-open in practice. Only literal, correctly-cased, non-aliased protected paths are refused, and only by the sensitivity runner.

---

## 5. Filesystem and process-containment matrix

**Method.**
- Non-root user `auditor` in disposable clone `/tmp/ws29u`, with `TMPDIR` outside the workspace.
- The harness's own `test_tc_reg_fs_clean(candidate_patch=…)` was driven with candidate (b) plus injected escape payloads.
- After each probe, the clone's real package was polled for 10 s. Polling, not a fixed sleep, is what established the late writes.

| # | Escape | Verdict returned | Write landed? | Detected? |
|---|---|---|---|---|
| H0 | Candidate (b), clean | PASS | — | correct |
| H1 | Nested package path | FAIL | sandbox | **yes** |
| H2 | `<pkg>/..` (`src/`) | FAIL | sandbox | **yes** |
| H3 | `<pkg>/../../.osdag_cache` | FAIL | sandbox | **yes** |
| H3b | `<pkg>/../../../` | **PASS** | outside sandbox mirror | **no** |
| H3c | `<pkg>/../../../../` | **PASS** | outside sandbox mirror | **no** |
| H4 | Absolute real repository path | FAIL, cleaned up | repository | **yes** |
| H5 | Nested working directory | FAIL | workspace | **yes** |
| H5b | Write into `testing/evidence/phase_2_8/` | **PASS** | evidence tree (excluded from the snapshot) | **no** |
| H5c | Workspace `.osdag_cache` | **PASS** | workspace (excluded) | **no** |
| H6 | Detached `setsid` grandchild that ignores SIGTERM, delayed write | **PASS** | **real package, about 3 s after verdict** | **no** |
| H7 | Same-process-group grandchild, delayed write | **PASS** | **real package, about 3 s after verdict** | **no** |
| H8 | Writer spawned at interpreter exit | **PASS** | **real package, about 3 s after verdict** | **no** |
| H9 | `atexit` write into sandbox | FAIL | sandbox | **yes** |
| — | Read-only check as root | BLOCKED | — | correct |

On Windows, the shipped FS logs (a) report "Detached process detected: False". That is consistent with the no-op class, not with a Job Object.

**Windows code review of the real `ProcessLifetimeJob`** (not reached by the runner):
- `CreateJobObjectW` and `SetInformationJobObject(KILL_ON_JOB_CLOSE)` return values are unchecked.
- `AssignProcessToJobObject` runs after `Popen` returns, so a child can spawn before assignment.
- There is no breakaway-flag handling.
- The `__enter__`, `__exit__`, `get_process_count` and `terminate` methods that the runner calls are missing, so the class would raise `AttributeError` if it were ever wired in.

**Verdict: TC-REG-FS REJECTED.** Containment claims in the remediation report (§3, §4.2) and in limitations §3.2 are not supported. All probe artefacts were removed afterwards, the clone was verified clean, and no auditor processes remained.

---

## 6. EQ findings (DEF-18)

The input oracle now derives the expected values from `input_dict`:
- steel density, which closes the Phase 2.8 E20 circularity;
- deck thickness, wearing-course thickness and density;
- barrier load;
- per-line and nodal distribution with the 1.05 / 3.183 / 5.317 / 7.45 m transverse mesh.

| Probe | Result | Expected |
|---|---|---|
| E0 candidate (b) without the DEF-13 fix (application 78.5 vs input 76.4 kN/m³, +2.7 %) | **PASS** | should FAIL (inside the 3 % tolerance) |
| E20 production steel constant 120 | FAIL | FAIL ✓ |
| E14 genuine fix reading input density 70 | PASS | PASS ✓ |
| E31 / E32 / E33 spans 12 / 24 / 30 m | PASS / PASS / PASS | PASS ✓ |
| E1–E11, E21, E22 distribution faults (support lumping, midspan lumping, equal lumping, 25/50/25, barrier shift and split, swapped DD shares) | all FAIL | FAIL ✓ |
| V1 DD intensity −20 % (applied at load-vertex creation) | FAIL | FAIL ✓ |
| V2 DD −2.5 % | **PASS** | should FAIL |
| V3 DW −4 % (wearing course 48 mm) | FAIL | FAIL ✓ |
| V4 DW −2 % (49 mm, or density 23.5) | **PASS** | should FAIL |
| V5 / V6 barrier +0.8 % / +1.5 % | FAIL / FAIL | FAIL ✓ |
| V7 left barrier only at z = 1.00 | FAIL | FAIL ✓ |
| V8 / V9 symmetric barrier move to 1.00/7.50 and 0.30/8.20 | FAIL / FAIL | FAIL ✓ |

**Limitations.**
1. **Tolerances.**
   - The 3 % tolerance on SW, DD and DW lets genuine input-sensitivity errors pass: a 2 mm change in wearing-course thickness, a 0.5 kN/m³ density change, and the un-fixed 78.5/76.4 steel density.
   - Barrier lines use 1 %.
2. **The oracle is not fully independent.**
   - `deck_thickness_from_inputs`, `crash_barrier_load_from_inputs` and `crash_barrier_dead_load_kN_m` are production helpers.
   - Concrete density is hard-coded at 25.0 instead of the input `material.deck.density = 24.5`.
   - Barrier positions are hard-coded at 0.25 m / W − 0.25 m.
   - Wearing course is taken over the full 8.5 m deck. The A02 oracle uses a 7.5 m carriageway and ρ<sub>c</sub> 24.5.
   - **The two oracles contradict each other on the same inputs, yet both pass the same model**, so at least one of them is not checking what it claims.
3. **The oracle reads different objects from the ones analysed.**
   - The definition checks read `bgm.deck_load_case` and similar attributes, which are different objects (verified by identity) from the analysed `load_case_list` entries.
   - Mutations injected post hoc into `load_case_list` were not detected, but they also did not change the analysed results. Those probes (E12, E19, E23–E28) are therefore classified **inconclusive**, not false passes.
   - Mutations at load-vertex creation reach both objects and were detected above tolerance.

**Verdict: ACCEPTED WITH LIMITATIONS.**

---

## 7. RPT findings

Phase 2.9 added G1–G6 × four DCR modes, plus girder boundaries (Scenario 3B: 0.999 / 1.000 / 1.001) and deck boundaries (Scenario 6B). There are 66 scenarios in total.

| Probe | Result |
|---|---|
| R0 candidate (b) | PASS ✓ |
| R1 ignore stiffener; R2 moment checked only on G1; R9 DCR checked only for shear; R13 DCR checked only on G4 | FAIL ✓ |
| R3 / R5 cross-bracing first / last member only; R4 / R6 end-diaphragm first / last member only | FAIL ✓ |
| R7 cross-bracing first panel only; R15 end diaphragm ignores M3; R16 cross-bracing ignores P2; R14 ignore end diaphragm entirely | FAIL ✓ |
| R8 deck moment only; R17 deck `>=` boundary; R21 deck threshold 1.001 | FAIL ✓ |
| R10 table copied from overall status; R11 fail-all | FAIL ✓ |
| R18 girder `>=` boundary; R19 girder threshold 1.001; R22 DCR rounded to 2 dp | FAIL ✓ |
| **R12 narrative derived from overall status only** | **PASS** (undetected) |
| **R20 cross-bracing / end-diaphragm `>=` boundary** | **PASS** (no cross-bracing or end-diaphragm boundary scenario) |
| R23 girder threshold 1.0005 | PASS (resolution limit of the 0.001 boundary; acceptable) |

**Limitations.**
- Narrative masking (R12) is still undetected.
- Cross-bracing and end-diaphragm `>` versus `>=` is untested.
- All inputs are synthetic dictionaries. No scenario exercises the real design pipeline.

**Verdict: ACCEPTED WITH LIMITATIONS.**

---

## 8. A02 findings

**Independent derivation** from the inputs (L 24 m, girder area 0.025192 m² × 6 … gives SW 165.28 kN; deck 8.5 m × 0.25 m × ρ<sub>c</sub> 24.5; carriageway 7.5 m × 0.05 m × 24; barrier 6.54 kN/m × 24 m × 2):

R<sub>ULS</sub> = 1.35 × (165.28 + 1,249.50 + 313.92) + 1.75 × 216.00 = 2,333.75 + 378.00 = **2,711.74 kN** ✓ (matches the test).

The assertion is now mandatory: `rel_tol = 0.005`, i.e. ±13.56 kN. The 2,710.16 kN superposition linearity target is kept separate, which is correct.

**Critical finding: agreement by cancellation.** The analysed component reactions disagree with the oracle components:

| Component | Oracle | FE component reaction | Deviation |
|---|---|---|---|
| SW | 165.28 | 169.819 | +2.7 % |
| DD | 1,249.50 | 1,314.375 | +5.2 % |
| Crash barrier | 313.92 | 196.200 | **−37.5 %** |
| DW | 216.00 | 252.360 | +16.8 % |

The factored deviations, 1.35 × (+4.54 + 64.88 − 117.72) + 1.75 × 36.36 = −65.2 + 63.6, net to **−1.58 kN**. The test reports this as a "0.06 % match to the independently derived resultant". The A02 resultant assertion therefore does **not** verify that the applied loads are correct; it passes a model whose individual load components are significantly wrong.

| Mutation (application side, at vertex creation) | Superposition | Result |
|---|---|---|
| A0 candidate (b) | 2,710.16 | PASS |
| A1 steel constant 120 | 2,831.36 | FAIL ✓ |
| A3 barrier ×0.5 | 2,577.73 | FAIL ✓ |
| A4 barrier ×0.97 | 2,702.22 | **PASS** (inside ±13.56 kN) |
| A5 DD ×0.99 | 2,692.42 | FAIL ✓ |
| A6 DD ×0.995 | 2,701.29 | **PASS** |
| A7 / A8 DW ×0.97 / ×0.95 | 2,696.91 / 2,688.08 | FAIL ✓ |
| A9 shared helper `crash_barrier_dead_load_kN_m` halved (actual and expected) | applied 2,499.84 vs 2,577.73 | FAIL. Detected only because of the component inconsistency above; the helper itself is shared between actual and expected. |
| A2 (post hoc `load_case_list` edit) | unchanged | inconclusive (the edit does not reach the analysis) |

**Verdict: ACCEPTED WITH LIMITATIONS.**
- The factor, linearity and barrier-presence gates are sound.
- **The applied-resultant sub-assertion is not trustworthy** as an engineering check until it is made component-wise.

---

## 9. C01 findings

The four-state history is +200, +500, −1,500, +1,200 kNm. The true range is 2,700 kNm, giving Δσ = 2,700 × 10⁶ / 15.9426 × 10⁶ = **169.36 MPa**. The candidate gives 169.368 ✓.

The sign-reversal cases give 125.458 MPa ✓ (2,000 kNm), and the static case gives 0 ✓.

**Capacity, independently recomputed** (code path unchanged from Phase 2.8):
- f<sub>f</sub> = 92 × (5 × 10⁶ / 2 × 10⁶)<sup>1/3</sup> = 124.863 MPa
- f<sub>fd</sub> = 92.491 MPa
- DCR = 125.458 / 92.491 = **1.356**

| Probe | Stress ranges (cyclic, hog→sag, sag→hog) | Result |
|---|---|---|
| C3 signed last − first | 62.73 / 125.46 / 0 | FAIL ✓ |
| C4 \|last − first\| | 62.73 | FAIL ✓ |
| C5 \|M\| range | 81.55 | FAIL ✓ |
| C7 shared-node envelope with raw signs | static 125.46 | FAIL ✓ |
| C8 first two load cases only | 18.82 | FAIL ✓ |
| C13 first three load cases only | 125.46 | FAIL ✓ |
| C9 peak amplitude instead of range | 94.09 | FAIL ✓ |
| C6 reversed element order | 169.37 | PASS (order-invariant; correct) |
| C1 / C2 one or both ends sign-flipped | 169.37 | PASS. **Benign**: max − min is invariant under a per-end sign flip. |
| **C14 last two load cases only** | 169.37 | **PASS (undetected)**: both extrema sit in LC3 and LC4 |
| **C10 ignore i-end / C11 ignore j-end** | 169.37 | **PASS (undetected)**: both ends carry identical magnitudes |
| **C12 first element only** | 169.37 | **PASS (undetected)** |

**Verdict: ACCEPTED WITH LIMITATIONS.**
- The range mathematics is correct.
- The synthetic history does not discriminate "last-two-only", "one end ignored" or "first element only" candidates.

---

## 10. B01 findings

**Independent derivation** (b<sub>f</sub> 410, t<sub>f</sub> 18, d<sub>w</sub> 1,304, t<sub>w</sub> 8 mm; doubly symmetric):

| Property | Formula | Value | Test expected |
|---|---|---|---|
| A | 2 b<sub>f</sub> t<sub>f</sub> + d<sub>w</sub> t<sub>w</sub> | 0.025192 m² | 0.025192 ✓ |
| I<sub>z</sub> | t<sub>w</sub> d<sub>w</sub>³/12 + 2[b<sub>f</sub> t<sub>f</sub>³/12 + b<sub>f</sub> t<sub>f</sub>((d<sub>w</sub> + t<sub>f</sub>)/2)²] | 7.92758 × 10⁻³ m⁴ | ✓ |
| I<sub>y</sub> | 2 t<sub>f</sub> b<sub>f</sub>³/12 + d<sub>w</sub> t<sub>w</sub>³/12 | 2.0682 × 10⁻⁴ m⁴ | ✓ |
| J (thin-walled open section) | (2 b<sub>f</sub> t<sub>f</sub>³ + d<sub>w</sub> t<sub>w</sub>³)/3 | 1.81663 × 10⁻⁶ m⁴ | ✓ |

Tolerances: A and I<sub>z</sub> 0.5 %; I<sub>y</sub> and J 1 %. All four properties are now asserted.

| Mutation (solver section) | Result |
|---|---|
| A ×1.006, I<sub>z</sub> ×1.006, I<sub>y</sub> ×1.012, J ×1.012 (oversized) | FAIL ✓ |
| J ×0.5, I<sub>y</sub> ×2.0 (individual gross errors) | FAIL ✓ |
| A ×0.996, I<sub>z</sub> ×0.996, I<sub>y</sub> ×0.992, J ×0.992 (undersized, inside tolerance) | PASS (expected by the tolerance band) |
| **Production snapping returns t<sub>w</sub> 10 mm** | **PASS** (expected moves with production) |
| **Production snapping returns b<sub>f</sub> 450 mm** | **PASS** (expected moves with production) |
| Asymmetric bottom flange 24 mm | FAIL, but for the wrong reason: the test assumes symmetry, and neither side computes the true A of 0.027604 m² |

**Limitations.**
- The expected values are derived at runtime from production `_girder_value`, so they are not independent of production.
- The formula is textually identical to candidate (b)'s, so the derivation is shared.
- Snapping errors pass, and both sides assume a symmetric section.
- The hard-coded independent values from Phase 2.8 were removed instead of being kept as a fixed-input cross-check.

**Verdict: ACCEPTED WITH LIMITATIONS.**

---

## 11. Repository and database integrity (device, read-only)

| Item | Observed | Status |
|---|---|---|
| HEAD | `ref: refs/heads/dev` → `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` | ✓ |
| Branches | `dev` only | ✓ |
| `.git/*.lock` | none | ✓ |
| `.git/index` mtime | 2026-11-15 12:26:18 (unchanged) | ✓ |
| Source aggregate (282 files) | `7c9294813b58fb84ecd965643daec240276747d1788b13187c0e0f46c52b024c` | ✓ baseline |
| `Intg_osdag.sqlite` | `25f978575be64a11…`, 270,336 B, 2026-11-15 12:26:13 | ✓ |
| `weather.sqlite` (untracked) | `1d767658099bef9d…`, 180,224 B, 2026-11-16 05:48:51 | ✓ unchanged since Phase 2.8 |
| Files newer than 11-15 14:30 under `src` | `weather.sqlite` (above) and `osdagbridge.egg-info/*` (11-16 04:56, pre-existing install metadata, excluded from the aggregate) | ✓ no source change |

Note: the `src/` directory entry itself has mtime 2026-11-17 06:14. A file was created or removed there before the Phase 2.9 runs. No content difference results.

---

## 12. Remaining limitations (independent view)

1. Evidence immutability is procedural, not enforced. Historical evidence was overwritten in three successive phases (2.6, 2.7/2.8, 2.9).
2. FS containment is absent. A passing FS verdict says nothing about delayed or detached writers.
3. The A02 resultant and the EQ definition oracle rest on inconsistent input interpretations:
   - concrete density 25.0 vs 24.5;
   - wearing-course width 8.5 m vs 7.5 m.
4. The 3 % EQ tolerance and the 0.5 % A02 tolerance hide 2–3 % input-sensitivity errors.
5. B01 expected values follow production geometry.
6. The C01 and RPT synthetic fixtures leave identified non-discriminating candidates (C10–C12, C14, R12, R20).
7. Windows evidence provenance is incomplete: there is no guard hash, and the baseline ran before the final guard edit.
8. "12/12 verified" depends on the platform and on running without root. It verifies sensitivity against hand-written candidates, not engineering correctness.

---

## 13. Prioritised remediation (harness and evidence only; no application source changes)

**P0 — required before any re-gate**

1. Remove the `ImportError` fallback in `run_all_baseline_tests.py` and import only symbols that exist. A missing guard must abort the run.
2. Make `validate_evidence_directory` resolve `realpath`, compare case-insensitively on Windows, refuse an existing non-empty directory by default, and require an explicit, logged opt-in for reuse.
3. Add governance tests that run **both official runners** against protected, symlinked, case-variant and populated directories and assert refusal with no bytes written.
4. Implement process containment correctly:
   - **Windows:** create the child with `CREATE_SUSPENDED`, assign it to the Job, then resume; check every Win32 return value; query `JobObjectBasicAccountingInformation` for active processes.
   - **POSIX:** use `start_new_session=True` with `killpg`, plus `prctl(PR_SET_CHILD_SUBREAPER)`.
   - Implement the interface the runner actually calls.
   - Add an FS check that polls for late writes for a bounded period after process-tree termination is confirmed, not a fixed sleep.
5. Restore the four Phase 2.8 candidate logs from their `_c_naive` twins, preserve the overwritten versions, and publish a corrected disclosure. Withdraw the "0 artifacts overwritten" statement.
6. Record the SHA-256 of `evidence_guard.py` (and of every imported harness module) in each run summary. Re-run the Windows baseline with the final guard.

**P1 — engineering oracles**

7. A02: assert each component reaction against its own component oracle (SW, DD, DW, CB) before asserting the resultant.
8. Reconcile the EQ and A02 oracles on a single documented interpretation of `material.deck.density` and of the wearing-course width.
9. Tighten the EQ SW/DD/DW tolerance to about 0.5–1 %. Replace the production helpers in the oracle with values computed from raw input keys.
10. B01: add a fixed-input, hand-derived cross-check that does not read production `_girder_value`. Add an asymmetric-flange fixture with the correct general formula.

**P2 — discrimination gaps**

11. C01: use a history whose extrema are not adjacent (e.g. the maximum in LC2 and the minimum in LC4), use different magnitudes at the i and j ends, and put the peak in a non-first element.
12. RPT: add cross-bracing and end-diaphragm 1.000 / 1.001 boundary scenarios, and a narrative-independence scenario (component failure while `overall_status` is PASS).
13. Add post-manifest verification to both runners: re-hash on completion and fail on drift.

---

## 14. Gate decision

**Phase 2.9: REJECTED. Phase 3 is not authorised.**

The evidence-recovery work is genuine. The engineering tests are materially stronger than in Phase 2.8 and are each acceptable with the limitations stated.

However, Phase 2.9's defining deliverables were fail-closed evidence governance and OS-level process containment, and both are inoperative in the shipped runner. During the phase, historical evidence was overwritten again, and the reports state the opposite. Until the P0 items are fixed and independently re-verified, no Phase 2.9 claim of evidence integrity or containment can be relied on.

— *End of report.*
