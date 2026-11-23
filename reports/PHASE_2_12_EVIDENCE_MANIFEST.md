# Phase 2.12 Evidence Manifest & Cryptographic Verification

**Phase:** Phase 2.12 — Final Harness Security and Evidence Governance Remediation  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`  
**Timestamp (UTC):** 2026-11-17T14:45:00Z  
**Trust Store:** `~/.osdagbridge_trust` (`C:\Users\Subodh\.osdagbridge_trust`)  

---

## 1. Cryptographic Run Seals (HMAC-SHA256 Authenticated)

| Subdirectory | Runner ID | Run UUID | Timestamp (UTC) | Files | Bytes | Manifest SHA-256 | HMAC-SHA256 Signature | Status |
|:---|:---|:---|:---|:---:|:---:|:---|:---|:---:|
| `evidence/phase_2_12/baseline` | `baseline_runner` | `efb61d9c-2986-4ecd-90cf-62fbd278f6a4` | `2026-11-17T14:37:16.250668+00:00` | 19 | 71437 | `47241d0ff85a5707...` | `f14497a0daf33438...` | **VALID** |
| `evidence/phase_2_12/sensitivity` | `sensitivity_runner` | `09dca119-7acd-450d-8b6b-11c63cf9b5a8` | `2026-11-17T14:44:26.939226+00:00` | 19 | 104166 | `111669b39db09c3b...` | `9dd1276cd4c0906b...` | **VALID** |
| `evidence/phase_2_12/candidates` | `candidates_runner` | `c97ab96f-dccc-47f6-b4c9-b2fa7a973b45` | `2026-11-17T14:44:27.024377+00:00` | 54 | 115289 | `75cf5cad23096262...` | `ff51d6aa61c8c6ee...` | **VALID** |

---

## 2. Directory File Manifests

### 2.1 Subdirectory: `baseline` (19 files)

| Relative Path | Size (Bytes) | SHA-256 Hash |
|:---|:---:|:---|
| `baseline_exit_code.txt` | 3 | `13bf7b3039c63bf5a50491fa3cfd8eb4e699d1ba1436315aef9cbe5711530354` |
| `console_error.txt` | 10673 | `6df59e10ce4fbf1d5c11ba680d222e6ebcb43cd9615bf6715431e2e2dbb759d8` |
| `console_output.txt` | 12511 | `bde3ab22e882b9debc4af5afedef915b5f91a9f4674717c71dab83102c090ed3` |
| `phase_2_12_baseline_summary.json` | 15408 | `da523e77a727e3eaad286cd9bf5e3908e4408f0170f6fb6cab6695d0ad005edd` |
| `tc_reg_a01_factor_scaling.log` | 1079 | `ab3921b72cc467d4953b31ade067884ab1808516197eb6c22a3034d89ca36f5f` |
| `tc_reg_a02_uls_combination_sum.log` | 3115 | `a3cc5d16ad3fcf80fc606dbcfc99a4baef6f8d9e8d7d4394542a69fad1a92941` |
| `tc_reg_b01_section_property_sync.log` | 3806 | `353fb6e1066bbabde7a2f37a8386c3f9b7634a725cb1faed41ca502699268cbe` |
| `tc_reg_c01_sectional_stress_range.log` | 2400 | `d50d4f04455776d527a26f50e039f4d76afd1e1b7d4dc6ea9c99557d373686a8` |
| `tc_reg_c02_fatigue_vehicle_analysis.log` | 1715 | `9d24c8bfa2a2c84ca665d736a8b8da911aa8041d2f6a2ea219b30b9229afae96` |
| `tc_reg_cad_export_vs_screenshot.log` | 963 | `41267d99caf8db34ec3960ec3281e23da21c031d469cd0378db66fa6f53175c9` |
| `tc_reg_cap_stiffener_buckling.log` | 1336 | `65e5796f1c2c48f0d6375c7f9a2750984df49714e899598ec28c52068bf4c4e5` |
| `tc_reg_d01_wind_speed_propagation.log` | 1317 | `27e359031f059d840b61a316fdda69f714c1123e70a8505beca7fe4422c91a1c` |
| `tc_reg_d02_temperature_propagation.log` | 1394 | `0dab988e86186700b49d0f6f30671de5909c44f0311ad26bdd5f65dfa2ec505f` |
| `tc_reg_eq_load_conservation.log` | 6232 | `a05826899fe7363b015d8c83742f8ecad7d52cb9b8fce0dc771e4464a3d1c1b5` |
| `tc_reg_fs_clean_working_tree.log` | 2445 | `79099f3b27a6d03ac5ab149b4e51c25f97a0d0abc94bf2b92d611c2087c63ec1` |
| `tc_reg_geo_girder_count_alignment.log` | 996 | `e4ff97e6c54a7f3da6d2dc65ab852457e42f60808e5f1832fb922a88f6b67b06` |
| `tc_reg_geo_slab_section_properties.log` | 1491 | `b192d331292c5adbe52a5c15df7263c15e15ccac4181566f32c30b371cafc34b` |
| `tc_reg_mat_density_consistency.log` | 1078 | `71ca47478ee844c3d9a00c67514e27fa1e48164cc43e62faa6588ca4c5eb30f3` |
| `tc_reg_rpt_exec_summary_status.log` | 3475 | `e34072baa3ddbf6851cbd3eb67c9f9f693a903600757b396d6914796341f3f3b` |

### 2.2 Subdirectory: `sensitivity` (19 files)

| Relative Path | Size (Bytes) | SHA-256 Hash |
|:---|:---:|:---|
| `console_error.txt` | 30435 | `688addba5ec92c90e43db10a14a947005b5d2e0c0f1838a0c351bdc2b05a5fbe` |
| `console_output.txt` | 14096 | `78653761c03352a27c5ad3db774dadfb27828de576586cc10c8fd25ab5918d33` |
| `phase_2_12_sensitivity_matrix_summary.json` | 31109 | `a5fbc6ff1321f09f012d9a0486bfe74929d16d564516045ab9030d58f149b34f` |
| `sensitivity_exit_code.txt` | 3 | `13bf7b3039c63bf5a50491fa3cfd8eb4e699d1ba1436315aef9cbe5711530354` |
| `tc_reg_a01_factor_scaling_sensitivity.json` | 1357 | `d201313972d7bbcad4f194daf3ddb66873afcb63528640190630307ed9bcdf10` |
| `tc_reg_a02_uls_combination_sum_sensitivity.json` | 2224 | `aeca73e30c3a795c9ffb54ac841d50598e61303f4bff9a7656daa9ae73c0ecc3` |
| `tc_reg_b01_section_property_sync_sensitivity.json` | 1724 | `5daea5b443c25f2867c03deda7e4e26f98d2ddff68fe63ac70620f2486120219` |
| `tc_reg_c01_sectional_stress_range_sensitivity.json` | 1719 | `28f5aa721e271c52c028e1e24dec872e55edcae3a26c8d17e4c7ce2f935d2c65` |
| `tc_reg_c02_fatigue_vehicle_analysis_sensitivity.json` | 1348 | `049e7e2b7ea964b306312ea71dfb34213501e3fa01109ffedbe2e5cccd1d0e21` |
| `tc_reg_cad_export_vs_screenshot_sensitivity.json` | 1310 | `d7ea2974a1b80abb8f97084088d9f7f69dbabf7dcbf8e01e671b030a0027370b` |
| `tc_reg_cap_stiffener_buckling_sensitivity.json` | 1570 | `09f03cc517310f4af4ca08982264d3feee0ada835838a96dd4516215108bdf15` |
| `tc_reg_d01_wind_speed_propagation_sensitivity.json` | 1540 | `79de694586f9a5582a2618f699cb7fe674e14466fc5ee34a571aef8a792b8783` |
| `tc_reg_d02_temperature_propagation_sensitivity.json` | 1274 | `c2654fde10e6a704e1ef98eaf34dd84763398c6f56d657bc22c604300a4f3e0f` |
| `tc_reg_eq_load_conservation_sensitivity.json` | 2766 | `ddc3beda3c7b28a183049f87d842d123ce808f323fa7278b4695a3949b17b9df` |
| `tc_reg_fs_clean_working_tree_sensitivity.json` | 1689 | `c92ced857c31d61dd1774552caf5aa490030286782a5dbf938f1a4b93f1f3bf2` |
| `tc_reg_geo_girder_count_alignment_sensitivity.json` | 1440 | `bf8d1a9336d7fbaf6c8708afb11a6cbbb663118c17bbeb3822acc520a52dcbc5` |
| `tc_reg_geo_slab_section_properties_sensitivity.json` | 1365 | `962c9c7b3a17a0c008f473ceff4d8993bf4459acfc3d464533bfc83b3296f2ce` |
| `tc_reg_mat_density_consistency_sensitivity.json` | 1449 | `3c6ea9511f4f6186ce45fad7225d5928f1795b930bba5391a6a5a23b4193c974` |
| `tc_reg_rpt_exec_summary_status_sensitivity.json` | 5748 | `f01556a3db13ea686c7cbc9088efebf6cf93970e6adb05a5f6b26db1fec2b172` |

### 2.3 Subdirectory: `candidates` (54 files)

| Relative Path | Size (Bytes) | SHA-256 Hash |
|:---|:---:|:---|
| `tc_reg_a01_factor_scaling.log` | 1079 | `e1eb21af18183b3b56bf4ed3231a53333fe1c8c0edd2c3c02ab66cce2280b0c6` |
| `tc_reg_a01_factor_scaling_a_baseline.log` | 1079 | `ddaed209caae276f537e7049974c438240906aeeea9001ffcee58f0d9d22013b` |
| `tc_reg_a01_factor_scaling_b_correct.log` | 1057 | `e02d8fb056a8819488370c63263a1bb6ddf4936a453f4abeff88e822db4b672f` |
| `tc_reg_a01_factor_scaling_c_naive.log` | 1079 | `e1eb21af18183b3b56bf4ed3231a53333fe1c8c0edd2c3c02ab66cce2280b0c6` |
| `tc_reg_a02_uls_combination_sum.log` | 3117 | `2bb716b0dbb6ce78fc1adac8da173c47f2ed817a9d7047e368870c246ec4487b` |
| `tc_reg_a02_uls_combination_sum_a_baseline.log` | 3115 | `ce2a91b1ac97af1aa2b3001b957adea419810f2de0738def6af3a8b3b6b39ac3` |
| `tc_reg_a02_uls_combination_sum_b_correct.log` | 2649 | `fb9a774d60bff18ab39d6645359730d05a5b4e30cb130f5d1832616c0d97169d` |
| `tc_reg_a02_uls_combination_sum_c_naive.log` | 3117 | `2bb716b0dbb6ce78fc1adac8da173c47f2ed817a9d7047e368870c246ec4487b` |
| `tc_reg_b01_section_property_sync.log` | 3806 | `3fb9949b1063a56ff3e48458e82b13546a08d2c8da269b9439edb7c2d0835c91` |
| `tc_reg_b01_section_property_sync_a_baseline.log` | 3806 | `e3af73dfbdf2d4a31dcb767e15a34125823fbaabd99bef0bcc509037b25268ea` |
| `tc_reg_b01_section_property_sync_b_correct.log` | 3578 | `aa7a34307ba46b1dac4e2d0eedf38a4d4937e701ec8da1c569d95e50086ec7f1` |
| `tc_reg_b01_section_property_sync_c_naive.log` | 3806 | `3fb9949b1063a56ff3e48458e82b13546a08d2c8da269b9439edb7c2d0835c91` |
| `tc_reg_c01_sectional_stress_range.log` | 2390 | `499d5ddefd7da3aa491e1d943a7ac81666fba83847f3a4cfdf1c280716c302e1` |
| `tc_reg_c01_sectional_stress_range_a_baseline.log` | 2400 | `79136b6adf2ffa0878947081f24460da18b470cec3b9e741845136751da03b3d` |
| `tc_reg_c01_sectional_stress_range_b_correct.log` | 2376 | `38d442ae6b5a22b4055e2cf3f0260185587b9e0c68e4cecc659f1645e807fc38` |
| `tc_reg_c01_sectional_stress_range_c_naive.log` | 2390 | `499d5ddefd7da3aa491e1d943a7ac81666fba83847f3a4cfdf1c280716c302e1` |
| `tc_reg_c02_fatigue_vehicle_analysis.log` | 1715 | `06fa2e65ae177a73f917e80465f5f3e2f49b8560e4e3d42c4244097d71daf60e` |
| `tc_reg_c02_fatigue_vehicle_analysis_a_baseline.log` | 1715 | `06fa2e65ae177a73f917e80465f5f3e2f49b8560e4e3d42c4244097d71daf60e` |
| `tc_reg_cad_export_vs_screenshot.log` | 942 | `afe7d918cd1234e4244c4b78101c540972df8dc06c8b2e56395065753ac4ed76` |
| `tc_reg_cad_export_vs_screenshot_a_baseline.log` | 963 | `ae3ea1135bf056f72ab7b0f2b3611fed201c577f1c18f723d3e2070c22a26087` |
| `tc_reg_cad_export_vs_screenshot_b_correct.log` | 963 | `971a333cd62f85fbc1e03675f6f4788c2cf1569916a4c4e92ae87020942a0c41` |
| `tc_reg_cad_export_vs_screenshot_c_naive.log` | 942 | `afe7d918cd1234e4244c4b78101c540972df8dc06c8b2e56395065753ac4ed76` |
| `tc_reg_cap_stiffener_buckling.log` | 1328 | `5abad9ee4b784af19945131d55025efcdb8311ff8deae8fe7bc880c0dd768f82` |
| `tc_reg_cap_stiffener_buckling_a_baseline.log` | 1336 | `8b38137abc4e99d14e6666d97f23c641b461652273cf96f463128684aba9a4a6` |
| `tc_reg_cap_stiffener_buckling_b_correct.log` | 1226 | `973661d116235ab688ac395a79db440137b7802d73c3db4564f852bb96d54770` |
| `tc_reg_cap_stiffener_buckling_c_naive.log` | 1328 | `5abad9ee4b784af19945131d55025efcdb8311ff8deae8fe7bc880c0dd768f82` |
| `tc_reg_d01_wind_speed_propagation.log` | 1317 | `ebebacfd1b373f355fb45f87393b8d7c2e1a4e79c63defb807a52472c6bace7a` |
| `tc_reg_d01_wind_speed_propagation_a_baseline.log` | 1317 | `4ff99d767cc2f0f1f3853eafbc5f524df64fcb06a1bd95213929d49576c23197` |
| `tc_reg_d01_wind_speed_propagation_b_correct.log` | 1188 | `f00b18a8e863365e8cc1dcdbcb8669847ee7d22d6a43d791201446b552967c0d` |
| `tc_reg_d01_wind_speed_propagation_c_naive.log` | 1317 | `ebebacfd1b373f355fb45f87393b8d7c2e1a4e79c63defb807a52472c6bace7a` |
| `tc_reg_d02_temperature_propagation.log` | 1394 | `92da3b12828011f19ffcb32c1302dc77416e72f420071f0da76ab29fcd1d9e39` |
| `tc_reg_d02_temperature_propagation_a_baseline.log` | 1394 | `92da3b12828011f19ffcb32c1302dc77416e72f420071f0da76ab29fcd1d9e39` |
| `tc_reg_eq_load_conservation.log` | 6048 | `5eb209bc5f9f5b90265d5699dcc22c61ef1735f97f8673d24d121a1239549573` |
| `tc_reg_eq_load_conservation_a_baseline.log` | 6232 | `ff99a52c92a82b4159f71059f2ff3006a1494583f9008b33586bd592edfc0837` |
| `tc_reg_eq_load_conservation_b_correct.log` | 5473 | `01a121be33eff2632bcce224c46b18c77e8fea474d50b7e2583ca232116a37e9` |
| `tc_reg_eq_load_conservation_c_naive.log` | 6048 | `5eb209bc5f9f5b90265d5699dcc22c61ef1735f97f8673d24d121a1239549573` |
| `tc_reg_fs_clean_working_tree.log` | 1905 | `5548e6afee0663e108fe16dc276c2308ce2b44f3c582e3547c780d134ac3c40f` |
| `tc_reg_fs_clean_working_tree_a_baseline.log` | 2445 | `0e1ac42a31c422fc6617e8c76d6b922dc16465d5d3828d0622699166bd804d2a` |
| `tc_reg_fs_clean_working_tree_b_correct.log` | 2026 | `4d7c2d72ca1ce04d0eb0f39cae8ab63cb136d945877d8301340c3bf6d6c89c5c` |
| `tc_reg_fs_clean_working_tree_c_naive.log` | 1905 | `5548e6afee0663e108fe16dc276c2308ce2b44f3c582e3547c780d134ac3c40f` |
| `tc_reg_geo_girder_count_alignment.log` | 996 | `309aaa6e9f21be0de3a5f52479e353cd83f8b3cb296ed32fac173da8e4a13343` |
| `tc_reg_geo_girder_count_alignment_a_baseline.log` | 996 | `20fabebeb6263ce5159527d3a5d40e407b85f3b5a0ddd27926a0877911812c9e` |
| `tc_reg_geo_girder_count_alignment_b_correct.log` | 883 | `1ed6c1c503fd514e88834f3ceca0e732ce399ad31076bdb9ecfb74ff8f15b40c` |
| `tc_reg_geo_girder_count_alignment_c_naive.log` | 996 | `309aaa6e9f21be0de3a5f52479e353cd83f8b3cb296ed32fac173da8e4a13343` |
| `tc_reg_geo_slab_section_properties.log` | 1491 | `3f89cad8c0b99b6f50869d305e6392933a18391f8b78b54e19348552a78e7d31` |
| `tc_reg_geo_slab_section_properties_a_baseline.log` | 1491 | `3f89cad8c0b99b6f50869d305e6392933a18391f8b78b54e19348552a78e7d31` |
| `tc_reg_mat_density_consistency.log` | 1078 | `648541759044a10d1aa4c53d3da6d62a76ccd1c2378783dcf22944d0eac4838f` |
| `tc_reg_mat_density_consistency_a_baseline.log` | 1078 | `31b0d5caf9363d78be436531b5a8d1400b202599883f51a681581cfc0a37542e` |
| `tc_reg_mat_density_consistency_b_correct.log` | 1008 | `958f64c819f98a235892942f22a2620331a7f40f4d2a1cc1de0c566ab6ad4adf` |
| `tc_reg_mat_density_consistency_c_naive.log` | 1078 | `648541759044a10d1aa4c53d3da6d62a76ccd1c2378783dcf22944d0eac4838f` |
| `tc_reg_rpt_exec_summary_status.log` | 3099 | `5fca048954de8dcdf4ff7c38ce7334f9c3cfd21f63b3a599d245e503dc9a0d7b` |
| `tc_reg_rpt_exec_summary_status_a_baseline.log` | 3475 | `e3e7646f78337c030c2b20027eda9e2d69a768c6131bc5b74acab73540c5a5ab` |
| `tc_reg_rpt_exec_summary_status_b_correct.log` | 1210 | `997189ccf7fed9e87b37bf761a528cff2688e51bf2ae383cf8317fed1fbac593` |
| `tc_reg_rpt_exec_summary_status_c_naive.log` | 3099 | `5fca048954de8dcdf4ff7c38ce7334f9c3cfd21f63b3a599d245e503dc9a0d7b` |

