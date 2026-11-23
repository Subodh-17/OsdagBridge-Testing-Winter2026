# PHASE 2.11 — Complete Cryptographic Evidence Manifest

**Date:** 2026-11-17  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`, 100% clean)  
**Controlling Document:** `reports/PHASE_2_10_FINAL_INDEPENDENT_GATE_AUDIT.md`  
**Evidence Directory Root:** `testing\evidence\phase_2_11\`  
**Total Artifacts Cataloged:** **96**  

---

## 1. Evidence Overview & Integrity Guarantees

All artifacts cataloged below were produced under strict fail-closed write-once governance enforced by `testing/test_cases/baseline_regression/evidence_guard.py`.
Every file SHA-256 hash was computed directly from disk bytes at the completion of official Phase 2.11 baseline and sensitivity executions.
All runs are cryptographically sealed in `reports/PHASE_2_11_RUN_SEALS.json`.

| Subdirectory | Purpose | Artifact Count | Subdirectory Status |
|:---|:---|:---:|:---:|
| `baseline/` | Official 15-test baseline regression logs, summary JSON, and exit code | 18 | COMPLETE & SEALED |
| `sensitivity/` | 15 individual sensitivity matrix evaluations, summary JSON, and exit code | 18 | COMPLETE & SEALED |
| `candidates/` | Multi-condition execution logs (_a_baseline, _b_correct, _c_naive) | 55 | COMPLETE & SEALED |
| `preservation/` | Bit-exact restored Phase 2.9 candidate logs, preserved overwritten versions, and recovery report | 5 | COMPLETE & VERIFIED |
| **Total** | **Comprehensive Phase 2.11 Verification Suite** | **96** | **100% CRYPTOGRAPHICALLY SECURED** |

---

## Baseline Evidence Manifest (`baseline/`)

| # | Relative Path | Size (Bytes) | SHA-256 Digest |
|:---:|:---|:---:|:---|
| 1 | `baseline/baseline_exit_code.txt` | 3 | `13bf7b3039c63bf5a50491fa3cfd8eb4e699d1ba1436315aef9cbe5711530354` |
| 2 | `baseline/manifest_hashes.json` | 3275 | `88c6d197c7db5a7726d294f29cd0e7d7ecfbfcd90d00da07cea020e3e107ab14` |
| 3 | `baseline/phase_2_11_baseline_summary.json` | 15410 | `e15ff4651872ee0f3f693e998e62eebd8b09bee274d35f739f39121926e26860` |
| 4 | `baseline/tc_reg_a01_factor_scaling.log` | 1079 | `969f779986e123ce72cc33e3edb0488679314024d9e42420c6ea1da71806310d` |
| 5 | `baseline/tc_reg_a02_uls_combination_sum.log` | 3115 | `7d71914e3e4a0a02f8f79bfb62036dfae39879944cc544bdfba098528245f9c2` |
| 6 | `baseline/tc_reg_b01_section_property_sync.log` | 3806 | `e29e47238b2a3fa6943b2ded68ff7d26df8f7757884108c516400de854957cc2` |
| 7 | `baseline/tc_reg_c01_sectional_stress_range.log` | 2345 | `718c5c2ba779c49707fbaa5d27bb08d3edde21e558ee5265e0c5ec94e07209e7` |
| 8 | `baseline/tc_reg_c02_fatigue_vehicle_analysis.log` | 1715 | `e384167cd6dc962fc01346ddc75ffd23154db4c509426f47f891b0a4427603c2` |
| 9 | `baseline/tc_reg_cad_export_vs_screenshot.log` | 963 | `ea9b18f7562db7ab958c5b99688fd54835b610619cd84a4a7a9aec5eb06dd9e1` |
| 10 | `baseline/tc_reg_cap_stiffener_buckling.log` | 1336 | `7aac491581f96983c8ed6d36b8234bc2d9f388c149f65fccdb5526378fb87136` |
| 11 | `baseline/tc_reg_d01_wind_speed_propagation.log` | 1317 | `1532c77ec4d2831a82e309b0fb1bd4976e2a7e58af5e9e64eda54ad4faa48810` |
| 12 | `baseline/tc_reg_d02_temperature_propagation.log` | 1394 | `bd93bb7c1b4386d2e5b7df51ca4106aefb55f89322c30f9e6b795566d5d19df4` |
| 13 | `baseline/tc_reg_eq_load_conservation.log` | 6232 | `0196466fcedc75466126edef8eafdf0358fd87f851d9fefa3e8d64f21686f584` |
| 14 | `baseline/tc_reg_fs_clean_working_tree.log` | 2445 | `62403b4e17eb59e5e769597c5fb592247765183a1dc8321aa0199af4a5952238` |
| 15 | `baseline/tc_reg_geo_girder_count_alignment.log` | 996 | `71a16105bfbf904d52864eb8fc330a57a76355f5b7a5570ba6a17d5204bae0e3` |
| 16 | `baseline/tc_reg_geo_slab_section_properties.log` | 1491 | `499f8aabcf3538932aa434430853fed480c35a50de47e30804c7650453abf702` |
| 17 | `baseline/tc_reg_mat_density_consistency.log` | 1078 | `6bcd55acd3150d7f5696434c986d15ac3186d474934a39c0bfe91f28936d0f43` |
| 18 | `baseline/tc_reg_rpt_exec_summary_status.log` | 3475 | `4b125274f8e1624db27a155b510956491862ea9876887512f8bb27235d188f2a` |

---

## Sensitivity Matrix Manifest (`sensitivity/`)

| # | Relative Path | Size (Bytes) | SHA-256 Digest |
|:---:|:---|:---:|:---|
| 1 | `sensitivity/manifest_hashes.json` | 3477 | `494886219d43ebd7d0d3bec395d86bf88f1bb3e2d4f8ea27b5ce7eeb254a2ad7` |
| 2 | `sensitivity/phase_2_11_sensitivity_matrix_summary.json` | 31094 | `083be1903d72ff462a56af5421e82ebd892f5ffccca9a362ed8128f717dc9bae` |
| 3 | `sensitivity/sensitivity_exit_code.txt` | 3 | `13bf7b3039c63bf5a50491fa3cfd8eb4e699d1ba1436315aef9cbe5711530354` |
| 4 | `sensitivity/tc_reg_a01_factor_scaling_sensitivity.json` | 1355 | `cce2633b23d58b005b44e87557bedacb29fbf31b2ee8249d01172ebe1c58969b` |
| 5 | `sensitivity/tc_reg_a02_uls_combination_sum_sensitivity.json` | 2224 | `3d77c8e564acefcd5192c5f42e533e019fa62da8cba6fb78de95221baadd23b4` |
| 6 | `sensitivity/tc_reg_b01_section_property_sync_sensitivity.json` | 1724 | `f044f5694676af3fb11df00dc71b32170b30f02743f322f3ebcb4fce2233c460` |
| 7 | `sensitivity/tc_reg_c01_sectional_stress_range_sensitivity.json` | 1704 | `5272597663135221a90dcca11cb00885b80ec021adfe7f2ed812e84051c08192` |
| 8 | `sensitivity/tc_reg_c02_fatigue_vehicle_analysis_sensitivity.json` | 1348 | `e7b0a47f7ce51b8cf136de1998b626cd1874a1f99227c7ebdbaab8f539533d73` |
| 9 | `sensitivity/tc_reg_cad_export_vs_screenshot_sensitivity.json` | 1310 | `5661e7ce6d2cd2710a3b81fb4b55bd965d51e74985f05f9ede96b311ae6c36e4` |
| 10 | `sensitivity/tc_reg_cap_stiffener_buckling_sensitivity.json` | 1571 | `10813cdddfddc59614416683a2fec43c9cfa2202638a0d5aa2156dc6a4c6ee3e` |
| 11 | `sensitivity/tc_reg_d01_wind_speed_propagation_sensitivity.json` | 1540 | `106b71de23c73f3a9f933afcc56e5cee1b0e1bbf54fa13b1bd509ae85c0a8d2f` |
| 12 | `sensitivity/tc_reg_d02_temperature_propagation_sensitivity.json` | 1274 | `b47cb775d5f345a69f1bab9dd19ef2bb02b6260a0b5c2d336a758290de54085e` |
| 13 | `sensitivity/tc_reg_eq_load_conservation_sensitivity.json` | 2766 | `df8cc097f746575eb63656ffdc39591391eca7123f96f1678767cd41d8649263` |
| 14 | `sensitivity/tc_reg_fs_clean_working_tree_sensitivity.json` | 1689 | `13145889f8040ad8b6c41403b07aa12ec1599a70555bf96ed7062cf106ffb634` |
| 15 | `sensitivity/tc_reg_geo_girder_count_alignment_sensitivity.json` | 1440 | `df3e413199c96a2e885d69152005e31cb577315361839810f092df0acbf5fa3e` |
| 16 | `sensitivity/tc_reg_geo_slab_section_properties_sensitivity.json` | 1365 | `8aa8043cb0f0dd6ad86b7ccbf51cdd1bc777a2d995a07fddd51fda5716e7f64f` |
| 17 | `sensitivity/tc_reg_mat_density_consistency_sensitivity.json` | 1449 | `d56a5f9b3a15020824342fd46700554cf97f538fb4f6e2fae813b14956644bde` |
| 18 | `sensitivity/tc_reg_rpt_exec_summary_status_sensitivity.json` | 5748 | `729a897dc1a1b78abe092a616253561e77f92c43e1ebe92d0311012699133752` |

---

## Candidates Condition Logs Manifest (`candidates/`)

| # | Relative Path | Size (Bytes) | SHA-256 Digest |
|:---:|:---|:---:|:---|
| 1 | `candidates/manifest_hashes.json` | 10296 | `a60e85dfe3f55439addaf77115e2fc92b14fe1b593e1c6790334bdacd8af9914` |
| 2 | `candidates/tc_reg_a01_factor_scaling.log` | 1079 | `9dcb0287180d96fecd0fc75aafab488c5408c9b85db194e9f93561490d0e1ce7` |
| 3 | `candidates/tc_reg_a01_factor_scaling_a_baseline.log` | 1079 | `07013e567d9bfec52541b2eecb33700e0e53745ba704ce42499e3e357631cd7e` |
| 4 | `candidates/tc_reg_a01_factor_scaling_b_correct.log` | 1057 | `099d4a232c0ab531b89b7912cfacabb8c24947303ec5ea9903644e39536f23a6` |
| 5 | `candidates/tc_reg_a01_factor_scaling_c_naive.log` | 1079 | `9dcb0287180d96fecd0fc75aafab488c5408c9b85db194e9f93561490d0e1ce7` |
| 6 | `candidates/tc_reg_a02_uls_combination_sum.log` | 3117 | `0ae39fff6b5c7465f779d990b903bbde1a5638e77c5953a44ec244beee488688` |
| 7 | `candidates/tc_reg_a02_uls_combination_sum_a_baseline.log` | 3115 | `14bb0a59c6bb6cf14387755829356ebc80512fbea3697bfc617f6fcccbf7ae9f` |
| 8 | `candidates/tc_reg_a02_uls_combination_sum_b_correct.log` | 2649 | `66d8ef8577d6ebfc9f03009d5fe116e4892c6acbd5529dc6953b4d0d78e3c2c6` |
| 9 | `candidates/tc_reg_a02_uls_combination_sum_c_naive.log` | 3117 | `0ae39fff6b5c7465f779d990b903bbde1a5638e77c5953a44ec244beee488688` |
| 10 | `candidates/tc_reg_b01_section_property_sync.log` | 3806 | `9d4502163281ca50bdaf75f4cd846115e8d218755c11cf345a09b8860ce3f6ce` |
| 11 | `candidates/tc_reg_b01_section_property_sync_a_baseline.log` | 3806 | `f4560a7a4ef8eee706c912ef9e768402dde8ffb949c0db1a1ffe05ba0aa4d90d` |
| 12 | `candidates/tc_reg_b01_section_property_sync_b_correct.log` | 3578 | `a564d7e156e3980e6682b6165286b9d4c3683326765ff894227730345b5f7823` |
| 13 | `candidates/tc_reg_b01_section_property_sync_c_naive.log` | 3806 | `9d4502163281ca50bdaf75f4cd846115e8d218755c11cf345a09b8860ce3f6ce` |
| 14 | `candidates/tc_reg_c01_sectional_stress_range.log` | 2338 | `6ef28cd12cc8add8c77fe7d5a5a716833e24b6defc88e517d87d503a7dca7f2a` |
| 15 | `candidates/tc_reg_c01_sectional_stress_range_a_baseline.log` | 2345 | `8d554b075c390c76d7338a562140dc65232596f24f11e10f8cb85ce0a90032e0` |
| 16 | `candidates/tc_reg_c01_sectional_stress_range_b_correct.log` | 2308 | `cddc742383336130bb5110ba521d3cf302ca0e89f5e5fd64a64b44cc78da8ed0` |
| 17 | `candidates/tc_reg_c01_sectional_stress_range_c_naive.log` | 2338 | `6ef28cd12cc8add8c77fe7d5a5a716833e24b6defc88e517d87d503a7dca7f2a` |
| 18 | `candidates/tc_reg_c02_fatigue_vehicle_analysis.log` | 1715 | `79a6b0ed5b07cc43868171a0f2ead70a46287cf3a49bd50c875fa7946c598ffa` |
| 19 | `candidates/tc_reg_c02_fatigue_vehicle_analysis_a_baseline.log` | 1715 | `79a6b0ed5b07cc43868171a0f2ead70a46287cf3a49bd50c875fa7946c598ffa` |
| 20 | `candidates/tc_reg_cad_export_vs_screenshot.log` | 942 | `47ed7bd4f7e50e13f5b61e4c512819139fbf514eaab8e51ff402f3d1854dccfc` |
| 21 | `candidates/tc_reg_cad_export_vs_screenshot_a_baseline.log` | 963 | `c858471ef8e266af063b7aea5f33a03ae2f958129f78d11a1f10c4db1d5bb42f` |
| 22 | `candidates/tc_reg_cad_export_vs_screenshot_b_correct.log` | 963 | `b466928355269b5e0bdbb00475758db117addcd501a9a80d7b6bb164b75df472` |
| 23 | `candidates/tc_reg_cad_export_vs_screenshot_c_naive.log` | 942 | `47ed7bd4f7e50e13f5b61e4c512819139fbf514eaab8e51ff402f3d1854dccfc` |
| 24 | `candidates/tc_reg_cap_stiffener_buckling.log` | 1328 | `1c94e442d37d1506096674482077cd19930ec1d7b2aaf2f4dde724379d00fa3d` |
| 25 | `candidates/tc_reg_cap_stiffener_buckling_a_baseline.log` | 1336 | `41bc38c5bcc71f86baf53b2bc684a9d270be9dcba25e74595e179f99553de21e` |
| 26 | `candidates/tc_reg_cap_stiffener_buckling_b_correct.log` | 1226 | `0a118b80c9a0bbe2afacddd2a2f0e815491f04a6de820d63b2e90dfdb720defd` |
| 27 | `candidates/tc_reg_cap_stiffener_buckling_c_naive.log` | 1328 | `1c94e442d37d1506096674482077cd19930ec1d7b2aaf2f4dde724379d00fa3d` |
| 28 | `candidates/tc_reg_d01_wind_speed_propagation.log` | 1317 | `3556d52cf8aae49e303bf94c240463914418f97b3429d43dc45fbd989cca2870` |
| 29 | `candidates/tc_reg_d01_wind_speed_propagation_a_baseline.log` | 1317 | `ea364f4c2269caf5f7e08a097506860aa1758299759b65fb66b8e70ef221e2a4` |
| 30 | `candidates/tc_reg_d01_wind_speed_propagation_b_correct.log` | 1188 | `cb552a3254e495ed7b0a0bd61b1ecdc8bdb86bcde462b9001be9aa3e12ab0224` |
| 31 | `candidates/tc_reg_d01_wind_speed_propagation_c_naive.log` | 1317 | `3556d52cf8aae49e303bf94c240463914418f97b3429d43dc45fbd989cca2870` |
| 32 | `candidates/tc_reg_d02_temperature_propagation.log` | 1394 | `50be60b08f96a5f6393b4e91e184c7a120f71b4b0b985734193e337d754bba97` |
| 33 | `candidates/tc_reg_d02_temperature_propagation_a_baseline.log` | 1394 | `50be60b08f96a5f6393b4e91e184c7a120f71b4b0b985734193e337d754bba97` |
| 34 | `candidates/tc_reg_eq_load_conservation.log` | 6048 | `e557a2331bfba8a037ea244bd0c08c3a7a18ef9c8337b89af1208ddc9976bb51` |
| 35 | `candidates/tc_reg_eq_load_conservation_a_baseline.log` | 6232 | `1be96aaa613c650333cf8a48f5c2cf70c7beca7e3dca2c1e4bb02ef89a0d2e60` |
| 36 | `candidates/tc_reg_eq_load_conservation_b_correct.log` | 5473 | `c99eb0d12171bf25be57381d3e7fb8ae317f689ea59f30e0c513dcb40d1412e7` |
| 37 | `candidates/tc_reg_eq_load_conservation_c_naive.log` | 6048 | `e557a2331bfba8a037ea244bd0c08c3a7a18ef9c8337b89af1208ddc9976bb51` |
| 38 | `candidates/tc_reg_fs_clean_working_tree.log` | 1905 | `f80302f0a523981c6b2b5f5b0c28c73e8f5d5fb2b67d96c1dd3ae0d714773ded` |
| 39 | `candidates/tc_reg_fs_clean_working_tree_a_baseline.log` | 2445 | `82163e1f726eea7d92d6e82ba9716be018b5e8715ec99be5b5d40ebf64bc3649` |
| 40 | `candidates/tc_reg_fs_clean_working_tree_b_correct.log` | 2026 | `a6f3b05edc6d625de236c9792713cc0581b2eac6a1d331c2401eb9de511e954a` |
| 41 | `candidates/tc_reg_fs_clean_working_tree_c_naive.log` | 1905 | `f80302f0a523981c6b2b5f5b0c28c73e8f5d5fb2b67d96c1dd3ae0d714773ded` |
| 42 | `candidates/tc_reg_geo_girder_count_alignment.log` | 996 | `e24b65449a9ccf9eeabc1490157d3b296a121edb08c2c3d8706a821ee157a6a9` |
| 43 | `candidates/tc_reg_geo_girder_count_alignment_a_baseline.log` | 996 | `e033e09f90180e2373fcdc85f12dcc62ccf117abcbf2bf1f99fd45342b0067e9` |
| 44 | `candidates/tc_reg_geo_girder_count_alignment_b_correct.log` | 883 | `5b3c470437328a0bc0a21a9553b1b41d4db3dde704be675bbcea4479f003243b` |
| 45 | `candidates/tc_reg_geo_girder_count_alignment_c_naive.log` | 996 | `e24b65449a9ccf9eeabc1490157d3b296a121edb08c2c3d8706a821ee157a6a9` |
| 46 | `candidates/tc_reg_geo_slab_section_properties.log` | 1491 | `aed52ddf56001ff55d069a0c2eb2604e5d264f2ae1f1d3c49e92007797949922` |
| 47 | `candidates/tc_reg_geo_slab_section_properties_a_baseline.log` | 1491 | `aed52ddf56001ff55d069a0c2eb2604e5d264f2ae1f1d3c49e92007797949922` |
| 48 | `candidates/tc_reg_mat_density_consistency.log` | 1078 | `a9b98a1e489b23f94305ebe539fafae0133c0d6e4878da275ab9c18aab674065` |
| 49 | `candidates/tc_reg_mat_density_consistency_a_baseline.log` | 1078 | `34964a421c1b1c285d9a29151e0cacd4f07825c463ef2f5012d13a2d31c582c9` |
| 50 | `candidates/tc_reg_mat_density_consistency_b_correct.log` | 1008 | `786b34eb8f05f66550fde20a65d4df1d0b5d9dfefab078381025a82e476e7b96` |
| 51 | `candidates/tc_reg_mat_density_consistency_c_naive.log` | 1078 | `a9b98a1e489b23f94305ebe539fafae0133c0d6e4878da275ab9c18aab674065` |
| 52 | `candidates/tc_reg_rpt_exec_summary_status.log` | 3099 | `7762d0ef36e5bc0772a99ee4c23d70ee31f421039f07fd877a36402307202998` |
| 53 | `candidates/tc_reg_rpt_exec_summary_status_a_baseline.log` | 3475 | `f09353be763dd8cf2c94b270683ddd126bc29cfaa35c10e2fcac9ad41ea8f3ec` |
| 54 | `candidates/tc_reg_rpt_exec_summary_status_b_correct.log` | 1210 | `20a75b3d92b7b41c3d5bed2839a0171b3e1fe5377f8c0597e7809e913d2eb015` |
| 55 | `candidates/tc_reg_rpt_exec_summary_status_c_naive.log` | 3099 | `7762d0ef36e5bc0772a99ee4c23d70ee31f421039f07fd877a36402307202998` |

---

## Preservation & Incident Disclosure Manifest (`preservation/`)

| # | Relative Path | Size (Bytes) | SHA-256 Digest |
|:---:|:---|:---:|:---|
| 1 | `preservation/PHASE_2_9_RECOVERY_REPORT.md` | 4473 | `4c97a8dc3928e47b364eccde1cdebe9238da8942ee224337bd3556875fcc69ec` |
| 2 | `preservation/overwritten_phase_2_9_versions/tc_reg_b01_section_property_sync.log` | 3729 | `7403df5ae194d032d60bb6481bc109d3220614428a8e4fba3436fbaa5d2828d2` |
| 3 | `preservation/overwritten_phase_2_9_versions/tc_reg_c01_sectional_stress_range.log` | 2338 | `2ed1edad3c589e37938efbdf10b4b13b4a26613567c067c8f0e85cac21b43c16` |
| 4 | `preservation/overwritten_phase_2_9_versions/tc_reg_eq_load_conservation.log` | 6048 | `eae7b52676c8ebe6f4d1bfa2c6f0ff465db1aea504578e301520e27b94ef7a6d` |
| 5 | `preservation/overwritten_phase_2_9_versions/tc_reg_rpt_exec_summary_status.log` | 3100 | `d3e836ecf829969eb6b9573ae02186fd378ef4c2f12e4531b175aad9b4e53b26` |
