# Phase 2.14 — Independent Reproduction Results

## 0. Inputs (hash-verified)

| File | SHA-256 (prefix) | Change vs 2.13 |
|---|---|---|
| `evidence_guard.py` | `3d5e8d227d41f7e6` | 3 comment/docstring lines only |
| `test_evidence_governance.py` | `133d72a02ff931ab` | isolation: `trust_dir=` passed; `setUp`/`tearDown` ledger-hash assertion |
| `validate_windows_containment.py` | `30782fbfc7572d75` | unchanged |
| `verify_manifest.py` | `3418069455e0f87c` | unchanged |
| `run_all_baseline_tests.py` | `33a5777d676fe8fb` | unchanged |
| `run_sensitivity_matrix.py` | `7cc8293d0c7183af` | unchanged |

Environment: Python 3.12.16, Linux 6.18.44, `xvfb-run -a`. Disposable clone `/tmp/ws214` of `d74f56dd…`; suite run as non-root `auditor` (uid 30033) with `HOME=/tmp/aud_home`. The device trust store was read in place only; nothing in it was written.

## 1. Trust ledger reconciliation (device, read-only)

| Item | Value |
|---|---|
| Ledger captured independently in my Phase 2.13 audit | `c10febe01b8e8c18…` (10 entries) |
| `trusted_run_seals.json.bak_phase_2_13` | `c10febe01b8e8c18…` — **byte-identical** to the above (`cmp` clean) |
| Current `trusted_run_seals.json` | `5a9b9273c26ed92f…` (6 entries), mtime 18:15:33 UTC |
| Removed | `fc28cba1` 17:26:48 · `c344dafd` 17:27:34 · `339e7bf0` 17:27:40 · `e17e80cf` 17:27:46 — all `phase_label "Test"`, `evidence_dir` = `C:/Users/Subodh/AppData/Local/Temp/tmp…` |
| Kept (all byte-identical to backup records) | `efb61d9c` 2.12 baseline · `09dca119` 2.12 sensitivity · `c97ab96f` 2.12 candidates · `fb966e81` 2.13 baseline · `9aac2738` 2.13 sensitivity · `867d222a` 2.13 candidates |
| Signing key | `e84a3bfc…`, 32 B, mtime 14:23:43 (unchanged since Phase 2.12) |

**On-device seal verification (key used in place):**

| Seal | Evidence | HMAC | Manifest = seal | Files | Mismatch | Unlisted |
|---|---|---|---|---|---|---|
| `efb61d9c` | phase_2_12/baseline | ✓ | ✓ | 19 | 0 | 0 |
| `09dca119` | phase_2_12/sensitivity | ✓ | ✓ | 19 | 0 | 0 |
| `c97ab96f` | phase_2_12/candidates | ✓ | ✓ | 54 | 0 | 0 |
| `fb966e81` | phase_2_13/baseline | ✓ | ✓ | 19 | 0 | 0 |
| `9aac2738` | phase_2_13/sensitivity | ✓ | ✓ | 19 | 0 | 0 |
| `867d222a` | phase_2_13/candidates | ✓ | ✓ | 54 | 0 | 0 |

Total: **184 evidence files verified** (92 per phase).

## 2. Governance isolation from the production ledger (REPRODUCED)

Seeded `~/.osdagbridge_trust/trusted_run_seals.json` (= current production content `5a9b9273…`) plus a random key, then ran the full suite without setting any trust environment variable:

| Run | Ledger mode | Exit | Result | Ledger before → after |
|---|---|---|---|---|
| G1 (18:29:02) | read-only (inherited from staging) | 1 | 22 ok, 3 skip, 2 error | identical (but a read-only file cannot prove isolation) |
| **G2** (18:30:13) | **writable 0644** | 1 | **22 ok, 3 skip (9, 16, 17), 2 ERROR (10, 22)** | `5a9b9273…` → `5a9b9273…` **byte-identical, mtime unchanged** |

Outputs: `/tmp/p25/live214/g_stdout` `3a16ab94cfd2d88f`, `g2_stdout` `604fee45e6cb5e8e`.

- The subprocess vectors (7, 8, 23, 24) did not touch the production ledger.
- No `PRODUCTION TRUST LEDGER COMPROMISE` assertion fired.
- **Tests 10 and 22 ERROR on POSIX** with `PermissionError` while re-reading a file. The cause is the tests' own `os.chmod(f, stat.S_IWRITE)`, which is mode `0o200` (write-only) on POSIX. This is a test-portability defect; on Windows the same call only clears `FILE_ATTRIBUTE_READONLY`.

## 3. Windows evidence (ANTIGRAVITY CLAIM — read, not executed)

| Artefact | SHA-256 | Content |
|---|---|---|
| `phase_2_14/windows/windows_containment_validation.txt` (2,640 B; identical `.log` copy) | `3abad109c0a0586d` | 6/6 PASS. Check 1: marker absent before and after assign, present after resume. Check 5: writer active=1 at 0.5 s, terminated at 0.5 s, no files at the 4.5/9.5/16.5/31.5 s labels. |
| `phase_2_14/windows/governance_test_output.txt` (8,126 B; identical `.log` copy) | `141b11caa172e21b` | Verbose: all 27 `ok`; `Ran 27 tests in 17.599s` `OK`; 0 skips. ResourceWarnings in V11 and V20. |

What the transcripts lack:
- no wall-clock timestamps or exit-code line (exit 0 is recorded only in `PHASE_2_14_EXECUTION_HISTORY.md`: containment 18:17:19 UTC, governance 18:18:18 UTC);
- no seal or manifest over `phase_2_14/`;
- no positive control for Check 5.

**I could not execute either script: my device shell is a Linux VM. Independent execution is BLOCKED.**

## 4. Claims grep (reports + code)

- "kernel-level": removed from code and the 2.13 remediation report.
- "complete non-repudiation": replaced with "requires external authority; NOT in Tier 3".
- Tier 3 now states local HMAC is not a boundary against the same user.
- **Remaining:** `PHASE_2_13_SECURITY_ARCHITECTURE.md` §3.2 still reads "guarantee sealed evidence cannot be overwritten from any process".

## 5. Repository & databases (device)

| Item | Value |
|---|---|
| HEAD / branch | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` / `dev` |
| `.git` locks | none |
| Source aggregate (282 files) | `7c9294813b58fb84ecd965643daec240276747d1788b13187c0e0f46c52b024c` |
| `weather.sqlite` | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` ✓ |
| `Intg_osdag.sqlite` | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` ✓ (the brief's `…74b4f1` matches no record) |
| `src/` files changed since 17:45 UTC | 0 |
| Historical evidence files changed since 17:45 UTC (outside `phase_2_14`) | 0 |
