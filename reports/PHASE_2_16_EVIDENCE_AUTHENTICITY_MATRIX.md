# Phase 2.16 — Evidence Authenticity Matrix

**Classes:**

- **IR** = independently reproduced by me
- **AG** = executed by Antigravity and inspected by me
- **CR** = code-reviewed only
- **BL** = blocked by environment

No Antigravity execution is counted as an independent operator run. I did not execute anything natively on Windows.

## 1. Results claimed in the Phase 2.16 reports

| Claim (source) | Artefact | Hash / mtime (UTC) | Class | Authenticity finding |
|---|---|---|---|---|
| Containment 6/6 under "Python 3.12.16 (`osdagbridge-py312`)" (`VALIDATION_RESULTS` Table 1) | `testing/evidence/phase_2_15/windows/windows_containment_validation.txt` (+ `transcripts/….log`) | `1c7d0f98fe85c519…` / 19:18:03 | AG | Genuine-looking Windows transcript (PIDs, Win32 checks). **The interpreter is Python 3.11 (`…\Python311\python.exe`), not the pinned 3.12.** Run directly, not via the package. **It overwrote the 2.15 evidence `cb5c77b9…`.** |
| Governance 27/27 "Phase 2.16" (Table 2) | `…/windows/governance_test_output.txt` | `7d84341abedcf99c…` / 18:43:38 | AG (Phase 2.15) | **Not a 2.16 run.** Byte-identical to the Phase 2.15 transcript. |
| PS 5.1 `Stop` test, "exit code 42 propagated" (`PACKAGE_REMEDIATION` P0.1) | `scratch/test_ps_gates.ps1` "transcript" | absent | — | **Unverifiable.** The file does not exist in the workspace. |
| 4 pre-flight mismatch rejections (P0.3) | `scratch/test_preflight_mismatches.ps1` | absent | — | **Unverifiable** script. Consistent with 4 **empty** run directories (`run_20261117_191452_4eb21e54`, `…191453_348d2cec`, `…191453_9874f9a1`, `…191454_c8449b19`). |
| Collision test (P0.5) | `scratch/test_ps_gates.ps1` Test 2 | absent | — | Unverifiable; IR confirms the behaviour independently. |
| Post-flight manifest values "true" (P0.4) | any `independent_run_manifest.json` | none exists on the device | — | **No package-generated manifest exists.** The package has never completed a run. |
| Production ledger unchanged; 6 seals intact (§4) | ledger and seals | `5a9b9273…`; 6/6 | IR | Confirmed. |
| "Zero surviving overclaims" (P1) | wording documents | see Finding H | IR (grep) | Largely true; minor residue (2.13 L121, 2.15 risks §4). |

## 2. My own results

| Result | Class | Method | Evidence |
|---|---|---|---|
| Device baseline (HEAD, refs, reflog, aggregate, DBs, ledger) | IR | Read-only on the device (`.git` files, `agg25.py`, `sha256sum`) | Final Audit §3.1 |
| 6 seals: HMAC + manifest + 184/184 files | IR | Key read in place on the device, never copied; canonical `RUN_ID=…\n…\nRUNNER_ID=…` | Final Audit §3.1 |
| Check 5 discrimination, 7/7 | IR (Linux cgroup2) | Verbatim 2.16 code against harness `ProcessLifetimeJob` | `/tmp/p25/c5/216_*.out` |
| Runner gates (11 scenarios) | IR (PS 7.4.6 / Linux) | Disposable fixture workspace and ledger copy; `cmd.exe` shim | `/tmp/p216/out_*.txt` |
| Collision / concurrency / read-only base | IR (PS 7.4.6) | Same fixture | `/tmp/p216/out_exist.txt`, `ws_rep/`, `out_ro.txt` |
| Exit-code propagation through `Tee-Object` | IR (PS 7.4.6) | Fake suite exits 3 | `/tmp/p216/out_suite_fail.txt` |
| Clean-tree `$null.Trim()` error; abort under `Stop` | IR (PS 7.4.6) | Same fixture | `/tmp/p216/out_stop.txt` |
| Version/platform not enforced | IR (PS 7.4.6) | Fake "3.9.0 (linux)" interpreter → PASS | `/tmp/p216/out_old.txt` |
| Null manifest while console says PASS | IR (PS 7.4.6) | Error inside manifest literal | first `ws_baseline` run |
| Interrupted run leaves no manifest | IR (PS 7.4.6) | SIGINT during a suite | `/tmp/p216/out_int.txt` |
| PS 5.1 behaviour, `cmd.exe` quote parsing | CR | — | Finding A |
| Win32 Job Object kill-on-close, breakaway, suspended assign | AG + CR | — | containment transcript |
| Final independent operator run | **BL** | No independent Windows session; none exists | — |

## 3. Integrity of prior evidence

| Item | Status |
|---|---|
| Phase 2.12 / 2.13 sealed evidence (184 files) | Intact (IR) |
| Phase 2.13 / 2.14 Windows transcripts | Intact (`3a894209…`, `3abad109…`) |
| Phase 2.15 Windows containment transcript `cb5c77b9…` | **Destroyed** (overwritten 19:18:03 UTC; no copy anywhere) |
| Phase 2.15 governance transcript `7d84341a…` | Intact, but re-cited as 2.16 evidence |
| My Phase 2.14 / 2.15 audit reports | Byte-identical to my delivered copies |
| Phase 2.15 Antigravity reports (wording, risks, guide, README) | Edited in place 19:11–19:14 UTC, as the requested correction pattern; prior versions not preserved |
