# Phase 2.17 — Final Independent Audit

| | |
|---|---|
| **Auditor** | Claude (independent; did not implement Phase 2.17) |
| **Audit date** | 2026-11-18, 06:45–07:00 UTC |
| **Subject** | Antigravity Phase 2.17 remediation (reports 06:42–06:44 UTC) and its native Windows run `run_20261118_063946_fe82935a` |

---

## 1. Verdict

# CONDITIONALLY ACCEPTED

**The Phase 2.17 package is ready for separate operator execution.** C1–C4 from Phase 2.16 are substantially fixed, and I reproduced the fixes. Antigravity's Windows run genuinely completed the full package end to end. It is correctly self-attributed as `AntigravityAgent / agent_execution`, and **it is not an independent operator run.**

### Remaining conditions (priority order)

| # | Condition | Gating for |
|---|---|---|
| **1** | **Separate Windows operator execution** of the unchanged Phase 2.17 package (`run_independent_validation.ps1` SHA-256 `31f0ea498c7b9293…`), outside any Antigravity process tree, with the complete `runs/run_*` directory preserved and returned for independent review. | **Phase 2 closure** |
| **2** | **Correct the Phase 2.17 report misstatements** (no package change needed): (a) the 27-vector list in `PHASE_2_17_VALIDATION_RESULTS.md` §3.4 does not match the tests that actually ran; at least 8 descriptions are wrong (see F-13). (b) "executed … without mocking or emulation" contradicts SC-04's mock interpreter. (c) Manifest size is stated as 6,364 B; it is 7,932 B. (d) Remove "eliminate any possibility of future cross-phase overwrites" and "filesystem-level isolation" from the preservation report: the guard is Python-gateway only (F-4). (e) State that the four top-level `phase_2_17/windows/*` files are copies of the run's own outputs. | Phase 2 closure (documentation only; may proceed in parallel with #1) |

**Recommended (non-gating) hardening:**

- Compare the probe's `sys.executable` with the configured path, and/or pin the interpreter's SHA-256. A spoof interpreter that prints the expected JSON passes today (F-7).
- Reject an `-OutputDir` outside `phase_2_17` (F-4).
- Enforce the architecture, not just record it.
- Write an interruption record.
- Fix the failure-record text, which lists both version and platform failures even when only one failed.

### Explicit answers

| Question | Answer |
|---|---|
| 1. Is the Phase 2.17 package technically trustworthy? | **Yes, for its intended use, with documented limits.** Every gate I tested fails closed (31 fixture scenarios, PS 7.4). Manifest-failure, preflight-record, Stop-preference, collision, concurrency and live-streaming fixes all reproduce. Limits: interpreter identity and operator identity are self-reported, so they are not tamper-proof (F-7, F-8). |
| 2. Are its reported results authentic and correctly attributed? | **The run results are authentic and correctly attributed to the agent.** The manifest, transcripts, hashes, timings, harness hashes and the in-transcript `sys.executable` are mutually consistent and fresh (F-8, F-11, F-12). **The written report is not fully accurate:** the vector descriptions are wrong, and the "without mocking" claim, the manifest size and the unpreserved SC-01…SC-04 artefacts are problems (F-13). |
| 3. Is the Phase 2.15 evidence loss adequately documented? | **Yes.** It is declared permanently lost; no reconstruction exists; Phase 2.15 has not been touched since 2026-11-17 19:18 (F-2, F-3). |
| 4. Is the package ready for separate operator execution? | **Yes.** |
| 5. Has Phase 2 formally closed? | **No.** |
| 6. Is Phase 3 authorized? | **No.** |

No further remediation phase is initiated by this audit.

---

## 2. Evidence classes used

| Code | Meaning |
|---|---|
| **IR** | Independently reproduced by me: Linux cloud VM; PowerShell 7.4.6 with disposable fixtures; Python 3.12.16 under genuine cgroup2 |
| **AG** | Antigravity's native Windows execution, inspected by me |
| **CP** | Copied output (copies of the Phase 2.17 run's own files; no historical copies found) |
| **CR** | Code review only |
| **BL** | Blocked: I ran nothing natively on Windows and did not personally run Windows PowerShell 5.1 |

---

## 3. Key results

**Baseline (IR, device, read-only).** All of these are unchanged:

- `dev` @ `d74f56dd…`; reflog has 1 entry (clone); no locks; refs unchanged.
- `src` aggregate 282 / `7c929481…`.
- `weather.sqlite` `1d767658…7e98`; `Intg_osdag.sqlite` `25f97857…ea91`; ledger `5a9b9273…f57f1`.
- All 6 seals pass HMAC and manifest checks, with **184/184** files re-hashing correctly.

**Phase 2.17 run `fe82935a` (AG, inspected).**

- **Interpreter and platform:** pinned conda 3.12.16 on win32/AMD64, Windows 11 Home build 26300, PowerShell **Desktop 5.1.26100.9818**.
- **Timings:** start 06:39:45.99Z, end 06:41:13.47Z (87.5 s); containment 67.8 s (exit 0); governance 18.7 s (exit 0, "Ran 27 tests in 18.324s / OK", **0 skipped**).
- **Integrity gates:** pre and post both PASS.
- **Corroboration:** artefact hashes in the manifest match the files on disk. The transcripts are UTF-16LE, which is consistent with PS 5.1's `Tee-Object`. The Check 5 marker timestamp, 06:39:50Z, falls inside the containment window, and the in-suite header shows the pinned `sys.executable`.

**Copy provenance.** All four files in `phase_2_17/windows/{*.txt, transcripts/*}` are byte-identical to the run's own outputs (`088eaaae…`, `0a66f7ed…`). They carry preserved mtimes, and the directory entries were created at 06:41:42, after the run finished. None matches any historical transcript (2.13 `3a894209`, 2.14 `3abad109` / `141b11ca`, 2.15 `7d84341a`, 2.16 `1c7d0f98`). The phrase "copy baseline transcripts to phase_2_17/windows" therefore describes a copy of the 2.17 run's own outputs, **not** historical material passed off as fresh.

**Package (IR, PS 7.4 fixtures).**

| Scenario | Result |
|---|---|
| Missing interpreter, fake 3.9/linux, Python 3.11, real CPython 3.12 on linux, non-JSON probe | Rejected with a `preflight_failure_manifest.json` |
| Spoof interpreter printing the expected win32/3.12 JSON | **Accepted (PASS)** |
| Dirty tree; DB, git, HEAD, branch or ledger drift during the run | FAIL, exit 1, with suite and gate statuses separated |
| Manifest construction error | exit 1 plus `MANIFEST_WRITE_FAILURE.txt` |
| Manifest write failure (read-only run directory) | exit 1, no PASS summary |
| Caller `$ErrorActionPreference='Stop'` on a clean tree | PASS (fixed) |
| Live output | Suite lines reach the console as they are emitted |
| Collision | Refused; the prior manifest is unchanged |
| 3 concurrent runs | 3 distinct directories |
| Interrupt | No manifest, so it cannot report PASS |
| `-OutputDir` inside `phase_2_15` | **Accepted** |

**Check 5 and governance (IR).**

- **Check 5:** the 2.17 `evidence_guard.py` (`19e8223f…`, which adds `phase_2_13..16` to the protected list and sets `ACTIVE_PHASE=phase_2_17`) with `validate_windows_containment.py` (`d55754de…`, unchanged since 2.16) gives 7/7 correct discrimination variants under genuine cgroup2.
- **Governance as non-root:** Ran 27, OK, skipped=3 (V9, V16, V17).
- **Governance as root + cgroup2:** Ran 27, OK, skipped=1 (V16).
- The ledger was byte-identical across every run, with no leaked cgroups or probe processes.

**Documentation.**

- 2.13 L121 is now qualified: "provided the adversary does not also re-seal".
- The 2.15 §4 "zero bugs" claim is replaced.
- Same-user re-seal is acknowledged in every security document.
- Streaming documentation now matches the implementation.
- Residual problems: the preservation-report overclaims and the report errors in F-13. L119 "immutable" is Low.

**Preservation.**

- No changes to source, databases, ledger or seals.
- Phase 2.12–2.16 evidence is unchanged since my 2.16 audit.
- My 2.16 reports are byte-identical. Antigravity's 2.16 reports were left unedited, and the corrections were documented in the 2.17 reports instead.
- No commit, reset or branch switch; no Phase 3 artefacts.
- `testing/scratch/*.ps1` now exist in the workspace. They run their scenarios in `%TEMP%` and delete their outputs, so SC-01…SC-04 results survive only as excerpts in the reports.

---

## 4. Operator run: what will make it evidential

1. **Who runs it:** you or another person, from a fresh `cmd.exe` or Explorer, with no Antigravity session active. Launch it as follows:

   ```
   testing\evidence\phase_2_17\run_independent_validation.bat -OperatorName "<name>" -ExecutionMode operator_execution
   ```

2. **Do not edit the package first.** The manifest's `run_independent_validation_ps1` hash must equal `31f0ea498c7b929366a7897ab0b1693e6cc669d32673d9f60151b3e41760e183`.
3. **Keep the whole folder.** Leave the new `runs/run_*` directory untouched and do not copy files out of it.
4. **Send it for review.** I will check the manifest against the transcripts, the seals and the parent process. A parent of `cmd` or `explorer` is expected; Antigravity's shell is not.

`operator_name` and `execution_mode` are self-declared strings. They are **not proof** of independence. Independence must rest on the operator's own out-of-band confirmation together with the review in step 4.
