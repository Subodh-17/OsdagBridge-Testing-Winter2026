# PHASE 2.4 — Evidence Manifest & Cryptographic Ledger

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Software Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Repository Baseline:** `source/OsdagBridge` (`dev` at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`)  
**Controlling Audit:** `reports/PHASE_2_3_FINAL_INDEPENDENT_GATE_AUDIT.md`  
**Date Generated:** 2026-11-16  

---

## 1. Directory Structure Overview

All Phase 2.4 evidence is permanently and immutably isolated under:
`F:\FOSSEE internship\testing\evidence\phase_2_4\`

The directory contains four dedicated functional trees:
1. `baseline/`: Pristine baseline execution logs for all 15 tests, machine-readable summary JSON, and recorded process exit code.
2. `sensitivity/`: Complete sensitivity matrix summary JSON, exit code, and per-test sensitivity JSON records.
3. `candidates/`: Dedicated candidate execution logs with distinct file suffixes for every condition (`_a_baseline.log`, `_b_correct.log`, `_c_naive.log`), preventing any overwrite.
4. `environment/`: Python 3.12 environment fingerprint, package inventory, and native module bindings.

---

## 2. Baseline Evidence Directory (`testing/evidence/phase_2_4/baseline/`)

| File Name | File Size | SHA-256 Checksum | Description |
| :--- | :---: | :---: | :--- |
| `baseline_exit_code.txt` | 1 byte | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` | Shell exit code recorded by runner (`0`) |
| `phase_2_4_baseline_summary.json` | 11,991 bytes | `0583737a33e951fe8b365f4b6350532f1ccbde87ba04f998931862dda63f5102` | Structured execution summary (15/15 matched) |
| `tc_reg_a01_factor_scaling.log` | 1,079 bytes | `5dda87b5d930b770bea7f125a5b34c31d450cbb5b8233bdf2052aec0ae569248` | Log for TC-REG-A01 baseline run |
| `tc_reg_a02_uls_combination_sum.log` | 1,659 bytes | `f4ff57a747c083c08962751a13b6d41baeadf4028327b6ed44a4f94e54a2678e` | Log for TC-REG-A02 baseline run |
| `tc_reg_b01_section_property_sync.log` | 1,977 bytes | `b806b2773be84150e49707b1eef17da9bcbbf482e8441b4bf4f21146da4afaa4` | Log for TC-REG-B01 baseline run |
| `tc_reg_c01_sectional_stress_range.log` | 1,760 bytes | `e5ff44284bbe41d8c58719acdeb1999e6beaac8ec5e3e60f7f7fa461b6f48816` | Log for TC-REG-C01 baseline run |
| `tc_reg_c02_fatigue_vehicle_analysis.log`| 1,724 bytes | `e3d81c13b25ea275bc6bc51a4e11c2fdb7865d2aae719686d7493f0d87366e77` | Log for TC-REG-C02 baseline run (Blocked DEC-018) |
| `tc_reg_cad_export_vs_screenshot.log` | 963 bytes | `61ff8833a21d1759ed6c4284e331e58a7a896e984d970483ddf038b9a3baf205` | Log for TC-REG-CAD baseline run |
| `tc_reg_cap_stiffener_buckling.log` | 1,336 bytes | `a8e4b35132025dc82c8b1e3aadd3e2f37c41c68f8f429570ce3b6e678325cabb` | Log for TC-REG-CAP baseline run |
| `tc_reg_d01_wind_speed_propagation.log` | 1,317 bytes | `f42bef71ccdaa007ab5597b6795cba90e62c1aadcaadf6cc812efb7c118a13ce` | Log for TC-REG-D01 baseline run |
| `tc_reg_d02_temperature_propagation.log`| 1,394 bytes | `fafe9359fd2a78b3867589748d65bc8a1c4ada079ea34fb9a3af1d271f8a5ed6` | Log for TC-REG-D02 baseline run (Blocked DEC-015) |
| `tc_reg_eq_load_conservation.log` | 2,040 bytes | `8451ee544a1fef8607e7c55b1c51cd5e3230b3df3b8c6c9d4de6ee728c6d0c16` | Log for TC-REG-EQ-LOAD-CONSERVATION run |
| `tc_reg_fs_clean_working_tree.log` | 1,477 bytes | `16254022d9fa47c3035d0802c34c1d80661e9a208214f5a927d8f34c19d80f63` | Log for TC-REG-FS baseline run |
| `tc_reg_geo_girder_count_alignment.log` | 996 bytes | `0f529876f10e0d028ca88a18138d6f47b8c1011b252c6fc4a6346ee8c4510235` | Log for TC-REG-GEO-COUNT baseline run |
| `tc_reg_geo_slab_section_properties.log`| 1,491 bytes | `e12a705b27ba402293f9c97493630581769c9b305970a753bc1e246911d79290` | Log for TC-REG-GEO-SLAB baseline run (Blocked DEC-013) |
| `tc_reg_mat_density_consistency.log` | 1,078 bytes | `63c949fa5f77d7edc3b89e746f75bb0583e26a732b56245d13bec4d07fe870fa` | Log for TC-REG-MAT baseline run |
| `tc_reg_rpt_exec_summary_status.log` | 1,413 bytes | `644cd6b299ccb54edd75be0824184a9fbf750fbc0e3032133865e57a396d6ca7` | Log for TC-REG-RPT baseline run |

---

## 3. Sensitivity Matrix Evidence Directory (`testing/evidence/phase_2_4/sensitivity/`)

| File Name | File Size | SHA-256 Checksum | Description |
| :--- | :---: | :---: | :--- |
| `sensitivity_exit_code.txt` | 3 bytes | `13bf7b3039c63bf5a50491fa3cfd8eb4e699d1ba1436315aef9cbe5711530354` | Shell exit code recorded by sensitivity runner (`0`) |
| `phase_2_4_sensitivity_matrix_summary.json`| 24,545 bytes | `579007e87908d1d7b3713b89087ce43eed6d353da57c08ec3dd3870f41bc7740` | Master sensitivity summary with candidate function hashes |
| `tc_reg_a01_factor_scaling_sensitivity.json` | 1,356 bytes | `dfeb3d30fb2e2698fe06fddc06719083e14afb3ed1a1509c5b161304d8b163c7` | Sensitivity record for TC-REG-A01 |
| `tc_reg_a02_uls_combination_sum_sensitivity.json` | 1,675 bytes | `1a8f3cdaa7eedc9d6ff6e82856b87c495a286e604c6c64cbce946553d96dba62` | Sensitivity record for TC-REG-A02 |
| `tc_reg_b01_section_property_sync_sensitivity.json` | 1,652 bytes | `6982210505613e7d3d267ff833365d2cf179616f9acab5ca044c75794bf8394a` | Sensitivity record for TC-REG-B01 |
| `tc_reg_c01_sectional_stress_range_sensitivity.json` | 1,633 bytes | `9b4c417fa08f428b324ae8087fc4bffb59a80bfdfb355975eec73d4006afe56d` | Sensitivity record for TC-REG-C01 |
| `tc_reg_c02_fatigue_vehicle_analysis_sensitivity.json` | 1,346 bytes | `2cf8cca1483815bde4125c3c0fd8c889b4e6021c75bf4e6cbfb166045a32e412` | Sensitivity record for TC-REG-C02 (Blocked) |
| `tc_reg_cad_export_vs_screenshot_sensitivity.json` | 1,310 bytes | `0f80bf4e726983c8e63f1784e68dfcacb1f9d8452f23a00e41d8d5a760a11ffc` | Sensitivity record for TC-REG-CAD |
| `tc_reg_cap_stiffener_buckling_sensitivity.json` | 1,570 bytes | `903f351da6b0e67243ab42d061f26e8c5e1702f9f43d606c328cd250177737e9` | Sensitivity record for TC-REG-CAP |
| `tc_reg_d01_wind_speed_propagation_sensitivity.json` | 1,540 bytes | `2e5e4e655cfc1748805773427cf62dd418091ef25e4f49bd03053cde2eb42eb7` | Sensitivity record for TC-REG-D01 |
| `tc_reg_d02_temperature_propagation_sensitivity.json` | 1,272 bytes | `ef5a34920f630145545c7b7ccce3db4c802581cee0a74ce8cf0116ac7cc95929` | Sensitivity record for TC-REG-D02 (Blocked) |
| `tc_reg_eq_load_conservation_sensitivity.json` | 1,626 bytes | `4569d6763a97a5db61a1cdaf0844033dce74f3848ebbb1d4df566f6cc6cd39a7` | Sensitivity record for TC-REG-EQ-LOAD-CONSERVATION |
| `tc_reg_fs_clean_working_tree_sensitivity.json` | 1,494 bytes | `1f24caa63eb5ca1b282ebac9914240733315ff0c974802abad534646541d8bd6` | Sensitivity record for TC-REG-FS |
| `tc_reg_geo_girder_count_alignment_sensitivity.json` | 1,440 bytes | `2fa410566e39dd03c53cb5ea4b0e33c7c695bc9882aa0c6086cfee768789ce7c` | Sensitivity record for TC-REG-GEO-COUNT |
| `tc_reg_geo_slab_section_properties_sensitivity.json` | 1,365 bytes | `8aa8043cb0f0dd6ad86b7ccbf51cdd1bc777a2d995a07fddd51fda5716e7f64f` | Sensitivity record for TC-REG-GEO-SLAB (Blocked) |
| `tc_reg_mat_density_consistency_sensitivity.json` | 1,450 bytes | `56502158ac5ddb5edde9e83e07d47a72260a6a72773467f2416d367c8e22d65c` | Sensitivity record for TC-REG-MAT |
| `tc_reg_rpt_exec_summary_status_sensitivity.json` | 1,539 bytes | `a91306814aaba899339366e1423629096c1917a59aa1d089d57c164651b861bc` | Sensitivity record for TC-REG-RPT |

---

## 4. Multi-Condition Candidate Logs Directory (`testing/evidence/phase_2_4/candidates/`)

All 12 actionable tests preserve distinct logs for all three conditions:
- `_a_baseline.log` (Baseline run)
- `_b_correct.log` (Minimal correct candidate run)
- `_c_naive.log` (Plausible naive candidate run)
Blocked tests (`c02`, `d02`, `geo_slab`) contain exclusively `_a_baseline.log`.

| Test Identifier | Condition (a) Log SHA-256 | Condition (b) Log SHA-256 | Condition (c) Log SHA-256 |
| :--- | :---: | :---: | :---: |
| `A01-FACTOR-SCALING` | `90384cc75693c28a...` | `4fffce6508707230...` | `4fc667ff2b988c51...` |
| `A02-ULS-COMBINATION-SUM` | `b9c8bd513f6b1bb3...` | `a41b4536a12eb6fb...` | `87144823cebd6fee...` |
| `B01-SECTION-PROPERTY-SYNC` | `31cf786363472513...` | `e09b03adf7a7a0f5...` | `0a1a4f626e32858a...` |
| `C01-SECTIONAL-STRESS-RANGE` | `fea0faf1f916a709...` | `f1c252f823a3bd1d...` | `69aa488430268771...` |
| `C02-FATIGUE-VEHICLE-ANALYSIS` | `befc04d012430bdf...` | *None (Blocked DEC-018)* | *None (Blocked DEC-018)* |
| `CAD-EXPORT-VS-SCREENSHOT` | `a807cb9dd31ea178...` | `429285093f65e2be...` | `a3ba72589e6eb130...` |
| `CAP-STIFFENER-BUCKLING` | `2df9fcf5c52c502b...` | `aee86c3d902bebc7...` | `83ea1cebb8889aa3...` |
| `D01-WIND-SPEED-PROPAGATION` | `fa78a2e7c4f4b238...` | `2d408f654b9cf4d2...` | `6687a41ec53be41b...` |
| `D02-TEMPERATURE-PROPAGATION` | `7be459998df91754...` | *None (Blocked DEC-015)* | *None (Blocked DEC-015)* |
| `EQ-LOAD-CONSERVATION` | `bc8e604724b1c676...` | `3715c328e81881cb...` | `dc7a0eaee9139366...` |
| `FS-CLEAN-WORKING-TREE` | `67c74cfbe1092b1e...` | `73f58cf2953732f8...` | `3f38b0c5051c4cbb...` |
| `GEO-GIRDER-COUNT-ALIGNMENT` | `7a0604afdaea45f2...` | `8dbb14047b181952...` | `b4091a6c075ad722...` |
| `GEO-SLAB-SECTION-PROPERTIES` | `3c1c1f63e7d1b29c...` | *None (Blocked DEC-013)* | *None (Blocked DEC-013)* |
| `MAT-DENSITY-CONSISTENCY` | `547cff27798af07d...` | `93b6ebb88e428c4a...` | `92fdaa027491e3da...` |
| `RPT-EXEC-SUMMARY-STATUS` | `6f9d0358c353a33e...` | `a8b5bf75c6dd3690...` | `f094a9012036cdee...` |

---

## 5. Candidate Mutation Function Cryptographic Hashes

Every candidate implementation function tested in `run_sensitivity_matrix.py` has been inspected via `inspect.getsource()` and fingerprinted via SHA-256:

| Candidate Function | Associated Test | Function Purpose | SHA-256 Checksum |
| :--- | :--- | :--- | :---: |
| `mut_b_a01` | TC-REG-A01 | Scales load magnitudes in LoadCase.add_load and applies to Line/Patch loads | `8aea6bd94b289a469c3d989a9d9fae374335228b3e5ef064b390941c05dac0f1` |
| `mut_c_a01` | TC-REG-A01 | Naive partial 1.15x scaling | `4747fc79c5045bd7072ff1c7c11cae54830368b63778b7a9d1b3b76171a18fc8` |
| `mut_b_b01` | TC-REG-B01 | Synchronizes _girder_section with snapped section geometry | `afbd3a38ffa14d64155ced209df4bee92a48021a4eb588c2dc2d48787a9016e1` |
| `mut_c_b01` | TC-REG-B01 | Updates metadata post-setup leaving OpenSees stiffness preliminary | `b9991206f368ad41d6b0577fc20c4a4505316ff1a0c4f82875a61dbadabeb858` |
| `mut_b_c01` | TC-REG-C01 | Genuine stress range across load cases in _extract_demands_from_analysis_results | `fffeae704f0d6ce8e3760ea4db247d48348633bf54b98fae8705e4f4fb02f542` |
| `mut_c_c01` | TC-REG-C01 | Zeroes envelope but leaves per-LC broken (moment as range) | `b13c7bb61c8a6703554030635e98f0e57209930f78c89da442f9b2fa68fba9a3` |
| `mut_b_a02` | TC-REG-A02 | Creates SIDL before DL combination and factors line/patch loads | `d48c8df6e685f6ce5fa8bf7d2d3858c89ce47101683be81f9ca086e42b6a78ea` |
| `mut_c_a02` | TC-REG-A02 | Factors SW and DW but omits crash barrier from BASIC_1 | `ff6caea7a1e05d045c704f05252ae07b22591ae9f893fa9e4ea235bf328905e4` |
| `mut_b_eq_load_conservation` | TC-REG-EQ-LOAD | Normalizes mesh tributary areas and segment integration for 100% equilibrium | `04d7d0dd6d86ebcb13ce474f85e5cf64d39ee73507d9fcaee7fa70222a075253` |
| `mut_c_eq_load_conservation` | TC-REG-EQ-LOAD | Normalizes patch loads only, leaving crash barrier shortfall (-37.5%) | `e2a05cf4cb09919b489ef0c30a597a7da9318b76c8c4bc6ec2cf4fdb07a98ca9` |
| `mut_b_d01` | TC-REG-D01 | Propagates wind speed, exposed height, barrier and railing heights | `ea165f12aa52d585b7468134710a30b2003c2069c99173c38bdae9c9f75ec54c` |
| `mut_c_d01` | TC-REG-D01 | Reads basic_wind_speed only, leaves height/barrier as defaults | `c97db3c28df7a88eb22c7a6e138a2e58286ca0792a5438885b59744c803ffc0d` |
| `mut_b_rpt` | TC-REG-RPT | Dynamically derives component outcomes across all girders and components | `c21e64906bbbf80f682d3ea9549326e9594f87243cbeceb0255c464aa6bfd5ea` |
| `mut_c_rpt` | TC-REG-RPT | Hardcodes "Girder design fail", failing Scenario 1 | `f280e227fc6e053fedd0da7e3160a3734e5a9539fa344e2ee04c004c0ff95a32` |
| `mut_b_geo_count` | TC-REG-GEO-COUNT | Sets bcfg.geometry.n_girders = bridge._girder_count() (4) | `4f4b1626c927f87961298816c27867fa780d6f466b70a793fc0c5f2ec39f506e` |
| `mut_c_geo_count` | TC-REG-GEO-COUNT | Sets bcfg.geometry.n_girders = 0 | `ca614a9235d9df967a33bc21d603e91129994c5e31f0cfb3f9ff7bdf7f938aa8` |
| `mut_b_cap` | TC-REG-CAP | Web strip buckling under IS 800:2007 Cl. 8.7.3.1 with r = tw / sqrt(12) | `c830dd5713ddda6b37ba4ef577b21dc98276f7535b91a78c187be06ee69cb0eb` |
| `mut_c_cap` | TC-REG-CAP | Evaluates squash load (fy / gm0) * A_wb / 1000 | `e7a17726e6328639e44bc6055d7fc7cf78a705193630fba1eecfa34341aa91e3` |
| `mut_b_mat` | TC-REG-MAT | Dynamically reads material.girder.density and applies to steel unit weight | `f0dd9ea24d26fdf24368dd9ea3114d591fe50d4f13459c735d46002f1a30263d` |
| `mut_c_mat` | TC-REG-MAT | Hardcodes database default 78.5 kN/m3 | `bfa1ba2aa6fa3869b2d861d8bc5db2ef25bfbc94477db1f94532a8435d045d0b` |
| `mut_b_fs` | TC-REG-FS | Anchors DB_PATH and Database default path to User AppData | `132e4d9ebca89ca39d671b56360c7b2c58976b9ee27b031cbaec11c2a1c2269a` |
| `mut_c_fs` | TC-REG-FS | Anchors ui module DB_PATH but leaves Database.__init__ unanchored | `9b369c0d75c8793b82736e4f32dc8fa97ee89dc1d84ea235542fca1215bb5fe7` |
| `mut_b_cad` | TC-REG-CAD | Baseline native OCC offscreen export (passes) | `d03da24a13bf73cb11b157488f7871b2d354a93322d716d123e4ebdfa05fa147` |
| `mut_c_cad` | TC-REG-CAD | Generates blank uniform image (std = 0.0) | `1e95cfc91ec671d02cf12c3f8f12db01484ca8f5f643e990390f1d5e3be0a4f5` |

---

## 6. Immutable Application Baseline Verification

- **Repository Root:** `F:\FOSSEE internship\source\OsdagBridge`
- **Current Branch:** `refs/heads/dev`
- **Frozen Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`
- **Working Tree Status:** 100% clean (`nothing to commit, working tree clean`)
- **Git Status Fingerprint:** Clean working tree verified prior to, during, and after Phase 2.4 execution.
- **SQLite Database Hashes:**
  - `source/OsdagBridge/data/Intg_osdag.sqlite`: `25f97857be91ca5be3eb31495c0c926db45bb38ec08bc88484fcf138d33ec148`
  - `source/OsdagBridge/src/osdagbridge/core/data/project_location/weather.sqlite`: `1d767658826d9cf848c4cf19cb4ee0c1c87515b13b1928092a188f574d320aa4`
