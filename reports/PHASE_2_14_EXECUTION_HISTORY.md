# Phase 2.14 — Execution Provenance & Operational History

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge` on branch `dev` @ [`d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`](file:///F:/FOSSEE%20internship/source/OsdagBridge)  
**Controlling Audit:** Claude's Phase 2.13 Independent Gate Audit ([`reports/PHASE_2_13_FINAL_INDEPENDENT_GATE_AUDIT.md`](file:///F:/FOSSEE%20internship/reports/PHASE_2_13_FINAL_INDEPENDENT_GATE_AUDIT.md))  
**Date:** 2026-11-17 (UTC / IST)  
**Status:** **SATISFIED**

---

## 1. Executive Summary

Phase 2.14 is strictly a harness-validation, evidence-governance isolation, and documentation precision phase. In accordance with Claude's CONDITIONAL ACCEPTANCE verdict in Phase 2.13, work was strictly confined to closing the three specified conditions:
1. Actual Windows empirical validation (Job Object containment across full 32s horizon + 27/27 governance attack vectors).
2. Correcting security claims regarding read-only attributes, kernel protection, and non-repudiation.
3. Isolating governance tests from production trust and non-destructively pruning stray test entries from `trusted_run_seals.json`.

Zero application source files under `source/OsdagBridge` were modified. Zero database records were altered. Phase 3 was not authorized or started.

---

## 2. Chronological Provenance Ledger

| Timestamp (UTC) | Timestamp (IST) | Event / Operation | Exact Command / Script | Exit Code | Result / Artifact Produced |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **2026-11-17T18:10:00Z** | 23:40:00 | Controlling Audit Ingestion | Read `reports/PHASE_2_13_FINAL_INDEPENDENT_GATE_AUDIT.md`, `PHASE_2_13_FINDING_BY_FINDING_VERDICT.md`, `PHASE_2_13_REPRODUCTION_RESULTS.md`, `PHASE_2_13_REMAINING_RISKS.md` | `0` | Identified 3 mandatory conditions |
| **2026-11-17T18:10:30Z** | 23:40:30 | Trust Ledger Forensic Inspection | Python script inspecting `C:\Users\Subodh\.osdagbridge_trust\trusted_run_seals.json` | `0` | Analyzed 10 entries; identified 6 official and 4 scratch entries |
| **2026-11-17T18:11:50Z** | 23:41:50 | Transcript Provenance Matching | Python search of `transcript.jsonl` matching lines 8859, 8868, 8871, 8873 | `0` | Conclusively proved Entries 3-6 originated from manual interactive Phase 2.13 test one-liners |
| **2026-11-17T18:15:32Z** | 23:45:32 | Non-Destructive Ledger Pruning | Python ledger pruning script | `0` | Recorded pre-hash `c10febe...`; backed up to `.bak_phase_2_13`; pruned 4 scratch entries; recorded post-hash `5a9b927...` |
| **2026-11-17T18:15:40Z** | 23:45:40 | Re-Verification of All Official Runs | `verify_manifest.py` on Phase 2.12 and 2.13 baseline, sensitivity, candidates | `0` | 92 / 92 files verified with 100% cryptographic integrity; zero drift |
| **2026-11-17T18:16:40Z** | 23:46:40 | Governance Test Suite Isolation | Edited `test_evidence_governance.py` | `0` | Isolated trust dir in `setUp`; explicit parameter passing in `test_10`, `test_22`, `test_24`; automated hash assertion in `tearDown` |
| **2026-11-17T18:17:19Z** | 23:47:19 | Windows Containment Empirical Validation | `validate_windows_containment.py` live on Windows host | `0` | 6 / 6 checks PASSED in 35.73s; observed full 32s horizon; output saved to `windows_containment_validation.txt` |
| **2026-11-17T18:18:18Z** | 23:48:18 | Adversarial Governance Suite Execution | `test_evidence_governance.py -v` live on Windows host | `0` | 27 / 27 vectors PASSED in 17.60s; verified production ledger unchanged (`True`); output saved to `governance_test_output.txt` |
| **2026-11-17T18:19:00Z** | 23:49:00 | Security Claims Documentation Corrections | Edited `PHASE_2_13_REMEDIATION_REPORT.md`, `PHASE_2_13_SECURITY_ARCHITECTURE.md`, `evidence_guard.py` | `0` | Eliminated "kernel-level", "complete non-repudiation", and overstated read-only claims |
| **2026-11-17T18:21:00Z** | 23:51:00 | Deliverables Publication | Created 6 Phase 2.14 reports in `reports/` | `0` | Documented validation, isolation, security claims, history, results, and remaining risks |

---

## 3. Evidence Artifacts & Transcripts Inventory

All evidence artifacts generated during Phase 2.14 reside exclusively in `testing/evidence/phase_2_14/windows/`:

| Artifact Path | Format | Size | Description & Contents |
| :--- | :---: | :---: | :--- |
| [`testing/evidence/phase_2_14/windows/windows_containment_validation.txt`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_14/windows/windows_containment_validation.txt) | Text | 3.5 KB | Complete live stdout/stderr of `validate_windows_containment.py` (6 checks, 35.73s duration, 32s horizon) |
| [`testing/evidence/phase_2_14/windows/transcripts/windows_containment_validation.log`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_14/windows/transcripts/windows_containment_validation.log) | Log | 3.5 KB | Byte-identical primary execution transcript of the Windows containment validation suite |
| [`testing/evidence/phase_2_14/windows/governance_test_output.txt`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_14/windows/governance_test_output.txt) | Text | 4.8 KB | Complete live stdout/stderr of `test_evidence_governance.py -v` (27 tests, 17.60s duration, ledger hash check) |
| [`testing/evidence/phase_2_14/windows/transcripts/governance_test_output.log`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_14/windows/transcripts/governance_test_output.log) | Log | 4.8 KB | Byte-identical primary execution transcript of the 27-vector adversarial governance suite |

---

## 4. Host Environment Specifications

- **Operating System:** Windows 11 Professional (Build 10.0.26100), 64-bit AMD64 architecture
- **Shell:** PowerShell 5.1 / Windows Terminal
- **Active User Principal:** `Subodh`
- **Python Environment:** Conda environment `osdagbridge-py312` (`C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe`)
- **Python Version:** Python 3.12.16 (tags/v3.12.16:5d33f7c)
- **Key Modules:** `ctypes`, `_winapi`, `openseespy` (3.7.0.3), `OpenCASCADE` (7.7.2)
