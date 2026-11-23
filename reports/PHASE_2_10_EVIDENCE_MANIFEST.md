# PHASE 2.10 — Complete Cryptographic Evidence Manifest

**Date:** 2026-11-17  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`, 100% clean)  
**Controlling Document:** `reports/PHASE_2_9_FINAL_INDEPENDENT_GATE_AUDIT.md`  
**Evidence Directory Root:** `testing\evidence\phase_2_10\`  
**Total Artifacts Cataloged:** **96**  

---

## 1. Evidence Overview & Integrity Guarantees

All artifacts cataloged below were produced under strict fail-closed write-once governance enforced by `testing/test_cases/baseline_regression/evidence_guard.py`.
Every file SHA-256 hash was computed directly from disk bytes at the completion of official Phase 2.10 baseline and sensitivity executions.

| Subdirectory | Purpose | Artifact Count | Subdirectory Status |
|:---|:---|:---:|:---:|
| `baseline/` | Official 15-test baseline regression logs, summary JSON, console output, and exit code | 19 | COMPLETE |
| `sensitivity/` | 15 individual sensitivity matrix evaluations, summary JSON, console output, and exit code | 18 | COMPLETE |
| `candidates/` | Multi-condition execution logs (_a_baseline, _b_correct, _c_naive) | 54 | COMPLETE |
| `preservation/` | Bit-exact restored Phase 2.8 candidate logs, preserved overwritten versions, and recovery report | 5 | COMPLETE |
| **Total** | **Comprehensive Phase 2.10 Verification Suite** | **96** | **100% CRYPTOGRAPHICALLY SECURED** |

---

## Baseline Evidence Manifest (`baseline/`)

| # | Relative Path | Size (Bytes) | SHA-256 Digest |
|:---:|:---|:---:|:---|
| 1 | `baseline/baseline_exit_code.txt` | 3 | `13bf7b3039c63bf5a50491fa3cfd8eb4e699d1ba1436315aef9cbe5711530354` |
| 2 | `baseline/console_output.txt` | 24250 | `2d55e6178dd40da835f46503d8b32783f5460848da4bec3f74639bb19ceee92c` |
| 3 | `baseline/phase_2_10_baseline_summary.json` | 15399 | `387fad04d967831d077151953df5f22e678358a3705789a2e5151ea32f9d14f9` |
| 4 | `baseline/post_run_evidence_manifest.json` | 2804 | `cd8844bdde36b8f04f2c1a5605ef8bd3671f3c66863f46445857a7114045ba11` |
| 5 | `baseline/tc_reg_a01_factor_scaling.log` | 1079 | `1cdc0da82ee8fc637963cb81221d4aa8e23a4faed56c5a5101b822bae0311416` |
| 6 | `baseline/tc_reg_a02_uls_combination_sum.log` | 3116 | `8ca9176eb0840073a4d970fb5eb9c3f72c92cdaa40b4a5acea0c77a7a9687857` |
| 7 | `baseline/tc_reg_b01_section_property_sync.log` | 3729 | `e48707fb8822e8b72f1f2556ad720b0a6b4e5176c18d46d9ef51c3409d567b23` |
| 8 | `baseline/tc_reg_c01_sectional_stress_range.log` | 2345 | `97b0db4449a33b7eb55d201baa33360c6b626d9211f0362a86d4697b6ae3e778` |
| 9 | `baseline/tc_reg_c02_fatigue_vehicle_analysis.log` | 1715 | `0f6b018209d75323f65675ff11835ec496e9542a3a6971b6654bb2ac53b39590` |
| 10 | `baseline/tc_reg_cad_export_vs_screenshot.log` | 963 | `6a6291bb760f1bbbabfdcf62be0f14f65cd9c54d977dae9c3087b8050597ebce` |
| 11 | `baseline/tc_reg_cap_stiffener_buckling.log` | 1336 | `857c19faad93a6bcbdaec4df7ed809526f1b81ba47e8017306d693f6952cbd85` |
| 12 | `baseline/tc_reg_d01_wind_speed_propagation.log` | 1317 | `6823ef241b3a3b086205f1bb82eb6a4b926a511306fc99e44920428cf8fcbb6a` |
| 13 | `baseline/tc_reg_d02_temperature_propagation.log` | 1394 | `29de2b83990e581df32f169038f74243d7cf50a4ab49378ab43b4ba330ae9b73` |
| 14 | `baseline/tc_reg_eq_load_conservation.log` | 6232 | `ff88e5b33fcb218868af437601ede3ef4a7ceecb152e6e6e47c966cef9639bec` |
| 15 | `baseline/tc_reg_fs_clean_working_tree.log` | 2445 | `b8c4f9abdc51222ac2a4d445dec4ecf456f29c4f5f63f9496411377eb070d50e` |
| 16 | `baseline/tc_reg_geo_girder_count_alignment.log` | 996 | `74cb8b4ef134ad2d64469d91d2c6dd25dd0eea35a1e0762a6f2e8a94c5f4ea0f` |
| 17 | `baseline/tc_reg_geo_slab_section_properties.log` | 1491 | `2a928f840f2be726a1137b8db68432ae62a36cd489c2f79aca5aec06599e73e6` |
| 18 | `baseline/tc_reg_mat_density_consistency.log` | 1078 | `5230d0ba84a29299705b11ff960b4547e8d86f8e0209d314dc6f4c0e9a3b84ea` |
| 19 | `baseline/tc_reg_rpt_exec_summary_status.log` | 3476 | `b50fae2212c74f5857aec23d6bb88dfb9e3f9af3ce942ae40bd87b04726d0fe8` |

---

## Sensitivity Matrix Manifest (`sensitivity/`)

| # | Relative Path | Size (Bytes) | SHA-256 Digest |
|:---:|:---|:---:|:---|
| 1 | `sensitivity/console_output.txt` | 47064 | `cfd7043b1535e4149f63ed35d06ba4ef421c8fc723e0b802e251d5ee1f5c3028` |
| 2 | `sensitivity/phase_2_10_sensitivity_matrix_summary.json` | 31075 | `5742f128da174f594a9ec590d4e0ba79bddffd96c8e5a355abf9a4fddd92218a` |
| 3 | `sensitivity/sensitivity_exit_code.txt` | 3 | `13bf7b3039c63bf5a50491fa3cfd8eb4e699d1ba1436315aef9cbe5711530354` |
| 4 | `sensitivity/tc_reg_a01_factor_scaling_sensitivity.json` | 1357 | `bed23cf292f4ceaf1d4b1949001fd8c9a40e653795808a268829f1f835aac356` |
| 5 | `sensitivity/tc_reg_a02_uls_combination_sum_sensitivity.json` | 2223 | `d4f0673e1520e1fbf678425519fafedb1e0c38af524a20f699d67e570e196065` |
| 6 | `sensitivity/tc_reg_b01_section_property_sync_sensitivity.json` | 1706 | `3448a9cfce7a6f58e5c7447d869ed3c6442541b4d33e8462cf4d0291d65e457b` |
| 7 | `sensitivity/tc_reg_c01_sectional_stress_range_sensitivity.json` | 1704 | `93cf93d6106f410381811faaee79d3f3f9b69089ec541e002bf8efcfda43e6fd` |
| 8 | `sensitivity/tc_reg_c02_fatigue_vehicle_analysis_sensitivity.json` | 1346 | `2cf8cca1483815bde4125c3c0fd8c889b4e6021c75bf4e6cbfb166045a32e412` |
| 9 | `sensitivity/tc_reg_cad_export_vs_screenshot_sensitivity.json` | 1310 | `e037349a20e7250ed45fbdb85a8a41fde7496e688a2f04212908fc69845313c3` |
| 10 | `sensitivity/tc_reg_cap_stiffener_buckling_sensitivity.json` | 1571 | `7d9b237effa9902935b4de944c1b401ad016be4f351c656ba50d8edf386c16e6` |
| 11 | `sensitivity/tc_reg_d01_wind_speed_propagation_sensitivity.json` | 1540 | `0e06bc4669115aea1da3d34e9a9d2842bdfe632f459ac77b014405d02ee70be3` |
| 12 | `sensitivity/tc_reg_d02_temperature_propagation_sensitivity.json` | 1272 | `ef5a34920f630145545c7b7ccce3db4c802581cee0a74ce8cf0116ac7cc95929` |
| 13 | `sensitivity/tc_reg_eq_load_conservation_sensitivity.json` | 2766 | `0858abca218c870d995fef7d4c2389d5a0a86dbac9cf3e9c54514327166a65bc` |
| 14 | `sensitivity/tc_reg_fs_clean_working_tree_sensitivity.json` | 1691 | `cc5add2a61ff0a9beb5884283f893b2665c815bebdb9ef59221942dc1f28b733` |
| 15 | `sensitivity/tc_reg_geo_girder_count_alignment_sensitivity.json` | 1440 | `3c35d5287883973697763d51045a778bae2588bd6021856741e82e0c4dc04cd5` |
| 16 | `sensitivity/tc_reg_geo_slab_section_properties_sensitivity.json` | 1365 | `8aa8043cb0f0dd6ad86b7ccbf51cdd1bc777a2d995a07fddd51fda5716e7f64f` |
| 17 | `sensitivity/tc_reg_mat_density_consistency_sensitivity.json` | 1449 | `f19d3ebe4c821ebd2d101c5c797bf681787effac89899b1839467f09c30d2a3a` |
| 18 | `sensitivity/tc_reg_rpt_exec_summary_status_sensitivity.json` | 5748 | `4d88e976995b8d847e05704cfe8081da7c08e29bd757b8d6a47144dfea350502` |

---

## Candidates Condition Logs Manifest (`candidates/`)

| # | Relative Path | Size (Bytes) | SHA-256 Digest |
|:---:|:---|:---:|:---|
| 1 | `candidates/tc_reg_a01_factor_scaling.log` | 1079 | `c5d8e76f489e3d74016e31dcb855558654e8d67c136352f97d90561639ad87f2` |
| 2 | `candidates/tc_reg_a01_factor_scaling_a_baseline.log` | 1079 | `cba91638b237cca5eb515f0b60323ab36b99d3387a605e87ce42e10767bdb803` |
| 3 | `candidates/tc_reg_a01_factor_scaling_b_correct.log` | 1057 | `07967d40765aae56ee4c947a3ed6a284d7d5f83b717a68b5ddf63e9a1586bd5b` |
| 4 | `candidates/tc_reg_a01_factor_scaling_c_naive.log` | 1079 | `c5d8e76f489e3d74016e31dcb855558654e8d67c136352f97d90561639ad87f2` |
| 5 | `candidates/tc_reg_a02_uls_combination_sum.log` | 3117 | `888072f33c105441ba30ca28c523fe1e23ab3cb770f5d1c5731b9f72196d42a8` |
| 6 | `candidates/tc_reg_a02_uls_combination_sum_a_baseline.log` | 3115 | `d26f31fa1111b8e4fc67fc8408a238266c968c7f9bcea823617d12115e6113e1` |
| 7 | `candidates/tc_reg_a02_uls_combination_sum_b_correct.log` | 2649 | `591bc36bf3836630d86dd82eb5c85401aa9db460891907e5d525cc3645b4afcb` |
| 8 | `candidates/tc_reg_a02_uls_combination_sum_c_naive.log` | 3117 | `888072f33c105441ba30ca28c523fe1e23ab3cb770f5d1c5731b9f72196d42a8` |
| 9 | `candidates/tc_reg_b01_section_property_sync.log` | 3729 | `290c9d2274584a3f3c90a2d7539c424d10afd6f91f6b0800d18f792d1e77c081` |
| 10 | `candidates/tc_reg_b01_section_property_sync_a_baseline.log` | 3729 | `0ab50dbff75d378cfef37d83bf8a4891c793914e8b2fdd02fde1d1ebb4a3883f` |
| 11 | `candidates/tc_reg_b01_section_property_sync_b_correct.log` | 3510 | `3b38b89ca7bc9ed96ce5a935763ff7ed0ce662f2f69569a14df90152663f1dde` |
| 12 | `candidates/tc_reg_b01_section_property_sync_c_naive.log` | 3729 | `290c9d2274584a3f3c90a2d7539c424d10afd6f91f6b0800d18f792d1e77c081` |
| 13 | `candidates/tc_reg_c01_sectional_stress_range.log` | 2338 | `5097cd8b3b8a411232abe692cb6bd8461af64f7d47bc9f47a384699610dfe2fe` |
| 14 | `candidates/tc_reg_c01_sectional_stress_range_a_baseline.log` | 2345 | `cbd833a161c5c692beb01e54595aea7e0b21cbca3690f2f08e0da8e67ab738c2` |
| 15 | `candidates/tc_reg_c01_sectional_stress_range_b_correct.log` | 2308 | `6be2bd94fd6ebfe13aeab45081a3298d88529bd851708fba79663b464dbad6d9` |
| 16 | `candidates/tc_reg_c01_sectional_stress_range_c_naive.log` | 2338 | `5097cd8b3b8a411232abe692cb6bd8461af64f7d47bc9f47a384699610dfe2fe` |
| 17 | `candidates/tc_reg_c02_fatigue_vehicle_analysis.log` | 1715 | `7aad45e6fe10d577aba8c919b1d4b19236577a65eada3a44310691eee6ed6e2a` |
| 18 | `candidates/tc_reg_c02_fatigue_vehicle_analysis_a_baseline.log` | 1715 | `7aad45e6fe10d577aba8c919b1d4b19236577a65eada3a44310691eee6ed6e2a` |
| 19 | `candidates/tc_reg_cad_export_vs_screenshot.log` | 942 | `2d5d1bba1eb897b321f3e93c8d032f068d548b6860d937a2c5175ad2850adb78` |
| 20 | `candidates/tc_reg_cad_export_vs_screenshot_a_baseline.log` | 963 | `06083e01bd69950644d07a97de674437f5f399be6b63509a31792157fb2a1cfc` |
| 21 | `candidates/tc_reg_cad_export_vs_screenshot_b_correct.log` | 963 | `f08737dad79caf20b541f317e1ff20bf3f0e44fc362a2d41a140513b7e6316b4` |
| 22 | `candidates/tc_reg_cad_export_vs_screenshot_c_naive.log` | 942 | `2d5d1bba1eb897b321f3e93c8d032f068d548b6860d937a2c5175ad2850adb78` |
| 23 | `candidates/tc_reg_cap_stiffener_buckling.log` | 1328 | `32bb05873e45f336c2e65cc71d820bd9a1bb628167311e5a9e5e2e7753b749a5` |
| 24 | `candidates/tc_reg_cap_stiffener_buckling_a_baseline.log` | 1336 | `448c262f4661de35cd48b6a79de420b7808122b5f20eb30d1a6f192cc3f1cf21` |
| 25 | `candidates/tc_reg_cap_stiffener_buckling_b_correct.log` | 1226 | `327edfda54668614beadb0c103aa42d51288b42e6e650b8450fb6ff0804032bc` |
| 26 | `candidates/tc_reg_cap_stiffener_buckling_c_naive.log` | 1328 | `32bb05873e45f336c2e65cc71d820bd9a1bb628167311e5a9e5e2e7753b749a5` |
| 27 | `candidates/tc_reg_d01_wind_speed_propagation.log` | 1317 | `a4c9d22617da9dc5bde913021e5af9acd67c9b5d64b39b02743728640d6dd198` |
| 28 | `candidates/tc_reg_d01_wind_speed_propagation_a_baseline.log` | 1317 | `1c86ffaf8dd5d701a343a8540e6d70319d79abbdb4a9771182e5e760128fea37` |
| 29 | `candidates/tc_reg_d01_wind_speed_propagation_b_correct.log` | 1188 | `81b07b8c969b609cfe4f0d25684c2d4ec46d377773e31c1a29b9755da332aec8` |
| 30 | `candidates/tc_reg_d01_wind_speed_propagation_c_naive.log` | 1317 | `a4c9d22617da9dc5bde913021e5af9acd67c9b5d64b39b02743728640d6dd198` |
| 31 | `candidates/tc_reg_d02_temperature_propagation.log` | 1394 | `1749757e3a2918875a73d7de36f4e65974d21b218edcb226407be35ff5a1b221` |
| 32 | `candidates/tc_reg_d02_temperature_propagation_a_baseline.log` | 1394 | `1749757e3a2918875a73d7de36f4e65974d21b218edcb226407be35ff5a1b221` |
| 33 | `candidates/tc_reg_eq_load_conservation.log` | 6048 | `4b4bf4d4cddb16ab9e0f21402ef0d836f901be27e7d5ae1c5bc3c38c148c5238` |
| 34 | `candidates/tc_reg_eq_load_conservation_a_baseline.log` | 6232 | `416ac47c3d122e99d846ab3d804e0800269d697eea5c949c8b8715ad5f0e5e75` |
| 35 | `candidates/tc_reg_eq_load_conservation_b_correct.log` | 5473 | `fd69b7a74025820e2a0f2683b275412c88e952f17bb7f050a55ebaebf2e4a125` |
| 36 | `candidates/tc_reg_eq_load_conservation_c_naive.log` | 6048 | `4b4bf4d4cddb16ab9e0f21402ef0d836f901be27e7d5ae1c5bc3c38c148c5238` |
| 37 | `candidates/tc_reg_fs_clean_working_tree.log` | 1906 | `a0b5c1637a3c76ac2f83e39c694db6ab84aadfcf183c2226dd1a151877029de1` |
| 38 | `candidates/tc_reg_fs_clean_working_tree_a_baseline.log` | 2445 | `a83b9a8c4d087c44622babec33772979b6dfc6bfa2ebb6cdb12066eb4fd8cdf2` |
| 39 | `candidates/tc_reg_fs_clean_working_tree_b_correct.log` | 2027 | `2c0bd6aa54bfd898f653f89765554a33563ad5cea1be188631b91ed5083b960a` |
| 40 | `candidates/tc_reg_fs_clean_working_tree_c_naive.log` | 1906 | `a0b5c1637a3c76ac2f83e39c694db6ab84aadfcf183c2226dd1a151877029de1` |
| 41 | `candidates/tc_reg_geo_girder_count_alignment.log` | 996 | `bdccaa7c6c6e0981c8646f09aab565544dbe681f6cb12fb08f723c23b6431840` |
| 42 | `candidates/tc_reg_geo_girder_count_alignment_a_baseline.log` | 996 | `9df70dabcc9408ea32e6b4bbb4f21a2345b8fb7713dd91a2270347449d2d4bcf` |
| 43 | `candidates/tc_reg_geo_girder_count_alignment_b_correct.log` | 883 | `fdd7208c20e557fcb5f3672aab2a8a0fc4eb35d2a7690b7f161f6163804b497a` |
| 44 | `candidates/tc_reg_geo_girder_count_alignment_c_naive.log` | 996 | `bdccaa7c6c6e0981c8646f09aab565544dbe681f6cb12fb08f723c23b6431840` |
| 45 | `candidates/tc_reg_geo_slab_section_properties.log` | 1491 | `f13dff78bdb1165107c10cb253e454932bdf5780628e4778e417faac84f2cc83` |
| 46 | `candidates/tc_reg_geo_slab_section_properties_a_baseline.log` | 1491 | `f13dff78bdb1165107c10cb253e454932bdf5780628e4778e417faac84f2cc83` |
| 47 | `candidates/tc_reg_mat_density_consistency.log` | 1078 | `3366737290faea3eacbca99780033061b132ff0a794b884f5663b9f8a5e5fc5e` |
| 48 | `candidates/tc_reg_mat_density_consistency_a_baseline.log` | 1078 | `36c555705e1f6638f6019315f4a9029ddf678ed4004d0a04f7076062eded992e` |
| 49 | `candidates/tc_reg_mat_density_consistency_b_correct.log` | 1008 | `83b683ee953abcf7253d6badf62651444197a59545cd347296f83fa218c50f62` |
| 50 | `candidates/tc_reg_mat_density_consistency_c_naive.log` | 1078 | `3366737290faea3eacbca99780033061b132ff0a794b884f5663b9f8a5e5fc5e` |
| 51 | `candidates/tc_reg_rpt_exec_summary_status.log` | 3099 | `79d02f060d8d90aef68304e0d92ee167c315a97e500f4ad48a807f506061c402` |
| 52 | `candidates/tc_reg_rpt_exec_summary_status_a_baseline.log` | 3475 | `b89be0f9679ee1dbe5ab8bcb2ee61b7e6911a999893926d9bdd1168c15363ba1` |
| 53 | `candidates/tc_reg_rpt_exec_summary_status_b_correct.log` | 1210 | `5314a48c56f6df99628c9da5051c25724bc3d14fe94c96115303114456afdf17` |
| 54 | `candidates/tc_reg_rpt_exec_summary_status_c_naive.log` | 3099 | `79d02f060d8d90aef68304e0d92ee167c315a97e500f4ad48a807f506061c402` |

---

## Preservation & Restored Log Manifest (`preservation/`)

| # | Relative Path | Size (Bytes) | SHA-256 Digest |
|:---:|:---|:---:|:---|
| 1 | `preservation/PHASE_2_8_RECOVERY_REPORT.md` | 3790 | `55bc8ba9a7fc7bd259dd53c3510ffcc2ba2691e7e493d176c276191d709b3271` |
| 2 | `preservation/overwritten_phase_2_8_versions/tc_reg_a02_uls_combination_sum.log` | 2565 | `a6004dd4e20c29afdeab985b11d99b92ce292b5de12f9a2617ba41b867290ddc` |
| 3 | `preservation/overwritten_phase_2_8_versions/tc_reg_eq_load_conservation.log` | 5679 | `9ea32ce3ef54c5443e1da3db59bb8c754107e9d85f6e9a3706e81583db91fc72` |
| 4 | `preservation/overwritten_phase_2_8_versions/tc_reg_fs_clean_working_tree.log` | 1905 | `5fba8d56ee982decb5c6ea036e5b057fef5d45c5c70670ec3313c4c73b9dfd86` |
| 5 | `preservation/overwritten_phase_2_8_versions/tc_reg_rpt_exec_summary_status.log` | 3014 | `2e147cec33425bdb9af443ab579d23ce1f8d0c60dbe48dbdca5225346f2d7ca6` |

---
