# Phase 2.12 — Final Independent Gate Audit

**Project:** FOSSEE OsdagBridge — baseline regression and sensitivity harness
**Workspace:** `F:\FOSSEE internship` · **Application repo:** `source\OsdagBridge`, `dev` @ `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`
**Evidence audited:** `testing\evidence\phase_2_12\`, plus the trust store `C:\Users\Subodh\.osdagbridge_trust` (read-only access granted for this audit)
**Controlling audit:** `reports\PHASE_2_11_FINAL_INDEPENDENT_GATE_AUDIT.md` (`26bd4182f45a158c…`)
**Auditor:** Claude (independent) · **Date:** 2026-11-17

**Companion documents:**
- `PHASE_2_12_FINDING_BY_FINDING_VERDICT.md` — the per-finding table;
- `PHASE_2_12_REPRODUCTION_RESULTS.md` — commands, hashes and raw outcomes;
- `PHASE_2_12_REMAINING_RISKS.md` — prioritised risk list.

**Mode:** audit only.
- No source, harness, evidence, manifest, ledger or database was modified. No commit, push or branch change. Phase 3 was not started.
- Destructive probes ran only in fresh disposable clones (`/tmp/ws212*`), each with its own disposable trust directory.
- The real signing key was read on the device to verify the HMACs and was **not** copied off the device.

Labels used throughout:
- **REPRODUCED** — I executed it and checked disk state and hashes afterwards;
- **CODE REVIEW** — I inspected the implementation only;
- **UNVERIFIED / BLOCKED** — I could not execute it.

---

## 1. Executive verdict

# **REJECTED**

Phase 2.12 fixes several Phase 2.11 defects for real, and each was reproduced:
- the gateway no longer truncates or empties protected files under a TOCTOU swap (Linux);
- the verifier now fails closed on missing, corrupt, forged and relabelled seals and on copied directories;
- the EQ/A02 barrier oracle now uses the real application key and catches production ignoring it;
- C01 now discriminates the girder, end and −1.0 % / −1.5 % shortcuts;
- non-root Linux honestly reports FS as **BLOCKED**;
- live transcripts exist for the official runs.

Material defects remain:

1. **The HMAC seal is not an independent trust anchor.** The same Windows user owns the key, the ledger and the evidence. Tampered evidence verified as authentic after:
   - re-signing with the existing key (K10);
   - replacing the key and re-signing (K11);
   - deleting the ledger entry and re-sealing with the harness's own function, without reading the key (K13);
   - redirecting the verifier with `OSDAGBRIDGE_TRUST_DIR` (K14).

   Phase 2.12's own workflow used K13: preliminary seals were moved out of the ledger and the same directories re-sealed.
2. **Current sealed evidence can be overwritten.** A direct official test-function call in a new process overwrote sealed `phase_2_12/baseline` evidence. The sealed set and the allowlist are per-process memory. The workspace root and `reports/` are writable, and the gateway is advisory.
3. **Provenance is incomplete.**
   - The preliminary runs reused the official directories, and their evidence was deleted.
   - The ledger was edited.
   - No output was preserved for the Windows containment run or the governance runs.
   - The Phase 2.11 disclosure misstates the rerun time.
4. **Linux capability detection reports false containment as root.** It treats a writable tmpfs as cgroup v2; under that condition the harness's own Vector 17 fails and cgroup directories leak.
5. **Windows containment is BLOCKED.**
   - It was not executable by me, and no output of the claimed 6/6 run is preserved.
   - The validation script cannot demonstrate assign-before-execute, and cannot detect the 8, 15 and 30 s delayed writes it claims to have prevented.
   - The Windows symlink and TOCTOU governance tests were skipped.

---

## 2. Finding-by-finding summary

| Phase 2.11 ID | Claimed remediation | Independent verification | Verdict | Remaining risk |
|---|---|---|---|---|
| F-07 seals | HMAC ledger in `.osdagbridge_trust`; fail-closed verifier | REPRODUCED K0–K15 and real-ledger HMACs | **REJECTED** (as a trust anchor) | Same-user resealing |
| F-06 gateway scope | Allowlist, sealed refusal, src and root refusal, `uuid` fix | REPRODUCED W1–W9; Vector 23 | **REJECTED** | Sealed active evidence overwritable |
| F-05 TOCTOU | Staging + `O_EXCL` + `os.replace` | REPRODUCED W10 (3 swap points), Linux | **ACCEPTED** (Linux) / **NOT VERIFIED** (Windows) | Windows junctions untested |
| F-08 Linux containment | cgroup v2 / namespace probe; BLOCKED otherwise | REPRODUCED non-root (BLOCKED) and root (false cgroup) | **ACCEPTED WITH LIMITATIONS** (non-root) / **REJECTED** (detection) | No Linux containment exists |
| F-09 Windows containment | 6/6 empirical checks | CODE REVIEW; no output preserved | **BLOCKED** | Checks 1 and 5 cannot prove their claims |
| F-10 EQ/A02 barrier | Real `crash_barrier_load`; candidate restored | REPRODUCED X0–X10 | **ACCEPTED WITH LIMITATIONS** | Width from a constant; A02 1 % tolerance |
| F-12 provenance | Execution history; transcripts | REPRODUCED seal/manifest checks; inspected history and ledger | **REJECTED** | Evidence reuse and deletion; ledger edit |
| F-11b C01 | 3,200 kNm G2; 0.8 % tolerance | REPRODUCED C0–C29 | **ACCEPTED WITH LIMITATIONS** | −0.7 % passes; Z<sub>b</sub> embedded |
| F-01–F-04, F-11a, F-11c | Historical integrity; protection; B01; RPT | REPRODUCED | **ACCEPTED** | — |

---

## 3. Seal trust architecture

**Inspected:** `evidence_guard.py` `010c5135…`:
- `get_trust_dir` honours the `OSDAGBRIDGE_TRUST_DIR` environment variable, falling back to `%USERPROFILE%\.osdagbridge_trust`;
- `get_or_create_signing_key` creates a 32-byte key with `0o600`, which on Windows means the current user's ACL;
- `generate_and_seal_manifest` refuses re-sealing only if the ledger already holds the directory, then rewrites the ledger in place with plain `open()`;
- `verify_manifest_integrity` checks the HMAC over a canonical record, the manifest hash and a full directory walk.

**What it protects against:**
- accidental or third-party modification of evidence, the manifest or the seal by a party who cannot read or write the trust directory;
- copying or relabelling evidence (the evidence directory is inside the signature);
- a missing, corrupt or forged ledger;
- unlisted and missing files.

**What it does not protect against:**
- the evidence-producing user, who has full read/write access to the key and the ledger and can therefore re-sign (K10), re-key (K11) or delete-and-re-seal (K13);
- an environment that points `OSDAGBRIDGE_TRUST_DIR` elsewhere (K14).

The trust store is **outside the repository, not outside the trust domain**. An HMAC with a co-located symmetric key is integrity, not independently anchored trust.

**Authoritative ledger on the device:** three official seals, each with a valid HMAC and matching its manifest. The governance tests use a temporary trust directory and did not pollute the ledger. The three preliminary seals were moved to `preliminary_run_seals_phase_2_12.json`; their HMACs are valid, but their manifests are gone.

---

## 4. Gateway and filesystem races

`SafeFileWrapper` now stages to an `O_EXCL` temporary file and commits with `os.replace` after re-validation. In all three swap positions the protected file was untouched (REPRODUCED, Linux). This closes the Phase 2.11 truncation defect on Linux.

Remaining:
- **W1:** sealed active evidence overwritten from a new process.
- **W6 / W7:** workspace root and `reports/` writable.
- **W8 / W9:** raw `open()` and `copy()` are unmediated.
- **Windows:** Vectors 5, 13 and 15 (symlink, TOCTOU, non-truncation) were skipped, so the defences were never executed there. `os.path.islink` does not recognise junctions; only the `realpath` comparison guards that case (CODE REVIEW).

---

## 5. Process containment

### Windows — BLOCKED

**Code review:** `ContainedPopen` ORs in `CREATE_SUSPENDED`, hooks `_winapi.CreateProcess` under a lock, calls `AssignProcessToJobObject(hJob, hProcess)` before `ResumeThread(hThread)`, and terminates and raises on failure. The job uses `KILL_ON_JOB_CLOSE` with no breakaway flags. This design is correct.

**Empirical evidence:** none is preserved, and `validate_windows_containment.py` is itself inadequate:
- **Check 1** asserts only that the child printed and was counted. It cannot show the child executed nothing before assignment.
- **Check 2** (kill-on-close), **Check 3** (breakaway denied, via `PermissionError` on `CREATE_BREAKAWAY_FROM_JOB`) and **Check 6** (termination) are plausible tests, but unreproduced.
- **Check 4** counts at least 2 processes after 1.5 s, which is a reasonable inheritance check but unreproduced.
- **Check 5** terminates the job at 0.5 s and inspects files 4 s later. Its 8, 15 and 30 s writes could not have appeared by then without any containment, so **delayed writes at 8, 15 and 30 s were never tested**.

### Linux — no containment capability

**Non-root:** `is_contained = False`, FS returns **BLOCKED**, the sensitivity gate is 11/12, and governance skips Vectors 9 and 17. This is correct and honest reporting.

**Root:** `/sys/fs/cgroup` is a writable tmpfs (cgroup v1/hybrid), so `os.mkdir` "succeeds" and the harness reports `cgroup_v2`.
- `cgroup.procs` is a plain file, so the process count never reaches 0; FS flags a false detached process.
- `cgroup.kill` does nothing.
- **Vector 17 fails** because the 3 s write succeeded.
- The child is joined to the cgroup only after `Popen` returns, and a failed join is swallowed.

---

## 6. Engineering tests

- **EQ / A02:**
  - The real key `crash_barrier_load` is used, and the invented keys are absent from the harness.
  - Candidate (b) is the production path (`crash_barrier_load_from_inputs`) and serves as the *correct* reference. Candidate (c) is the incorrect, naive one.
  - Production ignoring an input of 8.0 kN/m fails both EQ and A02; correct propagation passes.
  - A wrong helper ×0.9 is caught. Component-wise checks prevent cancellation: each component is asserted separately, as verified in Phase 2.11.
  - **Limitations:** barrier width uses the production constant `DEFAULT_CRASH_BARRIER_WIDTH`, and A02 accepts errors under 1 %.
- **C01:**
  - Independent stresses are 181.92 MPa (G1, 2,900 kNm) and 200.73 MPa (G2, 3,200 kNm), with composite Z<sub>b</sub> = 15.9416 × 10⁶ mm³ (short-term m = 7.5, b<sub>eff</sub> 2,100 mm).
  - Every girder and end shortcut is caught, as are −1.5 % and −1.0 %.
  - −0.7 % passes. The 0.8 % band is a design choice, not an error bound derived from the oracle, and it is not merely the candidate's output.
- **B01:** every geometry mutation beyond the stated tolerance is caught. **ACCEPTED.**
- **RPT:** 29 of 31 shortcuts caught, including every cross-bracing and end-diaphragm 0.999 / 1.000 / 1.001 boundary, missing members, fail-all and narrative-only. **ACCEPTED.**
- **Baseline quality:**
  - The 11 BASELINE_FAIL tests reproduce the defects established in Phases 2.4–2.11.
  - The CAD PASS is justified.
  - D02, C02 and GEO-SLAB are BLOCKED for undecided specifications. These are honest specification gaps, not architectural ones.
  - On Linux, FS is a fourth BLOCKED.

---

## 7. Governance suite (23 tests)

| Platform | Result |
|---|---|
| Windows (reported, not reproduced) | 20 ok, 3 skipped: **Vectors 5, 13, 15**, i.e. the symlink and TOCTOU attack tests |
| Linux non-root (reproduced) | 20 ok, 3 skipped: Vectors 9, 16, 17 (containment and Windows-only) |
| Linux root (reproduced) | 21 ok, 1 skipped (16), **1 FAIL (Vector 17)** |

Skipped tests are not passes. Vector 22 covers seal attacks S1–S11 but none of the same-user attacks (K10, K11, K13, K14).

---

## 8. Provenance

- The official runs have distinct run UUIDs, live stdout and stderr, exit codes and HMAC seals. Their manifests match disk exactly: 19 / 19 / 54 files, no unlisted files.
- `PHASE_2_12_EVIDENCE_MANIFEST.json` and `PHASE_2_12_RUN_SEALS.json` are consistent with disk and with the ledger.

Defects:
- The preliminary Runs 3 and 4 used the **same official directories**. Their evidence was deleted and their seals removed from the authoritative ledger, which is undisclosed manual ledger surgery.
- No preserved output exists for the Windows containment run (Run 1), the governance runs (Runs 2 and 5) or the preliminary runs.
- The Phase 2.11 historical note says the rerun was at 12:48; the seals show 12:44:30–12:45:36.

---

## 9. Repository and database integrity (device, read-only)

| Item | Observed |
|---|---|
| Branch / HEAD | `dev` / `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` |
| Locks | No `.git/*.lock` |
| `.git/index` mtime | 2026-11-15 12:26:18 (unchanged) |
| Source aggregate | 282 files, `7c9294813b58fb84ecd965643daec240276747d1788b13187c0e0f46c52b024c` = baseline |
| Files under `src/` modified after 11:40 UTC | 0 |
| `weather.sqlite` | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` ✓ |
| `Intg_osdag.sqlite` | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` ✓ |
| Historical evidence | Phases 2.5, 2.7, 2.8, 2.9, 2.10 and 2.11 match their manifests. Phase 2.6 is unchanged apart from its two known-lost baseline logs. No historical file changed during Phase 2.12. |

**ACCEPTED.** The application is untouched.

---

## 10. Overall verdict

# **REJECTED**

Material defects remain:
- the trust anchor (F-07);
- gateway prevention scope (F-06);
- provenance (F-12);
- Linux capability detection (F-08, root).

The essential Windows containment evidence (F-09) is BLOCKED.

Before the harness can be called trustworthy:
1. Anchor the seals in a key or log the evidence-producing user cannot write, and pin the verifier's trust location.
2. Make sealed directories immutable across processes, for example by consulting the ledger at write time and setting OS read-only ACLs after sealing.
3. Preserve every run's output, and never reuse an official directory for preliminary work.
4. Fix the Linux detection: require `cgroup2fs`, and join the cgroup before the child executes.
5. Re-run the Windows checks with valid designs (a write-after-PASS test that waits more than 30 s; a pre-assignment execution probe) and the Windows junction and TOCTOU vectors, preserving all output.

**Phase 3 is not authorized** by this audit; that decision rests with the project owner.
