# Phase 2.15 — Final Independent Gate Audit

**Auditor:** Claude (independent adversarial auditor)
**Audit date:** 2026-11-17 (UTC; audit closed 19:0x UTC)
**Subject:** Antigravity Phase 2.15 remediation (Check 5 hardening, security wording, Linux governance portability, Windows execution package)
**Baseline:** `source/OsdagBridge`, branch `dev`, HEAD `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`

---

## 1. Overall verdict

# CONDITIONALLY ACCEPTED — Phase 2 is NOT closed

The Phase 2.15 code remediation is accepted on the evidence I could independently reproduce: Linux governance now passes cleanly as non-root, as root, and as root under a genuine cgroup2 hierarchy, and a Linux analogue of the new Check 5 discriminates the main false-positive modes. Integrity is intact: all six official seals are valid and the production ledger is unchanged.

Phase 2 **cannot close** yet. Three gating conditions remain open:

| # | Condition | Status |
|---|---|---|
| G1 | A **separately initiated** independent Windows execution of the containment + governance suites | **BLOCKED / PENDING** — never executed. The `independent_run/` directory does not exist. |
| G2 | Defects in the independent execution package (`run_independent_validation.ps1`/`.bat`/README) fixed **before** G1 is run | **OPEN** — see F-5.x |
| G3 | Removal of the new Tier 3 overclaim introduced in `PHASE_2_15_SECURITY_WORDING_CORRECTIONS.md` line 50 | **OPEN** — see F-2.3 |

**Precise answer to the gate question.** The only remaining condition is **not** solely a separately initiated Windows execution. Two other things must be done first:

- **G2:** the package is defective enough that a clean run cannot be trusted, and may not complete on Windows PowerShell 5.1.
- **G3:** a documentation overclaim must be corrected.

Once G2 and G3 are fixed, the single remaining gating item is G1, which needs an independent Windows run that passes.

**Phase 3 is not authorized** by this audit.

---

## 2. Evidence classes (kept separate throughout)

| Class | What it covers |
|---|---|
| **A. Antigravity's own execution** | Windows transcripts `windows_containment_validation.txt` (`cb5c77b9…`, 6/6) and `governance_test_output.txt` (`7d84341a…`, 27 ok). Self-run by the remediating party. **Not independent.** |
| **B. My independent reproduction** | Linux only (cloud VM, Python 3.12.16): governance as non-root/root/root+cgroup2; Check 5 code executed verbatim against the harness `ProcessLifetimeJob` under genuine cgroup2 with 5 discrimination variants; on-device integrity + HMAC verification of all six seals. |
| **C. Code inspection** | Check 5 logic, tests 10/22 portability edits, the PowerShell/batch package, README, and the security wording. |
| **D. Unverified claims** | Any Windows-specific behaviour: Job Object kill-on-close, Windows ACL/read-only semantics, and whether the ps1 runs under PS 5.1 vs 7. |
| **E. Environmental blockers** | I have no independently controlled Windows session. Package creation does **not** satisfy independent execution. |

---

## 3. Section summaries

### §1 Check 5 delayed-writer validation — ACCEPTED with minor findings

- **Design.** The positive control (uncontained) must produce all four delayed writes (3/8/15/30 s). The contained run must show:
  - a start marker;
  - ≥1 live process in the job before termination;
  - termination before 3 s;
  - zero processes after termination;
  - no files at 4.5/9.5/16.5/31.5 s;
  - ≥32 s of observation.
- **Reproduction (B).** Under genuine cgroup2 the verbatim Check 5 code behaved as follows:
  - **Correctly failed:** "child exits early", "child never starts (no marker)" and "terminate disabled".
  - **Passed:** baseline.
  - **Accepted a pre-existing stale marker** (the "stale_marker" variant). This confirms the code-review finding that 5B never binds the marker to `cont_pid`.
- **Control creation times.** The control asserts existence only. It records no mtime or ordering, so it cannot show that each write happened at its scheduled time rather than all at the end. This is a low-severity weakness, because the milestone checks are time-gated.

### §2 Security wording — PARTIALLY ACCEPTED

- **Accepted.** `PHASE_2_13_SECURITY_ARCHITECTURE.md` §3.2 is now correctly limited to Tier 2, and an explicit Tier 3 warning is present.
- **Not accepted.** `PHASE_2_15_SECURITY_WORDING_CORRECTIONS.md:50` introduces a **new universal claim**: "Any such Tier 3 tampering breaks SHA-256 verification or seal verification". This is **false**. A same-user adversary holding the local key can remove a ledger entry, alter evidence, and re-seal, and the result verifies cleanly (demonstrated in 2.12 K10/K11/K13 and 2.13 D7).
- **Minor.** The same line says the layers "guarantee defense within Tier 2 (… unmediated writes …)", but unmediated writes are not a harness interface. The "immutable" wording in `evidence_guard.py` runtime messages is low severity.

### §3 Linux governance portability — ACCEPTED

| Run | Result |
|---|---|
| Non-root (uid 30033) | 24 ok, 3 honest skips (V9, V16, V17), 0 errors |
| Root on host | OK (skipped=3) |
| Root + genuine cgroup2 (private mount ns) | Ran 27, OK (skipped=1, only V16); V9 and V17 executed and passed |

Ledger byte-identical in every run; 0 leaked `osdagbridge_cg*` cgroups; no stray probe processes. The Phase 2.14 POSIX `S_IWRITE`/root defect in tests 10/22 is fixed.

### §4 Windows containment and governance — BLOCKED / PENDING (independent)

Antigravity's Windows transcripts (A) report 6/6 and 27/27, and they post-date the final script edits (runs at 18:42:51 and 18:43:38 UTC; edits at 18:39–18:41). They are internally consistent: control PID 35640, contained PID 28364, termination at 0.109 s, 32.00 s observation. They are, however, **self-executed** evidence. Independent Windows execution: **not performed**.

### §5 Independent execution package — NOT READY (defects; never executed)

A separate operator could launch it. The batch file `cd`s to the workspace and propagates ERRORLEVEL. But the run cannot be trusted as written:

| ID | Defect | Severity |
|---|---|---|
| F-5.1 | `$ErrorActionPreference="Stop"` combined with `2>&1` on a native command: on Windows PowerShell 5.1, the first stderr line (and `unittest -v` writes everything to stderr) becomes a terminating `NativeCommandError`. The governance suite would likely abort the script. Needs host confirmation. | High |
| F-5.2 | Silent fallback to `python` on PATH if the pinned conda interpreter is missing. The wrong interpreter can run unnoticed. | High |
| F-5.3 | Preflight only **prints** HEAD/status/DB/ledger hashes. Nothing is compared against expected values, and nothing fails. | High |
| F-5.4 | No postflight git/DB check. Only the ledger hash is re-checked. | Medium |
| F-5.5 | `OutputDir` is fixed, so a rerun **overwrites** the previous independent run's evidence. | Medium |
| F-5.6 | The manifest lacks harness-script hashes, per-suite start/end timestamps, timezone and interpreter version. Only a single end timestamp is recorded. | Medium |
| F-5.7 | The README claims the runner "Validates Git HEAD … working tree is clean". This is an overclaim (see F-5.3). | Medium |
| F-5.8 | Package never executed (no `independent_run/`). | Gate (G1) |

Positive points: non-zero exit if either suite fails or the ledger changes; transcript hashes are recorded; trust records are not modified by the script.

### §6 Regression and integrity — ACCEPTED (verified on device)

- HEAD is `ref: refs/heads/dev` → `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`. No `.git` lock files.
- Source aggregate: 282 files, `7c9294813b58fb84ecd965643daec240276747d1788b13187c0e0f46c52b024c` (unchanged). No `src` file modified after 18:25 UTC.
- `weather.sqlite` = `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98`.
- `Intg_osdag.sqlite` = `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91`.
- Production ledger `trusted_run_seals.json` = `5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1` (unchanged since 2.14).
- All six official seals pass. I computed HMAC-SHA256 with the key in place on the device (never copied), and each manifest SHA-256 matches. Every one of the 184 listed evidence files re-hashes correctly.
- No historical evidence files modified outside `phase_2_15/`.

---

## 4. Conditions to close Phase 2 (in order)

1. **G2:** Fix F-5.1 through F-5.7. For F-5.1, avoid `Stop` + `2>&1` on native commands, or run Python with stdout/stderr redirected to separate files via `Start-Process -RedirectStandardError` or `cmd /c`. Make preflight/postflight comparisons enforced and fatal. Fail hard on interpreter mismatch. Use a timestamped, `New-Item`-fails-if-exists output directory. Record harness-script hashes, interpreter path/version, and UTC start/end per suite.
2. **G3:** Correct `PHASE_2_15_SECURITY_WORDING_CORRECTIONS.md:50`. State that Tier 3 tampering is **not** reliably detected: a same-user re-seal with the local key verifies cleanly.
3. **G1:** A separately initiated Windows execution of the fixed package. It must be run by the user or another operator, **not** Antigravity, in a fresh session. The full output directory, manifest and transcripts must be preserved and then independently checked.
4. **Non-gating (recommended):** in 5B, assert that the marker content PID equals `cont_pid` and that the marker did not pre-exist. In 5A, record control-file mtimes and assert their ordering.

When 1–3 are satisfied with passing results, Phase 2 may close.
