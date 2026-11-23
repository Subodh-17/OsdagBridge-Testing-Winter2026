# Phase 2.15 — Final Remaining Risks

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge` on branch `dev` @ [`d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`](file:///F:/FOSSEE%20internship/source/OsdagBridge)  
**Controlling Audit:** Claude's Phase 2.14 Independent Gate Audit ([`reports/PHASE_2_14_FINAL_INDEPENDENT_GATE_AUDIT.md`](file:///F:/FOSSEE%20internship/reports/PHASE_2_14_FINAL_INDEPENDENT_GATE_AUDIT.md))  
**Date:** 2026-11-18  
**Status:** **ACTIVE RISK EVALUATION**  

---

These are harness-side and governance risks only; none implies an application source code modification. They are organized by gating impact on final independent gate acceptance.

---

## 1. Gating Risks (Pre-Requisite for Converting CONDITIONALLY ACCEPTED to FULL ACCEPTED)

### 1.1 Independent Operator Execution of Windows Validation Package
- **Risk Characterization:**  
  The native Windows Win32 Job Object containment suite (6 checks) and the 27-vector adversarial governance suite have passed with 100% success on the Windows host under Antigravity orchestration. However, under the independent audit governance rules, any test run conducted by the audited AI agent is classified as **ANTIGRAVITY CLAIM** and remains **BLOCKED** for independent reproduction until run outside of agent mediation.
- **Current State:**  
  An automated, deterministic **Independent Windows Execution Package** is staged in [`testing/evidence/phase_2_15/`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_15/) (`run_independent_validation.ps1` and `run_independent_validation.bat`).
- **Path to Closure:**  
  The project owner or the independent auditor (e.g., Claude via desktop computer-use) executes `run_independent_validation.bat` in a clean, non-agent terminal on the host machine. The package will automatically execute the suites, verify pre/post-run hashes, and write an immutable JSON execution manifest to `testing/evidence/phase_2_15/windows/independent_run/independent_run_manifest.json`.

---

## 2. Resolved Gating & Technical Risks (Closed in Phase 2.15)

### 2.1 Check 5 Writer Liveness and False-Negative Potential — CLOSED
- **Prior Finding:** Check 5 observed absence of delayed write files at 3s, 8s, 15s, and 30s, but liveness was printed rather than asserted, lacked probe start markers, and had no uncontained positive control run to prove the probe script was capable of creating files.
- **Phase 2.15 Resolution:** Check 5 was redesigned into two sequential phases:
  - **Part 5A (Uncontained Positive Control Run):** Spawns the identical probe script outside a Job Object; confirms line-1 start marker; verifies that all 4 target files (`w3.txt`, `w8.txt`, `w15.txt`, `w30.txt`) are created at measured timestamps ($t = 4.50\text{ s}, 9.50\text{ s}, 16.51\text{ s}, 31.50\text{ s}$).
  - **Part 5B (Contained Target Run):** Spawns contained probe; verifies start marker; asserts child liveness (`poll() is None`) and Job Object accounting (`ActiveProcesses >= 1`); enforces termination at $t = 0.11\text{ s} < 3.0\text{ s}$; observes full 32.0s horizon and confirms **0 files created**.

### 2.2 Security Architecture §3.2 Scope Boundary Overclaim — CLOSED
- **Prior Finding:** `PHASE_2_13_SECURITY_ARCHITECTURE.md` §3.2 claimed that the defense layers "guarantee sealed evidence cannot be overwritten from any process".
- **Phase 2.15 Resolution:** Scoped strictly to Tier 2 interfaces ("guarantee sealed evidence cannot be overwritten through any supported harness interface (Tier 2)"). Added explicit `[!NOTE]` alert detailing that same-user scripts (Tier 3) with full discretionary filesystem permissions can clear read-only attributes or recalculate HMACs, which is outside the prevention guarantees of this local harness; same-user re-sealing using the local device key cannot be reliably detected by local verification alone.

### 2.3 POSIX Portability of Evidence Governance Suite (Vectors 10 and 22) — CLOSED
- **Prior Finding:** On Linux non-root environments, `test_10` and `test_22` produced `ERROR` because `os.chmod(f, stat.S_IWRITE)` set mode `0o200` (write-only without read), causing subsequent `verify_manifest_integrity` reads to fail with `PermissionError`.
- **Phase 2.15 Resolution:** Replaced `stat.S_IWRITE` with portable combined mask `RW_MODE = (stat.S_IRUSR | stat.S_IWUSR)` (`0o600`) and `RO_MODE = stat.S_IRUSR` (`0o400`). Handled POSIX root DAC bypass in `test_10`. Added child subprocess reaping to prevent `ResourceWarning` messages.

---

## 3. Non-Gating Inherent Architectural Boundaries

### 3.1 Same-User Tampering Boundary (Tier 3 Threat Model)
- **Status:** By design, local symmetric HMAC sealing (`seal_signing_key.bin`) and filesystem read-only attributes do not constitute an impenetrable boundary against a deliberate adversarial process executing under the same OS user identity (`Subodh`). Same-user access to the local signing key can permit deletion or alteration of ledger entries followed by re-sealing, which is not prevented or detected by local verification mechanisms. Tier 3 same-user malicious tampering is outside the prevention guarantees of this local harness. Stronger non-repudiation requires an independent external authority or a separately controlled trust boundary (Tier 4, not implemented).

### 3.2 Linux Environment Process Containment (FS BLOCKED)
- **Status:** Standard Linux user sessions without cgroup v2 delegation or root privileges cannot prevent detached background grandchildren or `setsid()` process escapes. Consequently, the FS sensitivity test remains honestly classified as **BLOCKED on Linux** (while fully passing on Windows NT Job Objects).

### 3.3 Engineering Tolerances Carried Forward
- **Status:** Historical baseline test tolerances accepted in earlier phases remain in effect:
  - C01: 0.8% allowable variance band and embedded section modulus $Z_b$.
  - A02: 1.0% component tolerance band.
  - EQ / A02: Barrier width derived from geometric constant.
  These reflect known domain modeling tolerances in structural engineering calculations.

---

## 4. Summary

With the completion of Check 5 positive control verification, security wording precision, and POSIX permission portability, the specific findings identified in Phase 2.14 have been remediated in the harness. The remaining requirement is the empirical execution of the staged Windows package by an independent operator outside the AI agent process tree.
