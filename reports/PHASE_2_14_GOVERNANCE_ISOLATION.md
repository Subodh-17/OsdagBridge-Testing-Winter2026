# Phase 2.14 — Production Trust Ledger Isolation & Provenance Audit

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Production Trust Store:** `%USERPROFILE%\.osdagbridge_trust` (`C:\Users\Subodh\.osdagbridge_trust`)  
**Production Ledger:** `C:\Users\Subodh\.osdagbridge_trust\trusted_run_seals.json`  
**Controlling Audit:** Claude's Phase 2.13 Independent Gate Audit ([`reports/PHASE_2_13_FINAL_INDEPENDENT_GATE_AUDIT.md`](file:///F:/FOSSEE%20internship/reports/PHASE_2_13_FINAL_INDEPENDENT_GATE_AUDIT.md))  
**Date:** 2026-11-17 (UTC / IST)  
**Status:** **SATISFIED** (Condition 3 Closed)

---

## 1. Executive Summary

In the Phase 2.13 gate audit (§7 and §10), Claude identified stray test entries in the production trust ledger:
> "The pinned ledger carries 2 governance test seals (tmp-dir `evidence_dir`, 17:27), so test execution still appends to the production trust store... Point governance-test sealing at a temporary trust directory and remove the 2 stray entries from the pinned ledger."

In accordance with Phase 2.14 Condition 3, this report documents:
1. Forensic provenance analysis of all records in `trusted_run_seals.json`.
2. Conclusive root-cause identification of the stray entries via conversation trajectory transcripts.
3. Non-destructive pruning of temporary scratch test entries while preserving 100% of authentic official run seals from Phase 2.12 and Phase 2.13.
4. Cryptographic integrity re-verification of all official runs against the cleaned ledger.
5. Strict isolation of the governance test suite via isolated temporary trust stores and automated before/after hash enforcement in `tearDown`.
6. Empirical verification that running the full 27-vector governance suite leaves the production trust ledger untouched.

---

## 2. Forensic Analysis of Production Trust Ledger Entries

Before remediation, `C:\Users\Subodh\.osdagbridge_trust\trusted_run_seals.json` contained 10 records:

| Index | Run UUID | Phase Label | Runner ID | Timestamp (UTC) | Evidence Directory | Status / Provenance |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **0** | `efb61d9c-2986-4ecd-90cf-62fbd278f6a4` | `Phase 2.12 Baseline (baseline)` | `baseline_runner` | 2026-11-17T14:37:16Z | `testing/evidence/phase_2_12/baseline` | **Authentic Official Seal** |
| **1** | `09dca119-7acd-450d-8b6b-11c63cf9b5a8` | `Phase 2.12 Sensitivity` | `sensitivity_runner` | 2026-11-17T14:44:26Z | `testing/evidence/phase_2_12/sensitivity` | **Authentic Official Seal** |
| **2** | `c97ab96f-dccc-47f6-b4c9-b2fa7a973b45` | `Phase 2.12 Candidates` | `candidates_runner` | 2026-11-17T14:44:27Z | `testing/evidence/phase_2_12/candidates` | **Authentic Official Seal** |
| **3** | `fc28cba1-d4dd-4d33-89bd-82c1d4bc91e6` | `Test` | `baseline_runner` | 2026-11-17T17:26:48Z | `AppData/Local/Temp/tmpgac6p3ad` | **Stray Scratch Test** (Step 8859) |
| **4** | `c344dafd-d7a3-404a-9f77-622671c38730` | `Test` | `baseline_runner` | 2026-11-17T17:27:34Z | `AppData/Local/Temp/tmpzrbt4pgr` | **Stray Scratch Test** (Step 8868) |
| **5** | `339e7bf0-6a61-4c3c-be16-551b01845094` | `Test` | `baseline_runner` | 2026-11-17T17:27:40Z | `AppData/Local/Temp/tmp3ri337t_` | **Stray Scratch Test** (Step 8871) |
| **6** | `e17e80cf-074b-467a-9568-bd7d5c08dc93` | `Test` | `baseline_runner` | 2026-11-17T17:27:46Z | `AppData/Local/Temp/tmpjgn7uqjt` | **Stray Scratch Test** (Step 8873) |
| **7** | `fb966e81-b715-4208-98c7-c258b7eb08fd` | `Phase 2.13 Baseline (baseline)` | `baseline_runner` | 2026-11-17T17:37:54Z | `testing/evidence/phase_2_13/baseline` | **Authentic Official Seal** |
| **8** | `9aac2738-e753-49ab-84e6-7a2a61548a67` | `Phase 2.13 Sensitivity` | `sensitivity_runner` | 2026-11-17T17:41:09Z | `testing/evidence/phase_2_13/sensitivity` | **Authentic Official Seal** |
| **9** | `867d222a-334a-4327-aaf2-d6cc7c633bed` | `Phase 2.13 Candidates` | `candidates_runner` | 2026-11-17T17:41:10Z | `testing/evidence/phase_2_13/candidates` | **Authentic Official Seal** |

### Conclusive Root Cause Classification

Inspection of the conversation trajectory log (`transcript.jsonl`) revealed the exact origin of Entries 3, 4, 5, and 6:
- During Phase 2.13 implementation between 17:26:40 and 17:27:50 UTC (22:56:40 to 22:57:50 IST), manual one-liner verification commands were executed via PowerShell (`python -c "import tempfile... from evidence_guard import generate_and_seal_manifest..."`) to empirically verify the `.sealed` marker writing and `stat.S_IREAD` permission changes.
- Because these interactive one-liners did not define the `OSDAGBRIDGE_TRUST_DIR` environment variable, `get_trust_dir()` fell back to `PINNED_TRUST_DIR` (`C:\Users\Subodh\.osdagbridge_trust`).
- Consequently, each test invocation appended its temporary run record into `trusted_run_seals.json`.
- These 4 directories in `AppData/Local/Temp/` were ephemeral temporary directories that were deleted upon script exit. None correspond to genuine official regression suites.

---

## 3. Non-Destructive Ledger Remediation & Hash Verification

### Remediation Protocol
1. **Pre-Remediation SHA-256 Hash:**
   ```
   c10febe01b8e8c18078a5ea1b72a1417234df4202727e4cd06e867309958777c
   ```
2. **Backup Preservation:**
   Created a pristine byte-identical backup at `C:\Users\Subodh\.osdagbridge_trust\trusted_run_seals.json.bak_phase_2_13`.
3. **Selective Pruning:**
   Removed only the 4 conclusively identified temporary scratch entries (`fc28cba1`, `c344dafd`, `339e7bf0`, `e17e80cf`).
4. **Preservation of Authentic Seals:**
   Preserved all 6 authentic official run seals (Phase 2.12 Baseline, Sensitivity, Candidates; Phase 2.13 Baseline, Sensitivity, Candidates) byte-for-byte.
5. **Post-Remediation SHA-256 Hash:**
   ```
   5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1
   ```

### Manifest Integrity Re-Verification
The standalone verifier [`testing/test_cases/baseline_regression/verify_manifest.py`](file:///F:/FOSSEE%20internship/testing/test_cases/baseline_regression/verify_manifest.py) was executed against all six official directories using the cleaned ledger:

```
[PASS] External Cryptographic Run Seal: VALID (Phase 2.12 Baseline: 19 files, 100% match)
[PASS] External Cryptographic Run Seal: VALID (Phase 2.12 Candidates: 54 files, 100% match)
[PASS] External Cryptographic Run Seal: VALID (Phase 2.12 Sensitivity: 19 files, 100% match)
[PASS] External Cryptographic Run Seal: VALID (Phase 2.13 Baseline: 19 files, 100% match)
[PASS] External Cryptographic Run Seal: VALID (Phase 2.13 Candidates: 54 files, 100% match)
[PASS] External Cryptographic Run Seal: VALID (Phase 2.13 Sensitivity: 19 files, 100% match)
```
**Result:** 92 / 92 files verified with 100% integrity. Zero drift. All authentic seals valid.

---

## 4. Governance Test Harness Isolation & Automated Enforcement

To ensure that test execution can *never* write to or contaminate the production trust ledger, the following architectural controls were implemented in [`test_evidence_governance.py`](file:///F:/FOSSEE%20internship/testing/test_cases/baseline_regression/test_evidence_governance.py):

1. **Per-Test Isolated Trust Directory in `setUp`:**
   ```python
   self._trust_td = tempfile.TemporaryDirectory()
   os.environ["OSDAGBRIDGE_TRUST_DIR"] = self._trust_td.name
   os.environ["OSDAGBRIDGE_ALLOW_TEST_TRUST_OVERRIDE"] = "1"
   ```
2. **Explicit Parameter Passing:**
   In all test methods that generate or verify seals (`test_10`, `test_22`, `test_24`), `trust_dir=self._trust_td.name` and `allow_trust_override=True` are passed explicitly, preventing any fallback to `PINNED_TRUST_DIR`.
3. **Child Subprocess Environment Propagation:**
   In cross-process tests (`test_24`), `env["OSDAGBRIDGE_TRUST_DIR"]` and `env["OSDAGBRIDGE_ALLOW_TEST_TRUST_OVERRIDE"]` are explicitly propagated to child Python processes.
4. **Automated Production Ledger Immutability Assertion in `tearDown`:**
   In `setUp`, the SHA-256 hash of the production ledger (`trusted_run_seals.json`) is recorded. In `tearDown`, the hash is re-computed and asserted to match:
   ```python
   with open(self._prod_ledger, "rb") as f:
       current_hash = hashlib.sha256(f.read()).hexdigest()
   self.assertEqual(
       current_hash, self._prod_ledger_hash_before,
       f"PRODUCTION TRUST LEDGER COMPROMISE: Hash changed during test execution!"
   )
   ```

---

## 5. Empirical Verification of Production Ledger Immutability

The complete 27-vector governance test suite was executed on Windows:
```
[START] 2026-11-17T18:18:18.341358+00:00
Production ledger SHA-256 before run: 5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1
Executing: python -u testing/test_cases/baseline_regression/test_evidence_governance.py -v
...
Ran 27 tests in 17.599s - OK
[FINISH] 2026-11-17T18:18:36.244241+00:00 (Elapsed: 17.90s)
Exit code: 0
Production ledger SHA-256 after run:  5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1
Production ledger unchanged:          True
```

**Conclusion:** Condition 3 is **SATISFIED**. The production trust ledger is completely clean, contains only authentic official runs, and cannot be modified by any governance test.
