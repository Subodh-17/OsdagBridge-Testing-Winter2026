# Phase 2.7 Independent Gate Audit: OsdagBridge Regression Harness (audit only)

| | |
|---|---|
| **Date** | 2026-11-17 |
| **Auditor** | independent QA and structural-verification audit (same auditor as Phases 2.3–2.6) |
| **Repository** | `F:\FOSSEE internship\source\OsdagBridge`, branch `dev`, frozen at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` |
| **Controlling document** | `reports\PHASE_2_6_FINAL_INDEPENDENT_GATE_AUDIT.md` (SHA-256 `f260ebc0…`, unchanged since issue) |

**Material examined:**
- Runners: `run_all_baseline_tests.py` (126,276 B, `6af66095…`) and `run_sensitivity_matrix.py` (49,354 B, `dc6632bc…`). Every affected test and candidate was read in full, and each function was compared against the previous version.
- The four Phase 2.7 reports.
- All 94 files under `testing\evidence\phase_2_7\`.

**How I worked:**
- Every experiment ran in a **disposable cloud clone** of `d74f56d`.
- Nothing was executed or written on your machine apart from saving this report. That is the only file this audit creates.
- Evidence labels: **CONFIRMED** (independently reproduced) and **CONTRADICTED** (the evidence disagrees with the claim).

---

## 1. Executive verdict

**The harness is not yet trustworthy as a whole. Verdict: CONDITIONAL ACCEPTANCE, unchanged from Phase 2.6.**

| Status | Tests |
|---|---|
| ACCEPTED | A01, D01, GEO-COUNT, CAP, CAD (environment/export check only) |
| ACCEPTED WITH LIMITATIONS | A02, MAT, C01, B01, RPT |
| **REJECTED** | **EQ-LOAD-CONSERVATION (DEF-18), FS-CLEAN-WORKING-TREE (DEF-10)** |
| BLOCKED | D02 (DEC-015), C02 (DEC-018 / DEF-17), GEO-SLAB (DEC-013) |

The claim that "all six Phase 2.6 findings are remediated" and that the suite is "100% trustworthy" is **CONTRADICTED**:

1. **EQ** still accepts wrong along-span distributions, including the exact Phase 2.6 M9 mutant the report says is now rejected.
   - The wearing-course (DW) load distribution is not checked at all.
   - It **falsely fails a correct DEF-13 fix that reads the input density**.
   - It **falsely fails a correct distributor at a 12 m span**.
2. **FS** misses writes made outside `src/osdagbridge`, delayed writes, and writes to the working directory.
   - Writes it *does* detect have already polluted the repository.
   - For candidates, read-only resilience is still never exercised through production code.
3. **Phase 2.6 evidence has been overwritten without disclosure.** 8 of the 93 files listed in `phase_2_6/hashes/manifest_hashes.json` no longer match (§7.2).

Phase 3 is **not authorised**, and no application source change is recommended.

---

## 2. Reproduction results

**Environment:** a clean clone of `d74f56d` at `/tmp/ws27`. Its source aggregate is identical to your `src/` (§8). The Phase 2.7 runners were copied byte-identical. Platform: Linux 6.18, Python 3.12.16, numpy 2.5.4, openseespy 3.8.0.0, pythonocc-core 8.0.1.2, Xvfb, **running as root (euid 0)**.

| Command (cwd `/tmp/ws27`) | Exit | Duration | stdout / stderr | Result |
|---|---|---|---|---|
| `xvfb-run -a python testing/test_cases/baseline_regression/run_sensitivity_matrix.py` | 0 | 69.5 s | 44,765 B / 0 B, no tracebacks | 12 VERIFIED, 3 BLOCKED, identical to your summary |
| `xvfb-run -a python testing/test_cases/baseline_regression/run_all_baseline_tests.py --mode baseline` | 0 | 10.9 s | no tracebacks | 11 BASELINE_FAIL, 1 PASS (CAD), 3 BLOCKED; manifest 15/15 |

- Per-test diagnostic values match your Windows evidence.
  - Examples: EQ DD +39.4 kN; A02 1,736.6 vs 2,710.16 kN; B01 7.816 mm baseline and 7.239 mm for candidate (b); C01 125.458 MPa for the reversal case.
  - The one difference is CAD: std 65.0 on Windows against 66.6 here, which is environmental.
- Your Windows runs took 166.5 s and 17.45 s.
- The clean clone's file inventory before and after both runs was identical: the suite as shipped creates no artefacts.
- **Baseline reproduction: CONFIRMED.**

**Probe scripts** (`/tmp/p25/probe27a…f.py`) drive the real test functions with deliberately wrong implementations. Every mutation is an in-process monkeypatch, or a source variant of the shipped candidate (b) with the exact textual substitution recorded in each script. Mutations are listed per workstream below.

---

## 3. Findings by workstream

### 3.1 EQ / DEF-18: **REJECTED**

**What changed (runner lines 898–1283):**
- Barrier force, centroid and line shares are now derived from the load objects and mesh, instead of literals.
- The span is now `bgm.L`.
- Along-span bands were added: support-node share ≤ 12%, and share in [0.25L, 0.75L] within 45–60%. These apply to the left and right barriers and to DD only.
- `trib_lens_x` is computed but **never used** in any assertion.
- `mut_b` no longer sets 76.4 (CONFIRMED). Candidate (b) is the genuine consistent-load distributor (exact for uniform loads; Phase 2.5 §1.2).

**Probe results (`probe27a.py`):**

| # | Incorrect implementation (in the disposable clone) | Result | Detected? |
|---|---|---|---|
| E0 | Correct distributor (candidate b) | PASS | — |
| E1 | All load on support nodes (line shares kept) | FAIL (support share 100%) | ✓ |
| E2 | All load on the midspan node of each line | FAIL | ✓ |
| E3 | Equal nodal lumping, deck patch | FAIL (shares) | ✓ |
| **E4** | **Equal lumping along each line, end nodes not halved** (the Phase 2.6 M9 mutant) | **PASS** | **✗** |
| **E5** | **Three-point lumping 25/50/25 at x₁, L/2, xₙ₋₁** (correct total and centroid) | **PASS** | **✗** |
| **E6** | **DW only: equal nodal lumping** (DD correct) | **PASS** | **✗** |
| **E7** | **DW only: all load on supports** | **PASS** | **✗** |
| E8 | Barrier moved +1 node along the span (wrong centroid) | FAIL (dx +1.453 m) | ✓ |
| E9 | Barrier moved 0.30 m inboard by the distributor | FAIL | ✓ |
| E10 | Barrier forces +10% / −10% (total kept) | FAIL | ✓ |
| E11 | Barrier transverse split 70/30 | FAIL | ✓ |
| E12 | Application *defines* the barrier load object at z = 1.00 / 7.50 m | PASS | ✗ (expectation read from the same object) |
| E13 | DEF-13 fix that permanently overwrites `analyser.STEEL_UNIT_WEIGHT_kN_m3` with the input density (70) | PASS | — |
| **E14** | **DEF-13 fix that reads `material.girder.density` from input and leaves the module constant unchanged (70)** | **FAIL: "SW force diff −18.4 kN (−10.8%)"** | **✗ false failure** |
| E15 | Correct distributor, span 30 m | PASS | ✓ |
| E16 | Correct distributor, span 36 m | PASS | ✓ |
| **E17** | **Correct distributor, span 12 m** | **FAIL: support share 12.5% > 12%** | **✗ false failure** |
| E18 | Correct distributor, span 15 m | PASS | ✓ |

**Why each gap occurs:**

1. **Along-span bands are not derived from the mesh.**
   - For a consistent distribution on a uniform mesh, the support-node share is Δx/L. That is 1.5/24 = **6.25%**; the midspan region holds 9 nodes, so its share is 9 × 1.5/24 = **56.25%**.
   - Bounds of ≤ 12% and 45–60% are therefore arbitrary margins. They admit E4 (2/17 = 11.8% at the supports, 9/17 = 52.9% in midspan) and E5 (0%, 50%).
   - At L = 12 m with the same 1.5 m spacing, the *correct* values are 12.5% and 62.5%, so the bands reject a correct implementation.
   - They are not defensible in the sense the brief requires.
2. **`getattr(analyser_mod, "STEEL_UNIT_WEIGHT_kN_m3", 78.5)` is not independent.** It reads the same module constant the application uses (`analyser.py:416`):
   - The SW check is therefore a tautology for any fix that edits that constant (E13 passes).
   - It is a false failure for a fix that takes density from the user input without touching the constant (E14), which is the natural production fix for DEF-13.
   - A correct density correction passes only if it is implemented in that one specific way.
3. **DW** is checked only for total force and whole-case centroid; it has no share or along-span assertion.
4. **Barrier expectations** come from the application's own load objects. EQ can no longer detect a barrier defined at the wrong place (E12). Phase 2.6 used literals that would have detected it. This can reasonably be treated as out of scope for EQ, but it is not covered anywhere else.
5. **Transverse shares:** the expected values (6.18 / 18.73 / 25.10% and 76.19 / 23.81%) are correctly derived from tributary widths and the linear split (Phase 2.6 §1.2).
6. **Remaining fallbacks:** `78.5` (line 931); `deck_load_case` / `getattr` fallback chains.

**Mandatory corrections:**
- Compare the full nodal load vector of every case (DD, DW, each barrier line) against an independently computed consistent vector (per node, tight tolerance), or derive the band limits from `trib_lens_x`.
- Declare SW from the intensities of the applied self-weight line loads (in the load objects), not from the module constant.

---

### 3.2 FS / DEF-10: **REJECTED**

**What changed (runner lines 1928–2200):**
- A recursive snapshot of `pkg_root = src/osdagbridge` is taken before and after the whole test (Check 5).
- The full package is copied into a sandbox, and **for the baseline only**, production is re-imported from that sandbox.
- Queries are asserted.
- Read-only uses `icacls` on Windows, and recursive `chmod` on non-root POSIX.

**Probe results (`probe27c.py`):** each probe is candidate (b) plus a production call that writes a file. Each written file was removed from the clone afterwards.

| # | Behaviour | Result | Detected? |
|---|---|---|---|
| F0 | Candidate (b) as shipped | PASS | — |
| F1 | Direct write into the real package, nested directory (`…/project_location/shapefiles/_cache.tmp`) | FAIL | ✓ but **the file was left in the repository**: the test detects pollution after it happens, it does not prevent it |
| **F2** | Write to `src/weather.sqlite` (outside `pkg_root`) | **PASS** | **✗** |
| **F3** | Write to the repository root (`.osdag_cache/weather.sqlite`), an alternate path | **PASS** | **✗** |
| **F4** | **Delayed write** into the package (2 s timer) | **PASS**, file appeared afterwards | **✗** |
| **F5** | Code that raises `PermissionError` when the package directory is not writable | **PASS** | **✗** |
| **F6** | Write `weather.sqlite` into the current working directory | **PASS** | **✗** |

**Code-level findings:**

- **The snapshot scope is `src/osdagbridge` only.** The repository root, `src/` itself, the working directory and the temp directory are not monitored. There is no wait or second snapshot, so delayed or background writes are missed.
- **For candidates, production code runs against the real package, not the sandbox.** There is no `sys.path` redirect in that branch (lines 2050–2068). Any write the candidate makes goes into the frozen repository before it is detected.
- **The read-only scenario is not exercised for candidates.**
  - In the candidate branch (lines 2121–2130), production queries go to the real, writable package and user-data paths. The test then checks whether `ro_sb_weather` exists in a read-only sandbox that production code never imports.
  - That file cannot appear, so `ro_vulnerable = False` follows automatically. F5 passes.
  - For the baseline, the read-only scenario is a synthetic `Database(path).connect()` / `create_tables()` call, not a production query.
- **Windows vs POSIX:**
  - On Windows, `icacls /deny (OI)(CI)(W)` is a genuine OS denial. Your baseline log shows "OperationalError: unable to open database file".
  - On POSIX as root, the test sets `is_posix_root` and leaves `ro_vulnerable = False`. The result is **not** reported as BLOCKED, contrary to the remediation report. It counts as "not vulnerable" towards PASS. My run (root) confirms this.
  - **I did not accept `chmod` as protection anywhere**, and I could not exercise a non-root POSIX run in this environment. Not reproduced.
- **Credited:**
  - Production queries really execute, and their results are asserted.
  - Writes inside `src/osdagbridge` (including nested ones) are detected.
  - The shipped suite leaves the clone unchanged.

**Mandatory corrections:**
- Run production calls for **every** condition from an imported sandbox copy, ideally in a subprocess that runs to completion.
- Snapshot the whole repository, the working directory and the user-data directory, after the subprocess exits.
- Run the read-only scenario through that same sandbox import.
- Report POSIX-as-root as BLOCKED in the result status.

---

### 3.3 RPT / DEF-08: **ACCEPTED WITH LIMITATIONS**

**What the test covers now (lines 1425–1667):**
- **24 scenarios** (the report says 25: CONTRADICTED):
  - all pass;
  - G1–G6 × {moment, stiffener buckling, fatigue};
  - DCR-only failure (G5 shear);
  - cross-bracing P1/M2 failure;
  - end-diaphragm P1/M2 failure;
  - deck failure;
  - G3 stiffener + CB + deck together.
- **What is checked:** the narrative and the table are asserted in every scenario, so baseline (a) fails 20 of 24.

**Probe results (`probe27b.py`):** each probe is a source variant of `mut_b_rpt`.

| Incorrect candidate | Result |
|---|---|
| Ignores stiffener buckling | FAIL ✓ |
| Moment checked only on G1 | FAIL ✓ |
| Cross bracing: first member only | FAIL ✓ |
| End diaphragm: first member only | FAIL ✓ |
| **Cross bracing: last member only** | **PASS ✗** |
| **End diaphragm: last member only** | **PASS ✗** |
| **Cross bracing: first panel only** (P2 never fails) | **PASS ✗** |
| **Deck: checks `ur_moment` only** (shear never fails alone) | **PASS ✗** |
| **DCR check applied to shear only** | **PASS ✗** |
| **Table status copied from `design_results.overall_status`** | **PASS ✗** (the fixture sets this field from the injected state at line 1569, so a candidate can copy a mutable status field) |
| **Any failure marks every component FAIL** | **PASS ✗** (unaffected components are never asserted to remain PASS) |

**Verdict:** the four challenges the brief singled out are detected. The final status, however, **cannot be shown to come from actual component results**, because a candidate that copies the synchronised `overall_status` field passes.

**Required corrections:**
- Vary the failing member (first, middle, last, other panel).
- Deck shear-only failure.
- DCR-only failure for every check type.
- Assert that unaffected components remain PASS.
- Stop synchronising `overall_status` in the fixture, or set it inconsistently on purpose so that copying it is caught.

---

### 3.4 A02 / DEF-01, DEF-02: **ACCEPTED WITH LIMITATIONS**

**The 2,762.14 kN theoretical resultant, recomputed from the configured inputs** (lines 778–800):

| Component | Formula | Value |
|---|---|---|
| SW | ΣA × ρ × L = 0.0901376 × **76.4** (input) × 24 | 165.276 kN |
| DD | L × **W** × t × ρ<sub>c</sub> = 24 × **8.5** × 0.25 × **24.5** (input) | 1,249.500 kN |
| DW | 24 × 8.5 × 0.050 × 24.0 | 244.800 kN |
| CB | 2 × 24 × 6.54 (production helpers `crash_barrier_load_from_inputs` / `crash_barrier_dead_load_kN_m`) | 313.920 kN |
| Resultant | 1.35 × (165.276 + 1,249.5 + 313.92) + 1.75 × 244.8 = 2,333.74 + 428.40 | **2,762.14 kN** ✓ |

**How the value is built:**
- **W = 8.5 m is a literal fallback.** The keys `deck.width` and `carriageway_width` do not exist. The configured `geometry.carriageway_width` is 7.5 m and `typical_section.overall_bridge_width` is 8.4 m. "Without hardcoded literals" is CONTRADICTED.
- The barrier value **reproduces the production formula**, because it calls the production helpers.
- Observation, not a recommendation: the application's deck patch uses 6.25 kPa (0.25 × 25), whereas the input `material.deck.density` is 24.5.

**It is not asserted.**
- `applied_resultant_ok` is computed but `combination_ok = reactions_linearity_ok and forces_ok and barrier_present_in_b1` (line 862). The value appears only as an extra message *inside* an already-failing reason.
- Probe A1 (`probe27d.py`): candidate (b) with the application's steel density set to 120 kN/m³ gives superposition 2,831.36 kN against the "applied" 2,762.14 kN, and the test reports **PASS**.

**The 2,710.16 kN superposition:**
- Formula: 1.35 × (169.819 + 1,314.375 + 196.200) + 1.75 × 252.360 = **2,710.16 kN**.
- It uses solver component reactions *by design* (a linearity identity), with tolerance 0.5%.
- It stays correctly separated from equilibrium, and defective reactions are **not** used as an oracle for the applied resultant.
- Wrong factors, missing components and duplicated components in BASIC_1 all break the identity, together with the Vy/Mz factoring and barrier-presence checks. These were established in Phases 2.4 and 2.5; the candidate is unchanged.
- Wrong geometry or material inside the application is **not** detected (A1), because both sides of the identity move together.

---

### 3.5 C01 / DEF-07: **ACCEPTED WITH LIMITATIONS**

**What is new:**
- Sagging → hogging (+1,500 → −500 kNm), alongside hogging → sagging.
- A "cross-end shared node" check.
- Candidate (b): static 0.000; cyclic 62.729; hogging → sagging 125.458; sagging → hogging 125.458 MPa.
- The report's "Δσ = 83.639 MPa" is **CONTRADICTED** (the logs show 125.458).

**Probe results (`probe27e.py`):**

| Incorrect implementation | Result |
|---|---|
| One element end with reversed sign (Mzᵢ not negated) | **PASS ✗** |
| Both ends with reversed signs | **PASS ✗** |
| Reversed element ordering | PASS (harmless) |
| Order-dependent signed range (last − first) | FAIL ✓ (sagging → hogging gives 0) |
| Order-dependent \|last − first\| | **PASS ✗** (indistinguishable from max − min with only two load cases) |
| Range of absolute moments | FAIL ✓ (reversal gives 62.729) |
| Shared-node envelope combining both ends with raw signs | FAIL ✓ (static 125.458) |

**Findings:**
- **The shared-node check is a tautology.** Lines 664–673 apply the test's *own* sign rule to the test's *own* fixture data. They never call the application or the candidate, so the check always passes.
- **Where sign handling matters, it is detected:** a node envelope that mixes element ends with raw signs (the real DEF-07 mechanism) fails the static case.
- **Where it does not matter, it is not:** per-end sign errors are harmless for a range taken across load cases, so they go undetected.
- With only two load cases per history, the test cannot separate a true range from |last − first|.
- The stress histories are still **synthetic xarray** data passed through the real `_extract_demands_from_analysis_results`, not solver output.

**Capacity, recomputed:**
- N<sub>sc</sub> = **2,000,000** is genuinely used (`FatigueConfig`).
- f<sub>f</sub> = 92 × (5×10⁶ / 2×10⁶)^(1/3) = 92 × 1.35721 = **124.863 MPa**.
- f<sub>fd</sub> = 124.863 / 1.35 = **92.491 MPa** (matches the log).
- DCR: 62.729 / 92.491 = **0.6782**; 125.458 / 92.491 = **1.3564**.
- The DCR is still divided out in the test, not read from the application's designer.

---

### 3.6 B01 / DEF-03: **ACCEPTED WITH LIMITATIONS**

**Verdict logic (lines 412–432):**
- `mandatory_section_sync_ok = geom_consistent and snapped_sync_ok` is the only gate. Deflection is labelled `[INFORMATIONAL]`.

**Probe results (`probe27f.py`):**

| Condition | Result | Correct? |
|---|---|---|
| Candidate (b) | PASS (7.239 mm, info PASS) | ✓ |
| Section property fails (I<sub>z</sub> = 0.00779 < 0.0078) while deflection passes (7.367 mm, within 3%) | **FAIL** | ✓ (cannot be hidden by deflection) |
| Sections correct, deflection out of band (transformed slab, 6.501 mm) | PASS, info "VARIATION" | ✓ (informational) |
| Sections correct, D inconsistent by 2 mm | **FAIL** | ✓ |
| **Oversized sections: I<sub>z</sub> × 2, A × 2** | **PASS** (3.626 mm, info VARIATION) | ✗ |

**Findings:**
- **Property sync is only a lower bound** (I<sub>z</sub> ≥ 0.0078, A ≥ 0.024). The report's "match snapped properties within 0.5%" is CONTRADICTED.
- The report says the maximum deflection is at z = 3.183 m. The logs show **Node 49 at (x = 12.00, z = 0.00)**: CONTRADICTED.
- The deflection target is a model-consistency value, not an independent oracle. That limitation stands.

---

### 3.7 Previously accepted tests

- **Unchanged:** the A01, D01, GEO-COUNT, CAP and CAD test functions and all their candidates are identical to Phase 2.5. Phase 2.6 found them identical too.
- **Baselines reproduce:**
  - A01: ratio 1.00000.
  - D01: P<sub>z</sub> 463.7 vs 1,039.6 N/m².
  - GEO-COUNT: 6 vs 4.
  - CAP: 214,533 kN vs a 63.4 kN oracle.
  - CAD: PASS.
- **Verdicts stand.**
  - CAD remains an environment/export check only.
  - MAT is unchanged in substance: span and density both propagate (Phase 2.6 §5). It is ACCEPTED WITH LIMITATIONS: one test density, and the naive candidate equals the baseline.
- **Blocked tests:** D02, C02 and GEO-SLAB are unconditionally BLOCKED and not counted.

---

## 4. Mutation sensitivity matrix (independent)

| Test | Shipped (a) / (b) / (c) | Independent mutants detected | Mutants missed or false failures | Verdict |
|---|---|---|---|---|
| EQ | FAIL / PASS / FAIL | E1, E2, E3, E8–E11 | **E4, E5, E6, E7, E12 missed; E14, E17 false failures** | REJECTED |
| FS | FAIL / PASS / FAIL | F1 (after polluting the repository) | **F2–F6 missed**; read-only not exercised for candidates | REJECTED |
| RPT | FAIL / PASS / FAIL | stiffener ignored, moment-on-G1-only, first-member CB / ED | last member, first panel, deck moment only, shear-only DCR, copied status, fail-all | ACCEPTED WITH LIMITATIONS |
| A02 | FAIL / PASS / FAIL | factor, missing and duplicate components (identity) | wrong application geometry or material (A1); the applied resultant is not gated | ACCEPTED WITH LIMITATIONS |
| C01 | FAIL / PASS / FAIL | signed last − first, abs-moment range, raw-sign node envelope | per-end sign flips; \|last − first\|; tautological shared-node check | ACCEPTED WITH LIMITATIONS |
| B01 | FAIL / PASS / FAIL | section fail hidden behind a passing deflection; D inconsistency | oversized sections | ACCEPTED WITH LIMITATIONS |
| A01, D01, GEO-COUNT, CAP, MAT | FAIL / PASS / FAIL | as in Phases 2.4–2.6 | as previously recorded | as in §1 |
| CAD | PASS / PASS / FAIL | blank image | not the application export path | ACCEPTED (environment) |
| D02, C02, GEO-SLAB | BLOCKED | — | — | BLOCKED |

The shipped "12/12 VERIFIED" reproduces exactly, but it shows only that each shipped candidate (b) passes and each candidate (c) fails. It is **not** evidence that the tests reject the incorrect implementations listed above.

---

## 5. Evidence integrity

### 5.1 Phase 2.7 evidence

| Item | Finding | Status |
|---|---|---|
| Files | 94 on disk = 93 inventoried + `hashes/manifest_hashes.json` | CONFIRMED |
| JSON manifest | 93 of 93 SHA-256 values and sizes match (recomputed on your machine) | CONFIRMED |
| Markdown manifest | 101 of 101 hash rows exact (runners, fixtures, databases, `manifest_hashes.json` `d95036fb…`) | CONFIRMED |
| Report hashes | baseline summary `27379466…` (13,091 B), sensitivity summary `b293ddd4…` (26,532 B), runners, manifest: all correct. `runner_self_hash` = `6af66095…`. | CONFIRMED |
| Exit codes | `baseline_exit_code.txt` "0"; `sensitivity_exit_code.txt` "0\r\n"; both `shell_exit_code.txt` "0\r\n" | CONFIRMED |
| Console logs | UTF-8, 21,930 B and 46,690 B, no tracebacks. They contain the 15 MATCH and 12 VERIFIED lines and the interpreter path (`…osdagbridge-py312\python.exe`). **Both console files and both shell exit-code files carry the same mtime, 18:44:52 UTC.** That is 94 s after the sensitivity run ended (18:43:18) and 53 s after the baseline ended (18:43:59). Phase 2.6's UTF-16 PowerShell transcripts were twice the size. | **Provenance weakened**: written or converted after both runs, not captured live. Content is consistent. |
| Timeline (UTC) | Runner edits 18:39:21 / 18:40:06. Candidates and sensitivity JSONs 18:40:33–18:43:18. Baseline logs 18:43:41–18:43:59. Manifest 18:46:55. Environment fingerprint 18:46:50 (after the runs). Reports 18:48–18:49; CHANGELOG, DECISIONS and PROGRESS 18:50–18:51. Baseline runs after sensitivity. | CONFIRMED |
| Baseline / candidate separation | Sensitivity condition (a) writes to `candidates/`; the baseline runs later into `baseline/` | CONFIRMED |

### 5.2 Earlier evidence: **Phase 2.6 overwritten (undisclosed)**

Rehashing against `phase_2_6/hashes/manifest_hashes.json`, **8 of 93 files no longer match**. All were rewritten between 18:32:39 and 18:38:43 UTC by Phase 2.7 development runs; their internal timestamps confirm this.

| Phase 2.6 file | Manifest size → now |
|---|---|
| `baseline/tc_reg_eq_load_conservation.log` | 4,247 → 4,359 B |
| `baseline/tc_reg_fs_clean_working_tree.log` | 2,028 → 1,987 B |
| `candidates/tc_reg_a02_uls_combination_sum.log` | 2,003 → 2,486 B |
| `candidates/tc_reg_b01_section_property_sync.log` | 2,027 → 2,140 B |
| `candidates/tc_reg_c01_sectional_stress_range.log` | 2,046 → 2,363 B |
| `candidates/tc_reg_eq_load_conservation.log` | 4,073 → 3,917 B |
| `candidates/tc_reg_fs_clean_working_tree.log` | 1,651 → 1,685 B |
| `candidates/tc_reg_rpt_exec_summary_status.log` | 2,415 → 2,114 B |

- **Two Phase 2.6 baseline logs (EQ and FS) are lost.** The suffixed `_a/_b/_c` candidate logs are intact.
- No Phase 2.7 report mentions this.
- Phases 2.3, 2.4 and 2.5 are unchanged since my previous audits.

---

## 6. Repository and database integrity

| Check | Result |
|---|---|
| `.git/HEAD` | `ref: refs/heads/dev` → `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` |
| Branches | only `dev`; no Phase 3 branch |
| Locks and index | No `*.lock` files. `.git/index` mtime 2026-11-15 12:26:18 UTC, unchanged. The `.git` directory mtime is 18:51:26: a Git command was run after the reports, with no lasting effect. |
| Tracked source | 282 files under `src/` (CR-normalised; excluding caches, `*.sqlite`, `egg-info`). Aggregate SHA-256 `7c9294813b58fb84ecd965643daec240276747d1788b13187c0e0f46c52b024c` on your machine and in a clean checkout: **identical**. |
| Untracked or changed since 2026-11-15 14:30 | Only `src/…/project_location/weather.sqlite` (pre-existing, mtime 2026-11-16 05:48:51). No `*.tmp`, cache or sandbox files in the repository. |
| Databases | `Intg_osdag.sqlite` `25f978575be64a11…` (270,336 B) and `weather.sqlite` `1d767658099bef9d…` (180,224 B): both unchanged |
| My audit clone after all probes | Source inventory and aggregate identical to the pristine checkout. Every probe-created file was removed. |

**`source\OsdagBridge` is unchanged on `dev` at the frozen commit.**

---

## 7. Remaining limitations

1. **EQ:**
   - Along-span distribution is only band-checked, with limits not derived from the mesh (E4, E5 pass; E17 fails falsely).
   - DW is not checked for distribution (E6, E7).
   - SW is derived from the production module constant (E14 fails falsely; E13 is a tautology).
   - Barrier placement depends on the application's own load objects (E12).
2. **FS:**
   - The snapshot covers `src/osdagbridge` only, with no delayed check (F2–F4, F6).
   - Candidate production calls run against the real repository (F1 pollutes it).
   - Read-only behaviour is not exercised for candidates (F5).
   - POSIX-as-root is counted as "not vulnerable" rather than BLOCKED.
3. **RPT:**
   - Member and panel coverage is incomplete; deck shear-only and per-check DCR-only cases are absent.
   - Unaffected components are never asserted to remain PASS.
   - The fixture `overall_status` field can be copied.
4. **A02:**
   - The applied resultant is not gated.
   - It uses a literal 8.5 m width fallback and production helpers.
   - The combination identity cannot detect geometry or material errors inside the application.
5. **C01:**
   - The shared-node check is a tautology.
   - Two-load-case histories cannot separate a true range from |last − first|.
   - Stress histories are synthetic, and the DCR is computed in the test.
6. **B01:**
   - Section synchronisation is a one-sided lower bound.
   - The deflection target is not independent.
7. **Evidence:**
   - Phase 2.6 is partly overwritten.
   - Console transcripts were written after the runs.
8. **Report accuracy (CONTRADICTED claims):**
   - EQ "rejects uniform distributions without end-node halving";
   - C01 "83.639 MPa";
   - RPT "25 scenarios";
   - FS "explicitly reported as BLOCKED" on POSIX root;
   - B01 "within 0.5%" and "max deflection at z = 3.183 m";
   - A02 "without hardcoded literals";
   - "100% trustworthy".

---

## 8. Prioritised remediation plan (test harness only; no application changes)

1. **Evidence immutability (first).**
   - Disclose the 8 overwritten Phase 2.6 files and restore them from any backup, or mark the Phase 2.6 EQ/FS baseline logs as lost.
   - Make each phase's evidence directory write-once: development runs go to a scratch directory.
   - Capture console output live with redirection and record the command line.
2. **EQ.**
   - Assert the per-node nodal force vector for DD, DW and each barrier line against an independently computed consistent vector, or derive the support and midspan limits from `trib_lens_x` with a tight tolerance.
   - Derive declared SW from the applied self-weight line-load intensities.
   - Add a span-sensitivity case (e.g. 12 m) to the matrix.
3. **FS.**
   - Execute production calls for all conditions in a subprocess whose `sys.path` points at a sandbox package copy.
   - Snapshot the repository root, the working directory and the user-data directory after the subprocess exits.
   - Run the read-only case through the same import.
   - Report POSIX-as-root as BLOCKED.
4. **RPT.**
   - Parametrise the failing member index and panel.
   - Add deck shear-only and DCR-only cases for every check type.
   - Assert unaffected components remain PASS.
   - Stop synchronising `overall_status`.
5. **C01.**
   - Use histories with three or more load cases, where max − min differs from |last − first|.
   - Make the shared-node check go through the application or candidate extraction path.
6. **A02.** Gate the applied resultant from correctly keyed inputs, or remove it and its claims.
7. **B01.** Make section synchronisation two-sided against the snapped properties.

---

**Final gate:** Phase 3 is **not authorised**. This audit makes no recommendation to change application source.

The harness cannot be called trustworthy while EQ and FS remain REJECTED and the Phase 2.6 evidence overwrite is unresolved.
