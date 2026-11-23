# Phase 2.15 — Windows Containment Check 5 Hardening & Positive Control

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Baseline:** Branch `dev` @ [`d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`](file:///F:/FOSSEE%20internship/source/OsdagBridge)  
**Controlling Audit:** Claude's Phase 2.14 Independent Gate Audit ([`reports/PHASE_2_14_FINAL_INDEPENDENT_GATE_AUDIT.md`](file:///F:/FOSSEE%20internship/reports/PHASE_2_14_FINAL_INDEPENDENT_GATE_AUDIT.md))  
**Date:** 2026-11-18 (UTC / IST)  
**Status:** **CLOSED / VERIFIED**

---

## 1. Executive Summary & Audit Context

In the Phase 2.14 gate audit (§2 and §7), Claude identified that Check 5 in `validate_windows_containment.py` had a design limitation:
> "Check 5 still cannot fully exclude a writer that never started. There is no asserted liveness, no start marker, no positive control and no measured timestamps... Close by: assert `cnt >= 1`; have the probe write a start marker; add an uncontained positive-control run; record `time.monotonic()` for each observation."

In Phase 2.15, Check 5 was redesigned and hardened to establish complete empirical proof of both writer liveness and process containment:
1. **Uncontained Positive Control Run (Part 5A):** Proves that the multi-stage delayed-write mechanism actually works as scheduled when containment is absent.
2. **Contained Job Object Run (Part 5B):** Emits an explicit start marker, asserts writer process liveness and Job accounting before termination, terminates strictly before scheduled write milestones ($t_{\text{term}} < 3.0\text{ s}$), and observes a full 32-second post-termination observation horizon using high-resolution monotonic timestamps.
3. **Fail-Closed Verification:** If any writer fails to emit a start marker, exits prematurely, or fails to create (control) or block (contained) files, the check immediately reports **FAIL**.

---

## 2. Hardened Architecture of Check 5

### 2.1 Architecture Diagram

```
+---------------------------------------------------------------------------------------------------+
| CHECK 5: DELAYED WRITES PREVENTION & UNCONTAINED CONTROL VALIDATION                                |
+---------------------------------------------------------------------------------------------------+
                                                  |
           +--------------------------------------+--------------------------------------+
           |                                                                             |
           v                                                                             v
+-------------------------------------------------------+  +-------------------------------------------------------+
| PART 5A: UNCONTAINED CONTROL RUN                      |  | PART 5B: CONTAINED WIN32 JOB OBJECT RUN               |
| - Directory: td_control (disposable)                  |  | - Directory: td_contained (disposable, isolated)      |
| - Probe: ctrl_delayed_probe.py                        |  | - Probe: cont_delayed_probe.py                        |
| - Line 1: Emit ctrl_start_marker.txt (PID, timestamp) |  | - Line 1: Emit cont_start_marker.txt (PID, timestamp) |
| - Scheduled: 3s (w3), 8s (w8), 15s (w15), 30s (w30)   |  | - Scheduled: 3s (w3), 8s (w8), 15s (w15), 30s (w30)   |
| - Execution: subprocess.Popen (uncontained)           |  | - Execution: job.spawn (Win32 Job Object bound)       |
| - Verification:                                       |  | - Verification:                                       |
|   1. Assert start marker exists                       |  |   1. Assert start marker exists                       |
|   2. Assert PID alive                                 |  |   2. Assert job.get_process_count() >= 1              |
|   3. Milestone t=4.5s:  exists(w3.txt)  == True       |  |   3. Assert proc.poll() is None (alive before term)   |
|   4. Milestone t=9.5s:  exists(w8.txt)  == True       |  |   4. Terminate Job Object at t=0.109s (< 3.0s)        |
|   5. Milestone t=16.5s: exists(w15.txt) == True       |  |   5. Assert all processes dead (count == 0)           |
|   6. Milestone t=31.5s: exists(w30.txt) == True       |  |   6. Observe full 32s horizon with monotonic clocks:  |
| - Result: PASS (Proves probe works without Job)       |  |      - Milestone t=4.5s:  exists(w3.txt)  == False    |
+-------------------------------------------------------+  |      - Milestone t=9.5s:  exists(w8.txt)  == False    |
                                                           |      - Milestone t=16.5s: exists(w15.txt) == False    |
                                                           |      - Milestone t=31.5s: exists(w30.txt) == False    |
                                                           |      - Post-term observation: 32.00s (>= 32.0s)        |
                                                           | - Result: PASS (All 4 delayed writes prevented)       |
                                                           +-------------------------------------------------------+
                                                  |
                                                  v
                     +---------------------------------------------------------+
                     | OVERALL CHECK 5 VERDICT: PASS                           |
                     | Both Part 5A (Control) AND Part 5B (Contained) Verified |
                     +---------------------------------------------------------+
```

---

## 3. Step-by-Step Implementation Details

### 3.1 Uncontained Positive Control Run (Part 5A)
In `testing/test_cases/baseline_regression/validate_windows_containment.py`:
- **Probe Script:** Emits an explicit file marker `ctrl_start_marker.txt` on line 1 containing `STARTED: PID={os.getpid()}, TIME={time.time()}` and immediately calls `f.flush()`.
- **Liveness Confirmation:** The parent polls for up to 3.0s for the marker file. If missing, it immediately flags `ctrl_passed = False` and aborts.
- **Measured Milestones:** Using `time.monotonic()`, the parent measures elapsed time from process spawn and checks output file existence at exact milestones:
  - Milestone $t = 4.50\text{ s}$: verifies `exists(w3.txt) == True` (written at 3.0s).
  - Milestone $t = 9.50\text{ s}$: verifies `exists(w8.txt) == True` (written at $3+5 = 8.0\text{ s}$).
  - Milestone $t = 16.51\text{ s}$: verifies `exists(w15.txt) == True` (written at $8+7 = 15.0\text{ s}$).
  - Milestone $t = 31.50\text{ s}$: verifies `exists(w30.txt) == True` (written at $15+15 = 30.0\text{ s}$).
- **Outcome:** The uncontained writer successfully created all 4 files with expected contents `'3s'`, `'8s'`, `'15s'`, `'30s'`, and exited with code `0`.

### 3.2 Contained Win32 Job Object Run (Part 5B)
- **Isolated Directory:** Created in a distinct temporary directory `td_contained`.
- **Probe Script:** Identical delayed-write structure with start marker `cont_start_marker.txt`.
- **Spawn & Pre-Termination Assertion:**
  - Spawned via `job.spawn([PYTHON_EXE, "-u", cont_probe_py])`.
  - Parent polls for `cont_start_marker.txt` (verified within 0.1s).
  - **Liveness Asserted:** Parent asserts `job.get_process_count() >= 1` and `p.poll() is None`.
- **Termination Strictly Prior to Milestones:**
  - Termination triggered at measured $t_{\text{term}} = 0.109\text{ s}$ from spawn ($< 3.0\text{ s}$).
  - `job.terminate()` invoked; `wait_for_job_completion(3.0)` confirmed all dead; `get_process_count() == 0`.
- **Full 32-Second Observation Horizon:**
  - Checkpoint 1 ($t = 4.50\text{ s}$ from spawn): `exists(w3.txt) == False`.
  - Checkpoint 2 ($t = 9.50\text{ s}$ from spawn): `exists(w8.txt) == False`.
  - Checkpoint 3 ($t = 16.51\text{ s}$ from spawn): `exists(w15.txt) == False`.
  - Checkpoint 4 ($t = 31.50\text{ s}$ from spawn): `exists(w30.txt) == False`.
  - Total post-termination observation time measured via `time.monotonic()`: **32.00s** ($\ge 32.0\text{ s}$).
- **Outcome:** Zero delayed output files created.

---

## 4. Empirical Windows Execution Transcript

Executed natively on Windows 11 host (AMD64 / Python 3.12.16):

```
[CHECK 5] Delayed Writes Prevention at 3s, 8s, 15s, and 30s (with Uncontained Control)...
  [5A] Executing Uncontained Positive Control Run (Proves delayed writes succeed without containment)...
  [5A] Control writer PID 35640 started. Marker: 'STARTED: PID=35640, TIME=1794940907.7152827'
  [5A t=4.50s] Control 3s write:  exists=True (Expected: True)
  [5A t=9.50s] Control 8s write:  exists=True (Expected: True)
  [5A t=16.51s] Control 15s write: exists=True (Expected: True)
  [5A t=31.50s] Control 30s write: exists=True (Expected: True)
  [5A] Control Run Result: PASS (All 4 delayed files created)
  [5B] Executing Contained Run Under Win32 Job Object...
  [5B] Contained writer spawned: PID 28364
  [5B] Start marker verified: True
  [5B] Active processes in Job before termination: 1 (Assert >= 1)
  [5B] Process alive before termination: True (Assert True)
  [5B] Termination triggered at t = 0.109s (Scheduled targets: 3s, 8s, 15s, 30s)
  [5B] Commencing full 32-second post-termination observation horizon...
  [5B t=4.50s] Check 3s write:  exists=False (Expected: False)
  [5B t=9.50s] Check 8s write:  exists=False (Expected: False)
  [5B t=16.51s] Check 15s write: exists=False (Expected: False)
  [5B t=31.50s] Check 30s write: exists=False (Expected: False)
  [5B] Total post-termination observation time: 32.00s (Assert >= 32.0s)
  [5B] Contained Run Result: PASS (All delayed writes prevented)
  Check 5 Final Result: PASS
```

---

## 5. Conclusion

Finding 2 of Claude's Phase 2.14 Independent Gate Audit is **CLOSED**:
- Writer start markers are explicitly written, flushed, and verified before termination.
- Writer process liveness and Job Object accounting are asserted (`cnt >= 1`, `poll() is None`).
- An uncontained positive control run demonstrates that the multi-stage delayed-write mechanism functions as designed when containment is absent.
- The 32-second post-termination observation horizon is fully observed with high-resolution monotonic timestamps.
- Check 5 passes only when both control (positive) and contained (negative) runs succeed.
