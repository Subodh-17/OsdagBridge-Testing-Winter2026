# Phase 2.17 — Final Remaining Risks

## Conditions (priority order)

| # | Item | Severity | Closure |
|---|---|---|---|
| 1 | **No independent operator run.** The only complete Windows package run is agent-executed (`fe82935a`). | Gate (Phase 2 closure) | A separate operator runs the unchanged package (ps1 `31f0ea49…`) from a fresh, non-agent `cmd.exe` with `-OperatorName <name> -ExecutionMode operator_execution`. Preserve the full `runs/run_*` directory and submit it for review. |
| 2 | **Phase 2.17 report inaccuracies:** (a) the 27-vector list does not match the executed tests; (b) the "without mocking" claim; (c) the manifest size; (d) "eliminate any possibility" / "filesystem-level isolation" overclaims; (e) copies not labelled as copies. | Medium (documentation; required for closure, not for the run) | Correct these in a Phase 2.17 addendum. Do not edit the earlier reports in place. |

## Non-gating

| ID | Risk | Severity | Recommendation |
|---|---|---|---|
| R-1 | Interpreter identity is self-reported. A spoof that prints the expected JSON passes (reproduced). Architecture is recorded but not enforced. | Medium | Assert `samefile(probe.executable, PythonExe)`. Pin the SHA-256 of `python.exe` / `python312.dll`. Enforce `machine == "AMD64"`. |
| R-2 | The runner accepts `-OutputDir` inside historical phases (reproduced: a full run written into `phase_2_15/…/new_run`). The Python guard does not cover PowerShell or shell writes. | Medium | Reject any `OutputDir` that is not under `phase_2_17\windows\runs`. Never redirect shell output into `testing/evidence/phase_*`. |
| R-3 | Operator, mode and parent fields are self-declared or spoofable; the manifest is unsigned. | Inherent | Independence must rest on out-of-band attestation plus the auditor's review, not on manifest strings. |
| R-4 | An interrupted run leaves a partial directory with no interruption record. | Low | A `trap` / `finally` writing `INTERRUPTED.json`. |
| R-5 | The failure record lists both version and platform messages even when only one fails. | Low | Emit only the failing checks. |
| R-6 | SC-01–SC-05 outputs were deleted from `%TEMP%`; only report excerpts remain. | Low | Retain scenario outputs under `phase_2_17/scratch_results/`. |
| R-7 | The 2.16 reports still contain uncorrected claims, with no pointer to the 2.17 corrections. | Low | A one-line erratum file alongside them, rather than an in-place edit. |
| R-8 | Tier 3 same-user adversary (local key beside ledger). | Accepted design limit | Correctly documented. |
| R-9 | Windows PowerShell 5.1 and Win32 Job Object behaviour are verified only via Antigravity's run and code review. | Environmental | Covered by condition 1. |
| R-10 | `PHASE_2_13_SECURITY_ARCHITECTURE.md` L119 "sealed and immutable". | Low | Qualify as Tier 2. |

## Status

- **Verdict:** CONDITIONALLY ACCEPTED.
- **Package:** ready for separate operator execution now.
- **Phase 2:** not closed.
- **Phase 3:** not authorized.
