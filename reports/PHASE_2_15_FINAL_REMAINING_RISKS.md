# Phase 2.15 — Final Remaining Risks

## Gating (block Phase 2 closure)

| ID | Risk | Severity | Closure action |
|---|---|---|---|
| R-G1 | No independent Windows execution exists. Windows containment and governance rest solely on Antigravity's self-run transcripts. | **Gate** | A separately initiated run of the fixed package by the user or another operator, in a fresh session. Preserve its full output directory, then have it independently checked. |
| R-G2 | The independent package may abort on Windows PowerShell 5.1 (`Stop` + `2>&1` on native stderr). It may also silently use the wrong Python, does not enforce preflight, has no postflight git/DB check, overwrites prior runs, and has an incomplete manifest. Its README overclaims preflight validation. | **High (Gate)** | Fix F-5.1 through F-5.7 **before** R-G1 is executed. |
| R-G3 | `PHASE_2_15_SECURITY_WORDING_CORRECTIONS.md:50` falsely states that any Tier 3 tampering breaks verification. A same-user re-seal with the local key verifies cleanly. | **Medium (Gate)** | Reword it to state that Tier 3 tampering is not reliably detectable without an external authority (Tier 4). |

## Non-gating (carry forward / accept)

| ID | Risk | Severity | Note |
|---|---|---|---|
| R-1 | Check 5B start marker is not bound to `cont_pid`; a pre-existing marker is accepted (reproduced). | Low | Assert that the marker PID equals `cont_pid` and that the marker did not exist before spawn. |
| R-2 | Check 5A control asserts existence only, with no creation-time ordering. | Low | Record mtimes and assert ordering. |
| R-3 | No final recheck of all four 5B paths after observation padding. | Low | Add a final sweep. |
| R-4 | "guarantee … unmediated writes" wording; "immutable" in `evidence_guard.py` runtime messages. | Low | Wording cleanup. |
| R-5 | Tier 3 (same-user adversary) is fundamentally undefended: the HMAC key sits beside the ledger under the same user. | Accepted design limit | Documented. Tier 4 external authority is not implemented. |
| R-6 | Linux Vector 16 is always skipped, including under root+cgroup2. | Low | An honest skip; coverage gap remains. |
| R-7 | Linux cgroup containment is only exercised when a writable cgroup2 is available (root or delegated). Ordinary non-root CI skips V9/V17. | Low | Documented skip; verified here under a private namespace. |
| R-8 | The 2.12 sealed directories use `run_seal.json`, with no `.sealed` marker. Their protection relies on ledger lookup alone. | Low | Seals verified valid; consistent with the scheme at the time. |

## Status

- **Phase 2:** not closed.
- **Phase 3:** not authorized.
- **Path to closure:** R-G2 → R-G3 → R-G1. When all three are passed, Phase 2 may close.
