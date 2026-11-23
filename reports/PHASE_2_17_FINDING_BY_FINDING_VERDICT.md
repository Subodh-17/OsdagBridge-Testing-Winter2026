# Phase 2.17 — Finding-by-Finding Verdict

**Execution classes:**

- **IR** = independently reproduced by me
- **AG** = Antigravity native Windows execution, inspected
- **CP** = copied output
- **CR** = code review only
- **BL** = blocked

**Reproduction locations** (cloud, disposable):

| What | Location |
|---|---|
| Runner fixtures | `/tmp/p216/run17.sh`, `/tmp/p216/o17_*.txt`, `/tmp/p216/w17_*/` |
| Check 5 | `/tmp/p25/c5/run_check5_217.py`, `/tmp/p25/c5/217_*.out` |
| Governance | `/tmp/p25/g217_user.txt`, `/tmp/p25/g217_rootcg.txt` |

Device paths are relative to `F:\FOSSEE internship`.

---

### F-1 Baseline and preservation

| Field | Content |
|---|---|
| Original claim | Baseline, ledger and 6 seals intact (preservation report §2). |
| Implementation inspected | `.git/HEAD`, `refs/heads/dev`, `logs/HEAD`, `packed-refs`; DB files; ledger; seal manifests. |
| Reproduction | Read-only on the device: `agg25.py src`, `sha256sum`; HMAC-SHA256 with the key read in place (never copied); manifest and per-file re-hash. |
| Actual result | `dev` @ `d74f56dd…`; reflog 1 entry (clone); no locks; aggregate 282 / `7c929481…`; DBs `1d767658…` / `25f97857…`; ledger `5a9b9273…f57f1` (mtime 2026-11-17 18:15:33); 6/6 seals, **184/184** files. |
| Evidence | Device; ledger `5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1` |
| Class / Severity | IR / — |
| Verdict | **ACCEPTED** |
| Limitation | Git working-tree status inferred from refs, reflog and `src` mtimes (I do not run `git status` on the device). The Antigravity run's own pre/post `git status --porcelain` reported clean (AG). |

### F-2 Phase 2.15 loss declared honestly, without fabrication

| Field | Content |
|---|---|
| Original claim | `cb5c77b9…` declared permanently lost; zero fabrication (preservation §3). |
| Implementation inspected | `reports/PHASE_2_17_EVIDENCE_PRESERVATION_REPORT.md` (9,978 B); all `*containment_validation*` files in the workspace. |
| Reproduction | Workspace-wide hash inventory; comparison with my 2.15 and 2.16 records. |
| Actual result | Loss stated plainly, with the correct origin attribution of the residual `1c7d0f98…` (2.16, Python 3.11) and `7d84341a…` (2.15 governance). No file with `cb5c77b9…` exists, and no reconstructed 2.15 transcript is present. |
| Evidence | `testing/evidence/phase_2_15/windows/*` (unchanged since 2026-11-17 19:18:03) |
| Class / Severity | IR / — |
| Verdict | **ACCEPTED** |
| Limitation | The `%TEMP%` search is an Antigravity claim (AG, not reproducible by me). |

### F-3 No further overwrite of Phase 2.15/2.16 evidence

| Field | Content |
|---|---|
| Original claim | Phase 2.15 frozen; all new evidence under `phase_2_17`. |
| Reproduction | `find -newermt` across `testing/evidence`; hashes of 2.13–2.16 transcripts and reports. |
| Actual result | Only `phase_2_17/` changed. 2.13 `3a894209`, 2.14 `3abad109` / `141b11ca`, 2.15 `7d84341a` / `1c7d0f98` are unchanged. Antigravity's 2.16 reports (`a197538a`, `9e1f33b4`, `d8ff531a`) were not edited; corrections live in the 2.17 reports. My 2.16 reports are byte-identical. |
| Class / Severity | IR / — |
| Verdict | **ACCEPTED** |
| Limitation | The 2.16 reports still contain their uncorrected claims, with no in-file pointer to the 2.17 correction (Low). No `phase_2_16/` directory exists; the 2.16 artefacts remain in `phase_2_15/windows/`, labelled in the 2.17 report. |

### F-4 Evidence guard protects every historical phase

| Field | Content |
|---|---|
| Original claim | Phases up to 2.16 are "immutable"; "eliminate any possibility of future cross-phase overwrites"; "cryptographic and filesystem-level isolation". |
| Implementation inspected | `evidence_guard.py` (`19e8223f6831c4ae…`, 49,145 B): diff against 2.15 adds `phase_2_13…phase_2_16` to `HARDCODED_PROTECTED_PHASES` and sets `ACTIVE_PHASE="phase_2_17"`. Generic rule at L95 (`phase_*` ≠ active). |
| Reproduction | (a) `validate_evidence_directory()` as non-root on a disposable copy. (b) The 2.17 runner with `-OutputDir <ws>/testing/evidence/phase_2_15/windows/new_run`. |
| Actual result | (a) `phase_2_15`, `phase_2_16` and `PHASE_2_16` were **rejected** ("CRITICAL EVIDENCE OVERWRITE BLOCKED"); `phase_2_17` was accepted. (b) **The runner wrote a full run into `phase_2_15/windows/new_run`, exit 0.** The PowerShell runner and any shell redirection bypass the Python guard, and that is exactly how the 2.16 overwrite happened. |
| Evidence | `/tmp/p216/o17_hist.txt`, `w17_hist/` |
| Class / Severity | IR / **Medium** |
| Verdict | Python gateway: **ACCEPTED**. "Every historical phase protected" / "eliminate any possibility": **REJECTED as an overclaim** (condition 2(d)). |
| Limitation | There is no filesystem-level protection (ACLs or read-only attributes) on unsealed historical phases. |

### F-5 New evidence directed to Phase 2.17

| Field | Content |
|---|---|
| Implementation | ps1 L74–77: default `testing\evidence\phase_2_17\windows\runs\run_<UTC>_<guid8>` |
| Actual result | The real run went to `phase_2_17/windows/runs/run_20261118_063946_fe82935a` (AG). Fixture runs default to the same location (IR). |
| Severity | — (see F-4 for explicit overrides) |
| Verdict | **ACCEPTED** |

### F-6 Provenance of "copy baseline transcripts to phase_2_17/windows"

| Field | Content |
|---|---|
| Original claim | Evidence tree listing (preservation §5); the copies are not identified as copies. |
| Reproduction | Hash and mtime/ctime comparison against all historical transcripts; directory mtimes. |
| Actual result | `windows/windows_containment_validation.txt`, `windows/transcripts/windows_containment_validation.log` = `088eaaae…` (7,636 B) = run file. `windows/governance_test_output.txt`, `windows/transcripts/governance_test_output.log` = `0a66f7ed…` (15,230 B) = run file. Their mtimes are preserved from the run (06:40:54 / 06:41:13); the `windows/` and `transcripts/` directory entries were created at **06:41:42**, after the manifest (06:41:14). None matches any 2.13–2.16 transcript. |
| Class / Severity | CP (of 2.17 AG output) / Low |
| Verdict | **ACCEPTED as provenance** (fresh 2.17 output, duplicated). **FINDING:** the report does not label them as copies (condition 2(e)). |
| Limitation | NTFS creation times are not visible through the bridge; the conclusion rests on hashes and directory mtimes. |

### F-7 Python and platform enforcement

| Field | Content |
|---|---|
| Original claim | "Rejects any substitute"; 3.11, mock-linux and missing interpreters are rejected. |
| Implementation inspected | ps1 L133–181: `Test-Path -PathType Leaf`; JSON probe via `cmd.exe /c "<py> -c <code> 2>nul"`; asserts `major==3 && minor==12` and `platform=="win32"`; records `executable`, `machine` and `architecture`. **No** check that `executable` equals the configured path; architecture **not** enforced; no binary hash. No PATH fallback. |
| Reproduction | PS 7.4.6 fixtures with a `cmd.exe` shim; 7 interpreters. |

| Interpreter | Result |
|---|---|
| Missing path | exit 1; failure record "not found" |
| Fake 3.9 / linux | exit 1; "version mismatch … platform mismatch" |
| Fake 3.11 / win32 | exit 1; record says "Expected 3.12.x, got 3.11.9 / platform mismatch: Expected win32, got win32" (wording bug) |
| Real CPython 3.12.16 on Linux | exit 1 (platform) |
| Non-JSON output ("3.12.16 (win32)") | exit 1 (parse failure) |
| **Spoof script printing the expected win32/3.12 JSON** | **exit 0, overall PASS**; manifest `python_executable_resolved` = the pinned conda path (spoofed) |

| Field | Content |
|---|---|
| Interpreter that ran the suites (AG) | Manifest `resolved = configured = …\osdagbridge-py312\python.exe`, 3.12.16 conda-forge, win32, AMD64. Corroborated by the containment transcript header (`sys.executable` printed by the suite process): `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe`. |
| Evidence | `/tmp/p216/o17_{missing,fake39linux,py311,real312linux,garbage,spoof}.txt`; run manifest `d0e791ef2a35efef…` |
| Class / Severity | IR + AG / **Medium** |
| Verdict | Version/platform enforcement, missing-interpreter rejection, no PATH fallback: **ACCEPTED**. "No mocked interpreter can pass by printing expected strings": **FAILS** (non-gating recommendation). Architecture check: **not implemented**. |
| Limitation | Any self-reported probe is spoofable by a deliberate same-user substitution (a Tier 3 actor). Adding `samefile(executable, configured)` and an interpreter hash pin would raise the bar. |

### F-8 Manifest of run `fe82935a`

| Field | Content |
|---|---|
| Original claim | Valid, verified manifest (Validation §3). |
| Implementation inspected | ps1 L437–569 (construction, then serialize, null check, `Set-Content -ErrorAction Stop`, existence, size and parse-back checks) |
| Reproduction | Parsed the real manifest; cross-checked against the files. |
| Actual result | JSON **object** (schema 2.17.0), run_id `fe82935a-0927-443a-b7be-aa730468d388`. Timings 06:39:45.99Z → 06:41:13.47Z (87.538 s); containment 06:39:46.85 → 06:40:54.67 (exit 0); governance 06:40:54.68 → 06:41:13.35 (exit 0). These match the file mtimes (06:40:54.65 / 06:41:13.19 / manifest 06:41:14.42). Host `HP`, profile `C:\Users\Subodh`, Windows 11 Home 10.0.26300, PS Desktop 5.1.26100.9818. Pre and post gates all true. Harness hashes equal the current device files (`19e8223f`, `e1e67cbb`, `d55754de`, `31f0ea49`). Artefact paths and hashes equal the on-disk files. `overall/test_suites/integrity_gates` = PASS/PASS/PASS. **Operator `AntigravityAgent`, mode `agent_execution`, parent `powershell` (PID 28684).** |
| Evidence | `testing/evidence/phase_2_17/windows/runs/run_20261118_063946_fe82935a/independent_run_manifest.json` `d0e791ef2a35efef…` (7,932 B) |
| Class / Severity | AG / — |
| Verdict | **ACCEPTED as a genuine, complete agent run.** **Not an independent operator run.** |
| Limitation | `operator_name` defaults to `$env:USERNAME`, and `execution_mode` defaults to `agent_execution` but is caller-selectable. Both are self-declared; `operator_execution` proves nothing on its own. The parent process name is the strongest field but is spoofable by launching through an intermediate shell. The manifest is unsigned. |

### F-9 Failure handling

| Field | Content |
|---|---|
| Original claim | C4(a)/(d) fixed. |
| Reproduction | PS 7.4 fixtures. |
| Actual result | Every preflight failure writes `preflight_failure_manifest.json` with `status=PREFLIGHT_FAILURE`, failures, environment and partial checks. The suite-failure manifest shows `FAIL/FAIL/PASS`, governance exit 3, overall exit 1. Every drift scenario gives `FAIL/PASS/FAIL`, exit 1. A manifest construction error gives exit 1 plus `MANIFEST_WRITE_FAILURE.txt` ("Manifest serialized to null or whitespace"); under Stop the same exit 1 occurs, without a note. Manifest write failure (read-only run directory) gives exit 1, no manifest, no PASS summary. **Interrupt:** no manifest and no interruption record; a partial transcript remains. |
| Evidence | `/tmp/p216/o17_{dirty,suite_fail,mutate_*,manifest_null,manifest_null_stop,ro,int}.txt` |
| Class / Severity | IR / Low (interrupt record; failure-record wording) |
| Verdict | **ACCEPTED** |
| Limitation | The preflight record and the failure note are best-effort (`SilentlyContinue`), but the exit code is always 1. |

### F-10 Operational behaviour

| Field | Content |
|---|---|
| Implementation | ps1 L310–336: `cmd.exe /c "$cmdLine 2>&1" \| Tee-Object -FilePath $OutputFile \| Out-Host`; safe `Out-String` git parsing; `.bat` uses `cd /d`, passes `%*` and propagates ERRORLEVEL. |

| Scenario | Result |
|---|---|
| Caller Stop + clean tree | PASS |
| Clean / dirty | PASS / FAIL |
| Exit-code propagation (governance exit 3) | Recorded |
| Collision | Refused; prior manifest hash `8d377883…` unchanged |
| Repeat / 3 concurrent | 3 distinct directories and manifests |
| Live output | 3 lines arrived 1 s apart, within 10 ms of emission |
| Return value | No longer polluted |

| Field | Content |
|---|---|
| PS 5.1 / paths with spaces / native stderr | **AG + CR.** The real run used PS Desktop 5.1 with workspace `F:\FOSSEE internship` (contains a space). The UTF-16LE transcripts are consistent with PS 5.1 `Tee-Object`. Exit 0 with the unittest stderr stream captured means there was no `NativeCommandError` abort. |
| Evidence | `/tmp/p216/o17_*`; run directory |
| Class / Severity | IR (PS 7.4) + AG (PS 5.1) / Low |
| Verdict | **ACCEPTED** |
| Limitation | I did **not** run Windows PowerShell 5.1 myself (BL). The Stop test in `testing/scratch/test_clean_preflight_stop.ps1` exercises a copy of the git logic, not the runner; my runner-level Stop test is PS 7.4. Transcripts are UTF-16 under 5.1 (a reader note, not a defect). |

### F-11 Check 5 provenance and containment

| Field | Content |
|---|---|
| Implementation | `validate_windows_containment.py` `d55754deb1b4cb02…` (unchanged since 2.16) |
| Reproduction | Verbatim Check 5 block against the 2.17 `evidence_guard.ProcessLifetimeJob`, under genuine cgroup2, 7 variants. |
| Actual result | baseline PASS. stale_marker_pre, stale_marker_late, forged_pid, forged_runid, premature_exit and no_termination all correctly **FAIL**. 5A provenance and mtime order True. 0 leaked cgroups. **AG:** 5A PID 6004 / RUN_ID `189f66a2…` provenance True, mtimes strictly increasing ~5/7/15 s apart. 5B PID 3616 provenance True, 1 process in the job, alive, terminated at 0.078 s, all milestones False, 32.00 s horizon, final sweep empty. 6/6. |
| Evidence | `/tmp/p25/c5/217_*.out`; transcript `088eaaae0abaef27…` |
| Class / Severity | IR + AG / — |
| Verdict | **ACCEPTED** |
| Limitation | Win32 Job Object semantics are AG + CR only. |

### F-12 Governance actually ran in Phase 2.17

| Field | Content |
|---|---|
| Original claim | 27/27 fresh. |
| Reproduction | Transcript decode (UTF-16 → UTF-8) and compare; Linux re-run with the 2.17 guard. |
| Actual result | **AG:** `0a66f7edcc9bb5e1…` (15,230 B) differs from every historical transcript; 27 test IDs, "Ran 27 tests in 18.324s", OK, **0 skipped**; written inside the manifest's governance window. **IR:** non-root Ran 27 OK (skipped=3: V9, V16, V17); root + cgroup2 Ran 27 OK (skipped=1: V16); ledger unchanged. |
| Evidence | Run directory; `/tmp/p25/g217_*.txt` |
| Class / Severity | AG + IR / — |
| Verdict | **ACCEPTED — fresh, not copied.** |
| Limitation | The "16.97 s" governance run cited in the preservation report §4 has no surviving transcript (unverified). |

### F-13 Accuracy of the Phase 2.17 reports

| Field | Content |
|---|---|
| Inspected | `PHASE_2_17_VALIDATION_RESULTS.md` (13,783 B), `…EXECUTION_PROVENANCE_REMEDIATION.md` (15,575 B), `…EVIDENCE_PRESERVATION_REPORT.md`, `…REMAINING_RISKS.md` (7,097 B) |

**Actual result — wrong vector descriptions.** §3.4 does not match the docstrings that actually ran. Examples:

| Vector | Report says | Actual test |
|---|---|---|
| V1 | "historical overwrite rejection" | missing evidence directory fails closed |
| V2 | "traversal" | direct historical path |
| V3 | "absolute path" | traversal |
| V9 | "candidates runner CLI" | ProcessLifetimeJob containment |
| V10 | "TOCTOU swap" | post-manifest tamper detection |
| V12 | "directory tampering" | `log_test_result` write |
| V13 | "non-destructive TOCTOU" | realpath symlink check |
| V15 | "never truncates" | matches, but listed as a different item |

**Actual result — other errors.**

| Claim in report | Problem |
|---|---|
| "Without mocking or emulation" | SC-04 used a mock `python.bat` |
| Manifest size 6,364 B | Actual size 7,932 B |
| SC-01–SC-04 results | Run in `%TEMP%` and deleted (`Remove-Item`); only excerpts survive |
| SC-05 | Tests a scratch replica of the git logic, not the runner |

| Field | Content |
|---|---|
| Evidence | Report text vs. transcript `0a66f7ed…` |
| Class / Severity | CR / **Medium** |
| Verdict | **REJECTED until corrected** (condition 2) |
| Limitation | The test **outcomes** are authentic; only the descriptions are wrong. |

### F-14 Documentation corrections

| Field | Content |
|---|---|
| Inspected | `PHASE_2_13_SECURITY_ARCHITECTURE.md` (18,764 B, edited 06:34), `PHASE_2_15_SECURITY_WORDING_CORRECTIONS.md` (unchanged since 2.16), `PHASE_2_15_REMAINING_RISKS.md` (6,615 B, edited 06:34), 2.17 README (8,934 B) |
| Actual result | 2.13 L121 is now qualified ("provided the adversary does not also re-seal"). The 2.15 §4 "zero software bugs or test design gaps" claim is replaced. Same-user key access is described as not prevented or detected in all security documents. README streaming, identity and attribution descriptions match the code. The loss disclosure is accurate. Copied and fresh evidence are not conflated in substance, but are unlabelled (F-6). Residual items: F-4 overclaims; 2.13 L119 "sealed and immutable" (Low). |
| Class / Severity | CR / Low |
| Verdict | **ACCEPTED**, except the F-4 / F-13 items |

### F-15 Attribution of the complete Windows execution

| Field | Content |
|---|---|
| Actual result | The full package completed (preflight, both suites, postflight, verified manifest, exit 0) under PS 5.1. It is self-attributed `AntigravityAgent / agent_execution` with parent `powershell`, and the 2.17 reports call it agent execution. |
| Class | AG |
| Verdict | **Genuine agent run, correctly attributed. NOT an independent operator run.** |
| Limitation | The separate operator execution remains **outstanding**. |

### F-16 Regression and restrictions

| Field | Content |
|---|---|
| Actual result | No source, database, ledger or seal change; no commit, push, reset or branch switch (reflog has 1 entry). Harness changes are limited to `evidence_guard.py` protected-phase constants; the other harness files are unchanged (`33a5777d`, `7cc8293d`, `e1e67cbb`, `3418069455`, `d55754de`). No Phase 3 artefacts. `.git` directory mtime 06:44:56, with no content change (transient lock from `git status`). |
| Class | IR |
| Verdict | **ACCEPTED** |
