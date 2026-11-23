# Phase 2.15 — Execution Provenance and Operational History

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge` on branch `dev` @ [`d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`](file:///F:/FOSSEE%20internship/source/OsdagBridge)  
**Controlling Audit:** Claude's Phase 2.14 Independent Gate Audit ([`reports/PHASE_2_14_FINAL_INDEPENDENT_GATE_AUDIT.md`](file:///F:/FOSSEE%20internship/reports/PHASE_2_14_FINAL_INDEPENDENT_GATE_AUDIT.md))  
**Date:** 2026-11-18  
**Status:** **OPERATIONAL READINESS VERIFIED — EXECUTION PACKAGE STAGED**  

---

## 1. Executive Summary

Phase 2.15 addresses every remaining finding and condition identified in Claude's Phase 2.14 Independent Gate Audit. The scope was strictly confined to:
1. Hardening Windows Containment Check 5 with explicit start marker verification, process liveness assertion, early termination, dynamic `time.monotonic()` delta measurements, and an uncontained positive control run producing all delayed files.
2. Formally scoping the surviving security overclaim in Section 3.2 of `PHASE_2_13_SECURITY_ARCHITECTURE.md` to Tier 2 interfaces.
3. Remedying the POSIX permission mask defect (`stat.S_IWRITE` / `0o200` to `0o600`) and root user handling in `test_evidence_governance.py` tests 10 and 22, and cleaning up dangling child subprocess handles.
4. Packaging a standalone, turnkey Independent Windows Execution Runner (`run_independent_validation.ps1` and `.bat`) and comprehensive documentation for external operator execution.

Zero application source code files under `source/OsdagBridge` were altered. Both SQLite databases remain byte-identical to their baseline hashes. The official trust ledger `trusted_run_seals.json` (6 seals, 184 files) remains completely untouched. Phase 3 was not started.

---

## 2. Chronological Provenance Ledger

| Timestamp (UTC) | Timestamp (IST) | Event / Operation | Command / Script | Exit Code | Result / Artifact Produced |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **2026-11-17T18:25:00Z** | 23:55:00 | Audit Review & Planning | Ingested `PHASE_2_14_FINAL_INDEPENDENT_GATE_AUDIT.md` and `PHASE_2_14_FINAL_REMAINING_RISKS.md` | `0` | Identified 3 gating items and non-gating portability defects |
| **2026-11-17T18:30:15Z** | 00:00:15 | Check 5 Hardening Implementation | Edited `validate_windows_containment.py` | `0` | Added Part 5A (uncontained control) & Part 5B (contained run), start markers, liveness assertions, monotonic timers |
| **2026-11-17T18:32:00Z** | 00:02:00 | Windows Containment Verification | `python -u validate_windows_containment.py` | `0` | **6 / 6 Checks PASS** (67.80s total; Part 5A created 4 files, Part 5B created 0 files). Output saved to `testing/evidence/phase_2_15/windows/` |
| **2026-11-17T18:34:00Z** | 00:04:00 | Security Overclaim Remediation | Edited `reports/PHASE_2_13_SECURITY_ARCHITECTURE.md` | `0` | Scoped §3.2 strictly to Tier 2 interfaces; added Tier 3 scope boundary alert; updated `chmod` permission references |
| **2026-11-17T18:36:00Z** | 00:06:00 | Linux Governance Portability Fix | Edited `test_evidence_governance.py` | `0` | Replaced `stat.S_IWRITE` with `RW_MODE = (stat.S_IRUSR \| stat.S_IWUSR)` in tests 10 and 22; handled root DAC; added subprocess wait cleanup |
| **2026-11-17T18:38:00Z** | 00:08:00 | Windows Governance Verification | `python -u test_evidence_governance.py -v` | `0` | **27 / 27 Vectors PASS** (17.18s, 0 skips, 0 failures, 0 errors, 0 `ResourceWarning` messages); ledger hash unchanged (`True`) |
| **2026-11-17T18:41:00Z** | 00:11:00 | Independent Package Creation | Created `run_independent_validation.ps1` and `.bat` | `0` | Standalone runner validating pre-flight hashes, executing suites, verifying post-flight ledger immutability, emitting JSON manifest |
| **2026-11-17T18:43:00Z** | 00:13:00 | Independent Package Documentation | Created `testing/evidence/phase_2_15/README_INDEPENDENT_PACKAGE.md` | `0` | Turnkey operator instructions, prerequisites, and expected outcomes |
| **2026-11-17T18:44:00Z** | 00:14:00 | Check 5 Hardening Report | Created `reports/PHASE_2_15_CHECK5_HARDENING.md` | `0` | Comprehensive technical report on Check 5 architecture and empirical findings |
| **2026-11-17T18:46:00Z** | 00:16:00 | Security Claims Report | Created `reports/PHASE_2_15_SECURITY_WORDING_CORRECTIONS.md` | `0` | Documented §3.2 wording corrections and workspace review |
| **2026-11-17T18:47:00Z** | 00:17:00 | Linux Governance Portability Report | Created `reports/PHASE_2_15_LINUX_GOVERNANCE_FIXES.md` | `0` | Detailed POSIX `0o600` permission mode fix and root handling |
| **2026-11-17T18:48:00Z** | 00:18:00 | Windows Execution Guide | Created `reports/PHASE_2_15_WINDOWS_EXECUTION_GUIDE.md` | `0` | Comprehensive external operator run guide |
| **2026-11-17T18:49:00Z** | 00:19:00 | Results Matrix Publication | Created `reports/PHASE_2_15_TEST_RESULTS.md` | `0` | Full condition, check, vector, and integrity audit matrix |

---

## 3. Evidence Artifacts Staged

All Phase 2.15 readiness evidence files are recorded in [`testing/evidence/phase_2_15/`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_15/):

| File Path | Format | Size | Description |
| :--- | :---: | :---: | :--- |
| `windows/windows_containment_validation.txt` | Text | 3.5 KB | Raw console output of `validate_windows_containment.py` (6 checks, 67.80s duration, Parts 5A and 5B) |
| `windows/transcripts/windows_containment_validation.log` | Log | 3.5 KB | Primary transcript of the containment suite execution |
| `windows/governance_test_output.txt` | Text | 7.6 KB | Raw console output of `test_evidence_governance.py -v` (27 tests, 17.18s duration, ledger hash verification) |
| `windows/transcripts/governance_test_output.log` | Log | 7.6 KB | Primary transcript of the governance suite execution |
| `run_independent_validation.ps1` | PowerShell | 7.1 KB | Standalone execution runner for external operator |
| `run_independent_validation.bat` | Batch | 0.6 KB | One-click command-prompt launcher |
| `README_INDEPENDENT_PACKAGE.md` | Markdown | 4.8 KB | Technical guide for independent operator |

---

## 4. Host Environment Specifications

- **Operating System:** Microsoft Windows 11 Enterprise (64-bit AMD64)
- **Host User Principal:** `Subodh` (standard unprivileged user)
- **Python Environment:** Conda environment `osdagbridge-py312` (`C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe`)
- **Python Version:** 3.12.16 (tags/v3.12.16:5d33f7c)
- **Git HEAD:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (dev)
- **Production Trust Ledger:** `C:\Users\Subodh\.osdagbridge_trust\trusted_run_seals.json` (SHA-256: `5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1`)
