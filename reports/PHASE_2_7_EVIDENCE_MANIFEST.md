# PHASE 2.7 EVIDENCE MANIFEST & INTEGRITY AUDIT

**Date:** 2026-11-17  
**Controlling Audit:** 
eports/PHASE_2_6_FINAL_INDEPENDENT_GATE_AUDIT.md  
**Application Repository:** source/OsdagBridge  
**Frozen Baseline Commit:** d74f56dd7f22925fb8148cabf5740ed8d1e39ff3 (branch dev, working tree clean)  

---

## 1. Test Infrastructure & Core Artifact Hashes

| Component / File | Path | Size (Bytes) | SHA-256 Checksum |
|---|---|---|---|
| Baseline Regression Runner | testing/test_cases/baseline_regression/run_all_baseline_tests.py | 126,276 | 6af66095b53f21871c578a4a7fe9f4cafe1760571ebe613d58b9b692f2e7fb5f |
| Sensitivity Matrix Runner | testing/test_cases/baseline_regression/run_sensitivity_matrix.py | 49,354 | dc6632bc5a3c5ff3810c738dfd37fac5b2ad70f5cf3f12fc64a70bee5d6fc1a0 |
| Input Configuration Fixture | testing/evidence/phase_1d/input_configuration.json | 44,653 | 31ae62dc08a0de7797aa4ca6451a178fd46cc66bba4c00f7414021336fb10191 |
| Output Dictionary Snapshot | testing/evidence/phase_1d/output_dictionary_snapshot.json | 3,333,439 | 429a3198fc93c157a5bd5ee13c74b95612c3410d35a7be1f246867167991a5ab |
| Structural Database | source/OsdagBridge/src/osdagbridge/core/data/ResourceFiles/Intg_osdag.sqlite | 270,336 | 25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91 |
| Weather Location Database | source/OsdagBridge/src/osdagbridge/core/data/project_location/weather.sqlite | 180,224 | 1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98 |
| Complete Machine Manifest | testing/evidence/phase_2_7/hashes/manifest_hashes.json | 16,047 | d95036fb77bc9a1d4876636bdcbc3324f8ad8e0cf90e11bcdb88be35aa823180 |

---

## 2. Environment Evidence (environment/)

Total files: 1

| Relative Path | Size (Bytes) | SHA-256 Checksum |
|---|---|---|
| environment/environment_fingerprint.json | 1,142 | b3564aec4028666268cf001d2d0d908413ec89f8f0434081ce0b665372786aba |

---

## 3. Baseline Evidence (aseline/)

Total files: 19 (15 individual test logs, structured JSON summary, runner exit code, raw console transcript, shell exit code).

| Relative Path | Size (Bytes) | SHA-256 Checksum |
|---|---|---|
| baseline/baseline_exit_code.txt | 1 | 5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9 |
| baseline/console_output.txt | 21,930 | db1c5287881966ad2c042b726faacf38d11cd634a9ce1ebf21309b6e21e03896 |
| baseline/phase_2_7_baseline_summary.json | 13,091 | 27379466ebcc929313d24748676e0e19455c11ad03faa4a73fd6c76cdf719011 |
| baseline/shell_exit_code.txt | 3 | 13bf7b3039c63bf5a50491fa3cfd8eb4e699d1ba1436315aef9cbe5711530354 |
| baseline/tc_reg_a01_factor_scaling.log | 1,079 | ec659b911e069ea967e269b4d219350e8128979cc69759e24fae92e9416b3d25 |
| baseline/tc_reg_a02_uls_combination_sum.log | 2,484 | 78f8c1d253a1c19fa078399b7911f22f7986f67ac504ebb13b7f9fe82bd84d1f |
| baseline/tc_reg_b01_section_property_sync.log | 2,140 | 7226059f1a2dcc2b890e144eeac0e2d3875afb064ad86f0ae33d8401828e1d1a |
| baseline/tc_reg_c01_sectional_stress_range.log | 2,373 | f16b0dddd1153f56419848983f93031f7ab67ae48dcae9e0bb0dadc9407ba6ca |
| baseline/tc_reg_c02_fatigue_vehicle_analysis.log | 1,715 | 938ba30c0b90123d9170b4c7d0c252acd7f7baeea9916d7b81e95ef005fd7a03 |
| baseline/tc_reg_cad_export_vs_screenshot.log | 963 | 7eaf94439d4e77ad3b683e1000edfbcca28b3cdd4b8a89cc6132b4bfbc54ef7c |
| baseline/tc_reg_cap_stiffener_buckling.log | 1,336 | 3e569d69d1ae5f992651c296593ad60801c100c1d913f4ae6782abb4125ee434 |
| baseline/tc_reg_d01_wind_speed_propagation.log | 1,317 | a8ff74e578acb354e50d0fc432128de67d68df83a01bdb45a9776eb4c72101c8 |
| baseline/tc_reg_d02_temperature_propagation.log | 1,394 | 545f02737647d34f9a3e8ae3ba35bc03d0e60376c6d0f25e82aee934f2e6f9fa |
| baseline/tc_reg_eq_load_conservation.log | 4,359 | e41e647a89e94aba560b867d70a92e7f5b7c4138b609f2fcc73060e1fbe16556 |
| baseline/tc_reg_fs_clean_working_tree.log | 2,196 | 1db49c268df20f22a42cd890e75ecf121cfaf334802ee19b561dc44559851a91 |
| baseline/tc_reg_geo_girder_count_alignment.log | 996 | 60ecf60969a8ba7bb0a7913f0375092eca0816a3ad03f002bd56869e36920d87 |
| baseline/tc_reg_geo_slab_section_properties.log | 1,491 | 358099bdee8feeee9e71825083585bd1f0850d057d441203a1b3ced6319f99b5 |
| baseline/tc_reg_mat_density_consistency.log | 1,078 | 86887b4b153803f6eb79fca0801cf426a27bde69fa06fde099a6a5da5e2d3f7d |
| baseline/tc_reg_rpt_exec_summary_status.log | 2,205 | 71fa7287ba855ba5db34238cece62aab8bb575fd19eba79aaf290b72afb0c154 |

---

## 4. Candidate Validation Evidence (candidates/)

Total files: 54 (15 individual test logs, 15 condition _a_baseline logs, 12 condition _b_correct logs, 12 condition _c_naive logs).

| Relative Path | Size (Bytes) | SHA-256 Checksum |
|---|---|---|
| candidates/tc_reg_a01_factor_scaling.log | 1,079 | b51a3e098b53e50c8933d68410440acda11f91ec58ef06e7971c323badfe8205 |
| candidates/tc_reg_a01_factor_scaling_a_baseline.log | 1,079 | a5309b77d2fe748b1e745d209a0c5c6a9b9114a8344be58a265f8ea189757b03 |
| candidates/tc_reg_a01_factor_scaling_b_correct.log | 1,057 | 8f988e67cbc3cd4b8a50e6b3b3bae9546b4731afaa1e11cf37f4bcd3b58b9b51 |
| candidates/tc_reg_a01_factor_scaling_c_naive.log | 1,079 | b51a3e098b53e50c8933d68410440acda11f91ec58ef06e7971c323badfe8205 |
| candidates/tc_reg_a02_uls_combination_sum.log | 2,487 | 04c510ded74450dfc71ab9654d2e66215fec4239ca59a35d00e5ca22c62e0d7f |
| candidates/tc_reg_a02_uls_combination_sum_a_baseline.log | 2,485 | e8113f08dc731504db280f588bd63be042258f69fe65ed96ec5b8d6c7bc44472 |
| candidates/tc_reg_a02_uls_combination_sum_b_correct.log | 2,214 | 59d6426cb03558d368b3baff191ea3fd881d38b3243ecc96b887ad6e04f10e30 |
| candidates/tc_reg_a02_uls_combination_sum_c_naive.log | 2,487 | 04c510ded74450dfc71ab9654d2e66215fec4239ca59a35d00e5ca22c62e0d7f |
| candidates/tc_reg_b01_section_property_sync.log | 2,140 | d005dc9cb8cc4742aa7ad2c95281d003a8e939df80fdbabe7af30c627c9db698 |
| candidates/tc_reg_b01_section_property_sync_a_baseline.log | 2,140 | 9c8eb653effba2b9c8ee00897ba4701e3d4462d9f24fe806d1f96931148c2cc3 |
| candidates/tc_reg_b01_section_property_sync_b_correct.log | 2,040 | 5712c12506d6ffcae9090c1420b39336a15f6d444c9554acb49976219c9064e1 |
| candidates/tc_reg_b01_section_property_sync_c_naive.log | 2,140 | d005dc9cb8cc4742aa7ad2c95281d003a8e939df80fdbabe7af30c627c9db698 |
| candidates/tc_reg_c01_sectional_stress_range.log | 2,363 | 5068cd331ca9cce19f11a86728b76fe92681b9b8cbb1b68cfa6571a70262bcaf |
| candidates/tc_reg_c01_sectional_stress_range_a_baseline.log | 2,373 | 9dfd2daaaf6ca1720eddc8789d9efd6c80faf89f94591088cdf53a750c02c979 |
| candidates/tc_reg_c01_sectional_stress_range_b_correct.log | 2,324 | 95408027ff5bbdd204953035ea4fb134deb17dd4572950c363a836891b5bfe0f |
| candidates/tc_reg_c01_sectional_stress_range_c_naive.log | 2,363 | 5068cd331ca9cce19f11a86728b76fe92681b9b8cbb1b68cfa6571a70262bcaf |
| candidates/tc_reg_c02_fatigue_vehicle_analysis.log | 1,715 | c1ce54268783088914c10b57eec28be7c12629f9bd8dce645849f0157c118ccc |
| candidates/tc_reg_c02_fatigue_vehicle_analysis_a_baseline.log | 1,715 | c1ce54268783088914c10b57eec28be7c12629f9bd8dce645849f0157c118ccc |
| candidates/tc_reg_cad_export_vs_screenshot.log | 942 | 2d095afcd44a0573f1b2e96c5716a28fed208470e810741f55bc22a74b03b008 |
| candidates/tc_reg_cad_export_vs_screenshot_a_baseline.log | 963 | e03ce08675a8d644c11163fe0de05d861cba89979bd7739a27e37b1869cee80a |
| candidates/tc_reg_cad_export_vs_screenshot_b_correct.log | 963 | 6205f86b6107e3908720366e4ab1d629415d077f9c3849cc07d6bd6820aaf133 |
| candidates/tc_reg_cad_export_vs_screenshot_c_naive.log | 942 | 2d095afcd44a0573f1b2e96c5716a28fed208470e810741f55bc22a74b03b008 |
| candidates/tc_reg_cap_stiffener_buckling.log | 1,328 | 2523001244549766684fc568091a5bd2a3302084e49d17f30280578070113006 |
| candidates/tc_reg_cap_stiffener_buckling_a_baseline.log | 1,336 | f6f090d01f39718d06c631a2392b201f01720cc320793bb038b29b386cdee701 |
| candidates/tc_reg_cap_stiffener_buckling_b_correct.log | 1,226 | 5b3fa10c34bd13d20a20de821463c88faa46119eb13cbcdc47bbe306fd90f7f0 |
| candidates/tc_reg_cap_stiffener_buckling_c_naive.log | 1,328 | 2523001244549766684fc568091a5bd2a3302084e49d17f30280578070113006 |
| candidates/tc_reg_d01_wind_speed_propagation.log | 1,317 | 880378397d4ff1d3415e381ee0d03d61096aca386500be63e4f88bcb3c291283 |
| candidates/tc_reg_d01_wind_speed_propagation_a_baseline.log | 1,317 | 87b3e1d6f146cd3dcfecda685fd80002a5605656b28efc39b176e7fe0f8744cf |
| candidates/tc_reg_d01_wind_speed_propagation_b_correct.log | 1,188 | 61fa8c242323d2bd7df2f616943810cb3cad3b02a7abed9ec117e1ad11ce7699 |
| candidates/tc_reg_d01_wind_speed_propagation_c_naive.log | 1,317 | 880378397d4ff1d3415e381ee0d03d61096aca386500be63e4f88bcb3c291283 |
| candidates/tc_reg_d02_temperature_propagation.log | 1,394 | 91827ec907d7944bc202b2ca8d16cb2a1da8730f7963d055a97b7e90acc9db3b |
| candidates/tc_reg_d02_temperature_propagation_a_baseline.log | 1,394 | 91827ec907d7944bc202b2ca8d16cb2a1da8730f7963d055a97b7e90acc9db3b |
| candidates/tc_reg_eq_load_conservation.log | 4,168 | 9ee3fe4b89b8a90788a26b45c50cd7a0a17650cc3efc723c8b1d3df59632bf44 |
| candidates/tc_reg_eq_load_conservation_a_baseline.log | 4,359 | 0dd35688ca5e8d48f28938b8144aff438fd916268258e5146dc1e90edf3d6ac0 |
| candidates/tc_reg_eq_load_conservation_b_correct.log | 3,917 | 17b5b274ee5a2b68cf5105e6e183a05fb359b9fb26cea6004587c730c4ac44e0 |
| candidates/tc_reg_eq_load_conservation_c_naive.log | 4,168 | 9ee3fe4b89b8a90788a26b45c50cd7a0a17650cc3efc723c8b1d3df59632bf44 |
| candidates/tc_reg_fs_clean_working_tree.log | 1,778 | 0a22fb34f645dd2f4fb52dd13864179e904e406290d375388b4d4f27b716d56f |
| candidates/tc_reg_fs_clean_working_tree_a_baseline.log | 2,197 | e5b046c722b90f1932c602ccac65115055657c4f3d9727d5ca0669f7e68a8f29 |
| candidates/tc_reg_fs_clean_working_tree_b_correct.log | 1,879 | 13e44b9a64d4be3875366d4348fee820c638260eac70dc1a8ebe0cc3c320491e |
| candidates/tc_reg_fs_clean_working_tree_c_naive.log | 1,778 | 0a22fb34f645dd2f4fb52dd13864179e904e406290d375388b4d4f27b716d56f |
| candidates/tc_reg_geo_girder_count_alignment.log | 996 | aef05665cfdf8c77d204241acb1cf10c0fc01bfe58e9df1160c50f0e66c03c84 |
| candidates/tc_reg_geo_girder_count_alignment_a_baseline.log | 996 | beb3af9cd2c31973c41a10d4cae2217d4c6f254cac03208ef849835b26f2c22a |
| candidates/tc_reg_geo_girder_count_alignment_b_correct.log | 883 | 59b610ad2cdd65a770eaf13cf3792fdb30da8e98872586b4a02896d88b195dcb |
| candidates/tc_reg_geo_girder_count_alignment_c_naive.log | 996 | aef05665cfdf8c77d204241acb1cf10c0fc01bfe58e9df1160c50f0e66c03c84 |
| candidates/tc_reg_geo_slab_section_properties.log | 1,491 | 9e5f080a6b9cea53e99df7a26988f5701c04cf3bfbd124e9a0c815fc5a9809d8 |
| candidates/tc_reg_geo_slab_section_properties_a_baseline.log | 1,491 | 9e5f080a6b9cea53e99df7a26988f5701c04cf3bfbd124e9a0c815fc5a9809d8 |
| candidates/tc_reg_mat_density_consistency.log | 1,078 | af0343331680e9d43c1e2296f1c9a36bc8d8b7242013028967fcf8c9462191c0 |
| candidates/tc_reg_mat_density_consistency_a_baseline.log | 1,078 | 92d2c4d7f289ed9ffa1711809c5a7ba5fd39f7122740954c32738c90438cf4f0 |
| candidates/tc_reg_mat_density_consistency_b_correct.log | 1,008 | 077c136c798e2cd77ef459722ba9ded3cf9b8b631fe99486d3b9788273b2a2a6 |
| candidates/tc_reg_mat_density_consistency_c_naive.log | 1,078 | af0343331680e9d43c1e2296f1c9a36bc8d8b7242013028967fcf8c9462191c0 |
| candidates/tc_reg_rpt_exec_summary_status.log | 2,114 | f614945bda9597fb27e93c554fe8ad1387597a276229485ca039e8ca39f3b019 |
| candidates/tc_reg_rpt_exec_summary_status_a_baseline.log | 2,205 | 5be8e551410ac38190e118b0e37e87aad2a53ef85e85add82c07df9e6587fa61 |
| candidates/tc_reg_rpt_exec_summary_status_b_correct.log | 1,447 | 38d4ccd1d512965abaecc2d751013660f178986f7d6a88827397eba21e9edf85 |
| candidates/tc_reg_rpt_exec_summary_status_c_naive.log | 2,114 | f614945bda9597fb27e93c554fe8ad1387597a276229485ca039e8ca39f3b019 |

---

## 5. Sensitivity Matrix Evidence (sensitivity/)

Total files: 19 (15 individual test sensitivity JSON records, master sensitivity matrix summary, sensitivity exit code, raw console transcript, shell exit code).

| Relative Path | Size (Bytes) | SHA-256 Checksum |
|---|---|---|
| sensitivity/console_output.txt | 46,690 | c3b9507ba91d48998c43fc3e615dd0bfb08eb59229972c84a991f68fcccb1ee4 |
| sensitivity/phase_2_7_sensitivity_matrix_summary.json | 26,532 | b293ddd4bf9252b2ecd0ca487df337f74a38befff20f12df78927d3542a673a7 |
| sensitivity/sensitivity_exit_code.txt | 3 | 13bf7b3039c63bf5a50491fa3cfd8eb4e699d1ba1436315aef9cbe5711530354 |
| sensitivity/shell_exit_code.txt | 3 | 13bf7b3039c63bf5a50491fa3cfd8eb4e699d1ba1436315aef9cbe5711530354 |
| sensitivity/tc_reg_a01_factor_scaling_sensitivity.json | 1,357 | 3a5651e6e085fcebd79521b743d10ba36a0087d785ff53bb8ce62474ec903db6 |
| sensitivity/tc_reg_a02_uls_combination_sum_sensitivity.json | 1,853 | 2c0d9c63ee9399c74386aae2a6775c6b7e5375753a360e593784aa2af9120280 |
| sensitivity/tc_reg_b01_section_property_sync_sensitivity.json | 1,499 | 9f62e5e060789f61b13df7d09e32c05821f872a99f022c87849268105b11b164 |
| sensitivity/tc_reg_c01_sectional_stress_range_sensitivity.json | 1,692 | 6bde2d2e997ed4fe41660fd4dda84fcc318741023b15d0a1d7ae667d00ee94dd |
| sensitivity/tc_reg_c02_fatigue_vehicle_analysis_sensitivity.json | 1,348 | e7b0a47f7ce51b8cf136de1998b626cd1874a1f99227c7ebdbaab8f539533d73 |
| sensitivity/tc_reg_cad_export_vs_screenshot_sensitivity.json | 1,310 | 24f0a4ede85ab178cbff04e75f395c8a22b3344bf300d6c07d0baf9d80dbf557 |
| sensitivity/tc_reg_cap_stiffener_buckling_sensitivity.json | 1,570 | 82ae7ace345b5fac771aeb7dfb60884415acbcd2e4ea90de3da2ac90a09d340c |
| sensitivity/tc_reg_d01_wind_speed_propagation_sensitivity.json | 1,540 | 320af9beeba05713e5bd220e41edb6d248086cf1001f6a75b935b103d4c2167f |
| sensitivity/tc_reg_d02_temperature_propagation_sensitivity.json | 1,274 | b47cb775d5f345a69f1bab9dd19ef2bb02b6260a0b5c2d336a758290de54085e |
| sensitivity/tc_reg_eq_load_conservation_sensitivity.json | 2,009 | 4b6dfe4416f68805291ee43eed46ca35d806089d374274c998ff010cd043c0e3 |
| sensitivity/tc_reg_fs_clean_working_tree_sensitivity.json | 1,656 | 239783af45626e6d1b225ba658466ad5cb381ea1cfbeabe20afbfce927b4c808 |
| sensitivity/tc_reg_geo_girder_count_alignment_sensitivity.json | 1,440 | f453e9e3a13ef79deb3c90a826839562a98cdf3c3cbcfd11d69ae6ecaa160cad |
| sensitivity/tc_reg_geo_slab_section_properties_sensitivity.json | 1,365 | 8aa8043cb0f0dd6ad86b7ccbf51cdd1bc777a2d995a07fddd51fda5716e7f64f |
| sensitivity/tc_reg_mat_density_consistency_sensitivity.json | 1,449 | 740e3966dee4d21cf2a700fce4fda641450770b40c4bed784f3da192c1f44eef |
| sensitivity/tc_reg_rpt_exec_summary_status_sensitivity.json | 2,894 | 4a736930bac2856eee708367064f754ec3fc9ed05bcded58ac71e552327fc042 |

---

## 6. Manifest File Verification

| File | Size (Bytes) | SHA-256 Checksum |
|---|---|---|
| 	esting/evidence/phase_2_7/hashes/manifest_hashes.json | 16,047 | d95036fb77bc9a1d4876636bdcbc3324f8ad8e0cf90e11bcdb88be35aa823180 |

All 93 evidence files have been programmatically inventoried directly from disk bytes without human transcription.
