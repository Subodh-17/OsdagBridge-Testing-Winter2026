# PHASE 2.5 — Cryptographic Evidence Manifest

**Date:** 2026-11-16  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`, 100% clean)  
**Controlling Document:** `reports/PHASE_2_4_FINAL_INDEPENDENT_GATE_AUDIT.md`  
**Evidence Root:** `testing\evidence\phase_2_5\`  

---

## 1. System & Environment Fingerprints

| Component | Value / Version | Cryptographic SHA-256 Hash |
|:---|:---|:---|
| **Python Version** | `3.12.16 (tags/v3.12.16:51152a2, Nov 15 2026, 18:24:28) [MSC v.1944 64 bit (AMD64)]` | — |
| **Python Executable** | `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe` | — |
| **OS Platform** | Windows 11 Enterprise (AMD64), Build 10.0.26300 | — |
| **Baseline Git Branch** | `dev` | — |
| **Baseline Git Commit** | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` | — |
| **Database: Intg_osdag.sqlite** | 270,336 bytes | `25f97857d4cbe2054ff1a669bc673fb370e7a2b97c23bc9514eef93df155a0b7` |
| **Database: weather.sqlite** | 180,224 bytes | `1d7676587372cf936f212239be9b2bf0df7b545f4cb609d57a916a4be7ad85e3` |
| **Harness: run_all_baseline_tests.py** | — | `e26a0cae18fa428e2023dbf7fc138fb0b3b44b9cb79f1efc9b19d5c4eaae0b6f` |
| **Harness: run_sensitivity_matrix.py** | — | `d9270bb3f567b45cae7c5b62b02e6eebef652a9261ff2f0e0db1eb1eb3602d24` |
| **Fixture: base_config.json** | 1,846 bytes | `31ae62dc08a0de7797aa4ca6451a178fd46cc66bba4c00f7414021336fb10191` |
| **Fixture: fixture_manifest.json** | 565 bytes | `9a660a9f5d6f4614e519c5c7dc24c1630b42f61869e98e27c1341c2c366ffbc3` |

### Installed Package Manifest
- `OCC` (pythonocc-core): `8.0.1`
- `openseespy`: `3.8.0.0`
- `ospgrillage`: `0.6.0`
- `numpy`: `2.5.5`
- `scipy`: `1.18.1`
- `pandas`: `3.1.1`
- `xarray`: `2026.9.0`
- `PIL` (Pillow): `13.0.0`

---

## 2. Phase 2.5 Complete File Inventory & Cryptographic Hashes

All 93 files in `testing/evidence/phase_2_5/` have been verified directly against disk:

### 2.1 Baseline Suite Evidence (`baseline/`)

| Relative File Path | Size (Bytes) | SHA-256 Digest |
|:---|:---:|:---|
| `baseline/baseline_exit_code.txt` | 1 | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` |
| `baseline/console_output.txt` | 42,848 | `c771144619ab2427a14e9fef39ff028bfdf9b27fce293c66f7fbb6b4923e390c` |
| `baseline/phase_2_5_baseline_summary.json` | 12,243 | `7cb5929822a13d2af98516eeadab326c9dfeb23ce36dd65b7501b44ec94b2f27` |
| `baseline/shell_exit_code.txt` | 8 | `4af4aed4248c649eb0cbdf71d87f54c30b2053155aa51152d2f70b77b96e95aa` |
| `baseline/tc_reg_a01_factor_scaling.log` | 1,079 | `2964523dfea1fa4721dd51a8470a169eb9c7d41f5341a9cbaf9b3dd2459fb7a2` |
| `baseline/tc_reg_a02_uls_combination_sum.log` | 1,987 | `e74acdf51025dd3a7b5e43a9b9a674db45df33faecdb27926b2d29255653ba3e` |
| `baseline/tc_reg_b01_section_property_sync.log` | 1,977 | `5716584aa20918a80d5656128062ecbb8cf6fb0081bf482e967a216f56c7d1e8` |
| `baseline/tc_reg_c01_sectional_stress_range.log` | 1,778 | `3c1069b30bcbb4f107f9754f9a74421b58535a909ea26871a2a8932fc4cbb040` |
| `baseline/tc_reg_c02_fatigue_vehicle_analysis.log` | 1,715 | `28d56b49416eab7982f6e5e8e8ae382ae7e8344e789ec3298a0ebc9fa30f40d1` |
| `baseline/tc_reg_cad_export_vs_screenshot.log` | 963 | `7d71df9a20903567d1dcf5fe8ebf4b1ba271c0800ba837b02db4f932e604f329` |
| `baseline/tc_reg_cap_stiffener_buckling.log` | 1,336 | `5dcf82d02c98bf5511c1d810f5451c4a03ee70c1e457f5c531061f237efb9bc0` |
| `baseline/tc_reg_d01_wind_speed_propagation.log` | 1,317 | `9fa733d711f564175b31df66d51ae16f5a34ec8d80f8c879ee07fe6b54eaec34` |
| `baseline/tc_reg_d02_temperature_propagation.log` | 1,394 | `797d022b3e4141d5b3ee28e75e119ea55a7309919f179c53cb09e13b82531e21` |
| `baseline/tc_reg_eq_load_conservation.log` | 2,638 | `e59a4bb59dbfc6b56ec483665a3962b322da54a43b221d607a94d80584488db0` |
| `baseline/tc_reg_fs_clean_working_tree.log` | 1,747 | `9b533db560a63aa6e1744ae1dd72605f6381656ec56fe73e3bf0d0bf3cbcc898` |
| `baseline/tc_reg_geo_girder_count_alignment.log` | 996 | `3b5443fae0176df3d35aeae89098e9ec19e59d997ccb428d099955e4bf5b7966` |
| `baseline/tc_reg_geo_slab_section_properties.log` | 1,491 | `c8df294ea5116aa92c5780a13efd20894e6378e9b6ae663674cff2008f51a700` |
| `baseline/tc_reg_mat_density_consistency.log` | 1,078 | `36d8dbf4305bc93c0bc5e8bc8652485ecf8373302bc6f1d06371cfb96b3a0937` |
| `baseline/tc_reg_rpt_exec_summary_status.log` | 1,744 | `9478f7e914041a7d65691eaec87877cecae3ebbe2fa460d3c5092a0e4c6328ee` |

### 2.2 Sensitivity Matrix Summaries & Per-Test JSONs (`sensitivity/`)

| Relative File Path | Size (Bytes) | SHA-256 Digest |
|:---|:---:|:---|
| `sensitivity/console_output.txt` | 94,030 | `9a7ce1c504ca4334bc7e4c27a92fb4e6c999be32aa8784d5df3ec76cbcf4e815` |
| `sensitivity/phase_2_5_sensitivity_matrix_summary.json` | 24,914 | `41a69a21e4a30eef7ec1aa7db44fc8b9759885bf22fa59dfcfd1f65dc7f6b907` |
| `sensitivity/sensitivity_exit_code.txt` | 3 | `525eb2c5240bc1c7aa7c30953a1a63c3ca16efc3b5fa770c02506e7681e1e944` |
| `sensitivity/shell_exit_code.txt` | 8 | `4af4aed4248c649eb0cbdf71d87f54c30b2053155aa51152d2f70b77b96e95aa` |
| `sensitivity/tc_reg_a01_factor_scaling_sensitivity.json` | 1,357 | `991207865f121d5c21fc7c71ba42db9d2ae2eb69408665ba48a74ec31c778408` |
| `sensitivity/tc_reg_a02_uls_combination_sum_sensitivity.json` | 1,674 | `ff3c1c4f69324ca2d76be5a21004eaefc975a6c3821a719d4b29bb887d15950e` |
| `sensitivity/tc_reg_b01_section_property_sync_sensitivity.json` | 1,652 | `4e2e3ffba0e4fe84f23e20ecf0f2cf7e3c15aa1f9b375b11c34a06587c6999a4` |
| `sensitivity/tc_reg_c01_sectional_stress_range_sensitivity.json` | 1,633 | `1621287e0766b44747eb4653dd774bdf73dfab3545dfd7ef7b198166c3a5b9b9` |
| `sensitivity/tc_reg_c02_fatigue_vehicle_analysis_sensitivity.json` | 1,346 | `3d6642781b4dfd0f2834b679ae114b77d6ee3e2d63499252084df9fa3d001b65` |
| `sensitivity/tc_reg_cad_export_vs_screenshot_sensitivity.json` | 1,310 | `b99d63897ca4fbb61e893e18a0ca952aaee14be95079a4993a404b04334360e2` |
| `sensitivity/tc_reg_cap_stiffener_buckling_sensitivity.json` | 1,571 | `86ca5b81a8f9ec297dd20eb389ca052ea63dd5df9fe91a5e1bb3429815041ff6` |
| `sensitivity/tc_reg_d01_wind_speed_propagation_sensitivity.json` | 1,540 | `739a888ca388653ca269550e1ef711b74251f2e6ee5ecb684cb40fb7e96b79c3` |
| `sensitivity/tc_reg_d02_temperature_propagation_sensitivity.json` | 1,272 | `f34d1dd77678c2e64fb6ebdb82955f190eec2604859a8508eb67828062829fc4` |
| `sensitivity/tc_reg_eq_load_conservation_sensitivity.json` | 1,707 | `4322d863f6a27e7be46fb0ce8dcbc6ce7eaee8d20371a5c68fce14fe47b7bb6f` |
| `sensitivity/tc_reg_fs_clean_working_tree_sensitivity.json` | 1,569 | `b6e1ee540a8bf79a515c54d1d9ec347102ff9478148b11b1cc83be251ea73b50` |
| `sensitivity/tc_reg_geo_girder_count_alignment_sensitivity.json` | 1,440 | `47318ff24858b2921a98075fe5d66649f4ae0ff05e79ffc6fa076a59bcaee9b4` |
| `sensitivity/tc_reg_geo_slab_section_properties_sensitivity.json` | 1,363 | `7bfd620ff3eb7bc714f3b7d15a519889be8cbf83b4007f3521d8b63486ccfef9` |
| `sensitivity/tc_reg_mat_density_consistency_sensitivity.json` | 1,450 | `dbd5dfd9715d909b0b4662d5fa4b84b5feae8e97ff0668b8e0108ec968f54c93` |
| `sensitivity/tc_reg_rpt_exec_summary_status_sensitivity.json` | 1,755 | `a84cb95758dd0a3ae2a677e4cfdfa06fb54618e76ae8d54c1537dc7b57fa962e` |

### 2.3 Candidate Mutation Logs (`candidates/`)

All 54 candidate log files in `candidates/` (covering Baseline, Minimal Correct, and Naive implementations for all 15 tests) are preserved. Key candidate hashes:
- `tc_reg_eq_load_conservation_b_correct.log` (2,454 B): `8946f047ff5b3f71c35b8014e047432bc9776d40026e95bf0885a0cbb0fb34c6`
- `tc_reg_eq_load_conservation_c_naive.log` (2,536 B): `01cf506eb36384a6c6ec2ec5d2b1f83c072c72b22bb95f57fcb5b5dfa9a3b6aa`
- `tc_reg_fs_clean_working_tree_b_correct.log` (1,605 B): `514bcbf26190800d9a6cbf3eb24d86b97b09ca51745778a48ef0e58f01b1b443`
- `tc_reg_fs_clean_working_tree_c_naive.log` (1,523 B): `d6511a0cb96bdfdb847c94132be783dff4b13eeec5c73d9e830f57630248e3cf`
- `tc_reg_rpt_exec_summary_status_b_correct.log` (1,566 B): `7f9b8fa7706d87e35b719bebc669fec6f37688243be8fc22359d93e823ca7760`
- `tc_reg_rpt_exec_summary_status_c_naive.log` (1,644 B): `ffb16eb3d22097e3cb7f83e390c95ce5e69e8f170a7bb140b9c3f25c27632626`
- `tc_reg_b01_section_property_sync_b_correct.log` (1,806 B): `44ebfa53e414c1fa0b55502c377d0793666b6e4e08285517173e63ba5fb77e51`
- `tc_reg_c01_sectional_stress_range_b_correct.log` (1,668 B): `2c2a04870c99f1fa15c13f990ea50ff6cb2d74a2cb5e985b9b71a2a468d6f517`

---

## 3. Known Historical Provenance Limitation

In accordance with Claude's Phase 2.4 audit findings, the following provenance record is documented:
- During Phase 2.4 test harness prototyping, 5 candidate log files in the legacy directory `testing/evidence/phase_2_3/candidates/` were overwritten prior to the introduction of the isolated `testing/evidence/phase_2_4/` directory.
- This historical event has zero impact on Phase 2.4 or Phase 2.5 integrity. All Phase 2.5 artifacts were generated strictly inside the isolated directory `testing/evidence/phase_2_5/`, leaving all prior directories intact and unchanged.

---

## 4. Manifest Integrity Assurance

The master cryptographic manifest containing the SHA-256 hash and byte size for all 93 files is stored at:
`testing\evidence\phase_2_5\hashes\manifest_hashes.json`

Integrity check command:
```powershell
& "C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe" -c "
import json, os, hashlib
with open('testing/evidence/phase_2_5/hashes/manifest_hashes.json') as f:
    mf = json.load(f)
for rel, meta in mf.items():
    fp = os.path.join('testing/evidence/phase_2_5', rel)
    h = hashlib.sha256(open(fp, 'rb').read()).hexdigest()
    assert h == meta['sha256'], f'Hash mismatch: {rel}'
print('All 93 evidence files verified byte-identical against manifest!')
"
```
