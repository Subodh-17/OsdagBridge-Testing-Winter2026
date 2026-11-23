# PHASE 3 — Baseline Preservation and Governance Audit Gate (Revision 2.0)

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Software Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Revision:** Revision 2.0 (Post-Audit Re-Baseline)  
**Controlling Audit:** `reports/phase_3/CLAUDE_INDEPENDENT_PHASE_3_PLANNING_AUDIT.md` (by independent auditor Claude)  
**Historical Revision Archive:** `reports/phase_3/v1_original/PHASE_3_BASELINE_PRESERVATION_REPORT.md`  
**Date:** 2026-11-18  

---

## 1. Executive Summary & Audit Context

This document is the revised Baseline Preservation Report for Phase 3 planning of the OsdagBridge Software Testing and Issue Reporting campaign. Following independent auditor Claude's Phase 3 Planning Audit ([`reports/phase_3/CLAUDE_INDEPENDENT_PHASE_3_PLANNING_AUDIT.md`](file:///F:/FOSSEE%20internship/reports/phase_3/CLAUDE_INDEPENDENT_PHASE_3_PLANNING_AUDIT.md)), all preservation assertions, environment specifications, and run metadata have been rigorously reconciled against authoritative physical files and sealed records.

The original v1 report contained four factual inaccuracies identified in Claude's audit (§2, §7):
1. A truncated/mis-copied UUID for reference run `fe82935a`.
2. An incorrect Windows OS edition label ("Enterprise" instead of "Home Single Language").
3. Inaccurate runtime package versions for OpenSeesPy and pythonOCC.
4. An overbroad statement claiming zero historical overwrites across all of Phase 2, omitting the known Phase 2.15 transcript overwrite that occurred during Phase 2.16.

This Revision 2.0 report corrects every inaccuracy while attesting to the **100% intact, bit-exact physical preservation** of the application source, databases, production trust ledger, and Phase 2 historical evidence archives.

---

## 2. Git Working Tree & Application Source State

The application repository is located at `source/OsdagBridge`. The working tree was audited directly via Git command-line tooling:

| Property | Required Baseline Specification | Observed Physical State | Compliance Status |
|:---|:---|:---|:---:|
| **Git Working Directory** | `source/OsdagBridge` | `source/OsdagBridge` | **COMPLIANT** |
| **Branch** | `dev` | `dev` | **COMPLIANT** |
| **Commit HEAD** | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` | **COMPLIANT** |
| **Working Tree Drift** | 0 modified, 0 untracked | 0 modified, 0 untracked (`git status --porcelain` = `""`) | **COMPLIANT** |
| **Source File Count & Hash** | 282 python files in `src/` | Aggregate source hash verified identical to frozen baseline | **COMPLIANT** |
| **Reflog & Lock Status** | Exactly 1 clone entry; 0 local commits | Frozen; no stale `.git/index.lock` | **COMPLIANT** |

**Zero Application Changes Assertion:**  
No file within `source/OsdagBridge` has been created, modified, staged, committed, or deleted. The frozen baseline remains 100% bit-exact with commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`.

---

## 3. Persistent Database Cryptographic Parity

Both reference SQLite databases governing project location, weather parameters, and structural standard sections were verified for exact physical size and SHA-256 cryptographic digest:

| Database Identifier | Relative Workspace Path | Expected / Authorized SHA-256 | Observed SHA-256 | Physical Size | Verification Result |
|:---|:---|:---|:---|:---:|:---:|
| **`weather.sqlite`** | `source/OsdagBridge/src/osdagbridge/core/data/project_location/weather.sqlite` | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` | 180,224 bytes | **MATCH (100% PARITY)** |
| **`Intg_osdag.sqlite`** | `source/OsdagBridge/src/osdagbridge/core/data/ResourceFiles/Intg_osdag.sqlite` | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` | 270,336 bytes | **MATCH (100% PARITY)** |

No database modifications, query schema updates, or working tree side-effects have occurred.

---

## 4. Production Trust Store & Official Seals

The centralized production trust ledger pinned at `~/.osdagbridge_trust/trusted_run_seals.json` governs all accepted Phase 2 runs. The file was verified via SHA-256 and HMAC-SHA256 signature evaluation across all registered runs using `evidence_guard.verify_manifest_integrity`:

### 4.1 Trust Store Physical Verification
- **Path:** `C:\Users\Subodh\.osdagbridge_trust\trusted_run_seals.json`
- **Observed SHA-256:** `5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1`
- **Physical Size:** 3,789 bytes
- **Registered Runs Count:** 6 distinct sealed runs

### 4.2 Individual Seal Integrity Verification

| # | Run UUID | Phase Label | Evidence Subdirectory | Sealed Files | Verification Status | Verification Detail |
|:---:|:---|:---|:---|:---:|:---:|:---|
| 1 | `efb61d9c` | Phase 2.12 Baseline (baseline) | `testing/evidence/phase_2_12/baseline` | 19 | **VALID** | All 19 files match manifest and external cryptographic seal with 100% integrity. |
| 2 | `09dca119` | Phase 2.12 Sensitivity | `testing/evidence/phase_2_12/sensitivity` | 19 | **VALID** | All 19 files match manifest and external cryptographic seal with 100% integrity. |
| 3 | `c97ab96f` | Phase 2.12 Candidates | `testing/evidence/phase_2_12/candidates` | 54 | **VALID** | All 54 files match manifest and external cryptographic seal with 100% integrity. |
| 4 | `fb966e81` | Phase 2.13 Baseline (baseline) | `testing/evidence/phase_2_13/baseline` | 19 | **VALID** | All 19 files match manifest and external cryptographic seal with 100% integrity. |
| 5 | `9aac2738` | Phase 2.13 Sensitivity | `testing/evidence/phase_2_13/sensitivity` | 19 | **VALID** | All 19 files match manifest and external cryptographic seal with 100% integrity. |
| 6 | `867d222a` | Phase 2.13 Candidates | `testing/evidence/phase_2_13/candidates` | 54 | **VALID** | All 54 files match manifest and external cryptographic seal with 100% integrity. |

**Cumulative Sealed Files Verified:** **184 files** across 6 production seals. Zero seal tampering, file modification, or ledger divergence detected.

---

## 5. Phase 2.17 Independent Windows Run Manifests

The authoritative Phase 2.17 independent validation run manifests executed by human operator Subodh and automated agent reference were verified directly from their JSON manifests on disk:

| Run Description | Canonical Full Run UUID | Manifest Relative Path | Manifest SHA-256 Hash | Physical Size |
|:---|:---|:---|:---|:---:|
| **Native Human Operator Run** | `bb29f1a4-5089-4180-ad1c-96154bb405c8` | `testing/evidence/phase_2_17/windows/runs/run_20261118_073955_bb29f1a4/independent_run_manifest.json` | `02e81c07d1eed16f134b80456b47359be18645c55eedd23090890c7064d25706` | 7,918 bytes |
| **Agent Reference Run** | `fe82935a-0927-443a-b7be-aa730468d388` | `testing/evidence/phase_2_17/windows/runs/run_20261118_063946_fe82935a/independent_run_manifest.json` | `d0e791ef2a35efefeb0a6dd7df330aa0f21a922bdebd09b9251561fed8f7b682` | 7,932 bytes |

*Correction Note (F-PRES-01):*  
The v1 preservation report mistakenly recorded the reference run UUID as `fe82935a-93f5-4428-98e3-0c463f28cf0d`. The physical manifest on disk confirms the true canonical UUID is `fe82935a-0927-443a-b7be-aa730468d388`. Both manifests remain byte-identical and sealed.

---

## 6. Runtime Environment Specifications

The Python and OS environment details were read directly from the conda environment metadata and manifest environment blocks:

| Environment Property | Authoritative Measured Value | Source Basis |
|:---|:---|:---|
| **Operating System** | `Microsoft Windows 11 Home Single Language` (Build 26300) | `independent_run_manifest.json:os_caption` |
| **PowerShell Version** | Windows PowerShell 5.1 (Desktop Edition, 5.1.26100.9818) | Manifest environment metadata |
| **Python Executable** | `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe` | Conda environment path |
| **Python Version** | Python 3.12.16 (64-bit win32, MSC v.1944 AMD64) | `sys.version` |
| **OpenSeesPy Version** | `openseespy 3.8.0.0` (with `openseespywin 3.8.0.0`) | Pip & Conda metadata |
| **OpenCASCADE Version** | `pythonocc-core 8.0.1.2` (backed by `occt 8.0.1`) | `conda-meta/pythonocc-core-8.0.1.2...json` |

*Correction Note (F-PRES-02, F-PRES-03):*  
The v1 report claimed "Windows 11 Enterprise" and older package versions (OpenSeesPy 3.5.1.1, pythonOCC 7.8.1). These were inaccurate claims not derived from physical environment queries. The authoritative values above are verified against physical package manifests.

---

## 7. Historical Evidence Overwrite & Command Execution Disclosures

In accordance with strict evidence-integrity principles, the following historical events are explicitly disclosed:

1. **Phase 2.15 Transcript Overwrite Disclosure (F-PRES-04):**  
   During Phase 2.16 execution, the original Phase 2.15 Windows containment transcript (`cb5c77b9...`) was unintentionally overwritten by an unanchored test run and was formally declared lost in [`reports/PHASE_2_16_FINAL_INDEPENDENT_GATE_AUDIT.md`](file:///F:/FOSSEE%20internship/reports/PHASE_2_16_FINAL_INDEPENDENT_GATE_AUDIT.md). All six official HMAC seals in the production trust ledger (covering 184 files in Phase 2.12 and 2.13) and all subsequent Phase 2.17 evidence runs remain 100% valid and untampered. The v1 statement "nothing overwritten across phase_2_4 ... phase_2_17" was overbroad and is now corrected.

2. **Discovery Command Exit Code 1 Disclosure (F-PRES-05):**  
   During initial Phase 3 preservation discovery, a PowerShell one-liner executing a Python script exited with code 1. Inspection reveals this was caused by an unterminated multiline string / f-string quotation in the one-liner command text (`SyntaxError: unterminated string literal`), not an underlying system or repository failure. Once properly formatted, the command executed to completion (exit code 0).

---

## 8. Preservation Gate Attestation

I hereby certify that:
1. The application codebase `source/OsdagBridge` remains completely frozen at commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` on branch `dev`.
2. Both reference databases `weather.sqlite` and `Intg_osdag.sqlite` match their authoritative cryptographic digests.
3. The centralized production trust ledger and all six HMAC seals (184 files) are 100% valid.
4. All environment details, UUIDs, and historical events are accurately recorded.
5. Zero application source code modifications have been made. Phase 3 remains strictly in read-only planning mode.

*Preservation Gate Status:* **PASSED — ALL GATES VERIFIED**
