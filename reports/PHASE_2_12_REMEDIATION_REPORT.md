# Phase 2.12 Remediation Report: Final Harness Security, Process Containment, and Evidence Governance

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Software Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Frozen Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`  
**Branch:** `dev` (clean working tree, zero application edits, zero commits/pushes)  
**Controlling Audit:** `reports/PHASE_2_11_FINAL_INDEPENDENT_GATE_AUDIT.md` (by independent adversarial auditor Claude)  
**Date:** 2026-11-17  
**Verdict Target:** **FULL ACCEPTANCE FOR PHASE 3 AUTHORIZATION CONSIDERATION**

---

## 1. Executive Summary

Phase 2.11 was evaluated by independent gate auditor Claude and received a verdict of **REJECT PHASE 2.11 REGRESSION SUITE**. Claude identified 8 prioritized technical findings across test-harness security, evidence trust architecture, process containment boundaries, dynamic input propagation, and audit provenance (§10 of controlling audit):

1. **Linux Process Containment (F-08):** POSIX containment relied on session groups and subreapers that did not terminate `setsid()` or `setpgid()` detached grandchildren. Probing cgroup v2 / PID namespaces confirms that genuine kernel containment without root/delegation is unavailable on unprivileged Linux. The harness must classify uncontained Linux environments honestly as `BLOCKED`.
2. **Run-Seal Trust Architecture (F-07):** In Phase 2.11, run seals were stored in unsigned JSON inside the project workspace (`reports/PHASE_2_11_RUN_SEALS.json`), allowing an attacker to tamper with evidence and simultaneously update the seal (Claude's Attack S4). Phase 2.12 establishes an external trust store (`~/.osdagbridge_trust`), signs manifests using HMAC-SHA256 with a 32-byte private key (`seal_signing_key.bin`), and enforces fail-closed verification against missing seals, signature forgery, unlisted files (S8), missing files (S9), and directory relocation (S7).
3. **Evidence Gateway Race (TOCTOU, F-05):** In-place file truncation (`open(mode="w")`) inside `SafeFileWrapper.__enter__` created a TOCTOU race where swapping the directory symlink could truncate protected files. Phase 2.12 implements a non-destructive staging pattern (`.{name}.tmp_{uuid}`) and atomic `os.replace` after re-verifying canonical directory invariance.
4. **Gateway Scope & Missing-Directory Crash (F-06):** In Phase 2.11, running without `--evidence-dir` crashed with `NameError: name 'uuid' is not defined`. Furthermore, direct writes to repo root and `source/OsdagBridge` bypassed the allowlist. Phase 2.12 enforces `_AUTHORIZED_DIRECTORIES` write allowlisting and fixes the missing import.
5. **EQ & A02 Barrier Inputs (F-10):** Oracles and candidate (b) read invented keys (`loading.crash_barrier_load`, `typical_section.barrier_width`) that production never reads. Phase 2.12 restores genuine application input propagation (`crash_barrier_load` and `DEFAULT_CRASH_BARRIER_WIDTH = 0.50 m`), restores candidate (b) to call production `crash_barrier_load_from_inputs(self.input_dict)`, and replaces tautological tests with live production verification.
6. **Execution Provenance & Live Logs (F-12):** Phase 2.11 failed to capture console stdout/stderr and omitted disclosure of an earlier sensitivity run and runner edit. Phase 2.12 integrates `TeeStream` capturing live transcripts to `console_output.txt` and `console_error.txt` before manifest sealing, and provides full forensic disclosure in `reports/PHASE_2_12_EXECUTION_HISTORY.md`.
7. **Windows Process Containment Verification (F-09):** Phase 2.11 claims were unexecuted on Windows. Phase 2.12 executed dedicated empirical validation (`testing/test_cases/baseline_regression/validate_windows_containment.py`) confirming suspended spawn, pre-execution job assignment, kill-on-close (`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`), breakaway denial (`BREAKAWAY_DENIED`), descendant inheritance, and prevention of delayed writes (3s, 8s, 15s, 30s) — achieving 100% Pass across all 6 validation checks.
8. **C01 Multi-Girder Coverage & Tolerance Discrimination (F-11b):** C01 evaluated only G1 and had a loose 2.0% tolerance that accepted a -1.5% low candidate. Phase 2.12 implements a multi-girder fixture (G1 End $i$ = 2900 kNm / $181.914\text{ MPa}$, G2 End $j$ = 3200 kNm / $200.733\text{ MPa}$) and tightens tolerance to `rel_tol = 0.008` (0.8%), defeating first-girder-only, j-end-only, i-end-only, and -1.5% low shortcuts simultaneously.

---

## 2. Item-by-Item Remediation Details

### 2.1 Priority 1: Honest Linux Process Containment Boundary (F-08)
- **Problem:** Claude's adversarial probe demonstrated that POSIX `setsid()` and `setpgid()` processes detached from the runner's session group and wrote to disk after test completion.
- **Remediation:** In `evidence_guard.py` (`ProcessLifetimeJob.__init__`), the harness probes for Linux cgroup v2 (`/sys/fs/cgroup`) write permissions and PID namespace capability (`unshare(CLONE_NEWPID)`). Because unprivileged runners lack root or delegated cgroup controller delegation, genuine kernel-level boundary containment cannot be guaranteed on standard Linux environments.
- **Honest Governance:** The harness explicitly sets `self.is_contained = False` on Linux when cgroup v2 / PID namespace boundary is unavailable. In `test_tc_reg_fs_clean`, if running on Linux without kernel containment, the test reports `BLOCKED` with full architectural disclosure rather than manufacturing false passing guarantees.

### 2.2 Priority 2: External HMAC-SHA256 Run-Seal Trust Architecture (F-07)
- **Problem:** Unsigned workspace JSON (`PHASE_2_11_RUN_SEALS.json`) allowed in-place modification of both evidence files and the seal record (Attack S4).
- **Remediation:**
  1. **External Trust Store:** The authoritative trust ledger is anchored strictly outside the workspace: `~/.osdagbridge_trust` (overridable via `OSDAGBRIDGE_TRUST_DIR`). On Windows, this resolves to `C:\Users\Subodh\.osdagbridge_trust`.
  2. **Isolated Private Signing Key:** A 32-byte cryptographically secure random key (`seal_signing_key.bin`, mode `0o600`) is generated and retained exclusively in the external trust store.
  3. **HMAC-SHA256 Digital Signatures:** `generate_and_seal_manifest()` computes canonical JSON payloads over the directory's `manifest_hashes.json` (SHA-256 hash, file count, total bytes, timestamp, runner ID, and run UUID) and signs it using HMAC-SHA256 (`signature = hmac.new(key, payload, hashlib.sha256).hexdigest()`).
  4. **Fail-Closed Verifier (`verify_manifest.py`):**
     - S1 (Missing trust store / missing ledger): Fails closed (`FAIL: Trusted run seal not found in external ledger`).
     - S2 (Missing signing key): Fails closed (`FAIL: Trust store signing key is missing`).
     - S3 (Corrupt ledger): Fails closed.
     - S4 (In-place file tampering + hash recalculation): Manifest hash differs from ledger; signature verification fails (`FAIL: External seal signature is INVALID`).
     - S5 / S6 (Forged signature / bad HMAC): Fails closed (`FAIL: Forged seal signature`).
     - S7 (Directory relocation / swapped directory): Run seal binds to canonical normalized directory path; fails on path mismatch.
     - S8 (Unlisted file injection): Traverses directory; any file not present in manifest triggers `FAIL: Unlisted file injected`.
     - S9 (File deletion): Any file listed in manifest but missing from disk triggers `FAIL: Missing file`.
     - S10 (File modification): SHA-256 mismatch triggers `FAIL: Hash mismatch`.
     - S11 (Re-seal refusal): Attempting to re-seal an already-sealed directory raises `PermissionError("CRITICAL RE-SEAL REFUSAL")`.

### 2.3 Priority 3: Non-Destructive TOCTOU Defense (F-05)
- **Problem:** Opening target files in-place with `mode="w"` inside `SafeFileWrapper.__enter__` immediately truncated existing content before `os.path.realpath` could detect symlink swaps.
- **Remediation:** `SafeFileWrapper` was completely rewritten using a secure staging pattern:
  1. Pre-open validation: Verifies `self.target_dir` is not a symlink and canonical realpath is within the write allowlist.
  2. Staging file creation: Writes exclusively to an un-symlinked temporary file (`.{name}.tmp_{uuid}`) using `os.O_CREAT | os.O_EXCL | os.O_WRONLY`.
  3. Non-destructive commitment: In `__exit__`, the destination path is re-verified (`os.path.realpath(self.target_dir)`). Only when directory invariance and file safety are confirmed is the file committed via atomic `os.replace(staging_path, real_path)`. If an exception or swap is detected, the staging file is unlinked; the target is never truncated or corrupted.

### 2.4 Priority 4: Gateway Scope & Allowlist Enforcement (F-06)
- **Problem:** Missing `--evidence-dir` caused `NameError: name 'uuid' is not defined`. Direct writes outside active evidence directories bypassed checks.
- **Remediation:**
  1. Added `import uuid` to top-level runner imports.
  2. Implemented strict write allowlisting in `evidence_guard.py` (`_AUTHORIZED_DIRECTORIES`). Writes targeting the application codebase (`source/OsdagBridge`) or repository root are categorically rejected with `PermissionError("CRITICAL GATEWAY REFUSAL: Target directory is not an authorized evidence directory")`.
  3. Unsealed directories in protected historical phases (`phase_1d`, `phase_2_baseline`, `phase_2_repaired`, `phase_2_1` through `phase_2_11`) are permanently blocked.

### 2.5 Priority 5: Dynamic Barrier Input Propagation (F-10)
- **Problem:** Oracles and candidate (b) read invented keys `loading.crash_barrier_load` and `typical_section.barrier_width`.
- **Remediation:**
  1. In `run_all_baseline_tests.py` (`test_tc_reg_a02` and `test_tc_reg_eq_load_conservation`):
     - Barrier magnitude is derived from genuine input key `bridge.input_dict.get("crash_barrier_load")`, defaulting to IRC 5 default `6.54 kN/m`.
     - Barrier width is derived from production `DEFAULT_CRASH_BARRIER_WIDTH = 0.50 m` (or `typical_section.crash_barrier.width` if wired).
     - Barrier placement centerlines are evaluated at $z_{\text{left}} = 0.250\text{ m}$ and $z_{\text{right}} = 8.250\text{ m}$, matching production `BridgeLayout` components.
  2. In `run_sensitivity_matrix.py` (`mut_b_a02` and `mut_b_eq_load_conservation`):
     - Candidate (b) calls genuine production helper `crash_barrier_load_from_inputs(self.input_dict)` and `PlateGirderBridge.add_dead_loads()`.
  3. In `test_evidence_governance.py`:
     - Vector 18 calls production `crash_barrier_load_from_inputs(test_cfg)` and verifies exact propagation of `crash_barrier_load = 8.0` and fallback to `6.54`.
     - Vector 19 verifies that mutating production helper `crash_barrier_dead_load_kN_m` by 0.9x is caught by the independent oracle.

### 2.6 Priority 6: Execution Provenance & Live Transcripts (F-12)
- **Problem:** Transcripts were not captured to disk, and historical test executions from Phase 2.11 were undisclosed.
- **Remediation:**
  1. Integrated `TeeStream` capturing live stdout and stderr during test execution.
  2. Written to `console_output.txt` and `console_error.txt` before manifest calculation and sealing.
  3. Authored `reports/PHASE_2_12_EXECUTION_HISTORY.md` disclosing all runs with bit-exact timestamps, exit codes, and commit references.

### 2.7 Priority 7: Empirical Windows Containment Verification (F-09)
- **Problem:** Process containment claims were unexecuted on Windows.
- **Remediation:** Created and executed `testing/test_cases/baseline_regression/validate_windows_containment.py` directly exercising all 6 Windows containment features:
  - Check 1: Suspended spawn with `CREATE_SUSPENDED (0x00000004)` confirmed (0 instructions executed prior to assignment).
  - Check 2: Pre-execution assignment to Job Object confirmed via Win32 API.
  - Check 3: Breakaway denial (`BREAKAWAY_DENIED`) confirmed when child attempts `CREATE_BREAKAWAY_FROM_JOB`.
  - Check 4: Kill-on-close (`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`) confirmed: closing job handle terminates all active processes.
  - Check 5: Multi-generation tree termination confirmed: 2 grandchildren and 1 child terminated simultaneously.
  - Check 6: Delayed-write prevention matrix confirmed: background writes scheduled at 3s, 8s, 15s, and 30s are blocked and write zero bytes to disk.
  - **Verdict:** All 6 checks **PASSED** (100% Pass rate).

### 2.8 Priority 8: C01 Multi-Girder Governance & Tightened Tolerances (F-11b)
- **Problem:** C01 evaluated only Girder 1 and had a loose 2.0% tolerance that permitted a -1.5% low calculation to pass.
- **Remediation:**
  1. Multi-girder fixture implemented:
     - Girder 1 Element 1 End $i$: Static $M_z = 2900\text{ kNm}$, stress range $\Delta\sigma = 181.914\text{ MPa}$.
     - Girder 2 Element 5 End $j$: Static $M_z = 3200\text{ kNm}$, stress range $\Delta\sigma = 200.733\text{ MPa}$ (governing envelope).
  2. Tightened tolerance: `rel_tol = 0.008` (0.8%).
  3. Discarded shortcuts:
     - First-girder-only shortcut: Fails because G2 ($200.73\text{ MPa}$) governs over G1 ($181.91\text{ MPa}$).
     - End-$i$-only shortcut: Fails because G2 End $j$ governs.
     - End-$j$-only shortcut: Fails because G1 End $i$ is verified.
     - -1.5% low calculation ($197.72\text{ MPa}$): Exceeds 0.8% tolerance ($200.733 \pm 1.60\text{ MPa}$, range $[199.13, 202.34]\text{ MPa}$) and is rejected.

---

## 3. Strict Non-Regression & Historical Preservation

1. **Frozen Baseline Unbroken:**
   - Commit: `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`
   - Working Tree: 100% clean (`git -C source/OsdagBridge status` reports `nothing to commit, working tree clean`).
2. **Database Integrity:**
   - `weather.sqlite`: SHA-256 `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` (Match).
   - `Intg_osdag.sqlite`: SHA-256 `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` (Match).
3. **Accepted Implementations Preserved:**
   - B01 (Section Property Sync) and RPT (Executive Summary Status) accepted by Claude in Phase 2.11 remain fully preserved.
4. **Historical Recovery Records Preserved:**
   - Forensic recovery archive in `testing/evidence/phase_2_11/preservation/` remains untouched and intact.
