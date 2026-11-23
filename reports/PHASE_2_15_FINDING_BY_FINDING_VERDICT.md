# Phase 2.15 — Finding-by-Finding Verdict

Evidence key:

- **A** = Antigravity self-execution
- **B** = my independent reproduction (Linux)
- **C** = code inspection
- **D** = unverified claim
- **E** = environmental blocker

| ID | Item | Claim (Antigravity) | Evidence | Verdict |
|---|---|---|---|---|
| F-1.1 | Check 5A positive control proves the probe writes when uncontained | Control produces w3/w8/w15/w30 | A (Windows), B (Linux: all 4 present at 4.5/9.5/16.5/31.5 s) | **ACCEPTED** |
| F-1.2 | Check 5B contained run proves termination prevents all later writes | 0 files, 0 procs, ≥32 s observation | A, B (baseline passes; `no_termination` variant correctly FAILS with all 4 files written) | **ACCEPTED** (Linux mechanism); Windows Job Object = **D** |
| F-1.3 | 5B rejects a child that exits before termination | alive + count ≥1 assertions | B (`premature_exit` → contained_passed=False) | **ACCEPTED** |
| F-1.4 | 5B rejects a child that never started | marker required | B (`no_marker` → False) | **ACCEPTED** |
| F-1.5 | Marker proves *this* child started | "Start marker verified" | B (`stale_marker` → **passes**); C (PID never compared to `cont_pid`) | **FINDING — Low.** Marker not bound to process identity. |
| F-1.6 | Control creation times / ordering | not claimed | C (existence only, no mtime) | **FINDING — Low.** Recommend recording mtimes. |
| F-1.7 | Final recheck after observation padding | implied | C (no re-check of all 4 paths after `rem_obs` sleep) | **FINDING — Low** |
| F-2.1 | §3.2 limited to Tier 2 | yes | C (`PHASE_2_13_SECURITY_ARCHITECTURE.md`, `2b922670…`) | **ACCEPTED** |
| F-2.2 | Explicit Tier 3 warning | yes | C (line 114) | **ACCEPTED** |
| F-2.3 | No surviving universal claims | yes | C: `PHASE_2_15_SECURITY_WORDING_CORRECTIONS.md:50` "Any such Tier 3 tampering breaks SHA-256 verification or seal verification" is false (same-user re-seal verifies; 2.12 K10/K11/K13, 2.13 D7) | **REJECTED — Medium. Gate G3.** |
| F-2.4 | "guarantee defense within Tier 2 (… unmediated writes …)" | — | C | **FINDING — Low** (unmediated writes ≠ harness interface) |
| F-2.5 | "immutable" in `evidence_guard.py` error strings | — | C | **FINDING — Low** (runtime message wording) |
| F-3.1 | Tests 10/22 portable to POSIX non-root | yes | B (non-root: 24 ok / 3 skip / 0 err) | **ACCEPTED** |
| F-3.2 | Tests 10/22 correct as root | yes (root skips read-only append assertion) | B (root: OK skipped=3) | **ACCEPTED** |
| F-3.3 | Vectors 9/17 under real cgroup2 | — | B (root+cgroup2: OK skipped=1; V9 and V17 executed and passed) | **ACCEPTED** |
| F-3.4 | Subprocess / cgroup cleanup | yes | B (0 leaked cgroups, no stray probes) | **ACCEPTED** |
| F-3.5 | Production ledger isolation during tests | yes | B (seeded ledger byte-identical in all runs) | **ACCEPTED** |
| F-4.1 | Windows containment 6/6 | yes | A only (`cb5c77b9…`, run after edits) | **NOT INDEPENDENTLY VERIFIED** (E) |
| F-4.2 | Windows governance 27/27 | yes | A only (`7d84341a…`) | **NOT INDEPENDENTLY VERIFIED** (E) |
| F-4.3 | Independent Windows execution | package provided | No `independent_run/` exists | **BLOCKED / PENDING — Gate G1** |
| F-5.1 | ps1 robust on PS 5.1 | implied | C: `Stop` + `2>&1` on native stderr → `NativeCommandError` | **FINDING — High** (needs host confirmation) |
| F-5.2 | Correct interpreter enforced | implied | C: silent fallback to `python` on PATH | **FINDING — High** |
| F-5.3 | Preflight validates HEAD/clean tree/DBs | README says yes | C: values printed, never compared or enforced | **REJECTED — High** (README overclaim, F-5.7) |
| F-5.4 | Postflight git/DB | — | C: ledger only | **FINDING — Medium** |
| F-5.5 | No overwrite of prior evidence | — | C: fixed `OutputDir` | **FINDING — Medium** |
| F-5.6 | Manifest completeness | — | C: no harness hashes, no per-suite timestamps/TZ/interpreter | **FINDING — Medium** |
| F-5.7 | README accuracy | — | C | **FINDING — Medium** |
| F-5.8 | Exit code / failure propagation | yes | C: exits 1 on suite fail or ledger change; .bat propagates ERRORLEVEL | **ACCEPTED** (subject to F-5.1) |
| F-5.9 | Package does not modify trust records | yes | C | **ACCEPTED** |
| F-6.1 | HEAD/branch/clean refs | — | B (device): `dev` @ `d74f56dd…`, no locks | **ACCEPTED** |
| F-6.2 | Source unchanged | — | B: aggregate 282 / `7c929481…` | **ACCEPTED** |
| F-6.3 | DB hashes | — | B: `1d767658…`, `25f97857…` | **ACCEPTED** |
| F-6.4 | Six official seals valid | — | B: HMAC ✓, manifest ✓, 184/184 files ✓ | **ACCEPTED** |
| F-6.5 | Production ledger unchanged | — | B: `5a9b9273…` | **ACCEPTED** |
| F-6.6 | Historical evidence untouched | — | B: no files outside `phase_2_15/` newer than 18:25 UTC | **ACCEPTED** |

**Tally.**

- ACCEPTED: 22
- REJECTED: 2 — F-2.3 (gating), F-5.3
- Findings: 11 — High 2, Medium 4, Low 5
- BLOCKED / not independently verified: 3 — F-4.1, F-4.2, F-4.3 (gating)
