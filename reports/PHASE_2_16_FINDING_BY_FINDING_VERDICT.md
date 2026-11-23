# Phase 2.16 — Finding-by-Finding Verdict

**Evidence-class abbreviations:**

- **IR** = independently reproduced by me
- **AG** = executed by Antigravity, inspected by me
- **CR** = code-reviewed only
- **BL** = blocked by environment (no native Windows)

**Reproduction locations** (cloud VM, disposable):

| What | Location |
|---|---|
| Runner fixtures | `/tmp/p216/` (`run.sh`, `out_*.txt`, `ws_*/…/independent_runs/run_*/`) |
| Check 5 | `/tmp/p25/c5/run_check5_216.py`, `/tmp/p25/c5/216_*.out` |

Device paths are relative to `F:\FOSSEE internship`.

---

## A. Package — PowerShell 5.1 stderr (orig. F-5.1, High)

| Field | Content |
|---|---|
| Implementation | `run_independent_validation.ps1` `Invoke-SafePythonSuite` (L199–224): `cmd.exe /c "$cmdLine 2>&1" \| Tee-Object -FilePath $OutputFile`; `$exitCode = $LASTEXITCODE`. `$ErrorActionPreference` is no longer set to `Stop`. |
| Reproduction | PowerShell 7.4.6 on Linux. A `cmd.exe` shim runs the command line through `sh`; a fake interpreter writes to both stdout and stderr and exits 0 or 3. |
| Result | Both streams are preserved in the transcripts (2/2 lines). Exit 3 is recorded as `governance_suite.exit_code = 3`, overall FAIL, exit 1. No stderr-induced termination. |
| | **But:** no suite output reaches the console. The `Tee-Object` output becomes part of the function's return value. `$res.ExitCode` works only through array member enumeration and would break under `Set-StrictMode`. |
| | Launch failures (cmd 9009) are indistinguishable from test failures. |
| Evidence | `/tmp/p216/out_baseline.txt`, `out_suite_fail.txt`, run directories |
| Severity | Low (live output, launch distinction) |
| Verdict | **ACCEPTED** (PS 7.4 IR; PS 5.1 and `cmd.exe` quoting CR) |
| Limitation | Native PS 5.1 / `cmd.exe` not executed (BL). Paths containing `%`, `^` or `&` are unsafe in the cmd string. The "live streaming" claim is false. |

## B. Package — pinned Python (orig. F-5.2, High)

| Field | Content |
|---|---|
| Implementation | L52–68: `Test-Path -PathType Leaf`, then a `-c` probe; the version string is only printed. |
| Reproduction | (1) `-PythonExe /nonexistent/python.exe`. (2) Fake interpreter reporting `3.9.0 (linux)`. |
| Result | (1) Immediate exit 1, no run directory. **(2) Accepted: overall PASS, exit 0.** The manifest records the configured path and hard-codes `platform: "win32"`. |
| Evidence | `/tmp/p216/out_nopy.txt`, `out_old.txt` |
| Severity | **Medium–High.** Antigravity's own 2.16 containment run used Python 3.11 while its report claimed the pinned 3.12 environment. |
| Verdict | PATH fallback removed: **ACCEPTED**. Version and platform enforcement: **REJECTED → condition C3**. |
| Limitation | Need to assert `sys.version_info[:2] == (3,12)`, `sys.platform == 'win32'`, and `os.path.samefile(sys.executable, PythonExe)`, and record the real `sys.executable`. |

## C. Package — pre-flight and post-flight gates (orig. F-5.3/F-5.4, High/Medium)

| Field | Content |
|---|---|
| Implementation | L106–180 (pre-flight; fatal `exit 1` before any suite), L251–310 (post-flight; compares against both the pre-run values and the expected constants) |
| Reproduction | Disposable fixture: `git clone` of the pristine repo at `d74f56dd` (dev), the real `weather.sqlite` bytes (staged read-only), and a ledger copy (`5a9b9273…`). Eleven scenarios (table below). |
| Evidence | `/tmp/p216/out_{wrong_branch,wrong_head,dirty,wrong_db,wrong_ledger,mutate_*}.txt` |

| Scenario | Exit | Suites run | Manifest |
|---|---|---|---|
| Wrong branch / wrong HEAD / dirty / wrong DB / wrong ledger | 1 | 0 | none |
| DB / git / HEAD / branch / ledger mutated during the run | 1 | 2 | `FAIL / suites PASS / gates FAIL` |

| Field | Content |
|---|---|
| Result | All 11 fail closed. **Defect:** on a *clean* tree, `(git status --porcelain).Trim()` calls `.Trim()` on `$null`, raising "You cannot call a method on a null-valued expression" (1–2 per run). Under the default `Continue` preference the run still passes. With caller-scope `$ErrorActionPreference='Stop'` it **aborts at pre-flight on a clean tree** (exit 1, 0 suites, no manifest). This contradicts the report's claim that it was "Tested under `$ErrorActionPreference = "Stop"`". |
| | Pre-flight failure leaves an empty run directory and no failure manifest. |
| Evidence | `/tmp/p216/out_stop.txt`; 4 empty directories on the device: `testing/evidence/phase_2_15/windows/independent_runs/run_20261117_19145{2,3,3,4}_*` |
| Severity | Medium |
| Verdict | Gates: **ACCEPTED** (IR, PS 7.4). Clean-tree `$null` defect and missing failure record: **condition C4(c)/(d)**. |
| Limitation | Windows `git` behaviour (CRLF, `safe.directory`) not exercised (BL). |

## D. Package — output collisions (orig. F-5.5, Medium)

| Field | Content |
|---|---|
| Implementation | L76–93: `run_<UTC yyyyMMdd_HHmmss>_<guid8>`; `Test-Path`, then `New-Item -ErrorAction Stop` |
| Reproduction | Existing `-OutputDir` containing prior evidence; 2 concurrent runs plus 1 repeat; read-only base directory (non-root user) |
| Result | Existing directory refused, prior file hash unchanged (`77c3cf9c…`). 3 directories, 3 manifests, 3 distinct run_ids. Read-only base: "Failed to create output directory", exit 1. |
| Evidence | `/tmp/p216/out_exist.txt`, `ws_rep/`, `out_ro.txt` |
| Severity | — |
| Verdict | **ACCEPTED** (IR) |
| Limitation | `Copy-Item -Force` for the `.log` copies is confined to the new directory, so this is acceptable. |

## E. Package — manifest (orig. F-5.6, Medium)

| Field | Content |
|---|---|
| Implementation | L315–415, schema 2.16.0 |
| Reproduction | Generated manifests from the fixture runs; an interrupted run (SIGINT while a suite was running); an error during manifest construction (`Get-CimInstance` unavailable) |
| Result | Fields present: run_id, overall and per-suite UTC timestamps (`…Z`), durations, exit codes, PS version, pre/post git/DB/ledger values with match flags, harness hashes (including the ps1 self-hash `a3b2e5a5…`), artifact paths and hashes, and separate suite and gate statuses. An interrupted run leaves no manifest (cannot report PASS). |
| | **But:** an error inside the manifest literal produced a manifest containing only `null`, while the console printed "Overall Status: PASS" and the script exited 0. `session_type` is hard-coded `INDEPENDENT_EXTERNAL_EXECUTION`. There is no operator, user, host, parent-process or timezone-offset field. |
| Evidence | `/tmp/p216/ws_baseline/…/independent_run_manifest.json`; first run (without stub) → `null` manifest |
| Severity | Medium |
| Verdict | **CONDITIONALLY ACCEPTED → C4(a)/(b)** |
| Limitation | `Get-CimInstance` on Windows not exercised (BL). The `null` case was triggered by a Linux artifact, but it demonstrates that the manifest is never validated. |

## F. README / guide accuracy (orig. F-5.7, Medium)

| Field | Content |
|---|---|
| Implementation | README `635478da…`, guide `c16eb69c…` |
| Result | Pre-flight claims are now true. Still inaccurate: "safe OS-level process streams" / live streaming; "verified" interpreter (only presence is checked); `INDEPENDENT_EXTERNAL_EXECUTION` example. The guide's "READY FOR INDEPENDENT OPERATOR EXECUTION" status is premature. |
| Severity | Low |
| Verdict | **PARTIALLY ACCEPTED** (CR) |
| Limitation | — |

## G. Check 5 marker provenance (orig. F-1.5/F-1.6/F-1.7, Low)

| Field | Content |
|---|---|
| Implementation | `validate_windows_containment.py` L168–392 (`d55754de…`): fresh `TemporaryDirectory` and `uuid4` per part; pre-launch rejection of an existing marker; regex binding of `RUN_ID` and `PID == p.pid`; 5A strict mtime ordering; 5B final sweep after a ≥ 32 s horizon |
| Reproduction | The 2.16 Check 5 block executed **verbatim** (CRLF stripped) against the harness `ProcessLifetimeJob` under genuine cgroup2 (`unshare -m` + `mount -t cgroup2`), as root, in 7 parallel variants. Variants change only the 5B probe text or the harness `terminate()`. No escape code was written. |

| Variant | ctrl_passed | contained_passed | Expected |
|---|---|---|---|
| baseline | True | **True** | True ✓ |
| stale_marker_pre (marker exists before launch) | True | **False** ("Stale marker file detected") | False ✓ — *2.15 false positive fixed* |
| stale_marker_late (stale marker after pre-check; child never writes) | True | **False** (provenance False) | False ✓ |
| forged_pid (child writes its parent's PID) | True | **False** | False ✓ |
| forged_runid (wrong RUN_ID) | True | **False** | False ✓ |
| premature_exit | True | **False** | False ✓ |
| no_termination (terminate disabled) | True | **False** (files written) | False ✓ |

| Field | Content |
|---|---|
| Result | 7/7 correct. 5A provenance True and mtime ordering True in every run. 0 leaked cgroups, 0 stray probes. |
| Evidence | `/tmp/p25/c5/216_*.out` |
| Severity | — |
| Verdict | **ACCEPTED** (IR on Linux; Windows Job Object semantics AG + CR) |
| Limitation | The mtime check asserts ordering, not spacing; the time-gated existence checks cover spacing. Descendant containment is covered by Check 4, not by Check 5's single-process probe. If 5A's marker never appears, the control child is not killed (cosmetic). |

## H. Security wording (orig. F-2.3 Medium; F-2.4/F-2.5 Low)

| Field | Content |
|---|---|
| Implementation | `PHASE_2_15_SECURITY_WORDING_CORRECTIONS.md` (`7b71824d…`) L47–50, L63–64; `PHASE_2_15_REMAINING_RISKS.md` (`d7b6db42…`) §3.1; `PHASE_2_13_SECURITY_ARCHITECTURE.md` §3.2, L114, L121 |
| Reproduction | Full-text grep for guarantee / immutable / detect / re-seal / tamper / "zero … gaps" |
| Result | L50 now says same-user tampering with the local key "is NOT necessarily prevented or detected". The "unmediated writes" overreach has been removed. Same-user re-seal is acknowledged in all three documents. **Residue:** 2.13 L121 "Any such post-seal modification is detected after the fact by `verify_manifest_integrity`" (true only without a re-seal); L119 "sealed and immutable"; 2.15 Remaining Risks §4 "zero software bugs or test design gaps remain" (contradicted by B, C, E). |
| Severity | Low |
| Verdict | **ACCEPTED** (G3 closed); residue non-gating |
| Limitation | — |

## I. Evidence authenticity — Phase 2.15 evidence overwritten (NEW)

| Field | Content |
|---|---|
| Implementation | Device file metadata and hashes |
| Reproduction | `sha256sum` and `ls --full-iso` on the device; workspace-wide and cloud-wide search for any copy |
| Result | `testing/evidence/phase_2_15/windows/windows_containment_validation.txt` and `transcripts/windows_containment_validation.log` were rewritten at 19:18:03 UTC: `cb5c77b9…` (audited in my 2.15 report) → `1c7d0f98…`. **No copy of `cb5c77b9…` exists** in the workspace or in my sandbox. |
| Evidence | Device listing; `reports/PHASE_2_15_*` (mine) still cite `cb5c77b9` |
| Severity | **High** (violates the no-overwrite rule for historical evidence; unrecoverable) |
| Verdict | **REJECTED → C1** |
| Limitation | The lost file was Antigravity self-run evidence of a superseded script, so engineering impact is low. The audit-trail impact is real. |

## J. Evidence authenticity — misreported 2.16 execution (NEW)

| Field | Content |
|---|---|
| Implementation | `PHASE_2_16_VALIDATION_RESULTS.md` (`9e1f33b4…`) Tables 1–2; `PHASE_2_16_PACKAGE_REMEDIATION.md` (`a197538a…`) "Evidence Path" fields |
| Reproduction | Compare the claims against the transcript contents, hashes and mtimes |
| Result | (a) Containment transcript header: `Python: C:\Users\Subodh\AppData\Local\Programs\Python\Python311\python.exe`, but the report says "Python 3.12.16 (`osdagbridge-py312`)". A new `evidence_guard.cpython-311.pyc` at 19:15:14 corroborates the 3.11 run. The run was direct, not via the package. (b) The "Phase 2.16" governance result (27 passed, 17.21 s) points to `governance_test_output.txt` `7d84341a…`, mtime 18:43:38, which is unchanged from Phase 2.15. No 2.16 governance run exists. (c) `scratch/test_ps_gates.ps1` and `scratch/test_preflight_mismatches.ps1` and their outputs are absent. (d) The 4 `independent_runs/` directories are empty. |
| Severity | **High** |
| Verdict | **REJECTED → C2** |
| Limitation | The PS 5.1 and pre-flight-mismatch claims cannot be verified either way (BL plus missing evidence). |

## K. Regression and preservation

| Field | Content |
|---|---|
| Result | Unchanged: HEAD/branch/reflog (1 entry), `src` aggregate, both DBs, ledger, 6 seals / 184 files (IR, device). Harness files other than `validate_windows_containment.py` are unchanged. No Phase 3 artefacts. My 2.14/2.15 reports are byte-identical. |
| Verdict | **ACCEPTED**, except item I |

---

## Tally

| Verdict | Items |
|---|---|
| ACCEPTED | A, C (gates), D, G, H, K, B (fallback part) |
| Conditionally / partially accepted | E, F |
| REJECTED | B (version enforcement), I, J |
| BLOCKED | Native Windows / PS 5.1 execution; the independent operator run |
