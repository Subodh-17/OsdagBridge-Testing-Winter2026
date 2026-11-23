# OsdagBridge — Software Testing & Issue Reporting (FOSSEE Winter Internship 2026 screening task)

**Candidate:** Subodh Shivmurti Bansode (`Subodh-17`)
**Software under test:** `Nidhikhare12/OsdagBridge`, branch `dev`, commit `d74f56d`, composite plate girder module.

- **Report:** `submission/pdf/OsdagBridge_Testing_Technical_Report_Subodh_Bansode.pdf`. Start here.
- **Fixes as patches:** `patches/0001`–`0006`. These are the six commits that fix DEF-12, DEF-08, DEF-11, DEF-18 (two commits) and DEF-01. Apply them to upstream with:

  ```bash
  git clone https://github.com/Nidhikhare12/OsdagBridge.git && cd OsdagBridge
  git checkout -b fix d74f56dd7f22925fb8148cabf5740ed8d1e39ff3
  git am ../patches/*.patch
  ```

- **Issues reported upstream:** `submission/github_issues/README.md` lists the new issues and the comments on existing ones.
- `source/OsdagBridge/` already contains the source with the patches applied, so the tests run without any install of the fixed code.

---


**Candidate:** Subodh Shivmurti Bansode · subodh171011@gmail.com · GitHub `Subodh-17`
**Module tested:** composite plate girder bridge (OsdagBridge, upstream `Nidhikhare12/OsdagBridge`, base commit `d74f56d`)
**Fixes:** branch `fix/phase-3-engineering-remediation`, HEAD `f555075`. The source in this ZIP is that HEAD.

## Start here

1. **`submission/pdf/OsdagBridge_Testing_Technical_Report_Subodh_Bansode.pdf`** — a 5-page report. Its first table answers what was tested, what was found, what was fixed, the proof and the limitations.
2. **`run_submission_tests.bat`** — runs the three verification suites. Expected results:

| Suite | Expected |
|:--|:--|
| Batch 2 – FE load conservation (DEF-18) | 17/17 OK |
| Batch 3 – load factor scaling (DEF-01, re-checks Batch 1) | 15/15 OK |
| Evidence governance | 27/27 OK on Windows (24 + 3 Windows-only skips on Linux) |

## Requirements

You need Python 3.12 with OsdagBridge's dependencies:

- **Upstream list:** `source/OsdagBridge/environment.yml`.
- **Exact environment used** (`osdagbridge-py312`): `documentation/PHASE_1C_ENVIRONMENT_MIGRATION_REPORT.md`.

The tests import the application from `source/OsdagBridge/src` inside this package, so no install of the fixed code is needed.

```bat
conda activate osdagbridge-py312
cd <extracted folder>
run_submission_tests.bat
```

To open the GUI on the packaged source:

```bat
cd source\OsdagBridge\src
python -m osdagbridge.desktop
```

## What is in the package

| Path | Contents |
|:--|:--|
| `submission/` | Report PDF, resume, sample project file (`osi/`), video script |
| `source/OsdagBridge/` | Application source at `f555075` (5 defects fixed; other defects intentionally left as found) |
| `testing/test_cases/` | Regression suite (`baseline_regression/`) and acceptance suites (`phase_3/`) |
| `testing/evidence/` | Logs and sealed manifests. Baseline failures: `phase_2_13/baseline/`; post-fix results: `phase_3/` |
| `reports/` | Phase-by-phase records; defect matrix: `reports/phase_3/PHASE_3_DEFECT_TRACEABILITY_MATRIX_REV3.md` |
| `documentation/` | Environment setup, upstream issue de-duplication register, test plan |

## Notes

- The Batch 3 suite rewrites its three logs in `testing/evidence/phase_3/batch_3/` on every run, with a new timestamp and the same result.
- Some older scripts in `testing/scripts/` have hard-coded `F:\FOSSEE internship` paths. They are kept as historical records and are not needed for the checks above.
- Only 5 of the 20 register entries are fixed. The others are documented as open, blocked or latent in the report.
