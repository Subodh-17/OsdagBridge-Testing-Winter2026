# Phase 2.14 — Verification Test Results & Gate Audit Matrix

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge` on branch `dev` @ [`d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`](file:///F:/FOSSEE%20internship/source/OsdagBridge)  
**Controlling Audit:** Claude's Phase 2.13 Independent Gate Audit ([`reports/PHASE_2_13_FINAL_INDEPENDENT_GATE_AUDIT.md`](file:///F:/FOSSEE%20internship/reports/PHASE_2_13_FINAL_INDEPENDENT_GATE_AUDIT.md))  
**Date:** 2026-11-17 (UTC / IST)  
**Overall Status:** **ALL 3 CONDITIONS SATISFIED** (Awaiting Independent Audit Review)

---

## 1. Condition-by-Condition Audit Matrix

| Audit Condition | Description | Required Verification | Phase 2.14 Empirical Outcome | Condition Status |
| :--- | :--- | :--- | :--- | :---: |
| **Condition 1** | Actual Windows Empirical Validation | 1. Run 6 Job Object checks on real Windows host observing full 32s horizon.<br>2. Run 27 governance attack vectors on Windows.<br>3. Capture live transcripts without recycling Phase 2.13 logs. | 1. 6 / 6 checks PASSED in 35.73s (observed 3s, 8s, 15s, 30s milestones).<br>2. 27 / 27 vectors PASSED (0 skips, 0 failures) in 17.60s.<br>3. Transcripts preserved in `testing/evidence/phase_2_14/windows/`. | **SATISFIED** |
| **Condition 2** | Correct Security Claims | 1. Inspect Phase 2.13 reports and code comments.<br>2. Remove "kernel-level", "tamper-proof", "complete non-repudiation", and independent trust boundary claims for `S_IREAD`.<br>3. Maintain 4-tier threat model distinctions. | 1. Audited all reports and code.<br>2. Corrected 7 overstated descriptions in `REMEDIATION_REPORT`, `SECURITY_ARCHITECTURE`, and `evidence_guard.py`.<br>3. Preserved honest Tier 3 disclaimers. | **SATISFIED** |
| **Condition 3** | Isolate Governance Tests from Production Trust | 1. Forensically investigate stray entries in `trusted_run_seals.json`.<br>2. Conclusively classify origin.<br>3. Non-destructively clean ledger while preserving valid seals.<br>4. Isolate governance suite to temporary trust store.<br>5. Verify before/after hashes and zero ledger modification. | 1. Conclusively matched Entries 3-6 to manual Phase 2.13 verification commands in `transcript.jsonl`.<br>2. Backed up ledger; pruned 4 scratch entries; preserved 6 official seals.<br>3. Verified 92 files across official runs.<br>4. Automated immutability assertion added to `tearDown`.<br>5. Verified production ledger hash strictly identical before/after 27-vector run. | **SATISFIED** |

---

## 2. Table 1: Win32 Job Object Empirical Validation Results

**Script:** `testing/test_cases/baseline_regression/validate_windows_containment.py`  
**Host:** Windows 11 AMD64, Python 3.12.16  
**Execution Duration:** 35.73s | **Exit Code:** 0

| Check # | Check Name | Empirical Observations & Milestones | Expected State | Actual State | Verdict |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **1** | Suspended Process Creation & Assign-Before-Execute | Spawns child PID 37392 with `CREATE_SUSPENDED`.<br>- Marker exists before assign: `False`<br>- AssignProcessToJobObject: `1`<br>- Marker exists after assign, before resume: `False`<br>- ResumeThread previous count: `1`<br>- Marker exists 0.5s after resume: `True` | Zero instructions before assignment; executed only after resume | Fully Verified | **PASS** |
| **2** | Kill-On-Job-Close Enforcement | Child PID 37680 (`sleep(10)`). Closed Job handle directly via `CloseHandle`. Polled child at 0.5s: `proc.poll() is not None`. | Process killed immediately on handle closure | Fully Verified | **PASS** |
| **3** | Breakaway Restrictions | Child invoked `Popen` with `CREATE_BREAKAWAY_FROM_JOB`. Captured child stdout: `'BREAKAWAY_DENIED'`. Active processes in Job: 1. | Breakaway disallowed; child contained | Fully Verified | **PASS** |
| **4** | Descendant Inheritance (Nested Grandchildren) | Child PID 19900 spawned child -> grandchild. Queried Job Object basic accounting information. Captured `ActiveProcesses = 3`. | Multi-generation descendants contained ($\ge 2$) | Fully Verified | **PASS** |
| **5** | Delayed Writes Prevention (Full 32s Horizon) | Writer PID 2376 scheduled for 3s, 8s, 15s, 30s. Job terminated at $t = 0.5\text{ s}$. Observed milestones:<br>- $t = 4.5\text{ s}$: `exists(w3.txt) = False`<br>- $t = 9.5\text{ s}$: `exists(w8.txt) = False`<br>- $t = 16.5\text{ s}$: `exists(w15.txt) = False`<br>- $t = 31.5\text{ s}$: `exists(w30.txt) = False` | All delayed writes blocked across entire 32s window | Fully Verified | **PASS** |
| **6** | Complete Workload Termination | Child spawned; Job terminated. Called `wait_for_job_completion(3.0)`. Verified `all_done = True`, `ActiveProcesses = 0`. | Zero orphaned background processes | Fully Verified | **PASS** |

---

## 3. Table 2: Adversarial Governance Test Suite (27 Vectors)

**Script:** `testing/test_cases/baseline_regression/test_evidence_governance.py -v`  
**Host:** Windows 11 AMD64, Python 3.12.16  
**Execution Duration:** 17.60s | **Exit Code:** 0 | **Skips:** 0 | **Failures:** 0 | **Errors:** 0

| Vector # | Method | Verification Scope | Status |
| :---: | :--- | :--- | :---: |
| **1** | `test_01` | Missing evidence directory fails closed (`ValueError`) | **PASS** |
| **2** | `test_02` | Direct path targeting historical phase rejected (`PermissionError`) | **PASS** |
| **3** | `test_03` | Path traversal targeting historical phase rejected | **PASS** |
| **4** | `test_04` | Case variant targeting historical phase rejected | **PASS** |
| **5** | `test_05` | Directory junction alias pointing to historical phase rejected | **PASS** |
| **6** | `test_06` | Reusing populated directory without flag rejected | **PASS** |
| **7** | `test_07` | Baseline runner CLI invocation with protected phase exits code 1 | **PASS** |
| **8** | `test_08` | Sensitivity runner CLI invocation with protected phase exits code 1 | **PASS** |
| **9** | `test_09` | ProcessLifetimeJob containment and process counting on Windows | **PASS** |
| **10** | `test_10` | Post-seal file mutation detected (read-only attribute + hash mismatch) | **PASS** |
| **11** | `test_11` | Direct test function write rejected at write time | **PASS** |
| **12** | `test_12` | Direct logger write rejected at write time | **PASS** |
| **13** | `test_13` | TOCTOU junction swap rejected at write time via realpath invariance | **PASS** |
| **14** | `test_14` | Protected directories list includes all historical phases | **PASS** |
| **15** | `test_15` | SafeFileWrapper non-destructive staging never truncates target | **PASS** |
| **16** | `test_16` | Windows assign-before-execute job spawn verified live | **PASS** |
| **17** | `test_17` | Extended delayed writes contained on job exit | **PASS** |
| **18** | `test_18` | Dynamic `crash_barrier_load` key propagation verified | **PASS** |
| **19** | `test_19` | A02 raw inputs independent oracle verified | **PASS** |
| **20** | `test_20` | B01 bottom flange width mutation rejected (OpenSees analysis) | **PASS** |
| **21** | `test_21` | C01 multi-girder stress discrimination ($G_1$ / $G_2$) verified | **PASS** |
| **22** | `test_22` | Run-seal cryptographic trust architecture attacks S0-S11 rejected | **PASS** |
| **23** | `test_23` | Missing evidence directory CLI execution has no NameError | **PASS** |
| **24** | `test_24` | Fresh process sealed directory overwrite prevention verified | **PASS** |
| **25** | `test_25` | Gateway refuses writes to workspace root and `reports/` directory | **PASS** |
| **26** | `test_26` | Pinned trust store enforcement rejects unpinned override without flag | **PASS** |
| **27** | `test_27` | Probing false cgroup v2 mounts on Linux rejected fail-closed | **PASS** |

---

## 4. Table 3: Production Trust Ledger & Manifest Reconciliation

**Trust Store:** `C:\Users\Subodh\.osdagbridge_trust`  
**Ledger Path:** `C:\Users\Subodh\.osdagbridge_trust\trusted_run_seals.json`  
**Current SHA-256:** `5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1`

| Run UUID | Phase Label | Target Directory | Total Files | Manifest SHA-256 | Verification Verdict |
| :--- | :--- | :--- | :---: | :--- | :---: |
| `efb61d9c-2986-4ecd-90cf-62fbd278f6a4` | Phase 2.12 Baseline | `testing/evidence/phase_2_12/baseline` | 19 | `47241d0ff85a5707...` | **100% VALID** |
| `09dca119-7acd-450d-8b6b-11c63cf9b5a8` | Phase 2.12 Sensitivity | `testing/evidence/phase_2_12/sensitivity` | 19 | `111669b39db09c3b...` | **100% VALID** |
| `c97ab96f-dccc-47f6-b4c9-b2fa7a973b45` | Phase 2.12 Candidates | `testing/evidence/phase_2_12/candidates` | 54 | `75cf5cad23096262...` | **100% VALID** |
| `fb966e81-b715-4208-98c7-c258b7eb08fd` | Phase 2.13 Baseline | `testing/evidence/phase_2_13/baseline` | 19 | `b8711d3c777c2d53...` | **100% VALID** |
| `9aac2738-e753-49ab-84e6-7a2a61548a67` | Phase 2.13 Sensitivity | `testing/evidence/phase_2_13/sensitivity` | 19 | `0027c52b9028e70f...` | **100% VALID** |
| `867d222a-334a-4327-aaf2-d6cc7c633bed` | Phase 2.13 Candidates | `testing/evidence/phase_2_13/candidates` | 54 | `465d3f1ef9d7b14b...` | **100% VALID** |

---

## 5. Table 4: Repository & Database Integrity

| Verification Target | Expected Baseline / Hash | Observed State | Integrity Status |
| :--- | :--- | :--- | :---: |
| **Git Branch** | `dev` | `dev` | **IDENTICAL** |
| **Git Commit HEAD** | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` | **IDENTICAL** |
| **Application Tree Status** | Clean working directory | `nothing to commit, working tree clean` | **100% CLEAN** |
| **Source File Changes** | 0 files modified under `source/OsdagBridge` | 0 files modified | **UNTOUCHED** |
| **weather.sqlite Hash** | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` | **MATCH** |
| **Intg_osdag.sqlite Hash** | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` | **MATCH** |
