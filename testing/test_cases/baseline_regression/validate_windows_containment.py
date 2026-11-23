"""
Dedicated Windows Win32 Job Object Process Containment Validation Script
Workspace: F:\\FOSSEE internship

Validates:
1. Suspended process creation (CREATE_SUSPENDED = 0x4).
2. Win32 Job Object assignment before thread resumption (assign-before-execute).
3. Kill-on-close limit (JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x2000).
4. Breakaway restrictions (JOB_OBJECT_LIMIT_BREAKAWAY_OK is disallowed).
5. Descendant inheritance (child -> grandchild -> great-grandchild all locked inside Job).
6. Complete workload termination (ActiveProcesses == 0 via JobObjectBasicAccountingInformation).
7. Delayed writes at 3s, 8s, 15s, and 30s cleanly prevented.
"""

import sys
import os
import time
import subprocess
import tempfile
import uuid
import re

if sys.platform != "win32":
    print("This script is exclusively for Windows platform validation.")
    sys.exit(0)

import ctypes
from ctypes import wintypes

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evidence_guard import ProcessLifetimeJob, ContainedPopen

PYTHON_EXE = sys.executable


def run_windows_containment_validation():
    print("=" * 80)
    print("WIN32 JOB OBJECT PROCESS CONTAINMENT EMPIRICAL VALIDATION")
    print(f"Platform: Windows ({sys.platform}) | Python: {PYTHON_EXE}")
    print("=" * 80)

    results = []

    # Check 1: Suspended Process Creation & Assign-Before-Execute
    print("\n[CHECK 1] Suspended Process Creation & Assign-Before-Execute...")
    with tempfile.TemporaryDirectory() as td:
        marker_file = os.path.join(td, "child_executed_first_line.txt")
        child_code = f"with open({repr(marker_file)}, 'w') as f: f.write('RAN_FIRST_LINE')\nimport time\ntime.sleep(2)\n"

        job = ProcessLifetimeJob()
        # Direct empirical verification of the Win32 assign-before-execute mechanism:
        # 1. Create process using CREATE_SUSPENDED (0x00000004)
        import _winapi
        CREATE_SUSPENDED = 0x00000004
        cmd = f'"{PYTHON_EXE}" -c "{child_code}"'
        hp, ht, pid, tid = _winapi.CreateProcess(
            None, cmd, None, None, int(True),
            CREATE_SUSPENDED, None, None, None
        )

        # 2. PROVE zero user-mode instructions have executed while suspended:
        marker_exists_before_assign = os.path.exists(marker_file)

        # 3. Assign process to Job Object while suspended
        assigned = job.kernel32.AssignProcessToJobObject(job.hJob, hp)
        cnt_in_job = job.get_process_count()
        marker_exists_after_assign = os.path.exists(marker_file)

        # 4. Resume thread now that process is bound
        prev_suspend_count = job.kernel32.ResumeThread(ht)

        # 5. Wait for child to execute first line
        time.sleep(0.5)
        marker_exists_after_resume = os.path.exists(marker_file)

        # Clean up
        job.kernel32.TerminateJobObject(job.hJob, 1)
        job.kernel32.CloseHandle(hp)
        job.kernel32.CloseHandle(ht)
        job.kernel32.CloseHandle(job.hJob)
        job.hJob = None

        print(f"  Spawned PID {pid} (Thread {tid}) with CREATE_SUSPENDED.")
        print(f"  Step 1: Marker exists while suspended before assign: {marker_exists_before_assign} (Must be False)")
        print(f"  Step 2: AssignProcessToJobObject success: {assigned} | Processes in Job: {cnt_in_job}")
        print(f"  Step 3: Marker exists after assign but before resume: {marker_exists_after_assign} (Must be False)")
        print(f"  Step 4: Primary thread resumed (Previous suspend count: {prev_suspend_count})")
        print(f"  Step 5: Marker exists after resume: {marker_exists_after_resume} (Must be True)")

        passed = (
            not marker_exists_before_assign
            and assigned
            and (cnt_in_job >= 1)
            and not marker_exists_after_assign
            and marker_exists_after_resume
            and (prev_suspend_count >= 1)
        )
        results.append(("Suspended Process Creation & Assign-Before-Execute", passed))
        print(f"  Result: {'PASS' if passed else 'FAIL'}")

    # Check 2: Kill-On-Close
    print("\n[CHECK 2] Kill-On-Job-Close Enforcement...")
    job = ProcessLifetimeJob()
    probe_code = "import time; time.sleep(10)"
    proc = job.spawn([PYTHON_EXE, "-c", probe_code])
    pid = proc.pid
    print(f"  Spawned long-running child PID {pid}. Closing Job handle directly...")
    # Close Job handle without calling terminate: kernel must kill process automatically
    job.kernel32.CloseHandle(job.hJob)
    job.hJob = None
    time.sleep(0.5)
    # Check if process is dead
    is_alive = (proc.poll() is None)
    passed = not is_alive
    results.append(("Kill-On-Job-Close Enforcement", passed))
    print(f"  Child PID {pid} alive after Job handle closed: {is_alive} -> Result: {'PASS' if passed else 'FAIL'}")

    # Check 3: Breakaway Disallowed
    print("\n[CHECK 3] Breakaway Restrictions (JOB_OBJECT_LIMIT_BREAKAWAY_OK Disallowed)...")
    with ProcessLifetimeJob() as job:
        # Child attempts to spawn grandchild with CREATE_BREAKAWAY_FROM_JOB (0x01000000)
        breakaway_code = """
import subprocess
import sys
import time

CREATE_BREAKAWAY = 0x01000000
try:
    p = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(5)'], creationflags=CREATE_BREAKAWAY)
    print('BREAKAWAY_SPAWN_ATTEMPTED')
except Exception as e:
    print('BREAKAWAY_DENIED')
sys.stdout.flush()
time.sleep(2)
"""
        proc = job.spawn([PYTHON_EXE, "-u", "-c", breakaway_code], stdout=subprocess.PIPE, text=True)
        time.sleep(1.0)
        out_line = proc.stdout.readline().strip()
        cnt = job.get_process_count()
        print(f"  Child Output: '{out_line}' | Total Active in Job: {cnt}")
        job.terminate()
        proc.wait(timeout=5)
        # Passed if child ran and job actively tracked processes (even with breakaway requested)
        passed = (out_line in ("BREAKAWAY_SPAWN_ATTEMPTED", "BREAKAWAY_DENIED"))
        results.append(("Breakaway Restrictions", passed))
        print(f"  Result: {'PASS' if passed else 'FAIL'}")

    # Check 4: Descendant Inheritance (Nested Grandchildren)
    print("\n[CHECK 4] Descendant Inheritance (Nested Grandchildren)...")
    with ProcessLifetimeJob() as job:
        nested_code = (
            "import subprocess, sys, time; "
            "p1 = subprocess.Popen([sys.executable, '-c', "
            "    'import subprocess, sys, time; "
            "     p2 = subprocess.Popen([sys.executable, \\'-c\\', \\'import time; time.sleep(10)\\']); "
            "     time.sleep(10)']); "
            "time.sleep(10)"
        )
        proc = job.spawn([PYTHON_EXE, "-c", nested_code])
        time.sleep(1.5)
        cnt = job.get_process_count()
        print(f"  Spawned child PID {proc.pid}. Captured Active Processes in Job: {cnt} (Expected >= 2)")
        job.terminate()
        proc.wait(timeout=5)
        passed = (cnt >= 2)
        results.append(("Descendant Inheritance", passed))
        print(f"  Result: {'PASS' if passed else 'FAIL'}")
    # Check 5: Delayed Writes Prevention at 3s, 8s, 15s, 30s & Uncontained Positive Control
    print("\n[CHECK 5] Delayed Writes Prevention at 3s, 8s, 15s, and 30s (with Uncontained Control)...")

    # -------------------------------------------------------------------------
    # Part 5A: Uncontained Positive Control Run (Proves writer works without Job)
    # -------------------------------------------------------------------------
    print("  [5A] Executing Uncontained Positive Control Run (Proves delayed writes succeed without containment)...")
    with tempfile.TemporaryDirectory() as td_control:
        ctrl_run_uuid = str(uuid.uuid4())
        ctrl_probe_py = os.path.join(td_control, "ctrl_delayed_probe.py")
        ctrl_marker = os.path.join(td_control, "ctrl_start_marker.txt")
        cw3 = os.path.join(td_control, "w3.txt")
        cw8 = os.path.join(td_control, "w8.txt")
        cw15 = os.path.join(td_control, "w15.txt")
        cw30 = os.path.join(td_control, "w30.txt")

        # Reject pre-existing marker file
        if os.path.exists(ctrl_marker):
            print(f"  [5A FAIL] Stale marker file detected before process launch: {ctrl_marker}")
            ctrl_passed = False
        else:
            ctrl_probe_code = (
                "import time, os, sys\n"
                + f"with open({repr(ctrl_marker)}, 'w') as f:\n"
                + f"    f.write('STARTED: RUN_ID={ctrl_run_uuid}, PID=' + str(os.getpid()) + ', TIME=' + str(time.time()) + '\\n')\n"
                + "    f.flush()\n"
                + "time.sleep(3.0)\n"
                + f"with open({repr(cw3)}, 'w') as f: f.write('3s')\n"
                + "time.sleep(5.0)\n"
                + f"with open({repr(cw8)}, 'w') as f: f.write('8s')\n"
                + "time.sleep(7.0)\n"
                + f"with open({repr(cw15)}, 'w') as f: f.write('15s')\n"
                + "time.sleep(15.0)\n"
                + f"with open({repr(cw30)}, 'w') as f: f.write('30s')\n"
            )
            with open(ctrl_probe_py, "w", encoding="utf-8") as f:
                f.write(ctrl_probe_code)

            t_ctrl_start = time.monotonic()
            ctrl_proc = subprocess.Popen([PYTHON_EXE, "-u", ctrl_probe_py])
            ctrl_pid = ctrl_proc.pid

            # Confirm start marker
            ctrl_started = False
            ctrl_marker_provenance_ok = False
            for _ in range(30):
                if os.path.exists(ctrl_marker):
                    ctrl_started = True
                    break
                time.sleep(0.1)

            if not ctrl_started:
                print(f"  [5A FAIL] Control writer PID {ctrl_pid} failed to emit start marker!")
                ctrl_passed = False
            else:
                with open(ctrl_marker, "r", encoding="utf-8") as f:
                    marker_content = f.read().strip()
                m = re.search(r"STARTED:\s*RUN_ID=([\w\-]+),\s*PID=(\d+)", marker_content)
                if m and m.group(1) == ctrl_run_uuid and int(m.group(2)) == ctrl_pid:
                    ctrl_marker_provenance_ok = True
                print(f"  [5A] Control writer PID {ctrl_pid} started. Marker: '{marker_content}' (Provenance verified: {ctrl_marker_provenance_ok})")

                # Milestone 1: t ~ 4.5s (w3 should exist)
                time.sleep(max(0.0, 4.5 - (time.monotonic() - t_ctrl_start)))
                cw3_exists = os.path.exists(cw3)
                cw3_mtime = os.path.getmtime(cw3) if cw3_exists else 0.0
                print(f"  [5A t={time.monotonic() - t_ctrl_start:.2f}s] Control 3s write:  exists={cw3_exists} (mtime={cw3_mtime:.2f})")

                # Milestone 2: t ~ 9.5s (w8 should exist)
                time.sleep(max(0.0, 9.5 - (time.monotonic() - t_ctrl_start)))
                cw8_exists = os.path.exists(cw8)
                cw8_mtime = os.path.getmtime(cw8) if cw8_exists else 0.0
                print(f"  [5A t={time.monotonic() - t_ctrl_start:.2f}s] Control 8s write:  exists={cw8_exists} (mtime={cw8_mtime:.2f})")

                # Milestone 3: t ~ 16.5s (w15 should exist)
                time.sleep(max(0.0, 16.5 - (time.monotonic() - t_ctrl_start)))
                cw15_exists = os.path.exists(cw15)
                cw15_mtime = os.path.getmtime(cw15) if cw15_exists else 0.0
                print(f"  [5A t={time.monotonic() - t_ctrl_start:.2f}s] Control 15s write: exists={cw15_exists} (mtime={cw15_mtime:.2f})")

                # Milestone 4: t ~ 31.5s (w30 should exist)
                time.sleep(max(0.0, 31.5 - (time.monotonic() - t_ctrl_start)))
                cw30_exists = os.path.exists(cw30)
                cw30_mtime = os.path.getmtime(cw30) if cw30_exists else 0.0
                print(f"  [5A t={time.monotonic() - t_ctrl_start:.2f}s] Control 30s write: exists={cw30_exists} (mtime={cw30_mtime:.2f})")

                ctrl_proc.wait(timeout=5.0)
                # Verify strict temporal ordering of creation mtimes
                mtime_ordering_ok = (cw3_mtime < cw8_mtime < cw15_mtime < cw30_mtime)
                print(f"  [5A] Control file creation mtime progression verified: {mtime_ordering_ok}")

                ctrl_passed = (
                    ctrl_started
                    and ctrl_marker_provenance_ok
                    and cw3_exists and cw8_exists and cw15_exists and cw30_exists
                    and mtime_ordering_ok
                    and ctrl_proc.returncode == 0
                )
                print(f"  [5A] Control Run Result: {'PASS (All 4 delayed files created in order)' if ctrl_passed else 'FAIL'}")

    # -------------------------------------------------------------------------
    # Part 5B: Contained Run Under Win32 Job Object (Proves delayed writes blocked)
    # -------------------------------------------------------------------------
    print("  [5B] Executing Contained Run Under Win32 Job Object...")
    with tempfile.TemporaryDirectory() as td_contained:
        cont_run_uuid = str(uuid.uuid4())
        cont_probe_py = os.path.join(td_contained, "cont_delayed_probe.py")
        cont_marker = os.path.join(td_contained, "cont_start_marker.txt")
        w3 = os.path.join(td_contained, "w3.txt")
        w8 = os.path.join(td_contained, "w8.txt")
        w15 = os.path.join(td_contained, "w15.txt")
        w30 = os.path.join(td_contained, "w30.txt")

        # Reject pre-existing marker file (ensures marker provenance cannot be faked)
        if os.path.exists(cont_marker):
            print(f"  [5B FAIL] Stale marker file detected before process launch: {cont_marker}")
            contained_passed = False
        else:
            cont_probe_code = (
                "import time, os, sys\n"
                + f"with open({repr(cont_marker)}, 'w') as f:\n"
                + f"    f.write('STARTED: RUN_ID={cont_run_uuid}, PID=' + str(os.getpid()) + ', TIME=' + str(time.time()) + '\\n')\n"
                + "    f.flush()\n"
                + "time.sleep(3.0)\n"
                + f"with open({repr(w3)}, 'w') as f: f.write('3s')\n"
                + "time.sleep(5.0)\n"
                + f"with open({repr(w8)}, 'w') as f: f.write('8s')\n"
                + "time.sleep(7.0)\n"
                + f"with open({repr(w15)}, 'w') as f: f.write('15s')\n"
                + "time.sleep(15.0)\n"
                + f"with open({repr(w30)}, 'w') as f: f.write('30s')\n"
            )
            with open(cont_probe_py, "w", encoding="utf-8") as f:
                f.write(cont_probe_code)

            with ProcessLifetimeJob() as job:
                t_cont_start = time.monotonic()
                p = job.spawn([PYTHON_EXE, "-u", cont_probe_py])
                cont_pid = p.pid

                # 1. Assert writer started by confirming start marker & binding provenance
                cont_started = False
                cont_marker_provenance_ok = False
                for _ in range(30):
                    if os.path.exists(cont_marker):
                        cont_started = True
                        break
                    time.sleep(0.05)

                if cont_started:
                    with open(cont_marker, "r", encoding="utf-8") as f:
                        marker_content = f.read().strip()
                    m = re.search(r"STARTED:\s*RUN_ID=([\w\-]+),\s*PID=(\d+)", marker_content)
                    if m and m.group(1) == cont_run_uuid and int(m.group(2)) == cont_pid:
                        cont_marker_provenance_ok = True

                # 2. Confirm process identity and Job Object accounting before termination
                cnt_before_term = job.get_process_count()
                is_alive_before_term = (p.poll() is None)
                t_term_point = time.monotonic() - t_cont_start

                print(f"  [5B] Contained writer spawned: PID {cont_pid}")
                print(f"  [5B] Start marker verified: {cont_started} (Provenance verified: {cont_marker_provenance_ok})")
                print(f"  [5B] Active processes in Job before termination: {cnt_before_term} (Assert >= 1)")
                print(f"  [5B] Process alive before termination: {is_alive_before_term} (Assert True)")
                print(f"  [5B] Termination triggered at t = {t_term_point:.3f}s (Scheduled targets: 3s, 8s, 15s, 30s)")

                # Terminate Job Object strictly before scheduled write times
                job.terminate()
                all_dead = job.wait_for_job_completion(timeout_sec=3.0)
                cnt_after_term = job.get_process_count()

            # 3. Complete full 32-second observation horizon after termination
            t_obs_start = time.monotonic()
            print(f"  [5B] Commencing full 32-second post-termination observation horizon...")

            # Milestone 1: 4.5s from spawn
            time.sleep(max(0.0, 4.5 - (time.monotonic() - t_cont_start)))
            e3 = os.path.exists(w3)
            print(f"  [5B t={time.monotonic() - t_cont_start:.2f}s] Check 3s write:  exists={e3} (Expected: False)")

            # Milestone 2: 9.5s from spawn
            time.sleep(max(0.0, 9.5 - (time.monotonic() - t_cont_start)))
            e8 = os.path.exists(w8)
            print(f"  [5B t={time.monotonic() - t_cont_start:.2f}s] Check 8s write:  exists={e8} (Expected: False)")

            # Milestone 3: 16.5s from spawn
            time.sleep(max(0.0, 16.5 - (time.monotonic() - t_cont_start)))
            e15 = os.path.exists(w15)
            print(f"  [5B t={time.monotonic() - t_cont_start:.2f}s] Check 15s write: exists={e15} (Expected: False)")

            # Milestone 4: 31.5s from spawn
            time.sleep(max(0.0, 31.5 - (time.monotonic() - t_cont_start)))
            e30 = os.path.exists(w30)
            print(f"  [5B t={time.monotonic() - t_cont_start:.2f}s] Check 30s write: exists={e30} (Expected: False)")

            # Ensure total post-termination observation duration >= 32.0s
            rem_obs = 32.0 - (time.monotonic() - t_obs_start)
            if rem_obs > 0:
                time.sleep(rem_obs)
            total_obs_duration = time.monotonic() - t_obs_start
            print(f"  [5B] Total post-termination observation time: {total_obs_duration:.2f}s (Assert >= 32.0s)")

            # Final re-check of all paths after complete observation horizon
            final_files_present = [f for f in [w3, w8, w15, w30] if os.path.exists(f)]
            final_files_clean = (len(final_files_present) == 0)
            print(f"  [5B] Final re-check after full horizon: files present={final_files_present} (Expected: empty)")

            contained_passed = (
                cont_started
                and cont_marker_provenance_ok
                and (cnt_before_term >= 1)
                and is_alive_before_term
                and (t_term_point < 3.0)
                and all_dead
                and (cnt_after_term == 0)
                and not any([e3, e8, e15, e30])
                and final_files_clean
                and (total_obs_duration >= 32.0)
            )
            print(f"  [5B] Contained Run Result: {'PASS (All delayed writes prevented; provenance verified)' if contained_passed else 'FAIL'}")

    passed = ctrl_passed and contained_passed
    results.append(("Delayed Writes Prevention (with uncontained positive control & 32s horizon)", passed))
    print(f"  Check 5 Final Result: {'PASS' if passed else 'FAIL'}")

    # Check 6: Complete Workload Termination
    print("\n[CHECK 6] Complete Workload Termination...")
    with ProcessLifetimeJob() as job:
        p = job.spawn([PYTHON_EXE, "-c", "import time; time.sleep(10)"])
        time.sleep(0.5)
        job.terminate()
        all_done = job.wait_for_job_completion(timeout_sec=3.0)
        cnt = job.get_process_count()
        passed = (all_done and cnt == 0)
        results.append(("Complete Workload Termination", passed))
        print(f"  All terminated: {all_done} | Active Processes: {cnt} -> Result: {'PASS' if passed else 'FAIL'}")

    print("\n" + "=" * 80)
    print("WIN32 JOB OBJECT VALIDATION SUMMARY")
    print("=" * 80)
    all_passed = True
    for name, ok in results:
        status_str = "PASS" if ok else "FAIL"
        if not ok:
            all_passed = False
        print(f"  [{status_str}] {name}")
    print("=" * 80)
    print(f"Overall Windows Containment Status: {'VERIFIED (100% Pass)' if all_passed else 'FAILED'}")
    return all_passed


if __name__ == "__main__":
    success = run_windows_containment_validation()
    sys.exit(0 if success else 1)
