# Phase 2.13 — Remaining Risks (prioritised)

Harness-side only. No application source change is implied. Risks are framed against the harness's own declared four-tier threat model.

## High — blocks a clean ACCEPTED

1. **Windows containment and the 27/27 governance pass are unreproduced (BLOCKED).**
   - These are the core enforcement evidence for Tiers 2–3 on the real target platform.
   - They exist only in Antigravity's own `windows_containment_validation.txt` and `governance_test_output.txt`.
   - The test *designs* are now adequate (Check 5 spans the full 32 s; Check 1 proves no pre-resume execution), but an independent Windows run is required before accepting them.
   - On Linux the governance suite is **not** 27/27: 3 vectors skip (9, 16, 17) and, as root, `test_10` fails.

2. **The OS read-only control is described more strongly than it behaves.**
   - The remediation report calls the `S_IREAD` block on `open("a")` "kernel-level" protection, and the architecture lists `stat.S_IREAD` as a Tier-2 enforcement mechanism.
   - As root on POSIX it is ignored entirely (reproduced: `test_10` fails). As the same non-root user or on Windows it is cleared with a single `chmod`/attribute change — the harness's own `test_10` does exactly that in step 2.
   - It is an accidental-overwrite deterrent (Tier 1–2), not an enforcement boundary. The wording should match the honest Tier-3 statement already present elsewhere in the same document.

## Medium

3. **Same-user resealing remains possible (F-07, acknowledged).**
   - A fresh process that deletes the ledger entry + `.sealed` can overwrite (D5) or re-seal tampered evidence so the verifier passes (D7).
   - This is correctly declared out of scope (Tier 3), but it means the seal provides **tamper-evidence against accidental drift and uncoordinated edits only** — not non-repudiation.
   - Do not let any report (e.g. the Tier-4 "complete cryptographic non-repudiation" language) read as an implemented property. Real independence needs a key the evidence-producing user cannot read (separate principal / HSM / OS key store) or an append-only external/transparency log.

4. **Governance tests write to the production trust ledger.**
   - The authoritative `trusted_run_seals.json` carries 2 test seals (tmp-dir `evidence_dir`, 17:27).
   - Point every test's `generate_and_seal_manifest` at a temporary `OSDAGBRIDGE_TRUST_DIR` (setUp already allocates one) so the pinned ledger is never appended to by test execution, and purge the 2 stray entries.

5. **Raw filesystem writes bypass the gateway (F-06, Tier 3).**
   - `open()` / `shutil.copy` outside `safe_open_evidence` are unmediated (D6); detection is after-the-fact via hash.
   - Acceptable under the declared model, but any code path that must be trusted should be routed through the gateway, and a post-run full-tree re-hash should gate the final summary.

## Low

6. **Linux has no usable containment capability.**
   - Detection is now correct and honest (non-root → BLOCKED), but FS cannot be positively verified on Linux at all. This is a platform limitation, not a defect; keep it stated.

7. **Windows junction TOCTOU not reproduced.**
   - `is_symlink_or_junction` + realpath handle it in code; Vectors 5/13/15 run on Windows but were not reproduced here.

8. **Engineering tolerances carried over from 2.12.**
   - C01 0.8 % band and embedded composite Z<sub>b</sub>; A02 1 % component tolerance; EQ/A02 barrier width from a constant. Unchanged and still acceptable-with-limitations.

## Conditions for upgrading to ACCEPTED

- Independent Windows reproduction of the 6 containment checks and all 27 governance vectors, with preserved output.
- Correct the "kernel-level" / Tier-2 `S_IREAD` wording to match the honest Tier-3 statement.
- Isolate governance test sealing from the pinned trust store and remove the 2 stray ledger entries.
