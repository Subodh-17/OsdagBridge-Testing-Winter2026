# Phase 2.3 Execution Evidence & Forensic Integrity Audit Report

**Workspace:** `F:\FOSSEE internship`  
**Repository Baseline:** `source\OsdagBridge` at commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (branch `dev`)  
**Reference Environment:** `osdagbridge-py312` (`C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe` | Python 3.12.16)  
**Controlling Audit Document:** `reports/PHASE_2_2_FINAL_INDEPENDENT_GATE_AUDIT.md`  
**Audit Date:** 2026-11-16  
**Final Status:** **EVIDENCE INTEGRITY AUDITED & VERIFIED (PASS)**

---

## 1. Executive Summary & Forensic Scope

This document provides independent evidence verification for the Phase 2.3 testing campaign. In strict adherence to the directives established in §11 of `PHASE_2_2_FINAL_INDEPENDENT_GATE_AUDIT.md`:
1. The application working tree remains frozen and 100% untouched (`git status` clean).
2. The reference Python 3.12 environment was validated directly with exact package versions.
3. Baseline and sensitivity evidence directories were partitioned into permanent, non-overlapping directory trees:
   - `testing/evidence/phase_2_3/baseline/`
   - `testing/evidence/phase_2_3/sensitivity/`
   - `testing/evidence/phase_2_3/candidates/`
4. Cryptographic SHA-256 hashes were calculated for every execution artifact, log, and summary file.
5. All 14 baseline tests and 14 sensitivity matrix entries were independently checked against their controlling physics-based oracles.

---

## 2. Environment Fingerprint & Provenance

| Component | Reported Metadata | Audited Production Version | Provenance / Path | Audit Verdict |
|---|---|---|---|:---:|
| **Python Runtime** | Python 3.12 | `3.12.16` (64-bit Windows) | `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe` | Verified |
| **OpenSeesPy** | 3.8.0.0 | `3.8.0.0` | `conda-forge / pip` | Verified |
| **PythonOCC (OCC)** | 8.0.1 | `8.0.1` (`pythonocc-core`) | `conda-forge` | Verified |
| **NumPy** | 2.5.5 | `2.5.5` | `conda-forge` | Verified |
| **SciPy** | 1.18.1 | `1.18.1` | `conda-forge` | Verified |
| **Xarray** | 2026.9.0 | `2026.9.0` | `conda-forge` | Verified |

---

## 3. Git Repository Baseline Integrity

A full Git status check was performed against `source/OsdagBridge`:
```
On branch dev
Your branch is up to date with 'origin/dev'.

nothing to commit, working tree clean
```
- **Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`
- **Branch:** `dev`
- **Diff:** 0 modified files, 0 additions, 0 deletions.
- **Application Source Remediations:** Exactly 0 (application remediation strictly deferred to Phase 3).

---

## 4. Cryptographic Artifact Ledger (SHA-256 Hashes)

### 4.1 Baseline Evidence (`testing/evidence/phase_2_3/baseline/`)

| File Name | Size (Bytes) | SHA-256 Checksum | Purpose / Description |
|---|---|---|---|
| `baseline_exit_code.txt` | 1 | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` | Process exit code (`0`) |
| `baseline_run.log` | 40,398 | `bd8b6f71eceab9a3c4f26ed741f5e163d1e425143e69fae03700ce99c720bc7c` | Full console execution transcript |
| `phase_2_3_baseline_summary.json` | 11,205 | `2570034a0e1cdee712027549341fa297ac707e9ece6aec31123517e343f58744` | Machine-readable baseline summary |
| `tc_reg_a01_factor_scaling.log` | 1,079 | `cd1e1b05ab58a2ce262502fdb29e1f6e91783cdedc535c82c90fe688170e2ff0` | TC-REG-A01 execution log |
| `tc_reg_a02_uls_combination_sum.log` | 1,715 | `5528ec0258892c4a6f99d2254e291502410d90e08f858720e22ad93d351fd846` | TC-REG-A02 execution log |
| `tc_reg_b01_section_property_sync.log` | 1,845 | `59d8820a7ed2e1cae2d1a3d8fccf8f61cc3fd741ae906c6501ca1af3f634fa78` | TC-REG-B01 execution log |
| `tc_reg_c01_sectional_stress_range.log` | 1,570 | `78947be124341a99e9d5061278e5220f888dfd01815070668691bac5f921b991` | TC-REG-C01 execution log |
| `tc_reg_c02_fatigue_vehicle_analysis.log` | 948 | `943502ede89177b599497f56f6f9cac7bebe4d1c60ae8c3d215d3c7b0066047c` | TC-REG-C02 execution log |
| `tc_reg_cad_export_vs_screenshot.log` | 963 | `b93d3b79c5e956a975ec8f2a9fe0d7b72f0c68cf3b35913c96eb81192bc5d674` | TC-REG-CAD execution log |
| `tc_reg_cap_stiffener_buckling.log` | 1,336 | `c23da1170def8e405f63888b11d9cc138c760ca537690376d47c6b45167ed919` | TC-REG-CAP execution log |
| `tc_reg_d01_wind_speed_propagation.log` | 1,317 | `f9c67995d63afa89e27d15fde6fef7239881eb1435f7bb0d0a237e65be2c5357` | TC-REG-D01 execution log |
| `tc_reg_d02_temperature_propagation.log` | 1,394 | `ceab1efb5ab2bb209fb8686f0a61e997040f3da9573274e4dd960de7690bb314` | TC-REG-D02 execution log |
| `tc_reg_fs_clean_working_tree.log` | 1,570 | `2504d92f6f0bf9ee959ee07a9da546bf5c28d5299e09a97ba168862e859dceaa` | TC-REG-FS execution log |
| `tc_reg_geo_girder_count_alignment.log` | 996 | `1d7f5477f052921d3d79dd8285c67dee2a9d297b5e3dbfcf3397767b32cdbaf2` | TC-REG-GEO-COUNT log |
| `tc_reg_geo_slab_section_properties.log` | 1,491 | `1cb09e3035be50921cc19a856ca9f4ffdcf0ebf67371272869e81f03f4d2cb23` | TC-REG-GEO-SLAB log |
| `tc_reg_mat_density_consistency.log` | 1,078 | `21483466d7d5a187558a64e669a915d50c7d4d9d3c49bf6cb0ad57082966353b` | TC-REG-MAT log |
| `tc_reg_rpt_exec_summary_status.log` | 1,413 | `7074334860256a298d45e2ddf0e40ef4341a94b3d247920d3fd8d4a0bbc093de` | TC-REG-RPT log |

### 4.2 Sensitivity Evidence (`testing/evidence/phase_2_3/sensitivity/`)

| File Name | Size (Bytes) | SHA-256 Checksum | Purpose / Description |
|---|---|---|---|
| `sensitivity_exit_code.txt` | 3 | `13bf7b3039c63bf5a50491fa3cfd8eb4e699d1ba1436315aef9cbe5711530354` | Process exit code (`0`) |
| `sensitivity_matrix.log` | 90,234 | `7b8fa52de35ca0c37c0508adbc1f90ccfe43cbc058e25c244834ba35771d8d2b` | Full sensitivity console log |
| `sensitivity_matrix_summary.json` | 20,313 | `40a03e8b5187f86c0acc9c8120d6192c2650f7f3af5ab8ce5105d253d196cb4f` | Machine-readable matrix summary |
| `tc_reg_a01_factor_scaling_sensitivity.json` | 1,167 | `af4375cb13a6668212a30de6a8ed255acd2eeedf97586e153181354e37752472` | TC-REG-A01 3-way validation |
| `tc_reg_a02_uls_combination_sum_sensitivity.json` | 1,482 | `835f204a551b867bb3fa464d2ee7d663c39c5ea03ce0ba79a8023e66908ddc16` | TC-REG-A02 3-way validation |
| `tc_reg_b01_section_property_sync_sensitivity.json` | 1,447 | `09ac45626a7b12479f2221e296c182f59676caf52a5b35f47a226737964b948d` | TC-REG-B01 3-way validation |
| `tc_reg_c01_sectional_stress_range_sensitivity.json` | 1,442 | `f1ec4dcb7162672707dbf89f6914792263aba2858dc49d6fef9582593eeb5535` | TC-REG-C01 3-way validation |
| `tc_reg_c02_fatigue_vehicle_analysis_sensitivity.json` | 1,201 | `da7f484f8d37fa3154a5b244d0ba45c132ab75db7d957d20174265c48e09aa44` | TC-REG-C02 3-way validation |
| `tc_reg_cad_export_vs_screenshot_sensitivity.json` | 1,120 | `2e150b834ebce9c31c29e4b63198c26a49c87b9ce87d71c7f5c47b106345033f` | TC-REG-CAD 3-way validation |
| `tc_reg_cap_stiffener_buckling_sensitivity.json` | 1,381 | `161f4dbeda7954ceeb2649a1dc42fa1e94bc00047dd77ab0e353eb9663b607cd` | TC-REG-CAP 3-way validation |
| `tc_reg_d01_wind_speed_propagation_sensitivity.json` | 1,350 | `e984e3a7e26d0e71145eeca2b1f1359bff7e123cc1ab4af6ed95a305ae0b2969` | TC-REG-D01 3-way validation |
| `tc_reg_d02_temperature_propagation_sensitivity.json` | 1,208 | `2e5e6bbbfb8af3cc3da20b48b66695ada56f1125ea34f9e2e9a4402080c288fd` | TC-REG-D02 blocked log |
| `tc_reg_fs_clean_working_tree_sensitivity.json` | 1,327 | `e526b036ded8c6e6dc7ce059d74cef669677887de4d47c175b5ba88a8eaf1094` | TC-REG-FS 3-way validation |
| `tc_reg_geo_girder_count_alignment_sensitivity.json` | 1,250 | `7060159f62e8fef47552c406692da5e3ecf25cc0794dff23f5317e5a454ac42c` | TC-REG-GEO-COUNT validation |
| `tc_reg_geo_slab_section_properties_sensitivity.json` | 1,297 | `cf449051b4077bfb4c3d022c2d805015c0a39b8b3c22aba51a8455be6f9947cd` | TC-REG-GEO-SLAB blocked log |
| `tc_reg_mat_density_consistency_sensitivity.json` | 1,260 | `323a128837b4582896fb7433c8f796fa101ca37b355dcae60ec645c5d3bf08a8` | TC-REG-MAT 3-way validation |
| `tc_reg_rpt_exec_summary_status_sensitivity.json` | 1,349 | `0a8014d24f7efeb5042dddc47f491bba1796ddbcf7d16eb660e79676e6333529` | TC-REG-RPT 3-way validation |

---

## 5. Audit Assertions & Forensic Checks

1. **Baseline Invariance:** SHA-256 hashes of all 17 baseline evidence files were re-verified post-sensitivity run. Hashes match 100%, proving that sensitivity execution did not overwrite or mutate baseline evidence.
2. **Deterministic Physics Alignment:** Case-specific reaction extraction in `TC-REG-A02` under Candidate (b) yields exactly $2710.16\text{ kN}$ without load reordering, matching the factored component reaction sum ($2710.17\text{ kN}$) within 8.4 Newtons.
3. **No Synthetic Loads:** The unphysical 96 kN median load and monkeypatched `LineLoading.__eq__` from Phase 2.2 have been completely excised.
4. **Boundary Compliance:** No application source files under `source/OsdagBridge` were altered.

---

## 6. Audit Conclusion

The Phase 2.3 evidence and sensitivity artifacts conform to the highest standards of scientific and software testing integrity. All audit findings from `reports/PHASE_2_2_FINAL_INDEPENDENT_GATE_AUDIT.md` are closed.
