# Phase 2.14 — Security Claims & Threat Model Wording Corrections

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Controlling Audit:** Claude's Phase 2.13 Independent Gate Audit ([`reports/PHASE_2_13_FINAL_INDEPENDENT_GATE_AUDIT.md`](file:///F:/FOSSEE%20internship/reports/PHASE_2_13_FINAL_INDEPENDENT_GATE_AUDIT.md))  
**Date:** 2026-11-17 (UTC / IST)  
**Status:** **SATISFIED** (Condition 2 Closed)

---

## 1. Executive Summary

In the Phase 2.13 gate audit (§1, §2, §3, and §10), Claude conditionally accepted the four-tier threat model architecture, noting:
> "Phase 2.13 is the first phase whose security story is honestly scoped... It is not a clean ACCEPTED, for three reasons: ... 2. Two report statements overstate the OS read-only control, calling `stat.S_IREAD` 'kernel-level' protection and listing it as a Tier-2 enforcement mechanism. I broke it as root, and the harness's own `test_10` clears it with one `chmod`."

Claude issued **Condition 2**:
> "2. Reword the 'kernel-level protection' (remediation) and Tier-2 `S_IREAD` enforcement language, and the Tier-4 'complete non-repudiation' line, to match the honest Tier-3 statement. Do not describe non-repudiation as implemented."

This report details the audit review, technical corrections, and updated definitions implemented across all Phase 2.13 and Phase 2.14 documentation and source code comments.

---

## 2. Technical Inventory of Overstated Statements & Corrections

The following specific statements were identified, scrutinized, and updated with technically accurate language:

### Correction 1: Elimination of "Kernel-Level" Characterization of Read-Only Attributes
- **Original Phrasing (`PHASE_2_13_REMEDIATION_REPORT.md` §1):**  
  *"Raw open denied by kernel."*
- **Corrected Phrasing:**  
  *"Raw `open(filepath, 'w')` is deterred for unprivileged same-user callers by filesystem read-only attributes, raising `[Errno 13] Permission denied`. This serves as an accidental-overwrite deterrent (Tier 1-2); as the owner, the same user can clear read-only attributes with `chmod` (Tier 3), which is detected upon verification via SHA-256 hash mismatch."*
- **Technical Rationale:**  
  Filesystem read-only bits (`stat.S_IREAD` on POSIX and `FILE_ATTRIBUTE_READONLY` on Windows FAT/NTFS) are file metadata flags checked by the OS file system driver during file open routines. They do *not* constitute a kernel security boundary against the file owner. On POSIX, `root` bypasses the check entirely. On Windows and POSIX, the owning user principal (`Subodh`) possesses full discretionary access control rights to reset permissions via `chmod` or `SetFileAttributesW`. Characterizing this as "kernel-level protection" conflated standard file attribute error handling with security enforcement boundaries.

### Correction 2: Correction of Access Denial Description in Remediation Report
- **Original Phrasing (`PHASE_2_13_REMEDIATION_REPORT.md` §2.1):**  
  *"Raw `open(sample_file, "a")` was attempted, resulting in kernel-level denial:"*
- **Corrected Phrasing:**  
  *"Raw `open(sample_file, "a")` was attempted, resulting in operating system access denial (`PermissionError: [Errno 13] Permission denied`):"*

### Correction 3: Elimination of "Complete Non-Repudiation" in Threat Model Diagram
- **Original Phrasing (`PHASE_2_13_SECURITY_ARCHITECTURE.md` §2 Diagram):**  
  *"`| - Protection: Complete cryptographic non-repudiation against local user tampering |`"*
- **Corrected Phrasing:**  
  *"`| - Protection: Cryptographic non-repudiation (requires external authority; NOT in Tier 3) |`"*
- **Technical Rationale:**  
  Non-repudiation is a property where an entity cannot successfully dispute the authorship or integrity of a statement. In a local execution environment where the symmetric signing key (`seal_signing_key.bin`) is readable by the executing user (`Subodh`), non-repudiation is mathematically impossible: the user can re-compute HMAC signatures over modified data. True non-repudiation is achievable *only* via an external principal (Tier 4) holding an asymmetric private key or through a remote append-only transparency log. The diagram now explicitly states that this is an external requirement, not an implemented local property.

### Correction 4: Recategorization of `S_IREAD` in Tier 2 Enforcement Mechanisms
- **Original Phrasing (`PHASE_2_13_SECURITY_ARCHITECTURE.md` §2.2):**  
  *"OS-level read-only permissions (`stat.S_IREAD`) applied to all sealed files."*
- **Corrected Phrasing:**  
  *"Filesystem read-only attributes (`stat.S_IREAD` / `FILE_ATTRIBUTE_READONLY`) applied to sealed files as an accidental-overwrite deterrent."*

### Correction 5: Precise Description of Read-Only Scope in Multi-Layered Protection
- **Original Phrasing (`PHASE_2_13_SECURITY_ARCHITECTURE.md` §3.2 Item 3):**  
  *"Consequently, even if an attacker bypasses the gateway entirely and invokes built-in open(filepath, "w") or shutil.copy(), the Windows NT kernel itself rejects the operation with `PermissionError: [Errno 13] Permission denied`."*
- **Corrected Phrasing:**  
  *"Upon sealing, `evidence_guard.py` applies filesystem read-only attributes via `os.chmod(fp, stat.S_IREAD)` (setting `FILE_ATTRIBUTE_READONLY` on Windows). This deters accidental modifications and unmediated `open(filepath, "w")` calls by unprivileged processes. However, this is NOT an immutable kernel security boundary against malicious local execution: on Windows or POSIX, the file owner (or root) can reset write permissions via `os.chmod(fp, stat.S_IWRITE)` (Tier 3). Any such post-seal modification is detected after the fact by `verify_manifest_integrity` via SHA-256 hash mismatch, but read-only attributes do not prevent an intentional same-user attacker from mutating files."*

### Correction 6: Containment Design Heading Precision
- **Original Heading (`PHASE_2_13_SECURITY_ARCHITECTURE.md` §6.1):**  
  *"### 6.1 Kernel-Level Containment Design"*
- **Corrected Heading:**  
  *"### 6.1 Win32 Job Object Process Containment Design"*

### Correction 7: Module Docstrings and Section Headers in Code
- **`testing/test_cases/baseline_regression/evidence_guard.py`:**
  - Line 7: Changed *"provides kernel-level process containment"* to *"provides OS-level process containment"*.
  - Line 463: Changed *"# 3. Kernel-Level Process Containment"* to *"# 3. OS-Level Process Containment"*.
  - Line 877: Changed *"locks evidence files with OS-level read-only attributes"* to *"applies filesystem read-only attributes (accidental-overwrite deterrent)"*.

---

## 3. Four-Tier Threat Model: Definitive Boundaries & Scope

The four-tier threat model is now uniformly and consistently maintained across all project documentation:

```
+---------------------------------------------------------------------------------------+
| TIER 4: EXTERNAL TRUST AUTHORITY / INDEPENDENT OFFLINE AUDITOR                        |
|  - Cryptographic Boundary: Asymmetric Public/Private Keys (Auditor holds private key) |
|  - Transparency: Immutable remote append-only log / Git signed commits / HSM           |
|  - Status: NOT IMPLEMENTED IN TEST HARNESS (Requires external authority like Claude)  |
|  - Scope: Where true non-repudiation originates                                       |
+---------------------------------------------------------------------------------------+
                                           ^
                                           | Independent Attestation
+---------------------------------------------------------------------------------------+
| TIER 3: SAME-USER LOCAL EXECUTION DOMAIN (Windows User: 'Subodh')                     |
|  - Threat: Arbitrary Python code / malicious scripts executing under the same user   |
|  - Reality: Same user possesses OS ACL rights to overwrite files, keys, and ledgers   |
|  - Scope: Local HMAC provides INTERNAL TAMPER DETECTION against accidental drift     |
|    and uncoordinated edits, NOT a security boundary against the user                  |
+---------------------------------------------------------------------------------------+
                                           ^
                                           | Unmediated Bypass / Local Execution
+---------------------------------------------------------------------------------------+
| TIER 2: SUPPORTED TEST-HARNESS INTERFACES & RUNNERS                                   |
|  - Threat: Sub-harness misconfigurations, cross-process test calls, stale cache reads |
|  - Mitigation: Centralized gateway (safe_open_evidence), persistent ledger lookup     |
|    (trusted_run_seals.json), ancestor .sealed markers, protected-phase refusal,       |
|    workspace-root / reports refusal, read-only attributes (accidental deterrent)       |
|  - Status: FULLY CLOSED & VERIFIED                                                    |
+---------------------------------------------------------------------------------------+
                                           ^
                                           | Direct API Invocations
+---------------------------------------------------------------------------------------+
| TIER 1: ACCIDENTAL CORRUPTION, TOCTOU RACES, CONCURRENT PROCESS COLLISIONS            |
|  - Threat: Symlink swaps, directory junction swaps, parallel write race conditions   |
|  - Mitigation: SafeFileWrapper with staging (.{name}.tmp_{uuid}) + O_EXCL +           |
|    realpath canonical invariance verification + atomic os.replace commitment          |
|  - Status: FULLY CLOSED & VERIFIED                                                    |
+---------------------------------------------------------------------------------------+
```

---

## 4. Summary Conclusion

Condition 2 of Claude's Phase 2.13 Independent Gate Audit is **SATISFIED**:
- All overstated claims referring to `S_IREAD` or same-user file attributes as "kernel-level", "tamper-proof", "complete non-repudiation", or an "independent trust boundary" have been eliminated.
- The distinction between tamper-detection (what local HMAC and read-only attributes provide) and non-repudiation (what requires an independent external authority) is technically precise and preserved throughout.
- All code comments and report sections have been synchronized with the honest threat model.
