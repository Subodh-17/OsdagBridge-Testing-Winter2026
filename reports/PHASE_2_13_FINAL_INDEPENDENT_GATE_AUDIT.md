# Phase 2.13 — Final Independent Security Gate Audit

**Project:** FOSSEE OsdagBridge — baseline regression & sensitivity harness
**Workspace:** `F:\FOSSEE internship` · **App repo:** `source\OsdagBridge`, `dev` @ `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`
**Trust store:** `C:\Users\Subodh\.osdagbridge_trust` (read-only access granted for this audit)
**Controlling prior audit:** `PHASE_2_12_FINAL_INDEPENDENT_GATE_AUDIT.md`
**Auditor:** Claude (independent) · **Date:** 2026-11-17

**Companion deliverables:** `PHASE_2_13_FINDING_BY_FINDING_VERDICT.md`, `PHASE_2_13_REPRODUCTION_RESULTS.md`, `PHASE_2_13_REMAINING_RISKS.md`.

**Mode:** audit only. No source, database, evidence, manifest, ledger or report modified; no commit, push or branch change; Phase 3 not started. All adversarial probes ran in disposable `/tmp/ws213*` clones, each with a disposable trust directory. The device signing key was read in place only and never copied off the device.

Labels: **REPRODUCED** (executed + disk/hash checked), **CODE REVIEW** (inspection only), **BLOCKED** (Windows not executable by me).

---

## 1. Overall verdict

# **CONDITIONALLY ACCEPTED**

Phase 2.13 is the first phase whose security story is **honestly scoped**. Its four-tier threat model states plainly that the same-user HMAC is *tamper-detection against accidental drift and uncoordinated edits, not a security boundary against the user* (Tier 3), and it reserves non-repudiation for an external authority (Tier 4) that it does **not** claim to have built. Measured against that declared model, the Tier 1–2 controls I could reach hold up under reproduction, and the Phase 2.12 defects I could test on Linux are genuinely fixed.

It is **not** a clean ACCEPTED, for three reasons:
1. **The platform-critical evidence is BLOCKED.** Windows Job Object containment (6 checks) and the 27/27 governance pass exist only in Antigravity's own logs. I cannot run Windows. On Linux the governance suite is not 27/27 (3 skip; as root `test_10` fails), and the filesystem containment test is BLOCKED.
2. **Two report statements overstate the OS read-only control**, calling `stat.S_IREAD` "kernel-level" protection and listing it as a Tier-2 enforcement mechanism. I broke it as root, and the harness's own `test_10` clears it with one `chmod`.
3. **Same-user resealing still works** (reproduced): deleting the two bookkeeping files (ledger entry + `.sealed`, both user-writable) lets a fresh process overwrite or re-seal tampered evidence so the verifier passes. This is disclosed as out of scope, but it caps what "sealed/immutable" can mean.

Phase 3 is **not** authorized by this audit.

---

## 2. Threat model (objective 1)

The four tiers are technically accurate and the boundaries are drawn honestly:
- **Tier 1** (accidental corruption, TOCTOU races): `O_EXCL` staging + atomic `os.replace` + realpath re-validation. **Reproduced** — never truncates (F-05).
- **Tier 2** (supported harness interfaces): centralized gateway, protected-phase and sealed-dir refusal, workspace-root and `reports/` refusal. **Reproduced** — fresh-process writes through the gateway are now refused (F-06 / Vector 24).
- **Tier 3** (same Windows user running arbitrary code): the document states HMAC is **not** a boundary here. **Confirmed accurate** — my D2/D5/D6/D7 all live in this tier.
- **Tier 4** (independent authority: asymmetric keys / HSM / append-only log): described as where non-repudiation would come from. **Not implemented.**

The one wording problem: the Tier-4 box says "Complete cryptographic non-repudiation against local user tampering," and the remediation report calls the read-only block "kernel-level." Non-repudiation is not achieved by anything implemented, and the read-only attribute is not kernel-enforced against the owner or root. These should be reworded to match the otherwise-honest Tier-3 statement. **`--allow-unpinned-trust-dir`** is a genuine explicit opt-in: verification fails closed on an unpinned trust dir without it (reproduced D8), and ordinary runs use the pinned store, so it cannot be enabled accidentally by normal execution.

---

## 3. Cross-process sealed evidence protection (objective 2)

REPRODUCED as non-root `auditor` (see `REPRODUCTION_RESULTS.md` §2):

| Attack | Outcome |
|---|---|
| Same-user append to a sealed file | Refused (read-only honored for non-root owner) — **D1** |
| Same-user `chmod` + write | Succeeds, but `verify` REJECTs (HASH_MISMATCH) — **D2** |
| Fresh process: remove `.sealed`, write via gateway | **Refused** (ledger still lists dir) — **D4** |
| Fresh process: remove ledger entry + `.sealed`, write via gateway | **Overwrites** (attacker content committed) — **D5** |
| Fresh process: raw `open()` (no gateway) | **Overwrites**; detected only by later hash — **D6** |
| Fresh process: tamper + delete entry + re-seal | **verify PASSES on attacker content** — **D7** |

So the Phase 2.12 F-06 gap is **closed for the supported interface** (D4): a fresh process can no longer overwrite sealed evidence through the gateway while the ledger entry stands. What remains (D5/D6/D7) is pure Tier 3 and is disclosed.

**On the specific claim that `os.chmod(S_IREAD)` / `FILE_ATTRIBUTE_READONLY` give kernel-level protection:** it does not. Reproduced — POSIX root ignores it (Linux `test_10` fails), and the same user clears it with one call (the test's own step 2). It deters accidental and supported-harness overwrites; it is not an enforcement boundary.

---

## 4. Linux cgroup v2 detection (objective 3)

REPRODUCED in private mount namespaces (§3 of results). The Phase 2.12 tmpfs false-positive is fixed:
- genuine `cgroup2` → contained, **and the child is placed in the child cgroup before it executes** (`0::/osdagbridge_cg_…` in `/proc/self/cgroup`) — L1;
- `tmpfs` + fabricated `cgroup.controllers` → **rejected** — L2;
- `cgroup2` overmounted by tmpfs → rejected — L3;
- host hybrid default → rejected, no leaked directories — L4;
- genuine `cgroup2`, non-root, no delegation → BLOCKED — L5.

A fake writable directory never produces PASS. **ACCEPTED.** In practice this host (and the non-root target) has no delegated cgroup2, so the Linux FS test correctly returns **BLOCKED**, not PASS.

---

## 5. Windows containment (objective 4) — BLOCKED

CODE REVIEW: the design is now correct *and* its validation is no longer self-defeating — Check 1 proves the marker is absent before/after Job assignment and present only after resume; Check 5 observes the 3/8/15/30 s writes across a true 32 s horizon (t = 4.5/9.5/16.5/31.5 s), so it cannot pass merely because the writer had not yet scheduled. `CREATE_SUSPENDED` → assign → resume ordering, `KILL_ON_JOB_CLOSE`, no breakaway flags, and the lock-protected `_winapi` hook are all present.

EMPIRICAL: **BLOCKED.** My environment is Linux-only; I could not execute `validate_windows_containment.py`. The 6/6 PASS is Antigravity's own preserved log, not independent reproduction.

---

## 6. Windows governance suite (objective 5)

27 vectors. Vectors 24–27 (cross-process overwrite, root/reports refusal, trust pinning, cgroup-tmpfs rejection) exercise the real attack rather than asserting a helper's return value — I confirmed this by code review and reproduced the Linux-reachable equivalents (D4, Vector 25, D8, L2–L4). Junction creation uses `_winapi.CreateJunction`.

Reproduction: on Linux I ran all 27 — **3 skip** (9, 16, 17; containment/Windows-only) and, as root, **test_10 fails** (read-only ignored by root). The claimed Windows "27/27, 0 skips" is plausible (Windows runs the containment and junction vectors and honors read-only for a non-admin user) but is **BLOCKED** for independent confirmation.

---

## 7. Execution provenance (objective 6)

REPRODUCED (device): the three official seals have valid HMAC signatures and match both the on-disk manifests and `reports/PHASE_2_13_RUN_SEALS.json`. Live `console_output`/`console_error` and `transcripts/` exist. Manifests match disk exactly (19/19/54, no unlisted files), each with a `.sealed` marker.

Two caveats:
- The pinned ledger carries **2 governance test seals** (tmp-dir `evidence_dir`, 17:27), so test execution still appends to the production trust store.
- The "governance launched and awaited" vs "27/27 completed" sequencing is consistent in the preserved output (`Ran 27 tests … OK`), but that output is Windows-only and unreproduced here. The baseline/sensitivity `console_output` headers still read "PHASE 2.12 REGRESSION TEST SUITE" — cosmetic, but worth correcting.

No completion summary was accepted as proof; every accepted item above was checked against disk, hashes, or reproduction.

---

## 8. Engineering regression (objective 7)

All five baseline `test_tc_reg_*` functions and all five sensitivity `mut_b_*` functions are **byte-identical** to Phase 2.12. The accepted improvements are therefore preserved and were not rewritten:
- `crash_barrier_load` input propagation and the EQ/A02 component-level assertions (EQ/A02 **ACCEPTED WITH LIMITATIONS**: width from a constant; A02 1 % component tolerance);
- C01 multi-girder / end coverage (**ACCEPTED WITH LIMITATIONS**: 0.8 % band, embedded Z<sub>b</sub>);
- B01 (**ACCEPTED**), RPT (**ACCEPTED**);
- Linux non-root BLOCKED behaviour preserved.

---

## 9. Repository & database integrity (objective 8)

| Item | Value | |
|---|---|---|
| Branch / HEAD | `dev` / `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` | ✓ |
| `.git` locks | none | ✓ |
| Source aggregate (282 files) | `7c9294813b58fb84ecd965643daec240276747d1788b13187c0e0f46c52b024c` | ✓ baseline |
| `weather.sqlite` | `1d767658099bef9da035cd8e4c4fdfa5f8e83794a6756a7832bc824b67cd7e98` | ✓ |
| `Intg_osdag.sqlite` | `25f978575be64a11ce2e00562c7513c215a33ba26ea9da795171343c74d9ea91` | ✓ |
| `src/` files changed since 15:30 UTC | 0 | ✓ |
| Historical evidence (2.9–2.11) during 2.13 window | unchanged | ✓ |

**ACCEPTED.** The application is untouched.

---

## 10. Conditions to reach ACCEPTED

1. Independently reproduce, on a real Windows host, the 6 containment checks and all 27 governance vectors, and preserve the output.
2. Reword the "kernel-level protection" (remediation) and Tier-2 `S_IREAD` enforcement language, and the Tier-4 "complete non-repudiation" line, to match the honest Tier-3 statement. Do not describe non-repudiation as implemented.
3. Point governance-test sealing at a temporary trust directory and remove the 2 stray entries from the pinned ledger.

These are harness-only. **Phase 3 is not authorized by this audit;** that decision rests with the project owner.
