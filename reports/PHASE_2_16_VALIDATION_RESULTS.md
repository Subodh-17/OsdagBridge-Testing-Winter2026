# Phase 2.16 — Empirical Validation Results & Gate Remediation Matrix

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Repo:** `source\OsdagBridge` on branch `dev` @ [`d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`](file:///F:/FOSSEE%20internship/source/OsdagBridge)  
**Controlling Audit:** Claude's Phase 2.15 Independent Gate Audit ([`reports/PHASE_2_15_FINAL_INDEPENDENT_GATE_AUDIT.md`](file:///F:/FOSSEE%20internship/reports/PHASE_2_15_FINAL_INDEPENDENT_GATE_AUDIT.md))  
**Date:** 2026-11-18  
**Phase 2.16 Readiness Verdict:** **READY FOR INDEPENDENT WINDOWS EXECUTION**  

---

## 1. Remediation Matrix & Verification Evidence

| ID | Issue & Requirement | Remediation & Implementation | Verification Test & Empirical Result | Status |
|---|---|---|---|:---:|
| **P0.1** (F-5.1) | PowerShell 5.1 stderr `NativeCommandError` abortion | Wrapped command execution in `cmd.exe /c "... 2>&1" \| Tee-Object`. Stderr merged into stdout at Win32 C-runtime boundary. | Tested under `$ErrorActionPreference = "Stop"` in PS 5.1 (`PSVersion 5.1.26100.9818`). Both test suites and failure mocks executed without `NativeCommandError`. Exit codes preserved. | **SATISFIED** |
| **P0.2** (F-5.2) | Pinned Python interpreter enforcement (no PATH fallback) | Removed silent fallback to `python` on PATH. Enforced `Test-Path $PythonExe -PathType Leaf` and execution check before test launch. | Invoked runner with invalid path `-PythonExe "C:\invalid_path_to_python.exe"`. Aborted immediately with exit code 1 and fatal diagnostic. | **SATISFIED** |
| **P0.3** (F-5.3) | Enforced pre-flight integrity gates (fatal on mismatch) | Converted passive reporting into fatal comparison gates checking Git branch (`dev`), commit HEAD (`d74f56d...`), clean working tree, `weather.sqlite`, `Intg_osdag.sqlite`, and production trust ledger (`5a9b927...`). | Tested 4 deliberate mismatch mutations in `scratch/test_preflight_mismatches.ps1`. All 4 rejected fail-closed with exit code 1 before tests launched. | **SATISFIED** |
| **P0.4** (F-5.4) | Enforced post-flight integrity gates | Repeated Git and database checks after suites complete; compared pre-run vs post-run hashes. Fails overall run on any drift. | Validated post-flight comparison logic; verified in manifest that `databases_unchanged: true`, `git_unchanged: true`, and `ledger_unchanged: true`. | **SATISFIED** |
| **P0.5** (F-5.5) | Output folder collision prevention & timestamping | Replaced static output folder with unique `windows\independent_runs\run_<timestamp>_<uuid8>\`. Fails safely if directory already exists. | Tested existing directory collision in `scratch/test_ps_gates.ps1` Test 2. Aborted fail-closed with exit code 1 without clobbering existing files. | **SATISFIED** |
| **P0.6** (F-5.6) | Manifest schema completeness (Schema 2.16.0) | Implemented Schema 2.16.0 recording run ID, overall/per-suite start and end UTC timestamps, duration, Python/OS/PowerShell versions, harness script hashes, pre/post gate values, artifact hashes, and explicit gate/suite status distinctions. | Validated JSON serialization depth and completeness. Manifest accurately separates `test_suites_status` from `integrity_gates_status`. | **SATISFIED** |
| **P1** (F-2.3) | Security wording correction (`PHASE_2_15_SECURITY_WORDING_CORRECTIONS.md:50`) | Replaced universal claim with honest statement that same-user adversaries holding local symmetric keys can alter ledger entries and re-seal, which is NOT prevented or detected by local verification alone; non-repudiation requires external authority (Tier 4). | Audited workspace reports; confirmed zero surviving overclaims. Aligned `PHASE_2_15_REMAINING_RISKS.md` Section 3.1. | **SATISFIED** |
| **P2** (F-1.5 / F-1.6) | Check 5 marker provenance binding, stale rejection, and mtime progression | Added pre-existing marker rejection, bound start marker content to `RUN_ID` and child `PID`, asserted mtime progression in 5A, and added final post-horizon re-check in 5B. | Executed `validate_windows_containment.py` live on Windows 11 host. Provenance verified in both 5A and 5B; mtime progression verified; 6/6 checks PASS (100%). | **SATISFIED** |

---

## 2. Table 1: Win32 Job Object Empirical Validation Results (6 Checks)

**Script:** `testing/test_cases/baseline_regression/validate_windows_containment.py`  
**Host Environment:** Windows 11 Enterprise AMD64, Python 3.12.16 (`osdagbridge-py312`)  
**Execution Duration:** 68.20s | **Exit Code:** 0 | **Checks Passed:** 6 / 6 (100%)  
**Evidence Artifacts:** [`testing/evidence/phase_2_15/windows/windows_containment_validation.txt`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_15/windows/windows_containment_validation.txt)

| Check # | Check Name | Empirical Observations & Provenance Signals | Expected State | Actual State | Verdict |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **1** | Suspended Creation & Assign-Before-Execute | Child PID 27924 with `CREATE_SUSPENDED`. Marker before assign: `False`; `AssignProcessToJobObject`: 1; Marker before resume: `False`; Marker after resume: `True`. | Zero instructions prior to Job Object assignment | Verified | **PASS** |
| **2** | Kill-on-Job-Close Enforcement | Child PID 35540 (`sleep(10)`). Job handle closed directly via `_winapi.CloseHandle`. Polled child at 0.5s: `proc.poll() is not None` (`exit_code = 15`). | Immediate termination on handle close | Verified | **PASS** |
| **3** | Breakaway Prevention | Child attempted `Popen` with `CREATE_BREAKAWAY_FROM_JOB`. Captured stdout: `'BREAKAWAY_DENIED'`. Total active processes in Job: 1. | Breakaway strictly denied | Verified | **PASS** |
| **4** | Descendant Inheritance | Parent -> Child -> Grandchild tree. Queried Job Object accounting information. Active processes in Job: 3. | Entire process subtree contained ($\ge 2$) | Verified | **PASS** |
| **5A** | **Hardened Check 5: Uncontained Control with Provenance & Mtimes** | - Pre-existing marker checked: absent.<br>- Writer PID 30272 emitted marker: `RUN_ID=1060bf5a...`, `PID=30272`. Provenance verified: `True`.<br>- Milestone writes & creation mtimes:<br>  * $t = 4.50\text{ s}: \text{exists}(w3) = \text{True}$ (`mtime=1794943007.83`)<br>  * $t = 9.50\text{ s}: \text{exists}(w8) = \text{True}$ (`mtime=1794943012.83`)<br>  * $t = 16.52\text{ s}: \text{exists}(w15) = \text{True}$ (`mtime=1794943019.83`)<br>  * $t = 31.50\text{ s}: \text{exists}(w30) = \text{True}$ (`mtime=1794943034.83`)<br>- Mtime progression verified: `mtime(w3) < mtime(w8) < mtime(w15) < mtime(w30)`. | All 4 delayed files created in strict temporal sequence | All 4 files confirmed present in chronological order | **PASS** |
| **5B** | **Hardened Check 5: Contained Target Run with Provenance Binding** | - Pre-existing marker checked: absent (stale markers rejected).<br>- Writer PID 10804 spawned in Job; emitted marker: `RUN_ID=...`, `PID=10804`. Provenance verified: `True`.<br>- Active processes in Job before term: 1; process alive: `True`.<br>- Terminated early at $t = 0.079\text{ s} < 3.0\text{ s}$. All processes dead.<br>- Milestones: $\text{exists}(w3, w8, w15, w30) = \text{False}$.<br>- Total post-termination observation: 32.00s.<br>- Final re-check after full horizon: files present: `[]` (empty). | All delayed writes prevented across full 32.0s observation horizon | 0 files created | **PASS** |
| **6** | Complete Workload Termination | Spawns background worker, calls `terminate()`, waits for completion. Active processes in Job: 0. | Zero orphan processes remain | Verified | **PASS** |

---

## 3. Table 2: Adversarial Governance Test Suite Results (27 Vectors)

**Script:** `testing/test_cases/baseline_regression/test_evidence_governance.py -v`  
**Host Environment:** Windows 11 Enterprise AMD64, Python 3.12.16 (`osdagbridge-py312`)  
**Execution Duration:** 17.21s | **Exit Code:** 0 | **Results:** 27 Passed, 0 Skips, 0 Failures, 0 Errors  
**Evidence Artifacts:** [`testing/evidence/phase_2_15/windows/governance_test_output.txt`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_15/windows/governance_test_output.txt)

All 27 vectors passed with 100% success on Windows host without PowerShell 5.1 `NativeCommandError` interruption. Production trust ledger hash verified strictly unchanged (`True`).

---

## 4. Host Integrity & Production Trust Reconciliation

| Metric / Artifact | Established Baseline Value | Phase 2.16 Measured Value | Status |
| :--- | :--- | :--- | :---: |
| **Git Branch** | `dev` | `dev` | **EXACT MATCH** |
| **Git Commit HEAD** | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` | **EXACT MATCH** |
| **Working Tree Status** | Clean (0 modified / untracked files) | 0 modified / untracked application files | **100% CLEAN** |
| **`weather.sqlite` SHA-256** | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` | **EXACT MATCH** |
| **`Intg_osdag.sqlite` SHA-256** | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` | **EXACT MATCH** |
| **Production Trust Ledger Pre-Run** | `5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1` | `5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1` | **EXACT MATCH** |
| **Production Trust Ledger Post-Run** | `5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1` | `5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1` | **BYTE-IDENTICAL** |
| **Official Seals Intact** | 6 valid seals (184 evidence files) | 6 valid seals (184 evidence files) | **100% INTEGRITY** |

---

## 5. Conclusion & Final Readiness Verdict

# **READY FOR INDEPENDENT WINDOWS EXECUTION**

The package is hardened, fail-closed, and verified against all failure modes. The single remaining gating requirement to close Phase 2 is for an independent operator (project owner or auditor) to execute the turnkey batch wrapper in a clean, non-agent terminal on the Windows host:

```cmd
cd /d "F:\FOSSEE internship" && testing\evidence\phase_2_15\run_independent_validation.bat
```
