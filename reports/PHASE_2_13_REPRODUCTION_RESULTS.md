# Phase 2.13 — Independent Reproduction Results

Disposable clones of `d74f56dd…` with Phase 2.13 harness files hash-verified:

| File | SHA-256 (prefix) |
|---|---|
| `evidence_guard.py` | `8c249ca345749a51` |
| `run_all_baseline_tests.py` | `33a5777d676fe8fb` |
| `run_sensitivity_matrix.py` | `7cc8293d0c7183af` |
| `test_evidence_governance.py` | `2cf8a73e40e44a8b` |
| `validate_windows_containment.py` | `30782fbfc7572d75` |
| `verify_manifest.py` | `3418069455e0f87c` |

Env: Python 3.12.16, Linux 6.18.44, numpy 2.5.4, `xvfb-run -a`. Probes as root in `/tmp/ws213`, as non-root `auditor` (uid 30033) in `/tmp/ws213u`, each with a disposable `OSDAGBRIDGE_TRUST_DIR`. The device signing key was read in place only (never copied off-device).

## 1. Clean reproduction (root, `/tmp/ws213clean`)

| Run | Exit | Result |
|---|---|---|
| Baseline | 1 | 14/15 MATCH; **FS BLOCKED** (Linux, expected) |
| Sensitivity | 1 | 11/12 verified; FS UNVERIFIED |
| Governance | 1 | **Ran 27; 1 FAIL (test_10, as root), 3 skipped (9, 16, 17)** |

- `test_10` fails **as root** because POSIX root ignores the `S_IREAD` read-only bit, so the expected `PermissionError` on `open("a")` is not raised. On Windows/non-root this assertion holds.
- Non-root `auditor` baseline rerun: 14/15, FS BLOCKED; sensitivity 11/12.

## 2. Same-user seal / cross-process attacks (non-root `auditor`)

Probe: `/tmp/p25/s213_probe.py`, `/tmp/p25/s213b.py`; output `/tmp/p25/s213_probe.out`.

| # | Action | Result |
|---|---|---|
| D1 | Same-user `open(sealed_file,"a")` | `PermissionError` — read-only honored for non-root owner |
| D2 | Same-user `chmod(0o600)` + write | Succeeds; `verify_manifest_integrity` → **REJECT (HASH_MISMATCH)** |
| D4 | Fresh process removes `.sealed`, then **gateway** write | **Refused** (ledger still lists dir); file intact |
| D5 | Fresh process removes ledger entry **and** `.sealed`, then gateway write | **Succeeds** — attacker content committed (`3e2773`→`9e4eb7`) |
| D6 | Fresh process `chmod` + **raw `open()`** (no gateway) | **Overwrites**; verify → REJECT (detection only) |
| D7 | Fresh process: tamper + delete ledger entry + re-seal with `generate_and_seal_manifest` | `verify_manifest_integrity` → **PASS on `'TAMPERED_THEN_RESEALED'`** |
| D8 | `verify_manifest.py` unpinned trust dir, no flag | **Fail-closed: TRUST ANCHOR PINNING VIOLATION** |
| D8b | `verify_manifest.py --allow-unpinned-trust-dir` | PASS, with `[SECURITY WARNING]` |

Reading: the gateway now blocks fresh-process overwrites through the **supported interface** as long as the ledger entry survives (D4). Detection catches content tampering when the ledger is intact (D2, D6). But the same user can remove the two bookkeeping files (both user-writable) and either overwrite (D5) or re-seal (D7). Pinning is correctly fail-closed and needs an explicit CLI flag (D8/D8b).

## 3. Linux cgroup v2 detection (private mount namespaces)

Probe: harness `ProcessLifetimeJob` + governance Vectors 9/17/27.

| # | Mount at `/sys/fs/cgroup` | `is_contained` | Note |
|---|---|---|---|
| L1 | genuine `cgroup2` (root) | **True** | Child `/proc/self/cgroup` = `0::/osdagbridge_cg_…` **before exec**; Vectors 9+17+27 OK |
| L2 | `tmpfs` + fake `cgroup.controllers` | **False** | correctly rejected (no auto `cgroup.procs`) |
| L3 | `cgroup2` overmounted by `tmpfs`+fake controllers | **False** | rejected |
| L4 | host hybrid default (`tmpfs`) | **False** | rejected; no leaked `osdagbridge_cg_*` |
| L5 | genuine `cgroup2`, non-root, no delegation | **False** | honest BLOCKED |

The Phase 2.12 tmpfs false-positive is fixed, and the child is placed in the cgroup before it executes.

## 4. Windows containment & governance — BLOCKED

Not executable by me (Linux-only shell). From Antigravity's preserved logs:
- `windows_containment_validation.txt`: 6/6 PASS; Check 5 observes t=4.5/9.5/16.5/31.5 s (full 32 s horizon); Check 1 shows the marker absent before/after assign, present after resume.
- `governance_test_output.txt`: `Ran 27 tests … OK` (plain OK ⇒ 0 skips on Windows).

I confirmed the **design** of these tests by code review; I did **not** reproduce them.

## 5. Provenance (device, read-only)

- Official seals `fb966e81` (baseline, 17:37:54), `9aac2738` (sensitivity, 17:41:09), `867d222a` (candidates, 17:41:10): valid HMAC, match disk manifests and `reports/PHASE_2_13_RUN_SEALS.json`.
- Phase 2.13 manifests match disk exactly: 19 / 19 / 54 files, no unlisted files, with `.sealed` present in each.
- The pinned ledger holds **10** entries including **2 governance test seals** (tmp-dir `evidence_dir`, 17:27:40 and 17:27:46) — test execution still writes to the production ledger.
- Baseline/sensitivity `console_error.txt` are byte-identical to Phase 2.12; `console_output.txt` differ (header says "PHASE 2.12 REGRESSION TEST SUITE").
- All 5 baseline (`test_tc_reg_*`) and 5 sensitivity (`mut_b_*`) engineering functions are byte-identical to Phase 2.12.

## 6. Repository & databases (device)

| Item | Value |
|---|---|
| HEAD / branch | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` / `dev` |
| `.git` locks | none |
| Source aggregate (282 files) | `7c9294813b58fb84ecd965643daec240276747d1788b13187c0e0f46c52b024c` |
| `weather.sqlite` | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` ✓ |
| `Intg_osdag.sqlite` | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` ✓ |
| `src/` files changed since 15:30 UTC | 0 |

All probe-created files were confined to `/tmp` disposable copies; no `osdagbridge_cg_*` directories were left on the host.
