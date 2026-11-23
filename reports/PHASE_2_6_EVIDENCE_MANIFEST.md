# PHASE 2.6 EVIDENCE MANIFEST & INTEGRITY AUDIT

**Date:** 2026-11-16  
**Controlling Audit:** `reports/PHASE_2_5_FINAL_INDEPENDENT_GATE_AUDIT.md`  
**Application Repository:** `source/OsdagBridge`  
**Frozen Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (branch `dev`, working tree clean)  

---

## 1. Test Infrastructure & Core Artifact Hashes

| Component / File | Path | Size (Bytes) | SHA-256 Checksum |
|---|---|---|---|
| Baseline Regression Runner | `testing/test_cases/baseline_regression/run_all_baseline_tests.py` | 109,078 | `ef5a8151feead5a0b104bc8ec058a1f0c46e6147b2590df280f51f93a140dbf1` |
| Sensitivity Matrix Runner | `testing/test_cases/baseline_regression/run_sensitivity_matrix.py` | 48,898 | `d24db269e7079f0097d823c3e4693cff395c0e612266b219042d7ee997c3da04` |
| Input Configuration Fixture | `testing/evidence/phase_1d/input_configuration.json` | 44,653 | `31ae62dc08a0de7797aa4ca6451a178fd46cc66bba4c00f7414021336fb10191` |
| Output Dictionary Snapshot | `testing/evidence/phase_1d/output_dictionary_snapshot.json` | 3,333,439 | `429a3198fc93c157a5bd5ee13c74b95612c3410d35a7be1f246867167991a5ab` |
| Structural Database | `source/.../ResourceFiles/Intg_osdag.sqlite` | 270,336 | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` |
| Weather Location Database | `source/.../project_location/weather.sqlite` | 180,224 | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` |
| Complete Machine Manifest | `testing/evidence/phase_2_6/hashes/manifest_hashes.json` | 16,047 | `7f20225cb604186f37120c2ee0e0ecff2409f33ab06b46f103528d51c2ad9dc6` |

---

## 2. Environment Evidence (`environment/`)

| Relative Path | Size (Bytes) | SHA-256 Checksum |
|---|---|---|
| `environment/environment_fingerprint.json` | 1,142 | `5b8f09e71cb50c408cef1d839cfec518bec62204be1240faaba72e428729a815` |

---

## 3. Baseline Evidence (`baseline/`)

Total files: 19 (15 individual test logs, structured JSON summary, runner exit code, raw console transcript, shell exit code).

| Relative Path | Size (Bytes) | SHA-256 Checksum |
|---|---|---|
| `baseline/baseline_exit_code.txt` | 1 | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` |
| `baseline/console_output.txt` | 43,824 | `99c846cdda2225130f69f1574981742b7fee3f91b8ecc1084cb03f026d22d866` |
| `baseline/phase_2_6_baseline_summary.json` | 12,732 | `e2bd04069919b3ef826c0a766938fdb4ca9544d1b332f02707223aee41aae441` |
| `baseline/shell_exit_code.txt` | 1 | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` |
| `baseline/tc_reg_a01_factor_scaling.log` | 1,079 | `95c170d4d8108cffcd57bf4fbe57a8c4cf451202a12afb54420374d97a1ad376` |
| `baseline/tc_reg_a02_uls_combination_sum.log` | 2,001 | `b6e0c87f80ce2a1e30ba5fddfd3bac6b1ebc5a717f940b3da60cd873cbebbf9c` |
| `baseline/tc_reg_b01_section_property_sync.log` | 2,027 | `e30e0cd6e5d734591b230fb0b3bcb30b10aba771fa075fe3092ee3087992fc27` |
| `baseline/tc_reg_c01_sectional_stress_range.log` | 2,054 | `d33489c5e465381cf83e6976ff096a6c2b034c8ed16a1859612e75d0982447b5` |
| `baseline/tc_reg_c02_fatigue_vehicle_analysis.log` | 1,715 | `d3c240482fc82e97b1d5660993d972b181b98cddb7953076480b0f4a139691db` |
| `baseline/tc_reg_cad_export_vs_screenshot.log` | 963 | `df9435672210836bab3d1ee0d58deba6a67fa9aef1a8129411c857e59b5d253e` |
| `baseline/tc_reg_cap_stiffener_buckling.log` | 1,336 | `37a4ea16209115fd16115f3ef97264dead9de37e082e8dbcc87384831a3910b9` |
| `baseline/tc_reg_d01_wind_speed_propagation.log` | 1,317 | `76954c90849713373ae8a8d284a39906878ae7e4f855aed6ea827fd7d7587802` |
| `baseline/tc_reg_d02_temperature_propagation.log` | 1,394 | `84f10f4dae6257422712e1ade9b11a75710efeabaa1664baa3860b0a0ca30c41` |
| `baseline/tc_reg_eq_load_conservation.log` | 4,247 | `054876a7116ce1c00b2a128406038af25f3e1fe69d2f32f1d29d37952d1e4b1d` |
| `baseline/tc_reg_fs_clean_working_tree.log` | 2,028 | `cd1e28d7e63e02d5c9b3f2a3ec9cca12b9c13208405f30c3e0dac1634d49acf1` |
| `baseline/tc_reg_geo_girder_count_alignment.log` | 996 | `db777b360d042ac58eaf77e889ea8d8d6e2a836874f4ceca36119307e7389772` |
| `baseline/tc_reg_geo_slab_section_properties.log` | 1,491 | `79ac6290a782215a854ac767023856d7884674b3fd7c157a82fafad3a3c54502` |
| `baseline/tc_reg_mat_density_consistency.log` | 1,078 | `4bf5f0fe0f448f67b6dcf983b2698657b2f8d4aed1b27dd135b8b7cf56d34c02` |
| `baseline/tc_reg_rpt_exec_summary_status.log` | 2,438 | `6c4537d593d04fc574a11e457590a85b2d5382d405dd61e6ec41471a59c7ea00` |

---

## 4. Sensitivity Matrix Evidence (`sensitivity/`)

Total files: 19 (15 individual test logs, structured JSON matrix summary, runner exit code, raw console transcript, shell exit code).

| Relative Path | Size (Bytes) | SHA-256 Checksum |
|---|---|---|
| `sensitivity/console_output.txt` | 94,032 | `946e5e94ef34d2301fe9ae1157207173368cc0114e4fa2b47871031333690ed6` |
| `sensitivity/phase_2_6_sensitivity_matrix_summary.json` | 25,929 | `fbaf7f119ec749da76146def6c69442ac927789c6e12883f315af429a9f80d6c` |
| `sensitivity/sensitivity_exit_code.txt` | 3 | `13bf7b3039c63bf5a50491fa3cfd8eb4e699d1ba1436315aef9cbe5711530354` |
| `sensitivity/shell_exit_code.txt` | 1 | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` |
| `sensitivity/tc_reg_a01_factor_scaling_sensitivity.json` | 1,357 | `88a60d5b76c6964ce4910e7ecffb6afdb6aff109c9a78b71d4b8454fd7fa3e36` |
| `sensitivity/tc_reg_a02_uls_combination_sum_sensitivity.json` | 1,675 | `50497d74f6c7a7bb84e9391520dd4b3e7188fd9474b5025fd6c85105115173b8` |
| `sensitivity/tc_reg_b01_section_property_sync_sensitivity.json` | 1,650 | `4c6b90395218f8c8ddccede30d85b9f2deed3ce2ad77a1e2bc8fe3089593681e` |
| `sensitivity/tc_reg_c01_sectional_stress_range_sensitivity.json` | 1,641 | `acc54c8b32fc21d5b6473e53208d9df8aff82e2b5af30d317ddff2650fbf0485` |
| `sensitivity/tc_reg_c02_fatigue_vehicle_analysis_sensitivity.json` | 1,348 | `1678180c3959d773d414efbbda0b6579a0ee6a9db227990f4b43263073ddc839` |
| `sensitivity/tc_reg_cad_export_vs_screenshot_sensitivity.json` | 1,310 | `7d921af88120804149d8921f05e6d3cff976421f749ce209c0e42210ebbf0981` |
| `sensitivity/tc_reg_cap_stiffener_buckling_sensitivity.json` | 1,571 | `a352ec298ae7052c9067f7ad28116f7722a9af8e8c149df8dd8b8805805414cd` |
| `sensitivity/tc_reg_d01_wind_speed_propagation_sensitivity.json` | 1,540 | `1695b6f3507502892618d08937f767c1bc29b0fb23ba412fd97b21780e1ea766` |
| `sensitivity/tc_reg_d02_temperature_propagation_sensitivity.json` | 1,274 | `7d5d69dd4c59cfb1159f9adbe512e9e65c705f544fbbb684c83e6906df49b9b3` |
| `sensitivity/tc_reg_eq_load_conservation_sensitivity.json` | 2,323 | `fea1f57005924133fbf276435ef9d62ef672c70aeda69c6b8b9ef894b9750395` |
| `sensitivity/tc_reg_fs_clean_working_tree_sensitivity.json` | 1,626 | `f864c1b4444e300c3706fd6aace62e569c4e0894822d065efe8312577415e064` |
| `sensitivity/tc_reg_geo_girder_count_alignment_sensitivity.json` | 1,440 | `a06448c9b59893929e585e52641968d87cdbe587af8e32d8457f8065b1effa72` |
| `sensitivity/tc_reg_geo_slab_section_properties_sensitivity.json` | 1,365 | `0e7e3f8bf420b2c6708657aaa35e225320266f89439eea78ab39a9d3e1d34ea0` |
| `sensitivity/tc_reg_mat_density_consistency_sensitivity.json` | 1,450 | `ab3d44e0b1f629e42db15665807e3c63952c6748b44a944a0ca69692fd44358f` |
| `sensitivity/tc_reg_rpt_exec_summary_status_sensitivity.json` | 2,082 | `fad33dba2c91e77780c68584a8660d42cbee3178fa651a3cfe40eebc6a3450cd` |

---

## 5. Candidate Implementations Evidence (`candidates/`)

Total files: 54 (36 condition logs for actionable tests [conditions a, b, c], 3 condition logs for blocked tests [condition a], and 15 base logs).

| Relative Path | Size (Bytes) | SHA-256 Checksum |
|---|---|---|
| `candidates/tc_reg_a01_factor_scaling.log` | 1,079 | `472f27f6aac21c924496143726493c76fc20c2586afe43d25e78879917046b9f` |
| `candidates/tc_reg_a01_factor_scaling_a_baseline.log` | 1,079 | `d9372afe5c2664783d0c6693541a6291881492b2fca3f8952988b83d5b4fcc2f` |
| `candidates/tc_reg_a01_factor_scaling_b_correct.log` | 1,057 | `c60ddb541340ab65723ec6b3ec040bfe815f0f86b94d0b57d218b47a5c4229e4` |
| `candidates/tc_reg_a01_factor_scaling_c_naive.log` | 1,079 | `472f27f6aac21c924496143726493c76fc20c2586afe43d25e78879917046b9f` |
| `candidates/tc_reg_a02_uls_combination_sum.log` | 2,003 | `6b69e668424146c26f53eafaa87e4de1e5106848536fa4f02ad02094d12b07b6` |
| `candidates/tc_reg_a02_uls_combination_sum_a_baseline.log` | 2,001 | `7faf456b01d5188f2f7dde10658e68376da3a485ebaac43897f515228f137f4f` |
| `candidates/tc_reg_a02_uls_combination_sum_b_correct.log` | 1,824 | `59f27f4f931afc5e33c8895e103d2cb8d52f7a76be5f5e78bbc5a1a1d5d0fbdf` |
| `candidates/tc_reg_a02_uls_combination_sum_c_naive.log` | 2,003 | `6b69e668424146c26f53eafaa87e4de1e5106848536fa4f02ad02094d12b07b6` |
| `candidates/tc_reg_b01_section_property_sync.log` | 2,027 | `8fd719ce84f38f246693586785586d8078d02320ec4ed6a297df861154dd207e` |
| `candidates/tc_reg_b01_section_property_sync_a_baseline.log` | 2,027 | `b8bdc07a28b205caaeeeb35f8e4a0336c6d96ff314f87d581bfb32e65f870250` |
| `candidates/tc_reg_b01_section_property_sync_b_correct.log` | 1,856 | `5349a5737f888794e6e8b4553c412ab3cb3b75da2d0c481ca4a08f2e35111de7` |
| `candidates/tc_reg_b01_section_property_sync_c_naive.log` | 2,027 | `8fd719ce84f38f246693586785586d8078d02320ec4ed6a297df861154dd207e` |
| `candidates/tc_reg_c01_sectional_stress_range.log` | 2,046 | `ff2e7b532061c04332d681cc931328ee89769d3715539583c06724cfe5655763` |
| `candidates/tc_reg_c01_sectional_stress_range_a_baseline.log` | 2,054 | `8e8d4ef58cebaf3514e60accba05437302c8649627d71a1a7b42bbd5f8a8b3cd` |
| `candidates/tc_reg_c01_sectional_stress_range_b_correct.log` | 1,954 | `2bee9e4dad6dc68b5882a4d4a33ff118ea4cd462dd483e61b3719dc7dd636de0` |
| `candidates/tc_reg_c01_sectional_stress_range_c_naive.log` | 2,046 | `ff2e7b532061c04332d681cc931328ee89769d3715539583c06724cfe5655763` |
| `candidates/tc_reg_c02_fatigue_vehicle_analysis.log` | 1,715 | `9a1ae1abc9c4e2dcec328cd633c982083df492e6adfcd0cd1f3d08dec8355828` |
| `candidates/tc_reg_c02_fatigue_vehicle_analysis_a_baseline.log` | 1,715 | `9a1ae1abc9c4e2dcec328cd633c982083df492e6adfcd0cd1f3d08dec8355828` |
| `candidates/tc_reg_cad_export_vs_screenshot.log` | 942 | `e3cea207eb74eb740da9c5f4048f0ee1dcff75d868919bc8425b936c3f6d46cd` |
| `candidates/tc_reg_cad_export_vs_screenshot_a_baseline.log` | 963 | `5f39e8ae4cffe55c202b0dde50a14bfed4c1d6a372685a7bc8cf8e5d60974cba` |
| `candidates/tc_reg_cad_export_vs_screenshot_b_correct.log` | 963 | `d7b18b7db59204e8223cdf8f1997623e06ad54f8b50add1e2ad93c7e273d79ed` |
| `candidates/tc_reg_cad_export_vs_screenshot_c_naive.log` | 942 | `e3cea207eb74eb740da9c5f4048f0ee1dcff75d868919bc8425b936c3f6d46cd` |
| `candidates/tc_reg_cap_stiffener_buckling.log` | 1,328 | `a2805e1d4d12d4d695d82f5c67203892c46c9ef685e83cdc24f3dfb2138cb0d6` |
| `candidates/tc_reg_cap_stiffener_buckling_a_baseline.log` | 1,336 | `f7b014781207f54c6d2102c63e92f59fa34c845845bffd42c3032b9e08fc7f67` |
| `candidates/tc_reg_cap_stiffener_buckling_b_correct.log` | 1,226 | `3450458e509185aa451dccb094c1391560c3ba21950f4a1897e7bbcf5523aa82` |
| `candidates/tc_reg_cap_stiffener_buckling_c_naive.log` | 1,328 | `a2805e1d4d12d4d695d82f5c67203892c46c9ef685e83cdc24f3dfb2138cb0d6` |
| `candidates/tc_reg_d01_wind_speed_propagation.log` | 1,317 | `e175676b4484856fc480fcc3c7bd1e952fb479aa05886e394d121a550a2cb4bd` |
| `candidates/tc_reg_d01_wind_speed_propagation_a_baseline.log` | 1,317 | `971f2bb0a75109d8cc0620e7fe77b52cf68f4bac64cb56dae1085186bb983580` |
| `candidates/tc_reg_d01_wind_speed_propagation_b_correct.log` | 1,188 | `e8e7edd22e7f1442913cdbf172f13c9801706e6ed66185dd237a98109938abda` |
| `candidates/tc_reg_d01_wind_speed_propagation_c_naive.log` | 1,317 | `e175676b4484856fc480fcc3c7bd1e952fb479aa05886e394d121a550a2cb4bd` |
| `candidates/tc_reg_d02_temperature_propagation.log` | 1,394 | `6eb2ee2a6f21e60c500db7bdba711a58f673cc5c08becb668a4096a14963d845` |
| `candidates/tc_reg_d02_temperature_propagation_a_baseline.log` | 1,394 | `6eb2ee2a6f21e60c500db7bdba711a58f673cc5c08becb668a4096a14963d845` |
| `candidates/tc_reg_eq_load_conservation.log` | 4,073 | `0d490c374931b3335aefdc1cf3396e10e027e197986879105b45bc1c8fdff54a` |
| `candidates/tc_reg_eq_load_conservation_a_baseline.log` | 4,247 | `1f03ac8e5573c4c99864e309aff62feccc5151313d46a6759a0f89f2130f9df2` |
| `candidates/tc_reg_eq_load_conservation_b_correct.log` | 3,740 | `e8c58fd69e5301cfece6b1c84518c5f96200f4bed5e09e4b4726d48faaae07e8` |
| `candidates/tc_reg_eq_load_conservation_c_naive.log` | 4,073 | `0d490c374931b3335aefdc1cf3396e10e027e197986879105b45bc1c8fdff54a` |
| `candidates/tc_reg_fs_clean_working_tree.log` | 1,651 | `ab361431ea2a3d87a434890cbd1884aec3425c485ef644e09bb14559e7103a8f` |
| `candidates/tc_reg_fs_clean_working_tree_a_baseline.log` | 2,028 | `3c25632d9fdff8f6efe73c286d2d531e25aaca29907e4ce5aea26e140cdddf56` |
| `candidates/tc_reg_fs_clean_working_tree_b_correct.log` | 1,752 | `55a1e4d1685fca9b42c0c430c6330773a8e50fb43a4184f63610a37faf3f799b` |
| `candidates/tc_reg_fs_clean_working_tree_c_naive.log` | 1,651 | `ab361431ea2a3d87a434890cbd1884aec3425c485ef644e09bb14559e7103a8f` |
| `candidates/tc_reg_geo_girder_count_alignment.log` | 996 | `65481cda982f4627aed891d73c7a1ecc1a455384e3ce5556d028863aaab5c5eb` |
| `candidates/tc_reg_geo_girder_count_alignment_a_baseline.log` | 996 | `1b1890934f36021f105aa7d98592f0c7f659d08f8e1902fb974ee6dff657fc16` |
| `candidates/tc_reg_geo_girder_count_alignment_b_correct.log` | 883 | `8eab154e6542546810fbed230a422d892d2ed55ad26e53774744e44288503601` |
| `candidates/tc_reg_geo_girder_count_alignment_c_naive.log` | 996 | `65481cda982f4627aed891d73c7a1ecc1a455384e3ce5556d028863aaab5c5eb` |
| `candidates/tc_reg_geo_slab_section_properties.log` | 1,491 | `c997f16fe11b464de3dd74754d7bcb63850f865badd563eafce0b917a014820d` |
| `candidates/tc_reg_geo_slab_section_properties_a_baseline.log` | 1,491 | `c997f16fe11b464de3dd74754d7bcb63850f865badd563eafce0b917a014820d` |
| `candidates/tc_reg_mat_density_consistency.log` | 1,078 | `96c3dab39d8e8f61a0bd689d213e2c62c21c21da153269a455bda81bb9a6322c` |
| `candidates/tc_reg_mat_density_consistency_a_baseline.log` | 1,078 | `ff1aaa7c538799ac5c019f14c63422e07bb6647c0ca5f6399dae1e47dd92cd56` |
| `candidates/tc_reg_mat_density_consistency_b_correct.log` | 1,008 | `a1c28ff93c092b874b98231c17062db276195afe06e7dab9684b5c139c7f570c` |
| `candidates/tc_reg_mat_density_consistency_c_naive.log` | 1,078 | `96c3dab39d8e8f61a0bd689d213e2c62c21c21da153269a455bda81bb9a6322c` |
| `candidates/tc_reg_rpt_exec_summary_status.log` | 2,415 | `89d3466d20aa00839f0d63b4aabbb1bbdbd52f5affbbc38ff0b7c2362d6d36ae` |
| `candidates/tc_reg_rpt_exec_summary_status_a_baseline.log` | 2,438 | `53b78e3720aef08208a6ceeddafc932c2162c6f0119cbe64cf2ea81baf5fbfc9` |
| `candidates/tc_reg_rpt_exec_summary_status_b_correct.log` | 1,991 | `86a918b07995cc36e34cab084b6fead3ef6ef571ea0cb10069e18b30c1e7cab3` |
| `candidates/tc_reg_rpt_exec_summary_status_c_naive.log` | 2,415 | `89d3466d20aa00839f0d63b4aabbb1bbdbd52f5affbbc38ff0b7c2362d6d36ae` |

---

## 6. Provenance & Cryptographic Integrity Guarantees

1. **Zero Manual Hash Construction:** Every SHA-256 checksum and byte count in this document was extracted programmatically and directly from disk bytes using Python `hashlib.sha256()`. No hashes are typed, truncated, or padded.
2. **Separation of Evidence Trees:** Phase 2.6 evidence is strictly isolated under `testing/evidence/phase_2_6/`. Prior phase evidence trees (`phase_1d` through `phase_2_5`) remain 100% byte-identical and untouched.
3. **Execution Sequencing:** The sensitivity matrix runner was executed first, writing condition logs into `candidates/` and matrix summary into `sensitivity/`. The baseline regression runner was executed subsequently into `baseline/`, guaranteeing that baseline logs and summaries are pristine, authentic records of frozen baseline behavior unaffected by candidate monkeypatching.
4. **Repository Invariance:** The application repository at `source/OsdagBridge` was strictly unmutated throughout all tests. Working tree status remains clean at commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` on branch `dev`.
5. **Historical Provenance Limitations:** The Phase 2.3 overwritten log anomaly remains documented as an unalterable historical limitation; no data recovery is fabricated.
