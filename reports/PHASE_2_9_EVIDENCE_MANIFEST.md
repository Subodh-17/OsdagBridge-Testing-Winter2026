# PHASE 2.9 — Complete Cryptographic Evidence Manifest

**Date:** 2026-11-17  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`, 100% clean)  
**Controlling Document:** `reports/PHASE_2_8_FINAL_INDEPENDENT_GATE_AUDIT.md`  
**Evidence Directory Root:** `testing\evidence\phase_2_9\`  
**Total Artifacts Cataloged:** **100**  

---

## 1. Evidence Overview & Integrity Guarantees

All artifacts cataloged below were produced under strict fail-closed write-once governance enforced by `testing/test_cases/baseline_regression/evidence_guard.py`.
Every file SHA-256 hash was computed directly from disk bytes at the completion of official Phase 2.9 baseline and sensitivity executions.

| Subdirectory | Purpose | Artifact Count | Subdirectory Status |
|:---|:---|:---:|:---:|
| `baseline/` | Official 15-test baseline regression logs, summary JSON, console output, and exit code | 18 | COMPLETE |
| `sensitivity/` | 15 individual sensitivity matrix evaluations, summary JSON, console output, and exit code | 18 | COMPLETE |
| `candidates/` | Multi-condition execution logs (_a_baseline, _b_correct, _c_naive) | 54 | COMPLETE |
| `preservation/` | Restored historical logs, overwritten archive, and historical manifests | 10 | COMPLETE |
| **Total** | **Comprehensive Phase 2.9 Verification Suite** | **100** | **100% CRYPTOGRAPHICALLY SECURED** |

---

## 2. Baseline Evidence Manifest (`baseline/`)

| # | Relative Path | Size (Bytes) | SHA-256 Digest |
|:---:|:---|:---:|:---|
| 1 | `baseline/baseline_exit_code.txt` | 3 | `13bf7b3039c63bf5a50491fa3cfd8eb4e699d1ba1436315aef9cbe5711530354` |
| 2 | `baseline/console_output.txt` | 47600 | `a968a7bda0c0669470fc40050ea696682134a77a74bc1f0af442d1cc7512817d` |
| 3 | `baseline/phase_2_9_baseline_summary.json` | 14605 | `1d7bd0d464fb56cc2490794acab3a41d0b84797f758fefd9f1aa407943f66895` |
| 4 | `baseline/tc_reg_a01_factor_scaling.log` | 1079 | `1e59ce9b328d07615cb88e135165a4a590c33e2ea9e4d725f0d0ade11df0a790` |
| 5 | `baseline/tc_reg_a02_uls_combination_sum.log` | 2563 | `3549efcc7abcbb7f326cd096f2b174f9cc90e16f0411b3ae041308c9e5254f94` |
| 6 | `baseline/tc_reg_b01_section_property_sync.log` | 3130 | `fbe27d1412b620d520cc36698b2ca874af9b2a3cdc0ace3e9df2fc1b1d5eca11` |
| 7 | `baseline/tc_reg_c01_sectional_stress_range.log` | 2345 | `eeaa53391fe8f5ed7ab533a7afcef8d0578777b544487356c8239d989843be0d` |
| 8 | `baseline/tc_reg_c02_fatigue_vehicle_analysis.log` | 1715 | `1feb7a3c4ff5eb8f8f767b27572122e6eb405f02e6dc16c846573e6575af3258` |
| 9 | `baseline/tc_reg_cad_export_vs_screenshot.log` | 963 | `6502cdfaad60382b61a86747a5f1dfffe4e6dac21c41370636fee0f28d1281a8` |
| 10 | `baseline/tc_reg_cap_stiffener_buckling.log` | 1336 | `c64234aaea1b96c0306f2c28ba6ef3472069983fcaf02b3a2c1561737f7a3145` |
| 11 | `baseline/tc_reg_d01_wind_speed_propagation.log` | 1317 | `fe3777ccdc2e25a185b6725f08ff32a6dc3c555a1fa4bff2885c646fcf715656` |
| 12 | `baseline/tc_reg_d02_temperature_propagation.log` | 1394 | `ab2e91fdbdf121fedb15bd3c44bf75b47fdec2df18d2b14e7908b601a8f15299` |
| 13 | `baseline/tc_reg_eq_load_conservation.log` | 5945 | `3aa2b793995b7a776454c977259fd672a6fde6f2ad0f0cacfd1d059578423fe4` |
| 14 | `baseline/tc_reg_fs_clean_working_tree.log` | 2444 | `e631e714f4be533023028d0312ed357093a23130960bcb62f955c663016e789c` |
| 15 | `baseline/tc_reg_geo_girder_count_alignment.log` | 996 | `263776d985255fd6b6b0d746c2390c16cbd95500771a094b02fa52d394c63f20` |
| 16 | `baseline/tc_reg_geo_slab_section_properties.log` | 1491 | `6d6e52526acab63d4c33bd8f20a5b2a1d0b631b34e29b5c135d9c7a72d539884` |
| 17 | `baseline/tc_reg_mat_density_consistency.log` | 1078 | `3615a4cef2e208ed54592857e3529382d6a2a3a12f0b1b8e789696bc548a4e5c` |
| 18 | `baseline/tc_reg_rpt_exec_summary_status.log` | 3312 | `09e9b08ceb167e8f45941abdddd5cabad72bd9cab21c5e7a69b96ba5ae634852` |

---

## 3. Sensitivity Matrix Manifest (`sensitivity/`)

| # | Relative Path | Size (Bytes) | SHA-256 Digest |
|:---:|:---|:---:|:---|
| 1 | `sensitivity/console_output.txt` | 94050 | `ece2ffd52e1b49bd0287f65dc4cc06a64614c77c768304ed9f507823bac0d3e3` |
| 2 | `sensitivity/phase_2_9_sensitivity_matrix_summary.json` | 29370 | `a65c641a1f0351b6fb07c5086857d498f6344e675555c6aa961c636c4c67f170` |
| 3 | `sensitivity/sensitivity_exit_code.txt` | 3 | `13bf7b3039c63bf5a50491fa3cfd8eb4e699d1ba1436315aef9cbe5711530354` |
| 4 | `sensitivity/tc_reg_a01_factor_scaling_sensitivity.json` | 1357 | `f08eabcf700cff721085d2fab78985dae17d349d0ac48fa8e30aa2b0283e734e` |
| 5 | `sensitivity/tc_reg_a02_uls_combination_sum_sensitivity.json` | 1846 | `fffe11f43236472625eefb5b7cb35562800c3f55c28292095ef91391e520437b` |
| 6 | `sensitivity/tc_reg_b01_section_property_sync_sensitivity.json` | 1533 | `e9da3fe30a50d1c45f0d6cfed5d64c61dcff48a1e26a90fd26f3dff2dc56f625` |
| 7 | `sensitivity/tc_reg_c01_sectional_stress_range_sensitivity.json` | 1703 | `4dd6969875090482b881be713f9386690c292e3c03c5b00ba1fc3848f4b1f9e6` |
| 8 | `sensitivity/tc_reg_c02_fatigue_vehicle_analysis_sensitivity.json` | 1348 | `1678180c3959d773d414efbbda0b6579a0ee6a9db227990f4b43263073ddc839` |
| 9 | `sensitivity/tc_reg_cad_export_vs_screenshot_sensitivity.json` | 1310 | `91c2c2d8ea425fdf2349ef1576108f81f41369697b046ab528845b2f351a0269` |
| 10 | `sensitivity/tc_reg_cap_stiffener_buckling_sensitivity.json` | 1571 | `6009761aef441c6d3d32d2e1e53abcc616565f45fa22d1c11401b1291f71d17c` |
| 11 | `sensitivity/tc_reg_d01_wind_speed_propagation_sensitivity.json` | 1540 | `10bdb2c66bcdf3445e4d462a142ecc03af57c8431c179758721aba04fac3b406` |
| 12 | `sensitivity/tc_reg_d02_temperature_propagation_sensitivity.json` | 1274 | `41c59a3182d8c909c60fa0d12fe0771260570bf66c03206abae3f7750a2570c2` |
| 13 | `sensitivity/tc_reg_eq_load_conservation_sensitivity.json` | 2170 | `a21cbe8923ecc68f21826fbdb364dee1d7fecdb83f4c0c20d6d52de20371c04a` |
| 14 | `sensitivity/tc_reg_fs_clean_working_tree_sensitivity.json` | 1689 | `795c13225def18c6f97450679e9b59f285b63f044aaabac551219774eb03b964` |
| 15 | `sensitivity/tc_reg_geo_girder_count_alignment_sensitivity.json` | 1438 | `acbb918fa2fd3769a7d61421042d4f51ac92b62edbb333f889f71eb8e10d7ca6` |
| 16 | `sensitivity/tc_reg_geo_slab_section_properties_sensitivity.json` | 1365 | `8aa8043cb0f0dd6ad86b7ccbf51cdd1bc777a2d995a07fddd51fda5716e7f64f` |
| 17 | `sensitivity/tc_reg_mat_density_consistency_sensitivity.json` | 1450 | `b997fc6d405dba6ef84f4706d02f80fa63ea49f80ff79f1b414cdc511657b0af` |
| 18 | `sensitivity/tc_reg_rpt_exec_summary_status_sensitivity.json` | 5500 | `1bf4a0d3719d7284e0f6bead18b6ce3f5d8e34daefaefd798e4e95a13fb6418a` |

---

## 4. Candidate Execution Logs Manifest (`candidates/`)

| # | Relative Path | Size (Bytes) | SHA-256 Digest |
|:---:|:---|:---:|:---|
| 1 | `candidates/tc_reg_a01_factor_scaling.log` | 1079 | `2299098688adb0384d7c9436b551a93f61463bfce4565ee3492cd988c804fb28` |
| 2 | `candidates/tc_reg_a01_factor_scaling_a_baseline.log` | 1079 | `cc463046aa265529af65fcffc37b8fd54d768dea2bdcafc614f8033b286a3cad` |
| 3 | `candidates/tc_reg_a01_factor_scaling_b_correct.log` | 1057 | `a99b67aa589785e787184a471b1289dcc7b8e341bb6769647b927aaa6ba1813e` |
| 4 | `candidates/tc_reg_a01_factor_scaling_c_naive.log` | 1079 | `2299098688adb0384d7c9436b551a93f61463bfce4565ee3492cd988c804fb28` |
| 5 | `candidates/tc_reg_a02_uls_combination_sum.log` | 2565 | `cf8b15a7fd72826f4b50eb73d6cf73abc8b0c9a26aacfb84802d9e4feca57971` |
| 6 | `candidates/tc_reg_a02_uls_combination_sum_a_baseline.log` | 2563 | `edcaf225d36e68825ae81f1b0717bbdf846530b8de33d3935ffd49f70ff9d534` |
| 7 | `candidates/tc_reg_a02_uls_combination_sum_b_correct.log` | 2291 | `da556167ef8a536af11bf8494e67b7a2c445c4a5bfa7606e895f6c55cc05e230` |
| 8 | `candidates/tc_reg_a02_uls_combination_sum_c_naive.log` | 2565 | `cf8b15a7fd72826f4b50eb73d6cf73abc8b0c9a26aacfb84802d9e4feca57971` |
| 9 | `candidates/tc_reg_b01_section_property_sync.log` | 3130 | `195998d94e151006449b0898ada51bec0f159304c96b740e9d0baf5c99b12e5e` |
| 10 | `candidates/tc_reg_b01_section_property_sync_a_baseline.log` | 3130 | `680d297316a427fc6899e10327bffdd93adffcc04ab856609812453d3bebfb0d` |
| 11 | `candidates/tc_reg_b01_section_property_sync_b_correct.log` | 2997 | `851a0c2bb9602cfe56449c83848cb60a5e72e305aa3cfbd3394ef3a50f8ec931` |
| 12 | `candidates/tc_reg_b01_section_property_sync_c_naive.log` | 3130 | `195998d94e151006449b0898ada51bec0f159304c96b740e9d0baf5c99b12e5e` |
| 13 | `candidates/tc_reg_c01_sectional_stress_range.log` | 2338 | `fa11727fd05dc5c4d840530b5156494a24abebd0ad90a08faa8c6105331bf3a1` |
| 14 | `candidates/tc_reg_c01_sectional_stress_range_a_baseline.log` | 2345 | `14e9a3a4accdd539e33969f35b8cf359106914df1d6948b151527408cdaf53ea` |
| 15 | `candidates/tc_reg_c01_sectional_stress_range_b_correct.log` | 2308 | `0afa0d5f2f6c019f3976fcbfd0f385ccbd4e475e6e848182bc06e09265b82fdf` |
| 16 | `candidates/tc_reg_c01_sectional_stress_range_c_naive.log` | 2338 | `fa11727fd05dc5c4d840530b5156494a24abebd0ad90a08faa8c6105331bf3a1` |
| 17 | `candidates/tc_reg_c02_fatigue_vehicle_analysis.log` | 1715 | `df2f78f5f5cace48d2e2b44d89e2f36a0fbba2fed2426acec0a5ac2f0a096e0d` |
| 18 | `candidates/tc_reg_c02_fatigue_vehicle_analysis_a_baseline.log` | 1715 | `df2f78f5f5cace48d2e2b44d89e2f36a0fbba2fed2426acec0a5ac2f0a096e0d` |
| 19 | `candidates/tc_reg_cad_export_vs_screenshot.log` | 942 | `58c1c6b89aa2c85eba210449c34a7a93a97e20cbd9abaa6100520114692ae451` |
| 20 | `candidates/tc_reg_cad_export_vs_screenshot_a_baseline.log` | 963 | `74dcaf8e735af52e0639ece54704bcbbe823fd1ab077786022cafb4a3d46e05e` |
| 21 | `candidates/tc_reg_cad_export_vs_screenshot_b_correct.log` | 963 | `b988deebb89a0cf02a5c04642c7cb58a0328e9e94741304c8877a0237388a0ec` |
| 22 | `candidates/tc_reg_cad_export_vs_screenshot_c_naive.log` | 942 | `58c1c6b89aa2c85eba210449c34a7a93a97e20cbd9abaa6100520114692ae451` |
| 23 | `candidates/tc_reg_cap_stiffener_buckling.log` | 1328 | `cf9a75c5bfea6dfc8ec7964e7b291d6f22ee0f38033126d873c7e790820c02fa` |
| 24 | `candidates/tc_reg_cap_stiffener_buckling_a_baseline.log` | 1336 | `26af528e115c8f0322751c4b973f623923ed9e9e532d97db15daf5b864b549c2` |
| 25 | `candidates/tc_reg_cap_stiffener_buckling_b_correct.log` | 1226 | `be61554b3f2857bbb17c04a0f9f674008f7ecedd5be717d3f36724078d02b79e` |
| 26 | `candidates/tc_reg_cap_stiffener_buckling_c_naive.log` | 1328 | `cf9a75c5bfea6dfc8ec7964e7b291d6f22ee0f38033126d873c7e790820c02fa` |
| 27 | `candidates/tc_reg_d01_wind_speed_propagation.log` | 1317 | `6304f5dd115b29f073ab3af1ae69289851a2ca5c0d439a814b276758fc567eae` |
| 28 | `candidates/tc_reg_d01_wind_speed_propagation_a_baseline.log` | 1317 | `cd5fd5acebf4f85255845313f0894314aef0cf0bfb7f0919e4fd70166c266784` |
| 29 | `candidates/tc_reg_d01_wind_speed_propagation_b_correct.log` | 1188 | `3a493c34eac71c133dc2d0c72314c27ea06d53f34ad6d8fc742fa69ba3ba6d66` |
| 30 | `candidates/tc_reg_d01_wind_speed_propagation_c_naive.log` | 1317 | `6304f5dd115b29f073ab3af1ae69289851a2ca5c0d439a814b276758fc567eae` |
| 31 | `candidates/tc_reg_d02_temperature_propagation.log` | 1394 | `6d622abe7201d954ec0e3b8d54196ad4d1a7c1a077624d94bfd60c5b217e2931` |
| 32 | `candidates/tc_reg_d02_temperature_propagation_a_baseline.log` | 1394 | `6d622abe7201d954ec0e3b8d54196ad4d1a7c1a077624d94bfd60c5b217e2931` |
| 33 | `candidates/tc_reg_eq_load_conservation.log` | 5679 | `213966a3d12f78767afde28df8c32490772be1acfa4d6c4cfd9f74e719abb8cd` |
| 34 | `candidates/tc_reg_eq_load_conservation_a_baseline.log` | 5945 | `066a679c0a1f9fca8fc2005015c7b5ce4c6b095e46e88832cc4caf828efce865` |
| 35 | `candidates/tc_reg_eq_load_conservation_b_correct.log` | 5452 | `638d35c4ecc644bf9d5f44a6beb67ea5be7368e211e08e09dbfbc1d7a1388e96` |
| 36 | `candidates/tc_reg_eq_load_conservation_c_naive.log` | 5679 | `213966a3d12f78767afde28df8c32490772be1acfa4d6c4cfd9f74e719abb8cd` |
| 37 | `candidates/tc_reg_fs_clean_working_tree.log` | 1905 | `ca892054df235f6e72edcfdd5912c074bb2871f368b878848ad792fef972e272` |
| 38 | `candidates/tc_reg_fs_clean_working_tree_a_baseline.log` | 2445 | `3274347d27e80ea5c52347a4cd40827529995b0eea2ec3b3980f52ad778be325` |
| 39 | `candidates/tc_reg_fs_clean_working_tree_b_correct.log` | 2026 | `ea2faeae64d48991657e9bb3d42f1d6d0563b981f111bb431a46ee2899720906` |
| 40 | `candidates/tc_reg_fs_clean_working_tree_c_naive.log` | 1905 | `ca892054df235f6e72edcfdd5912c074bb2871f368b878848ad792fef972e272` |
| 41 | `candidates/tc_reg_geo_girder_count_alignment.log` | 996 | `31f56844a09f765e32ebe7f11064630b5d078f8d2a3e3ac70881abb00145c23f` |
| 42 | `candidates/tc_reg_geo_girder_count_alignment_a_baseline.log` | 996 | `585890dad9accf0d1c9bbf3a0e2ae65eae4691251e4379c4053d7008b6401cb5` |
| 43 | `candidates/tc_reg_geo_girder_count_alignment_b_correct.log` | 883 | `96f4542969c0a2bad61fbec921b9a04ae7f2598b436bf70ec02d2b21cadf0e15` |
| 44 | `candidates/tc_reg_geo_girder_count_alignment_c_naive.log` | 996 | `31f56844a09f765e32ebe7f11064630b5d078f8d2a3e3ac70881abb00145c23f` |
| 45 | `candidates/tc_reg_geo_slab_section_properties.log` | 1491 | `60b3d421b0817b348a602348c852bee769b173066292b77bfaf6ec3772ee2a60` |
| 46 | `candidates/tc_reg_geo_slab_section_properties_a_baseline.log` | 1491 | `60b3d421b0817b348a602348c852bee769b173066292b77bfaf6ec3772ee2a60` |
| 47 | `candidates/tc_reg_mat_density_consistency.log` | 1078 | `82336e97b90d7c6f896cc532b842c251671c110fd2453d7e23808072dc626c34` |
| 48 | `candidates/tc_reg_mat_density_consistency_a_baseline.log` | 1078 | `158766c0bb85301e7c9d31f899b4ab9acd1044e9611a30810a899eefdc3d580a` |
| 49 | `candidates/tc_reg_mat_density_consistency_b_correct.log` | 1008 | `924b244a19eae298b99424f7570a5d39de068bac98a4bf218d939ab0214516cb` |
| 50 | `candidates/tc_reg_mat_density_consistency_c_naive.log` | 1078 | `82336e97b90d7c6f896cc532b842c251671c110fd2453d7e23808072dc626c34` |
| 51 | `candidates/tc_reg_rpt_exec_summary_status.log` | 3014 | `28453fe8e49b9f50cb4afddfd9d5b43110abcf97900da29d616ca9a101027583` |
| 52 | `candidates/tc_reg_rpt_exec_summary_status_a_baseline.log` | 3312 | `20afc32a5e1d474ffe9dcd6565dc1dc1e2c9a69321bb57bf4484a1f43f82fe15` |
| 53 | `candidates/tc_reg_rpt_exec_summary_status_b_correct.log` | 1210 | `fcfad16988b3d40322073a2db6711b41f52d41e6607391b8d79d4f38ad00ef80` |
| 54 | `candidates/tc_reg_rpt_exec_summary_status_c_naive.log` | 3014 | `28453fe8e49b9f50cb4afddfd9d5b43110abcf97900da29d616ca9a101027583` |

---

## 5. Historical Preservation Manifest (`preservation/`)

| # | Relative Path | Size (Bytes) | SHA-256 Digest |
|:---:|:---|:---:|:---|
| 1 | `preservation/PHASE_2_6_2_7_RECOVERY_REPORT.md` | 5473 | `850d49efe3308bae78035b635f1a1e95b32fbbffac0544721afdc5d03fc68073` |
| 2 | `preservation/evidence_recovery_manifest.json` | 6776 | `8621684ae805f2f8832e6aeb8dd8b6c0a59510e2e90977cce121f8590dd9f091` |
| 3 | `preservation/manifest_preservation.json` | 110222 | `fb028e348ea74ad026bce653eba043fef20ffabadf637e90507b905437beb43d` |
| 4 | `preservation/overwritten_versions/phase_2_6_tc_reg_a02_uls_combination_sum.log.overwritten` | 2486 | `0fecf5570bb56d70be4a4cdd397fe12da5d53f8725937e23b1b613ae31d12eef` |
| 5 | `preservation/overwritten_versions/phase_2_6_tc_reg_b01_section_property_sync.log.overwritten` | 2140 | `7fe4da64dfeae5b0bb4420aa735931bd54d93a8cabc8a87f75a0f8e37db64897` |
| 6 | `preservation/overwritten_versions/phase_2_6_tc_reg_c01_sectional_stress_range.log.overwritten` | 2363 | `83de7855dccf7a9d37764d7bc98cc5e6962e88fa2d89636c6b688d5acb4ff650` |
| 7 | `preservation/overwritten_versions/phase_2_6_tc_reg_eq_load_conservation.log.overwritten` | 3917 | `40092b80eabf0e5b19eb241534dcb458c50ffdae07d4043af2df3ea87d43c32b` |
| 8 | `preservation/overwritten_versions/phase_2_6_tc_reg_fs_clean_working_tree.log.overwritten` | 1685 | `c966fe8ec07aa4974d50d8e3dd6a60c55373210b0ae19cb4c261b0d2abe66824` |
| 9 | `preservation/overwritten_versions/phase_2_6_tc_reg_rpt_exec_summary_status.log.overwritten` | 2114 | `d7ca1f685f7c5b1fb293bbffb1207dc9b13bd17dc703d1fdbc6729d4fceaf35a` |
| 10 | `preservation/overwritten_versions/phase_2_7_tc_reg_eq_load_conservation.log.overwritten` | 3917 | `8476f0535f5810f732d1e60a66cbe0860eefc7a326053c61fcb675f405e3d3a6` |
