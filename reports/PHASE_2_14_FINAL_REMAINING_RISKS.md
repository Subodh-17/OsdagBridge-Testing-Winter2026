# Phase 2.14 — Final Remaining Risks

These are harness-side risks only; none implies an application source change. They are ordered by what blocks a full **ACCEPTED** first.

## Gating (keep the verdict at CONDITIONALLY ACCEPTED)

1. **Windows containment and the 27-vector Windows suite have not been run by anyone other than the party being audited.**
   - Both Phase 2.14 transcripts are host-native, verbose and consistent with code I reviewed.
   - But no independent party has executed them, and the transcripts are unsealed and carry no timestamps.
   - **Close by:** the project owner (or the auditor, using desktop computer-use on the owner's machine) runs the two commands below in a fresh terminal, captures raw output with timestamps and the exit code, and seals or hashes the output.

     ```
     python -u testing/test_cases/baseline_regression/validate_windows_containment.py
     python -u testing/test_cases/baseline_regression/test_evidence_governance.py -v
     ```

2. **Windows Check 5 cannot rule out a writer that "never really started".**
   - Liveness at 0.5 s is printed but not asserted.
   - There is no start marker, no positive-control run (same probe, uncontained, producing w3 at about 3 s), and no measured timestamps.
   - **Close by:** assert `cnt >= 1`; have the probe write a start marker; add an uncontained control run; record `time.monotonic()` for each observation.

3. **One residual overclaim.**
   - `PHASE_2_13_SECURITY_ARCHITECTURE.md` §3.2 says the three layers "guarantee sealed evidence cannot be overwritten from any process".
   - Same-user processes can do exactly that (2.13 probes D5/D6/D7).
   - **Close by:** limit the sentence to "any supported harness interface (Tier 2)".

## Non-gating

4. **Same-user tamper/reseal (Tier 3) remains possible by design.**
   - It is disclosed honestly. HMAC here is integrity/tamper-evidence only; there is no non-repudiation without an external authority (Tier 4, not implemented).
5. **POSIX portability of the governance suite.**
   - Tests 10 and 22 ERROR on Linux non-root because `os.chmod(f, stat.S_IWRITE)` makes the file write-only (`0o200`). Use `0o600` on POSIX.
   - Linux is not the target platform, but "honest Linux BLOCKED" currently presents as 2 errors rather than clean results.
6. **Ledger-pruning attribution relies on Antigravity's private agent transcript.**
   - The `transcript.jsonl` it cites is not in the workspace.
   - Circumstantial evidence (label `Test`, `%TEMP%` paths, timing) strongly supports the classification, and the backup preserves the originals.
7. **Historical deliverables were edited in place.**
   - The 2.13 reports were changed after audit, which was disclosed. Prefer addenda so audited documents keep their hashes.
8. **Guard file changed after the Windows runs (comment-only).**
   - Record harness hashes inside each transcript so equivalence is provable without a diff.
9. **Leaked test subprocesses on Windows.**
   - ResourceWarnings appear in V11 and V20.
10. **Vector 27 is a no-op on Windows.**
    - Its `ok` there demonstrates nothing; it is meaningful only on Linux.
11. **Engineering tolerances carried forward.**
    - C01 0.8 % band and embedded Z<sub>b</sub>; A02 1 % component tolerance; EQ/A02 barrier width from a constant.
12. **Linux has no usable containment capability**, so FS is BLOCKED on Linux. This is a platform limitation.
