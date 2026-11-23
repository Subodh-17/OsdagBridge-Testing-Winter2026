# Phase 2.12 — Remaining Risks (prioritised)

This list covers harness-side risks only. No application source change is implied.

## Critical

1. **Trust anchor is inside the same trust domain (F-07).**
   - The signing key, the seal ledger and the evidence are all writable by the same Windows user.
   - Tampered evidence was certified as authentic in three ways:
     - re-signing with the existing key (K10);
     - replacing the key and re-signing everything (K11);
     - deleting the ledger entry and re-sealing with the harness's own `generate_and_seal_manifest`, without reading the key (K13).
   - The verifier also trusts whatever `OSDAGBRIDGE_TRUST_DIR` points to (K14).
   - Phase 2.12 itself did the K13 operation: it moved the preliminary seals out of the ledger and re-sealed the same directories.
   - Real independence needs a key the evidence-producing user cannot read: a separate account or service, an HSM or OS key store with an access policy, or an append-only external log or transparency service. The verifier also needs a pinned trust location.
2. **The gateway does not prevent overwriting the current sealed evidence (F-06).**
   - The sealed set and the allowlist exist only in memory, per process. Any new process can rewrite `phase_2_12/*` through the official test functions (W1).
   - Workspace root and `reports/` writes are allowed.
   - Plain `open()` and `copy()` are unmediated.
   - The verifier only detects tampering after the fact.

## High

3. **Windows containment is not demonstrated (F-09).**
   - No preserved output exists for the claimed 6/6 run.
   - The validation script cannot demonstrate assign-before-execute (Check 1).
   - The script cannot detect 8, 15 or 30 s writes either: it waits only 4 s after terminating the job (Check 5).
   - Windows symlink and TOCTOU vectors (5, 13, 15) were skipped; junctions were never tested.
4. **Linux capability detection is unsafe on root and CI hosts (F-08).**
   - A writable tmpfs at `/sys/fs/cgroup` is accepted as cgroup v2, and the harness reports containment that does not exist.
   - The child is joined to the cgroup only after it starts, and join failures are ignored.
   - Under these conditions Vector 17 fails and cgroup directories leak.
   - Non-root Linux correctly reports BLOCKED, but **Linux has no containment capability at all**, so FS cannot be verified on Linux.
5. **Provenance (F-12).**
   - The preliminary runs wrote into the official directories, and their evidence was deleted.
   - The ledger was edited.
   - Transcripts are missing for the Windows containment run, the governance runs and the preliminary runs.
   - The Phase 2.11 rerun time is misreported (12:48 vs the sealed 12:44:30–12:45:36).

## Medium

6. **Governance suite coverage (N-1, N-2).**
   - Three attack tests are skipped on each platform: 5, 13 and 15 on Windows; 9, 16 and 17 on Linux.
   - Vector 22 omits the same-user attacks K10, K11, K13 and K14.
7. **EQ/A02.**
   - Barrier width is the production constant, so the application's silent disregard of `typical_section.crash_barrier.width` is not flagged.
   - A02 accepts component errors up to 1 %.
8. **C01.**
   - The expected stresses embed production's composite Z<sub>b</sub> (m = 7.5).
   - The 0.8 % tolerance is not derived, and −0.7 % passes.

## Low

9. RPT and B01 threshold resolution (0.001; stated tolerance bands).
10. Root runs leave the false-cgroup directories under `/sys/fs/cgroup`.

## Unchanged platform limitation

TC-REG-FS is verifiable only on Windows, and the Windows evidence was not independently reproduced.
