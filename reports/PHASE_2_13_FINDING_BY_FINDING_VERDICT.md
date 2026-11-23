# Phase 2.13 — Finding-by-Finding Verdict

**Controlling prior audit:** `PHASE_2_12_FINAL_INDEPENDENT_GATE_AUDIT.md`
**Auditor:** Claude (independent) · **Date:** 2026-11-17 · **Baseline:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`

Verification labels: **REPRODUCED** (I executed it in a disposable copy and checked disk state), **CODE REVIEW** (inspection only), **BLOCKED** (could not execute — Windows unavailable to me).

| Phase 2.12 finding | Phase 2.13 remediation | Independent test | Actual evidence | Verdict |
|---|---|---|---|---|
| **F-07** Trust anchor is same-user writable; tampered evidence re-verifiable (K10/K11/K13) | Keeps HMAC; adds a four-tier threat model that **explicitly** declares HMAC as tamper-detection only and same-user attack out of scope (Tier 3); trust-dir pinning added | REPRODUCED D2, D5, D7 as non-root `auditor` | Same user still: clears read-only + writes → detected only by hash (D2); a fresh process that removes the ledger entry + `.sealed` commits attacker content (D5, `3e2773`→`9e4eb7`); delete-entry-then-re-seal (K13) makes `verify_manifest_integrity` **PASS on attacker content** (D7). No asymmetric key, HSM or external log exists. | **ACCEPTED WITH LIMITATIONS** — honest within the declared model; **non-repudiation is NOT achieved** and must not be claimed as implemented |
| **F-06** Gateway didn't stop fresh-process overwrite of sealed/active evidence | `.sealed` on-disk marker + persistent ledger consulted by `is_sealed_directory`; workspace-root and `reports/` refusal | REPRODUCED D4 (fresh process, gateway) and D6 (raw bypass) | Through the **supported gateway**, a fresh process is now **refused** even after deleting `.sealed`, because the ledger still lists the dir (D4; file intact). A **raw `open()`** outside the gateway still overwrites (D6) — Tier 3, disclosed. Workspace-root / `reports/` writes refused (Vector 25 reproduced). | **ACCEPTED WITH LIMITATIONS** |
| **F-05** TOCTOU truncation | `O_EXCL` staging + `os.replace` + pre/post realpath re-validation; never truncates destination | REPRODUCED: swap after init, after open, before replace | Protected file **never truncated** in all three; operation raises and the staging temp is unlinked. Vector 15 passes. Windows junction path is CODE REVIEW only. | **ACCEPTED** (Linux) / **NOT VERIFIED** (Windows junctions) |
| **F-08** Linux falsely reported cgroup v2 on tmpfs (root) | `/proc/mounts` must show `cgroup2` at `/sys/fs/cgroup`, `cgroup.controllers` must exist, and the child cgroup must auto-expose `cgroup.procs`; child joined via `preexec_fn` before exec | REPRODUCED L1–L5 in private mount namespaces | Genuine cgroup2 → contained, and child's `/proc/self/cgroup` shows `0::/osdagbridge_cg_…` **before exec** (L1). tmpfs + fake `cgroup.controllers` → **rejected** (L2). cgroup2 overmounted by tmpfs → rejected (L3). Host hybrid default → rejected, no leaked dirs (L4). Non-root genuine cgroup2 without delegation → BLOCKED (L5). | **ACCEPTED** (detection fixed). Linux still has no usable containment in practice → FS **BLOCKED**, honestly reported |
| **F-09** Windows containment unproven; Check 5 waited only 4 s | Check 1 now proves no marker before resume; Check 5 now waits past 3/8/15/30 s (full 32 s horizon) | CODE REVIEW; BLOCKED empirically (no Windows host) | Test **design is now adequate** (unlike 2.12): Check 5 observes each milestone at t=4.5/9.5/16.5/31.5 s; Check 1 checks the marker is absent before/after assign and present after resume. The 6/6 PASS exists only in Antigravity's `windows_containment_validation.txt`; I could not run it. | **BLOCKED** |
| **F-12** Evidence reuse/deletion; missing transcripts; misreported times | `transcripts/` with live stdout+stderr; `EXECUTION_HISTORY.md` | REPRODUCED seal/manifest reconciliation (device) | Three official seals (`fb966e81`, `9aac2738`, `867d222a`) have valid HMACs and match the disk manifests and `reports/PHASE_2_13_RUN_SEALS.json`. Live transcripts exist. Engineering test functions byte-identical to 2.12. **But** the pinned ledger carries **2 governance test seals** (tmp-dir `evidence_dir`, 17:27) → test runs still touch the production ledger. Governance "27/27, 0 skips" is **Windows-only**; on Linux 3 skip and (as root) test_10 fails. | **ACCEPTED WITH LIMITATIONS** |
| **F-11b** C01 tolerance / girder coverage | Unchanged from 2.12 (3,200 kNm G2, 0.8 %) | Byte-identical function hash to 2.12 | Carried forward: catches girder/end/−1.0 %/−1.5 % shortcuts; −0.7 % passes; Z<sub>b</sub> embedded | **ACCEPTED WITH LIMITATIONS** |
| **F-10** EQ/A02 barrier input | Unchanged from 2.12 | Byte-identical function hashes | Real `crash_barrier_load` key used; production ignoring it fails both; width still a constant; A02 1 % component tolerance | **ACCEPTED WITH LIMITATIONS** |
| EQ/A02/C01/B01/RPT, crash-barrier propagation | Preserved, not rewritten | All 5 baseline + 5 sensitivity functions byte-identical to 2.12 | B01 and RPT **ACCEPTED**; EQ/A02/C01 as above | **ACCEPTED** / **ACCEPTED WITH LIMITATIONS** |
| Repository & databases | Frozen | REPRODUCED (device) | HEAD `d74f56dd`, branch `dev`, no `.git` locks, source aggregate `7c929481…`, `weather.sqlite`/`Intg_osdag.sqlite` match required hashes, 0 source files changed | **ACCEPTED** |

## New Phase 2.13 governance vectors (24–27)

| Vector | Intent | Verdict |
|---|---|---|
| 24 cross-process sealed overwrite | Tests the real attack (spawns a fresh `python -c`, asserts gateway refusal). Genuine, not a helper-return assertion. | ACCEPTED (code-confirmed; reproduced equivalently as D4) |
| 25 workspace-root / reports refusal | Real `check_write_permission` calls | ACCEPTED (reproduced) |
| 26 trust-dir pinning (K14) | Real `get_trust_dir` + CLI gate | ACCEPTED (reproduced: fail-closed without flag) |
| 27 cgroup tmpfs rejection | Asserts `is_contained`/`containment_type` | ACCEPTED (reproduced via L2–L4) |

## Overall

**CONDITIONALLY ACCEPTED.** The declared four-tier model is honest and holds for Tiers 1–2 where I could reproduce it; the same-user limitation (Tier 3) is openly disclaimed; Tier 4 (independent authority) is **not implemented**. Blocking gaps: Windows containment and the 27/27 governance pass are **BLOCKED** (unreproduced by me), and two report statements overstate the OS read-only control. Phase 3 is **not** authorized.
