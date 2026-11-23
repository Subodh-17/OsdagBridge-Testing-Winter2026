# Phase 2.12 — Finding-by-Finding Verdict

**Controlling audit:** `reports/PHASE_2_11_FINAL_INDEPENDENT_GATE_AUDIT.md` (SHA-256 `26bd4182f45a158c…`)
**Auditor:** Claude (independent) · **Date:** 2026-11-17 · **Baseline:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`

How to read this document:
- The **Verification type** column says how each result was established:
  - **REPRODUCED** — I executed it in a disposable copy and checked disk state and hashes afterwards;
  - **CODE REVIEW** — I inspected the implementation only;
  - **UNVERIFIED** — the claim could not be tested.
- Probe scripts and outputs are listed with their hashes in `PHASE_2_12_REPRODUCTION_RESULTS.md`.

## 1. Phase 2.11 findings (prioritised list items P0–P2)

### F-08 — Linux process containment (P0-1)

- **Phase 2.12 claim:** a cgroup v2 / PID-namespace probe; if neither is available, `is_contained = False` and FS returns BLOCKED.
- **Independent verification (REPRODUCED):**
  - **Non-root:** FS returns **BLOCKED**, the governance suite skips Vectors 9 and 17, and the sensitivity gate is 11/12.
  - **Root, on a host whose `/sys/fs/cgroup` is a writable tmpfs (cgroup v1/hybrid):** the probe's `os.mkdir` succeeds on tmpfs, so the harness reports **`cgroup_v2` containment that does not exist**.
    - `cgroup.procs` is written as a plain file. The process count therefore never drops, so FS records "Detached process detected: True" against a clean candidate.
    - **Vector 17 FAILS:** "Delayed 3s write succeeded despite Job Object termination!"
    - Six `osdagbridge_cg_*` directories were left behind in `/sys/fs/cgroup`.
  - The child is moved into the cgroup only **after** `Popen` returns, and a failed `cgroup.procs` write is silently ignored.
- **Verdict:** **ACCEPTED WITH LIMITATIONS** for non-root: it honestly reports BLOCKED. **REJECTED** for the capability-detection logic: on root it reports false containment.
- **Remaining risk:** Linux has **no** containment capability. Results from root or CI hosts are untrustworthy until the detection checks `cgroup2fs` and moves the child into the cgroup before it executes.

### F-07 — Run-seal trust anchor (P0-2)

- **Phase 2.12 claim:** an HMAC-SHA256-signed ledger in `%USERPROFILE%\.osdagbridge_trust`, a fail-closed verifier, governance tests isolated from the ledger.
- **Independent verification:**
  - **REPRODUCED:** a probe matrix K0–K15, and HMAC verification of the real ledger on the device using the key in place (not copied off the device).
  - **Detected:** modified, added and deleted files; manifest recompute; ledger deleted or corrupt; forged signature; copied directory; relabelled seal; key replaced alone.
  - **Accepted as authentic** (each the same OS user):
    - **K10** — tamper the evidence and re-sign with the existing key;
    - **K11** — replace the key and re-sign the whole ledger;
    - **K13** — delete the ledger entry and re-seal with the harness's own `generate_and_seal_manifest`, without ever reading the key. This is the operation Phase 2.12 itself performed with its preliminary seals.
    - **K14** — point the verifier at an attacker trust store through `OSDAGBRIDGE_TRUST_DIR`.
  - The governance tests do isolate the ledger (they use a temporary `OSDAGBRIDGE_TRUST_DIR`). Nothing test-generated is in the real ledger.
- **Verdict:** **REJECTED** as a trust anchor. ACCEPTED as integrity against accidental drift and against a party who has no access to the trust directory.
- **Remaining risk:** the key, the ledger and the evidence are all writable by the same Windows user. The HMAC gives integrity *within* that trust domain, not independent anchoring.

### F-05 — TOCTOU truncation (P0-3)

- **Phase 2.12 claim:** stage to an `O_EXCL` temporary file, re-validate, then `os.replace`.
- **Independent verification:**
  - **REPRODUCED (Linux):** swaps were tested at three points: after the check, after the staging open, and immediately before `os.replace`. In all three the protected file was **unchanged**; the operation raised `PermissionError` or `FileNotFoundError`.
  - **UNVERIFIED (Windows):** Vectors 5, 13 and 15 are the three skipped Windows tests, so the symlink and TOCTOU defences were **not executed on the target platform**. Junctions (no admin needed) were not tried.
  - **CODE REVIEW (Windows):** `os.path.islink` does not detect junctions; protection there relies on the `realpath` comparison.
- **Verdict:** **ACCEPTED** (Linux); **NOT VERIFIED** (Windows).
- **Remaining risk:** Windows junction swaps remain untested.

### F-06 — Gateway scope and the missing `--evidence-dir` crash (P1-4)

- **Phase 2.12 claim:** an allowlist, sealed-directory refusal, source and repo-root refusal, and the `uuid` fix.
- **Independent verification (REPRODUCED):**
  - **Refused:** writes into protected phases, the application `src`, and the application repository root. The `uuid` crash is fixed (Vector 23).
  - **Allowed (W1):** in a **new process**, a direct `R.test_tc_reg_a01(evidence_dir=<sealed phase_2_12/baseline>)` **overwrote the sealed active evidence**. `_SEALED_DIRECTORIES` and `_AUTHORIZED_DIRECTORIES` are in-memory per process, so a fresh process has an empty allowlist and an empty sealed set. The verifier detects this afterwards; the gateway does not prevent it.
  - **Allowed (W6, W7):** writes to the workspace root and to `reports/`.
  - **Allowed (W8, W9):** plain `open()` and `shutil.copy` into `phase_2_6` and into sealed `phase_2_12` (the gateway is advisory).
- **Verdict:** **REJECTED**.
- **Remaining risk:** current-phase evidence can be overwritten by any harness code path launched in a new process.

### F-10 — EQ/A02 barrier input oracle (P1-5)

- **Phase 2.12 claim:** the oracle uses the real `crash_barrier_load` key and `DEFAULT_CRASH_BARRIER_WIDTH`; candidate (b) is restored to `crash_barrier_load_from_inputs`; Vectors 18 and 19 are rewritten.
- **Independent verification (REPRODUCED):**
  - The invented keys `loading.crash_barrier_load` and `typical_section.barrier_width` are **absent** from the harness.
  - Correct production following `crash_barrier_load = 8.0` passes (X10).
  - **Production ignoring the input fails in both EQ and A02 (X9):** EQ 157.0 vs 192.0 kN per line; A02 2,711.7 vs 2,806.3 kN.
  - A wrong helper ×0.9 is caught by both; the barrier moved 0.06 m is caught by EQ.
  - Component tolerances: A02 lets a 1 % helper error pass (X2); EQ catches it.
- **Verdict:** **ACCEPTED WITH LIMITATIONS**.
- **Remaining risk:** barrier *width* comes from the production constant, not from an input. Production ignores `typical_section.crash_barrier.width = 0.45` and no test flags this.

### F-12 — Provenance (P1-6)

- **Phase 2.12 claim:** an execution history, live transcripts and disclosed preliminary runs.
- **Independent verification:**
  - **REPRODUCED:** live stdout and stderr exist for the official baseline and sensitivity runs. All three official seals carry valid HMACs and match their manifests. 19 / 19 / 54 files match, with no unlisted files.
  - **Inspected:**
    - The **preliminary runs 3 and 4 wrote to the same official directories**. Their evidence no longer exists: all three preliminary seals have valid HMACs, but their manifests are gone from disk.
    - Their seals were **removed from the authoritative ledger** (moved to `preliminary_run_seals_phase_2_12.json`) so the directories could be re-sealed.
    - No transcript or output was preserved for Run 1 (Windows containment), Run 2, the Run 5 governance runs, or the preliminary runs.
    - The Phase 2.11 disclosure is inaccurate: it gives the rerun as 12:48; the seals show 12:44:30–12:45:36.
- **Verdict:** **REJECTED**.
- **Remaining risk:** evidence was reused and deleted, and the ledger was edited. The execution history is a narrative, not evidence.

### F-09 — Windows containment (P2-7)

- **Phase 2.12 claim:** `validate_windows_containment.py` passed 6/6.
- **Independent verification:**
  - **UNVERIFIED:** no Windows execution was available to me, and **no output of the 6/6 run is preserved**.
  - **CODE REVIEW:** the design is correct (`CREATE_SUSPENDED`, assign, resume, `KILL_ON_JOB_CLOSE`, no breakaway flags, lock-protected hook). But the validation script **cannot prove two of its claims**:
    - **Check 1** only shows the child runs and is counted. It cannot show no instruction ran before assignment.
    - **Check 5** terminates the job at 0.5 s and looks for files after 4 s. The 8, 15 and 30 s writes could not have occurred by then even with **no** containment. Delayed writes at 8, 15 and 30 s are **not tested**.
- **Verdict:** **BLOCKED**.
- **Remaining risk:** Windows containment may well work but has not been demonstrated. The "30 s delayed-write prevented" claim is unsupported by the test's design.

### F-11b — C01 (P2-8)

- **Phase 2.12 claim:** G2 refixtured to 3,200 kNm; tolerance 0.8 %.
- **Independent verification (REPRODUCED):**
  - Expected values: 2,900 kNm / 15.9416 × 10⁶ mm³ = **181.92 MPa** (G1, element 1 i-end) and 3,200 kNm → **200.73 MPa** (G2, element 5 j-end). Both match.
  - **Caught:** first girder only, last girder only, i-end only, j-end only, first or last element, incomplete histories, order-dependent and absolute-value shortcuts, raw shared-node signs, and **−1.5 % and −1.0 %** scaling.
  - **Pass:** −0.7 % (inside 0.8 %); dropping LC5 (not an extremum); merging mixed end signs.
- **Verdict:** **ACCEPTED WITH LIMITATIONS**.
- **Remaining risk:** the expected values are fixed constants that embed production's composite Z<sub>b</sub> (m = 7.5). The 0.8 % tolerance is a test-design choice, not a derived error bound.

## 2. Phase 2.11 findings not on the P0–P2 list

| Phase 2.11 ID | Status in 2.12 | Verification | Verdict |
|---|---|---|---|
| F-01 / F-02 / F-03 historical integrity and repository | All historical manifests match (2.5–2.11). The two Phase 2.6 baseline logs are still lost and documented. No historical file changed after 13:30 UTC. HEAD, source aggregate and both databases are unchanged. | REPRODUCED (device) | **ACCEPTED** |
| F-04 protected-path refusal | Still refused: protected phases, `..`, symlink, case variants, `phase_2_baseline` / `phase_2_repaired`, `phase_2_11`. | REPRODUCED | **ACCEPTED** |
| F-11a B01 | All dimension and property mutations beyond tolerance are caught, including bottom flange width. | REPRODUCED | **ACCEPTED** |
| F-11c RPT | 29 of 31 shortcuts caught. Only the sub-resolution 1.0005 thresholds pass. | REPRODUCED | **ACCEPTED** |
| F-13 clean reproduction | Linux non-root: 14/15 (FS BLOCKED) and 11/12. Linux root: 14/15 and 11/12. The Windows claim of 15/15 and 12/12 is consistent with the Windows FS path but was not reproduced. | REPRODUCED / UNVERIFIED | **ACCEPTED WITH LIMITATIONS** |

## 3. Additional Phase 2.12 findings

| ID | Finding | Verification | Verdict |
|---|---|---|---|
| N-1 | Governance tests skipped on Windows (5, 13, 15) are exactly the symlink and TOCTOU attack tests. On Linux non-root, 9, 16 and 17 are skipped; on root, Vector 17 **fails**. "20 OK + 3 skipped" is not "23 pass". | REPRODUCED | **ACCEPTED WITH LIMITATIONS** (the suite is honest about skips; the attack coverage is incomplete) |
| N-2 | Vector 22 covers S1–S11 but none of the same-user re-sign, key-replace, ledger-edit or trust-directory-redirect attacks (K10, K11, K13, K14). | REPRODUCED | **REJECTED** as evidence of trust-anchor strength |
| N-3 | Baseline test quality: the 11 BASELINE_FAIL tests match the defects verified in Phases 2.4–2.11. The PASS (CAD) is justified. The three BLOCKED tests (D02, C02, GEO-SLAB) are specification gaps, not architecture. On Linux, FS is a fourth BLOCKED. | REPRODUCED + previous phases | **ACCEPTED WITH LIMITATIONS** |

## 4. Overall

**REJECTED.** Material defects remain:
- the trust anchor (F-07);
- the gateway scope (F-06);
- provenance (F-12);
- Linux capability detection (F-08, root).

Windows containment (F-09) is BLOCKED.
