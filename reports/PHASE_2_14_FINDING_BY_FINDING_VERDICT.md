# Phase 2.14 — Finding-by-Finding Verdict

**Controlling prior audit:** `PHASE_2_13_FINAL_INDEPENDENT_GATE_AUDIT.md` (CONDITIONALLY ACCEPTED, three conditions)
**Auditor:** Claude (independent) · **Date:** 2026-11-18 · **Baseline:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`

Labels: **REPRODUCED** (I executed it and checked disk/hashes), **CODE REVIEW** (inspection only), **ANTIGRAVITY CLAIM** (evidence produced by Antigravity that I could only read), **BLOCKED** (I could not execute it: no Windows host).

## 1. The three Phase 2.13 conditions

| # | Condition (from 2.13 audit) | Phase 2.14 remediation | Independent test | Evidence | Verdict |
|---|---|---|---|---|---|
| **1** | Independently reproduce the 6 Windows Job Object containment checks on a real Windows host, with preserved output | Antigravity re-ran `validate_windows_containment.py` on the host (18:17:19 UTC, exit 0) and preserved output | CODE REVIEW of the script (unchanged since 2.13, `30782fbf…`); read the transcript; **could not execute** | `phase_2_14/windows/windows_containment_validation.txt` `3abad109…`: 6/6 PASS, host-native PIDs and paths | **BLOCKED** (independent execution). The run was performed by the party being audited, so it is not an independent reproduction. Check 5 design gap noted in §2. |
| **2** | Independently reproduce all 27 governance vectors on Windows, zero skips/errors/failures, preserved output | Antigravity re-ran `test_evidence_governance.py -v` on the host (18:18:18 UTC, exit 0) | CODE REVIEW of every vector; read the verbose transcript; REPRODUCED the suite on Linux | `phase_2_14/windows/governance_test_output.txt` `141b11ca…`: all 27 `ok`, `Ran 27 tests … OK`, 0 skips. On Linux non-root I get **22 ok / 3 skipped / 2 ERROR** | **BLOCKED** (Windows, independent execution) — transcript is consistent and complete. **ACCEPTED WITH LIMITATIONS** as a Linux result (see N-2) |
| **3** | Correct the "kernel-level" / Tier-2 `S_IREAD` and Tier-4 "complete non-repudiation" wording | Edited `PHASE_2_13_REMEDIATION_REPORT.md`, `PHASE_2_13_SECURITY_ARCHITECTURE.md` and three `evidence_guard.py` comments (18:19 UTC); `PHASE_2_14_SECURITY_CLAIMS_CORRECTIONS.md` | Grep of all 2.13/2.14 reports and all harness code; `diff` of `evidence_guard.py` 2.13→2.14 | "kernel-level" and "complete non-repudiation" are gone; read-only is now called an "accidental-overwrite deterrent"; Tier 3 states HMAC is not a boundary against the user. **Residual:** `PHASE_2_13_SECURITY_ARCHITECTURE.md` §3.2 still says the three layers "**guarantee sealed evidence cannot be overwritten from any process**" — false for same-user processes (2.13 probes D5/D6/D7) | **ACCEPTED WITH LIMITATIONS** (one residual overclaim) |
| **3b** | Stop governance tests writing to the production ledger; remove the stray entries | Backup created; 4 entries pruned; tests pass `trust_dir=self._trust_td.name`; `setUp`/`tearDown` assert the production-ledger hash is unchanged | REPRODUCED: ledger reconciliation on device (read-only), HMAC re-verification, Linux full-suite run against a **writable** seeded production ledger | See §3 below | **ACCEPTED** |

## 2. Windows containment — check-by-check (transcript review; BLOCKED for execution)

| Check | What the transcript shows | Design adequacy (code review) | Verdict |
|---|---|---|---|
| 1 Suspended child before assignment | Marker absent while suspended, absent after assign, present only after resume; assign returned 1; suspend count 1 | Sound: `_winapi.CreateProcess(…, CREATE_SUSPENDED)` + marker file is a direct observation. **But** it drives `_winapi` by hand, not the harness's `ContainedPopen`/`job.spawn` path (that path is exercised by Vector 16) | BLOCKED; design ACCEPTED |
| 2 Kill-on-close | Child alive after handle close: False | Sound | BLOCKED; design ACCEPTED |
| 3 Breakaway denied | Child printed `BREAKAWAY_DENIED`, job count 1 | Sound (`CREATE_BREAKAWAY_FROM_JOB` raises inside a job without `BREAKAWAY_OK`) | BLOCKED; design ACCEPTED |
| 4 Nested inheritance | 3 active processes in job (≥2 expected) | Sound | BLOCKED; design ACCEPTED |
| 5 Delayed writes 3/8/15/30 s | Writer "active in job=1" at 0.5 s; job terminated at t≈0.5 s; no file at t=4.5/9.5/16.5/31.5 s | **Partially meets the brief.** Termination before 3 s and the 32 s horizon are built in. But: (a) the writer being *alive* is printed, not asserted in `passed`; (b) there is **no start marker and no positive control** (same probe run uncontained, showing it does write), so a writer that would have failed for another reason is not excluded; (c) the transcript records **no wall-clock timestamps**: the t= labels are fixed strings, not measurements | BLOCKED; design **ACCEPTED WITH LIMITATIONS** |
| 6 Complete termination | Active processes 0 | Sound | BLOCKED; design ACCEPTED |

Host/environment: `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe`, Python 3.12.16 (execution history). Exit code 0 and timestamps are recorded only in `PHASE_2_14_EXECUTION_HISTORY.md`, not in the transcript. The `phase_2_14/windows/` evidence is **not sealed** (no manifest or seal).

## 3. Trust ledger cleanup (REPRODUCED)

| Requirement | Result |
|---|---|
| Backup byte-identical to the original ledger | **Yes.** `trusted_run_seals.json.bak_phase_2_13` = `c10febe0…` = the ledger I **independently captured during my Phase 2.13 audit**, before Phase 2.14 began. |
| Pre-/post-cleanup hashes | Pre `c10febe01b8e8c18…` (10 entries) ✓; post `5a9b9273c26ed92f…` (6 entries) ✓ |
| Removed entries | Exactly 4: `fc28cba1` 17:26:48, `c344dafd` 17:27:34, `339e7bf0` 17:27:40, `e17e80cf` 17:27:46 — all `phase_label: "Test"`, all `evidence_dir` under `C:/Users/Subodh/AppData/Local/Temp/tmp…`, all before the official 2.13 runs (17:37) |
| Classification evidence | Strong circumstantial evidence: label, temp paths, timing. Antigravity's per-entry attribution cites its own agent `transcript.jsonl` lines 8859–8873, which is **not** in the workspace and which I could not inspect. Treated as ANTIGRAVITY CLAIM, corroborated. |
| Six official seals intact | All six (`efb61d9c`, `09dca119`, `c97ab96f`, `fb966e81`, `9aac2738`, `867d222a`) are present and **byte-for-byte unaltered** versus the backup; HMAC valid with the device key; manifest hash = seal |
| Associated evidence | **184 files** (92 per phase × 2) verify: 0 mismatches, 0 unlisted. (The brief's "92" is per phase.) |
| Governance isolation (all processes) | REPRODUCED: full 27-vector suite run as non-root against a **writable** seeded pinned ledger (`~/.osdagbridge_trust`). Ledger `5a9b9273…` → `5a9b9273…`, **byte-identical, mtime unchanged**, including subprocess vectors 7, 8, 23, 24. No `tearDown` compromise assertion fired. On Windows, the ledger mtime (18:15:33) predates the governance run (18:18:18), consistent with no write. |

## 4. Additional Phase 2.14 findings

| ID | Finding | Test | Verdict |
|---|---|---|---|
| N-1 | Residual overclaim in revised 2.13 architecture §3.2 ("guarantee … cannot be overwritten from any process") | Grep + 2.13 probes D5–D7 | **REJECTED** (that sentence); must say "through any supported harness interface (Tier 2)" |
| N-2 | Governance suite is not portable to POSIX: tests 10 and 22 "reset permissions" with `os.chmod(f, stat.S_IWRITE)`, which on POSIX is mode `0o200` (write-only), so the verifier cannot re-read the file → **ERROR** (non-root). On Windows the same call merely clears the read-only attribute. | REPRODUCED twice (`3a16ab94…`, `604fee45…`) | **ACCEPTED WITH LIMITATIONS** (test defect, not a security regression; Linux results are 22 ok / 3 skip / 2 error, not BLOCKED) |
| N-3 | `evidence_guard.py` edited at 18:19:55, **after** both Windows runs (18:17–18:18). Diff = three comment/docstring lines only; no functional change | `diff` 2.13→2.14 | **ACCEPTED** (disclosed; functionally the runs used equivalent code). The guard hash that ran (`8c249ca3…` content-equivalent) differs from the file now on disk (`3d5e8d22…`) |
| N-4 | Phase 2.13 deliverables were edited in place (not appended as an addendum) | mtimes, sizes | **ACCEPTED WITH LIMITATIONS** (disclosed in execution history; historical report hashes no longer match what was audited) |
| N-5 | Vector 27 is a no-op on Windows (`if sys.platform != "win32"`) — its `ok` there exercises nothing | Code review | Limitation |
| N-6 | `ResourceWarning: subprocess … still running` in Vectors 11 and 20 on Windows | Transcript | Low: possible leaked child processes from tests |

## 5. Regression (previously accepted work)

| Item | Test | Verdict |
|---|---|---|
| Cross-process gateway, TOCTOU, cgroup detection, trust pinning | `evidence_guard.py` functional code unchanged from 2.13 (comment-only diff); Linux suite vectors 3–8, 11–15, 23–27 pass | **ACCEPTED** (carried forward) |
| EQ/A02, C01, B01, RPT | `run_all_baseline_tests.py` and `run_sensitivity_matrix.py` byte-identical to 2.13 (which were byte-identical to 2.12) | carried forward: B01, RPT **ACCEPTED**; EQ/A02, C01 **ACCEPTED WITH LIMITATIONS** |
| Honest Linux BLOCKED | FS still BLOCKED on Linux; governance vectors 9 and 17 skip honestly; but 10 and 22 ERROR (N-2) | **ACCEPTED WITH LIMITATIONS** |
| Repository & databases | HEAD `d74f56dd`, `dev`, no locks, source aggregate `7c929481…`, 0 source files changed; `weather.sqlite` `1d767658…` ✓; `Intg_osdag.sqlite` **`25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91`** ✓ | **ACCEPTED** |

**Database hash note:** the brief's alternative value `…74b4f1` does **not** match the file or any prior audit record. The established baseline hash, recorded since Phase 2.4 and re-confirmed in every audit since, is `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91`. The file matches that value, so the brief's value looks like a transcription error.

## Overall

**CONDITIONALLY ACCEPTED** — see `PHASE_2_14_FINAL_INDEPENDENT_GATE_AUDIT.md` §9.
