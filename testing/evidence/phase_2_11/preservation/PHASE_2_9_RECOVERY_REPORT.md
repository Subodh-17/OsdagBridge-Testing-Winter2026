# Forensic Investigation & Recovery Report: Phase 2.9 Historical Candidate Logs

**Date:** 2026-11-17  
**Workspace:** `F:\FOSSEE internship`  
**Application Baseline:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`  
**Controlling Audit:** `reports/PHASE_2_10_FINAL_INDEPENDENT_GATE_AUDIT.md` (Finding F-04)  
**Report Status:** **AUTHENTICATED FORENSIC DISCLOSURE & BIT-EXACT RESTORATION**

---

## 1. Executive Summary & Root Cause Analysis

During Phase 2.10 execution, Claude's independent gate audit identified that four Phase 2.9 candidate logs in `testing/evidence/phase_2_9/candidates/` were overwritten in place between 11:18:59 and 11:20:52 UTC on 2026-11-17.

### Root Cause
In Phase 2.10, `evidence_guard.py` was invoked only at the top-level command-line entry point of `run_all_baseline_tests.py` and `run_sensitivity_matrix.py` in their `main()` functions. When individual test runner methods, candidate evaluation probes, or direct logger calls (`log_test_result()`) were invoked directly with custom `evidence_dir` paths or via module-level globals (`CANDIDATES_DIR`), the protection check was completely bypassed. Furthermore, although `phase_2_9` had been added to `PROTECTED_PHASES`, bypass calls never routed through `validate_evidence_directory()`, resulting in silent in-place overwrite.

The Phase 2.10 reports failed to detect or disclose this overwrite event because post-run manifest verification only checked the active phase's evidence directory, not prior historical directories.

---

## 2. Overwrite Discrepancy & Bit-Exact Recovery Record

All four overwritten logs were preserved before restoration, and then restored from their uncorrupted `_c_naive.log` twins in `testing/evidence/phase_2_9/candidates/`, which remained bit-identical to the original Phase 2.9 manifest (`testing/evidence/phase_2_9/hashes/manifest_hashes.json`).

| Relative Log Path | Original / Manifest Hash | Overwritten Disk Hash | Overwritten Size | Restored Disk Hash | Restored Size | Bit-Exact Parity |
|---|---|---|---|---|---|:---:|
| `candidates/tc_reg_eq_load_conservation.log` | `213966a3d12f78767afde28df8c32490772be1acfa4d6c4cfd9f74e719abb8cd` | `eae7b52676c8ebe6f4d1bfa2c6f0ff465db1aea504578e301520e27b94ef7a6d` | 6,048 B | `213966a3d12f78767afde28df8c32490772be1acfa4d6c4cfd9f74e719abb8cd` | 5,679 B | **100% MATCH** |
| `candidates/tc_reg_c01_sectional_stress_range.log` | `fa11727fd05dc5c4d840530b5156494a24abebd0ad90a08faa8c6105331bf3a1` | `2ed1edad3c589e37938efbdf10b4b13b4a26613567c067c8f0e85cac21b43c16` | 2,338 B | `fa11727fd05dc5c4d840530b5156494a24abebd0ad90a08faa8c6105331bf3a1` | 2,338 B | **100% MATCH** |
| `candidates/tc_reg_rpt_exec_summary_status.log` | `28453fe8e49b9f50cb4afddfd9d5b43110abcf97900da29d616ca9a101027583` | `d3e836ecf829969eb6b9573ae02186fd378ef4c2f12e4531b175aad9b4e53b26` | 3,100 B | `28453fe8e49b9f50cb4afddfd9d5b43110abcf97900da29d616ca9a101027583` | 3,014 B | **100% MATCH** |
| `candidates/tc_reg_b01_section_property_sync.log` | `195998d94e151006449b0898ada51bec0f159304c96b740e9d0baf5c99b12e5e` | `7403df5ae194d032d60bb6481bc109d3220614428a8e4fba3436fbaa5d2828d2` | 3,729 B | `195998d94e151006449b0898ada51bec0f159304c96b740e9d0baf5c99b12e5e` | 3,130 B | **100% MATCH** |

### Preservation of Overwritten Versions
The overwritten copies (generated during the Phase 2.10 test cycle) have been preserved in:
`testing/evidence/phase_2_11/preservation/overwritten_phase_2_9_versions/`

### Restoration Verification
Post-restoration SHA-256 verification confirms that all 100 entries in `testing/evidence/phase_2_9/hashes/manifest_hashes.json` match disk with 100.0% cryptographic parity.

---

## 3. Corrective Architecture Mandates for Phase 2.11
1. **Centralized Write Gateway:** All evidence file writes must route exclusively through an OS-level write gateway in `evidence_guard.py` that validates the canonical path at write-time immediately before opening the file.
2. **Complete Historical Inventory:** The protected phase directory set must dynamically discover and protect ALL historical evidence directories, including `phase_2_baseline`, `phase_2_repaired`, and `phase_2_10`.
3. **No Populated Directory Default:** If `--evidence-dir` is missing, the system must never default to an existing populated directory.
4. **External Seal & Post-Run Verifier:** Manifest hashes and run metadata must be recorded in an external ledger outside the mutable run directory, verified by an independent verification tool.
