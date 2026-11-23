# Phase 2.15 — Reproduction Results

All reproduction was performed by me in disposable locations.

- **Cloud VM:** `/tmp/ws215`, `/tmp/p25`, with a disposable root ledger.
- **User's device:** read-only integrity checks only.

No application source, databases, historical evidence or trust seals were modified. Nothing was committed or pushed, and no branch was switched.

## 1. Environment

- Linux cloud VM, Python 3.12.16 (`/home/claude/envs/repro/bin/python`), `xvfb-run -a`.
- Harness copies (`/tmp/ws215`), SHA-256 prefixes:

| File | SHA-256 prefix | Status |
|---|---|---|
| `evidence_guard.py` | `3d5e8d227d41f7e6` | unchanged since 2.14 |
| `run_all_baseline_tests.py` | `33a5777d676fe8fb` | |
| `run_sensitivity_matrix.py` | `7cc8293d0c7183af` | |
| `test_evidence_governance.py` | `e1e67cbb53ccd5b6` | edited 18:41:09 |
| `validate_windows_containment.py` | `34e7572ceb9823c2` | edited 18:39:12 |
| `verify_manifest.py` | `3418069455e0f87c` | |

- Non-root user `auditor` (uid 30033), with `HOME=/tmp/aud_home`, `TMPDIR=/tmp/aud_tmp` and a seeded writable pinned ledger.
- Root runs used a disposable `/root/.osdagbridge_trust`. The pre-existing sandbox directory was moved aside and **restored** afterwards; the test ledger is retained at `/tmp/p25/root_test_trust_used`.
- Genuine cgroup2: `unshare -m sh -c "mount -t cgroup2 none /sys/fs/cgroup && …"`.

## 2. Governance suite (`test_evidence_governance.py`)

| Run | Result | Skips | Ledger | Leaks |
|---|---|---|---|---|
| Non-root host | exit 0, Ran 27: 24 ok | 3 (V9, V16, V17; honest reasons) | byte-identical | none |
| Root host | exit 0, OK | 3 | byte-identical | none |
| Root + genuine cgroup2 | exit 0, Ran 27, OK | 1 (V16 only) | byte-identical | 0 `osdagbridge_cg*` dirs, no stray probes |

Outputs: `/tmp/p25/live215/gu_out`, `gr_out`, `gc_out`.

## 3. Check 5 discrimination (Linux analogue)

**Method.**

- The Check 5 block (Part 5A … before `passed = …`) is extracted **verbatim** from `validate_windows_containment.py`.
- It runs as a function against the harness's own `evidence_guard.ProcessLifetimeJob` under genuine cgroup2.
- Variants change only the probe text or disable the harness `terminate()`. No containment-escape code was written.

| Variant | What changes | ctrl_passed | contained_passed | Expected | OK? |
|---|---|---|---|---|---|
| baseline | none | True | **True** | True | ✓ |
| premature_exit | contained child writes marker then `sys.exit(0)` | True | **False** (count 0, not alive) | False | ✓ |
| no_marker | contained child never writes marker | True | **False** (marker False) | False | ✓ |
| stale_marker | marker pre-created by parent; child never writes it | True | **True** | False | ✗ **false positive** |
| no_termination | `terminate()` disabled | True | **False** (all 4 files written) | False | ✓ |

- **Baseline timing:** termination at t = 0.069 s; no files at 4.5/9.5/16.5/31.5 s; observation 32.00 s; wall time 63.6 s.
- **Control:** marker "STARTED: PID=459…"; all four writes present at their milestones.
- **Conclusion.** Check 5 correctly detects failed termination, premature exit and a missing start. It does **not** verify that the marker came from the contained PID (F-1.5).
- **Practical risk: low.** The marker path is in a fresh temp directory per run, so a stale marker needs a harness bug or tampering.

Outputs: `/tmp/p25/c5/*.out`, script `/tmp/p25/c5/run_check5.py`.

## 4. On-device integrity (user's machine, read-only)

| Check | Result |
|---|---|
| `.git/HEAD` | `ref: refs/heads/dev` |
| `refs/heads/dev` | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` |
| `.git` lock files | none |
| `src` aggregate | 282 files, `7c9294813b58fb84ecd965643daec240276747d1788b13187c0e0f46c52b024c` |
| `src` files newer than 18:25 UTC | none |
| `weather.sqlite` | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` |
| `Intg_osdag.sqlite` | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` |
| `trusted_run_seals.json` | `5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1` (unchanged) |
| Evidence files changed outside `phase_2_15/` | none |
| `independent_run/` | **does not exist** |

### Official seals (HMAC-SHA256 with the key read in place; canonical `RUN_ID=…\nEVIDENCE_DIR=…\n…\nRUNNER_ID=…`)

| Seal | Label | HMAC | Manifest SHA | Files re-hashed |
|---|---|---|---|---|
| efb61d9c | 2.12 Baseline | ✓ | ✓ | 19/19 |
| 09dca119 | 2.12 Sensitivity | ✓ | ✓ | 19/19 |
| c97ab96f | 2.12 Candidates | ✓ | ✓ | 54/54 |
| fb966e81 | 2.13 Baseline | ✓ | ✓ | 19/19 |
| 9aac2738 | 2.13 Sensitivity | ✓ | ✓ | 19/19 |
| 867d222a | 2.13 Candidates | ✓ | ✓ | 54/54 |

Total: **184/184** files.

The 2.12 directories carry `run_seal.json` rather than a `.sealed` marker. This is consistent with their pre-2.13 sealing scheme. The 2.13 directories carry `.sealed`.

## 5. Artefact hashes inspected (prefixes)

| File | SHA-256 prefix |
|---|---|
| `run_independent_validation.ps1` | `56190f5011d461e7` (7,080 B) |
| `run_independent_validation.bat` | `d1dc7fc72a22acd4` |
| `README_INDEPENDENT_PACKAGE.md` | `2e5adbcc6a5ecd1d` |
| `windows/windows_containment_validation.txt` | `cb5c77b9fdc9e522` (A) |
| `windows/governance_test_output.txt` | `7d84341abedcf99c` (A) |
| `PHASE_2_13_SECURITY_ARCHITECTURE.md` | `2b9226709e6f82fa` |
| `PHASE_2_15_SECURITY_WORDING_CORRECTIONS.md` | `533765edd8fb0407` |

## 6. Not reproduced

All Windows behaviour is unreproduced: Job Object kill-on-close, Windows read-only/ACL semantics, and PowerShell 5.1 vs 7 behaviour of the package. **Reason:** there is no independently controlled Windows session. Antigravity's transcripts are recorded as self-execution only.
