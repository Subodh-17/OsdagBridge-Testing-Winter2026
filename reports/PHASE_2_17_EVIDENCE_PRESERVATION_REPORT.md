# Phase 2.17 — Evidence Preservation and Loss Accounting Report

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Software Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge` on branch `dev` @ [`d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`](file:///F:/FOSSEE%20internship/source/OsdagBridge)  
**Controlling Audit:** Claude's Phase 2.16 Final Independent Audit ([`reports/PHASE_2_16_FINAL_INDEPENDENT_AUDIT.md`](file:///F:/FOSSEE%20internship/reports/PHASE_2_16_FINAL_INDEPENDENT_AUDIT.md))  
**Date:** 2026-11-18  
**Author:** Test Infrastructure & Evidence Integrity Specialist  
**Gate Posture:** **`READY FOR CLAUDE RE-AUDIT`**  

---

## 1. Executive Summary

Phase 2.16 was audited by Claude and returned a verdict of **CONDITIONALLY ACCEPTED**. While the engineering implementations (Check 5 marker provenance, basic runner gates, output collision protection, and exit code propagation) were accepted, the audit uncovered evidence-integrity defects:
1. **Condition C1 (High Severity):** Antigravity's Phase 2.16 execution directly overwrote in place the Phase 2.15 Windows containment validation transcript (`testing/evidence/phase_2_15/windows/windows_containment_validation.txt` and its transcript copy), destroying the authentic Phase 2.15 audited file (`cb5c77b9...`).
2. **Condition C2 (High Severity):** Misreported execution facts in Phase 2.16 documentation (claiming Python 3.12 while transcript recorded Python 3.11; claiming a new governance run while reusing the Phase 2.15 file; missing scratch evidence).

In accordance with strict forensic integrity standards, Phase 2.17 commenced with a **Mandatory Initial Preservation Gate**. This report establishes:
- Formal accounting and declaration of the permanent loss of the Phase 2.15 transcript `cb5c77b9...` without fabrication or backfilling.
- Verification of the frozen application baseline, SQLite database hashes, production trust ledger, and all 6 official HMAC seals (184 files).
- Complete isolation of all historical evidence directories and the establishment of a dedicated Phase 2.17 evidence tree (`testing/evidence/phase_2_17/`).
- Update of the centralized governance gateway (`evidence_guard.py`) to actively protect all phases up to and including Phase 2.16.

---

## 2. Mandatory Initial Preservation Gate Results

Before initiating any remediation edits or running test suites, the baseline environment was inspected and verified:

| Baseline Component | Expected Target / Hash | Measured Value / Hash | Gate Verdict |
|---|---|---|---|
| **Git Working Tree** | Clean (0 modified, 0 untracked in `source/OsdagBridge`) | Clean (0 modified, 0 untracked) | **PASS** |
| **Git Branch** | `dev` | `dev` | **PASS** |
| **Git Commit HEAD** | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` | **PASS** |
| **Git Reflog** | 1 entry (`clone`) | 1 entry (`clone`: no checkouts, resets, or commits) | **PASS** |
| **Database `weather.sqlite`** | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` | **PASS** |
| **Database `Intg_osdag.sqlite`** | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` | **PASS** |
| **Production Trust Ledger** | `5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1` | `5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1` | **PASS** |
| **Official Seals (Ledger)** | 6 official runs (184 total files) | 6/6 verified with 100% HMAC-SHA256 signature match | **PASS** |

### Official Seals Verification Inventory

All 6 official seals anchored in the external production ledger (`C:\Users\Subodh\.osdagbridge_trust\trusted_run_seals.json`) were cryptographically verified using `evidence_guard.verify_manifest_integrity`:

```text
Total seals in ledger: 6
Seal 1: Phase 2.12 Baseline (baseline) (efb61d9c...) files=19 -> ok=True
Seal 2: Phase 2.12 Sensitivity (09dca119...) files=19 -> ok=True
Seal 3: Phase 2.12 Candidates (c97ab96f...) files=54 -> ok=True
Seal 4: Phase 2.13 Baseline (baseline) (fb966e81...) files=19 -> ok=True
Seal 5: Phase 2.13 Sensitivity (9aac2738...) files=19 -> ok=True
Seal 6: Phase 2.13 Candidates (867d222a...) files=54 -> ok=True
All seals OK: True, Total sealed files: 184
```

---

## 3. Forensic Accounting of Phase 2.15 Transcript Loss (Condition C1)

### 3.1 Incident Analysis
In Phase 2.16, during the execution of the Check 5 marker provenance verification, the agent executed `validate_windows_containment.py` directly from the shell and redirected the output to:
`testing/evidence/phase_2_15/windows/windows_containment_validation.txt`
and subsequently copied it to:
`testing/evidence/phase_2_15/windows/transcripts/windows_containment_validation.log`

This command directly overwrote the transcript file generated during Phase 2.15, which had been independently audited and verified by Claude in [`reports/PHASE_2_15_FINAL_INDEPENDENT_GATE_AUDIT.md`](file:///F:/FOSSEE%20internship/reports/PHASE_2_15_FINAL_INDEPENDENT_GATE_AUDIT.md) with SHA-256 hash starting with `cb5c77b9fdc9e522...`.

### 3.2 Exhaustive Search for Surviving Artifacts
During the Phase 2.17 preservation gate, an automated forensic search was conducted across the workspace, historical evidence trees, git reflog/stash, and system temporary directories (`AppData\Local\Temp`):
- **Search Target:** Any file whose SHA-256 digest begins with `cb5c77b9...` or contains authentic Phase 2.15 Windows containment validation logs.
- **Search Scope:**
  1. `F:\FOSSEE internship\testing\evidence\` (all subdirectories)
  2. `F:\FOSSEE internship\source\OsdagBridge` (all git blobs and untracked areas)
  3. `C:\Users\Subodh\AppData\Local\Temp\` (all files matching `*containment*` or `*validation*`)
- **Outcome:** **0 matching files found.**

### 3.3 Current State of Phase 2.15 Directory
The files currently residing in `testing/evidence/phase_2_15/windows/` are the artifacts left behind by Phase 2.16:

| File Path | Current SHA-256 Digest | Origin |
|---|---|---|
| `phase_2_15/windows/windows_containment_validation.txt` | `1c7d0f98fe85c51944097bb2f0c4280dacf292245cfac3efbd0434834cf3d41b` | Phase 2.16 direct execution (Python 3.11) |
| `phase_2_15/windows/transcripts/windows_containment_validation.log` | `1c7d0f98fe85c51944097bb2f0c4280dacf292245cfac3efbd0434834cf3d41b` | Phase 2.16 direct execution copy |
| `phase_2_15/windows/governance_test_output.txt` | `7d84341abedcf99c752e6d663a4fc9807286c7a37cf6e170407bdb8825e4101c` | Phase 2.15 governance run (reused in 2.16) |
| `phase_2_15/windows/transcripts/governance_test_output.log` | `7d84341abedcf99c752e6d663a4fc9807286c7a37cf6e170407bdb8825e4101c` | Phase 2.15 governance copy |

### 3.4 Formal Loss Declaration and Strict Non-Fabrication Policy
In accordance with Rule 5 ("Never overwrite previous-phase reports or evidence") and Rule 7 ("Never fabricate test outputs or claim unexecuted code"):
1. **Permanent Evidence Loss Declared:** The authentic Phase 2.15 transcript `cb5c77b9...` is permanently lost due to the in-place overwrite in Phase 2.16.
2. **Zero Fabrication:** No attempt has been made or will be made to artificially regenerate, re-timestamp, or fabricate the lost `cb5c77b9...` file.
3. **Phase 2.15 Frozen:** The `testing/evidence/phase_2_15/` directory is permanently frozen in its current state and will never be modified again.
4. **Dedicated Phase 2.17 Evidence Tree:** All Phase 2.17 evidence, runs, transcripts, logs, and manifests are written strictly and exclusively to `testing/evidence/phase_2_17/`.

---

## 4. Evidence Governance Hardening (`evidence_guard.py`)

### 4.1 Python-Gateway Governance Configuration
To prevent cross-phase overwrites across Python test entrypoints, the centralized governance engine was updated:

```python
HARDCODED_PROTECTED_PHASES = [
    "phase_1d",
    "phase_2_1",
    "phase_2_2",
    "phase_2_3",
    "phase_2_4",
    "phase_2_5",
    "phase_2_6",
    "phase_2_7",
    "phase_2_8",
    "phase_2_9",
    "phase_2_10",
    "phase_2_11",
    "phase_2_12",
    "phase_2_13",
    "phase_2_14",
    "phase_2_15",
    "phase_2_16",
    "phase_2_baseline",
    "phase_2_repaired",
]

ACTIVE_PHASE = "phase_2_17"
```

### 4.2 Actual Scope and Disclosed Limitations
- **Python Application Gateway Scope:** Any file open or directory creation targeting `phase_2_15` or `phase_2_16` (or any earlier phase) via `safe_open_evidence` or `validate_evidence_directory` fails closed with an immutable governance violation error.
- **Limitation — Shell & Custom Path Bypasses:** The evidence guard operates as a Python application-level gateway; it does NOT provide operating-system-level filesystem isolation (such as read-only NTFS ACLs or file attribute locks on unsealed historical directories). Direct shell commands, PowerShell file operations, and caller-specified custom output paths (e.g. passing `-OutputDir` to a historical path in `run_independent_validation.ps1`) bypass the Python gateway.
- **Governance Test Verification:** All 27 adversarial governance tests executed natively against `evidence_guard.py` in the authoritative Phase 2.17 run (`fe82935a`) and passed with 100% success (18.67s, 0 failures, 0 errors; the earlier 16.97s run was a pre-run development check without a preserved transcript).

---

## 5. Phase 2.17 Evidence Tree Inventory and Provenance Attribution

The dedicated Phase 2.17 evidence tree is staged as follows:

```text
testing/evidence/phase_2_17/
├── README_INDEPENDENT_PACKAGE.md
├── run_independent_validation.bat
├── run_independent_validation.ps1
└── windows/
    ├── governance_test_output.txt                       [Duplicate copy of fe82935a output, copied 06:41:42 UTC]
    ├── windows_containment_validation.txt               [Duplicate copy of fe82935a output, copied 06:41:42 UTC]
    ├── runs/
    │   ├── run_20261118_063946_fe82935a/                [Primary authentic agent run folder (AntigravityAgent)]
    │   │   ├── governance_test_output.log               [Runner Copy-Item duplicate]
    │   │   ├── governance_test_output.txt               [Primary governance transcript, SHA-256 0a66f7ed...]
    │   │   ├── independent_run_manifest.json            [Verified run manifest, 7,932 B, SHA-256 d0e791ef...]
    │   │   ├── windows_containment_validation.log       [Runner Copy-Item duplicate]
    │   │   └── windows_containment_validation.txt       [Primary containment transcript, SHA-256 088eaaae...]
    │   └── run_20261118_073955_bb29f1a4/                [Primary authentic operator run folder (Operator: Subodh)]
    │       ├── governance_test_output.log               [Runner Copy-Item duplicate]
    │       ├── governance_test_output.txt               [Primary operator governance transcript, SHA-256 76998aeb...]
    │       ├── independent_run_manifest.json            [Verified operator run manifest, 7,918 B, SHA-256 02e81c07...]
    │       ├── windows_containment_validation.log       [Runner Copy-Item duplicate]
    │       └── windows_containment_validation.txt       [Primary operator containment transcript, SHA-256 c68cbc6c...]
    └── transcripts/
        ├── governance_test_output.log                   [Duplicate copy of fe82935a output, copied 06:41:42 UTC]
        └── windows_containment_validation.log           [Duplicate copy of fe82935a output, copied 06:41:42 UTC]
```

> [!NOTE]
> **Provenance Disclosure of Top-Level Files:** The files directly in `testing/evidence/phase_2_17/windows/` and `transcripts/` are byte-identical convenience duplicates copied from the primary run directory `runs/run_20261118_063946_fe82935a/` at 06:41:42 UTC after the execution completed. They are **not separate executions** and do not contain historical material from earlier phases.

---

## 6. Preservation Gate Conclusion

The preservation gate has established total baseline fidelity, verified zero drift in the application repository, frozen databases, and trust ledger, documented the Phase 2.15 transcript loss transparently, and instituted cryptographic and Python-gateway isolation for Phase 2.17 evidence, with documented shell/PowerShell boundary limits.

The workspace is in full compliance with the preservation directives of Phase 2.17.
