# Phase 2.16 — Final Remaining Risks

## Gating: must be closed before the final independent Windows run (priority order)

| ID | Risk | Severity | Closure action |
|---|---|---|---|
| C1 | The Phase 2.15 Windows containment evidence (`cb5c77b9…`) was overwritten in place by the 2.16 run. It cannot be recovered, and prior-phase evidence directories are being reused. | High | Record the loss explicitly in the 2.16 reports. Move 2.16 transcripts to `testing/evidence/phase_2_16/` (copy, do not rewrite again). Default package output must go to a directory dedicated to the final run, never to an existing phase's transcript files. |
| C2 | The 2.16 reports misstate execution facts: a Python 3.11 run presented as pinned 3.12; a Phase 2.15 governance transcript presented as a 2.16 run; scratch evidence cited but absent. | High | Correct `PHASE_2_16_VALIDATION_RESULTS.md` and `PHASE_2_16_PACKAGE_REMEDIATION.md`. Either supply the scratch scripts and outputs, or withdraw those claims. |
| C3 | The runner does not enforce interpreter version or platform. A "3.9.0 (linux)" interpreter yields PASS. The manifest hard-codes `win32` and records the configured, not the actual, executable. | Medium–High | Fail unless `(3,12)`, `win32`, and `samefile(sys.executable, PythonExe)` all hold. Record the real `sys.executable`, `sys.version` and `platform.platform()`. |
| C4 | Manifest and run honesty: (a) a `null` manifest is possible alongside a console PASS and exit 0; (b) `session_type` is hard-coded "INDEPENDENT_EXTERNAL_EXECUTION" with no operator/host/user/parent-process identity; (c) clean-tree `$null.Trim()` errors, and an abort under a caller-scope `Stop` preference; (d) a pre-flight failure leaves an empty directory and no failure record. | Medium | (a) Re-read and validate the manifest after writing, and exit non-zero if invalid. (b) Record `$env:USERNAME`, `$env:COMPUTERNAME`, the parent process, and an operator-declared label rather than a self-asserted one. (c) Use `[string](git … )` or `@(git …) -join "\n"`. (d) Write a FAIL manifest on every exit path. |
| C5 | No independent operator run exists. | Gate | After C1–C4: a separate Windows operator (not Antigravity) runs the `.bat` in a fresh, non-agent console. Preserve the entire `run_*` directory, then submit it for independent review. |

## Non-gating

| ID | Risk | Severity | Note |
|---|---|---|---|
| R-1 | Runner prints no live suite output; `$res.ExitCode` relies on member enumeration. | Low | Separate the Tee output from the return value (for example `\| Tee-Object … \| Out-Host`), and return a single object. |
| R-2 | Launch failure (9009) is not distinguished from a test failure. | Low | Mitigated by the interpreter probe. |
| R-3 | `cmd.exe` would mis-parse `%`, `^` or `&` in the interpreter or script paths. | Low | The current pinned paths are safe. |
| R-4 | Wording residue: 2.13 L121 "detected after the fact" (not under re-seal); L119 "immutable"; 2.15 risks §4 "zero software bugs or test design gaps remain". | Low | Qualify or remove. |
| R-5 | Check 5 asserts mtime ordering, not spacing; the uncontained control child is not killed if its marker never appears. | Low | Cosmetic; time-gated checks cover spacing. |
| R-6 | Tier 3 same-user adversary is undefended by design (key beside ledger). | Accepted limit | Correctly documented now. |
| R-7 | PS 5.1, `cmd.exe` and Win32 semantics verified only by code review or Antigravity runs. | Environmental | Exercised by C5. |
| R-8 | 4 empty `independent_runs/run_20261117_19145x_*` directories in the evidence tree. | Low | Leave them in place, but document them as Antigravity pre-flight test debris. |

## Status

- **Verdict:** CONDITIONALLY ACCEPTED.
- **Not yet ready for the final independent Windows execution.** Close C1–C4 first; C5 is then the single remaining gate.
- **Phase 2:** not closed.
- **Phase 3:** not authorized.
