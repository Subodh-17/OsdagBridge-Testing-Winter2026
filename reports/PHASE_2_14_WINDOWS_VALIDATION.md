# Phase 2.14 — Windows Process Containment & Governance Empirical Validation

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge` on branch `dev` @ [`d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`](file:///F:/FOSSEE%20internship/source/OsdagBridge)  
**Controlling Audit:** Claude's Phase 2.13 Independent Gate Audit ([`reports/PHASE_2_13_FINAL_INDEPENDENT_GATE_AUDIT.md`](file:///F:/FOSSEE%20internship/reports/PHASE_2_13_FINAL_INDEPENDENT_GATE_AUDIT.md))  
**Platform:** Real Windows 11 Host (`win32` / AMD64), Python 3.12.16 (`osdagbridge-py312`)  
**Execution Date:** 2026-11-17 (UTC / IST)  
**Status:** **SATISFIED** (Condition 1 Closed)

---

## 1. Executive Summary

In the Phase 2.13 audit, Claude independently accepted the architectural design and code structure of the Win32 Job Object containment and governance suites, but was forced to mark empirical Windows execution as **BLOCKED** because the auditor's environment was Linux-only. Claude issued **Condition 1**:
> "1. Independently reproduce, on a real Windows host, the 6 containment checks and all 27 governance vectors, and preserve the output."

This report provides the primary empirical evidence collected from a fresh, native execution directly on the Windows host. No Linux emulation was used, no Phase 2.13 logs were recycled, all standard output and standard error streams were captured live, and the full 32-second post-termination observation horizon was observed.

**Overall Results:**
- **Win32 Job Object Process Containment:** **6 / 6 Checks PASSED (100%)** in 35.73s.
- **Adversarial Evidence Governance Suite:** **27 / 27 Attack Vectors PASSED (100%, 0 skips, 0 failures, 0 errors)** in 17.60s.

---

## 2. Win32 Job Object Process Containment (6 Checks)

**Harness Script:** [`testing/test_cases/baseline_regression/validate_windows_containment.py`](file:///F:/FOSSEE%20internship/testing/test_cases/baseline_regression/validate_windows_containment.py)  
**Command:** `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe -u testing/test_cases/baseline_regression/validate_windows_containment.py`  
**Execution Timestamp:** 2026-11-17T18:17:19.977Z to 2026-11-17T18:17:55.708Z (Duration: 35.73s)  
**Exit Code:** `0`  
**Primary Artifact:** [`testing/evidence/phase_2_14/windows/windows_containment_validation.txt`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_14/windows/windows_containment_validation.txt)  
**Live Transcript:** [`testing/evidence/phase_2_14/windows/transcripts/windows_containment_validation.log`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_14/windows/transcripts/windows_containment_validation.log)

### Check-by-Check Empirical Breakdown

| Check ID | Verification Objective | Mechanism & Empirical Observations | Verdict |
| :--- | :--- | :--- | :---: |
| **Check 1** | Suspended Process Creation & Assign-Before-Execute | Spawns child process with `CREATE_SUSPENDED` (0x00000004): PID 37392 (Thread 35620).<br>1. *Pre-assignment:* Checked marker file existence while thread suspended: `False` (zero instructions executed).<br>2. *Assignment:* Called `AssignProcessToJobObject(job.hJob, hp)` -> returned `1` (True). Active process count = 1.<br>3. *Pre-resume:* Checked marker file existence after assignment but before resume: `False` (still zero instructions executed).<br>4. *Resumption:* Called `ResumeThread(ht)` -> returned previous suspend count `1`.<br>5. *Post-resume:* Slept 0.5s; checked marker file existence: `True` (child executed safely within Job boundary). | **PASS** |
| **Check 2** | Kill-On-Job-Close Enforcement | Configured Job with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` (0x2000). Spawned long-running child PID 37680 (`sleep(10)`). Directly closed Job handle `job.hJob` via `CloseHandle` without invoking `TerminateJobObject`. Slept 0.5s. Polled child process: `proc.poll() is not None` (`is_alive = False`). Kernel terminated process immediately upon handle closure. | **PASS** |
| **Check 3** | Breakaway Restrictions | Job Object omits `JOB_OBJECT_LIMIT_BREAKAWAY_OK`. Spawned child process that invoked `subprocess.Popen(..., creationflags=CREATE_BREAKAWAY_FROM_JOB)`. Captured child output: `'BREAKAWAY_DENIED'` (Win32 raised access denied on breakaway flag). Active processes tracked in Job: 1. Terminated Job cleanly. | **PASS** |
| **Check 4** | Descendant Inheritance (Nested Grandchildren) | Spawned parent child PID 19900 which spawned a child, which spawned a grandchild (3 process generations). Queried `QueryInformationJobObject` with `JobObjectBasicAccountingInformation`. Captured `ActiveProcesses = 3` (Expected $\ge 2$). Proves multi-generation descendant containment holds. | **PASS** |
| **Check 5** | Delayed Writes Prevention (Full 32s Horizon) | Spawned delayed-writer PID 2376 scheduled to write at 3s (`w3.txt`), 8s (`w8.txt`), 15s (`w15.txt`), and 30s (`w30.txt`). Terminated Job Object at $t = 0.5\text{ s}$. Observed system across full 32-second horizon:<br>- Milestone $t = 4.5\text{ s}$: `exists(w3.txt) = False`<br>- Milestone $t = 9.5\text{ s}$: `exists(w8.txt) = False`<br>- Milestone $t = 16.5\text{ s}$: `exists(w15.txt) = False`<br>- Milestone $t = 31.5\text{ s}$: `exists(w30.txt) = False`<br>Total files created after termination: **0**. | **PASS** |
| **Check 6** | Complete Workload Termination | Spawned child process; invoked `job.terminate()`. Called `job.wait_for_job_completion(timeout_sec=3.0)`. Verified `all_done = True` and `ActiveProcesses = 0`. | **PASS** |

---

## 3. Adversarial Evidence Governance Suite (27 Vectors)

**Harness Script:** [`testing/test_cases/baseline_regression/test_evidence_governance.py`](file:///F:/FOSSEE%20internship/testing/test_cases/baseline_regression/test_evidence_governance.py)  
**Command:** `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe -u testing/test_cases/baseline_regression/test_evidence_governance.py -v`  
**Execution Timestamp:** 2026-11-17T18:18:18.341Z to 2026-11-17T18:18:36.244Z (Duration: 17.60s)  
**Exit Code:** `0`  
**Primary Artifact:** [`testing/evidence/phase_2_14/windows/governance_test_output.txt`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_14/windows/governance_test_output.txt)  
**Live Transcript:** [`testing/evidence/phase_2_14/windows/transcripts/governance_test_output.log`](file:///F:/FOSSEE%20internship/testing/evidence/phase_2_14/windows/transcripts/governance_test_output.log)

### Complete Vector-by-Vector Results Table

| Vector # | Test Function Name | Attack Class / Verification Target | Windows Outcome | Note |
| :---: | :--- | :--- | :---: | :--- |
| **1** | `test_01_missing_evidence_dir_fails_closed` | Empty or whitespace evidence directory | **PASS (ok)** | Fails closed with `ValueError` |
| **2** | `test_02_protected_historical_phase_rejected` | Direct path to historical phase (`phase_2_8`) | **PASS (ok)** | Fails closed with `PermissionError` |
| **3** | `test_03_path_traversal_targeting_protected_phases_rejected` | Traversal aliases (`active/../../phase_2_6`) | **PASS (ok)** | Canonical realpath rejects traversal |
| **4** | `test_04_case_variant_targeting_protected_phases_rejected` | Case-insensitive aliasing (`PHASE_2_6`) | **PASS (ok)** | Normcase/realpath catches variants |
| **5** | `test_05_symlink_or_junction_to_protected_phase_rejected` | Directory junction alias pointing to protected phase | **PASS (ok)** | Reparse point resolved; rejected |
| **6** | `test_06_populated_directory_reuse_rejected_by_default` | Reusing populated directory without flag | **PASS (ok)** | Re-use denied fail-closed |
| **7** | `test_07_baseline_runner_cli_fails_on_protected_phase` | Baseline runner CLI invocation with protected target | **PASS (ok)** | Process exits with code 1 |
| **8** | `test_08_sensitivity_runner_cli_fails_on_protected_phase` | Sensitivity runner CLI invocation with protected target | **PASS (ok)** | Process exits with code 1 |
| **9** | `test_09_process_lifetime_job_containment` | Win32 Job Object process containment & accounting | **PASS (ok)** | *Previously skipped on Linux*; runs live on Windows |
| **10** | `test_10_post_manifest_tamper_detection` | File mutation after manifest sealing | **PASS (ok)** | Read-only attribute deters append; reset + mutate caught by hash |
| **11** | `test_11_direct_test_function_write_rejected_at_write_time` | Direct test function targeting historical phase | **PASS (ok)** | Denied at write time |
| **12** | `test_12_direct_logger_write_rejected_at_write_time` | `log_test_result` targeting historical phase | **PASS (ok)** | Denied at write time |
| **13** | `test_13_toctou_symlink_swap_rejected_at_write_time` | Post-startup junction swap to protected phase | **PASS (ok)** | Realpath re-check in `SafeFileWrapper` rejects swap |
| **14** | `test_14_protected_directories_include_baseline_repaired_and_phase_2_11` | Exhaustive protected phase list inspection | **PASS (ok)** | All historical phases hardcoded |
| **15** | `test_15_non_destructive_toctou_defense_never_truncates` | Staging + atomic replace prevents target truncation | **PASS (ok)** | Target content preserved intact |
| **16** | `test_16_windows_assign_before_execute_job_spawn` | `job.spawn` assign-before-execute hook | **PASS (ok)** | *Previously skipped on Linux*; runs live on Windows |
| **17** | `test_17_extended_delayed_write_probes_contained` | Extended delayed writes (3s, 8s, 15s) in Job | **PASS (ok)** | *Previously skipped on Linux*; runs live on Windows |
| **18** | `test_18_eq_barrier_load_oracle_dynamic_derivation` | Dynamic `crash_barrier_load` key propagation | **PASS (ok)** | Verifies live production helper |
| **19** | `test_19_a02_raw_inputs_independent_from_production_helper` | A02 independent oracle catches mutated helper | **PASS (ok)** | Independent calculation verified |
| **20** | `test_20_b01_bottom_flange_width_mutation_rejected` | B01 geometry mutation rejection (410 -> 450 mm) | **PASS (ok)** | OpenSees analysis fails as expected |
| **21** | `test_21_c01_multi_girder_discrimination` | Multi-girder stress coverage ($G_1$ / $G_2$) | **PASS (ok)** | Rejects 1st-girder and low shortcuts |
| **22** | `test_22_run_seal_trust_architecture_attacks_s1_through_s11` | Cryptographic seal verification attacks (S0-S11) | **PASS (ok)** | Catches modification, forgery, extra files |
| **23** | `test_23_missing_evidence_dir_cli_execution_no_name_error` | CLI help invocation without `--evidence-dir` | **PASS (ok)** | Exits code 0 with zero NameErrors |
| **24** | `test_24_cross_process_sealed_overwrite_prevention` | Fresh process write to sealed directory | **PASS (ok)** | Fresh process denied via persistent ledger |
| **25** | `test_25_workspace_root_and_reports_protection` | Writes to workspace root and `reports/` directory | **PASS (ok)** | Unconditional denial enforced |
| **26** | `test_26_pinned_trust_directory_enforcement` | Unpinned trust directory redirect without flag (K14) | **PASS (ok)** | Fails closed with `PermissionError` |
| **27** | `test_27_linux_cgroup_tmpfs_detection_rejection` | Probing fake cgroup v2 mounts on Linux | **PASS (ok)** | Verified containment type logic |

---

## 4. Resolution of Linux-Blocked Vectors on Windows

In Claude's Phase 2.13 Linux audit (`REPRODUCTION_RESULTS.md` §1), the governance suite had 3 skipped tests and 1 failure:
1. **Vectors 9, 16, and 17 (Skipped on Linux):**
   - On Linux without cgroup v2 delegation, `job.is_contained` was `False`, causing Vectors 9, 16, and 17 to skip.
   - On Windows, `ProcessLifetimeJob` utilizes native Win32 Job Objects (`AssignProcessToJobObject`), which require zero elevated privileges. All three vectors executed live on Windows and **PASSED**.
2. **Vector 10 (Failed as root on Linux):**
   - On POSIX, `root` ignores the `S_IREAD` read-only bit, causing `open(..., 'a')` to succeed instead of raising `PermissionError`.
   - On Windows (running under normal user `Subodh`), `os.chmod(sample_file, stat.S_IREAD)` sets the Win32 `FILE_ATTRIBUTE_READONLY` flag. The Windows NT kernel rejects `open(..., 'a')` with `PermissionError: [Errno 13] Permission denied`. Then step 2 resets permissions, tampers with the file, and `verify_manifest_integrity` catches the tampering with `HASH_MISMATCH`. Vector 10 executed live on Windows and **PASSED**.
3. **Vectors 5, 13, and 15 (Junctions vs Symlinks):**
   - On Windows, creating symbolic links (`os.symlink`) requires `SeCreateSymbolicLinkPrivilege` or Developer Mode.
   - In Phase 2.13, these vectors were updated to use directory junctions (`_winapi.CreateJunction`), which are native NTFS reparse points available to all standard users. All three vectors executed live on Windows and **PASSED**.

---

## 5. Summary Conclusion

Condition 1 of Claude's Phase 2.13 Independent Gate Audit is **SATISFIED**:
- 6/6 Win32 Job Object containment checks were empirically executed and validated on the native Windows host, observing the full 32-second horizon.
- 27/27 governance attack vectors were empirically executed and validated on the native Windows host with zero skips, zero failures, and zero errors.
- Complete live transcripts and output logs are preserved in `testing/evidence/phase_2_14/windows/`.
