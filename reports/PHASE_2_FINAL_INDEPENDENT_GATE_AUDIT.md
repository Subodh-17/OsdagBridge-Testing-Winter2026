# Phase 2 Final Independent Gate Audit: Repaired Regression Suite

**Scope:** check the claim that the repaired Phase 2 suite is ready to gate Phase 3 remediation. That claim comes from:
- `reports/PHASE_2_REGRESSION_SUITE_REPAIR.md`
- `reports/PHASE_2_BASELINE_REVALIDATION.md`, which says "READY FOR REMEDIATION"

**Controlling document:** `PHASE_2_REGRESSION_INDEPENDENT_AUDIT.md`.

**Baseline:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`.

**Material examined:**
- The runner `testing/test_cases/baseline_regression/run_all_baseline_tests.py` (45,592 B, SHA-256 `12c9a796…fef7f`), read in full.
- All 14 logs and `repaired_regression_summary.json` in `testing/evidence/phase_2_repaired/`.
- Both reports.
- `DECISIONS.md` (DEC-010 and DEC-011).
- The Phase 1D input and output fixtures.

**How I checked the claims:**
- I traced every claim to the application source in a clean baseline clone.
- I ran read-only calls on the frozen source in a separate cloud environment: IRC 6 `table_12`, the mesh coordinates and the material assignment. Nothing ran in your workspace.
- I compared content hashes for repository integrity.
- In your workspace I only read files and created this report. I did not edit, install, commit, check out or run anything there.

**Evidence labels:** CONFIRMED / PLAUSIBLE / UNVERIFIED / CONTRADICTED.

---

## 1. Executive verdict

The repair is a real improvement:
- The runner exits non-zero on failure.
- Paths are now relative to the workspace.
- Eleven of the 14 tests now drive application code instead of grepping it or copying it.
- 13 baseline failures are genuine.

**The suite is still not a reliable gate:**
1. **TC-REG-A02 cannot detect DEF-01 (the dropped load factor).** Its resultant helper, `_load_case_resultant_kN`, applies the stored per-load factor itself (`analyser.py:990–993`). That is the same factor the solver ignores, so the "factor" half of the test passed on the defective baseline: 2,378.9 kN against a threshold of 1,657.9 kN. Only the attribute check on `sidl_combination` made it fail.
2. **TC-REG-GEO-SLAB passes with incorrect implementations.** Using a quarter of the steel girder (0.001835 m⁴) passes `Iz < 0.002`, and so does an untransformed concrete strip under steel E, which is about 6× too stiff.
3. **TC-REG-FS tests a code path production never uses.** It tests the `Database()` default path relative to the working directory. Every production caller passes an absolute path inside the package, so the real side effect, `weather.sqlite` written into the package, goes undetected.
4. **Three tests feed invented input keys**, so a correct fix may still fail:
   - D02 uses `max_temp`, `min_temp` and `thermal_coeff_concrete`.
   - C02 uses `loading.live_load.fatigue`.
   - The real keys exist in `common.py`.
5. **Test sensitivity is not shown for any test.** No test has been run against a corrected or deliberately mutated implementation. The reports' "Test Sensitivity" column only describes fixes that might be made.
6. **The reports contain figures the evidence contradicts:**
   - the A02 baseline mechanism;
   - the D01 wind pressure: reported as 945.7 N/m², the log and the application give 1,039.6;
   - the C02 fatigue vehicle definition;
   - the GEO-SLAB assertion;
   - the claim that "every test invokes actual application code paths": CAD calls pythonocc only.

**Verdict: REJECT PHASE 2 REGRESSION SUITE.** The remaining work is bounded and listed in §9. After it, a narrow re-audit is enough.

---

## 2. Test-by-test validity

Columns:
- **Can it detect the defect?** Does the assertion detect the original defect?
- **Correct fix could fail?** Could a correct implementation still fail the test?
- **Wrong fix could pass?** Could an incorrect implementation pass it?

| # | Test | Application function actually invoked | Synthetic or mock objects | Can it detect the defect? | Correct fix could fail? | Wrong fix could pass? | Classification |
|---|---|---|---|---|---|---|---|
| 1 | A01 factor scaling | ospgrillage `LoadCase.add_load(load_factor=)` and `model.analyze` on the real model | none | Yes. Ratio 1.00000 against 1.35. | Yes, if remediation scales loads in `_copy_loads` instead of patching ospgrillage | No | **VALID** (upstream scope; needs an application-path companion) |
| 2 | B01 section sync | `_stage_grillage_setup` → `girder_props[i]` | hand-written I-section oracle (correct formula) | Yes. 7.40% I<sub>z</sub>, 10.55% A, all 4 girders. | **Yes.** The extra d<sub>w</sub> assertion assumes D is authoritative (§4.2). | No | **VALID WITH CORRECTIONS** |
| 3 | C01 fatigue range | `designer._extract_demands_from_analysis_results` (production envelope path) | synthetic xarray; mocked `build_girders` and `classify_loadcases` (appropriate) | Yes, for the envelope path | Possible, if the fix moves fatigue to the fatigue vehicle case and returns 0 trivially | **Yes.** The per-load-case path (`designer.py:3082`) is untested (§5.3). | **VALID WITH CORRECTIONS** |
| 4 | A02 ULS sum | `create_uls_combinations` and `_load_case_resultant_kN` | none | **No, for DEF-01.** The helper applies the stored factors. It detects DEF-02 only through the attribute check. | Yes. A correct SIDL fix without `sidl_combination` fails. | Yes. Calling `create_sidl_combination()` alone passes. | **INVALID TEST** |
| 5 | D01 wind | real `add_wind_loads`; a wrapper spy on `create_wind_load` passes the call through | none | Yes. All 4 arguments fall back. | No. All 4 keys are real UI keys (`common.py:427, 446, 768, 769`). | No | **VALID** (minor: assert P<sub>z</sub>) |
| 6 | D02 temperature | real `add_temperature_load` | **invented keys** | Yes. Case is `None`. | **Yes.** A fix that reads the real keys `highest_max_temp`, `lowest_min_temp` and `thermal_coeff_rcc` gets no input from this test. | Yes. Any non-zero resultant passes. | **VALID WITH CORRECTIONS** |
| 7 | C02 fatigue vehicle | real `add_vehicle_load_cases_from_combinations` | **invented toggle key** (harmless: the real key is already True in the base configuration) | Yes. Only 2 cases exist. | Yes, if the new case's name doesn't contain "fatigue" | **Yes.** Any case named "fatigue", with any axles and never analysed, passes. | **VALID WITH CORRECTIONS** |
| 8 | RPT summary | real `executive_summary()` | output dictionary hand-made in a shape the function doesn't read | Yes. The literal is still emitted. | Possible. The application sees zero girders in this dictionary. | **Yes.** Rewording the literal passes. No passing scenario is tested. | **VALID WITH CORRECTIONS** |
| 9 | GEO count | `BridgeConfig.from_plate_girder_bridge` against `_girder_count()` | none | Yes. 6 against 4. | No | No | **VALID** (affects reported output only) |
| 10 | GEO-SLAB | `_transverse_section()` | none | Yes, at baseline | Possible, depending on the representation chosen | **Yes** (girder/4; untransformed concrete under steel E) | **INVALID TEST** |
| 11 | CAP stiffener | real `compute_bearing_stiffener()` | input overrides consistent with Phase 1D | Yes. 134,083 kN. | Unlikely | **Yes.** Clamping fcc at f<sub>y</sub>/γ<sub>m0</sub> gives exactly 1,918.8 kN and passes. | **VALID WITH CORRECTIONS** |
| 12 | MAT density | `grillage_model.create_self_weight_load()` called directly | expected value built from a **hard-coded preliminary area** | Yes. 169.82 kN matches 78.5 exactly. | **Yes.** (a) After a DEF-03 fix the area changes. (b) A fix that passes the density in through `add_dead_loads` is bypassed. | No | **VALID WITH CORRECTIONS** |
| 13 | FS side effect | `Database()` with its default relative name, in a temporary directory | — | Detects a default production never uses | Yes, if the fix anchors the default but is otherwise valid | **Yes.** The package-directory write in production (`ui_fields_project_location.py:15–24`) is untouched. | **INVALID TEST** |
| 14 | CAD export | **pythonocc `Viewer3d` on a box only.** The application's `PlateGirderBridge._export_cad_figures` is not called. | synthetic geometry | Not a defect test | — | A blank RGB image passes (opacity is set to 1.0 for RGB) | **Harness/environment verification only. VALID WITH CORRECTIONS for that purpose.** |

**Totals:**
- 3 valid: A01, D01, GEO-COUNT.
- 8 valid with corrections: B01, C01, D02, C02, RPT, CAP, MAT, CAD (harness).
- 3 invalid: A02, GEO-SLAB, FS.
- 0 false positives, 0 blocked.

---

## 3. Execution completeness

| Question | Finding | Status |
|---|---|---|
| Did every test complete? | 14 logs and 14 summary entries: 13 FAIL, 1 PASS, 0 BLOCKED. The summary is written only after the loop ends (`main()`), so it exists only because the loop completed. | CONFIRMED |
| Was the run made with the current script? | Script last modified 08:15:04.50 UTC. `.pyc` compiled 08:15:11. Logs 08:15:24.01–08:15:58.61. Summary 08:15:58.63. The script has not changed since. | CONFIRMED |
| Was a background task still running when the reports were written? | Reports were written at 08:17:10 and 08:17:45, after the summary. No artefact from a later run exists. I can't rule out a concurrent process positively, but nothing suggests one. | PLAUSIBLE (no indication) |
| Does the recorded exit code belong to the final run? | **No exit code was captured**: there is no stdout log and no exit-status file. "Exit code 1" is consistent with the runner's logic (13 FAIL → `sys.exit(1)`) but is asserted, not evidenced. | UNVERIFIED |
| Are PASS / FAIL / BLOCKED / NOT RUN distinguished? | PASS, FAIL and BLOCKED are. **NOT RUN does not exist.** If the import fails (numpy, PIL, `INPUT_JSON`) or `log_test_result` fails, the whole run aborts with no summary and no per-test attribution. | Partly |
| Are exceptions reported accurately? | Every test wraps its body in `except Exception` → BLOCKED with traceback. That is adequate. The logs carry no timestamps, durations, interpreter, package versions or commit SHA, so no single log can be tied to an environment. | Adequate; provenance thin |
| Is the evidence directory clean? | It is overwritten in place, with no run ID. A test removed from the list would leave a stale log beside a fresh summary. | Risk |
| Is the previous evidence still traceable? | The original runner was **overwritten under the same filename**, and its hash was never recorded. The logs in `testing/evidence/phase_2_baseline/` no longer have a script that produces them. | Provenance gap |

---

## 4. GEO-SLAB and B01

### 4.1 GEO-SLAB (DEF-14)

**The contradiction between the two reports, resolved.**
- The repair report says the test "computes concrete slab strip properties… asserts positive slab model".
- The revalidation table gives the expected value as "≈ 0.001302 m⁴ and ≠ girder/2".
- **The test asserts neither.** Its actual predicate (runner line 721) is `not is_half_steel_girder and transverse.Iz < 0.002`. The 0.001302 value appears only in a comment. A, J and I<sub>y</sub> are not asserted.

**What the model actually does (CONFIRMED from source and a read-only run):**
- The transverse section is built with `og.create_section(..., unit_width=True)` (`analyser.py:193–201`). ospgrillage multiplies unit-width properties by each element's width (`osp_grillage.py:905–915`). So the intended input is **per metre width**.
- The mesh transverse spacing is 1.5 m: `nox` = 0, 1.5, …, 24.
- **All transverse members use the steel material** `self.steel_custom`, with E = 200 GPa (`analyser.py:246–250`).
- The model has concrete properties available: M40, E<sub>cm</sub> = 33 GPa.
- Deck thickness is 250 mm.

**What this implies:**
- A valid representation must either assign a concrete material to the slab members, or give steel-equivalent (transformed) properties.
- The gross uncracked strip, transformed, is I = t³/12 ÷ (E<sub>s</sub>/E<sub>cm</sub>) = 0.001302 / 6.06 ≈ 2.15×10⁻⁴ m⁴/m.
- Cracked versus uncracked section, torsion constant and effective width are engineering decisions. I am not prescribing them; the project has not recorded any of them.

**Why the oracle fails:**

| Candidate implementation | I<sub>z</sub> (m⁴) | Passes `< 0.002`? | Correct? |
|---|---|---|---|
| Girder/4 (steel) | 0.001835 | **Yes** | No |
| Concrete strip, untransformed, under steel E | 0.001302 | **Yes** | No (≈6× too stiff) |
| Transformed strip | ≈0.000215 | Yes | Plausibly |
| Concrete strip ×1.5 m, if someone ignores `unit_width` | 0.001953 | Yes | No (double-counts width) |

The threshold does not separate correct from incorrect implementations. **INVALID.**

**DEF-14 itself:** the code uses half of the preliminary steel girder, multiplied by 1.5 m, for a concrete slab. As a modelling defect that is PLAUSIBLE, strongly. The correct model is UNDECIDED.

### 4.2 B01 (DEF-03): 1306 mm vs 1304 mm

**Trace, CONFIRMED:**
1. The input fixture **explicitly supplies both** total depth `section_input.depth = 1340` and web depth `section_input.web_depth = 1306`, for every girder. The flange thicknesses are `"All"`, meaning the optimiser chooses them.
2. 1340 − 1306 = 34 = 2 × 17, so the user's D and d<sub>w</sub> agree with 17 mm flanges.
3. `_resolve_optimized_bounds_to_mm` handles `KEY_MP_GIRDER_DEPTH` and `KEY_MP_GIRDER_WEB_DEPTH` independently (resolver lines ≈498–520). Numeric entries are kept; `"All"` flanges are snapped up to the SAIL-approved thickness of 18 mm.
4. After snapping, D (1340), d<sub>w</sub> (1306) and t<sub>f</sub> (18) **cannot all hold** at once. The designer resolves this by keeping D and deriving d<sub>w</sub> = 1304 (`design_results/dw_mm = 1304`; bearing-stiffener n1 = 652 mm, KL = 912.8 mm). The input dictionary keeps 1306.
5. The grillage uses neither. It uses the preliminary `SECTIONAL_AREA` and `SECTIONAL_IZ` values (A 22,534 mm², I<sub>z</sub> 7.341×10⁹ mm⁴). These don't correspond to any of the plate combinations above.

**Findings:**
- **The 7.40% I<sub>z</sub> / 10.55% A gap is a genuine synchronisation defect.** The analysed stiffness is not the designed section, whichever depth convention is used. CONFIRMED.
- **The 1306 / 1304 split is a second, separate inconsistency.** The reports call 1306 "stale from pre-snapped t<sub>f</sub> = 17 mm". That is inaccurate: 1306 is the user's explicit input, carried unchanged. Whether D or d<sub>w</sub> should govern when snapping makes them inconsistent is an **undocumented design decision**. Keeping D matches the designer's current behaviour; keeping d<sub>w</sub> (D → 1342) is equally defensible.
- **Stage checked:** the test inspects `girder_props` straight after `_stage_grillage_setup()`. That is where they are assigned, so it is the correct stage.
- **Correction needed:**
  - Replace `dw_dict == D − 2t<sub>f</sub>` with a consistency check: D = d<sub>w</sub> + t<sub>f,top</sub> + t<sub>f,bot</sub> after resolution.
  - Require that the grillage properties equal the section the designer checks, for all girders and for A, I<sub>z</sub>, I<sub>y</sub> and J.
  - Record which dimension governs in `DECISIONS.md`.

---

## 5. Engineering-oracle review

### 5.1 A02: ULS generation, factors, equilibrium

- **The ULS combination is real (CONFIRMED).** `create_uls_combinations` builds BASIC_1 as 1.35·DL + 1.75·DW + LL-lead (`analyser.py:2276, 2318–2420`).
- **The resultant is not a solver result.** `_load_case_resultant_kN` "integrates the total applied resultant … directly from its load objects", and **applies the stored per-load factor** (docstring, 990–993). DEF-01 is exactly that the solver ignores this stored factor. The resultant therefore shows the intended factored load whether or not the solver applies it, which makes it structurally blind to DEF-01.
- **The oracle has errors:**
  - It reads `surfacing_load_case`, an attribute that doesn't exist. The real attribute is `wearing_course_load` (`LC_ATTR_MAP`, 2318–2324). As a result DW = 0 in the oracle, while BASIC_1 contains about 1.75 × 244.8 kN of DW: 2,378.9 − 1.35 × 1,444.8 = 428.4 kN.
  - Crash-barrier load is not considered.
  - The comparison is one-sided (`r < 0.85 × expected`), so omitting barrier loads or any extra term can't fail it.
  - No equilibrium check is made.
- **The reports misstate the baseline.** They say "R<sub>ULS</sub> ≪ R<sub>expected</sub>". The log shows 2,378.9 kN > 1,950.5 kN, so the factor branch never fired. CONTRADICTED.
- **Required instead:** for an analysed combination, the sum of vertical support reactions should equal Σ γᵢ × (reaction sum of component i). The components (SW, deck, DW, barrier and SIDL) should come from the analysed model. Also assert that the SIDL and barrier loads are present. This identity fails while DEF-01 exists and passes once factors are honoured.

### 5.2 D01 / D02: input keys

- **D01:** all four keys are genuine UI keys, `KEY_WL_BASIC_WIND_SPEED`, `KEY_WL_AVG_EXPOSED_HEIGHT`, `KEY_CB_HEIGHT` and `KEY_RL_HEIGHT` (`common.py:768, 769, 427, 446`). `KEY_WL_BASIC_WIND_SPEED` is wired to the UI field at `ui_fields_additional_input.py:818`. The spy wraps the real call, so the propagation tested is real. Table 12 gives 1,039.59 N/m² at 47 m/s and 15 m, and 463.7 N/m² at 33 m/s and 10 m (both reproduced). The reports' 945.7 is CONTRADICTED. P<sub>z</sub> is computed but not asserted.
- **D02:** the real keys are `KEY_TL_HIGHEST_MAX_TEMP` and `KEY_TL_LOWEST_MIN_TEMP`, the computed `temp_rise`/`temp_fall`, and `KEY_TL_THERMAL_COEFF_RCC` (`common.py:819–826`). The test's keys exist nowhere in the source.
  - The revalidation's "remediation rule" is to convert ΔT into an equivalent pressure. IRC 6 cl. 215 thermal effects are restraint and gradient effects, not an applied pressure, and the report itself notes this. The rule is not traced to any code requirement.
  - The oracle (`r_temp > 0`) cannot be made meaningful until the representation is decided.

### 5.3 C01: is the production fatigue path exercised?

There are **two** fatigue-range paths in `designer.py`:
- **(a) Envelope path,** lines 2970–2988: `max(max,0) − min(min,0)` over `Mz_i` and `Mz_j` of all SLS_FREQUENT combinations. It feeds `per_girder_demands`. The test exercises this path and shows the doubling: 125.458 MPa = 2 × 10⁶ Nm / Z<sub>e</sub>. CONFIRMED. The Phase 1D value agrees: 182.63 = 2 × 1,455.73 kNm / 15.94×10⁶ mm³.
- **(b) Per-load-case path,** line 3082: `_stress_rng = Mz × 10⁶ / Ze`. This uses the **absolute single-case moment** as a "range". It feeds `_compute_per_lc_dcr` (line 3126) and the design-envelope engine that produces `KEY_UTIL_FATIGUE` (`plategirderbridge.py:3792, 4107`).

The test does not exercise path (b). A fix to (a) alone would leave the reported fatigue utilisation computed from a static moment. The i/j sign premise is still assumed rather than established from an ospgrillage result.

**Corrections:**
- Add a path (b) assertion.
- Add a sign-convention companion test on a simply supported beam.
- Assert that the fatigue range comes only from the fatigue-vehicle case. This ties to C02.

### 5.4 C02: does the fatigue vehicle take part in the analysis?

No. The test only checks a case **name** list.
- `cl_204_6_fatigue_load` defines 12 / 14 / 14 t axles (`irc6_2017.py:370–410`). The reports' "120 kN and 140 kN at 4.0 m" is CONTRADICTED by the source.
- The real toggle `loading.live_load.irc.class_fatigue` is already True in the base configuration. The test sets a non-existent key instead.

**Required:**
- With the real toggle on, a moving case must exist whose axle loads and spacing equal `cl_204_6_fatigue_load()`.
- That case must be analysed: a non-zero response in its results.
- The fatigue stress range must be derived from it.

### 5.5 RPT: is the summary derived from design results?

Partly.
- `overall_design_status` **is** derived. It comes from `design_results["per_girder"][g]["checks"]`, using the status and the DCR > 1 test (`executive_summary.py:71–110`).
- Lines 233–236 are hard-coded.
- The test's failing dictionary has no `per_girder`, so the application treats it as having **no girders** (status ""). It is not a failing design as the application understands one.
- Only one scenario is tested, and the assertion is a literal string.

**Required:**
- Use the real Phase 1D `output_dictionary_snapshot.json`, whose `per_girder` includes fatigue DCR 1.97. Assert that no component is reported as passing while it has a failing check, and that the failing check is named.
- Add a mirror case built from a dictionary where every check passes, asserting that the pass text appears.

### 5.6 CAP-STIFFENER: is the yield bound valid?

- **Implementation (CONFIRMED, `designer.py:1663–1671`):** fcc<sub>wb</sub> = π²E/(KL/r)², with no imperfection reduction.
  - r = √(I<sub>ys</sub>/A<sub>wb</sub>) mixes the stiffener inertia with the web strip area.
  - KL = 0.7d.
  - A<sub>wb</sub> = (b1 + n1)·t<sub>w</sub> = (101.81 + 652) × 8 = 6,030.48 mm².
  - Result: F<sub>cdw,wb</sub> = 22,234 MPa × 6,030.48 = 134,083 kN.
- **The bound applies.** I did not have the IS 800 text available. On the clause structure the code cites: under IS 800 cl. 7.1.2.1, f<sub>cd</sub> = χ·f<sub>y</sub>/γ<sub>m0</sub> with χ ≤ 1. The code's own cl. 8.7.3.1 / IRC 22 cl. 509.7.3.1 comment says the web resistance is f<sub>cd</sub> × (b1 + n1)·t<sub>w</sub>. Therefore F<sub>cdw,wb</sub> ≤ (f<sub>y</sub>/γ<sub>m0</sub>)·A<sub>wb</sub> = 318.182 × 6,030.48 / 1000 = 1,918.8 kN. Units are consistent: MPa × mm² / 1000 = kN.
- **But the bound is only necessary, not sufficient.**
  - An implementation that clamps the Euler stress at f<sub>y</sub>/γ<sub>m0</sub>, still unreduced and still with the mixed r, produces exactly 1,918.8 kN and **passes** (`<=`).
  - The bound is hard-coded, and it inherits the application's own A<sub>wb</sub>. A fix that changes b1 or n1 changes the true bound, but the test keeps 1,918.8.
  - The test computes f<sub>y</sub>/γ<sub>m0</sub> from configuration and never uses it.
- **Required:**
  - Compute the bound from the result's own `A_wb_mm2` and the configuration's f<sub>y</sub>/γ<sub>m0</sub>.
  - Add a positive oracle: the web strip with r = t<sub>w</sub>/√12, KL = 0.7d and the cited buckling curve, calculated independently in the test from the cited clauses.
  - Assert `fcc_wb_MPa` < f<sub>y</sub>/γ<sub>m0</sub> strictly, given the slenderness (KL/r ≈ 395).

### 5.7 MAT-DENSITY

- **The value 70.0 separates user input from both the database (78.5) and the constant (78.5)** (CONFIRMED). The database and the constant are numerically identical, so a fix that reads the database instead of the input would correctly fail. Whether that is the intended rule is DEC-pending.
- **Problems with the expected value:** it is `4 × 0.02253434 × 24 × ρ`, using the preliminary area, which ties it to DEF-03.
  - After DEF-03 is fixed (A = 0.025192 m²), a correct density fix gives 4 × 0.025192 × 24 × 70 = 169.3 kN. Against the 151.4 kN expectation that is a **FAIL**.
- **Problems with the entry point:** the test calls `grillage_model.create_self_weight_load()` directly, bypassing `add_dead_loads()`. A fix that routes the density through the bridge layer would not be exercised.
- **Required:** derive the expected load from the model's own member areas and span, and call the production entry point.

### 5.8 FS

- **What the test detects (CONFIRMED):** `Database.__init__(db_name='weather.sqlite')` is relative to the current directory. Only the manual `__main__` block (`database.py:356`) uses that default.
- **What production does:** every production caller passes the package path:
  - `ui_fields_project_location.py:15–24` (wrapped in `_with_db`);
  - `report_generator.py:664–666`;
  - `project_location.py:932`.
  - `Database.connect()` **creates the file if it is missing** (`database.py:19–30`).
  - `zone_lookup.py:183` also uses the package path, but returns early if the file is missing.
- **Effect:** the production side effect, writing into the installed package directory, is untested. A fix that only anchors the default would pass.
- **Required:** run the production entry points (`_with_db`-wrapped calls) with the package directory read-only, or on a copy. Assert that nothing is created or changed there, and that tracked database hashes don't change. Also cover the `create_sqlite` / `ensure_osdag_core_db` path in `desktop/__main__.py:109–195`.
- **Classification (as requested):** filesystem / reproducibility / packaging defect, not engineering design.

### 5.9 CAD-EXPORT

- **What runs:** native OCC `Viewer3d.ExportToImage` **is** exercised offscreen and produces a 656×519 RGB PNG (CONFIRMED from the log). That supports classifying the Phase 1D transparency as a harness artefact.
- **What doesn't run:** the application's export, `PlateGirderBridge._export_cad_figures` (`plategirderbridge.py:804–920`, headless `Viewer3d`, gradient background, `ExportToImage`), is not called. The bridge model is not displayed.
- **Weak content check:** for RGB images `opaque_ratio` is set to 1.0, so a blank background passes. At 4,324 B the PNG is small, and its content is UNVERIFIED.
- **Correct classification:** environment/harness verification, not a regression test. To guard the application, call `_export_cad_figures` on the real CAD generator and assert a minimum share of non-background pixels.

---

## 6. Test sensitivity

The previous gate required each test to be shown to distinguish defective from corrected behaviour. **The evidence does not show this for any test.**
- The "Test Sensitivity (Minimal Code Fix)" column in the repair report lists fixes that *might* be made. No test was run against a fix or a mutation.
- §2 shows that for at least A02 (DEF-01), GEO-SLAB, CAP, C02, RPT and FS, an incorrect implementation would pass.
- For B01, D02 and MAT, a correct implementation could fail.

**What remains necessary.** None of this touches the frozen repository or manufactures a pass in it.
1. Create a separate `sensitivity/` harness, isolated in a disposable copy of the source or via in-process monkeypatching, and clearly labelled as such. For each test, record:
   - (a) baseline → FAIL;
   - (b) a minimal correct candidate → PASS;
   - (c) at least one plausible *wrong* candidate → FAIL. Examples:
     - A02: call `create_sidl_combination` but leave factors ignored.
     - GEO-SLAB: girder/4.
     - CAP: clamp at f<sub>y</sub>/γ<sub>m0</sub>.
     - C02: a case named "fatigue" with Class A axles.
     - RPT: reword the literal.
     - FS: anchor only the default.
     - MAT: change the constant to 70.
2. Store the results of (a), (b) and (c) per test with commit SHA, environment and duration.
3. Discard all candidate code afterwards. Phase 3 then implements the real fixes on the remediation branch.

---

## 7. Runner and portability

| Requirement | Finding | Status |
|---|---|---|
| Non-zero exit on failure | `sys.exit(1)` if any FAIL or BLOCKED (lines 1013–1018) | CONFIRMED in code; not captured for this run |
| Correct status accounting | Correct counts of PASS, FAIL and BLOCKED. **`expected_baseline` is recorded but never compared.** There is no strict expected-failure (xfail) concept, so mid-remediation (some fixed, some not) the runner always exits 1 and cannot detect a *regression* in an already-fixed test. An unexpected baseline PASS would not be flagged either. | Gap |
| Workspace-relative paths | `SCRIPT_DIR` → `WORKSPACE_ROOT`. No drive letters in the code. The reports still embed `file:///F:/` links (cosmetic). | CONFIRMED |
| Missing dependencies | Imports inside each test become BLOCKED with traceback and exit 1. numpy and PIL at module level, and the input-fixture check, abort the whole run without a summary. | Mostly adequate |
| No silent skips or false passes | There are no skip paths. False passes are possible through weak oracles (§2). The CAD RGB branch sets opacity to 1.0 unconditionally. | Gap (oracle-level) |
| No dependence on stale files | FS and CAD now use temporary directories. The input fixture is read from `testing/evidence/phase_1d/`, run output reused as a fixture without a hash pin. The evidence directory is overwritten in place without a run ID. | Partly |
| Repository on `sys.path` | `REPO_SRC` is inserted at index 0, ahead of the gitignored `osdagbridge.egg-info` editable install. Correct, but not asserted. Recommend logging `osdagbridge.__file__`. | Adequate |

---

## 8. Repository integrity

| Check | Result |
|---|---|
| `HEAD` | `ref: refs/heads/dev` → `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` |
| Lock files | none in `.git/` |
| `.git/index` mtime | 2026-11-15 12:26:18 UTC. It predates all Phase 2 work, so no staging or checkout has happened since. |
| Source content | The aggregate of per-file SHA-256 values over all 282 non-ignored files under `src/` (CR-normalised) is `c6d61d03…a89d`. It is **identical** to a clean clone of `d74f56d`. Line-ending-only byte differences can't be ruled out by this method, but the index time and the tracked-DB hash give no sign of any. |
| Tracked database `Intg_osdag.sqlite` | SHA-256 `25f97857…ea91`, **byte-identical** to baseline |
| Untracked files | `src/osdagbridge.egg-info/` (6 files, gitignored) and `project_location/weather.sqlite` (180,224 B, mtime 05:48 UTC, before Phase 2, not changed by this run) |
| Source files newer than the previous audit | none |
| Workspace changes (not the repository) | the runner, `PROGRESS.md`, `DECISIONS.md` (DEC-010/011, recorded as "APPROVED" before this gate), `CHANGELOG.md`, the two reports and the evidence |

**Conclusion:** the application repository is at the frozen baseline and unmodified (CONFIRMED). All Phase 2 changes are workspace documentation and test assets.

---

## 9. Exact outstanding actions

1. **A02:** replace it. The oracle must use support reactions from the analysed combination against Σγᵢ × component reactions; SW, deck, DW (`wearing_course_load`), barrier and SIDL from the analysed model. Use a two-sided tolerance. Assert that SIDL and the barrier are present. Keep a separate SIDL-presence check that doesn't depend on the `sidl_combination` attribute.
2. **GEO-SLAB:** first record the transverse-member representation in `DECISIONS.md`: concrete material, or steel-transformed with E<sub>s</sub>/E<sub>cm</sub>; cracked or uncracked; J; per-metre basis under `unit_width=True`. Then assert A, I<sub>z</sub>, I<sub>y</sub> and J against that model within tolerance. Remove `Iz < 0.002`.
3. **FS:** test the production `_with_db` / `report_generator` paths with the package directory read-only or on a copy. Assert no new or changed files and unchanged tracked database hashes. Add the `desktop/__main__.py` `create_sqlite` path.
4. **D02 and C02:** use the real keys:
   - D02: `KEY_TL_HIGHEST_MAX_TEMP`, `KEY_TL_LOWEST_MIN_TEMP`, `KEY_TL_THERMAL_COEFF_RCC`.
   - C02: `KEY_LL_IRC_CLASS_FATIGUE`.
   - D02 also needs a decided thermal representation and a magnitude oracle traced to IRC 6 cl. 215.
   - C02 must assert axle loads and spacing from `cl_204_6_fatigue_load()`, plus a non-zero analysed response, plus use in the fatigue range.
5. **C01:** add a per-load-case path assertion (`designer.py:3082` → `KEY_UTIL_FATIGUE`) and an ospgrillage sign-convention companion test.
6. **B01:** replace the d<sub>w</sub>-equality assertion with D = d<sub>w</sub> + t<sub>f,top</sub> + t<sub>f,bot</sub>. Compare grillage properties with the designer's checked section for A, I<sub>z</sub>, I<sub>y</sub> and J. Record which dimension governs after snapping.
7. **MAT:** derive the expected load from the model's own areas and span, and call through `add_dead_loads()`.
8. **CAP:** compute the bound from the result's `A_wb_mm2` and the configuration's f<sub>y</sub>/γ<sub>m0</sub>. Add the positive cl. 8.7.3.1 web-strip oracle so that a clamp-only fix fails.
9. **RPT:** use the real Phase 1D output dictionary for the failing case and an all-passing dictionary for the mirror case. Assert semantically, not on one literal.
10. **CAD:** relabel it as environment verification. Optionally add an application-level check through `_export_cad_figures` with a non-background-pixel threshold.
11. **Sensitivity:** run the (a)/(b)/(c) protocol of §6 for all 14 tests and archive the results.
12. **Runner:**
    - Add strict expected-failure semantics, failing the run on any unexpected PASS or FAIL against a per-test expectation manifest.
    - Capture stdout and the exit code to a file.
    - Stamp each log with UTC time, duration, interpreter, key package versions, `osdagbridge.__file__` and the repository SHA.
    - Use per-run evidence subfolders.
    - Pin the input fixture's hash.
    - Record the superseded runner's hash for the `phase_2_baseline` evidence.
13. **Reports:** correct the A02 mechanism, the D01 P<sub>z</sub> (1,039.6 N/m²), the C02 vehicle definition, the GEO-SLAB assertion, the B01 "stale" wording and the "every test invokes application code" claim. Set DEC-010 and DEC-011 to pending until this gate is re-run.
14. **Phase 3 has not been started.** It should not start until items 1–12 are complete and a narrow re-audit confirms them.

---

## Verdict

**REJECT PHASE 2 REGRESSION SUITE**
