# Phase 2.14 — Prioritized Remaining Risks & Threat Boundary Audit

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge` on branch `dev` @ [`d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`](file:///F:/FOSSEE%20internship/source/OsdagBridge)  
**Controlling Audit:** Claude's Phase 2.13 Independent Gate Audit ([`reports/PHASE_2_13_FINAL_INDEPENDENT_GATE_AUDIT.md`](file:///F:/FOSSEE%20internship/reports/PHASE_2_13_FINAL_INDEPENDENT_GATE_AUDIT.md))  
**Date:** 2026-11-17 (UTC / IST)  
**Status:** **HONESTLY SCOPED & UPDATED**

---

## 1. Executive Summary

This risk evaluation reviews all outstanding risks identified in Claude's Phase 2.13 audit (`reports/PHASE_2_13_REMAINING_RISKS.md`) and updates their status following the empirical validation, ledger isolation, and documentation precision tasks executed in Phase 2.14.

All risks are evaluated strictly against the harness's declared four-tier threat model:
- **Tier 1:** Accidental corruption and race hazards.
- **Tier 2:** Supported harness interface misuse.
- **Tier 3:** Same-user local execution domain (Windows user `Subodh`).
- **Tier 4:** External authority and independent attestation.

---

## 2. Status of Phase 2.13 High-Priority Risks

| Phase 2.13 Risk | Original Severity | Remediation Executed in Phase 2.14 | Phase 2.14 Status |
| :--- | :---: | :--- | :---: |
| **Windows Containment & 27/27 Governance Unreproduced (BLOCKED)** | **High** | 1. Executed `validate_windows_containment.py` live on native Windows 11 host: 6/6 checks PASSED in 35.73s, observing full 32s horizon.<br>2. Executed `test_evidence_governance.py` live on native Windows 11 host: 27/27 vectors PASSED (0 skips, 0 failures) in 17.60s.<br>3. Primary output and transcripts preserved in `testing/evidence/phase_2_14/windows/`. | **CLOSED** |
| **Overstated OS Read-Only Control Wording** | **High** | Audited all reports and code comments. Replaced all descriptions of `S_IREAD` and `FILE_ATTRIBUTE_READONLY` claiming "kernel-level", "tamper-proof", or "complete non-repudiation" with technically precise definitions characterizing them as accidental-overwrite deterrents (Tier 1-2). Synchronized with honest Tier 3 disclaimers. | **CLOSED** |

---

## 3. Status of Phase 2.13 Medium-Priority Risks

| Phase 2.13 Risk | Original Severity | Remediation Executed in Phase 2.14 | Phase 2.14 Status |
| :--- | :---: | :--- | :---: |
| **Governance Tests Writing to Production Trust Ledger** | **Medium** | 1. Forensically investigated ledger entries; matched 4 scratch entries to manual test commands in `transcript.jsonl`.<br>2. Backed up ledger and non-destructively pruned 4 scratch entries; preserved 6 official run seals.<br>3. Hardened `test_evidence_governance.py` to use isolated temporary trust stores and added automated hash check in `tearDown`.<br>4. Verified production ledger hash strictly unchanged before/after 27-vector run (`5a9b927...` -> `5a9b927...`). | **CLOSED** |
| **Same-User Resealing & Key Access (Tier 3 Boundary)** | **Medium** | Maintained honest architectural boundary: in a single-user OS session, symmetric HMAC signing cannot prevent a user holding OS filesystem rights from deleting ledger entries and re-signing files. Non-repudiation requires an external authority (Tier 4, e.g., Claude's gate audit). | **REMAINS AN HONEST DISCLOSED BOUNDARY** |
| **Raw Filesystem Writes Bypassing Gateway (Tier 3 Boundary)** | **Medium** | Maintained honest architectural boundary: raw Python `open()` calls outside `safe_open_evidence` are deterred by read-only attributes for unprivileged processes, and detected post-run by `verify_manifest.py` via SHA-256 hash mismatch. | **REMAINS AN HONEST DISCLOSED BOUNDARY** |

---

## 4. Status of Platform Limitations & Engineering Trade-Offs

| Identified Limitation | Classification | Engineering Justification & Handling | Status |
| :--- | :---: | :--- | :---: |
| **Linux Lacks Usable Process Containment Without Delegation** | Platform Limitation | On unprivileged Linux hosts without delegated cgroup v2 controllers, `ProcessLifetimeJob` detects the absence of containment and honestly reports `is_contained = False`. `TC-REG-FS-CLEAN-WORKING-TREE` reports `BLOCKED` rather than a false PASS. | **HONESTLY REPORTED & ACCEPTED** |
| **Engineering Tolerances & Approximations Carried Over from Phase 2.12** | Engineering Trade-off | C01 multi-girder stress coverage uses 0.8% tolerance band and embeds composite $Z_b$; A02 uses 1% tolerance; EQ/A02 barrier width uses $0.50\text{ m}$ constant. These were accepted with limitations in Phase 2.12 and 2.13 and remain unchanged to avoid unnecessary regressions. | **PRESERVED & ACCEPTED WITH LIMITATIONS** |

---

## 5. Phase 3 Authorization Notice

Phase 2.14 work was strictly limited to closing the three conditions established in Claude's Phase 2.13 audit.

**Phase 3 remains STRICTLY UNAUTHORIZED.**

Authorization to proceed to Phase 3 rests exclusively with the project owner and requires the independent gate audit review and sign-off by Claude.
