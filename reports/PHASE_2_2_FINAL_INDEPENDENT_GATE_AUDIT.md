# Phase 2.2 Final Independent Gate Audit: OsdagBridge Regression Suite

**Purpose:** decide whether Phase 2.2 resolves the objections in `reports/PHASE_2_1_FINAL_GATE_AUDIT.md`, and whether the suite can gate Phase 3 remediation.

**Frozen baseline:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (branch `dev`)

**Material examined:**
- `run_all_baseline_tests.py` (69,593 B, SHA-256 `26991c15…fbfd5`, modified 12:22:50 UTC) and `run_sensitivity_matrix.py` (35,504 B, `e4e6f30b…918d`, modified 12:50:12 UTC), both read in full.
- All logs and JSON files under `testing/evidence/phase_2_2/`.
- The three Phase 2.2 reports, DEC-013, DEC-014 and DEC-015.
- The application source and the vendored ospgrillage at the baseline.

**Independent execution.** I ran both harnesses unchanged on a clean baseline clone in a cloud reference environment: Linux, Python 3.12, pythonocc-core 8.0.1.2, openseespy 3.8.0.0, numpy 2.5.4, scipy 1.18.1 and xarray 2026.9.0, with Xvfb. I also ran two probe scripts of my own: genuine-fix candidates for A02 and an incomplete C01 fix. Nothing was run, edited, installed or committed on your machine, apart from saving this report.

**Labels:**
- Evidence: CONFIRMED / PLAUSIBLE / UNVERIFIED / CONTRADICTED.

---

## 1. Executive verdict

**Phase 2.2 made real progress:**
- **B01** now inspects the solver-side sections and an analysed deflection. A metadata-only swap fails, which was my Phase 2.1 objection.
- **CAP** uses two geometries, so a single hard-coded constant fails.
- **C02** now builds and analyses a real 40 t vehicle.
- **D02 and GEO-SLAB** are properly blocked and excluded from the sensitivity count.
- Fixture hashes now abort on mismatch.
- A remediation manifest exists.
- The application repository is untouched.

**But the claims that matter for authorisation don't hold:**
1. **A02 cannot be passed by a correct fix.** It has two problems:
   - **Its oracle includes a median load (96 kN) that doesn't exist in the model.** The fixture has `geometry.include_median = "No"` and median width 0.
   - **Its reaction check reads OpenSees's global state**, which holds the *last* analysed case (`SEISMIC_4: 1.0DL + 1.0DW`), not BASIC_1.

   The "correct" candidate passes only by injecting a median line load, re-ordering the load cases so BASIC_1 runs last, and monkeypatching `LineLoading.__eq__` so the barrier identity check succeeds.

   My genuine fix (factor fixes, SIDL built before DL, no injections) **FAILs**: the reaction reads 1,932.8 kN and the barrier identity is false. Adding the re-ordering still FAILs: 2,710.2 kN against 2,932.3 kN.
2. **Several "correct" candidates are output substitution, not implementations:**
   - **C01** hard-codes 62.729 MPa, chosen by load-case count.
   - **RPT** string-replaces "pass" with "fail" when the dictionary contains "1.9746" or "fail".
   - **CAP** overwrites the result with a copy of the test's own oracle formula, with b1 picked from a lookup keyed on d<sub>w</sub>.

   These prove nothing about the application.
3. **C01 still accepts a degenerate fatigue path (probe, CONFIRMED).** A correct envelope combined with a per-load-case path that always returns 0 MPa **PASSes**, because path (b) has no positive case.
4. **RPT lost its all-pass mirror scenario**, which existed in Phase 2.1. It also *requires* the other three summary lines to say "pass" without checking their actual results.
5. **FS still gates on a path-string check.** Its observed-write check is logged but not asserted. A packaged read-only database would fail.
6. **Execution integrity has regressed:**
   - The only baseline record (12:10:37) was produced by a **superseded runner** (hash `b817861e…`; the current one is `26991c15…`).
   - **The `baseline/` logs were overwritten by the sensitivity run** and now contain naive-candidate (c) results. For example, the CAD log says BASELINE_FAIL while the summary says PASS.
   - No stdout or stderr was captured for either run.
7. **The environment is misreported.** The reports list OCCT 7.9.0 and OpenSeesPy 3.7.0.1. Those are the old `osdagbridge-env` (Python 3.11) versions. The interpreter that actually ran, `osdagbridge-py312`, contains OCCT 8.0.1 and OpenSeesPy 3.8.0.0, unchanged since 04:55 UTC.

**"12/12 actionable sensitivity verified" is CONTRADICTED.**
- 5 tests are genuinely demonstrated: B01, D01, GEO-COUNT, MAT and CAD.
- 3 are demonstrated only within a limited scope: A01, C02 and FS.
- 4 are not demonstrated: A02, C01, RPT and CAP.

**Verdict: REJECT PHASE 2.2 REGRESSION SUITE.** §11 lists the remaining actions. Only the A02 oracle and extraction, C01 path (b), RPT, FS and evidence handling are blocking. The other tests are close to usable.

---

## 2. Environment and reproducibility

| Question | Finding | Status |
|---|---|---|
| Which environment ran Phase 2.2? | Both runs used `C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\python.exe` with Python 3.12.16, per the summary, every log and the module paths in `F:\FOSSEE internship\source\…`. | CONFIRMED |
| Its actual package versions | `conda-meta`: `occt-8.0.1`, `pythonocc-core-8.0.1.2`, `python-3.12.16`, `numpy-2.5.5`. `site-packages`: `openseespy-3.8.0.0` and `openseespywin-3.8.0.0`. | CONFIRMED |
| Was it changed? | `conda-meta/history` was last modified 04:55:41 UTC, before Phase 2. No `conda-meta` or `site-packages` entry changed after 05:00 UTC except `__pycache__`. | CONFIRMED: not changed |
| Source of "OCCT 7.9.0 / OpenSeesPy 3.7.0.1" | These exactly match `osdagbridge-env` (Python 3.11.18: `occt-7.9.0`, `pythonocc-core-7.9.0`, `openseespy-3.7.0.1`). The reports **mislabel** the py312 environment. The runner records `"openseespy": "installed"` and `"OCC": "installed"`, so no version was captured at run time. | **Misreported** |
| Same environment for baseline and sensitivity runs? | Yes: same interpreter path in both sets of artefacts. | CONFIRMED |
| Do the results reproduce in the reference environment? | **Yes.** The current runner in baseline mode gives 11 BASELINE_FAIL / 2 BLOCKED / 1 PASS and process exit 0. The figures are identical: A02 72,392.5 N and 1.16×10⁻⁷ N, reaction 1,736.55 kN; B01 7.816 mm; CAP 134,083.23 / 231,365.01 kN; MAT 169.82 kN. The only difference is the CAD pixel standard deviation (19.5 against 20.0). The sensitivity matrix gives 12/12 with the same statuses and exit 0. | CONFIRMED |
| Do the version differences matter? | None of the regression numbers depend on the OCCT version except the CAD environment check. Linux numpy 2.5.4 against Windows 2.5.5 produced no differences. | CONFIRMED (for this suite) |

---

## 3. Sensitivity verification, all 14 tests

Every condition was executed in-process, by monkeypatching classes in the imported modules. It was not pre-populated: I reproduced it independently. The frozen source files were not modified (§10).

| # | Test | (b) "correct" candidate: what was actually executed | Changes behaviour upstream of the assertion? | Assertion and oracle unchanged? | (c) naive candidate | Could an incomplete fix still pass? | Sensitivity status |
|---|---|---|---|---|---|---|---|
| 1 | A01 | `LoadCase.add_load` deep-copies the load and calls the stock `apply_load_factor` (only `load_point_1..4`) | Yes | Yes | scales by 1.15 → FAIL | **Yes.** (b) lacks the `LineLoading.line_end_point` and `PatchLoading` interpolation fixes that A02's (b) shows are needed (§4). | Limited: detects factor drop only |
| 2 | B01 | `_girder_section` returns **hard-coded** snapped constants; `_validate_inputs` rewrites `web_depth` | Yes: the solver is built from them | Yes | swaps `girder_props` after setup → **FAIL** (deflection 7.816 mm) | Low | **Demonstrated** (the candidate isn't general; the oracle is self-calibrated, §6) |
| 3 | C01 | wraps `_extract_demands…` and **overwrites** `stress_range_MPa` with 0.0 or **62.729**, chosen by `len(Loadcase)` | **No: injects the expected values** | Yes | zeroes the envelope only → FAIL | **Yes. My probe: a genuine envelope plus a per-LC path that always returns 0 PASSes.** | **NOT DEMONSTRATED** |
| 4 | A02 | (i) upstream fixes: `LineLoading.apply_load_factor` also scales `line_end_point`; `PatchLoading.apply_load_factor` rebuilds `patch_mag_interpolate`; `add_load` scales a copy. (ii) **replaces `add_dead_loads` wholesale** with hard-coded parameters. (iii) **injects a 4 kN/m median load**. (iv) **re-orders `load_case_list` so BASIC_1 runs last**. (v) **monkeypatches `LineLoading.__eq__`** to compare by name. | Partly. (ii) to (v) exist only to satisfy the test's oracle and extraction. | Effectively weakened by (iv) and (v) | builds an extra BASIC_1 without barrier → FAIL | n/a. **A genuine fix FAILs** (probe, §4). | **NOT DEMONSTRATED; test invalid as a gate** |
| 5 | D01 | reimplements `add_wind_loads` reading the 4 real UI keys | Yes | Yes | reads speed only → FAIL | No | **Demonstrated** |
| 6 | D02 | none, BLOCKED (DEC-015) | — | — | — | — | **BLOCKED / not counted** (correct) |
| 7 | C02 | wraps `add_live_loads`, adds a real ospgrillage `MovingLoad` with the vendored `FATIGUE` vehicle, analysed | Yes | Yes | mock object with no loads → FAIL | **Yes:** wrong transverse placement passes, and so does any case named "fatigue"/"204" with the right total. Fatigue utilisation is not checked (§5). | Limited: generation and response only |
| 8 | RPT | wraps `executive_summary` and **string-replaces** "Girder design pass" with "fail" when `str(output_dict)` contains "1.9746" or "fail" | **No: output post-processing** | Yes | rewords to "completed" → FAIL | **Yes.** A hard-coded "Girder design fail" passes, because no all-pass scenario exists. | **NOT DEMONSTRATED** |
| 9 | GEO-COUNT | `n_girders = _girder_count()` | Yes | Yes | `n_girders = 0` (trivial) | No | **Demonstrated** (weak naive case) |
| 10 | GEO-SLAB | none, BLOCKED (DEC-013) | — | — | — | — | **BLOCKED / not counted** (correct) |
| 11 | CAP | wraps `compute_bearing_stiffener` and **overwrites** `Fcdw_wb_kN` and `fcc_wb_MPa` with the test's own formula, `b1 = 101.81 if dw≈1304 else 100.0` | **No: copies the oracle; the result is tautological** | Yes | hard-coded 63.4 kN → FAIL on geometry 2 | A per-geometry lookup passes (the (b) candidate is one) | **NOT DEMONSTRATED** (the test itself is improved, §7) |
| 12 | MAT | swaps the analyser module constant to the input density during `add_dead_loads` | Yes | Yes | **identical to baseline** | No | **Demonstrated** (no distinct naive case) |
| 13 | FS | repoints `ui_loc.DB_PATH` and the `Database()` default to `%TEMP%\OsdagBridgeAppData` | Yes | Yes | anchors `DB_PATH` only → FAIL (cwd default) | **Yes,** any path without "osdagbridge"/"core"/"src" in its name. A *correct* packaged read-only database fails (§8). | Limited: string-based |
| 14 | CAD | identical to baseline | n/a | Yes | uniform grey PNG → FAIL | n/a | **Demonstrated** (environment check) |

**Evidence capture:**
- Neither harness captured stdout, stderr or the operating-system exit status. `sensitivity_exit_code.txt` and `baseline_exit_code.txt` are written by the scripts themselves just before `sys.exit`.
- In my reproduction the actual process exit statuses were 0 and 0, matching those files.

---

## 4. A02 numerical audit

**Production path (CONFIRMED):**
- `add_dead_loads()` creates SW, deck, wearing course (`wearing_course_load`), footpath (none in this layout) and crash barrier (`crash_barrier_load_case`).
- `_DL_ATTRS` = SW, deck, footpath and `sidl_combination` (`analyser.py:1532–1537`). `create_sidl_combination()` groups barrier, railing and median, and is never called.
- `create_uls_combinations()` builds `BASIC_1: 1.35DL + 1.75DW` via `_copy_loads` → `add_load(load_factor=…)` (`analyser.py:2344–2349`).
- `model.analyze()` solves all 18 cases **in sequence**. The last one is `SEISMIC_4: 1.0DL + 1.0DW`.

**Independent resultants, from the load definitions:**

| Component | Resultant |
|---|---|
| Self-weight | 169.82 kN |
| Deck | 1,275.00 kN |
| Wearing course (DW) | 244.80 kN |
| Crash barrier | 313.92 kN (2 × 6.54 kN/m × 24 m) |
| Median | **none.** Fixture: `include_median = "No"`, width 0.0. No `median_load_case` exists. |

Correct BASIC_1, assuming 1.35 for SIDL (to be confirmed against IRC 6 Annex B): 1.35 × (169.82 + 1,275.00 + 313.92) + 1.75 × 244.80 = **2,802.7 kN**.

The test's target of **2,932.30 kN** adds 1.35 × 96 kN of non-existent median. CONTRADICTED.

**Reaction extraction is invalid:** `ops.reactions(); Σ nodeReaction(node, 2)` reads the OpenSees domain left by the last analysed case.
- On the baseline that value is 1,736.55 kN. My probe confirms it equals the global state after `SEISMIC_4`, not BASIC_1.
- The log label "Total Support Vertical Reaction in BASIC_1" is wrong.
- The (b) candidate's docstring admits it re-orders the cases "so OpenSees final reaction state reflects BASIC_1".

**Internal forces (valid):**
- `get_results(load_case="BASIC_1: …")` is case-specific.
- Vy_i and Mz_i of BASIC_1 against 1.35·"1.0 DL" + 1.75·"1.0 DW" detect the factor drop: an error of 1.16×10⁻⁷ N against the unfactored sum, and 72,392.5 N against the factored sum.
- In my genuine-fix probe this force check passed. It is the sound part of the test.

**Barrier check:** object identity (`load_obj in barrier_loads`) fails for any fix that scales *copies* of the loads, which is the only way to scale without mutating the source cases. The (b) candidate passes only by redefining `LineLoading.__eq__`.

**Probe results (CONFIRMED):**

| Candidate | Result | Reason given |
|---|---|---|
| Genuine: upstream line/patch factor fixes, copy scaling, SIDL created before the DL combination; no re-ordering, median or `__eq__` patch | **BASELINE_FAIL** | "Total reaction 1932.8 kN does not match 2932.3 kN; Crash barrier load omitted". The force check passed. |
| Same, plus BASIC_1 moved last | **BASELINE_FAIL** | reaction 2,710.2 kN against 2,932.3 kN |

The 92.5 kN gap between 2,710.2 and 2,802.7 kN is unexplained. It may be a load type still unscaled, or the SIDL factor. That makes the completeness of factor propagation itself UNVERIFIED.

**Can it reject an incomplete fix?**
- The force identity rejects ignored factors.
- But the test as a whole also rejects a correct fix, so it **cannot serve as a remediation gate**.

**Upstream fixes in A02's (b) (CONFIRMED as real mechanisms):**
- `LineLoading.line_end_point` is a separately stored copy of the end vertex (`load.py:657, 667`), not updated by `apply_load_factor` (`load.py:435–470`).
- `PatchLoading.patch_mag_interpolate` is built once in `_define_patch_edge_lines` (`:918, 1003`).
- PyPI ospgrillage 0.6.0 has the same structure, so the defect originates upstream.
- The vendored copy in `src/ospgrillage` is an OsdagBridge-modified fork: it adds `CLASSA`, `CLASS70R` and `FATIGUE` vehicles that PyPI lacks. **A01 / DEF-01 is therefore upstream-originated, but present in OsdagBridge-owned vendored code.** A fix belongs in the vendored copy and should also be reported upstream.

---

## 5. C02 fatigue vehicle audit

**The vehicle (CONFIRMED, vendored `load.py` `create_fatigue_vehicle`):**
- Axle loads are 12 / 14 / 14 t × 9.81 = 117.72 / 137.34 / 137.34 kN. These are **axle forces**, each split into **two wheels** (`p = axle/2`), so 58.86 / 68.67 / 68.67 kN per wheel.
- The total is 392.4 kN = 40 t.
- Axle spacing is 4.5 m and 1.4 m. The wheel track is ±0.84 m (1.68 m).
- The application's own `IRC6_2017.cl_204_6_fatigue_load` lists the same axle values under the name `wheel_loads`. That name is misleading but the function is unused.

**Moving-load generation:** the (b) candidate creates a path from x = −25 m to L + 25 m **at z = 0.0**. The deck spans z = 0 to 8.5 m (mesh coordinates), so one wheel line sits at **z = −0.84 m, outside the deck**, and the other near the edge. The test sums the weight from the *load objects* (392.4 kN), not the load actually applied to the mesh, so this placement passes. Transverse placement and lane position are not checked.

**Inclusion in the analysis:** yes. `model.analyze()` runs the moving case, and `get_results(load_case=mc.name)` returns a force above 10 N. CONFIRMED by reproduction.

**Connection to fatigue demand and utilisation: none.** The test never checks:
- that the fatigue stress range (C01 path) or `KEY_UTIL_FATIGUE` is derived from this case;
- that the production toggle `KEY_LL_IRC_CLASS_FATIGUE` (set True in the test) actually causes generation. The candidate adds the case unconditionally.

**Classification:** the scope is *fatigue-vehicle generation and solver response*. As a test of fatigue-analysis participation it is **INCOMPLETE**. Case selection is still by name ("fatigue"/"204").

---

## 6. B01 and C01 verification

### B01

**What it does (CONFIRMED):**
- It inspects `grillage_model.girder_sections[i]`, the objects passed to `og.create_member` during setup.
- It runs a 100 kN point load at x = 12 m, z = 1.05 m (a girder line) on the application's own grillage model and boundary conditions.

**Results:**
- Baseline: **7.816 mm**, reproduced.
- The (b) candidate, which feeds snapped constants into `_girder_section` *before* setup, passes the 3% tolerance around 7.218 mm.
- The metadata-only (c) candidate stays at 7.816 mm and FAILs. That resolves my Phase 2.1 objection.

**Is the oracle independent?** Not fully. 7.218 mm is not derived; it matches the output of the candidate model.
- The ratio 7.816 / 7.218 = 1.083 agrees with I<sub>z</sub> 0.00792758 / 0.00734091 = 1.080 to within 0.3%. That is consistent with a stiffness change dominated by I<sub>z</sub>. PLAUSIBLE.
- The candidate's I<sub>y</sub>, J, A<sub>y</sub> and A<sub>z</sub> are invented, and its comment says b<sub>f</sub> = 450 mm while the section has 410 mm. These barely affect vertical deflection.
- **Recommendation:** derive the target from the application's own section routine applied to the snapped plates, or bound it with a hand calculation.

**DEC-014** (D governs) is applied consistently. Its premise still describes user inputs as "preliminary sizing".

### C01

**What it exercises:** the real `_extract_demands_from_analysis_results`, both paths. Only `classify_loadcases` and `build_girders` are mocked.
- The baseline static case (±1000 kNm at the shared node) gives path (a) 125.46 MPa and path (b) 62.73 MPa; the expected value is 0.
- The positive cyclic case (500 → 1500 kNm) expects ΔM/Z<sub>e</sub> = 1,000 kNm / 15.94×10⁶ mm³ = 62.73 MPa. That arithmetic is CONFIRMED.

**The sign companion** (OpenSees 2D `eleForce`: +12,500 / −12,500 N·m) is now asserted. It is still not an ospgrillage 3D local-force result. PLAUSIBLE.

**Fixing one path but not the other:**
- Fixing only path (a) FAILs. That is the (c) candidate.
- **Fixing path (a) and making path (b) a degenerate zero PASSes** (my probe, CONFIRMED). The positive cyclic case is asserted for path (a) only.
- Path (b) feeds `per_girder[g]["per_lc"]` DCRs and the per-selection `KEY_UTIL_FATIGUE` (Phase 2.1 audit §4.4). A zeroed path (b) would report 0% fatigue utilisation and pass.

**Required:** a positive case on path (b) as well. Specify what a single-case "range" means; for example, a live-only fatigue-vehicle case gives Δσ = M<sub>LL</sub>/Z<sub>e</sub>.

---

## 7. CAP independent calculation

**Formula structure** (as cited: IS 800 cl. 7.1.2.1 with the cl. 8.7.3.1 web-strip treatment; clause text not available to me, so the wording is UNVERIFIED):
- A<sub>wb</sub> = (b1 + n1)·t<sub>w</sub>, with n1 = d/2;
- KL = 0.7d;
- r = t<sub>w</sub>/√12;
- λ = KL/r, f<sub>cr</sub> = π²E/λ², λ̄ = √(f<sub>y</sub>/f<sub>cr</sub>);
- curve c (α = 0.49);
- φ = 0.5[1 + α(λ̄ − 0.2) + λ̄²], χ = 1/(φ + √(φ² − λ̄²));
- f<sub>cd</sub> = χ·f<sub>y</sub>/γ<sub>m0</sub>;
- P = f<sub>cd</sub>·A<sub>wb</sub>/1000 (kN).

**Reproduction:**

| Quantity | Geometry 1 | Geometry 2 |
|---|---|---|
| t<sub>w</sub> / d | 8 / 1,304 mm | 10 / 1,000 mm |
| b1 | 101.81 mm | 100.0 mm |
| A<sub>wb</sub> | 6,030.5 mm² | 6,000 mm² |
| λ | 395.25 | 242.49 |
| f<sub>cr</sub> | 12.64 MPa | 33.57 MPa |
| λ̄ | 5.263 | 3.229 |
| χ | 0.0330 | 0.0830 |
| f<sub>cd</sub> | 10.51 MPa | 26.42 MPa |
| **P** | **63.40 kN** | **158.50 kN** |

Units are consistent. Both values are CONFIRMED. The "158.6 kN" in the brief and the "158.59" in the candidate docstring are rounding variants; the log value is 158.50.

**Material inputs:** f<sub>y</sub> = 350 MPa, γ<sub>m0</sub> = 1.10, E = 200,000 MPa.

**Rejection behaviour:**
- **A single hard-coded value is rejected (CONFIRMED).** 63.4 kN fails geometry 2.
- **A yield-only clamp is rejected:** 1,918.8 / 1,909.1 kN against oracles of 63.4 / 158.5 kN, and f<sub>cc</sub> against f<sub>y</sub>/γ<sub>m0</sub>.
- **Not rejected:** a per-geometry lookup. The (b) candidate is exactly that.

**Remaining issues:**
- The test assumes b1 = 100 mm for geometry 2, but the application computes b1 itself from bearing inputs that the test doesn't change. On the baseline the application gives 101.81 mm. The effect is about 0.3%, well inside the tolerance, but the oracle should read b1 from the application's inputs or be documented.
- The ±15% tolerance does not discriminate between buckling curves a, b, c and d (stated in the test, as I recommended).
- The (b) candidate is a copy of the oracle and demonstrates nothing about the application.

**Test validity:** VALID WITH CORRECTIONS. **Sensitivity:** not demonstrated by the current (b).

---

## 8. FS production-path verification

**Production path (CONFIRMED):**
1. `ui_fields_project_location.DB_PATH` = `<package>/core/data/project_location/weather.sqlite`.
2. `_with_db` → `Database(DB_PATH).connect()`. The same path is used by `report_generator.py:664–666` and `project_location.py:932`.
3. `connect()` calls `sqlite3.connect` (creating the file if absent). It runs `schema.sql`, populating stations, **when the file was missing or the `stations` table is absent** (`database.py:19–30`).

So production creates the database inside the package tree, and rebuilds it if `stations` is missing. The workspace copy (180,224 B, mtime 05:48 UTC) is unchanged by Phase 2.2.

**What the test asserts:**
- **The status is decided by** `is_inside_package` (a path-string test) **and** `created_in_cwd` (the default constructor).
- **The "observed side effect" check is not part of the status.** It calls `Database(mock_path).connect()` directly, without the production `_with_db` path, and only logs `wrote_in_package_dir`.

**Packaged read-only database:** **rejected.** A path under the package fails the string test even when nothing is written. A correct design therefore fails.

**Runtime writes:** not detected through the production path. Nothing is snapshotted or hashed.

**Classification:** filesystem, packaging and reproducibility. The test is **INVALID as a gate**; this finding is unchanged from Phase 2.1.

---

## 9. Blocker assessment

| Item | Finding |
|---|---|
| **D02 / DEC-015** | DEC-015 is "APPROVED (FORMAL BLOCKER)". It records that IRC 6 cl. 215 effective-temperature and gradient effects need an equivalent-load or thermal-element formulation the project hasn't specified. The test returns BLOCKED unconditionally. The matrix records (b) and (c) as BLOCKED with `sensitivity_verified = false`, excluded from the actionable count. **No hypothetical candidate is counted.** CONFIRMED. |
| **GEO-SLAB / DEC-013** | Still "APPROVED (FORMAL BLOCKER)", unresolved. The Phase 2.1 substitute assertion and the "Matches DEC-013" wording are gone from the harness. The log only *describes* the candidate representations. **No transformed model is treated as accepted.** CONFIRMED. |
| **Ratification** | DEC-013, DEC-014 and DEC-015 are all decided by the testing workstream itself. D-governs (DEC-014) and both blockers still need sign-off from the developers or an engineering authority. |
| **Effect on the gate** | The remediation manifest expects both blocked tests to stay BLOCKED, so `--mode remediation` can now exit 0. That resolves my Phase 2.1 point. |

---

## 10. Baseline and repository integrity

| Check | Result |
|---|---|
| Commit and branch | `.git/HEAD` → `refs/heads/dev` → `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`. No lock files. `.git/index` mtime 2026-11-15 12:26:18 UTC, unchanged since before Phase 2. |
| Clean repository | The aggregate SHA-256 of all 282 non-ignored files under `src/` (CR-normalised) is `c6d61d03…a89d`, identical to a clean `d74f56d` clone and to my two previous audits. `Intg_osdag.sqlite`: `25f97857…ea91`, byte-identical. No source file changed after 11:00 UTC. |
| Fixture hashes | `input_configuration.json` = `31ae62dc…0191` and `output_dictionary_snapshot.json` = `429a3198…a5ab`, equal to the runner's pins. A mismatch now **aborts**. **`testing/fixtures/` still does not exist**; the fixtures remain in `testing/evidence/phase_1d/`. |
| Baseline run | `phase_2_2_baseline_summary.json` (12:10:37) was produced by runner `b817861e…`. **The current runner (`26991c15…`, edited 12:22:50) was never recorded in baseline mode.** My run of the current runner reproduces the same statuses and figures, so the edit didn't change baseline outcomes, but your evidence does not show this. |
| Baseline logs | **All 14 `baseline/*.log` files are timestamped 12:50:30–12:52:21, written during the sensitivity run**, because the test functions write into `phase_2_2/baseline/`. For actionable tests the last write was condition (c):<br>• A01 log: ratio 1.15000<br>• C01 log: envelope 0.000 MPa<br>• CAP log: geometry-1 capacity 63.40 kN<br>• **CAD log: `BASELINE_FAIL`, blank image**, while the summary says PASS<br>I reproduced this overwrite. **The logs do not agree with the summary JSON.** |
| Run commands | Not recorded. The reports name `--mode baseline`; the sensitivity command is implied. |
| Process exit status | Not captured. The self-written files say baseline 0 (manifest alignment) and sensitivity 0. My reproduction gave exit 0 for both. **Baseline exit 0 means "11 defects reproduced as expected", not that the application passes.** The reports state this correctly. |
| stdout / stderr | Not captured for either run. |
| Completion before reports | Sensitivity summary 12:52:21; reports 12:54–12:55. CONFIRMED. |
| Workspace changes | The two harness scripts, `phase_2_2/` evidence, three reports, `CHANGELOG.md`, `DECISIONS.md` and `PROGRESS.md`. `reports/PHASE_2_1_FINAL_GATE_AUDIT.md` (11:52:50) is my previous deliverable, byte-identical to what I wrote. |

**Conclusion:** the application repository is at the frozen baseline and unmodified (CONFIRMED). The evidence set, however, mixes a superseded-runner summary with candidate-overwritten logs.

---

## 11. Exact remaining actions

1. **A02:**
   - Remove the median term; the expected value is 2,802.7 kN if the SIDL factor 1.35 is confirmed against IRC 6 Annex B.
   - Obtain the BASIC_1 reaction case-specifically, by analysing BASIC_1 alone or summing the reactions from its `get_results`. Do not read the global OpenSees state.
   - Replace the object-identity barrier check with a resultant or force check: for example, BASIC_1 minus the factored DL+DW forces should equal 1.35 × the barrier case.
   - Re-run sensitivity with a candidate that changes only production code paths: no load-case re-ordering, no `__eq__` patch, no injected loads. Investigate the 92.5 kN residual.
2. **A01:** add a line load whose `line_end_point` matters and a patch load, so that A01's own correct candidate must include the line and patch fixes.
3. **C01:** add a positive case for path (b), defining a per-load-case range explicitly. Replace the output-injecting (b) candidate with a real reimplementation of the range logic.
4. **C02:**
   - Assert the transverse placement within the carriageway (both wheel lines on the deck) and the applied load (vertical reaction equal to the vehicle weight at one position).
   - Assert that the production toggle drives generation.
   - Link the case to the fatigue range or `KEY_UTIL_FATIGUE`, or formally limit the test's stated scope.
5. **RPT:**
   - Restore the all-pass mirror scenario.
   - Derive the expected status of each component line from the dictionary's actual results, instead of requiring "pass".
   - Replace the string-replace (b) candidate with a status-derived implementation.
6. **CAP:** take b1 from the application's inputs for each geometry. Replace the (b) candidate with a change to `compute_bearing_stiffener`'s formula rather than a post-hoc overwrite. Optionally add a third geometry not hinted at in the code.
7. **FS:** base the status on an observed effect through the production path (`_with_db` calls against a copied or read-only package directory, with before/after listings and hashes). Accept a pre-built read-only database. Keep the default-constructor check as a separate assertion.
8. **B01:** derive the 7.218 mm target from the application's section routine on snapped plates, or a hand bound, instead of the candidate model's output. Correct the candidate's invented section constants.
9. **Evidence:**
   - Write sensitivity-run test logs to the sensitivity folder only.
   - Re-run the *current* runner in baseline mode afterwards.
   - Capture stdout, stderr, the actual process exit status and the exact command line for both runs.
   - Record real versions (`OCC.VERSION`, `openseespy` metadata).
   - Create `testing/fixtures/` or stop referring to it.
10. **Reports:** correct the environment line to OCCT 8.0.1 / pythonocc-core 8.0.1.2 / OpenSeesPy 3.8.0.0, the A02 target and median claim, and the "12/12" claim (per §3). Disclose that the logs were overwritten.
11. **Governance:** obtain developer or engineering ratification of DEC-013, DEC-014 and DEC-015, and of the SIDL factor used in A02.
12. **Phase 3** has not been started and should not start until items 1–9 are complete and re-audited. The re-audit can be limited to A01, A02, C01, C02, RPT, CAP, FS, B01's oracle and evidence handling.

---

## Verdict

**REJECT PHASE 2.2 REGRESSION SUITE**
