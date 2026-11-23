# Phase 2.6 Final Independent Gate Audit: OsdagBridge Regression Suite

- **Auditor:** independent QA and structural-verification audit (same auditor as Phases 2.3–2.5)
- **Date:** 2026-11-16
- **Repository:** `F:\FOSSEE internship\source\OsdagBridge`, branch `dev`, frozen at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`
- **Controlling document:** `reports\PHASE_2_5_FINAL_INDEPENDENT_GATE_AUDIT.md` (SHA-256 `04fbde1a…`, byte-identical to what I issued)

**Material examined**

- `run_all_baseline_tests.py`: 109,078 B, SHA-256 `ef5a8151…`.
- `run_sensitivity_matrix.py`: 48,054 → 48,898 B, SHA-256 `d24db269…`.
- Both scripts were read in full for the affected tests and candidates, and diffed function by function against Phase 2.5.
- All four Phase 2.6 reports.
- All 94 files under `testing\evidence\phase_2_6\`.

**Labels used in this report**

- **CONFIRMED:** independently reproduced.
- **CONTRADICTED:** independent evidence disagrees with the claim.
- **MISSING:** evidence absent.

---

## 0. Reproduction

**Setup**

- A clean checkout of `d74f56d` into an isolated cloud workspace, `/tmp/ws26`.
- The aggregate of its source tree is identical to your `src/` (§10).
- The Phase 2.6 scripts were copied in byte-for-byte.
- Phase 1D fixtures: `31ae62dc…` / `429a3198…`.
- Platform: Linux, Python 3.12, pythonocc-core 8.0.1.2, openseespy 3.8.0.0, Xvfb.

**Commands**

```
cd /tmp/ws26
xvfb-run -a python testing/test_cases/baseline_regression/run_sensitivity_matrix.py              # exit 0, 12/12 "VERIFIED"
xvfb-run -a python testing/test_cases/baseline_regression/run_all_baseline_tests.py --mode baseline   # exit 0, 15/15 manifest match
```

**Results**

- All per-test statuses and diagnostic values match your Windows evidence. Baseline reproduction: **CONFIRMED**.
- The clean clone's source-file inventory was taken before and after both runs and was identical. **No artefact was created in the source tree.** In Phase 2.5 the suite created `weather.sqlite`; that is now fixed. CONFIRMED.

**Adversarial probes**

- Scripts `/tmp/p25/probe26a…f.py` monkeypatch in-process only, in the cloud copy.
- They drive the real test functions with deliberately incorrect implementations.
- **Exit code 0 is not treated as evidence of correctness anywhere.**

---

## 1. Priority 1: EQ-LOAD-CONSERVATION (DEF-18)

### 1.1 Claims verified in the code (runner lines 806–1123)

| Claim | Finding |
|---|---|
| Independent left and right barrier centroids | **CONFIRMED.** Each barrier load group is re-distributed through `_distribute_load_types_to_model`. Its nodal-force total, x̄ and z̄ are each asserted (lines 1000–1060). |
| Individual barrier force assertion | CONFIRMED, but the expected **156.960 kN is a literal**, as are x̄ = 12.000, z̄ = 0.250 / 8.250, and the shares 76.19 / 23.81 (lines 1015–1050). |
| Transverse tributary shares | CONFIRMED for DD: the six line shares are asserted with ±0.5 percentage points. The report says ±1.5%, which is wrong. The expected list is a literal (line 1073). **DW shares are not checked.** |
| Density-derived self-weight | Uses `input_dict["material.girder.density"]` (76.4 in the fixture). There is still a fallback chain to `material_props…rho` and then `78.5` (lines 837–843). |
| Algebraic reaction summation | **CONFIRMED.** `ry = -nodeReaction(node, 2)`, with no `abs()` (line 934). |
| Fallbacks eliminated | **CONTRADICTED.** The density fallback chain, `12.0` / `4.25` (lines 909–910) and `4.25` (line 847) remain. Missing DD, DW or barrier cases now raise. |

### 1.2 Independent check of the expected shares

**Mesh**

- Transverse line positions: z = [0, 1.05, 3.183, 5.317, 7.45, 8.5] m.
- The deck patch covers 0–8.5 m.

**Deck tributary widths**

Each line receives half of each adjacent cell width, so the widths are [0.525, 1.5917, 2.1333, 2.1333, 1.5917, 0.525] m. Dividing by 8.5 m gives:

| Line | z (m) | Width (m) | Share |
|---|---|---|---|
| 0 | 0 | 0.525 | **6.176%** |
| 1 | 1.05 | 1.5917 | **18.725%** |
| 2 | 3.183 | 2.1333 | **25.098%** |
| 3 | 5.317 | 2.1333 | 25.098% |
| 4 | 7.45 | 1.5917 | 18.725% |
| 5 | 8.5 | 0.525 | 6.176% |

The shares sum to 100%. These are exactly the consistent bilinear nodal shares for a uniform pressure. **Justified.**

**Barrier at z = 0.25 m (between lines 0 and 1)**

The linear shape-function split gives:
- line 0: (1.05 − 0.25)/1.05 = **76.19%**
- line 1: 0.25/1.05 = **23.81%**

The barrier at z = 8.25 m mirrors this. Barrier force: 24 × 6.54 = **156.96 kN**. **Justified** for this geometry only.

**Observed results**

- **Baseline:** the barrier shares are already correct, so the defect is purely longitudinal (98.10 kN per barrier, x̄ = 12.750 m). The deck shares are 6.74 / 18.91 / 24.35%.
- **Candidate (b):** reproduces all the expected shares exactly. CONFIRMED.

### 1.3 Adversarial probes

`/tmp/p25/probe26a.py` and `probe26a2.py`. Except where stated, every mutant runs together with a genuine DEF-13 fix that reads the input density, so that only the load distribution is being tested.

| Probe | Result | Verdict |
|---|---|---|
| M0: correct distributor + genuine DEF-13 fix | PASS | ✓ |
| Drop first node column (boundary cells) | FAIL (DD −3.1%, x̄ +0.387 m) | ✓ |
| Equal-share nodal lumping | FAIL (DD shares) | ✓ |
| Uniform transverse spacing assumed | FAIL (DD shares) | ✓ |
| Left barrier 0.30 m inboard only | FAIL (line 0 share 47.6%, case z̄ +0.150) | ✓ |
| Right barrier 0.30 m inboard only | FAIL (line 5 share 47.6%) | ✓ |
| Left barrier 0.04 m inboard only | FAIL (line 0 share 72.4%) | ✓ |
| Both barriers 0.80 m inboard | FAIL (outer-line share 0%) | ✓ |
| Both barriers on the centreline | FAIL | ✓ |
| Barrier magnitudes +10% / −10% (total kept) | FAIL (172.7 / 141.3 kN) | ✓ |
| Barrier split 70/30 instead of 76.19/23.81 | FAIL | ✓ |
| Density changed to 70.0 (genuine fix) | PASS | ✓ |
| **All deck, DW and barrier load placed on the two support nodes of each line**, keeping line shares and x̄ | **PASS** | **✗ not detected** |
| **Equal lumping along each line** (end nodes not halved) | **PASS** | **✗ not detected** |
| **Correct distributor only, with no DEF-13 fix** | **FAIL**: "SW force diff +4.5 kN (+2.7%)" | **✗ false failure** |
| Correct distributor + genuine fix, **span 30 m** | **FAIL**: "Left barrier force = 196.2 kN (exp 156.96), x̄ = 15.00 (exp 12.00)" | **✗ false failure** |

**Findings**

1. **The longitudinal nodal distribution is unchecked.**
   - Placing the whole deck and barrier load on the support nodes produces zero midspan bending, yet passes every assertion.
   - The brief's requirement — reject incorrect spatial distributions whose total and centroid look correct — is still not met in the longitudinal direction.
2. **EQ is now coupled to DEF-13 in the opposite direction.**
   - The baseline declares SW = 0.0225344 × 4 × 76.4 × 24 = 165.276 kN, while the application applies 169.819 kN (78.5).
   - So **a correct DEF-18 fix on its own fails EQ**. The test now reports DEF-13 as a "DEF-18" SW failure.
3. **Candidate (b) hides finding 2.**
   - `mut_b_eq_load_conservation` sets `analyser.STEEL_UNIT_WEIGHT_kN_m3 = 76.4` (sensitivity script lines 627–629).
   - That hard-codes the fixture density, which is a DEF-13 fix keyed to this fixture, not a DEF-18 fix.
   - **Otherwise candidate (b)'s distributor is genuine**: it computes the exact consistent nodal load vector (Phase 2.5 §1.2).
4. **The expectations are fixture-bound.** The barrier force, position and share literals mean that any change in span or deck geometry fails a correct implementation (span 30 m probe).
5. **Report inaccuracies.**
   - Candidate (c) is described as "lumps barrier loads uniformly across all 6 lines". The code (lines 637–665) actually leaves the baseline barrier bug in place.
   - "±1.5%" should be ±0.5 percentage points.

### 1.4 Tolerances

- **Force:** 0.05%, well within what an exact consistent distribution achieves (about 0).
- **Centroid:** 0.05 m, appropriate.
- **Share:** ±0.5 percentage points. The 0.04 m barrier shift was detected.

**EQ verdict: REJECTED.** The defect is CONFIRMED and candidate (b)'s distributor is genuine.

---

## 2. Priority 2: RPT executive-summary status (DEF-08)

**What the test does now (runner lines 1265–1464)**

- **Scenario loop:** fails each of G1–G6 alone in turn (lines 1395–1402), plus:
  - a DCR-only failure (G5 shear, DCR 1.30, labelled `PASS`);
  - cross bracing, end diaphragm and deck failing individually;
  - G3 + deck failing together;
  - an all-pass scenario.
- **Assertions:** both the narrative **and** the table's "Overall Design Status" are checked in **all 12 scenarios**.
- **Fixture:** `design_results.overall_status` is set to match the injected state (line 1346). The expected outcomes are written into each scenario's assertion, not derived from the fixture. CONFIRMED.

**Probes (`/tmp/p25/probe26b.py`, `probe26b_2.py`)**

| Probe | Result | Verdict |
|---|---|---|
| Candidate (b) | PASS | ✓ |
| Inspects only G1 and G3 | FAIL in 5 of 12 scenarios | ✓ |
| Skips G2 / G4 / G5 / G6 (each tried separately) | FAIL (1–2 of 12 scenarios) | ✓ |
| Uses the status string only (ignores DCR) | FAIL (DCR-only scenario) | ✓ |
| Ignores fatigue checks | FAIL (6 of 12) | ✓ |
| Narrative fixed but table untouched | FAIL (CB, ED and deck scenarios) | ✓ |
| **Ignores "Stiffener Buckling" checks** | **PASS** | **✗** |
| **Checks moment capacity only on G1** | **PASS** | **✗** |
| **Table copied from the fixture's `overall_status`** | **PASS** | limitation |
| **Cross bracing: inspects the first member only** | **PASS** | **✗** |

**Findings**

- **Each girder fails with one fixed check type.** G1 always fails on moment; G2–G6 always fail on fatigue. No stiffener failure is ever injected. An implementation that skips a whole check category therefore passes.
- **The cross-bracing and end-diaphragm fixtures have a single member** (`P1/M1`).
- **The table now must include non-girder components.** This differs from the application's documented girder-only behaviour (`executive_summary.py:77`). DEC-021 records the scenarios but does not ratify that change in meaning.
- **"Unaffected girders correctly represented":** not applicable. The summary reports only an aggregate status, never a per-girder one.

**RPT verdict: ACCEPTED WITH LIMITATIONS.**
- The Phase 2.5 rejection reason (selected-girder candidates passing) is resolved.
- The remaining gaps are check-type and member coverage.

---

## 3. Priority 3: FS filesystem behaviour (DEF-10)

**What the test does now (runner lines 1728–1920)**

| Claimed | Finding |
|---|---|
| Package tree copied to an isolated temp directory | Only `core/data/project_location/` is copied, not the whole package. The report says "entire package tree": CONTRADICTED. |
| Recursive snapshots | CONFIRMED on the **sandbox copy**. A detector self-test plants a file in `shapefiles/` (lines 1768–1779). |
| Production DB calls executed | CONFIRMED: `get_state_list` and `get_weather`. Results are asserted (≥ 30 states; weather fields) (lines 1812–1820). |
| Package files unchanged | **Only meaningful on the baseline.** `DB_PATH` is redirected into the sandbox only when `prod_db_in_package` is true (lines 1806–1807). For any candidate, the production code never touches the sandbox, so the snapshot cannot change regardless of what the candidate writes into the **real** package. |
| Real OS read-only permission | **Windows:** `icacls /deny <user>:(OI)(CI)(W)`. Your baseline log shows "OperationalError: unable to open database file", so the permission is genuine there. **POSIX:** `chmod` on the directory only, not recursive (the report says `chmod -R`). As root it has no effect: my reproduction shows "Vulnerable: False". |
| Read-only operation exercised | **Baseline only, and with a synthetic call**: `Database(path).connect()` plus `CREATE TABLE`, not production code. For candidates, `ro_vulnerable = False` is **assigned without running anything** (lines 1867–1869). |
| Missing-database behaviour | CONFIRMED. The sandbox deletes `weather.sqlite`, and at baseline the redirected query creates it there, which is detected ("New files: ['weather.sqlite']"). |
| Intentionally incorrect write detected | Only the test's own self-test probe in the sandbox. A candidate's incorrect write to the real package is not detected (see probe below). |
| No artefacts in `source\OsdagBridge` | **CONFIRMED.** Nothing was created during either run in the clean clone. |

**Probe F1 (`/tmp/p25/probe26c.py`)**

- Setup: candidate (b), plus a production call that writes `project_location/weather_cache.sqlite` and `project_location/shapefiles/_index_cache.tmp` into the **real** package.
- Result: the test reports **PASS**, with "Package tree mutated: False".
- Both files were left in the real source tree; I deleted them afterwards from the cloud copy only.

**FS verdict: REJECTED.**
- The immutability and read-only checks do not observe the code path a candidate actually uses.
- Read-only resilience is never exercised for a candidate.

**Credited improvements:**
- The test no longer pollutes the real source tree.
- Queries are asserted.
- Read-only uses a genuine OS permission on Windows.

---

## 4. Priority 4: A02 combination correctness

- **The 2,802.70 kN resultant (runner lines 726–733).**
  - Formula: `sw = ΣA × 78.5 × L`, `dd = L × 8.5 × 0.25 × 25.0`, `dw = L × 8.5 × 0.050 × 24.0`, `cb = 2 × L × 6.54`.
  - Only L and ΣA come from the model. **Density, width, thicknesses, unit weights and barrier load are literals**, so the report's "derived dynamically from component models" is CONTRADICTED.
  - Value: 1.35 × (169.819 + 1,275.000 + 313.920) + 1.75 × 244.800 = **2,802.70 kN**. It does not depend on reactions, the load factors are correct, and the barrier SIDL is included.
  - It uses 78.5 kN/m³, while EQ declares 76.4: **an internal inconsistency** between the two tests.
- **It is not asserted.**
  - The pass condition is `reactions_ok and forces_ok and barrier_present_in_b1`.
  - The log line "Derived Applied ULS Resultant: 2802.70 kN (Physical target: 2802.70 kN)" compares the value with itself.
  - The report's "2802.70 kN ± 0.05% … asserted" is **CONTRADICTED**.
- **The 2,710.16 kN superposition.**
  - Target: 1.35 × (169.819 + 1,314.375 + 196.200) + 1.75 × 252.360 = **2,710.16 kN**, with tolerance tightened to 0.5%.
  - It does depend on the (defective) component reactions, **by design**. It is a linearity identity, BASIC_1 = Σγᵢ·Rᵢ, so it stays valid whatever the distribution error. That is exactly what keeps combination correctness separate from equilibrium.
  - It is necessary, together with the Vy/Mz element check and the barrier-contribution check, for detecting DEF-01 and DEF-02 at reaction level.
- **BASIC_1** is isolated with `analyze(load_case=b1_name)`.
- **Baseline:** 1,736.6 kN; shear error 72,392.5 N against factored, 1.6×10⁻⁷ N against unfactored; barrier contribution −708.7 kN. Reproduced.

**A02 verdict: ACCEPTED WITH LIMITATIONS.**
- Combination correctness is properly tested.
- The "physical resultant" is decorative and fixture-literal.

---

## 5. Priority 5: MAT self-weight

- **`geometry.span` is a genuine production key.** It is present in the fixture and in `input_dict`, and drives the model (`grillage_model.L` = 24.0 → 30.0 when the key changes). CONFIRMED.
- **The fallback.**
  - `L_span = input_dict.get("geometry.span", input_dict.get("span", 24.0))` (line 1691) still contains a silent fallback.
  - It is **unreachable in practice**: with the key removed, production setup raises `KeyError: 'geometry.span'` and the test reports ERROR, not a silent pass (probe).
- **Span propagation, under candidate (b):**
  - span 24: observed **151.43**, expected 151.43, PASS;
  - span 30: observed **189.29**, expected 189.29 (= 4 × 0.0225344 × 70 × 30), PASS.
  - **Geometry and density both reach the calculation.**
- **Baseline:** 169.82 against 151.43 kN. Detected.
- **Limitations:**
  - Only one test density (70) is used.
  - Candidate (c) is identical to the baseline.

**MAT verdict: ACCEPTED WITH LIMITATIONS.**

---

## 6. Priority 6: C01 fatigue stress range

**What is now tested**

| Case | Expected | Baseline | Candidate (b) |
|---|---|---|---|
| Static | 0 | — | 0.000 |
| Positive cyclic (500 → 1,500 kNm) | 62.729 MPa | 188.19 MPa (envelope), 0.000 (per load case) | 62.729 |
| **Sign reversal, hogging −500 → sagging +1,500 kNm** | 125.450 MPa | 188.19 MPa | 125.458 |

The reversal expectation is ΔM = 2,000 kNm / 15.94×10⁶ mm³.

**Probes (`/tmp/p25/probe26e.py`)**

| Probe | Result |
|---|---|
| Candidate (b) | PASS |
| **No sign flip** (+Mzᵢ, +Mzⱼ) | **PASS** |
| **Both element ends flipped** | **PASS** |
| **Order-dependent signed range** (last − first) | **PASS** |
| Range of absolute moments | FAIL (reversal gives 62.729) ✓ |

**Findings**

- **Only one transition direction is tested** (hogging → sagging). Sagging → hogging is absent. A signed last-minus-first implementation passes, although it would give −125 MPa in the other direction.
- **The sign convention is still not exercised.**
  - Each element end's range across load cases is invariant to sign, and both ends are evaluated separately.
  - The "element-end envelope" the Phase 2.5 audit asked for, combining ends at a shared node, is not tested.
  - "Verified element-end sign consistency" is CONTRADICTED.
- **The stress histories are synthetic xarray data**, not solver output.

**Capacity, unchanged and re-verified**

- N<sub>sc</sub> = 2,000,000 (from the application's `FatigueConfig`).
- f<sub>f</sub> = 92 × (5×10⁶ / 2×10⁶)^(1/3) = 124.863 MPa.
- f<sub>fd</sub> = 124.863 / 1.35 = **92.491 MPa**.
- DCR = 62.729 / 92.491 = **0.6782**.
- The application's own designer DCR is still not read; the test computes the DCR itself.

**C01 verdict: ACCEPTED WITH LIMITATIONS.**

---

## 7. Priority 7: B01 section synchronisation

- **The documentation is now honest.** The test and the limitations report describe the 7.218 mm target as "an internal grillage model consistency target … NOT a closed-form hand oracle". They give:
  - the correct six-line Courbon factors: 0.3977 → 7.22 mm, 0.3406 → 6.19 mm;
  - the eccentric four-girder value of 12.71 mm;
  - the transformed-slab value of 6.501 mm.
- **Remaining inaccuracies:**
  - **The code still gates on the deflection** (`geom_consistent and snapped_sync_ok and deflection_ok`), although the comment says "the gate verdict is carried by D-consistency and … girder_sections".
  - The log label "(at overhang edge line z=0.0m)" is a fixed string, not computed.
  - The limitations report still calls 4.541 mm a "lower bound". It is only the central-load share and does not bound this eccentric load case.
- **Behaviour is unchanged:** 7.816 mm at baseline, 7.239 mm for candidate (b). Reproduced.
- **No independent oracle exists.**

**B01 verdict: ACCEPTED WITH LIMITATIONS**, as an internal consistency check only.

---

## 8. Priority 8: previously accepted tests

The A01, D01, GEO-COUNT, CAP and CAD test functions and all their candidates are **byte-identical to Phase 2.5** (function-level diff). Their baseline results reproduce:

| Test | Baseline result |
|---|---|
| A01 | ratio 1.00000 |
| D01 | P<sub>z</sub> 463.7 vs 1,039.6 N/m² |
| GEO-COUNT | 6 vs 4 |
| CAP | 214,533 kN vs 63.4 kN oracle |
| CAD | std 66.6 |

**Verdicts stand.** CAD remains an **environment and export check only**: it does not exercise the application's export path and proves nothing about structural correctness.

D02 (DEC-015), C02 (DEC-018, DEF-17) and GEO-SLAB (DEC-013) are unconditionally BLOCKED, with no candidates and nothing counted as verified.

---

## 9. Priority 9: evidence integrity

| Item | Finding | Status |
|---|---|---|
| Files | 94 on disk = 93 inventoried + `hashes/manifest_hashes.json` (19 baseline, 19 sensitivity, 54 candidates, 1 environment) | CONFIRMED |
| `manifest_hashes.json` | **93 of 93** SHA-256 values and sizes match, recomputed on your machine | CONFIRMED |
| `PHASE_2_6_EVIDENCE_MANIFEST.md` | **100 of 100** printed hash and size rows are exact. This includes both scripts, the fixtures, both databases and `manifest_hashes.json` itself. The Phase 2.5 transcription defect is fixed. | CONFIRMED |
| Report hashes | Runner `ef5a8151…`, sensitivity script `d24db269…`, manifest `ae7b6d90…`, summaries `e2bd0406…` / `fbaf7f11…`, databases `25f97857 5be64a11…` / `1d767658 099bef9d…`: all correct. The baseline summary's `runner_self_hash` equals the current runner. | CONFIRMED |
| stdout/stderr | `baseline/console_output.txt` (43,824 B) and `sensitivity/console_output.txt` (94,032 B) are UTF-16 PowerShell transcripts with no tracebacks. The command line is truncated by PowerShell's error-record wrapping. | CONFIRMED; provenance partial |
| Exit codes | `shell_exit_code.txt` = "0" for both runs, now ASCII. The script-written exit codes are 0. | CONFIRMED |
| Timeline (UTC) | Script edits 17:39:51 / 17:40:32. Sensitivity run 17:41:30–17:43:40 (130 s). **Baseline run 17:43:50–17:44:40 (later).** Manifest 17:46:46; reports 17:46–17:50; CHANGELOG, DECISIONS and PROGRESS 17:50–17:51. Every candidate log is timestamped 17:41:30–17:43:40, so there are no stale logs. | CONFIRMED |
| Baseline and candidate separation | Condition (a) of the sensitivity run is written to `candidates/`, and the baseline run came afterwards. | CONFIRMED |
| Earlier evidence | No file under `phase_2_3/`, `phase_2_4/` or `phase_2_5/` changed after my Phase 2.5 audit. | CONFIRMED |
| Report wording | The limitations report §4 attributes the overwrite to "Phase 2.3" runs. It was Phase 2.4 work overwriting `phase_2_3/` files. | minor inaccuracy |

---

## 10. Repository status verification

| Check | Result |
|---|---|
| `.git/HEAD` | `ref: refs/heads/dev` → `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` |
| Branches | only `dev`; no Phase 3 branch |
| Locks and index | No `*.lock` files. `.git/index` mtime 2026-11-15 12:26:18 UTC, unchanged. The `.git` directory mtime is 17:52:04 UTC: a Git command was run after the reports, with no lasting effect. |
| Source content | 282 files under `src/` (CR-normalised; excluding caches, `*.sqlite`, `egg-info`). Aggregate SHA-256 `7c9294813b58fb84ecd965643daec240276747d1788b13187c0e0f46c52b024c` on your machine **and** in a clean checkout of `d74f56d`: identical. |
| Files changed after 2026-11-15 14:30 UTC | Only the untracked `weather.sqlite` (mtime 2026-11-16 05:48:51, unchanged since before Phase 2.4). No `*.tmp` or cache files are present. |
| Databases | `Intg_osdag.sqlite` `25f978575be64a11…`, `weather.sqlite` `1d767658099bef9d…`: unchanged |

**`source\OsdagBridge` remains unmodified on `dev` at the frozen commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`.** The only file outside the repository touched in your workspace is the new `reports\PHASE_2_6_FINAL_INDEPENDENT_GATE_AUDIT.md`.

---

## 11. Final classification

| Test | Classification | Reason / evidence |
|---|---|---|
| A01 | **ACCEPTED** | unchanged; genuine candidate; reproduced |
| D01 | **ACCEPTED** | unchanged; reproduced |
| GEO-COUNT | **ACCEPTED** | unchanged; reproduced (the naive candidate is trivial) |
| CAP | **ACCEPTED** | unchanged; IS 800 oracle; reproduced |
| CAD | **ACCEPTED** (environment/export check only) | not structural evidence |
| A02 | **ACCEPTED WITH LIMITATIONS** | combination identity valid; 2,802.70 kN not asserted and built from literals (§4) |
| MAT | **ACCEPTED WITH LIMITATIONS** | span and density both propagate; single density; naive candidate = baseline (§5) |
| C01 | **ACCEPTED WITH LIMITATIONS** | reversal case added in one direction only; sign convention still unexercised (§6) |
| B01 | **ACCEPTED WITH LIMITATIONS** | honest internal-consistency label; no independent oracle; the code still gates on the deflection (§7) |
| RPT | **ACCEPTED WITH LIMITATIONS** | G1–G6, DCR-only and table now covered; check-type and member coverage gaps (§2) |
| EQ (DEF-18) | **REJECTED** | longitudinal misdistribution passes; a DEF-18-only fix fails falsely; candidate hard-codes 76.4; expectations are fixture literals (§1) |
| FS | **REJECTED** | candidate writes to the real package go undetected; read-only path not exercised for candidates; POSIX root ineffective (§3) |
| D02 | **BLOCKED** | DEC-015 |
| C02 | **BLOCKED** | DEC-018 / DEF-17 |
| GEO-SLAB | **BLOCKED** | DEC-013 |

## 12. Mandatory corrections

1. **EQ**
   - Assert the longitudinal distribution, for example per-node comparison against the consistent nodal vector, or the first moment about each support per line.
   - Declare SW from the application's applied intensity, or leave density to MAT, so that a DEF-18-only fix passes.
   - Derive the barrier, position and share expectations from the load objects and mesh, not literals.
   - Remove the 76.4 assignment from candidate (b).
   - Remove the remaining fallbacks.
2. **FS**
   - Make production code operate on the sandboxed package copy for *every* condition, for example by importing the package from the copy.
   - Or snapshot the real package tree read-only, before and after.
   - Run the read-only scenario through production calls for candidates as well.
   - Use recursive `chmod` and run without root on POSIX, or skip the check with an explicit reason.
3. **RPT**
   - Inject every check type on every girder.
   - Use multi-member cross-bracing and end-diaphragm fixtures.
   - Record a decision on whether the table's overall status includes non-girder components.
4. **C01:** add the sagging → hogging direction and a cross-end envelope case at a shared node.
5. **A02:** either assert the applied resultant from input-derived values, or delete it.
6. **B01:** make the code match the stated gate (D-consistency and section synchronisation), or state explicitly that the deflection also gates.

---

## Final decision

**CONDITIONAL ACCEPTANCE**

| Status | Tests |
|---|---|
| **Accepted** | A01, D01, GEO-COUNT, CAP, CAD (environment check) |
| **Accepted with limitations** | A02, MAT, C01, B01, RPT |
| **Rejected** (§12 items 1–2 mandatory) | EQ-LOAD-CONSERVATION, FS |
| **Blocked** (not counted as verified) | D02, C02, GEO-SLAB |

Phase 2.6 is a substantial improvement:
- RPT is no longer rejected.
- The evidence manifest is now exact.
- The test suite no longer writes into the source tree.

The claim that every mandatory finding is resolved is **not justified**: EQ and FS still accept incorrect implementations or reject correct ones.

**This decision does not authorise application source-code changes, Phase 3 planning or branch creation.**
