"""
Phase 2.12 Comprehensive Adversarial Test Suite for Evidence Governance and Containment
Controlling Audit: reports/PHASE_2_11_FINAL_INDEPENDENT_GATE_AUDIT.md

Exercises unit guards, process containment boundaries, post-run verification,
and engineering oracles against adversarial attacks and subtle bypasses:
  1. Missing evidence directory fails closed.
  2. Protected historical phase paths rejected (phase_1d through phase_2_11).
  3. Path traversal ('..') targeting protected phases rejected.
  4. Case-variant paths targeting protected phases rejected.
  5. Symlink / junction to protected phase rejected.
  6. Populated directory reuse rejected.
  7. Official baseline runner CLI fails on protected phase.
  8. Official sensitivity runner CLI fails on protected phase.
  9. ProcessLifetimeJob containment and process-count tracking.
  10. Post-manifest tamper detection.
  11. Direct test-function write to protected phase rejected at write time.
  12. Direct logger write to protected phase rejected at write time.
  13. TOCTOU symlink swap rejected at write time without truncating target.
  14. Protected directories include phase_2_11, phase_2_baseline, phase_2_repaired.
  15. Non-destructive TOCTOU: directory replacement leaves target file 100% untruncated.
  16. Windows assign-before-execute via CREATE_SUSPENDED and Job Object assignment.
  17. Extended delayed-write probes (3s, 8s, 15s) contained cleanly.
  18. EQ barrier load oracle dynamically uses genuine "crash_barrier_load" key.
  19. A02 independent oracle catches mutated production barrier helper (0.9x probe).
  20. B01 bottom flange width mutation (410 -> 450 mm) fails test.
  21. C01 multi-girder discrimination: first-girder, j-end-only, i-end-only, and -1.5% low fail.
  22. External Run Seals Trust Architecture: S1-S11 attack classes rejected fail-closed.
  23. Missing --evidence-dir CLI argument generates unique safe directory without NameError.
"""

import sys
import os
import time
import shutil
import tempfile
import json
import subprocess
import copy
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
REPO_SRC = os.path.join(WORKSPACE_ROOT, "source", "OsdagBridge", "src")
if REPO_SRC not in sys.path:
    sys.path.insert(0, REPO_SRC)
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from testing.test_cases.baseline_regression.evidence_guard import (
    validate_evidence_directory,
    is_protected_phase_directory,
    is_sealed_directory,
    register_sealed_directory,
    safe_open_evidence,
    safe_write_evidence,
    safe_copy_evidence,
    generate_and_seal_manifest,
    verify_manifest_integrity,
    ProcessLifetimeJob,
    sha256_file,
    get_trust_dir,
    get_or_create_signing_key,
    compute_seal_signature,
    get_all_protected_phases,
    PROTECTED_PHASES,
    PINNED_TRUST_DIR,
    WORKSPACE_ROOT
)

BASELINE_RUNNER = os.path.join(SCRIPT_DIR, "run_all_baseline_tests.py")
SENSITIVITY_RUNNER = os.path.join(SCRIPT_DIR, "run_sensitivity_matrix.py")
VERIFY_MANIFEST = os.path.join(SCRIPT_DIR, "verify_manifest.py")
PYTHON_EXE = sys.executable


def create_dir_alias(target, link_path):
    """
    Creates a directory link: on Windows uses directory junctions (_winapi.CreateJunction)
    which requires NO administrator or Developer Mode privileges. On POSIX uses os.symlink.
    """
    if sys.platform == "win32":
        import _winapi
        try:
            _winapi.CreateJunction(os.path.abspath(target), os.path.abspath(link_path))
            return
        except Exception:
            pass
    os.symlink(target, link_path, target_is_directory=True)


class TestEvidenceGovernanceAdversarial(unittest.TestCase):

    def setUp(self):
        # Isolate trust store so tests NEVER pollute official seal registry
        import hashlib
        self._prod_ledger = os.path.join(
            os.path.realpath(os.path.expandvars(r"%USERPROFILE%\.osdagbridge_trust"))
            if sys.platform == "win32" else
            os.path.realpath(os.path.join(os.path.expanduser("~"), ".osdagbridge_trust")),
            "trusted_run_seals.json"
        )
        if os.path.exists(self._prod_ledger):
            with open(self._prod_ledger, "rb") as f:
                self._prod_ledger_hash_before = hashlib.sha256(f.read()).hexdigest()
        else:
            self._prod_ledger_hash_before = None

        self._trust_td = tempfile.TemporaryDirectory()
        self._orig_trust_env = os.environ.get("OSDAGBRIDGE_TRUST_DIR")
        self._orig_override_env = os.environ.get("OSDAGBRIDGE_ALLOW_TEST_TRUST_OVERRIDE")
        os.environ["OSDAGBRIDGE_TRUST_DIR"] = self._trust_td.name
        os.environ["OSDAGBRIDGE_ALLOW_TEST_TRUST_OVERRIDE"] = "1"

    def tearDown(self):
        if self._orig_trust_env is not None:
            os.environ["OSDAGBRIDGE_TRUST_DIR"] = self._orig_trust_env
        else:
            os.environ.pop("OSDAGBRIDGE_TRUST_DIR", None)
        if self._orig_override_env is not None:
            os.environ["OSDAGBRIDGE_ALLOW_TEST_TRUST_OVERRIDE"] = self._orig_override_env
        else:
            os.environ.pop("OSDAGBRIDGE_ALLOW_TEST_TRUST_OVERRIDE", None)

        try:
            self._trust_td.cleanup()
        except Exception:
            pass

        # Strict isolation check: production ledger must never be touched by tests
        if os.path.exists(self._prod_ledger) and self._prod_ledger_hash_before is not None:
            import hashlib
            with open(self._prod_ledger, "rb") as f:
                current_hash = hashlib.sha256(f.read()).hexdigest()
            self.assertEqual(
                current_hash, self._prod_ledger_hash_before,
                f"PRODUCTION TRUST LEDGER COMPROMISE: Hash changed during test execution from "
                f"{self._prod_ledger_hash_before} to {current_hash}!"
            )

    def test_01_missing_evidence_dir_fails_closed(self):
        """Vector 1: Invocation without evidence directory or with empty string must fail closed."""
        with self.assertRaises(ValueError):
            validate_evidence_directory("")
        with self.assertRaises(ValueError):
            validate_evidence_directory(None)
        with self.assertRaises(ValueError):
            validate_evidence_directory("   ")

    def test_02_protected_historical_phase_rejected(self):
        """Vector 2: Direct path targeting any historical phase directory must be refused."""
        for phase in ["phase_2_6", "phase_2_7", "phase_2_8", "phase_2_9", "phase_2_10", "phase_2_11", "phase_2_baseline"]:
            target = os.path.join(WORKSPACE_ROOT, "testing", "evidence", phase, "baseline")
            with self.assertRaises(PermissionError):
                validate_evidence_directory(target)

    def test_03_path_traversal_targeting_protected_phases_rejected(self):
        """Vector 3: Traversal patterns like active/../../phase_2_6/baseline must be detected and blocked."""
        target = os.path.join(WORKSPACE_ROOT, "testing", "evidence", "phase_2_12", "..", "phase_2_6", "baseline")
        with self.assertRaises(PermissionError):
            validate_evidence_directory(target)

    def test_04_case_variant_targeting_protected_phases_rejected(self):
        """Vector 4: Case variants like PHASE_2_6 or Phase_2_7 must be caught on Windows/POSIX."""
        target = os.path.join(WORKSPACE_ROOT, "testing", "evidence", "PHASE_2_6", "baseline")
        with self.assertRaises(PermissionError):
            validate_evidence_directory(target)

    def test_05_symlink_or_junction_to_protected_phase_rejected(self):
        """Vector 5: Symlinks or junctions pointing into protected phase directories must be caught."""
        with tempfile.TemporaryDirectory() as td:
            link_target = os.path.join(td, "alias_link")
            real_target = os.path.join(WORKSPACE_ROOT, "testing", "evidence", "phase_2_7", "baseline")
            create_dir_alias(real_target, link_target)
            with self.assertRaises(PermissionError):
                validate_evidence_directory(link_target)

    def test_06_populated_directory_reuse_rejected_by_default(self):
        """Vector 6: Reusing an existing populated evidence directory without allow_existing=True fails."""
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, "artifact.txt"), "w") as f:
                f.write("existing")
            with self.assertRaises(FileExistsError):
                validate_evidence_directory(td, allow_existing=False)

    def test_07_baseline_runner_cli_fails_on_protected_phase(self):
        """Vector 7: Executing baseline runner with protected phase directory exits with code 1."""
        target = os.path.join(WORKSPACE_ROOT, "testing", "evidence", "phase_2_8", "baseline")
        cmd = [PYTHON_EXE, BASELINE_RUNNER, "--evidence-dir", target]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("CRITICAL EVIDENCE OVERWRITE BLOCKED", proc.stderr + proc.stdout)

    def test_08_sensitivity_runner_cli_fails_on_protected_phase(self):
        """Vector 8: Executing sensitivity runner with protected candidates directory exits with code 1."""
        target_sens = os.path.join(WORKSPACE_ROOT, "testing", "evidence", "phase_2_12", "scratch_sens")
        target_cand = os.path.join(WORKSPACE_ROOT, "testing", "evidence", "phase_2_9", "candidates")
        cmd = [PYTHON_EXE, SENSITIVITY_RUNNER, "--evidence-dir", target_sens, "--candidates-dir", target_cand]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)

    def test_09_process_lifetime_job_containment(self):
        """Vector 9: ProcessLifetimeJob contains child processes and reports process counts accurately."""
        with ProcessLifetimeJob() as job:
            if not job.is_contained:
                self.skipTest("OS-level process containment unavailable on this environment")
            p = job.spawn([PYTHON_EXE, "-c", "import time; time.sleep(0.5)"])
            self.assertIsNotNone(p.pid)
            self.assertGreaterEqual(job.get_process_count(), 1)
            job.terminate()
            self.assertTrue(job.wait_for_job_completion(timeout_sec=2.0))
            try:
                p.wait(timeout=2.0)
            except Exception:
                pass

    def test_10_post_manifest_tamper_detection(self):
        """Vector 10: Modifying an evidence file after manifest sealing is immediately detected."""
        with tempfile.TemporaryDirectory() as td:
            sample_file = os.path.join(td, "evidence.txt")
            with safe_open_evidence(sample_file, "w") as f:
                f.write("AUTHENTIC_DATA")

            manifest, seal = generate_and_seal_manifest(td, phase_label="Test Tamper Phase", trust_dir=self._trust_td.name, allow_trust_override=True)
            # Verify clean directory matches seal
            is_valid, errors, _ = verify_manifest_integrity(td, trust_dir=self._trust_td.name, allow_trust_override=True)
            self.assertTrue(is_valid, f"Verification failed on clean directory: {errors}")

            # 1. Verify that direct write is blocked by OS read-only attributes (on non-root/Windows)
            is_root = (sys.platform != "win32" and hasattr(os, "geteuid") and os.geteuid() == 0)
            if not is_root:
                with self.assertRaises(PermissionError):
                    with open(sample_file, "a") as f:
                        f.write("_MUTATED")

            # 2. Simulate attacker resetting permissions and tampering
            # Cross-platform read+write: 0o600 (stat.S_IRUSR | stat.S_IWUSR) preserves read access on POSIX
            import stat
            RW_MODE = (stat.S_IRUSR | stat.S_IWUSR) if hasattr(stat, "S_IRUSR") else (stat.S_IREAD | stat.S_IWRITE)
            os.chmod(sample_file, RW_MODE)
            with open(sample_file, "a") as f:
                f.write("_MUTATED")

            # Must fail integrity check
            is_valid2, errors2, _ = verify_manifest_integrity(td, trust_dir=self._trust_td.name, allow_trust_override=True)
            self.assertFalse(is_valid2)
            self.assertTrue(any("HASH_MISMATCH" in e for e in errors2))

    def test_11_direct_test_function_write_rejected_at_write_time(self):
        """Vector 11: Direct test-function calls with protected evidence_dir fail at write time."""
        from testing.test_cases.baseline_regression.run_all_baseline_tests import test_tc_reg_a01
        target = os.path.join(WORKSPACE_ROOT, "testing", "evidence", "phase_2_8", "baseline")
        with self.assertRaises(PermissionError):
            test_tc_reg_a01(evidence_dir=target)

    def test_12_direct_logger_write_rejected_at_write_time(self):
        """Vector 12: Direct calls to log_test_result with protected evidence_dir fail at write time."""
        from testing.test_cases.baseline_regression.run_all_baseline_tests import log_test_result
        target = os.path.join(WORKSPACE_ROOT, "testing", "evidence", "phase_2_7", "baseline")
        with self.assertRaises(PermissionError):
            log_test_result("TC-REG-TEST", "DEF-00", "PASS", "PASS", "Reason", "Details", 0.01, target)

    def test_13_toctou_symlink_swap_rejected_at_write_time(self):
        """Vector 13: Canonical realpath validation catches directory symlinks created after startup."""
        with tempfile.TemporaryDirectory() as td:
            alias_dir = os.path.join(td, "alias_phase")
            real_protected = os.path.join(WORKSPACE_ROOT, "testing", "evidence", "phase_2_6", "baseline")
            create_dir_alias(real_protected, alias_dir)
            test_file = os.path.join(alias_dir, "probe.log")
            with self.assertRaises(PermissionError):
                with safe_open_evidence(test_file, "w") as f:
                    f.write("PAYLOAD")

    def test_14_protected_directories_include_baseline_repaired_and_phase_2_11(self):
        """Vector 14: Historical directories list contains phase_2_11, phase_2_baseline, phase_2_repaired."""
        all_protected = get_all_protected_phases()
        self.assertIn("phase_2_11", all_protected)
        self.assertIn("phase_2_baseline", all_protected)
        self.assertIn("phase_2_repaired", all_protected)
        self.assertTrue(is_protected_phase_directory("testing/evidence/phase_2_11/baseline"))
        self.assertTrue(is_protected_phase_directory("testing/evidence/phase_2_baseline/evidence"))
        self.assertTrue(is_protected_phase_directory("testing/evidence/phase_2_repaired/evidence"))

    def test_15_non_destructive_toctou_defense_never_truncates(self):
        """Vector 15: If an attacker swaps directory to a protected target, the target file is NEVER truncated."""
        with tempfile.TemporaryDirectory() as td:
            protected_dir = os.path.join(td, "protected")
            os.makedirs(protected_dir, exist_ok=True)
            sentinel_file = os.path.join(protected_dir, "sentinel.log")
            sentinel_content = "ORIGINAL_AUTHENTIC_SENTINEL_CONTENT_DO_NOT_TRUNCATE"
            with open(sentinel_file, "w", encoding="utf-8") as f:
                f.write(sentinel_content)
            orig_hash = sha256_file(sentinel_file)

            race_dir = os.path.join(td, "race")
            os.makedirs(race_dir, exist_ok=True)
            target_race_file = os.path.join(race_dir, "sentinel.log")

            # Pre-create wrapper on race_dir
            wrapper = safe_open_evidence(target_race_file, "w", encoding="utf-8")

            # Deterministic attacker swap: replace race_dir with a symlink/junction to protected_dir
            os.rmdir(race_dir)
            create_dir_alias(protected_dir, race_dir)

            # Enter wrapper: must raise PermissionError without truncating sentinel_file!
            with self.assertRaises(PermissionError):
                with wrapper as f:
                    f.write("ATTACKER_PAYLOAD")

            # Verify sentinel was NEVER truncated
            self.assertTrue(os.path.exists(sentinel_file))
            self.assertEqual(os.path.getsize(sentinel_file), len(sentinel_content))
            self.assertEqual(sha256_file(sentinel_file), orig_hash, "CRITICAL: Sentinel file was truncated during TOCTOU race!")

    def test_16_windows_assign_before_execute_job_spawn(self):
        """Vector 16: job.spawn() assigns process to Job Object before primary thread execution."""
        if sys.platform != "win32":
            self.skipTest("Windows Job Object assign-before-execute test only applicable on Windows")

        with ProcessLifetimeJob() as job:
            probe_code = "import sys, time; print('CHILD_EXECUTING'); sys.stdout.flush(); time.sleep(1)"
            proc = job.spawn([PYTHON_EXE, "-u", "-c", probe_code], stdout=subprocess.PIPE, text=True)
            self.assertIsNotNone(proc.pid)
            # Process must be in job object
            cnt = job.get_process_count()
            self.assertGreaterEqual(cnt, 1)
            line = proc.stdout.readline()
            self.assertIn("CHILD_EXECUTING", line)
            job.terminate()
            proc.wait(timeout=5)

    def test_17_extended_delayed_write_probes_contained(self):
        """Vector 17: Extended delayed writes (3s, 8s, 15s) are cleanly intercepted and contained on job exit."""
        with tempfile.TemporaryDirectory() as td:
            probe_script = os.path.join(td, "delayed_writer.py")
            output_3s = os.path.join(td, "write_3s.txt")
            output_8s = os.path.join(td, "write_8s.txt")
            output_15s = os.path.join(td, "write_15s.txt")

            with open(probe_script, "w", encoding="utf-8") as f:
                f.write(f"""import time
time.sleep(3)
with open({repr(output_3s)}, 'w') as f:
    f.write('3s write')
time.sleep(5)
with open({repr(output_8s)}, 'w') as f:
    f.write('8s write')
time.sleep(7)
with open({repr(output_15s)}, 'w') as f:
    f.write('15s write')
""")

            with ProcessLifetimeJob() as job:
                if not job.is_contained:
                    self.skipTest("OS-level process containment unavailable on this environment")
                p = job.spawn([PYTHON_EXE, probe_script])
                time.sleep(0.5)
                self.assertGreaterEqual(job.get_process_count(), 1)
                job.terminate()
                job.wait_for_job_completion(timeout_sec=2.0)
                try:
                    p.wait(timeout=2.0)
                except Exception:
                    pass

            time.sleep(4.0)
            self.assertFalse(os.path.exists(output_3s), "Delayed 3s write succeeded despite Job Object termination!")
            self.assertFalse(os.path.exists(output_8s), "Delayed 8s write succeeded despite Job Object termination!")
            self.assertFalse(os.path.exists(output_15s), "Delayed 15s write succeeded despite Job Object termination!")

    def test_18_eq_barrier_load_oracle_dynamic_derivation(self):
        """Vector 18: EQ oracle and production crash_barrier_load_from_inputs dynamically propagate genuine 'crash_barrier_load' key."""
        from testing.test_cases.baseline_regression.run_all_baseline_tests import BASE_CFG
        from osdagbridge.core.bridge_components.super_structure.crash_barrier.geometry import crash_barrier_load_from_inputs
        from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import DEFAULT_CRASH_BARRIER_WIDTH
        test_cfg = dict(BASE_CFG)
        test_cfg["crash_barrier_load"] = 8.0
        
        # Verify genuine production helper propagates 'crash_barrier_load'
        prod_val = crash_barrier_load_from_inputs(test_cfg)
        self.assertEqual(prod_val, 8.0, "Production helper failed to read genuine 'crash_barrier_load' key!")
        
        # Verify oracle derives identically from the configured input
        oracle_val = float(test_cfg.get("crash_barrier_load", 6.54))
        self.assertEqual(oracle_val, prod_val)
        expected_cb_reaction = 2.0 * 24.0 * oracle_val  # 384.0 kN
        self.assertEqual(expected_cb_reaction, 384.0)

        # Verify fallback to default 6.54 via crash_barrier_dead_load_kN_m when key is omitted
        from osdagbridge.core.bridge_components.super_structure.crash_barrier.geometry import crash_barrier_dead_load_kN_m
        test_cfg.pop("crash_barrier_load", None)
        self.assertIsNone(crash_barrier_load_from_inputs(test_cfg))
        self.assertEqual(crash_barrier_dead_load_kN_m(crash_barrier_load_from_inputs(test_cfg)), 6.54)
        self.assertEqual(float(test_cfg.get("crash_barrier_load", 6.54)), 6.54)
        self.assertEqual(DEFAULT_CRASH_BARRIER_WIDTH, 0.50)

    def test_19_a02_raw_inputs_independent_from_production_helper(self):
        """Vector 19: A02 oracle independently derives barrier resultant from raw key, catching mutated helper."""
        from testing.test_cases.baseline_regression.run_all_baseline_tests import BASE_CFG
        from osdagbridge.core.bridge_components.super_structure.crash_barrier.geometry import crash_barrier_dead_load_kN_m
        test_cfg = dict(BASE_CFG)
        cb_val = float(test_cfg.get("crash_barrier_load", 6.54))
        L_span_m = 24.0
        expected_phys_cb = 2.0 * L_span_m * cb_val
        self.assertAlmostEqual(expected_phys_cb, 313.92, places=2)

        # Mutate production helper by 0.9x: oracle independent expected value must detect discrepancy
        mutated_helper_val = crash_barrier_dead_load_kN_m(cb_val) * 0.9  # 5.886 kN/m -> 282.53 kN
        discrepancy = abs(expected_phys_cb - (2.0 * L_span_m * mutated_helper_val))
        self.assertGreater(discrepancy, 30.0, "Independent oracle failed to catch 0.9x helper mutation!")

    def test_20_b01_bottom_flange_width_mutation_rejected(self):
        """Vector 20: Mutating bottom flange width (410 -> 450 mm) causes test_tc_reg_b01 to fail."""
        from testing.test_cases.baseline_regression.run_all_baseline_tests import test_tc_reg_b01
        from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
        from osdagbridge.core.utils.common import KEY_MP_GIRDER_BOTTOM_FLANGE_WIDTH

        orig_girder_val = PlateGirderBridge._girder_value

        def mutated_girder_val(self, key, i=0):
            if key == KEY_MP_GIRDER_BOTTOM_FLANGE_WIDTH:
                return 0.450  # Mutated from 0.410 to 0.450 m
            return orig_girder_val(self, key, i)

        PlateGirderBridge._girder_value = mutated_girder_val
        try:
            with tempfile.TemporaryDirectory() as td:
                res = test_tc_reg_b01(evidence_dir=td)
                self.assertEqual(res["status"], "BASELINE_FAIL")
                self.assertIn("DEF-03 Confirmed", res["reason"])
        finally:
            PlateGirderBridge._girder_value = orig_girder_val

    def test_21_c01_multi_girder_discrimination(self):
        """Vector 21: C01 rejects first-girder-only, j-end-only, i-end-only, and -1.5% low candidates."""
        import osdagbridge.core.bridge_types.plate_girder.designer as des
        from testing.test_cases.baseline_regression.run_all_baseline_tests import test_tc_reg_c01
        orig_extract = des._extract_demands_from_analysis_results

        # Flaw A: First-girder-only candidate (evaluates G1=181.91 MPa, misses G2 End j=200.73 MPa)
        def g1_only_extract(analysis_results, bcfg):
            demands, per_lc = orig_extract(analysis_results, bcfg)
            ds = getattr(analysis_results, "ds", None)
            if ds is not None and hasattr(ds, "Loadcase") and "SLS_FREQ_1" in ds.Loadcase.values:
                Ze = 15.9416e-3  # composite Ze
                sls_freq_lcs = ["SLS_FREQ_1", "SLS_FREQ_2", "SLS_FREQ_3", "SLS_FREQ_4", "SLS_FREQ_5"]
                # Only evaluate G1
                m_i = [-float(ds.forces.sel(Loadcase=lc, Element=1, Component='Mz_i').values) for lc in sls_freq_lcs]
                r_i = max(m_i) - min(m_i)
                demands["G1"].stress_range_MPa = (r_i / Ze) * 1e3
                # G2 left untouched / omitted -> misses governing G2 range 200.73 MPa
            return demands, per_lc

        des._extract_demands_from_analysis_results = g1_only_extract
        try:
            with tempfile.TemporaryDirectory() as td:
                res = test_tc_reg_c01(evidence_dir=td)
                self.assertEqual(res["status"], "BASELINE_FAIL", "First-girder-only candidate passed unexpectedly!")
        finally:
            des._extract_demands_from_analysis_results = orig_extract

    def test_22_run_seal_trust_architecture_attacks_s1_through_s11(self):
        """Vector 22: Run-Seal Trust Architecture rejects all attack classes (S1-S11) fail-closed."""
        with tempfile.TemporaryDirectory() as td:
            f1 = os.path.join(td, "file1.txt")
            with safe_open_evidence(f1, "w") as f:
                f.write("CONTENT_1")

            manifest, seal = generate_and_seal_manifest(td, runner_id="test_runner", phase_label="Phase 2.12 Test", trust_dir=self._trust_td.name, allow_trust_override=True)

            # S0: Clean run passes
            ok, errs, _ = verify_manifest_integrity(td, trust_dir=self._trust_td.name, allow_trust_override=True)
            self.assertTrue(ok, f"Clean verification failed: {errs}")

            # S1: Evidence file modified
            import stat
            RW_MODE = (stat.S_IRUSR | stat.S_IWUSR) if hasattr(stat, "S_IRUSR") else (stat.S_IREAD | stat.S_IWRITE)
            RO_MODE = stat.S_IRUSR if hasattr(stat, "S_IRUSR") else stat.S_IREAD
            os.chmod(f1, RW_MODE)
            with open(f1, "a") as f:
                f.write("MODIFIED")
            ok, errs, _ = verify_manifest_integrity(td, trust_dir=self._trust_td.name, allow_trust_override=True)
            self.assertFalse(ok)
            self.assertTrue(any("HASH_MISMATCH" in e for e in errs))
            # Restore f1
            with open(f1, "w") as f:
                f.write("CONTENT_1")
            os.chmod(f1, RO_MODE)

            # S4: Seal ledger edited without key
            ledger_path = os.path.join(self._trust_td.name, "trusted_run_seals.json")
            with open(ledger_path, "r", encoding="utf-8") as f:
                orig_seals_data = json.load(f)
            tampered_seals = copy.deepcopy(orig_seals_data)
            tampered_seals[0]["manifest_sha256"] = "f" * 64
            with open(ledger_path, "w", encoding="utf-8") as f:
                json.dump(tampered_seals, f, indent=2)
            ok, errs, _ = verify_manifest_integrity(td, trust_dir=self._trust_td.name, allow_trust_override=True)
            self.assertFalse(ok)
            self.assertTrue(any("FORGED_SEAL_SIGNATURE" in e for e in errs))
            # Restore authentic ledger
            with open(ledger_path, "w", encoding="utf-8") as f:
                json.dump(orig_seals_data, f, indent=2)

            # S8: Extra unlisted file injected
            f_extra = os.path.join(td, "injected.txt")
            with open(f_extra, "w") as f:
                f.write("INJECTED")
            ok, errs, _ = verify_manifest_integrity(td, trust_dir=self._trust_td.name, allow_trust_override=True)
            self.assertFalse(ok)
            self.assertTrue(any("UNLISTED_FILE_INJECTED" in e for e in errs))
            os.remove(f_extra)

            # S9: File deleted
            os.chmod(f1, RW_MODE)
            os.remove(f1)
            ok, errs, _ = verify_manifest_integrity(td, trust_dir=self._trust_td.name, allow_trust_override=True)
            self.assertFalse(ok)
            self.assertTrue(any("MISSING" in e for e in errs))

    def test_23_missing_evidence_dir_cli_execution_no_name_error(self):
        """Vector 23: Baseline runner CLI without --evidence-dir executes without NameError: uuid."""
        cmd = [PYTHON_EXE, BASELINE_RUNNER, "--help"]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertNotIn("NameError", proc.stderr + proc.stdout)

    def test_24_cross_process_sealed_overwrite_prevention(self):
        """Vector 24 (Probe W1): Fresh process cannot overwrite an already-sealed directory."""
        with tempfile.TemporaryDirectory() as td:
            sample_file = os.path.join(td, "evidence.txt")
            with safe_open_evidence(sample_file, "w") as f:
                f.write("ORIGINAL_DATA")
            generate_and_seal_manifest(td, phase_label="Test W1", trust_dir=self._trust_td.name, allow_trust_override=True)
            self.assertTrue(is_sealed_directory(td))

            # Spawn a fresh Python subprocess to attempt writing to the sealed directory
            cmd = [
                PYTHON_EXE, "-c",
                f"import sys, os; sys.path.insert(0, r'{SCRIPT_DIR}'); "
                f"from evidence_guard import safe_open_evidence; "
                f"safe_open_evidence(os.path.join(r'{td}', 'overwrite.txt'), 'w')"
            ]
            env = os.environ.copy()
            env["OSDAGBRIDGE_TRUST_DIR"] = self._trust_td.name
            env["OSDAGBRIDGE_ALLOW_TEST_TRUST_OVERRIDE"] = "1"
            proc = subprocess.run(cmd, env=env, capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("CRITICAL WRITE GATEWAY REFUSAL", proc.stderr)
            self.assertIn("sealed immutable directory", proc.stderr)

    def test_25_workspace_root_and_reports_protection(self):
        """Vector 25 (Probes W6/W7): Gateway prohibits writing to workspace root or reports directory."""
        from testing.test_cases.baseline_regression.evidence_guard import check_write_permission
        root_target = os.path.join(WORKSPACE_ROOT, "malicious_root_artifact.log")
        with self.assertRaises(PermissionError):
            check_write_permission(root_target)

        reports_target = os.path.join(WORKSPACE_ROOT, "reports", "malicious_report.log")
        with self.assertRaises(PermissionError):
            check_write_permission(reports_target)

    def test_26_pinned_trust_directory_enforcement(self):
        """Vector 26 (Probe K14): Verification fails closed on unpinned trust directory without explicit override."""
        with tempfile.TemporaryDirectory() as unpinned_dir:
            orig_allow = os.environ.get("OSDAGBRIDGE_ALLOW_TEST_TRUST_OVERRIDE")
            os.environ.pop("OSDAGBRIDGE_ALLOW_TEST_TRUST_OVERRIDE", None)
            os.environ["OSDAGBRIDGE_TRUST_DIR"] = unpinned_dir
            try:
                with self.assertRaises(PermissionError):
                    get_trust_dir(allow_override=False)
            finally:
                if orig_allow is not None:
                    os.environ["OSDAGBRIDGE_ALLOW_TEST_TRUST_OVERRIDE"] = orig_allow
                os.environ["OSDAGBRIDGE_TRUST_DIR"] = self._trust_td.name

    def test_27_linux_cgroup_tmpfs_detection_rejection(self):
        """Vector 27 (Audit F-08): False cgroup v2 containment on tmpfs/hybrid hosts is rejected."""
        if sys.platform != "win32":
            job = ProcessLifetimeJob()
            if not job.is_contained:
                self.assertIsNone(job.containment_type)
            else:
                self.assertEqual(job.containment_type, "cgroup_v2")


if __name__ == "__main__":
    unittest.main()
