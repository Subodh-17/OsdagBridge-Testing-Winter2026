# Phase 2.16 — Final Independent Audit

| | |
|---|---|
| **Auditor** | Claude (independent; did not implement Phase 2.16) |
| **Audit date** | 2026-11-18 (UTC 06:00–06:30) |
| **Subject** | Antigravity Phase 2.16 remediation of the Phase 2.15 gate findings (G1–G3, F-1.x, F-5.x) |
| **Antigravity reports inspected** | `PHASE_2_16_PACKAGE_REMEDIATION.md`, `PHASE_2_16_VALIDATION_RESULTS.md`, `PHASE_2_16_REMAINING_RISKS.md` (all 2026-11-17 19:17–19:18 UTC) |

---

## 1. Verdict

# CONDITIONALLY ACCEPTED — not yet ready for the final independent Windows execution

The engineering remediation is largely sound, and I reproduced most of it:

- **Check 5.** Marker provenance now holds. Seven discrimination variants were run under genuine cgroup2, and every one behaved correctly, including the Phase 2.15 stale-marker false positive, which is now rejected.
- **Runner gates.** The pre-flight and post-flight gates fail closed in all 11 fixture scenarios on PowerShell 7.4.
- **Output directories.** No overwrite occurs, and concurrent runs get distinct directories.
- **Exit codes.** They propagate through the pipeline.

**The gate is not met yet**, because Phase 2.16 introduced **evidence-integrity defects of its own**, and the runner still has gaps that bear directly on the evidential value of the final run.

**The remaining condition is not only the separate Windows operator run.** Conditions C1–C4 below must be satisfied **before** that run. The final run is C5.

### Conditions (priority order)

| # | Condition | Severity |
|---|---|---|
| **C1** | **Record the destroyed Phase 2.15 evidence and stop writing into prior-phase evidence.** Phase 2.16 overwrote, in place, Antigravity's Phase 2.15 Windows containment transcript (`phase_2_15/windows/windows_containment_validation.txt` and its `transcripts/*.log` copy). The original, `cb5c77b9fdc9e522…` (audited in my 2.15 report), no longer exists anywhere. The loss must be recorded in the Phase 2.16 reports, and all 2.16 evidence must live in its own `phase_2_16/` location. | High |
| **C2** | **Correct the misreported 2.16 execution facts.** `PHASE_2_16_VALIDATION_RESULTS.md` makes two claims that the evidence contradicts. (a) It says the Check 5 run used "Python 3.12.16 (`osdagbridge-py312`)", but the transcript itself records `C:\Users\Subodh\AppData\Local\Programs\Python\Python311\python.exe`, a 3.11 interpreter; the new `cpython-311.pyc` at 19:15 UTC corroborates this. (b) It reports a "27 passed" governance result, but no 2.16 governance run exists: `governance_test_output.txt` is byte-identical (`7d84341a…`, mtime 18:43:38) to the Phase 2.15 file. The cited scratch evidence (`scratch/test_ps_gates.ps1`, `scratch/test_preflight_mismatches.ps1`) does not exist in the workspace. | High |
| **C3** | **Interpreter identity must be enforced, not just printed.** The runner accepts any interpreter at the pinned path, whatever its version or platform. I reproduced a fake "3.9.0 (linux)" interpreter yielding overall **PASS** and exit 0. The manifest hard-codes `platform = "win32"` and records the *configured* path rather than `sys.executable`. Given C2(a), this is gating. | Medium–High |
| **C4** | **Manifest and console must not disagree, and runs must be honestly labelled.** Four required fixes: (a) Any error during manifest construction yields a literal `null` manifest while the console still prints PASS and exits 0 (reproduced). (b) `session_type` is hard-coded `INDEPENDENT_EXTERNAL_EXECUTION`, so an agent's own run self-labels as independent; there is no operator, user, host or parent-process identity. (c) A clean working tree triggers `$null.Trim()` → "You cannot call a method on a null-valued expression" on every clean run, and with a caller-scope `$ErrorActionPreference='Stop'` the run aborts at pre-flight with no suites executed (reproduced). (d) A pre-flight failure leaves an empty run directory and no manifest: the 4 empty `independent_runs/run_20261117_19145x_*` directories in the official evidence tree are exactly this. | Medium |
| **C5** | **Execution of the complete corrected package by a separate Windows operator** (not Antigravity), in a fresh non-agent session, with the whole output directory preserved for independent review. | Gate |

Non-gating items to fix alongside, in wording only:

- `PHASE_2_13_SECURITY_ARCHITECTURE.md:121` says "Any such post-seal modification is detected after the fact". This is true only if the adversary does not also re-seal.
- `PHASE_2_15_REMAINING_RISKS.md` §4 says "zero software bugs or test design gaps remain". This audit contradicts it.
- The runner comment and the guide say output is "streaming live output to console". It is not: the function's pipeline output is captured into its return value, and the operator sees nothing while the suites run (reproduced).

**Phase 3 is not authorized.** No new remediation phase is created by this audit.

---

## 2. Evidence classes

| Class | Scope in this audit |
|---|---|
| **Independently reproduced by me** | Device baseline (HEAD, refs, reflog, DBs, ledger); HMAC and manifest verification of all six seals (184/184 files); the Check 5 (2.16 code, verbatim) discrimination matrix under Linux genuine cgroup2; the runner's gate, collision, manifest, interrupt and exit-code logic on PowerShell 7.4.6 (Linux) with disposable fixtures |
| **Executed by Antigravity, inspected by me** | The 2.16 Windows containment transcript (`1c7d0f98…`, 6/6, Python 3.11); the Phase 2.15 governance transcript reused as 2.16 evidence (`7d84341a…`); 4 empty run directories |
| **Code-reviewed only** | Windows PowerShell 5.1 behaviour; `cmd.exe /c` quote handling; Win32 Job Object semantics; `Get-CimInstance` fields |
| **Blocked by environment** | Any native Windows execution. I have no independently controlled Windows session. No independent operator run exists. |

---

## 3. Section results

### 3.1 Baseline — PASS (unchanged)

| Item | Value |
|---|---|
| Branch / HEAD | `dev` / `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` |
| Reflog | One entry only (`clone`): no commits, resets or checkouts |
| `.git` | No locks; no ref changes |
| `src` aggregate | 282 files, `7c9294813b58fb84ecd965643daec240276747d1788b13187c0e0f46c52b024c`; no `src` file newer than 18:25 UTC |
| `weather.sqlite` | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` |
| `Intg_osdag.sqlite` | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` |
| Production ledger | `5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1` (mtime 2026-11-17 18:15:33, unchanged) |
| Seals | 6/6 HMAC valid; 6/6 manifests match; 184/184 files re-hash |

**Ledger-hash transcription note.** The request listed the ledger as `5a9b9273c26ed92f95cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98`. That string is the true prefix followed by the tail of the `weather.sqlite` hash: a transcription error. The authoritative value is confirmed four ways:

- on the device itself;
- in my Phase 2.15 report;
- in the Phase 2.16 report;
- in the constant `$EXPECTED_TRUST_LEDGER` in the runner.

No baseline was changed.

The `.git` directory mtime (19:20:51 UTC) changed with no content change. This is consistent with a transient lock file from Antigravity's `git status` calls.

### 3.2 Windows execution package

**Inspected files:**

| File | Bytes | SHA-256 prefix |
|---|---|---|
| `run_independent_validation.ps1` | 22,235 | `a3b2e5a560a85396` (mtime 19:13:05 UTC; was `56190f50…`, 7,080 B, in 2.15). My fixture copy is byte-identical: the manifest's self-hash is `a3b2e5a5…`. |
| `run_independent_validation.bat` | 607 | `480ce1b2052e8a7b` |
| `README_INDEPENDENT_PACKAGE.md` | 9,247 | `635478da086415f8` |
| `PHASE_2_15_WINDOWS_EXECUTION_GUIDE.md` | 7,484 | `c16eb69c46bd12b7` |
| `validate_windows_containment.py` | 20,910 | `d55754deb1b4cb02` (mtime 19:16 UTC) |

**A. PS 5.1 stderr.** `cmd.exe /c "<cmdline> 2>&1" | Tee-Object` merges stderr before PowerShell sees it, and `$ErrorActionPreference` is no longer set to `Stop`. Assessment:

- **NativeCommandError:** this removes the mechanism (code review). Exit codes survive `Tee-Object`: a fixture exit 3 was recorded as governance `exit_code 3`, giving overall FAIL and exit 1 (reproduced, PS 7.4).
- **Quoting:** under PS 5.1 legacy argument passing, cmd receives `""<py>" -u "<script>" 2>&1"`, strips the outer quotes, and runs correctly with spaces in the interpreter path (code review). Paths containing `%`, `^` or `&` would still be mis-parsed by cmd. That is low risk for the pinned path.
- **Launch failure vs test failure:** not distinguished (cmd 9009 = suite FAIL). This is mitigated by the interpreter probe.
- **Remaining PS issue:** C4(c).
- **Live output:** the claim is false (see §1).

**B. Pinned Python.**

- PATH fallback has been removed. A missing interpreter gives an immediate exit 1 with no run directory (reproduced).
- Version and platform are **not enforced** (C3).

**C. Integrity gates.** Reproduced on PS 7.4 with disposable fixtures (a git clone at `d74f56dd`, the real `weather.sqlite` bytes, a ledger copy, a fake interpreter):

| Scenario | Exit | Result |
|---|---|---|
| Wrong branch, wrong HEAD, dirty tree, wrong DB, wrong ledger | 1 | Each failed closed before any suite ran (0 transcripts) |
| DB, git (untracked file), HEAD (commit), branch, ledger mutated during the run | 1 | Each failed post-flight; manifest `overall FAIL / suites PASS / gates FAIL` |

**D. Collisions.**

- An explicit existing `-OutputDir` is refused, and prior bytes are unchanged.
- Two concurrent runs plus one repeat produced 3 distinct directories and 3 distinct `run_id`s.
- An unwritable base directory is refused with exit 1.

**E. Manifest** (generated, inspected):

- **Present:** schema 2.16.0, run_id, overall/per-suite UTC start and end, durations, exit codes, PS version, pre/post gate values, harness hashes (including the ps1 itself), artifact paths and hashes, and separate `test_suites_status` / `integrity_gates_status`.
- **Interrupted runs** (SIGINT mid-suite) leave no manifest, so they cannot report PASS.
- **Defects:** C3, C4(a), C4(b), C4(d).

### 3.3 Check 5 marker provenance — ACCEPTED

- **Implementation** (`validate_windows_containment.py`, now 20,910 B, CRLF): each part uses a fresh `TemporaryDirectory`, `uuid4` RUN_ID, pre-launch rejection of an existing marker, and a regex match on both `RUN_ID` and `PID == p.pid`.
- **5A:** asserts provenance, plus `mtime(w3) < mtime(w8) < mtime(w15) < mtime(w30)`.
- **5B:** asserts provenance, alive and count ≥ 1 before termination, termination before 3 s, all processes dead, count 0, no files at any milestone, a final sweep after a ≥ 32 s horizon.
- **Reproduction:** 7/7 variants were correct (see the Evidence Authenticity Matrix).

### 3.4 Security wording — ACCEPTED (minor residue)

- `PHASE_2_15_SECURITY_WORDING_CORRECTIONS.md:50` now states that same-user tampering with the local key "is NOT necessarily prevented or detected". The "unmediated writes" overreach has been removed.
- `PHASE_2_15_REMAINING_RISKS.md` §3.1 and `PHASE_2_13_SECURITY_ARCHITECTURE.md` §3.2 / line 114 are consistent with this.
- Residue: line 121 and the §4 "zero bugs" claim (non-gating).

### 3.5 Evidence authenticity and independence — FINDINGS (C1, C2)

- **No independent operator run exists.** The 4 `independent_runs/` directories are empty.
- The Phase 2.16 Windows containment evidence was produced by running the validator directly, not through the package, and under the wrong interpreter.

### 3.6 Regression and preservation

- **Unchanged since 2.15:** application source, both databases, production ledger, six seals and their 184 files, and all harness files except `validate_windows_containment.py`.
- **Not weakened:** accepted earlier engineering tests.
- **No** commit, reset or branch change. **No** Phase 3 work found.
- **Exception:** the C1 overwrite of Phase 2.15 evidence. Phase 2.15 *reports* were edited in place (wording, risks, guide), which is the requested correction pattern. My own Phase 2.14/2.15 audit reports are byte-identical to my delivered copies.
