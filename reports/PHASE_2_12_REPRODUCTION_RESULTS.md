# Phase 2.12 — Independent Reproduction Results

All runs were captured live in disposable fresh clones of `d74f56dd…`, with the Phase 2.12 harness files hash-verified:

| File | SHA-256 (prefix) |
|---|---|
| `evidence_guard.py` | `010c5135bf443f59` |
| `run_all_baseline_tests.py` | `54de12ee7acf385a` |
| `run_sensitivity_matrix.py` | `092041ca2fbc5317` |
| `test_evidence_governance.py` | `512a271d7e9117ff` |
| `validate_windows_containment.py` | `987ea6950c71536e` |
| `verify_manifest.py` | `3169102620344eb8` |

Environment:
- Python 3.12.16, Linux 6.18.44 (glibc 2.39), numpy 2.5.4, `xvfb-run -a`.
- Environment fingerprint: `/tmp/p25/live212/env.txt` `f75974af2d14546a`.
- Each run used its own disposable `OSDAGBRIDGE_TRUST_DIR`. **The real trust store was never written.**

## 1. Official runners

| Run | User | Start (UTC) | Exit | Duration | stdout SHA-256 | Result |
|---|---|---|---|---|---|---|
| Baseline | root | 15:47:22 | 5 (`xvfb-run` cleanup); runner recorded 1 | 60.2 s | `614d43095a93a813` | 14/15; FS BLOCKED; **false `cgroup_v2` detection on tmpfs** |
| Sensitivity | root | 15:48:23 | 1 | 71.4 s | `3f9d2329bbb95241` | 11/12; FS UNVERIFIED |
| Governance | root | 15:49:34 | **1** | 11.2 s | `674f37a268bc2e53` | 23 run: **1 FAIL (Vector 17)**, 1 skip (16) |
| Baseline | auditor (uid 30033), no display | 16:51:17 | 1 | 53 s | `d3b110e5b41a0d0e` | 13/15 (CAD ERROR without a display; my setup error, rerun below) |
| Baseline | auditor, `xvfb-run` | 16:53:04 | 1 | 17 s | `6cf1e3c59ebc81d3` | **14/15; FS BLOCKED** |
| Sensitivity | auditor, `xvfb-run` | 16:53:22 | 1 | 36 s | `1817e7afd0ab6291` | **11/12; FS UNVERIFIED** |
| Governance | auditor | 16:52:41 | 0 | 7.5 s | stderr `e0e9f0eabe8e0bd7` | **20 ok, 3 skipped (9, 16, 17)** |
| `verify_manifest.py` on the non-root baseline | auditor | 16:54 | 0 | — | — | VALID, 19 files |

Live captures: `/tmp/p25/live212/` and `/tmp/p25/live212u/`. Afterwards both clones showed `git status` 0 lines and source aggregate `7c929481…`.

**Windows claim (not reproduced):** baseline 15/15 and sensitivity 12/12, exit 0, from `phase_2_12/*/console_output.txt`. These are consistent with the Windows FS path; I could not execute Windows.

## 2. Seal trust architecture

Probe `/tmp/p25/s212/probe_seal.py` `797b4cc620665d40`; output `probe_seal.out` `e7097ff2929715f8`.

| # | Attack | Verifier exit | Correct? |
|---|---|---|---|
| K0 | Authentic | 0 | ✓ |
| K1 | Evidence modified | 1 (HASH_MISMATCH) | ✓ |
| K2 | Unlisted file added | 1 | ✓ |
| K3 | Listed file deleted | 1 | ✓ |
| K4 | Evidence modified + manifest recomputed | 1 (MANIFEST_TAMPERED) | ✓ |
| K5 / K6 | Ledger deleted / corrupt | 1 | ✓ |
| K7 | Signature forged without the key | 1 | ✓ |
| K8 | Directory copied elsewhere | 1 (NO_SEAL_RECORD) | ✓ |
| K9 | Another run's seal relabelled | 1 | ✓ |
| K12 | Key replaced only | 1 | ✓ |
| **K10** | **Same user: tamper + re-sign with the existing key** | **0** | ✗ |
| **K11** | **Same user: new key + re-sign the whole ledger** | **0** | ✗ |
| **K13** | **Same user: delete the ledger entry, tamper, re-seal with `generate_and_seal_manifest`** | **0** | ✗ |
| **K14** | **Verifier redirected by `OSDAGBRIDGE_TRUST_DIR` to an attacker store** | **0** | ✗ |
| K14b | Same tampered evidence against the genuine store | 1 | ✓ |
| K15 | Authentic after reset | 0 | ✓ |

**Real ledger on the device** (key verified in place, read-only):
- The three official seals (`efb61d9c`, `09dca119`, `c97ab96f`) have valid HMACs and match the disk manifests.
- The three preliminary seals (`e7872f72`, `5e32c735`, `c52a6e19`) have valid HMACs, but their **manifests no longer exist**: the evidence was replaced.
- `reports/PHASE_2_12_RUN_SEALS.json` is byte-identical to the trust ledger.
- Key file: 32 B, mtime 14:23:43, never rotated.

## 3. Evidence gateway

Probe `/tmp/p25/g212/probe_gw.py`; output `probe_gw.out` `4be273065457810d`.

| # | Probe | Disk result |
|---|---|---|
| **W1** | New process: `R.test_tc_reg_a01(evidence_dir=<sealed phase_2_12/baseline>)` | **Overwritten** (`f6e44970`→`ab2bb91e`) |
| W2 / W3 | `phase_2_11` via test function; `phase_2_6` via `safe_write_evidence` | Refused, intact |
| W4 / W5 | Application `src`; application repository root | Refused |
| **W6 / W7** | Workspace root file; `reports/` file | **Written** (removed afterwards) |
| **W8 / W9** | Plain `open()` into `phase_2_6`; `shutil.copy` into sealed `phase_2_12` | **Written** (the gateway is advisory) |
| W10 | TOCTOU directory swap after the check / after the staging open / just before `os.replace` | Refused (`PermissionError` / `FileNotFoundError`); **protected file intact, never truncated** |

## 4. Engineering probes

| Probe | Output | Result |
|---|---|---|
| EQ/A02 X0–X8 | `probe_eqa02.out` `75285922b7d4a079` | Helper ×0.9: caught by EQ and A02. Helper ×1.01: caught by EQ, passes A02 (1 % tolerance). Barrier moved 0.06 m: caught by EQ. Invented keys have no effect. |
| EQ/A02 X9–X10 | `probe_eqa02b.out` `98d268d8e25ec4ee` | **Production ignoring `crash_barrier_load = 8.0` is caught by both** (157.0 vs 192.0 kN per line; 2,711.7 vs 2,806.3 kN). Correct propagation passes. |
| B01 | `probe_b01.out` `f0a52cab0c487358` | Every dimension mutation caught (including bottom flange 410→450 / 412 / 408). Only in-tolerance undersizing passes. |
| C01 | `probe_c01.out` `0b26956f352c0cef` | First/last girder, i-/j-end, incomplete histories caught. −1.5 % and −1.0 % caught; −0.7 % passes. |
| RPT | `probe_rpt.out` `997b06e6b009e2bc` | 29/31 caught. Only the 1.0005 thresholds pass. |

## 5. Linux containment (as root)

- `ProcessLifetimeJob()` created `/sys/fs/cgroup/osdagbridge_cg_*` on a **tmpfs**, not `cgroup2fs`, and reported `is_contained = True`.
- `cgroup.procs` became a regular file containing a PID; `cgroup.kill` was a no-op.
- Vector 17's 3 s write succeeded.
- Six directories were left behind; I removed them from my sandbox afterwards.

## 6. Not reproduced

- Windows Job Object checks 1–6.
- Windows symlink and junction attacks (Vectors 5, 13, 15).
- The Windows FS BASELINE_FAIL result.
