# Phase 2.6 Evidence Forensic Investigation & Preservation Report

| Metadata | Details |
|---|---|
| **Date** | 2026-11-17 |
| **Investigation Authority** | QA Engineering Infrastructure & Evidence Governance |
| **Controlling Audit Reference** | `reports/PHASE_2_7_FINAL_INDEPENDENT_GATE_AUDIT.md` (§5.2, §7.7, §8.1) |
| **Target Directory** | `testing/evidence/phase_2_6/` |
| **Recorded Manifest** | `testing/evidence/phase_2_6/hashes/manifest_hashes.json` (93 items) |
| **Status** | 8 Mismatches Confirmed; Root Cause Identified; Formal Disclosure Recorded |

---

## 1. Executive Summary

During the Phase 2.7 Independent Gate Audit, the auditor re-hashed all 93 artifacts cataloged in `testing/evidence/phase_2_6/hashes/manifest_hashes.json` against disk files and identified that 8 of 93 files exhibited hash and file size mismatches.

A forensic investigation was initiated immediately under Workstream 0 of Phase 2.8.
The findings are:
1. **Root Cause Confirmed:** During early Phase 2.7 test runner development (between 18:32:39 and 18:38:43 UTC on 2026-11-16), test runners `run_all_baseline_tests.py` and `run_sensitivity_matrix.py` were executed prior to updating default output constants (`DEFAULT_EVIDENCE_DIR`, `SENSITIVITY_DIR`, `CANDIDATES_DIR`) from `phase_2_6` to `phase_2_7`. Intermediate test runs consequently directed their outputs into `testing/evidence/phase_2_6/`.
2. **Impact Assessment:**
   - **85 of 93 artifacts** remain 100% authentic, untouched, and strictly match their recorded manifest SHA-256 hashes.
   - All conditioned sensitivity logs (`_a_baseline.log`, `_b_correct.log`, `_c_naive.log`) under `phase_2_6/candidates/` remain 100% authentic and untouched.
   - 6 intermediate un-suffixed candidate logs in `phase_2_6/candidates/` were overwritten by intermediate Phase 2.7 development runs.
   - 2 baseline logs (`baseline/tc_reg_eq_load_conservation.log` and `baseline/tc_reg_fs_clean_working_tree.log`) were overwritten by intermediate development runs.
3. **Recovery Determination:** A full filesystem search of the repository confirmed that no duplicate backups of the original Phase 2.6 baseline logs for EQ and FS exist. These two specific Phase 2.6 baseline logs are formally marked and disclosed as **OVERWRITTEN / LOST**.
4. **Remediation & Governance Safeguard (DEC-023):**
   - Development and trial runs in Phase 2.8 and all future phases are strictly restricted to a temporary scratch directory (`testing/evidence/scratch/`).
   - Official evidence directories are marked write-once upon final deliverable execution.
   - Live stdout/stderr logging via explicit command-line redirection captures live execution provenance.

---

## 2. Inventory of the 8 Discrepant Files

| Relative Path | Manifest SHA-256 (Original) | Disk SHA-256 (Observed) | Manifest Size | Disk Size | Status |
|---|---|---|---|---|---|
| `baseline/tc_reg_eq_load_conservation.log` | `054876a7116ce1c00b2a128406038af25f3e1fe69d2f32f1d29d37952d1e4b1d` | `cdcda56bd559dc332c641cd1f86dee67b411b5766b7fd53e55e1ce69effa2ad2` | 4,247 B | 4,359 B | OVERWRITTEN (Lost) |
| `baseline/tc_reg_fs_clean_working_tree.log` | `cd1e28d7e63e02d5c9b3f2a3ec9cca12b9c13208405f30c3e0dac1634d49acf1` | `ab1ecb30bb82506af612091527466345e51356e2821ac23ffbe9ef8708e02ea2` | 2,028 B | 1,987 B | OVERWRITTEN (Lost) |
| `candidates/tc_reg_a02_uls_combination_sum.log` | `6b69e668424146c26f53eafaa87e4de1e5106848536fa4f02ad02094d12b07b6` | `0fecf5570bb56d70be4a4cdd397fe12da5d53f8725937e23b1b613ae31d12eef` | 2,003 B | 2,486 B | OVERWRITTEN (Intermediate) |
| `candidates/tc_reg_b01_section_property_sync.log` | `8fd719ce84f38f246693586785586d8078d02320ec4ed6a297df861154dd207e` | `7fe4da64dfeae5b0bb4420aa735931bd54d93a8cabc8a87f75a0f8e37db64897` | 2,027 B | 2,140 B | OVERWRITTEN (Intermediate) |
| `candidates/tc_reg_c01_sectional_stress_range.log` | `ff2e7b532061c04332d681cc931328ee89769d3715539583c06724cfe5655763` | `83de7855dccf7a9d37764d7bc98cc5e6962e88fa2d89636c6b688d5acb4ff650` | 2,046 B | 2,363 B | OVERWRITTEN (Intermediate) |
| `candidates/tc_reg_eq_load_conservation.log` | `0d490c374931b3335aefdc1cf3396e10e027e197986879105b45bc1c8fdff54a` | `40092b80eabf0e5b19eb241534dcb458c50ffdae07d4043af2df3ea87d43c32b` | 4,073 B | 3,917 B | OVERWRITTEN (Intermediate) |
| `candidates/tc_reg_fs_clean_working_tree.log` | `ab361431ea2a3d87a434890cbd1884aec3425c485ef644e09bb14559e7103a8f` | `c966fe8ec07aa4974d50d8e3dd6a60c55373210b0ae19cb4c261b0d2abe66824` | 1,651 B | 1,685 B | OVERWRITTEN (Intermediate) |
| `candidates/tc_reg_rpt_exec_summary_status.log` | `89d3466d20aa00839f0d63b4aabbb1bbdbd52f5affbbc38ff0b7c2362d6d36ae` | `d7ca1f685f7c5b1fb293bbffb1207dc9b13bd17dc703d1fdbc6729d4fceaf35a` | 2,415 B | 2,114 B | OVERWRITTEN (Intermediate) |

---

## 3. Preservation Archive Creation

To guarantee that no further evidence mutation or drift can occur:
1. Current disk states of all evidence directories (Phase 1D, Phase 2.3, Phase 2.4, Phase 2.5, Phase 2.6, Phase 2.7) have been recursively hashed directly from disk bytes.
2. The preservation record is stored in `testing/evidence/phase_2_8/preservation/manifest_preservation.json`.
3. In Phase 2.8, all development runs are strictly isolated to `testing/evidence/scratch/`.
