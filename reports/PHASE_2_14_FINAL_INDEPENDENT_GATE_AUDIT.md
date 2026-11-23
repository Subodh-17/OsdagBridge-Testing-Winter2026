# Phase 2.14 — Final Independent Gate Audit (Phase 2 Harness)

**Project:** FOSSEE OsdagBridge — baseline regression and sensitivity harness
**Workspace:** `F:\FOSSEE internship` · **App repo:** `source\OsdagBridge`, `dev` @ `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`
**Trust store:** `C:\Users\Subodh\.osdagbridge_trust` (read-only access for this audit)
**Controlling prior audit:** `PHASE_2_13_FINAL_INDEPENDENT_GATE_AUDIT.md` — CONDITIONALLY ACCEPTED, three conditions
**Auditor:** Claude (independent) · **Date:** 2026-11-18

**Companion deliverables:** `PHASE_2_14_FINDING_BY_FINDING_VERDICT.md`, `PHASE_2_14_REPRODUCTION_RESULTS.md`, `PHASE_2_14_FINAL_REMAINING_RISKS.md`.

**Mode:** audit only.
- No application source, database, historical evidence, official trust seal or report was modified. No commit, push or branch change. Phase 3 was not started.
- Adversarial runs used the disposable clone `/tmp/ws214` and a disposable seeded ledger.
- The device signing key was read in place only and never copied off the device.

Labels: **REPRODUCED** (executed by me, disk and hashes checked) · **CODE REVIEW** · **ANTIGRAVITY CLAIM** (evidence produced by the audited party) · **BLOCKED** (I could not execute it).

---

## 1. Overall verdict

# **CONDITIONALLY ACCEPTED**

The Phase 2 harness is now in its strongest and most honestly documented state:
- the ledger cleanup was surgical and fully reversible;
- governance isolation from the production ledger holds empirically;
- the four-tier threat model no longer claims kernel-level protection or non-repudiation;
- all six official seals and their 184 evidence files verify;
- the frozen application and both databases are untouched.

**It is not a full ACCEPTED, and Phase 2 is not formally closed:**
1. **Conditions 1 and 2 (native Windows containment and the governance suite) are still not independently reproduced.** Phase 2.14 re-ran them, but the runs were performed by Antigravity, the party being audited, and I cannot execute Windows. The transcripts are detailed and consistent, but under this audit's rules an Antigravity-produced result is a claim, not a reproduction. They remain **BLOCKED** for independent execution.
2. **Windows Check 5 still cannot fully exclude a writer that never started.** There is no asserted liveness, no start marker, no positive control and no measured timestamps.
3. **One overclaim survived the correction pass.** The revised 2.13 architecture §3.2 still says the layers "guarantee sealed evidence cannot be overwritten from any process."

None of these is a demonstrated security failure. The remaining work is bounded: about two commands run by an independent party, plus small test and wording fixes.

---

## 2. Condition 1 — Native Windows containment

| Check | Transcript (ANTIGRAVITY CLAIM) | Design (CODE REVIEW) |
|---|---|---|
| 1 Suspended before assignment | Marker absent before and after assign, present after resume; assign = 1; suspend count 1 | Sound direct observation. It drives `_winapi` by hand; the harness `job.spawn` path is covered separately by Vector 16. |
| 2 Kill-on-close | Child dead after handle close | Sound |
| 3 Breakaway denied | `BREAKAWAY_DENIED` | Sound |
| 4 Nested inheritance | 3 active in job | Sound |
| 5 Delayed writes 3/8/15/30 s | Active = 1 at 0.5 s; terminated at 0.5 s; no files at t = 4.5 / 9.5 / 16.5 / 31.5 s | **Partial.** Termination before the first write and the 32 s horizon are built into the script. But liveness is printed rather than asserted, there is no start marker or uncontained positive control, and the t = labels are fixed strings, not measured times. |
| 6 Complete termination | 0 active | Sound |

`validate_windows_containment.py` is unchanged since 2.13 (`30782fbf…`). Host Python: `osdagbridge-py312` 3.12.16. The exit code (0) and timestamps (18:17:19 UTC) appear only in the execution history, not in the transcript. `phase_2_14/windows/` is unsealed.

**Verdict:** design **ACCEPTED WITH LIMITATIONS**; independent execution **BLOCKED**.

## 3. Condition 2 — Native Windows governance suite

The verbose Windows transcript (`141b11ca…`) shows **all 27 vectors `ok`, `Ran 27 … OK`, 0 skips, 0 errors, 0 failures**.

Code review confirms the focus vectors perform their intended adversarial operation:
- **V5 / V13:** create real junctions via `_winapi.CreateJunction`.
- **V15:** performs a deterministic directory swap and checks the target bytes.
- **V16 / V9 / V17:** exercise `job.spawn` with process counts and delayed writers. V17 covers 3, 8 and 15 s, not 30 s.
- **V24:** spawns a fresh process against a sealed directory.
- **V25 / V26:** call the real gateway and pinning functions.
- **V27:** a **no-op on Windows**; it is meaningful only on Linux.

**REPRODUCED on Linux (non-root):** 22 ok, 3 honest skips (9, 16, 17), and **2 ERRORs (10, 22)**. The errors are a POSIX test defect: `chmod(stat.S_IWRITE)` produces a write-only file that the verifier then cannot read. This is not a security regression.

**Verdict:** Windows **BLOCKED** (independent execution); Linux **ACCEPTED WITH LIMITATIONS**.

## 4. Condition 3 — Trust ledger cleanup and isolation (REPRODUCED)

- **Backup authenticity:** `trusted_run_seals.json.bak_phase_2_13` = `c10febe0…`, byte-identical to the ledger I **independently captured during the Phase 2.13 audit**, before any Phase 2.14 edit. The pre- and post-cleanup hashes match the claims (`c10febe0…` → `5a9b9273…`).
- **Removed entries:** exactly four (`fc28cba1`, `c344dafd`, `339e7bf0`, `e17e80cf`).
  - Each is labelled `Test`, each points into `C:\Users\Subodh\AppData\Local\Temp\tmp…`, and each is timestamped 17:26–17:27, before the official 2.13 runs.
  - Antigravity's per-entry attribution cites its private agent transcript, which is not in the workspace; I treat that attribution as a corroborated claim.
- **Official seals:** all six (2.12 and 2.13 baseline, sensitivity, candidates) are present and **unaltered** byte-for-byte, with valid HMACs and matching manifests. **184 evidence files** verify (92 per phase), with 0 mismatches and 0 unlisted files.
- **Isolation:**
  - REPRODUCED: the full 27-vector suite run against a **writable** seeded production ledger at the pinned location left it **byte-identical, mtime unchanged**, including the subprocess vectors 7, 8, 23 and 24.
  - On the device, the ledger mtime (18:15:33) predates the Windows governance run (18:18:18), consistent with no write.
  - Every test's `tearDown` asserts the production-ledger hash is unchanged.
- No additional production trust records were deleted or rewritten. I made no ledger edits.

**Verdict:** **ACCEPTED.**

## 5. Security claims

- "Kernel-level" is removed from code and reports.
- "Complete non-repudiation" now reads "requires external authority; NOT in Tier 3".
- Read-only is described as an "accidental-overwrite deterrent".
- Tier 3 states plainly that local HMAC is not a boundary against the same user. The four-tier model remains explicit and accurate.
- **Residual:** §3.2 "guarantee sealed evidence cannot be overwritten from any process" is false for same-user processes (reproduced in 2.13) and must be scoped to Tier 2.
- The 2.13 reports were corrected **in place** (disclosed), so their current hashes differ from the versions audited.

**Verdict:** **ACCEPTED WITH LIMITATIONS.**

## 6. Regression and integrity

- `evidence_guard.py`'s functional code is unchanged from 2.13: the only diff is three comment and docstring lines, written at 18:19:55, after the Windows runs. Disclosed, and functionally equivalent.
- The baseline and sensitivity runners are byte-identical to 2.13, which were byte-identical to 2.12.
- The following prior verdicts therefore stand:
  - cross-process gateway, TOCTOU, cgroup v2 detection and trust pinning: **ACCEPTED**;
  - B01 and RPT: **ACCEPTED**;
  - EQ/A02 and C01: **ACCEPTED WITH LIMITATIONS**;
  - honest Linux FS BLOCKED behaviour is preserved, apart from the N-2 test errors.

| Item | Result |
|---|---|
| Branch / HEAD | `dev` / `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` ✓ |
| Working tree | No `.git` locks; source aggregate `7c929481…` = baseline; 0 source files changed ✓ |
| `weather.sqlite` | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` ✓ |
| `Intg_osdag.sqlite` | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` ✓ |

**Database hash discrepancy:** the brief offers `…74b4f1` as a possible value. The file does **not** match it, and no prior record contains it. The established baseline hash, recorded since Phase 2.4 and re-confirmed in every audit, is `…74d9ea91`, and the file matches that. The brief's value appears to be a transcription error.

---

## 7. What would convert this to ACCEPTED

1. **An independent party runs the two Windows scripts** in a fresh terminal on the host: either the project owner, or me via desktop computer-use if you enable it. Capture the raw output with timestamps, the exit code and the harness hashes, then hash or seal the output.
2. **Harden Check 5:** assert liveness, have the probe write a start marker, add an uncontained positive-control run, and record measured times.
3. **Scope the §3.2 sentence to Tier 2.** Optionally, fix the POSIX `S_IWRITE` defect in tests 10 and 22.

## 8. What acceptance would authorize and what it would not

On reaching **ACCEPTED**, Phase 2 acceptance **would authorize only** the following:
- treating the harness as a trustworthy *regression and evidence instrument* for the frozen baseline `d74f56dd`, under its declared threat model (Tiers 1–2: accidental corruption and supported-interface misuse);
- relying on its BASELINE_FAIL results as reproducible defect detection: 11 defects, 1 PASS, and 3 or 4 BLOCKED specification or platform gaps;
- **considering** a Phase 3 proposal.

It **would not** authorize:
- any application source change or merge to `dev`;
- any claim of security against a malicious same-user process (Tier 3) or of non-repudiation (Tier 4, not implemented);
- treating Linux FS results as verified (BLOCKED on Linux);
- treating BLOCKED tests (D02, C02, GEO-SLAB; FS on Linux) as passing;
- starting Phase 3 itself.

## 9. Gate statement

**CONDITIONALLY ACCEPTED.** Every condition I could test empirically is met. The one condition I cannot test — independent native-Windows execution — remains open, together with two small corrections.

**Phase 3 is not authorized by this audit**; that decision rests with the project owner.
