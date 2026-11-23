# Phase 2.10 — Final Independent Gate Audit

**Project:** FOSSEE OsdagBridge — baseline regression and sensitivity harness
**Workspace:** `F:\FOSSEE internship`
**Frozen application baseline:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`
**Primary report audited:** `reports\PHASE_2_10_REMEDIATION_REPORT.md`, with the supporting reports `PHASE_2_10_REMAINING_LIMITATIONS.md`, `PHASE_2_10_TEST_RESULTS.md`, `PHASE_2_10_TEST_VALIDATION_MATRIX.md` and `PHASE_2_10_EVIDENCE_MANIFEST.md/.json`
**Controlling previous audit:** `reports\PHASE_2_9_FINAL_INDEPENDENT_GATE_AUDIT.md` (SHA-256 `41f84b327d617b47…`)
**Auditor:** Claude (independent adversarial auditor)
**Audit date:** 2026-11-17

**Mode:** audit only.
- No workspace file was edited, apart from creating this report.
- No source, harness, report, manifest, evidence, database, branch, commit or push was touched.
- Every destructive probe ran in a disposable copy built from a fresh `git clone` of the baseline:
  - `/tmp/ws210` — probes run as root;
  - `/tmp/ws210clean` — clean reproduction;
  - `/tmp/ws210u` — non-root user `auditor`, uid 30033;
  - `/tmp/ws210m` — missing-guard probes.

---

## 0. Decision summary

| Area | Verdict |
|---|---|
| Recovery of the four Phase 2.8 logs | **ACCEPTED** |
| The seven previously recovered logs (2.6 / 2.7) | **ACCEPTED** (still intact) |
| Phase 2.10 manifest (96 entries) | **ACCEPTED** |
| Historical evidence not overwritten during Phase 2.10 | **REJECTED**: four Phase 2.9 logs were overwritten and the overwrite was not disclosed |
| Evidence guard: protected-path refusal (direct, `..`, symlink, case, alternate spellings) | **ACCEPTED** |
| Evidence guard: unlisted dirs, populated reuse, alternate entry points, TOCTOU, manifest tamper | **REJECTED** |
| Missing guard import / missing guard method | **ACCEPTED** (fails closed) |
| Process containment, Linux / POSIX | **REJECTED** |
| Process containment, Windows (Job Object) | **BLOCKED**: code review only; no Windows execution was available to the auditor |
| TC-REG-FS late-write detection (5 s polling window) | **ACCEPTED WITH LIMITATIONS** (writes later than about 5.5 s escape) |
| EQ (DEF-18) | **ACCEPTED WITH LIMITATIONS** |
| A02 (ULS combination, component-wise) | **ACCEPTED WITH LIMITATIONS** |
| B01 (section properties) | **ACCEPTED WITH LIMITATIONS** |
| C01 (fatigue stress range) | **ACCEPTED WITH LIMITATIONS** |
| RPT (executive summary) | **ACCEPTED WITH LIMITATIONS** |
| Clean reproduction of both official runners | **ACCEPTED** |
| Source repository and both databases | **ACCEPTED** (frozen baseline intact) |
| **Overall** | **REJECT PHASE 2.10** (§10) |

The engineering workstreams are now substantially sound. Two governance failures decide the gate:
- **Phase 2.10 overwrote historical evidence again.** Four Phase 2.9 candidate logs were rewritten at 11:18–11:20 UTC by direct test-function calls that bypass the guard. None of the Phase 2.10 reports discloses this.
- **POSIX process containment does not work.** The harness's own governance test Vector 9 fails on Linux, and the remaining-limitations report describes a mechanism that the code does not implement.

The Phase 2.10 reports describe the harness as "fail-closed" and "production-ready". Those claims are not supported.

---

## 1. Recovery and evidence integrity

### F-01 — The four Phase 2.8 logs are restored to their original manifest hashes

| Field | Detail |
|---|---|
| Severity | Info (positive) |
| Inspected | `testing/evidence/phase_2_8/hashes/manifest_hashes.json` (91 entries); `phase_2_8/candidates/*.log`; `phase_2_10/preservation/overwritten_phase_2_8_versions/*`; `phase_2_10/preservation/PHASE_2_8_RECOVERY_REPORT.md` |
| Probe | Re-hashed every Phase 2.5–2.8 manifest entry against disk on the device |
| Command | `python3` SHA-256 walk over each `phase_2_X/hashes/manifest_hashes.json` (device shell, read-only) |
| Observed | **Phase 2.8: 91/91 match.** The overwritten copies are preserved with sizes 2,565 / 3,014 / 5,679 / 1,905 B and mtimes 10:00:21–10:03:45, matching the Phase 2.9 audit observation. |
| Verdict | **ACCEPTED** |

Restored files:

| Log | Hash (original = restored) | Size |
|---|---|---|
| `tc_reg_a02_uls_combination_sum.log` | `2a61229c…` | 2,532 B |
| `tc_reg_eq_load_conservation.log` | `33d432ce…` | 4,632 B |
| `tc_reg_fs_clean_working_tree.log` | `efd85cea…` | 1,825 B |
| `tc_reg_rpt_exec_summary_status.log` | `b84e57fb…` | 2,324 B |

- Each restored file equals the hash recorded in the Phase 2.8 manifest, which was written before the overwrite and so is authentic.
- The restored files carry mtime 11-17 06:33:25–06:34:04, i.e. their twins' original timestamps, not the restore time. The provenance is documented only in the recovery report.

### F-02 — The seven earlier recovered logs remain intact

| Field | Detail |
|---|---|
| Severity | Info |
| Observed | **Phase 2.5: 93/93. Phase 2.7: 93/93.** Phase 2.6: 91/93. The two mismatches are the baseline logs already classified as irretrievably lost: `054876a7`→`cdcda56b` and `cd1e28d7`→`ab1ecb30`, both unchanged since 11-16 18:33–18:34. All six Phase 2.6 candidate logs and the Phase 2.7 EQ log match. |
| Verdict | **ACCEPTED** |

### F-03 — Phase 2.10 manifest

| Field | Detail |
|---|---|
| Severity | Info |
| Inspected | `phase_2_10/hashes/manifest_hashes.json`; `reports/PHASE_2_10_EVIDENCE_MANIFEST.json` (`total_artifacts: 96`) |
| Observed | **96/96 entries match disk in both size and SHA-256.** The tree holds 97 files (96 plus the manifest). Evidence timestamps run from 11:23:07 to 11:26:59. |
| Provenance | The baseline summary records `guard_self_hash` `4d070795bb08840a…` and `runner_self_hash` `bc3a2c9aad246b0d…`. Both equal the current files, and both files were last edited (10:56:45, 11:20:43) before the runs. Python 3.12.16, Windows 11 26300. |
| Verdict | **ACCEPTED.** The Phase 2.9 provenance defect (no guard hash recorded) is closed. |

### F-04 — Historical evidence was overwritten during Phase 2.10 and not disclosed

| Field | Detail |
|---|---|
| Severity | **Critical** |
| Inspected | `testing/evidence/phase_2_9/hashes/manifest_hashes.json` (100 entries) against disk |
| Observed | **Four Phase 2.9 candidate logs mismatch** (table below). Each file header shows `PYTHON EXECUTABLE: C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe` and a matching `TIMESTAMP UTC`. All four timestamps precede the official Phase 2.10 runs (11:23–11:25), and `phase_2_9` was already in `PROTECTED_PHASES`. |
| Root cause | The mechanism reproduced in §2, probes G12–G14: test functions called directly with `evidence_dir`, or a sensitivity module global, pointed at `phase_2_9`, which bypasses `validate_evidence_directory`. |
| Recoverability | All four `_c_naive` twins are present and intact (`195998d9`, `fa11727f`, `213966a3`, `28453fe8` = the original manifest values). |
| Disclosure | No Phase 2.10 report mentions it. The remediation report discusses only the Phase 2.8 overwrites (lines 21, 45, 118). |
| Verdict | **REJECTED**. This is the fourth consecutive phase in which historical evidence was overwritten. |

| Phase 2.9 log | Manifest hash | Disk hash | Size (manifest → disk) | Overwritten (UTC) |
|---|---|---|---|---|
| `candidates/tc_reg_eq_load_conservation.log` | `213966a3` | `eae7b526` | 5,679 → 6,048 B | 11:18:59 |
| `candidates/tc_reg_c01_sectional_stress_range.log` | `fa11727f` | `2ed1edad` | 2,338 → 2,338 B | 11:19:09 |
| `candidates/tc_reg_rpt_exec_summary_status.log` | `28453fe8` | `d3e836ec` | 3,014 → 3,100 B | 11:19:48 |
| `candidates/tc_reg_b01_section_property_sync.log` | `195998d9` | `7403df5a` | 3,130 → 3,729 B | 11:20:52 |

### F-05 — Source repository and databases (device, read-only)

| Item | Observed |
|---|---|
| HEAD | `ref: refs/heads/dev` → `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` |
| Branches | `dev` only |
| Locks | No `.git/*.lock` |
| `.git/index` mtime | 2026-11-15 12:26:18 (unchanged) |
| Source aggregate | 282 files, `7c9294813b58fb84ecd965643daec240276747d1788b13187c0e0f46c52b024c` = baseline |
| `Intg_osdag.sqlite` | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91`, 270,336 B, 2026-11-15 12:26:13 (unchanged) |
| `weather.sqlite` (untracked) | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98`, 180,224 B, 2026-11-16 05:48:51 (unchanged since Phase 2.8) |
| `src/` files modified after 2026-11-17 10:42 | none |

**Verdict: ACCEPTED.**

---

## 2. Evidence guard

**Implementation inspected:** `evidence_guard.py` (10,696 B, SHA-256 `4d070795bb08840af63d7f39bee679f22458ca5c225f67e65510621d50885725`):
- `is_protected_phase_directory` uses `realpath`, a lower-cased comparison, and checks both the raw and the resolved path against `PROTECTED_PHASES` = `phase_1d`, `phase_2_1` … `phase_2_9`. On any exception it returns `False`.
- `validate_evidence_directory(…, allow_existing=False)` refuses populated directories unless `allow_existing`, `allow_active_phase` or `allow_creation` is passed.

**Call sites:**
- `run_all_baseline_tests.py` (166,722 B, `bc3a2c9a…`): direct import at lines 52–58, with **no** `ImportError` fallback. `main()` calls `validate_evidence_directory(args.evidence_dir, allow_active_phase=True)` (line 2970). `--evidence-dir` defaults to `phase_2_10/baseline`.
- `run_sensitivity_matrix.py` (59,708 B, `af0f8957…`): lines 1234–1235 call it with `allow_creation=True` on `abspath` values.

Probe scripts and output:
- `/tmp/p25/g210/probe_guard.sh` (`e40f0e7e…`), output `probe_guard.out` (`ec5877b8…`)
- `probe_alt.py` (`9b6171a1…`)
- `probe_toctou.sh` (`5be8a2e3…`)

Each probe seeds a sentinel file and afterwards checks the sentinel hash and the directory listing; the returned status was not relied on.

| # | Probe | Command (in `/tmp/ws210`) | Observed filesystem state | Verdict |
|---|---|---|---|---|
| G1 | Protected direct | `run_all_baseline_tests.py --mode baseline --evidence-dir …/phase_2_6/baseline` | `PermissionError`, exit 1; sentinel `6dd5ad45…` intact; 1 file | ACCEPTED |
| G2 | `..` traversal | `--evidence-dir …/phase_2_10/../phase_2_6/baseline` | `PermissionError`; intact | ACCEPTED |
| G3 | Symlink alias | `evidence/alias → phase_2_6`, `--evidence-dir …/alias/baseline` | `PermissionError`; intact | ACCEPTED |
| G4 | Case variant | `--evidence-dir …/PHASE_2_6/baseline` | `PermissionError`; no directory created | ACCEPTED |
| G5 | Alternate spelling | `--evidence-dir …//phase_2_6/./baseline` | `PermissionError`; intact | ACCEPTED |
| G6 | Sensitivity runner protected | `run_sensitivity_matrix.py --candidates-dir …/phase_2_9/candidates` | `PermissionError`; intact | ACCEPTED |
| G7 | Guard module absent | `/tmp/ws210m`, `evidence_guard.py` renamed, both runners | `ModuleNotFoundError`, exit 1, **no directory created** | ACCEPTED |
| G8 | Guard method absent | `get_process_count` removed | FS test `ERROR` (`AttributeError`), harness exceptions 1, exit 1 | ACCEPTED |
| **G9** | Unlisted historical directories | `--evidence-dir …/phase_2_baseline`, then `…/phase_2_repaired` (both exist in the real workspace and are absent from `PROTECTED_PHASES`) | **Sentinels overwritten** (`4c0d1a11`→`3bf8c424`, `b84a0e7e`→`1e3994dd`); 18 files written | **REJECTED** |
| **G10** | Default directory already populated | No `--evidence-dir`, with `phase_2_10/baseline` seeded | **Sentinel overwritten** (`604738da`→`13507271`). `allow_active_phase=True` is hard-coded, so the official Phase 2.10 evidence is overwritten by any argument-less run. | **REJECTED** |
| **G11** | Populated reuse via the sensitivity runner | `--candidates-dir` on a populated directory | **Sentinel overwritten** (`331760a1`→`7b2c6e0b`); 54 files | **REJECTED** |
| **G12** | Alternate entry point: test function | `R.test_tc_reg_a01(evidence_dir=…/phase_2_8/candidates)` | **Sentinel overwritten** (`0fc8e976`→`10c546cb`) | **REJECTED** |
| **G13** | Alternate entry point: logger | `R.log_test_result(…, evidence_dir=…/phase_2_7/candidates)` | **Overwritten** (`0fc8e976`→`5ada3a68`) | **REJECTED** |
| **G14** | Alternate entry point: module global | `S.CANDIDATES_DIR=…/phase_2_9/candidates; S.mut_c_a01()` | **Overwritten** (`0fc8e976`→`bdde1303`). This is the mechanism behind F-04. | **REJECTED** |
| **G15** | TOCTOU directory swap | `bash probe_toctou.sh`: run `--evidence-dir …/swap` (an empty real directory); after the banner, `mv swap swap.real; ln -s phase_2_6/baseline swap` | Runner exit 1. **18 files written into protected `phase_2_6/baseline`; sentinel `0fc8e976`→`6380b7b8`**; `swap.real` empty. Validation happens once at start and writes follow 46 s later. | **REJECTED** |
| **G16** | Post-manifest tamper | Appended to `tc_reg_a02…log` after the run, then rewrote `post_run_evidence_manifest.json` | Manifest `f399e75d` vs disk `e82e7cd0`: no harness command ever re-verifies. After a consistent rewrite the evidence is self-consistent (unsigned, stored beside the evidence). | **REJECTED** |

Notes on G16:
- The in-run "drift" check (lines 3055–3080) re-hashes the same bytes milliseconds after writing them, so it cannot detect anything.
- The exit-code file is written before that check.

`test_evidence_governance.py` (`7607e971…`) passes 9/10 vectors on Linux; **Vector 9 fails** (see F-06). It does not cover G9–G16.

**Overall guard verdict:** protected-path refusal **ACCEPTED**; overall governance **REJECTED**. The guard protects only the runner `main()` entry, only listed phase names, and only at the moment of validation.

---

## 3. Process containment

**Implementation inspected:** `ProcessLifetimeJob` in `evidence_guard.py`.

Windows path:
- `CreateJobObjectW` and `SetInformationJobObject(JobObjectExtendedLimitInformation, KILL_ON_JOB_CLOSE)`, with return values now checked.
- `attach_process` → `AssignProcessToJobObject(proc._handle)`.
- `get_process_count` via `JobObjectBasicAccountingInformation.ActiveProcesses`.
- `terminate` → `TerminateJobObject` and `CloseHandle`.

POSIX path:
- `attach_process` sets `self.pgid = proc.pid`.
- `get_process_count` uses `os.killpg(pgid, 0)`.
- `terminate` uses `os.killpg(pgid, SIGKILL)`.

Call sites:
- `run_all_baseline_tests.py:2680–2694`: `subprocess.Popen([...], env, cwd, stdout=PIPE, stderr=PIPE, text=True)` with **no `start_new_session`, no `preexec_fn`, no `CREATE_SUSPENDED`**. Then `attach_process`, `communicate(15)`, `sleep(0.05)`, `get_process_count()`, `terminate()`.
- `:2763–2767`: the same pattern for the read-only check.
- `Check 5` (`:2797–2850`): a **5.0 s** polling window that snapshots the real repository and the working directory every 0.5 s.

### F-06 — POSIX containment is a no-op

| Field | Detail |
|---|---|
| Severity | **Critical** |
| Analysis | The child is never made a process-group leader, so `pgid = proc.pid` names a group that does not exist. `killpg(pid, 0)` raises `ESRCH`, so the count is always 0, and `killpg(pid, SIGKILL)` silently does nothing. There is no subreaper (`PR_SET_CHILD_SUBREAPER`). |
| Probe 1 | The harness's own `test_09_process_containment_boundary` |
| Command 1 | `cd /tmp/ws210 && python -m unittest testing.test_cases.baseline_regression.test_evidence_governance.TestEvidenceGovernanceAdversarial.test_09_process_containment_boundary` |
| Observed 1 | `AssertionError: 0 not greater than or equal to 1 : Expected >= 1 active processes, got 0` |
| Probe 2 | Non-root user; candidate (b) FS patch plus an injected escaping descendant; real package polled 12 s after the verdict |
| Command 2 | `su auditor -c "cd /tmp/ws210u && HOME=/tmp/aud_home TMPDIR=/tmp/aud_tmp xvfb-run -a python probe210c2.py /tmp/ws210u"` (`ec0d765c…`) |
| Report claim | `PHASE_2_10_REMAINING_LIMITATIONS.md` §3.2 says POSIX uses "`start_new_session=True` with `os.killpg(pgid, SIGKILL)` and subreaper registration". **No such code exists.** Remediation report §3.2 says "`os.setpgid`", which is also absent. |
| Verdict | **REJECTED** |

Results of probe 2:

| # | Descendant | FS verdict | Writer alive at verdict | File in **real** package 12 s later |
|---|---|---|---|---|
| H14 | `setsid` grandchild, ignores SIGTERM, writes at 8 s | **PASS** | yes | **yes** |
| H15 | Same-group grandchild, writes at 8 s | **PASS** | yes | **yes** |
| H16 | `setsid` grandchild, writes at 5.5 s | BASELINE_FAIL (caught by polling) | yes | no (cleaned up) |

### F-07 — Late-write detection depends on a 5 s polling window

| Field | Detail |
|---|---|
| Severity | Major |
| Probe | `probe210c.py` (`01684ba0…`), non-root |
| Observed | Every escape that writes within about 5 s was **detected**, though only by the polling window, not by containment. These cases include detached `setsid` (H6), same group (H7), spawn at exit (H8), `atexit` sandbox write (H9), a three-level chain with a new session ignoring TERM/HUP (H10), a double-fork daemon (H11), and same group at 0.3 s and 5 s (H12, H13). Every writer **survived** the boundary. Writes later than the window escape (F-06 H14/H15). |
| Verdict | **ACCEPTED WITH LIMITATIONS** as a detector; it is not containment. |

### F-08 — Windows Job Object

| Field | Detail |
|---|---|
| Severity | Major (unverifiable) |
| Review finding 1 | **The child runs before assignment.** `Popen` starts the child, which is assigned later. A descendant spawned in that interval is outside the job. `CREATE_SUSPENDED` with assign-then-resume is not used. |
| Review finding 2 | Kill-on-close is set correctly. `JOB_OBJECT_LIMIT_BREAKAWAY_OK` and `SILENT_BREAKAWAY_OK` are not set, so breakaway is disallowed and descendants inherit the job, provided they start after assignment. |
| Review finding 3 | The ctypes `restype` / `argtypes` are not declared, so `HANDLE` is read as a 32-bit `c_int`. This works in practice but is not robust. |
| Shipped evidence | `phase_2_10/candidates/tc_reg_fs_clean_working_tree_b_correct.log` reports "Detached process detected: False". No Windows escape probe evidence is shipped. |
| Execution | Not possible: the auditor's device shell is a Linux VM, so no Windows process could be run. |
| Verdict | **BLOCKED.** Complete containment must not be claimed for Windows until assign-before-execute is proven. |

---

## 4. EQ (DEF-18) and A02 consistency

### Independent derivation from the inputs

Inputs: `material.deck.density` 24.5, `material.girder.density` 76.4, deck thickness 250 mm, `geometry.carriageway_width` 7.5 m, wearing course 50 mm × 24 kN/m³, L 24 m, deck width 8.5 m, barrier 6.54 kN/m (IRC 5 default, since `crash_barrier_load` is absent).

| Component | Derivation | Value |
|---|---|---|
| DD | 0.25 × 24.5 = 6.125 kN/m² × 24 × 8.5 | **1,249.50 kN** |
| DW | 0.05 × 24 = 1.2 kN/m² × 24 × 7.5 | **216.00 kN** |
| CB | 6.54 × 24 × 2 | **313.92 kN** |
| SW | Σ girder area × 76.4 × 24 | **165.28 kN** |
| ULS | 1.35 × (165.28 + 1,249.50 + 313.92) + 1.75 × 216 | **2,711.74 kN** |

Candidate (b) reproduces each component exactly. EQ and A02 now use the same input interpretation, which closes the Phase 2.9 contradiction. One documented difference remains: barrier magnitude (EQ hard-codes it, A02 uses the production helper; see F-10).

### F-09 — EQ mutation matrix

| Field | Detail |
|---|---|
| Probe | `/tmp/p25/e210/probe_eq.py` (`9dd53a72…`), cloud, `xvfb-run -a python probe_eq.py` |
| Tolerances | 0.5 % on SW, DD, DW and barrier; 0.05 m on centroids |

| Probe | Result | Correct? |
|---|---|---|
| Q0 candidate (b) | PASS | ✓ |
| Q1 candidate uses ρ<sub>c</sub> 25.0 instead of input 24.5 | FAIL (1,275.0 vs 1,249.5 kN) | ✓ |
| Q2 candidate spreads DW over the full 8.5 m | FAIL (244.8 vs 216.0 kN; shares 17 %) | ✓ |
| Q3 no steel-density fix (78.5 vs 76.4) | FAIL (169.8 vs 165.3 kN) | ✓ |
| Q4 DD −0.5 % | PASS | edge of tolerance |
| Q5 DD −1.0 % | FAIL | ✓ |
| Q6 / Q7 DW −0.5 % / −1.0 % | FAIL / FAIL | ✓ |
| Q8 / Q9 barrier +0.6 % / −0.4 % | FAIL / FAIL (per-line check) | ✓ |
| Q10 / Q11 barriers moved 0.04 / 0.06 m inboard | FAIL / FAIL | ✓ |
| Q12 left barrier only, to 0.35 m | FAIL | ✓ |
| Q13–Q16 genuine input changes (ρ<sub>c</sub> 26; carriageway 7.0; wearing course 65 mm; ρ<sub>s</sub> 70) | PASS ×4 (the oracle follows the inputs) | ✓ |
| **Q17 genuine input `crash_barrier_load` = 8.0 kN/m** | **FAIL (false failure)**: 384.0 vs hard-coded 313.9 | ✗ |
| Q18 genuine input barrier width 0.60 m | PASS. The oracle hard-codes z = 0.25 / W − 0.25, so it cannot detect a barrier position that ignores the width. | limitation |
| Q19 / Q20 spans 12 / 30 m | PASS / PASS | ✓ |

**Verdict: ACCEPTED WITH LIMITATIONS.** The barrier magnitude (`cb_line_kN_m = 6.54`) and position (0.25 m) are hard-coded, not derived from the inputs; deck width comes from production `bgm.w`.

### F-10 — A02 component-wise oracle

| Field | Detail |
|---|---|
| Inspected | `test_tc_reg_a02`: `sw/dd/dw/cb_comp_ok = isclose(…, rel_tol=0.01)`, AND-ed with linearity, factoring, barrier inclusion and the 0.5 % resultant |
| Probe | `/tmp/p25/e210/probe_a02.py` (`555bb2b3…`) |
| Verdict | **ACCEPTED WITH LIMITATIONS** |

| Probe | Components (SW / DD / CB / DW, kN) | Result |
|---|---|---|
| A0 candidate (b) | 165.276 / 1,249.500 / 313.920 / 216.000; total 2,711.74 | PASS ✓ |
| A1 DD −0.8 % | DD 1,239.5 | PASS (inside 1 %) |
| A2 DD −1.2 % | DD 1,234.5 | FAIL ✓ |
| A3 barrier −0.9 % / A5 DW −0.9 % | — | PASS (inside 1 %) |
| A4 barrier −1.5 % | CB 309.2 | FAIL ✓ |
| A6 offsetting +0.9 % DD, −0.9 % DW, −0.9 % CB | total 2,719.70 | PASS (each error inside its own tolerance) |
| **A7 large offsetting: DD +5 %, CB −20 % (total 2,711.32, Δ −0.42 kN)** | — | **FAIL ✓** |
| **A8 shared helper `crash_barrier_dead_load_kN_m` × 0.9 (actual and expected)** | expected and actual both 2,669.36 | **PASS ✗** |
| A9 / A10 genuine inputs ρ<sub>c</sub> 26 / `crash_barrier_load` 8 | — | PASS / PASS ✓ |

- **Cancellation is eliminated** (A7). The Phase 2.9 cancelling component errors (+2.7 / +5.2 / −37.5 / +16.8 %) are now each caught; the baseline reports BASELINE_FAIL.
- The A02 barrier oracle still reuses `crash_barrier_load_from_inputs` and `crash_barrier_dead_load_kN_m` from production (A8).
- Per-component errors under 1 % pass.
- **EQ and A02 derive the barrier differently.** EQ hard-codes 6.54, so it catches A8 but false-fails Q17. A02 uses the helper, so it misses A8 but handles Q17. This difference is not documented.

---

## 5. B01 — section properties

**Independent derivation** (b<sub>f</sub> 410, t<sub>f</sub> 18, d<sub>w</sub> = 1,340 − 36 = 1,304, t<sub>w</sub> 8 mm):

| Property | Value |
|---|---|
| A | 0.025192 m² |
| I<sub>z</sub> | 7.92758 × 10⁻³ m⁴ |
| I<sub>y</sub> | 2.0682 × 10⁻⁴ m⁴ |
| J | 1.81663 × 10⁻⁶ m⁴ |

These equal the new `FIXED_*` constants. The asymmetric fixture (400×20 / 1,200×10 / 500×25 mm) was re-derived independently: A 0.0325 m², ȳ 539.577 mm, I<sub>z</sub> 8.8701 × 10⁻³, I<sub>y</sub> 3.6719 × 10⁻⁴, J 4.0708 × 10⁻⁶ m⁴ — all match.

### F-11 — B01 dimension and property mutations

| Field | Detail |
|---|---|
| Inspected | `test_tc_reg_b01`: each property must match **both** the runtime value from production `_girder_value` (0.5 % / 1 %) **and** the fixed constant |
| Probe | `/tmp/p25/e210/probe_b01.py` (`cef26105…`); production `_girder_value` and the solver `SectionProperties` mutated |

| Mutation | Result |
|---|---|
| Web thickness 8 → 10 mm; 8 → 8.1 mm (+1.25 %) | FAIL / FAIL ✓ |
| Top flange width 410 → 450; 410 → 412 (+0.5 %) | FAIL / FAIL ✓ |
| Top flange thickness 18 → 20 | FAIL ✓ |
| Bottom flange thickness 18 → 20 | FAIL ✓ |
| Overall depth 1,340 → 1,360; web-depth key 1,306 → 1,324 | FAIL / FAIL ✓ |
| **Bottom flange width 410 → 450** | **PASS ✗**: neither oracle nor candidate reads bottom flange width |
| Solver A, I<sub>z</sub> ×1.006; I<sub>y</sub>, J ×1.012; J ×0.5; I<sub>y</sub> ×2 | FAIL ✓ |
| Solver A, I<sub>z</sub> ×0.996; I<sub>y</sub>, J ×0.992 | PASS (inside the stated tolerance band) |

**Verdict: ACCEPTED WITH LIMITATIONS.**
- The fixed reference does not reuse production dimensions or calculations, which closes the Phase 2.9 copying issue.
- The asymmetric fixture only checks the oracle formula. It is never compared with production.
- Bottom flange width is not checked.
- The fixed constants are valid only for this one input set.

---

## 6. C01 — fatigue stress range

**Fixture, as inspected:** five load cases × three elements. Element 2, end j carries +200, +1,200, +300, −1,500, +100 kNm; end i carries −150, −800, −250, +1,000, −80 kNm. Elements 1 and 3 are zero.

**Independent result:**
- Governing range: 1,200 − (−1,500) = **2,700 kNm** at element 2, end j.
- The composite bottom-fibre modulus was derived independently from the section (A 25,192 mm², y 670 mm, I 7.92758 × 10⁹ mm⁴), b<sub>eff</sub> = min(L/4, 2,100 mm) = 2,100 mm and a 250 mm slab:
  - with short-term m = 7.5, Z<sub>b</sub> = **15.9416 × 10⁶ mm³**, giving **Δσ = 169.37 MPa**. This matches candidate (b)'s 169.368 MPa and the test's 169.358 MPa within 0.006 %.
  - with m = E<sub>s</sub>/E<sub>cm</sub> = 6.06, Z<sub>b</sub> would be 16.108 × 10⁶ (Δσ 167.6 MPa, −1.0 %). The test therefore relies on production's modular-ratio choice.
- The production baseline path gives a false static range of 125.458 MPa and a hog/sag range of 188.187 MPa (expected 125.450), so DEF-07 is still reproduced.

### F-12 — C01 mutation matrix

| Field | Detail |
|---|---|
| Probe | `/tmp/p25/e210/probe_c01.py` (`bedf8ab5…`), substituting into candidate `mut_b_c01` |

| Probe | Cyclic range (MPa) | Result |
|---|---|---|
| C0 candidate (b) | 169.368 | PASS ✓ |
| C8 first two load cases / C13 first three / **C14 last two** | 62.73 / 62.73 / **100.37** | FAIL ✓ (closes the Phase 2.9 C14 gap) |
| C15 drop global max (LC2) / C16 drop global min (LC4) | 112.91 / 69.00 | FAIL ✓ |
| **C11 i-end only** | 112.91 | FAIL ✓ |
| **C12 first element only / C20 last element only** | 0 / 0 | FAIL ✓ |
| C3 / C4 last − first (signed / absolute); C5 \|M\| range; C9 peak amplitude | — | FAIL ✓ |
| C7 shared-node envelope with raw signs | — | FAIL ✓ |
| C6 reversed element order; C18 reversed load-case order | 169.37 | PASS (order-invariant; correct) |
| C1 / C2 per-end sign flip | 169.37 | PASS (benign: max − min is sign-invariant) |
| **C10 j-end only (i-end ignored)** | 169.37 | **PASS**: the fixture is asymmetric in one direction only |
| C17 first four load cases only | 169.37 | PASS (both extrema lie in LC1–LC4; dropping LC5 is not tested) |
| C19 mixed end signs combined per element | 169.37 | PASS (not discriminated) |

**Verdict: ACCEPTED WITH LIMITATIONS.**
- Shared-node continuity cannot be tested: element 3 is all zero, so element 2's j-end and element 3's i-end disagree at node 3.
- The production extraction path runs on a synthetic dataset, not on solver output.

---

## 7. RPT — executive summary

### F-13 — RPT through the production `executive_summary`

| Field | Detail |
|---|---|
| Inspected | `test_tc_reg_rpt_status` calls the production `osdagbridge.core.reports.executive_summary.executive_summary` on 74 synthetic component-result scenarios, including the new Scenarios 8 (cross-bracing), 9 (end diaphragm) and 10A/10B (narrative independence) |
| Probes | `/tmp/p25/e210/probe_rpt.py` (`8ea10728…`); `probe_rpt2.py` (`0ffed9b7…`) |

| Probe | Result |
|---|---|
| R0 candidate (b) | PASS ✓ |
| R1–R11, R13–R16 (ignored check types, girders, members or panels; table copied; fail-all) | FAIL ✓ |
| **R12 narrative derived from overall status** | **FAIL ✓** (closed by Scenario 10B) |
| R17 / R18 / R19 / R21 / R22 deck and girder boundaries (`>=`, 1.001, rounding) | FAIL ✓ |
| **R20 cross-bracing and end-diaphragm `>=`; R24 end diaphragm only `>=`** | **FAIL ✓** (closed by Scenarios 8 / 9 at 1.000) |
| **R25 end-diaphragm threshold 1.001; R26 cross-bracing threshold 1.001** | **FAIL ✓** (closed at 1.001) |
| R23 girder / R27 end-diaphragm threshold 1.0005 | PASS (resolution of the 0.001 grid) |

**Verdict: ACCEPTED WITH LIMITATIONS.**
- The 0.999 / 1.000 / 1.001 boundaries are now verified for girders, deck, cross-bracing and end diaphragms.
- Scenarios are synthetic dictionaries.
- Cross-bracing and end-diaphragm efficiency is read only from the `Axial/Osdag/efficiency` key.

---

## 8. Clean reproduction (live capture, no reconstruction)

The checkout was a fresh `git clone` of `d74f56dd…` into `/tmp/ws210clean`, with the Phase 2.10 harness files hash-verified (§2) and the Phase 1D fixtures. Environment: Python 3.12.16, Linux 6.18.44 (glibc 2.39), numpy 2.5.4, openseespy 3.8.0.0, `xvfb-run -a`.

| Run | User | Start (UTC) | Command | Exit | Duration | stdout / stderr | Result |
|---|---|---|---|---|---|---|---|
| Baseline | root | 11:42:09 | `run_all_baseline_tests.py --mode baseline --evidence-dir /tmp/ws210clean/testing/evidence/audit_run/baseline` | **1** | 45.99 s | 23,573 B `198510ae…` / 0 B | 14/15 match; FS **BLOCKED** (root; DEC-023) |
| Sensitivity | root | 11:42:55 | `run_sensitivity_matrix.py --evidence-dir …/audit_run/sensitivity --candidates-dir …/audit_run/candidates` | **1** | 52.39 s | 45,948 B `1934a2b4…` / 0 B | 11/12 verified; FS UNVERIFIED; 3 BLOCKED |
| Baseline | auditor (30033) | 11:53:50 | Same, `--evidence-dir /tmp/ws210u/testing/evidence/audit_u/baseline` | **0** | ≈22 s | `9318e3ba…` / 0 B | **15/15 match** |
| Sensitivity | auditor | 11:54:13 → 11:55:07 | Same, `audit_u/sensitivity`, `audit_u/candidates` | **0** | ≈55 s | `d8eb0811…` / 0 B | **12/12 verified**, gate PASSED |

Live captures are in `/tmp/p25/live210/` (environment `966d8b92…`) and `/tmp/p25/live210u/`.

- After the runs, both clones had `git status --porcelain` = 0 lines; only ignored `__pycache__` was present. Source aggregate `7c929481…` was unchanged.
- The non-root Linux reproduction matches the Windows claim (15/15, 12/12, exit 0). As stated above, this shows sensitivity against hand-written candidates, not engineering correctness, and it does not exercise the escapes in F-06.

**Verdict: ACCEPTED.**

---

## 9. Report claims versus observation

| Claim (Phase 2.10 reports) | Observation |
|---|---|
| "Fail-closed" guard; "zero-byte writes" on CLI refusal | True only for listed phase names via runner `main()`. False for G9–G16. |
| Only the Phase 2.8 overwrites need disclosure | Four Phase 2.9 logs were overwritten during Phase 2.10 (F-04) and are not disclosed. |
| "10/10 adversarial governance tests pass" | 9/10 on Linux; Vector 9 fails (F-06). |
| POSIX "`start_new_session=True` … subreaper registration" (limitations §3.2); "`os.setpgid`" (remediation §3.2) | Neither is in the code. |
| "Guarantees no descendant process escapes or runs after the boundary closes" (guard docstring) | False on POSIX (H14/H15). Unproven on Windows (assignment after start). |
| A02 component-wise, cancellation eliminated | Verified (A7), with the shared-helper limitation (A8). |
| EQ/A02 reconciled to ρ<sub>c</sub> 24.5 and 7.5 m carriageway | Verified. Barrier derivation still differs (F-10). |
| B01 fixed independent reference | Verified; bottom flange width is unchecked. |
| C01 discriminates last-two, first-element and i-end-only candidates | Verified; a j-end-only candidate passes (C10). |
| RPT cross-bracing / end-diaphragm boundaries and narrative independence | Verified. |
| "Robust, fail-closed, and production-ready" | Not supported. |

---

## 10. Overall decision

# **REJECT PHASE 2.10**

**Why:**
1. **Historical evidence was overwritten during this phase and not disclosed** (F-04). Four Phase 2.9 logs were overwritten at 11:18–11:20 UTC, after `phase_2_9` was protected. The guard cannot prevent this because direct test-function calls never pass through it (G12–G14).
2. **The guard is not fail-closed beyond literal protected names.** It allows a TOCTOU swap into `phase_2_6` (G15), writes into unlisted historical directories (G9), overwrites the official `phase_2_10` evidence on a default run (G10), and has no post-run tamper verification (G16).
3. **Process containment does not exist on POSIX** (F-06); the harness's own Vector 9 fails, and the limitations report describes code that is not there. Windows containment is unproven (F-08, BLOCKED: assignment after start).
4. The Phase 2.10 reports overstate the result in exactly these areas (§9).

**What improved and is accepted with limitations:** EQ, A02, B01, C01 and RPT now discriminate the Phase 2.9 gaps. In particular:
- A02 error cancellation is eliminated;
- the EQ and A02 density and width inputs are reconciled;
- B01 has a fixed independent reference;
- C01 catches last-two, first-element and i-end-only candidates;
- RPT covers cross-bracing and end-diaphragm boundaries and narrative independence.

The recovery work is genuine, provenance is now recorded, and the frozen application baseline and both databases are intact.

**Whether Phase 3 can be considered:** not yet. The engineering test suite is close to a state that could support Phase 3 consideration. Authorization should be considered only after the following harness-only items (no application source changes) are closed and independently re-verified:
- (a) restore the four Phase 2.9 logs from their twins and disclose the overwrite;
- (b) route every evidence write, including `log_test_result` and the module-global directories, through a guard that re-validates at write time;
- (c) protect every historical directory, including `phase_2_baseline` and `phase_2_repaired`, and refuse reuse of populated official directories;
- (d) implement real POSIX containment (`start_new_session=True` with `killpg`, a subreaper, and a process-tree check), and prove Windows assign-before-execute (`CREATE_SUSPENDED`);
- (e) add an independent post-run manifest verifier.

This audit does **not** authorize Phase 3.

---

*Audit artefacts (cloud workspace, disposable):*
- `/tmp/p25/g210/` — guard probes
- `/tmp/ws210u/probe210c*.py` — containment probes
- `/tmp/p25/e210/` — engineering probes
- `/tmp/p25/live210*/` — live runner captures

*All probe-created files were removed from the disposable repositories. No auditor processes remain.*
