# PHASE 2.8 EVIDENCE MANIFEST & INTEGRITY AUDIT

**Date:** 2026-11-17  
**Controlling Audit:** reports/PHASE_2_7_FINAL_INDEPENDENT_GATE_AUDIT.md  
**Application Repository:** source/OsdagBridge  
**Frozen Baseline Commit:** d74f56dd7f22925fb8148cabf5740ed8d1e39ff3 (branch dev, working tree clean)  

---

## 1. Test Infrastructure & Core Artifact Hashes

| Component / File | Path | Size (Bytes) | SHA-256 Checksum |
|---|---|---|---|
| Baseline Regression Runner | `testing/test_cases/baseline_regression/run_all_baseline_tests.py` | 131,324 | `26c2e9e46f437b86e4bfc747e8f6e60148716cd3fd801451ebb31636da024b09` |
| Sensitivity Matrix Runner | `testing/test_cases/baseline_regression/run_sensitivity_matrix.py` | 50,365 | `35689903ce0a8784541c7f490acd2fe36e71582b1d6db15d469ab3be025bf097` |
| Input Configuration Fixture | `testing/evidence/phase_1d/input_configuration.json` | 44,653 | `31ae62dc08a0de7797aa4ca6451a178fd46cc66bba4c00f7414021336fb10191` |
| Output Dictionary Snapshot | `testing/evidence/phase_1d/output_dictionary_snapshot.json` | 3,333,439 | `429a3198fc93c157a5bd5ee13c74b95612c3410d35a7be1f246867167991a5ab` |
| Structural Database | `source/OsdagBridge/src/osdagbridge/core/data/ResourceFiles/Intg_osdag.sqlite` | 270,336 | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` |
| Weather Location Database | `source/OsdagBridge/src/osdagbridge/core/data/project_location/weather.sqlite` | 180,224 | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` |
| Phase 2.8 Machine Manifest | `testing/evidence/phase_2_8/hashes/manifest_hashes.json` | 16,874 | `41f4d6146108d032420ea30b19cb55c2caa5d1de947a5b773504e17481761368` |
| Phase 2.8 Historical Preservation Manifest | `testing/evidence/phase_2_8/preservation/manifest_preservation.json` | 76,067 | `7f365d632c8c712ada74a2513a3e4944c95bffbceb934f04c0e573bee8042d0c` |

---

## 2. Baseline Evidence (baseline/)

Total files: 0

| Relative Path | Size (Bytes) | SHA-256 Checksum |
|---|---|---|

---

## 3. Candidate Validation Evidence (candidates/)

Total files: 0

| Relative Path | Size (Bytes) | SHA-256 Checksum |
|---|---|---|

---

## 4. Sensitivity Matrix Evidence (sensitivity/)

Total files: 0

| Relative Path | Size (Bytes) | SHA-256 Checksum |
|---|---|---|

---

## 5. Preservation & Forensic Evidence (preservation/)

Total files: 0

| Relative Path | Size (Bytes) | SHA-256 Checksum |
|---|---|---|

---
