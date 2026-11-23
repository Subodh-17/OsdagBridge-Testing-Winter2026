# Phase 2.1 Final Gate Audit: OsdagBridge Regression Suite

**Purpose:** decide whether Phase 2.1 resolves the objections in `reports/PHASE_2_FINAL_INDEPENDENT_GATE_AUDIT.md`, and whether the suite can gate Phase 3 remediation.

**Frozen baseline:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`

**Material examined:**
- `run_all_baseline_tests.py` (60,059 B, modified 10:07:04 UTC) and `run_sensitivity_matrix.py` (28,613 B, modified 10:08:12 UTC), both read in full.
- All 14 logs, `phase_2_1_summary.json`, `exit_code.txt` and `runner.log`.
- All 14 sensitivity JSONs, `sensitivity_matrix_summary.json` and `sensitivity_matrix.log`.
- The three Phase 2.1 reports and DEC-012 to DEC-014.
- Application source at the baseline.

**Independent execution.** I ran both harnesses unchanged in a separate cloud environment equivalent to `osdagbridge-py312`: Python 3.12, a clean baseline clone, the same fixtures (SHA-256 verified) and Xvfb. I also ran three probe scripts of my own. Nothing was run, edited, installed or committed on your machine or in your workspace, apart from saving this report.

**Labels:**
- Evidence: CONFIRMED / PLAUSIBLE / UNVERIFIED / CONTRADICTED.
- Tests: VALID / VALID WITH CORRECTIONS / INCOMPLETE / INVALID / BLOCKED.

---

## 1. Executive verdict

**What Phase 2.1 genuinely achieved:**
- The regression results are real and reproducible. My independent run gave the same 12 FAIL / 1 BLOCKED / 1 PASS, the same numbers in every log, and a real process exit status of 1.
- A02 now detects a solver that drops load factors: BASIC_1 shear equals the *unfactored* sum to 1.2×10⁻⁷ N.
- C01 now covers both fatigue paths.
- CAP has a reproducible IS 800-style positive oracle, 63.40 kN, which rejects the clamp.
- GEO-SLAB is correctly BLOCKED in the runner.
- The application repository is untouched.

**The sensitivity evidence does not support "14/14 verified":**
1. **Most "minimal correct" candidates are not implementations.** For 7 of the 14 tests, the PASS was produced by overwriting the value the test reads:
   - A02 spoofs `get_results`;
   - C01 zeroes every stress range;
   - CAP hard-codes 63.4 kN;
   - D02 uses a string placeholder;
   - C02 uses a mock object whose only content is its name;
   - B01 swaps a property list after the model is built;
   - GEO-SLAB uses constants plus a substitute assertion.

   Each such PASS proves that *an incorrect implementation passes the test*. That is the opposite of what the matrix was meant to show.
2. **B01 passes with the analysed stiffness unchanged (CONFIRMED by probe).** The test reads the `girder_props` record, not the OpenSees sections built from it. With the harness's "correct" candidate applied, the B01 PASS condition is satisfied, yet the probe's midspan deflection is identical to baseline: 4.72460 mm.
3. **A01 passes with a fix that leaves DEF-01 largely in place (CONFIRMED by probe).** With A01's own "correct" mechanism active, the BASIC_1 shears are still 66.3 kN away from the factored target, and only 6.06 kN from the unfactored sum.
4. **The GEO-SLAB "PASS" contradicts DEC-013.** DEC-013 is a formal BLOCKER. The sensitivity harness bypasses the real test, asserts an unratified transformed-section constant against itself, and counts the result as "VERIFIED".
5. **The only archived console record of the sensitivity run disagrees with the summary.** `sensitivity_matrix.log` (09:58:39 UTC) shows 7 UNVERIFIED tests, including CAP with the "correct" candidate FAILing and the clamp PASSing. Both scripts were then edited (10:07 and 10:08) and re-run with no console capture. The reports present the later 14/14 without disclosing this.
6. **The reports cite fixture hashes and paths that don't exist.** They cite `testing/fixtures/pinned_*.json`; that directory does not exist. Their full SHA-256 values match the real fixtures only in the first 8 hex digits.
7. **The FS test does not observe the side effect it claims.** It checks the *spelling* of the path string and the default-constructor behaviour. A correct design (ship a pre-built read-only database inside the package) would fail it.
8. **C02 (fatigue vehicle) and D02 (temperature) check existence only.** C02 checks a name; D02 accepts any non-`None` object. Neither checks participation in the analysis.

**Verdict: REJECT PHASE 2.1 REGRESSION SUITE.** §7 lists the remaining work. D01, GEO-COUNT and MAT are usable as they stand.

---

## 2. Execution and exit code

| Claim | Evidence | Status |
|---|---|---|
| 14 tests executed | 14 logs (10:09:00.68–10:09:11.03 UTC) and 14 summary entries. The summary starts at 10:09:00.30 and ends at 10:09:11.03, after the last runner edit at 10:07:04. My independent run executed all 14. | CONFIRMED |
| 12 FAIL / 1 BLOCKED / 1 PASS | Summary counts and logs agree. My reproduction gives identical statuses and identical numbers for A02, C01, CAP, MAT, RPT and D02. | CONFIRMED |
| Summary matches the logs | Status, reason and duration agree for every test. Every `matches_baseline_manifest` is true. | CONFIRMED |
| Exit code 1 | The runner writes `exit_code.txt` itself, immediately before `sys.exit(exit_code)` (lines 1259–1265). So the file holds the *intended* exit, not an observed operating-system status. There is no console capture of the 10:09 run: `runner.log` is from 09:57:04, before the final edit. **In my independent run the process exit status was 1** and the file contained `1`. | CONFIRMED by reproduction; not separately recorded on Windows |
| All tests completed before the reports were written | The reports were written at 10:10–10:11, after the summary. | CONFIRMED |
| No silent skips or substitution | The runner has no skip paths. **But** the sensitivity run calls the same test functions, and `log_test_result` writes into `phase_2_1/`. So the 10:08 sensitivity run overwrote the per-test logs with condition (c) results. The 10:09 runner run then overwrote them back. Evidence integrity depends on that run order. | Risk |
| Pinned fixtures | The runner pins the correct hashes (`31ae62dc08a0…0191`, `429a3198fc93…a5ab`), but a mismatch **only prints a warning**. The reports' `testing/fixtures/` paths and full hashes are CONTRADICTED. | Partly |
| Provenance | `OSDAGBRIDGE MODULE: None`, because `osdagbridge` is a namespace package with no `__init__.py`, so this field proves nothing. `baseline_commit` is a constant in the script, not read from the repository. The warnings in `sensitivity_matrix.log` show modules loaded from `F:\FOSSEE internship\source\OsdagBridge\src`. | Weak |
| Gate semantics | Exit is 1 whenever any test FAILs or is BLOCKED. With GEO-SLAB permanently BLOCKED, the suite can **never** exit 0. There is only a baseline manifest and no post-fix manifest, so progress and regressions during Phase 3 cannot be told apart. `run_sensitivity_matrix.py` never exits non-zero, even when UNVERIFIED. | Gap |

---

## 3. Test-by-test validity

| # | Test | Application path actually exercised | Detects the defect? | Wrong or incomplete fix can pass? | Correct fix can fail? | Classification |
|---|---|---|---|---|---|---|
| 1 | A01 | ospgrillage `add_load(load_factor)` and `analyze()` on one line load | Yes | **Yes.** Scaling only `load_point_1..4` passes A01 while BASIC_1 remains essentially unfactored (probe). | Yes, if the fix is in `_copy_loads` instead | VALID WITH CORRECTIONS |
| 2 | B01 | `_stage_grillage_setup()` → the `girder_props` record | Yes. 7.40% / 10.55% gap; D ≠ d<sub>w</sub> + 2t<sub>f</sub>. | **Yes.** Swapping the record after setup passes; analysed deflection unchanged (probe). | Only if the DEC-014 hierarchy is reversed | **INCOMPLETE** |
| 3 | C01 | real `_extract_demands_from_analysis_results`, synthetic xarray | Yes, both paths | **Yes.** "Always 0 MPa" (no fatigue at all) passes; this is the harness's own (b) candidate. | Possibly BLOCKED if the fix stops using SLS_FREQUENT | **INCOMPLETE** |
| 4 | A02 | real `add_dead_loads` → `create_uls_combinations` → `analyze()` → `get_results` | **Yes. Solver factor drop CONFIRMED.** | Yes: (i) correcting only `Vy_i` passes; (ii) SIDL, barrier and DW are checked only as attributes; barrier omission from BASIC_1 is invisible. | Yes, if SIDL is fixed without a `sidl_combination` attribute | VALID WITH CORRECTIONS |
| 5 | D01 | real `add_wind_loads` with a pass-through spy, plus Table 12 | Yes | No | No | **VALID** |
| 6 | D02 | real `add_temperature_load` with real keys | Yes | **Yes.** Any non-`None` object passes; the harness uses the string `"MockTemperatureLoadCase"`. | — | **INCOMPLETE** |
| 7 | C02 | real `add_vehicle_load_cases_from_combinations` with the real toggle | Yes. Only 2 cases. | **Yes.** Any object named "…fatigue…" passes, even if never analysed and with any axles. | Yes, if the case name lacks "fatigue" | **INCOMPLETE** |
| 8 | RPT | real `executive_summary` with the real Phase 1D dictionary plus a mirror | Yes | Partly: only the *girder* line is checked, so the hard-coded Cross bracing, End Diaphragm and Deck "pass" lines are untested. | Yes, if the wording changes | VALID WITH CORRECTIONS |
| 9 | GEO-COUNT | `BridgeConfig.from_plate_girder_bridge` | Yes | No | No | **VALID** |
| 10 | GEO-SLAB | `_transverse_section()`, unconditionally BLOCKED | — | — | — | **BLOCKED** (correct in runner; misrepresented in the matrix, §5) |
| 11 | CAP | real `compute_bearing_stiffener()` | Yes | **Yes.** A hard-coded return of 63.4 kN passes; this is the harness's own (b) candidate. Only one geometry is tested. | No | VALID WITH CORRECTIONS |
| 12 | MAT | real `add_dead_loads()`; oracle from the model's own areas and span | Yes. 169.82 kN against 151.43 kN expected. | No | No | **VALID** (minor: the naive candidate equals the baseline) |
| 13 | FS | `ui_loc.DB_PATH` *string* test plus `Database()` default in a temporary directory | Detects the path spelling, not the side effect | Yes. Any path without lowercase "osdagbridge" and "core"/"src" passes. | **Yes.** A pre-built read-only database shipped in the package fails. | **INVALID** |
| 14 | CAD | pythonocc `Viewer3d.ExportToImage` on a box | Environment check only | — | — | **VALID as environment verification** (not an application test) |

**Totals:**
- VALID: 4 (D01, GEO-COUNT, MAT, CAD as environment verification).
- VALID WITH CORRECTIONS: 4 (A01, A02, RPT, CAP).
- INCOMPLETE: 4 (B01, C01, D02, C02).
- INVALID: 1 (FS).
- BLOCKED: 1 (GEO-SLAB).

---

## 4. Specific findings

### 4.1 A02: ULS combination and factors

- **The production path is real (CONFIRMED):**
  - `add_dead_loads()` creates self-weight, deck, wearing course (`wearing_course_load`), footpath and crash barrier (`crash_barrier_load_case`).
  - It then builds the "1.0 DL" combination from `_DL_ATTRS` = self-weight, deck, footpath and `sidl_combination` (`analyser.py:1532–1537`).
  - `create_uls_combinations()` builds `"BASIC_1: 1.35DL + 1.75DW"` by `_copy_loads` → `target_lc.add_load(entry["load"], load_factor=…)` (`analyser.py:2344–2349`).
  - `analyze()` solves every load case, and `get_results(load_case="BASIC_1: …")` returns that case's solver forces.
  - The test therefore inspects the intended factored combination. In this model it contains no live-load term, because no vehicles are added.
- **Detection of factor drop: CONFIRMED.** Max |V<sub>BASIC_1</sub> − (V<sub>DL</sub> + V<sub>DW</sub>)| = 1.16×10⁻⁷ N, against 72,392 N from 1.35·DL + 1.75·DW. The oracle uses solver results for the components, so the helper-applies-factors flaw from the previous audit is gone.
- **Independent resultants**, from the load definitions; reproduced in the console output:

  | Component | Resultant |
  |---|---|
  | Self-weight | 4 × 1,768.95 N/m × 24 m = 169.8 kN |
  | Deck | 6,250 N/m² × 8.5 m × 24 m = 1,275.0 kN |
  | Wearing course | 1,200 N/m² × 8.5 m × 24 m = 244.8 kN (applied over the full 8.5 m width; intent UNVERIFIED) |
  | Crash barrier | 2 × 6,540 N/m × 24 m = 313.9 kN |

  BASIC_1 as intended by the code: 1.35 × (169.8 + 1,275.0) + 1.75 × 244.8 = **2,378.9 kN**. Actually solved: 1,689.6 kN (unfactored). With the barrier as SIDL at 1.35 (factor assumed; to be confirmed against IRC 6 Annex B): about 2,802.6 kN.
- **Remaining gaps:**
  - **Only `Vy_i` is compared.** The (b) candidate shows that correcting that one component of `get_results` passes. Compare at least Mz_i, Mz_j and support reactions.
  - **The barrier is not checked inside BASIC_1.** It is not in `_DL_ATTRS`; it belongs to the never-created SIDL combination. The oracle uses the application's own "1.0 DL" as its component, so a BASIC_1 without the barrier satisfies the identity. `crash_barrier_load_case is not None` is already true on the baseline.
  - **SIDL is still detected by attribute.** Calling `create_sidl_combination()` after the DL combination already exists sets the attribute without adding the barrier to ULS. A correct fix that folds the barrier into DL without that attribute fails.
  - **The test inspects element shears, not "reactions"** as the reports state.
- **Required:**
  - Add a total-vertical-reaction identity, Σ reactions(BASIC_1) = Σ γᵢ·Rᵢ, over independently built component cases: SW, deck, DW, barrier, and any railing or median present.
  - Assert the barrier's contribution explicitly.
  - Compare Mz as well as Vy.

### 4.2 GEO-SLAB: the undecided model

- **The runner is correct.** It returns BLOCKED unconditionally, the manifest expects BLOCKED, and DEC-013 says "FORMAL BLOCKER".
- **The candidate calculation is dimensionally consistent** as a per-metre steel-transformed gross strip:
  - I = 1.0 × 0.25³ / 12 / 6.06 = 2.148×10⁻⁴ m⁴/m;
  - A = 0.25 / 6.06 = 0.0413 m²/m;
  - m = E<sub>s</sub>/E<sub>cm</sub> = 200/33, with E<sub>cm</sub> = 33 GPa for M40 from the model's own material data.
  - This is consistent with `unit_width=True` (properties per metre, multiplied by the 1.5 m element width in `osp_grillage.py:905–915`) and with the steel material assigned to transverse members (`analyser.py:246–250`).
- **Still undecided, by DEC-013's own wording:** short- versus long-term modular ratio, cracked versus uncracked section, the torsion constant J, I<sub>y</sub>, and shear areas. The candidate's J = 1×10⁻⁵ and I<sub>y</sub> = 0.001 are arbitrary.
- **The sensitivity matrix contradicts DEC-013:**
  - `mut_b_geo_slab` does not call `test_tc_reg_geo_slab`. It defines its own `test_repaired_slab`, asserting `Iz ≈ 0.0002148` against a candidate that returns the hard-coded 0.0002148, which is tautological.
  - It labels the result "Matches DEC-013 transformed concrete model", although DEC-013 authorises no model.
  - Condition (a) is BLOCKED = expected, so the entry counts as "VERIFIED".
- **Correct status:** BLOCKED / NOT VERIFIABLE. It must be excluded from the sensitivity count until DEC-013 is ratified by an engineering authority.

### 4.3 C02: fatigue vehicle

- **Inputs are now genuine.** The UI key is real (`KEY_LL_IRC_CLASS_FATIGUE`). The vehicle comes from the real `cl_204_6_fatigue_load()`: values 117,720 / 137,340 / 137,340 N at x = 0, 4.5, 5.9 m. These are 12 / 14 / 14 t **masses**, converted at 9.81 kN/t into **forces** of 117.72 / 137.34 / 137.34 kN. Together that is 40 t = 392.4 kN, consistent with the code comment for the IRC 6 cl. 204.6 truck.
- **Latent issue: wheel or axle load?** The source calls these values `wheel_loads` and gives two transverse wheel positions, z = ±0.84 m. If each value is later applied *per wheel*, the truck would weigh 80 t. UNVERIFIED, because the function is never consumed. A fix should assert a total vehicle load of 392.4 kN.
- **What the test checks:** only that some generated case's *name* contains "fatigue". It does not check that the case is added to the model, analysed, has the 204.6 axle loads and spacings, or affects the fatigue demand or utilisation. The (b) candidate, a `MockFatigueLC` object holding only a name, passes. **INCOMPLETE.**
- **Required:** with the toggle on:
  - a moving-load case whose axle forces and spacings equal `cl_204_6_fatigue_load()`;
  - a non-zero analysed response in its results;
  - the fatigue stress range or DCR derived from that case;
  - a change in the fatigue utilisation when the toggle changes.

### 4.4 C01: both fatigue paths

- **Real code is exercised:** `_extract_demands_from_analysis_results`, envelope path (`designer.py:2970–2988`) and per-load-case path (`:3082`). Only `classify_loadcases` and `build_girders` are mocked, which is appropriate.
- **Baseline results:**
  - Path (a) gives 125.458 MPa, that is 2M₀/Z<sub>e</sub> from the end-sign doubling.
  - Path (b) gives 62.729 MPa, that is M₀/Z<sub>e</sub>, a static moment treated as a range.
- **Feeding of the reported fatigue utilisation (CONFIRMED in part):**
  - Path (b) feeds `_compute_per_lc_dcr` → `per_girder[g]["per_lc"]` (`designer.py:3116, 3354`).
  - The per-selection utilisation `KEY_UTIL_FATIGUE` is the maximum of checks 8 and 9 from `get_dcr_engine_for_selection` (`plategirderbridge.py:3885–3904`).
  - Path (a) feeds the envelope `per_girder` checks used by the summary and report.
  - Which engine applies to which UI selection is UNVERIFIED in detail.
- **Fixing only one path still fails (CONFIRMED).** The (c) candidate fixes (a) only and FAILs; the converse fails the same way, because both conditions are required.
- **Sign fixture:**
  - The OpenSees 2D companion gives +12,500 N·m at end j of element 1 and −12,500 N·m at end i of element 2. That is consistent with the synthetic data pattern (+M₀ at end j, −M₀ at end i).
  - **But** the companion result is only logged, never asserted.
  - It is a plain 2D `eleForce` model, not the ospgrillage 3D local-force output that production consumes.
  - So the convention is PLAUSIBLE for the production data, not established.
- **Critical gap:** the only expected value is 0 MPa for a static case. An implementation that never computes fatigue passes: the (b) candidate sets every `stress_range_MPa = 0.0`. **INCOMPLETE.**
- **Required:** add a positive case, for example two frequent states (permanent + live, permanent only) with known Δσ = ΔM/Z<sub>e</sub>. Assert it on both paths. Assert the sign convention from an ospgrillage beam result.

### 4.5 CAP: stiffener buckling oracle

**Independent reproduction:**

| Quantity | Value |
|---|---|
| t<sub>w</sub>, d | 8 mm, 1,304 mm (designer section) |
| b1 + n1 | 101.81 + 652 = 753.81 mm (from the application result) |
| A<sub>wb</sub> | 753.81 × 8 = 6,030.48 mm² |
| KL | 0.7 d = 912.8 mm |
| r | t<sub>w</sub>/√12 = 2.309 mm |
| λ = KL/r | 395.25 |
| f<sub>cr</sub> | π²E/λ² = 12.635 MPa (E = 200,000 MPa) |
| λ̄ | √(f<sub>y</sub>/f<sub>cr</sub>) = √(350/12.635) = 5.263 |
| Curve c | α = 0.49 |
| φ | 0.5[1 + α(λ̄ − 0.2) + λ̄²] = 15.590 |
| χ | 1/(φ + √(φ² − λ̄²)) = 0.0330 |
| f<sub>cd</sub> | χ · f<sub>y</sub>/γ<sub>m0</sub> = 0.0330 × 350/1.10 = 10.51 MPa |
| P<sub>c</sub> | 10.51 × 6,030.48 / 1000 = **63.40 kN** |

Units are consistent: MPa × mm² / 1000 = kN. **CONFIRMED.**

**Clause applicability:** I did not have the IS 800 text available. The formula structure matches the cited cl. 7.1.2.1 (f<sub>cd</sub> = χf<sub>y</sub>/γ<sub>m0</sub>), and the web-strip treatment with A = (b1 + n1)·t<sub>w</sub> and KL = 0.7d matches the application's own cl. 8.7.3.1 / IRC 22 509.7.3.1 citation. The clause wording itself is UNVERIFIED.

**Sensitivity of the oracle to modelling choices:**
- Curves a / b / c / d give 66.6 / 65.1 / 63.4 / 60.6 kN.
- The "λ = 2.5 d/t" slenderness form gives 59.8 kN.
- All of these lie inside the ±15 % tolerance. The oracle confirms the order of magnitude and the presence of the slenderness reduction, not the choice of curve or slenderness definition. That is acceptable as long as it is stated.

**Can a clamp or hard-coded value pass?**
- The clamp (1,918.8 kN, 318.18 MPa) FAILs both the oracle and the strict elastic bound. CONFIRMED.
- **A hard-coded 63.4 kN passes.** The (b) candidate is exactly that, because only one geometry is tested.
- `res.get("A_wb_mm2", 6030.48)` silently falls back to a constant if the key disappears.

**Required:** test at least two geometries with different t<sub>w</sub> and d (for example 10 mm × 1,000 mm), compute the oracle from inputs rather than from returned keys, and make a missing key fail the test.

### 4.6 B01: dimensional hierarchy

- **Input semantics:** the fixture supplies **user inputs** `section_input.depth = 1340` and `section_input.web_depth = 1306` for every girder, with flanges set to "All" (optimised).
- **DEC-014's premise is inaccurate.** It describes 1340 / 1306 / 17 as values from "preliminary sizing". They are explicit user entries. Whether D governs is a product decision that DEC-014 records as "APPROVED", but it was ratified by the testing workstream itself, not by the developers.
- **Trace (CONFIRMED):**
  - D and d<sub>w</sub> are resolved independently; flanges snap to 18 mm.
  - The designer holds D and uses d<sub>w</sub> = 1,304 mm.
  - `input_dict` keeps 1,306 mm.
  - `create_sections()` copies the preliminary `SECTIONAL_*` values into `girder_props`, then builds `og.create_section` / `og.create_member` objects from them during setup (`analyser.py:165–179, 230–245`).
- **The test detects the defect:** all 4 girders are 7.40 % / 10.55 % off, and D ≠ d<sub>w</sub> + 2t<sub>f</sub>.
- **But it checks the wrong object.** `girder_props` is a record copied *before* the OpenSees sections are created. My probe applied the harness's own B01 "correct" patch, which replaces `girder_props` after setup, then analysed a 100 kN point load:
  - midspan deflection: 4.724596 mm, **identical to baseline**;
  - `girder_props` I<sub>z</sub>: now 0.00792758 m⁴.

  The test would pass while the solver still uses the preliminary stiffness. **INCOMPLETE.**
- **Required:** assert the section actually assigned to the solver (`girder_sections[i]` / member objects, or OpenSees element properties), or a response-based check. One example is a midspan deflection under a known load against a hand calculation with the snapped section.

### 4.7 FS: production database path

- **Production path (CONFIRMED):**
  1. `ui_fields_project_location.DB_PATH` = `<package>/core/data/project_location/weather.sqlite` (lines 15–17).
  2. `_with_db` → `Database(DB_PATH).connect()` (lines 20–28). `report_generator.py:664–666` and `project_location.py:932` use the same path.
  3. `connect()` opens the file with `sqlite3.connect` (creating it if missing) and runs `schema.sql` if the file was missing **or** the `stations` table is absent (`database.py:19–30`).

  So the application **creates, and if `stations` is missing re-populates**, `weather.sqlite` inside the package directory. The file in your workspace (180,224 B) dates from 05:48 UTC, during Phase 1D, and is unchanged since.
- **What the test checks:**
  - Check 1 is a string test on the path: `"osdagbridge" in path and ("core" or "src")`. It observes no creation or rewrite.
  - Check 2 is the default-constructor behaviour, which is a different issue: an unanchored relative default used only by `database.py:356`'s `__main__` block.
- **Consequences:**
  - A standard correct design, shipping a pre-built read-only database in the package and never writing to it, fails Check 1.
  - The (b) candidate passes only because `%TEMP%\OsdagBridgeAppData` contains no lowercase "osdagbridge". This is fragile.
- **Classification:** filesystem / packaging / reproducibility defect. Test **INVALID** as a detector of that defect.
- **Required:**
  - Copy the package-data directory to a temporary location (or make it read-only), import the production module there, call a `_with_db`-wrapped function, and assert that no file is created or changed.
  - Test the default-constructor issue separately.
  - Note that the sensitivity run itself left `weather.sqlite` files in the system temp folder. This happened in my run; on your machine it is UNVERIFIED, because that folder is outside the connected workspace.

---

## 5. Sensitivity protocol verification

**Execution.** I ran `run_sensitivity_matrix.py` independently. It gave 14/14 VERIFIED, matching the 10:08 JSON files. The results are **executed, not pre-populated**: every entry comes from calling the real test function under an in-process monkeypatch, with plausible durations (A02 about 6.3 s).

**Isolation.** Patches are restored in `finally` blocks, and the frozen source is unmodified (§6). Side effects:
- per-test logs in `phase_2_1/` are overwritten during the matrix run;
- temporary `weather.sqlite` files are left in the system temp folder.

**History.** `sensitivity_matrix.log` (09:58:39), from the earlier script versions, records:
- A01, B01, D01, CAP and MAT: UNVERIFIED;
- CAP: (b) FAIL and (c) **PASS**;
- B01, D01 and MAT: (b) and (c) BLOCKED.

No console log exists for the final 10:08 run. Iterating until green is allowed, but this history is undisclosed.

| Test | (b) "minimal correct": what it actually changes | Real implementation? | (c) "naive": what it changes | Informative? | What this proves |
|---|---|---|---|---|---|
| A01 | `LoadCase.add_load` deep-copies the load, scales `load_point_1..4`, adds with factor 1 | Partial. Incomplete for compound/patch loads (probe: BASIC_1 still ≈ unfactored). | scales by 1.15 | Yes | A01 accepts an incomplete library fix |
| B01 | replaces the `girder_props` record **after** the model is built; rewrites `web_depth` keys | **No.** Solver stiffness unchanged (probe). | updates girder 0 only | Yes | **A false pass is possible** |
| C01 | sets every `stress_range_MPa = 0.0` after the call | **No** (degenerate) | zeroes path (a) only | Yes | **"No fatigue" passes** |
| A02 | wraps `get_results` to *replace* BASIC_1 `Vy_i` with 1.35DL + 1.75DW; sets `sidl_combination = "MockSIDLCombination"` | **No** (spoofs the observation) | sets the SIDL string only | Yes | **One-component spoof and string attribute pass** |
| D01 | reimplements `add_wind_loads` reading the 4 real keys | **Yes** | reads speed only | Yes | Genuine sensitivity |
| D02 | sets `temperature_load_case = "MockTemperatureLoadCase"` if the key is present | **No** | equivalent to baseline | No | **Any object passes** |
| C02 | appends `MockFatigueLC(name="IRC Cl. 204.6 Fatigue Vehicle")` | **No** | invented key, so no case (= baseline) | No | **Name-only check** |
| RPT | string-replaces "pass" with "fail" when "Fail" appears | Text post-processor only | rewords the literal | Yes | Detects rewording; doesn't cover other components |
| GEO-COUNT | sets `n_girders = _girder_count()` | **Yes** | `n_girders = 0` | Trivial | Genuine (weak naive case) |
| GEO-SLAB | hard-coded section **and a substitute assertion**; the real test is not called | **No.** Unauthorised under DEC-013. | girder/4 against the same substitute | No | **Not verifiable; must not count** |
| CAP | sets `Fcdw_wb_kN = 63.4`, `fcc_wb_MPa = 12.63` | **No** (hard-coded) | clamp at 1,918.8 kN | Yes | **Hard-coding passes**; clamp rejected |
| MAT | swaps the module constant to the input density during `add_dead_loads` | Yes (minimal) | no change (= baseline) | No | Genuine (weak naive case) |
| FS | repoints `DB_PATH` and the default to `%TEMP%\OsdagBridgeAppData` | Partly; passes through the path string | moves the default only | Yes | Path-string check, not behaviour |
| CAD | identical to baseline | n/a | uniform-grey PNG | Yes | Environment check is sensitive to blank images |

**Assessment:**
- Genuine correct-versus-incorrect discrimination is shown for **D01, GEO-COUNT, MAT and CAD**, and for A01 and RPT within their limited scope.
- For **B01, C01, A02, D02, C02 and CAP**, the "correct" candidate is itself an incorrect or degenerate implementation that passes. That establishes the tests' *vulnerability*, not their sensitivity.
- GEO-SLAB is not verifiable.
- "14/14 verified" is **CONTRADICTED** as a statement of test reliability.

---

## 6. Repository integrity

| Check | Result |
|---|---|
| `HEAD` | `ref: refs/heads/dev` → `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` |
| Lock files / index | No `.lock` files. `.git/index` mtime is 2026-11-15 12:26:18 UTC, unchanged since before Phase 2. |
| Source content | The aggregate of per-file SHA-256 values over all 282 non-ignored files under `src/` (CR-normalised) is `c6d61d03…a89d`, **identical** to a clean clone of `d74f56d` and to my previous audit. |
| Databases | `Intg_osdag.sqlite`: SHA-256 `25f97857…ea91`, byte-identical to baseline. Untracked `weather.sqlite`: `1d767658…7e98`, mtime 05:48 UTC, unchanged by Phase 2.1. |
| Source files changed since 09:30 UTC | none, including `__pycache__` |
| Workspace changes since 09:30 UTC | the two runner scripts, `phase_2_1/` evidence, three reports, `CHANGELOG.md`, `DECISIONS.md` and `PROGRESS.md`. `reports/PHASE_2_FINAL_INDEPENDENT_GATE_AUDIT.md` (09:32:47) is my previous deliverable, byte-identical to what I wrote. |
| The reports' "git status clean" | consistent with the above; the git command itself was not re-run, to avoid lock-file side effects |

**Conclusion:** the application repository remains at the frozen baseline and unmodified (CONFIRMED). All Phase 2.1 work is confined to testing assets, evidence, reports and tracking documents.

---

## 7. Exact outstanding actions

1. **B01:** assert the solver-side sections (`grillage_model.girder_sections[i]` or the member objects, or OpenSees element properties), or a deflection check with a hand oracle. Re-run sensitivity with a candidate that changes the analysed stiffness.
2. **C01:** add a positive fatigue case with a known non-zero Δσ on both paths. Assert the OpenSees sign companion, preferably from an ospgrillage result, not only log it.
3. **A02:**
   - Add the total-reaction identity Σ R(BASIC_1) = Σ γᵢ·Rᵢ over independently built SW, deck, DW and barrier cases (plus railing or median if present).
   - Compare Mz_i and Mz_j as well as Vy_i.
   - Replace the attribute-based SIDL and barrier checks with "barrier load present in BASIC_1".
   - Record the SIDL factor source (IRC 6 Annex B).
4. **A01:** add patch and compound load types, or move the factor-honouring assertion to the application path (`_copy_loads`). Its correct candidate must also make A02's factor identity hold.
5. **C02:** assert the axle forces and spacings against `cl_204_6_fatigue_load()` (total 392.4 kN, and resolve the wheel-versus-axle question), analysed participation (a non-zero response), and its effect on the fatigue range and utilisation.
6. **D02:** first record the thermal representation (IRC 6 cl. 215); then assert magnitude and combination membership. Until then, mark the test BLOCKED like GEO-SLAB.
7. **CAP:** add at least one more geometry. Compute the oracle from inputs. Fail on missing result keys. State in the test that the ±15 % tolerance does not discriminate the buckling curve.
8. **FS:** replace the path-string check with an observed side-effect test: package-data copy or read-only directory, the `_with_db` call, and before/after hashes and listing. Keep the default-constructor check as a separate test. Clean up the temporary files the matrix creates.
9. **RPT:** assert all four component lines (girder, cross bracing, end diaphragm, deck) against their own results, and use a semantic match rather than one literal.
10. **GEO-SLAB:** keep it BLOCKED. Remove the substitute assertion and the "Matches DEC-013" wording from the sensitivity harness. Exclude it from the verification count until an engineering authority ratifies DEC-013.
11. **Sensitivity harness:**
    - Every (b) candidate must change behaviour upstream of the observation (no result spoofing, mocks, placeholders or hard-coded outputs).
    - Every (c) candidate must differ from the baseline.
    - The harness must exit non-zero when any entry is UNVERIFIED.
    - It must write to its own evidence folder, without overwriting the runner's logs.
    - Capture console output and exit status for the final run, and keep superseded runs with their script hashes.
12. **Runner:**
    - Abort on a fixture-hash mismatch.
    - Record the repository HEAD by reading `.git/HEAD` (not a constant) and the runner's own SHA-256.
    - Replace `osdagbridge.__file__` with the path of a concrete module.
    - Add a post-remediation expectation manifest so Phase 3 progress and regressions can be gated. A permanently BLOCKED test makes exit 0 unreachable.
13. **Reports:**
    - Correct the fixture paths and hashes (the real values are `31ae62dc08a0…0191` and `429a3198fc93…a5ab`; `testing/fixtures/` does not exist).
    - Disclose the 09:58 UNVERIFIED sensitivity run.
    - Restate "14/14 verified" according to §5.
    - Correct DEC-014's description of 1340 / 1306 as user inputs, and record who ratified the D-governs rule.
14. **Phase 3 has not been started** and should not start until items 1–12 are complete and re-audited. The re-audit can be limited to the changed tests and the sensitivity harness.

---

## Verdict

**REJECT PHASE 2.1 REGRESSION SUITE**
