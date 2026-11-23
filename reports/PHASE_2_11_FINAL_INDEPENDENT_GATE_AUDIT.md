# Phase 2.11 — Final Independent Gate Audit

**Project:** FOSSEE OsdagBridge — baseline regression and sensitivity harness
**Workspace:** `F:\FOSSEE internship`
**Frozen application baseline:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`
**Audited:**
- `reports\PHASE_2_11_REMEDIATION_REPORT.md`, together with `…_PROCESS_CONTAINMENT_REPORT.md`, `…_REMAINING_LIMITATIONS.md`, `…_TEST_RESULTS.md`, `…_TEST_VALIDATION_MATRIX.md`, `…_EVIDENCE_MANIFEST.json/.md` and `…_RUN_SEALS.json`
- The harness under `testing\test_cases\baseline_regression\`

**Controlling previous audit:** `reports\PHASE_2_10_FINAL_INDEPENDENT_GATE_AUDIT.md` (SHA-256 `d8017f9041e3d585…`)
**Auditor:** Claude (independent adversarial auditor)
**Date:** 2026-11-17

**Mode:** audit only.
- Nothing in the workspace was edited, repaired, committed or pushed, apart from creating this report.
- Every probe ran in disposable clones made fresh from the baseline commit:
  - `/tmp/ws211` — guard and engineering probes, run as root;
  - `/tmp/ws211clean` — clean reproduction as root;
  - `/tmp/ws211u` — clean reproduction as non-root user `auditor`, uid 30033;
  - `/tmp/ws211p` — containment probes as non-root;
  - `/tmp/ws211s` — seal probes.
- The audit was paused once on the owner's instruction and resumed with written authorization. No probe was running while it was paused.

---

## 0. Executive verdict

# **REJECT PHASE 2.11**

Phase 2.11 makes real progress:
- the historical evidence is intact;
- the guard now refuses every direct path into a protected phase;
- B01 and RPT now catch every mutation I tried;
- a clean reproduction matches the reported counts.

The gate still fails on three independent security and containment results, none of which is a mere limitation:

1. **Linux containment fails.** A descendant that calls `setsid()` or `setpgid()`, or is spawned at interpreter exit, survived the boundary and wrote into the real application package. At 8, 15 and 30 s the FS test reported **PASS**. `start_new_session=True` plus subreaper registration does not contain the workload.
2. **The run seals are not a trust anchor.** The seal ledger is an unsigned, editable JSON file in the same workspace. Tampered evidence was accepted by `verify_manifest.py` in six of seven attack classes, including re-sealing with the harness's own `generate_and_seal_manifest`. The verifier also passes when the seal is missing, corrupt or inapplicable.
3. **The evidence gateway can be raced.** If the directory is replaced between check and open, an existing protected file is **truncated to zero bytes** before the gateway raises its TOCTOU error. The gateway is also advisory: plain `open()` and `shutil.copy` bypass it, and it lets direct calls overwrite the active, sealed Phase 2.11 evidence and write into the application source tree.

Further problems:
- The EQ/A02 "raw-input" barrier oracle reads a key the application does not use. Candidate (b) was changed to read the same invented key, so the application's real `crash_barrier_load` input is ignored by both.
- Governance Vectors 18 and 19 are tautological.
- An earlier sensitivity run and its seals are not disclosed.
- No console transcripts were captured.
- The documented fallback for a missing `--evidence-dir` crashes with `NameError`.
- Windows containment is **BLOCKED**: code review only, never executed.

| Area | Verdict |
|---|---|
| Historical recovery and integrity (2.5–2.10, the four Phase 2.9 logs, the seven earlier logs) | **ACCEPTED** |
| Two lost Phase 2.6 baseline logs | **ACCEPTED** (still documented and unchanged) |
| No historical overwrite during Phase 2.11 | **ACCEPTED** |
| Phase 2.11 manifests (96 / 17 / 17 / 54 entries) | **ACCEPTED** |
| Repository HEAD, source hashes, both databases | **ACCEPTED** |
| Gateway: protected-path refusal (CLI, direct test, logger, helper, copy, module global) | **ACCEPTED** |
| Gateway: TOCTOU directory replacement | **REJECTED** |
| Gateway: completeness (raw `open`/`copy`, active-phase and source-tree writes) | **REJECTED** |
| Missing `--evidence-dir` | **REJECTED**: the documented behaviour crashes |
| External run seals / `verify_manifest.py` | **REJECTED** |
| Linux process containment | **REJECTED** |
| Windows process containment | **BLOCKED** |
| EQ (DEF-18) | **ACCEPTED WITH LIMITATIONS**; the barrier-input oracle is **REJECTED** |
| A02 | **ACCEPTED WITH LIMITATIONS**; the barrier-input oracle is **REJECTED** |
| B01 | **ACCEPTED** |
| C01 | **ACCEPTED WITH LIMITATIONS** |
| RPT | **ACCEPTED** |
| Governance suite (22 tests) | **ACCEPTED WITH LIMITATIONS**: it passes, but Vectors 17–19 do not test what they claim |
| Official execution history and provenance | **REJECTED**: no live transcripts; an earlier run is undisclosed |
| Clean reproduction | **ACCEPTED** (counts reproduce; this does not establish acceptance) |

---

## 1. Historical recovery and integrity

### F-01 — Historical manifests (ACCEPTED, info)

| Field | Detail |
|---|---|
| Inspected | `testing/evidence/phase_2_{5..10}/hashes/manifest_hashes.json`; `phase_2_9/candidates/*`; `phase_2_11/preservation/overwritten_phase_2_9_versions/*`; `phase_2_11/preservation/PHASE_2_9_RECOVERY_REPORT.md` (4,473 B) |
| Test | Every manifest entry re-hashed on the device; mtimes of every file in every historical directory checked |
| Command | Device `python3` SHA-256 walk, read-only |
| Result: manifests | 2.5: 93/93. 2.6: 91/93 (the two known-lost baseline logs, unchanged since 11-16 18:33–18:34). 2.7: 93/93. 2.8: 91/91. **2.9: 100/100. 2.10: 96/96.** |
| Result: Phase 2.9 logs | All four restored and equal to their `_c_naive` twins: `195998d9`, `fa11727f`, `213966a3`, `28453fe8`. Those twin hashes are the values in the original Phase 2.9 manifest, which was written before the overwrite, so the twins are authentic. |
| Result: preservation | The overwritten copies (11:18:59–11:20:52, 6,048 / 2,338 / 3,100 / 3,729 B) are preserved. |
| Result: overwrite check | No file in any historical directory (`phase_1d`, `phase_2_1` … `phase_2_10`, `phase_2_baseline`, `phase_2_repaired`) was modified after 11:40 UTC. |
| Note | The restored files carry their twins' mtimes (10:07:34–10:08:17), so the restore time is visible only in the recovery report. |
| Verdict | **ACCEPTED** |

### F-02 — Phase 2.11 manifests (ACCEPTED)

| Field | Detail |
|---|---|
| Result: report manifest | `reports/PHASE_2_11_EVIDENCE_MANIFEST.json`: **96/96** entries match disk in size and SHA-256 |
| Result: baseline | `phase_2_11/baseline/manifest_hashes.json` (`88c6d197c7db5a77`): 17/17 entries, no unlisted files |
| Result: sensitivity | `phase_2_11/sensitivity/manifest_hashes.json` (`494886219d43ebd7`): 17/17, no unlisted files |
| Result: candidates | `phase_2_11/candidates/manifest_hashes.json` (`a60e85dfe3f55439`): 54/54, no unlisted files |
| Seal correspondence | Each final manifest hash and `run_uuid` matches the last seal record for its directory (`0d1ffe3c`, `3f53ab9b`, `b8e24ed7`) |
| Verdict | **ACCEPTED.** These files are internally consistent. What that consistency is worth is assessed in F-07. |

### F-03 — Repository and databases (ACCEPTED)

| Item | Observed (device, read-only, at end of audit) |
|---|---|
| HEAD | `ref: refs/heads/dev` → `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` |
| Branches | `dev` only |
| Locks | No `.git/*.lock` |
| `.git/index` mtime | 2026-11-15 12:26:18 (unchanged) |
| Source aggregate | 282 files, `7c9294813b58fb84ecd965643daec240276747d1788b13187c0e0f46c52b024c` = baseline |
| `Intg_osdag.sqlite` | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` (unchanged) |
| `weather.sqlite` (untracked) | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` (unchanged) |
| Files under `src/` modified after 11:40 UTC | 0 |

**Verdict: ACCEPTED.**

---

## 2. Centralized evidence gateway

**Implementation inspected:** `evidence_guard.py` (28,842 B, SHA-256 `3e822db682af03b485d30b867260b5e0d3a3e0c28602346aba94050b4549aca8`).
- `HARDCODED_PROTECTED_PHASES` covers `phase_1d` … `phase_2_10`, `phase_2_baseline` and `phase_2_repaired`. Every `phase_*` directory except `ACTIVE_PHASE = "phase_2_11"` is also discovered dynamically.
- `is_protected_phase_directory` checks both `realpath` and the raw path, lower-cased. On any exception it returns `False`.
- `check_write_permission`, `SafeFileWrapper`, `safe_open_evidence`, `safe_write_evidence` and `safe_copy_evidence` form the gateway.
- `_AUTHORIZED_DIRECTORIES` is populated but **never consulted**.

**Call sites:**
- `run_all_baseline_tests.py` (168,691 B, `e7cbb120bc6708a9…`): `log_test_result:217`, summary `:3078`, exit code `:3092` and seal `:3096` all go through the gateway. `--evidence-dir` defaults to `None`, with a fallback at `:3001–3005`.
- `run_sensitivity_matrix.py` (61,416 B, `447ee0da97908b31…`): gateway at `:195`, `:1336`, `:1355`; `validate_evidence_directory(..., allow_creation=True)` at `:1263–1264` (`allow_creation` is no longer honoured, so populated directories are refused).
- The FS test writes `sitecustomize.py` into its sandboxes with plain `open()` at `:2662` and `:2748` (outside the evidence tree).

Probes and outputs (sentinel hash and file count checked on disk after every probe):

| Script | Output |
|---|---|
| `/tmp/p25/g211/probe_guard.sh` | `probe_guard.out` `09c93fd81dd4eadc` |
| `probe_guard2.sh` | `probe_guard2.out` `8371dba11c960c55` |
| `probe_direct.py` | `probe_direct.out` `c80aa1c4fc27e670` |
| `probe_race.py` | `probe_race.out` `b953d26706be509d` |
| `probe_race2.py` | `probe_race2.out` `171b1e4add55309f` |

### F-04 — Protected-path refusal (ACCEPTED)

| # | Probe | Result on disk |
|---|---|---|
| G1–G4 | CLI `--evidence-dir` to `phase_2_6/baseline`; `active/../phase_2_6`; symlink `alias → phase_2_6`; `PHASE_2_6` | `PermissionError`, exit 1, sentinel intact, no directory created |
| G5–G7 | `phase_2_baseline`; `phase_2_repaired`; `phase_2_10/baseline` (even with `--allow-existing`) | `PermissionError`, sentinels intact (`21b75bac`, `65922fb1`, `8c2b050f`) |
| G9 / G10 | Sensitivity runner: populated `--candidates-dir`; `phase_2_9/candidates` | `FileExistsError` / `PermissionError`; intact |
| D1–D5 | Direct `R.test_tc_reg_a01(evidence_dir=phase_2_8/…)`; `R.log_test_result(…, phase_2_7)`; `S.CANDIDATES_DIR=phase_2_9` then `S.mut_c_a01()`; `safe_write_evidence` and `safe_copy_evidence` into `phase_2_6` | All `PermissionError`; sentinel `0fc8e976…` intact |

This closes Phase 2.10 findings G9–G14 and the alternate-entry mechanism behind the Phase 2.9 overwrite. **Verdict: ACCEPTED.**

### F-05 — TOCTOU directory replacement truncates protected evidence (REJECTED, Critical)

| Field | Detail |
|---|---|
| Inspected | `SafeFileWrapper.__init__` runs `check_write_permission` and resolves `real_path`. `__enter__` then calls `open(real_path, "w")` and only **afterwards** re-checks `realpath`. |
| Test D9 | Create the wrapper on `evidence/race/tc_reg_toctou.log` (the check passes). Then `mv race race.real; ln -s phase_2_6/baseline race`. Then enter the wrapper. |
| Command | `xvfb-run -a python /tmp/p25/g211/probe_direct.py` |
| Result D9 | The gateway raised `PermissionError: CRITICAL TOCTOU VIOLATION`, but **the protected file `phase_2_6/baseline/tc_reg_toctou.log` was already truncated: sentinel `0fc8e976…` → `e3b0c442…` (empty, 0 bytes)**. The post-open check detects the swap only after `open(…, "w")` has destroyed the content. |
| Random races D10–D12 | 3,000 symlink-flip writes, 20,000 in-process directory swaps, and 20,000 with a separate-process flipper: no corruption observed. The gateway's `makedirs` recreates the directory, which disturbs the flipper. A random race was therefore **not reproduced**; the window itself is demonstrated deterministically by D9. |
| Verdict | **REJECTED.** Detection after truncation is not protection. No `O_NOFOLLOW`, `openat` or directory-handle pinning is used. |

### F-06 — Gateway completeness and the missing `--evidence-dir` fallback (REJECTED, High)

| # | Probe | Result |
|---|---|---|
| D6 | Plain `open(p,"w")` and `shutil.copy` into `phase_2_6/baseline` from harness-process code | **Overwritten** (`0fc8e976`→`5236cd33`). The gateway is advisory; nothing enforces it. |
| D7 | `R.test_tc_reg_a01(evidence_dir=phase_2_11/baseline)` (the active, sealed official directory) | **Overwritten** (`0fc8e976`→`be1e92f0`). `phase_2_11` is unprotected, and the per-file gateway does not apply the populated-directory rule. |
| D8 | `R.log_test_result(…, evidence_dir=<application src/osdagbridge>)` | **A file was written into the application source tree** (`887b8ed8…`; removed afterwards). `_AUTHORIZED_DIRECTORIES` is never enforced. |
| G11 | `--evidence-dir evidence/scratch --allow-existing` | Populated `scratch` overwritten after an explicit opt-in (low) |
| G8 / G12 | Baseline runner with no `--evidence-dir` | **`NameError: name 'uuid' is not defined`** at `run_all_baseline_tests.py:3003`; exit 1, nothing written. It fails closed by accident; the documented "unique isolated run directory" behaviour has never run. |

**Verdict: REJECTED.**

---

## 3. External run seals

**Implementation inspected:**
- `generate_and_seal_manifest` (`evidence_guard.py:574–638`) writes `manifest_hashes.json` into the evidence directory. It then appends `{run_uuid, evidence_dir, manifest_sha256, …}` with plain `open()` (not the gateway, not atomic) to `reports/PHASE_2_11_RUN_SEALS.json`.
- `verify_manifest.py` (3,528 B, `05630d645e4c41a4…`) looks up the **newest** seal whose `evidence_dir` string matches the target. If none matches, or the ledger is missing or unparseable, `expected_seal_hash=None` and verification falls back to the manifest alone. It checks only files listed in the manifest.

**Probe:** `/tmp/p25/s211/probe_seal.sh`, output `probe_seal.out` `cd9bb9e346c99964`, run on a copy of the clean reproduction run.

### F-07 — Seals do not anchor trust (REJECTED, Critical)

| # | Attack | `verify_manifest.py` result | Correct? |
|---|---|---|---|
| S0 | Authentic run | exit 0 | ✓ |
| S1 | Evidence file modified after sealing | exit 1 (disk tamper) | ✓ |
| S2 | Ordinary manifest modified | exit 1 (manifest tamper) | ✓ |
| S3 | Evidence modified, manifest hashes recomputed, seal untouched | exit 1 | ✓ |
| **S4** | S3 plus seal ledger edited to the new manifest hash | **exit 0, "authentic and tamper-free"** | ✗ |
| **S5** | Tampered evidence re-sealed with the harness's own `generate_and_seal_manifest` (appends a newer record) | **exit 0** | ✗ |
| **S6** | `run_uuid` and timestamp replaced in the seal | **exit 0** | ✗ |
| **S7** | Evidence and manifest copied elsewhere, tampered, hashes recomputed (no seal for the new path) | **exit 0** | ✗ |
| **S8** | Extra unlisted file injected into the evidence directory | **exit 0** | ✗ |
| S9 | Listed file deleted | exit 1 | ✓ |
| **S10** | Seal ledger deleted, plus consistent tamper | **exit 0** | ✗ |
| **S11** | Seal ledger corrupted (unparseable) | **exit 0** (warning only) | ✗ |

What the seal does and does not protect:
- It protects only against someone who edits the evidence or the manifest **without** also editing a second, equally writable JSON file in the same workspace.
- Its trust anchor is **not independent** of the files it verifies: there is no signature, no key, no write-once storage, and no record outside the workspace.
- The verifier fails **open** when no seal is found.
- It is not cryptographic immutability, and the reports' description of a "cryptographic run seal" is inaccurate.

Additional observations:
- **Test pollution of the real ledger.** The device ledger holds **17 records**. **12** come from governance test runs ("Test Tamper", "Test Seal", "Test CLI Verifier"), with Windows `%TEMP%` paths, at 12:39–12:41 and again at **12:53:37–12:53:45**, after the official runs. Each governance run appends to the production ledger.
- The sensitivity runner labels its seals `runner_id: "baseline_runner"`.

**Verdict: REJECTED.**

---

## 4. Linux process containment

**Implementation inspected:**
- `ProcessLifetimeJob.__init__` calls `prctl(PR_SET_CHILD_SUBREAPER, 1)` on the **runner process**, with errors swallowed.
- `spawn()` uses `subprocess.Popen(…, start_new_session=True)` and sets `pgid = proc.pid`.
- `get_process_count()` is `killpg(pgid, 0)` → 0 or 1.
- `wait_for_job_completion(5.0)` polls that count; `terminate()` is `killpg(pgid, SIGKILL)`.

FS call site: `run_all_baseline_tests.py:2710–2725` (`spawn` → `communicate(15)` → `wait_for_job_completion(5.0)` → `terminate`), followed by Check 5 polling of the real repository for 5.0 s (`:2828`).

Analysis:
- **Only the original process group is tracked or killed.** A descendant that leaves the group with `setsid()` or `setpgid()` is invisible to `killpg`.
- The subreaper re-parents orphans to the runner, but nothing enumerates or kills them.
- There is no cgroup, PID namespace, `/proc` walk or seccomp.

**Probe:** `/tmp/ws211p/probe211c.py` (`e574f5dfbe47265e`).
- Command: `su auditor -c "cd /tmp/ws211p && HOME=/tmp/aud_home TMPDIR=/tmp/aud_tmp xvfb-run -a python probe211c.py /tmp/ws211p {A|B|C}"`
- Outputs: `/tmp/p25/live211c_A.out` `c063a3ea3fd741ea`, `_B.out` `478b25cbe13d10fb`, `_C.out` `eb3afc8351480052`.
- Method: candidate (b) FS patch plus an injected descendant that ignores SIGTERM and SIGHUP and writes into the **real** clone package after the stated delay. The package was polled until delay + 4 s.

### F-08 — Detached descendants escape and write after PASS (REJECTED, Critical)

| Descendant | 3 s | 8 s | 15 s | 30 s |
|---|---|---|---|---|
| Same process group (direct) | FAIL (detected); **no write** | FAIL; no write | FAIL; no write | FAIL; no write |
| Same group, nested (child → grandchild) | — | — | FAIL; no write | — |
| Same group, spawned at interpreter exit | — | FAIL; no write | — | — |
| **`setsid()` (direct)** | FAIL (detected by polling), **but file written to real package** | **PASS, file written** | **PASS, file written** | **PASS, file written** |
| **`setpgid(0,0)` new process group** | FAIL, **file written** | **PASS, file written** | **PASS, file written** | **PASS, file written** |
| **Nested, new session** | — | FAIL; no write | — | FAIL (parent detected), **file written at 30 s** |
| **`setsid()` spawned at interpreter exit** | — | FAIL, **file written** | — | **PASS, file written** |

- The same-process-group class is contained: detected, killed with SIGKILL, and nothing written.
- **Every class that leaves the group escaped.** Where they were "detected", the detection came from repository polling after the write, so the real package had already been modified.
- At 8, 15 and 30 s the FS test returned **PASS** while the escaped writer was still alive, and the write followed.
- The probe removed all written files afterwards. The clone ended clean (`git status` 0 lines) and no `auditor` processes remained.
- Governance Vector 17 (3 / 8 / 15 s delayed writes) passes only because its writer stays in the original group. It does not test detachment.

**Verdict: REJECTED.** Linux containment is not complete, and `start_new_session=True` with a subreaper is not containment.

---

## 5. Windows process containment

**Implementation inspected:** `ContainedPopen._execute_child` (`evidence_guard.py:274–350`) and `ProcessLifetimeJob` (Windows branch, `:360–450`, `495–560`). Scratch prototypes `testing/evidence/scratch/test_contained_popen.py` and `test_job_suspended.py` were also reviewed.

### F-09 — Windows Job Object (BLOCKED)

| Item | Code review |
|---|---|
| Job creation | `CreateJobObjectW` with checked return; `argtypes`/`restype` declared |
| Limits | `JOBOBJECT_EXTENDED_LIMIT_INFORMATION` with `KILL_ON_JOB_CLOSE` (0x2000). No `BREAKAWAY_OK` or `SILENT_BREAKAWAY_OK`, so breakaway is disallowed. |
| `CREATE_SUSPENDED` | OR-ed into `creationflags`; `_winapi.CreateProcess` is hooked |
| Assign before resume | `AssignProcessToJobObject(hJob, hProcess)` runs before `ResumeThread(hThread)`, using the handles returned by `CreateProcess` (correct) |
| Assign failure | `TerminateProcess`, close both handles, raise `PermissionError` (correct) |
| Resume failure | `0xFFFFFFFF` → terminate and raise (correct) |
| Descendant inheritance | By default, children of a job process inherit the job (correct) |
| Timeout handling | `communicate(timeout=15)` raises `TimeoutExpired`; `__exit__` → `TerminateJobObject`. The test then reports an exception, not a verdict (acceptable). |
| Completion before PASS | `wait_for_job_completion(5.0)` checks `ActiveProcesses == 0`; if not, the FS test fails and the job is terminated. A long-lived descendant would be detected and killed. |
| Concerns | The hook replaces the **module-global** `_winapi.CreateProcess` for the duration of `super()._execute_child`, which is not thread-safe. The legacy post-hoc `attach_process` still exists. Nothing is recorded to show that the official FS run used `spawn()` rather than `attach_process`. |
| Execution | **Not possible.** The auditor's device shell is a Linux VM, so no Windows process could be run. Vector 16, the only assign-before-execute test, is skipped on Linux, and no Windows output for it is preserved (F-12). |
| Verdict | **BLOCKED.** The design is correct on review but unverified. No acceptance credit is given. |

---

## 6. Engineering tests

Probe scripts and outputs (cloud, disposable `/tmp/ws211`):

| Script | Output |
|---|---|
| `/tmp/p25/e211/probe_eqa02.py` | `probe_eqa02.out` `b7bd58841d2070c6` |
| `probe_b01.py` | `probe_b01.out` `f0a52cab0c487358` |
| `probe_c01.py` | `probe_c01.out` `ff1f83e0d05a1863` |
| `probe_rpt.py` + `probe_rpt2.py` | `probe_rpt.out` `997b06e6b009e2bc` |

### F-10 — EQ and A02 barrier oracle reads a key the application does not use (REJECTED, High)

| Field | Detail |
|---|---|
| Inspected: oracles | EQ (`:1197`) and A02 (`:929`): `cb = input_dict.get("loading.crash_barrier_load", 6.54)`. EQ barrier width: `input_dict.get("typical_section.barrier_width", 0.50)`. |
| Inspected: production | The application reads `crash_barrier_load` (`geometry.py:313`, `_KEY_CRASH_BARRIER_LOAD`) and places barriers using `DEFAULT_CRASH_BARRIER_WIDTH` (`plategirderbridge.py:1019`). The input file's `typical_section.crash_barrier.width = 0.45` is not used. |
| Inspected: candidate (b) | Phase 2.11 **changed** `mut_b_eq_load_conservation` and `mut_b_a02` from `crash_barrier_load_from_inputs(self.input_dict)` to `float(self.input_dict.get("loading.crash_barrier_load", 6.54))`, i.e. the candidate was rewritten to read the oracle's invented key. |
| Governance Vectors 18 / 19 | Tautological. They assign `test_cfg["loading.crash_barrier_load"] = 8.0` and assert that `test_cfg.get(...)` returns 8.0, without ever running an oracle or production code. |
| Verdict | **REJECTED** for the barrier oracle. It is "raw input" in name only and cannot detect a failure to propagate the barrier input. |

| Probe | EQ | A02 |
|---|---|---|
| X0 candidate (b) | PASS | PASS |
| X1 **production helper `crash_barrier_dead_load_kN_m` × 0.9** | FAIL ✓ (141.3 vs 157.0 kN/line) | FAIL ✓ (CB 282.5 vs 313.9 kN) |
| X2 production helper × 1.01 | FAIL ✓ | **PASS** (inside the 1 % component tolerance) |
| **X3 genuine input `crash_barrier_load` = 8.0 (production key)** | **PASS**: candidate and oracle both ignore the real input and use 6.54 | **PASS** (same) |
| **X4 `loading.crash_barrier_load` = 8.0 (oracle key; production ignores it)** | **PASS**: both move together on a key production never reads | **PASS** |
| X5 `typical_section.crash_barrier.width` = 0.60 (production key) | PASS (neither reads it) | PASS |
| X6 `typical_section.barrier_width` = 0.60 (oracle key) | FAIL (oracle-only key) | PASS (A02 has no position check) |
| X7 barriers moved 0.06 m inboard by the application | FAIL ✓ | PASS (no position check) |
| X8 barrier intensity −1.5 % | FAIL ✓ | FAIL ✓ |

What still holds:
- Force and centroid conservation for SW, DD and DW behave as verified in Phase 2.10. The independent DD 1,249.50 / DW 216.00 / CB 313.92 kN and ULS 2,711.74 kN reproduce exactly.
- A wrong production helper is now caught.

The barrier **input** path is not tested; it is simulated with an invented key.

**Overall: EQ and A02 ACCEPTED WITH LIMITATIONS; barrier-input oracle REJECTED.**

### F-11a — B01 (ACCEPTED)

The oracle now reads all six plate dimensions and uses the general asymmetric formula. It also asserts bottom-flange width = 410 mm = top-flange width, and compares against fixed constants (A 0.025192 m², I<sub>z</sub> 7.92758 × 10⁻³, I<sub>y</sub> 2.0682 × 10⁻⁴, J 1.81663 × 10⁻⁶).

Independent check for bottom flange width 450 mm: A = 0.41 × 0.018 + 0.45 × 0.018 + 1.304 × 0.008 = **0.025912 m²**, which matches the harness value.

| Mutation | Result |
|---|---|
| Bottom flange width 410 → 450, → 412, → 408 | FAIL ✓ (closes the Phase 2.10 gap) |
| Web thickness 8 → 10 and → 8.1 mm | FAIL ✓ |
| Top flange width → 450 and → 412 | FAIL ✓ |
| Top or bottom flange thickness → 20 | FAIL ✓ |
| Depth → 1,360; web-depth key → 1,324 | FAIL ✓ |
| Solver A, I<sub>z</sub> +0.6 %; I<sub>y</sub>, J +1.2 %; J ×0.5; I<sub>y</sub> ×2 | FAIL ✓ |
| −0.4 % / −0.8 % | PASS (inside the stated 0.5 % / 1 % band) |

**Verdict: ACCEPTED.**

### F-11b — C01 (ACCEPTED WITH LIMITATIONS)

**Fixture:** two girders.
- G1, element 1, **i-end**: +200 / +1,400 / +300 / −1,500 / +100 kNm, a range of **2,900 kNm**.
- G2, element 5, **j-end**: a range of **2,700 kNm**.

**Independent stress:** composite Z<sub>b</sub> = 15.9416 × 10⁶ mm³ (short-term m = 7.5, b<sub>eff</sub> 2,100 mm, 250 mm slab) gives **181.92 MPa** and **169.37 MPa**. These match the harness values (181.914 / 169.358).

The production path still reproduces DEF-07 (static envelope 125.46 MPa).

| Mutation | Result |
|---|---|
| **i-end only, j-end only** | FAIL ✓ (closes the Phase 2.10 j-end gap) |
| First / last element only; last girder only | FAIL ✓ |
| First two / first three / last two load cases; dropping LC2 or LC4; last − first; \|M\| range; peak amplitude; shared-node raw signs | FAIL ✓ |
| Order reversal; per-end sign flip | PASS (benign) |
| **First girder only** | **PASS.** G2's untouched production value happens to fall within tolerance, so girder coverage is not discriminated. |
| Dropping LC5 (not an extremum); j and −i merged per element | PASS (not discriminated) |
| **Range ×0.985 (−1.5 %)** | **PASS** (the tolerance is now `rel_tol = 0.02`); ×0.975 FAIL |

**Verdict: ACCEPTED WITH LIMITATIONS.**

### F-11c — RPT (ACCEPTED)

The test calls the production `executive_summary` over 74 scenarios.
- Detected (FAIL), as required:
  - girder, deck, cross-bracing and end-diaphragm boundaries at 0.999 / 1.000 / 1.001, with `>=` and 1.001-threshold variants for each component;
  - narrative from overall status (Scenario 10B);
  - table copied from overall status; fail-all;
  - first, last or one-missing member and panel;
  - an efficiency read that defaults to pass when the key is missing.
- Only the sub-resolution 1.0005 threshold passes, which is acceptable.
- Inputs are synthetic dictionaries, as before.

**Verdict: ACCEPTED.**

---

## 7. Official reproduction and execution history

### F-12 — Execution history and provenance (REJECTED, High)

| Item | Finding |
|---|---|
| Live transcripts | **None.** `phase_2_11/` has no `console_output.txt` for baseline or sensitivity (Phase 2.10 had them). The 22-test governance output is not preserved anywhere in the workspace. Only `*_exit_code.txt` (`0`) and the summaries exist. |
| Earlier sensitivity run | Seals at **12:43:51** (sensitivity, manifest `824718805e11ca5b`, run `a293aa45`) and **12:43:52** (candidates, `eb4f2edd21d6d91f`, run `677d87d7`) describe evidence that no longer exists. `run_sensitivity_matrix.py` was then edited at **12:44:06**, and the run repeated at 12:44:30–12:45:36 into the same directories. Because populated reuse is refused, the first run's evidence must have been deleted in between. **None of the Phase 2.11 reports discloses the first run, its result, the code change, or the deletion.** |
| Code used by the final runs | Baseline runner last edited 12:37:40; run 12:42:07–12:42:34. Sensitivity runner edited 12:44:06; run 12:44:30–12:45:35. Guard 12:22:41; governance test 12:40:57. The final summaries record the runner and guard hashes, matching the staged files. |
| Seal correspondence | The final baseline, sensitivity and candidates seals match the final manifests (F-02). Twelve test-generated seals are interleaved, three of them after the official runs. |
| Missing `--evidence-dir` | Crashes (F-06). |

### F-13 — Independent clean reproduction (ACCEPTED, but not sufficient for acceptance)

Live capture, no reconstruction. Fresh `git clone` of `d74f56dd…`, Phase 2.11 harness files hash-verified, Python 3.12.16, Linux 6.18.44, numpy 2.5.4, `xvfb-run -a`.

| Run | User | Start (UTC) | Exit | Duration | stdout SHA-256 | Result |
|---|---|---|---|---|---|---|
| Baseline | root | 12:58:33 | 1 | 50.7 s | `28d4506c8387e16a` | 14/15; FS **BLOCKED** (root) |
| Sensitivity | root | 12:59:24 | 1 | 56.7 s | `443ca680beb28eae` | 11/12; FS UNVERIFIED |
| Governance | root | 13:00:20 | 0 | 10.1 s | `919707f6440ef920` | 22 run: 21 ok, 1 skipped (Vector 16, Windows-only) |
| Baseline | auditor | 13:35:51 | **0** | 56 s | `34bf61fa766107ed` | **15/15** |
| Sensitivity | auditor | 13:36:47 | **0** | 60 s | `2123d0ba3bb5f1c9` | **12/12**, gate PASSED |
| Governance | auditor | 13:37:47 | 0 | 10 s | `c17db4fe6e0a8764` | OK |

- stderr was 0 B for every run.
- Live captures are in `/tmp/p25/live211/` and `/tmp/p25/live211u/`.
- Afterwards both clones showed `git status` 0 lines, and the source aggregate was unchanged.

The reported 15/15 and 12/12 reproduce. They measure sensitivity against hand-written candidates. They do **not** exercise F-05, F-07, F-08 or F-10, so they are not evidence that the gate should pass.

---

## 8. Report claims versus observation

| Claim | Observation |
|---|---|
| Centralized gateway; "direct calls cannot bypass write-time realpath validation" | True for protected names. False for TOCTOU replacement (F-05), raw `open`/`copy`, the active phase and the source tree (F-06). |
| "External cryptographic run seal" | Unsigned, editable, fail-open JSON ledger (F-07) |
| POSIX: double-fork daemons "re-parented to the runner" via subreaper | They are re-parented but never killed. `setsid` and `setpgid` descendants wrote after PASS (F-08). |
| Windows assign-before-execute "Guaranteed" | Correct by design; not executed (F-09, BLOCKED) |
| EQ/A02 barrier derived from raw inputs; Vectors 18 and 19 | Invented key that production does not read; candidate rewritten to match; vectors tautological (F-10) |
| "22/22 adversarial unit tests pass" | 21 ok + 1 skipped on Linux. Vectors 17–19 do not test what they describe. |
| Missing `--evidence-dir` generates a unique run directory | Crashes with `NameError` (F-06) |
| Execution record | First sensitivity run, deleted evidence and missing transcripts not disclosed (F-12) |

---

## 9. Overall decision

# **REJECT PHASE 2.11**

The rejection rests on failed security and containment tests, not on limitations:
- F-05: protected evidence destroyed through a TOCTOU window;
- F-07: tampered evidence certified as authentic;
- F-08: detached descendants wrote into the application package after PASS.

F-10 and F-12 add integrity concerns about how the results were produced and reported.

**Phase 3:** it cannot yet be considered for authorization. The engineering suite is now close to adequate: B01 and RPT are accepted; EQ, A02 and C01 are accepted with limitations, apart from the barrier-input oracle. The remaining blockers are in the harness's evidence and containment guarantees, which Phase 3 would depend on. The decision belongs to the project owner; **this audit does not authorize Phase 3.**

---

## 10. Prioritized unresolved findings (harness-only; no application source changes)

1. **P0 — F-08 Linux containment.** Contain the whole workload, not just the process group. Use a cgroup v2 or systemd scope, or a PID namespace, and kill or verify the empty cgroup before any verdict. Otherwise classify Linux FS as BLOCKED and say so. Re-run the delayed-write matrix (3 / 8 / 15 / 30 s × same group / `setsid` / `setpgid` / nested / at exit).
2. **P0 — F-07 seal trust anchor.** Sign the seals with a key outside the workspace, or record them in write-once external storage. Make the verifier fail closed when no seal exists, the ledger is missing or corrupt, or a file is unlisted. Stop governance tests from writing to the production ledger.
3. **P0 — F-05 TOCTOU.** Open without following links and without truncating until the target is verified: `O_NOFOLLOW`, `openat` from a pinned directory handle, `O_EXCL` for new files, or write-temp-then-atomic-rename inside a verified directory handle.
4. **P1 — F-06 gateway scope.** Enforce `_AUTHORIZED_DIRECTORIES` (a write allowlist). Refuse overwrites of existing files in sealed active-phase directories. Fix the missing-`--evidence-dir` path and add a test for it.
5. **P1 — F-10 barrier oracle.** Derive the oracle from the application's real input keys (`crash_barrier_load`, `typical_section.crash_barrier.width`). Restore candidate (b) to the production input path. Replace Vectors 18 and 19 with tests that run the oracle and production.
6. **P1 — F-12 provenance.** Capture live stdout and stderr for every official and governance run. Disclose the 12:43 sensitivity run, its result, the 12:44:06 code change and the deletion of its evidence.
7. **P2 — F-09.** Execute Vector 16 and the delayed-write matrix on Windows and preserve the output. Remove the post-hoc `attach_process` path, and make the `_winapi` hook thread-safe or local.
8. **P2 — F-11b.** Tighten the C01 tolerance below 1 %, and give G2 a fixture where production's untouched value is wrong, so girder coverage is discriminated.

---

*Audit artefacts (cloud workspace, disposable):*
- `/tmp/p25/g211/` — gateway probes
- `/tmp/p25/s211/` — seal probes
- `/tmp/ws211p/probe211c.py` and `/tmp/p25/live211c_*.out` — containment probes
- `/tmp/p25/e211/` — engineering probes
- `/tmp/p25/live211*/` — live reproductions

*All probe-written files were removed from the disposable repositories. No auditor processes remain.*
