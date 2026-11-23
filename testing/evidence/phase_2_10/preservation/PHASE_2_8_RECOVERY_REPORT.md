# Phase 2.8 Candidate Evidence Recovery Report

**Phase:** Phase 2.10 Independent Gate Remediation  
**Date:** 2026-11-17  
**Status:** Completed & Bit-Verified  
**Baseline Git HEAD:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`  

---

## 1. Executive Summary & Finding Reference

In Section 2 and Section 12 of `reports/PHASE_2_9_FINAL_INDEPENDENT_GATE_AUDIT.md`, independent auditor Claude identified that four candidate log files in `testing/evidence/phase_2_8/candidates/` were overwritten during Phase 2.9 execution:
1. `tc_reg_a02_uls_combination_sum.log`
2. `tc_reg_eq_load_conservation.log`
3. `tc_reg_fs_clean_working_tree.log`
4. `tc_reg_rpt_exec_summary_status.log`

The root cause was identified: during the Phase 2.9 runner execution, the runner wrote directly to the base candidate log filenames in `testing/evidence/phase_2_8/candidates/` due to a missing guard configuration, modifying files that belonged to the frozen Phase 2.8 evidence record.

However, forensic analysis revealed that the Phase 2.8 test execution had generated bit-identical candidate variants alongside the base names, specifically `_c_naive.log` for each test. Furthermore, the official Phase 2.8 hash manifest (`testing/evidence/phase_2_8/hashes/manifest_hashes.json`, recorded at 2026-11-17 12:04) recorded the exact SHA-256 digests and byte counts for both the base logs and their `_c_naive.log` twins prior to corruption.

---

## 2. Preservation of Overwritten Phase 2.9 Artifacts

Before performing recovery, the four overwritten files (dating from 2026-11-17 15:30 to 15:33) were preserved into:
`testing/evidence/phase_2_10/preservation/overwritten_phase_2_8_versions/`

### Preserved Overwritten Files:
| File | Byte Size | SHA-256 Digest |
|---|---|---|
| `tc_reg_a02_uls_combination_sum.log` | 2,565 | `a8594916a22c5443fa3831d1dbe52367db6a9783f8b05dcfa526084a44eeec5f` |
| `tc_reg_eq_load_conservation.log` | 5,679 | `9944c6806509f7a7dfd221a7364125f448c9bf39db1b6fbf9143bfdbad618a8b` |
| `tc_reg_fs_clean_working_tree.log` | 1,905 | `04d6e902b74f3ffcc9bc41249b25bc8b98eb512c9bf14a480521e428c4e61d67` |
| `tc_reg_rpt_exec_summary_status.log` | 3,014 | `150b07b489dca5c75665181755104ca65ee1a35940d99824bb8cf145d2fef8be` |

---

## 3. Bit-Exact Restoration & Verification

Each of the four files was restored from its uncorrupted twin (`*_c_naive.log`) in `testing/evidence/phase_2_8/candidates/`.

The restored files were then independently re-hashed and verified against the controlling historical manifest `testing/evidence/phase_2_8/hashes/manifest_hashes.json`:

| File Name | Restored Source | Manifest Expected SHA-256 | Restored SHA-256 | Status |
|---|---|---|---|---|
| `tc_reg_a02_uls_combination_sum.log` | `tc_reg_a02_uls_combination_sum_c_naive.log` | `2a61229c81ee5ab3fb96d26c4f10351ce297ebd955b3bf00ee78febd35816fc9` | `2a61229c81ee5ab3fb96d26c4f10351ce297ebd955b3bf00ee78febd35816fc9` | **MATCH (100%)** |
| `tc_reg_eq_load_conservation.log` | `tc_reg_eq_load_conservation_c_naive.log` | `33d432ce8c60d3470ba5159a7d99e24a1f312a1a311d93527baeaafd127b1b27` | `33d432ce8c60d3470ba5159a7d99e24a1f312a1a311d93527baeaafd127b1b27` | **MATCH (100%)** |
| `tc_reg_fs_clean_working_tree.log` | `tc_reg_fs_clean_working_tree_c_naive.log` | `efd85cead472a368076e194b33be83681776498aedb4b56e401688bf59e0fd9d` | `efd85cead472a368076e194b33be83681776498aedb4b56e401688bf59e0fd9d` | **MATCH (100%)** |
| `tc_reg_rpt_exec_summary_status.log` | `tc_reg_rpt_exec_summary_status_c_naive.log` | `b84e57fbafc93fd2516bea45572aad4960c5dfa20335576ae3168c2df7d5a728` | `b84e57fbafc93fd2516bea45572aad4960c5dfa20335576ae3168c2df7d5a728` | **MATCH (100%)** |

All four files in `testing/evidence/phase_2_8/candidates/` are now 100% byte-for-byte identical to their state at the conclusion of Phase 2.8.
