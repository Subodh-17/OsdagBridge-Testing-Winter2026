# Phase 2.13 — Evidence Trust Architecture & Threat Model Specification

**Project:** FOSSEE OsdagBridge — Baseline Regression & Verification Harness  
**Workspace Root:** `F:\FOSSEE internship`  
**Application Repo:** `source\OsdagBridge` on branch `dev` (`d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`)  
**Controlling Audit:** `reports/PHASE_2_12_FINAL_INDEPENDENT_GATE_AUDIT.md`  
**Date:** 2026-11-17  
**Author:** Structural Engineering Software QA & Test-Infrastructure Team  

---

## 1. Executive Summary & Architectural Reorientation

In Phase 2.12, independent gate auditor Claude identified a fundamental architectural limitation:
> *"The trust store is outside the repository, not outside the trust domain. An HMAC with a co-located symmetric key is integrity, not independently anchored trust."* (Claude Phase 2.12 Audit §3, §10)

Under Phase 2.12's architecture, HMAC-SHA256 signatures were generated using a 32-byte symmetric key stored in `%USERPROFILE%\.osdagbridge_trust\seal_signing_key.bin`. While this anchored run records outside the Git repository workspace, the key, the seal ledger, and the evidence files were all owned by the same local operating system user account (`Subodh`). Consequently, any Python process executing under that user account possessed sufficient operating system privileges to:
1. Re-sign tampered evidence with the existing key (Probe K10);
2. Replace the key and re-sign all ledger entries (Probe K11);
3. Delete an entry from the ledger and re-seal using the harness's own functions without reading the key (Probe K13);
4. Redirect the verification utility using the `OSDAGBRIDGE_TRUST_DIR` environment variable (Probe K14).

Phase 2.13 resolves this defect by establishing an **honest, four-tier threat model**, explicitly acknowledging what a local test harness running under a single OS user account can and cannot cryptographically enforce, pinning verification trust anchors, enforcing cross-process seal persistence, applying OS-level filesystem protections, and defining the requirements for external trust authorities.

---

## 2. Four-Tier Threat Model & Security Boundaries

```
+---------------------------------------------------------------------------------------+
| TIER 4: EXTERNAL TRUST AUTHORITY / INDEPENDENT OFFLINE AUDITOR                        |
|  - Cryptographic Boundary: Asymmetric Public/Private Keys (Auditor holds private key) |
|  - Transparency: Immutable remote append-only log / Git signed commits / HSM           |
|  - Protection: Cryptographic non-repudiation (requires external authority; NOT in Tier 3) |
+---------------------------------------------------------------------------------------+
                                           ^
                                           | Verification / Attestation
+---------------------------------------------------------------------------------------+
| TIER 3: SAME-USER LOCAL EXECUTION DOMAIN (Windows User: 'Subodh')                     |
|  - Threat: Arbitrary Python code / malicious scripts executing under the same user   |
|  - Reality: Same user possesses OS ACL rights to overwrite files, keys, and ledgers   |
|  - Honest Boundary: Symmetric HMAC provides INTERNAL TAMPER DETECTION against       |
|    accidental drift and uncoordinated edits, NOT a security boundary against the user |
+---------------------------------------------------------------------------------------+
                                           ^
                                           | Enforcement Gateway & OS Attributes
+---------------------------------------------------------------------------------------+
| TIER 2: SUPPORTED HARNESS INTERFACES & RUNNER ENTRYPOINTS                             |
|  - Threat: Regression tests, candidate mutations, or logging routines writing data   |
|  - Protection: Centralized write gateway (SafeFileWrapper, check_write_permission)    |
|  - Defenses: Path canonicalization, traversal checks, allowlists, persistent sealed   |
|    directory checks, workspace root refusal, reports/ refusal, OS read-only chmod     |
+---------------------------------------------------------------------------------------+
                                           ^
                                           | Path Canonicalization & Non-Destructive Staging
+---------------------------------------------------------------------------------------+
| TIER 1: ACCIDENTAL CORRUPTION & CONCURRENT FILESYSTEM RACES                           |
|  - Threat: File truncation, TOCTOU symlink/junction races, accidental overwrites      |
|  - Protection: O_EXCL staging files, atomic os.replace, realpath re-validation       |
+---------------------------------------------------------------------------------------+
```

### 2.1 Detailed Tier Definitions

#### Tier 1: Accidental Corruption & Concurrent Filesystem Races
- **Scope:** Normal harness operations, concurrent runner invocations, filesystem race conditions, and accidental target collisions.
- **Enforcement Mechanisms:**
  - `SafeFileWrapper` writes exclusively to temporary hidden staging files (`.filename.tmp_<uuid>`) using `os.O_CREAT | os.O_EXCL | os.O_WRONLY`.
  - Directory and destination safety are verified *both before opening* and *immediately before commit*.
  - Final commit is performed via atomic `os.replace`. If an exception occurs, the staging file is unlinked, leaving the original destination completely intact and untruncated.
- **Threats Mitigated:** TOCTOU symlink/junction redirection during write, partial writes on interruption, accidental file truncation before safety validation.

#### Tier 2: Supported Harness Interfaces & Runner Entrypoints
- **Scope:** All test functions, loggers, runners, and subagent scripts operating within the test framework.
- **Enforcement Mechanisms:**
  - Centralized write gateway: all write paths must pass through `check_write_permission(filepath)`.
  - Canonicalization via `os.path.realpath` resolves symlinks, directory junctions, and path traversal (`..`).
  - Protected historical phase directories (`phase_1d` through `phase_2_12`, `phase_2_baseline`, `phase_2_repaired`) are hardcoded and rejected fail-closed.
  - Workspace root (`WORKSPACE_ROOT`) and repository root (`source/OsdagBridge`) writes are strictly prohibited.
  - Audit reports directory (`reports/`) is immutable to test execution; tests cannot write or modify audit reports.
  - Persistent sealed directory enforcement: target directories are checked against in-memory sets, on-disk `.sealed` markers, and the trust store ledger across fresh processes.
  - Filesystem read-only attributes (`stat.S_IREAD` / `FILE_ATTRIBUTE_READONLY`) applied to sealed files as an accidental-overwrite deterrent.
- **Threats Mitigated:** Direct test-function calls targeting historical phases, accidental reuse of populated directories, fresh process overwriting sealed evidence (Probe W1), test runs mutating reports or application source code.

#### Tier 3: Same-User Local Execution Domain
- **Scope:** Any script, Python interpreter, or binary executing under the same OS user principal (`Subodh`).
- **Cryptographic Reality & Honest Boundary Definition:**
  - Because the signing key (`seal_signing_key.bin`), the ledger (`trusted_run_seals.json`), and the evidence files all reside in filesystem paths accessible to the user `Subodh`, **no local symmetric HMAC algorithm can prevent code running as that user from modifying evidence and re-signing it.**
  - An HMAC proves *authenticity* only to an external verifier who possesses the symmetric key when the evidence producer *does not possess the key*. When the producer and the verifier share the same key on the same user account, the HMAC serves as an **integrity verification and tamper-detection tool** against accidental drift, out-of-band file editing, and uncoordinated modifications.
  - **Explicit Architectural Statement:** We do *not* claim that local symmetric HMAC creates an independent cryptographic security boundary against malicious code executing within the `Subodh` user session. Claims of "tamper-proof security" within a single user domain are mathematically impossible without separate OS credentials or hardware boundaries.

#### Tier 4: Separate Privileged Principal & External Trust Authority
- **Scope:** Independent third-party verification, offline gate audits (such as Claude's independent audits), and formal acceptance.
- **Requirements for Independent Trust:**
  1. **Asymmetric Key Pairs:** Signing keys should use asymmetric cryptography (e.g., Ed25519 or ECDSA). The private signing key must reside exclusively on an isolated service, separate OS account with restricted DACLs, or Hardware Security Module (HSM). The public key is published and pinned for verifiers.
  2. **Append-Only Transparency Logs:** Evidence hashes and run records must be committed to an append-only transparency log (e.g., Sigstore/Rekor, Certificate Transparency style log, or a remote Git commit signed by a dedicated CI bot) where the local user has no update or delete permissions.
  3. **Pinned Verifier Anchors:** The verifier must strictly reject unauthenticated trust directory redirects (`OSDAGBRIDGE_TRUST_DIR`) unless an explicit security override flag is supplied for unit testing.

---

## 3. Persistent Cross-Process Seal Enforcement (Remediating Probe W1)

### 3.1 Defect Analysis in Phase 2.12
In Phase 2.12, `_SEALED_DIRECTORIES` was maintained as an in-memory Python `set()`. When an independent test function was called directly in a fresh Python process:
```bash
python -c "import run_all_baseline_tests as R; R.test_tc_reg_a01(evidence_dir='testing/evidence/phase_2_12/baseline')"
```
The fresh process initialized with an empty `_SEALED_DIRECTORIES` set. Because `phase_2_12` was the active phase (and therefore not in `HARDCODED_PROTECTED_PHASES`), the gateway allowed the write, overwriting sealed evidence files.

### 3.2 Phase 2.13 Multi-Layered Persistent Protection (Tier 2 Scope)
Phase 2.13 implements three orthogonal layers of defense that guarantee sealed evidence cannot be overwritten through any supported harness interface (Tier 2):

> [!NOTE]
> **Explicit Tier 3 Same-User Limitation:** These layers do *not* guarantee that an arbitrary same-user process cannot overwrite or manipulate evidence. A script or user command executing within the same OS user domain (`Subodh`) possesses discretionary permissions to delete `.sealed` markers, remove read-only file attributes, alter `trusted_run_seals.json`, or re-sign modified directories with the local symmetric key. In-session protection is strictly limited to accidental overwrites (Tier 1) and supported harness gateway enforcement (Tier 2). Universal immutability, tamper-proof storage, and independent non-repudiation require an external authority (Tier 4).

1. **Persistent On-Disk Marker (`.sealed`):**
   Upon completion of manifest generation, `evidence_guard.py` writes a `.sealed` marker file into the evidence directory containing the run UUID and ISO 8601 UTC timestamp. `is_sealed_directory(path)` checks for this marker in the target directory and all ancestor directories up to the drive root.
2. **Persistent Ledger Lookup:**
   `is_sealed_directory(path)` dynamically reads `trusted_run_seals.json` from the pinned trust store. Any path matching or residing inside an existing seal's `evidence_dir` is immediately recognized as sealed and immutable.
3. **Filesystem Read-Only File Attributes (Accidental Overwrite Deterrent):**
   Upon sealing, `evidence_guard.py` applies filesystem read-only attributes via `os.chmod(fp, stat.S_IREAD)` (setting `FILE_ATTRIBUTE_READONLY` on Windows). This deters accidental modifications and unmediated `open(filepath, "w")` calls by unprivileged processes. However, this is NOT an immutable kernel security boundary against malicious local execution: on Windows or POSIX, the file owner (or root) can reset write permissions via `os.chmod(fp, stat.S_IRUSR | stat.S_IWUSR)` (`0o600`) (Tier 3). Any such post-seal modification is detected after the fact by `verify_manifest_integrity` via SHA-256 hash mismatch, provided the adversary does not also re-seal using the local symmetric key (as described in §3.2 above). Read-only attributes alone do not prevent an intentional same-user attacker from mutating files or re-computing local HMAC seals.

---

## 4. Pinned Trust Store Architecture (Remediating Probe K14)

### 4.1 Vulnerability in Phase 2.12
In Phase 2.12, `verify_manifest.py` and `evidence_guard.py` unconditionally honored the `OSDAGBRIDGE_TRUST_DIR` environment variable:
```python
trust_env = os.environ.get("OSDAGBRIDGE_TRUST_DIR")
if trust_env and str(trust_env).strip():
    return os.path.realpath(os.path.abspath(str(trust_env).strip()))
```
An attacker could redirect verification to an arbitrary temporary directory containing an attacker-generated key and ledger, certifying tampered evidence as authentic.

### 4.2 Phase 2.13 Pinning Enforcement
Phase 2.13 cryptographically pins the trust store location:
- **Pinned Official Location:** `%USERPROFILE%\.osdagbridge_trust` (Windows) / `~/.osdagbridge_trust` (POSIX).
- **Production Mode:** If `OSDAGBRIDGE_TRUST_DIR` is set to any path other than the pinned location, `get_trust_dir()` raises a fail-closed `PermissionError`:
  ```
  CRITICAL TRUST PINNING VIOLATION: OSDAGBRIDGE_TRUST_DIR override '...' is active,
  but unpinned trust directories are disallowed in production mode.
  Expected pinned store: C:\Users\Subodh\.osdagbridge_trust
  ```
- **Isolated Test Mode:** Overrides are permitted *only* when the environment explicitly sets `OSDAGBRIDGE_ALLOW_TEST_TRUST_OVERRIDE=1` or when the CLI verifier is invoked with `--allow-unpinned-trust-dir`. Under these conditions, the verifier explicitly emits a prominent security warning:
  ```
  [SECURITY WARNING] Running with UNPINNED trust directory override: ...
  ```

---

## 5. Linux Process Containment Probing (Remediating Audit F-08)

### 5.1 Defect Analysis in Phase 2.12
In Phase 2.12, Linux capability detection tested `/sys/fs/cgroup` writability:
```python
if os.path.exists(cgroup_v2_root) and os.access(cgroup_v2_root, os.W_OK):
    os.mkdir(cg_path)
    self.is_contained = True
    self.containment_type = "cgroup_v2"
```
On root or CI hosts with cgroup v1 or hybrid setups where `/sys/fs/cgroup` is mounted as a writable `tmpfs`, `os.mkdir` succeeded on `tmpfs`. The harness falsely reported `cgroup_v2` containment. Because `tmpfs` lacks cgroup controller semantics, `cgroup.procs` acted as a regular file, `cgroup.kill` did nothing, Vector 17 failed, and leaked directories remained.

### 5.2 Phase 2.13 Verified Mount Probing
In Phase 2.13, `ProcessLifetimeJob` implements three mandatory verification checks before claiming Linux containment:
1. **Filesystem Mount Type Verification:**
   Inspects `/proc/mounts` or `/proc/self/mountinfo` specifically for the mount point `/sys/fs/cgroup` having filesystem type `cgroup2`. Plain `tmpfs`, `sysfs`, or `cgroup` (v1) mounts are immediately rejected.
2. **Controller Hierarchy Verification:**
   Asserts that `/sys/fs/cgroup/cgroup.controllers` exists and is readable, proving the cgroup v2 unified hierarchy is active.
3. **Kernel Procs Creation Check:**
   When a trial or container cgroup directory is created via `os.mkdir`, the kernel automatically populates it with control files. `ProcessLifetimeJob` verifies that `cgroup.procs` exists *as generated by the kernel*. If not, the directory was created on a plain filesystem, and the harness immediately cleans up and sets `is_contained = False`.
4. **Assign-Before-Execute in `preexec_fn`:**
   When `cgroup_v2` is active, child processes are assigned to `cgroup.procs` inside `subprocess.Popen`'s `preexec_fn` callback (after `fork()` but before `exec()`). If assignment fails, the child raises an exception before executing the target binary, eliminating the race condition.

---

## 6. Windows Win32 Job Object Containment & Empirical Validation

### 6.1 Win32 Job Object Process Containment Design
On Windows, `ProcessLifetimeJob` utilizes the Win32 Job Object subsystem:
- Created with `CreateJobObjectW(None, None)`.
- Configured with `JobObjectExtendedLimitInformation` setting `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x2000`.
- Breakaway flags (`JOB_OBJECT_LIMIT_BREAKAWAY_OK`, `JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK`) are omitted, ensuring child processes cannot spawn uncontained descendants.
- Process creation hooks `_winapi.CreateProcess` under a threading lock, injecting `CREATE_SUSPENDED = 0x00000004`.
- The child process is assigned to the Job Object via `AssignProcessToJobObject` *while suspended*.
- Only after assignment is verified does `ResumeThread` resume the primary thread.

### 6.2 Empirical Validation Script (`validate_windows_containment.py`)
To resolve Claude's findings in F-09:
1. **Check 1 (Assign-Before-Execute Proof):**
   Spawns a child process whose very first instruction writes a marker file. While the child is suspended, the test verifies that:
   - Marker does *not* exist;
   - `AssignProcessToJobObject` succeeds;
   - Job Object process count increments to $\ge 1$;
   - Marker *still* does not exist;
   - Only after `ResumeThread` does the marker appear.
   This empirically proves zero instructions execute prior to Job assignment.
2. **Check 5 (Delayed-Write Full-Horizon Observation):**
   Spawns a child script with scheduled writes at 3s, 8s, 15s, and 30s. The Job Object is terminated at $t = 0.5\text{ s}$. The test observes the filesystem across the complete 32-second horizon, confirming at $t = 4.5\text{ s}$, $t = 9.5\text{ s}$, $t = 16.5\text{ s}$, and $t = 31.5\text{ s}$ that none of the files (`w3.txt`, `w8.txt`, `w15.txt`, `w30.txt`) were ever created.

---

## 7. Windows Directory Junction Support for Attack Vectors

In earlier phases, attack tests simulating directory swaps and TOCTOU races (Vectors 5, 13, 15) attempted `os.symlink()`. On Windows, standard non-administrator accounts cannot create directory symlinks without Developer Mode enabled, causing these tests to be skipped.

In Phase 2.13, `create_dir_alias()` utilizes Windows directory junctions via `_winapi.CreateJunction(target, link_path)` on Windows, falling back to `os.symlink()` on POSIX. Because directory junctions:
- Do not require administrator privileges or Developer Mode;
- Point to target directory paths via NT reparse points;
- Resolve via `os.path.realpath()`;
- Are detected by `is_symlink_or_junction()` via `FILE_ATTRIBUTE_REPARSE_POINT` (0x400);

Vectors 5, 13, and 15 execute completely on standard Windows accounts without skips, demonstrating robust TOCTOU non-truncation defenses across all platforms.
