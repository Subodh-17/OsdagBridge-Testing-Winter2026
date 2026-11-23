# PHASE 3 — Revision 2.0 Independent Re-Audit

**Auditor:** Claude (independent adversarial auditor)
**Date:** 2026-11-18. Inspection ran from about 09:55 to 11:20 UTC, measured on the device clock. The final preservation check was at 11:19:44 UTC.
**Baseline audited against:** `source/OsdagBridge`, branch `dev`, commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`. The frozen sealed evidence is the Phase 2.12, 2.13 and 2.17 runs.
**Controlling prior audit:** `reports/phase_3/CLAUDE_INDEPENDENT_PHASE_3_PLANNING_AUDIT.md`, sha256 `088b10fe…`. That file is unchanged and this report does not supersede its text.
**Mode:** read-only. I changed no source, tests, database, environment, ledger, seal or Phase 2 file. I made no commits and switched no branches. The only file written to the workspace is this report.

All numerical probes ran in a disposable cloud sandbox. It holds a pristine clone of `d74f56dd` at `/tmp/src3` and uses Python 3.12.16, openseespy and the vendored `ospgrillage`. Any monkeypatching was done in memory in that sandbox only. Nothing was run on the device that could mutate state.

## Documents audited

| Document | sha256 (prefix) |
|---|---|
| PHASE_3_CLAUDE_FINDING_RESOLUTION_MATRIX.md | `52ba00c9eb015135` |
| PHASE_3_BASELINE_PRESERVATION_REPORT_REV2.md | `6500f74a1e59b0ba` |
| PHASE_3_DEFECT_TRACEABILITY_MATRIX_REV2.md | `e22073a903ee17a5` |
| PHASE_3_DEPENDENCY_AND_PRIORITY_ANALYSIS_REV2.md | `a0de7aafd8a05d9a` |
| PHASE_3_TEST_ACCEPTANCE_CRITERIA_REV2.md | `95fcb063c53c518e` |
| PHASE_3_IMPLEMENTATION_BATCH_PLAN_REV2.md | `e61d7232fbe1a32f` |
| PHASE_3_ENGINEERING_REMEDIATION_BLUEPRINT_REV2.md | `e193a9241e9942ab` |

---

## 0. Verdict

# REJECTED — MATERIAL ENGINEERING ERRORS

Revision 2 is a substantial improvement on Revision 1:

- Seven of the headline numbers now re-derive correctly: DEF-03, DEF-05, DEF-12 (final value), DEF-17, DEF-02, DEF-13 and the DEF-18 fixture total.
- The preservation report is accurate in substance.
- The batch plan's rollback and commit discipline is now sound.

However, several acceptance oracles that would govern implementation are still wrong, and they fail in both directions:

- **Some oracles would reject a correct implementation:**
  - BASIC_1 = 2788.751 kN is an arithmetic error. The document's own inputs give 2818.242 kN.
  - The DW 216 kN, total 2023.586 kN and BASIC_1 oracles assume a 7.5 m wearing-course width. Production uses 8.5 m, and no defect or fix is registered for the difference.
  - The "unified fixture" uses girder A = 0.0324 m². The sealed bridge's snapped girder is A = 0.025192 m².
- **Some oracles would accept a defective implementation:**
  - The DEF-19 oracle is a one-sided "≥ 1.725 × nominal" bound.
  - The DEF-19 DLA value (1.15) and lane factors (1.0/1.0/0.9) match neither the code nor the formula the report prints.
  - The "+1 N" absolute floor passes the original DEF-18 defect at small load magnitudes. I demonstrated this.
- **The planned fix misses the cause:** DEF-18 fix #2 targets a code line that never fires. The real end-bay mechanism is unaddressed.

These are engineering errors in the acceptance criteria, not editorial slips. Under the governing rule (oracles must be independently correct), they block acceptance.

The required corrections are bounded and are listed in §11. Implementation remains **unauthorized**. Only the user can authorize it, and this audit does not.

---

## 1. Finding-by-finding reconciliation

I did not take the resolution matrix's "RESOLVED" status as evidence. Each row below was re-checked against source code, sealed logs or an independent calculation.

| Finding | Rev 2 claim | Re-audit classification | Basis |
|---|---|---|---|
| F-PRES-01 (fe82935a UUID) | Corrected to `fe82935a-0927-443a-b7be-aa730468d388` | **Corrected accurately** | Manifest `d0e791ef…` on disk |
| F-PRES-02 (OS edition) | Windows 11 Home Single Language | **Corrected accurately** | Manifest `os_caption` |
| F-PRES-03 (package versions) | OpenSeesPy 3.8.0.0 / pythonocc-core 8.0.1.2 | **Not verifiable** | No version fields for these packages in the sealed manifests; the cited conda-meta source was not provided as evidence |
| F-PRES-04 (Phase 2.15 loss) | Disclosed | **Partially corrected** | The disclosure is present, but it cites `reports/PHASE_2_16_FINAL_INDEPENDENT_GATE_AUDIT.md`, which does not exist. The real file is `PHASE_2_16_FINAL_INDEPENDENT_AUDIT.md`, and it records the event as the "C1 overwrite of Phase 2.15 evidence". |
| F-PRES-05 (exit-1 cause) | PowerShell multiline SyntaxError | **Not verifiable** | No transcript of the failing command is preserved |
| F-PRES (general) "282 python files" | — | **Partially corrected** | 282 is the count of *all* files in `src/` (aggregate `7c929481…`). There are 205 `.py` files. |
| F-DEF01 (factor ignored) | Fix spec + negative test | **Partially corrected** | The fix spec is sound. The negative test is nonsense: hard-coding 1.15× gives R = 1.15, not "1.09174". |
| F-DEF02 (barrier/SIDL) | 313.92 / 423.79 / −708.74 | **Corrected accurately**, but the gate tolerance is inconsistent | §2.5; the gate uses ±0.05% while the invariants require 10⁻⁶ |
| F-DEF03 (section sync) | A 0.0324, Iz 0.0097174 | **Corrected accurately** for the hand fixture | §2.2. Batch 5 applies the hand-fixture numbers to the sealed bridge; see F-FIX below. |
| F-DEF05 (wind) | 1039.6 N/m² | **Corrected accurately** | §2.3 |
| F-DEF07 (fatigue sign) | ±1000 sign-reversal control | **Corrected** (not re-derived in depth) | — |
| F-DEF08, F-DEF11 | Batch 1 | **Partially corrected** | `executive_summary.py` exists. `BridgeConfig` is in `designer.py:251`, so Commit 1.3's file list is consistent. No numeric oracle needed. |
| F-DEF10 (DB writes) | `mode=ro` + prebuilt package data | **Partially corrected** | §5 |
| F-DEF12 (stiffener buckling) | 118.79 kN; "3,380×" | **Partially corrected** | The final value is correct. The intermediate φ is wrong (7.1141; the correct value is 7.6130). The 3,380× ratio mixes geometries, and the safety consequence is overstated. See §2.1 and §7. |
| F-DEF13 (densities) | 217.728 kN | **Corrected arithmetically**, still uses the wrong girder | Correct only for A = 0.0324 |
| F-DEF17 (fatigue vehicle) | 1996.42 kNm | **Corrected accurately** | §2.4 |
| F-DEF18-01 (end-bay drop) | Caused by `if "ends" not in points.keys(): continue` | **Still incorrect** | §3.2. That branch never executes. |
| F-DEF18-02 (line magnitude / interpolation) | W·L; z index | **Corrected accurately** | §3.1, §3.3 |
| F-DEF18-03 (unified fixture) | 2023.586 kN | **Still incorrect** | The geometry is mixed, and DW 7.5 m differs from production's 8.5 m (§2.6) |
| F-DEF18-04 (patch inflation) | "exact numerical cell-integration" | **Partially corrected** | The cause is not identified and no algorithm is given (§3.4) |
| F-DEF19 (new: lane/DLA) | Registered; oracle 1.725α | **Still incorrect** | §4 |
| F-INV-01..05 (invariants / tolerance) | 10⁻⁶·ΣP + 1 N, etc. | **Partially corrected** | §6. The +1 N floor masks the defect. |
| F-DAG-01..03 | DEC items moved off the critical path | **Corrected**, with one ordering gap | DD oracle 1249.5 (ρ = 24.5) is asserted in Batch 2, but density propagation (DEF-13) lands in Batch 5 (§8) |
| F-BATCH-01..03 | Branch, atomic commits, `git revert` | **Corrected accurately** | §8 |
| F-HARNESS-01 | `ACTIVE_PHASE="phase_3"` prerequisite | **Corrected** (as a future prerequisite) | Not executed; correctly listed as a gated task |

---

## 2. Numerical re-derivations

All values are SI. E = 200,000 MPa. γ_m0 = 1.10 (IS 800:2007).

### 2.1 DEF-12 — bearing-stiffener web buckling (IS 800 Cl. 8.7.3.1 / 7.1.2.1, buckling curve c, α = 0.49)

Hand fixture: tw = 10 mm, d = 1300 mm, b1 = 100 mm, fy = 250 MPa.

| Step | Value |
|---|---|
| r = tw/√12 | 2.8868 mm |
| KL = 0.7d | 910 mm |
| KL/r | 315.23 |
| f_cc = π²E/(KL/r)² | 19.864 MPa (Rev 2: 19.860, a rounding difference) |
| λ̄ = √(fy/f_cc) | 3.5476 |
| φ = 0.5[1 + α(λ̄ − 0.2) + λ̄²] | **7.6130** (Rev 2 prints **7.1141**, which is wrong) |
| χ = 1/(φ + √(φ² − λ̄²)) | 0.069692 (consistent with φ = 7.6130; φ = 7.1141 would give 0.0753) |
| f_cd = χ·fy/γ_m0 | 15.839 MPa |
| A_eff = (b1 + d/2)·tw | 7500 mm² |
| **F_cdw** | **118.79 kN** ✔ |

Sealed geometry 1 (tw 8, d 1304, b1 101.81, fy 350): KL/r 395.25, λ̄ 5.2631, φ 15.591, χ 0.033040, f_cd 10.513 MPa, A 6030.5 mm² → **63.40 kN**. This matches the sealed oracle.

### 2.2 DEF-03 — hand-fixture section

Plates: web 1300×10, top flange 400×16, bottom flange 500×26, D = 1342 mm.

- A = 0.0324 m²
- ȳ = 0.539957 m from the bottom
- Iz = 0.0097174 m⁴
- Iy = 0.0003563 m⁴

All confirmed.

The single-beam deflection of 14.819 mm uses the fixture's own load. I did not re-derive it independently beyond the Iz input.

### 2.3 DEF-05 — wind pressure

P_z = 512.5 × (47/33)² = **1039.589 N/m²** ✔. Here 512.5 N/m² is the IRC 6 Table 12 hourly-pressure base for 33 m/s at the stated height and terrain; the result scales with V².

### 2.4 DEF-17 — IRC 6 Cl. 204.6 fatigue vehicle

Axles 117.72 / 137.34 / 137.34 kN at 0 / 4.5 / 5.9 m, on a 24 m simply supported span.

The critical axle (the second) sits at x = 12.43 m:

- R_L = Σ P_i(24 − x_i)/24 = 203.231 kN
- M = R_L·12.43 − 117.72·4.5 = **1996.415 kNm** ✔

### 2.5 DEF-02 — barrier SIDL (sealed geometry)

- CB = 2 × 156.96 kN = **313.92 kN** ✔
- Factored value 1.35 × 313.92 = **423.79 kN** ✔
- Sealed shortfall: 1736.55 − [1.35(169.819 + 1314.375) + 1.75·252.36] = **−708.74 kN** ✔

All three use the sealed production inputs consistently.

### 2.6 DEF-18 / BASIC_1 "unified fixture" — two material errors

| Term | Rev 2 | Re-derived | Issue |
|---|---|---|---|
| SW = 4·24·A·ρ_s | 244.166 (A = 0.0324, ρ = 78.5) | 244.166 | Arithmetic is correct, but A = 0.0324 is the DEF-03 hand-fixture girder. The sealed bridge's snapped girder (sealed B01 log) is **A = 0.025192**, which gives SW = 189.847 kN (ρ 78.5) or 169.290 kN (ρ 70). No mechanism is specified that would make the fixture build A = 0.0324 plates. |
| DD | 1249.5 (ρ_c = 24.5) | 1249.5 | Requires DEF-13 density propagation. Production default ρ = 25 gives 1275 kN (sealed FE 1314.375 = 1275 × 1.0309). |
| DW | 216.0 (7.5 m × 24 × 1.2) | — | **Production applies DW over the full 8.5 m deck.** The call `plategirderbridge.py:1334` → `create_wearing_course_load(..., edge_clearance=0.0)` → `load_placement.py:133 overlay_load` spans 0..bridge.width, giving 244.8 kN. The sealed EQ log line 17 states it directly: "Expected 216.000 … Applied 244.800". Rev 2 registers no defect and no fix for this, so a correct DEF-18 fix still fails the 216 / 2023.586 oracles. |
| CB | 313.92 | 313.92 | ✔ |
| Total | 2023.586 | 2023.586 | Internally consistent; inherits both issues above |
| **BASIC_1** = 1.35(SW + DD + CB) + 1.75·DW | **2788.751** | **1.35 × 1807.586 + 378.0 = 2818.242 kN** | **Arithmetic error of −29.49 kN (−1.05%).** It falls outside Rev 2's own ±0.05% gate, so a correct implementation would fail Batch 4. Back-solving 2788.751 needs SW = 222.32 kN, which matches no stated density or area. |

Results under the other assumptions:

- With production DW (8.5 m): BASIC_1 = 2868.642 kN.
- With the sealed snapped girder, ρ_s 78.5 and DW 7.5 m: BASIC_1 = 2744.910 kN.

The fixture has to pick one geometry and state it.

Historical note: Rev 2 says the sealed oracle "used preliminary SW 165.28". The sealed A02 log does show SW = 165.28 kN as an input (line 21). But preliminary SW is 169.8 kN (sealed EQ log). 165.28 kN corresponds to A = 0.021932, so the label "preliminary" is wrong.

### 2.7 DEF-19 — lane and DLA factors

See §4. None of the three candidate impact values agree with Rev 2's oracle:

| Source | Formula | Impact at L = 24 m |
|---|---|---|
| Rev 2 oracle | 4.5/(6 + L), the RCC formula | 0.15 |
| Report chapter 3 (`chap3.py`, Class A) | 9/(13.5 + L), the steel formula | 0.24 |
| Analysis code (`cl_208_3_impact_factor`) | Class 70R branch | 0.10 |

---

## 3. DEF-18 — the four corrections

### 3.1 Line magnitude / segment length

**Correct.** Assigning W·L per segment, together with the corrected centroid and index fixes, reproduces the exact resultant (prototype below).

### 3.2 First end bay — the Rev 2 mechanism is wrong

Rev 2 attributes the drop to `osp_grillage.py:1676`, `if "ends" not in points.keys(): continue`. Instrumentation showed all 16 grid entries carry an `"ends"` key, so **that `continue` never fires**.

The real mechanism is as follows:

1. The equivalent point is placed with `get_point_given_distance(xbar, point_coordinate=p2)`. This always offsets from p2 in −x.
2. In the first bay, the "trans, edge" branch yields p1 = 1.5 and p2 = 0, so the point lands at x = −0.75 m, outside the mesh.
3. `_assign_load_to_four_node` finds no grid and **silently returns `[]`** (`if grid_nodes is None: return []`, around line 1576).

This is a silent drop of an out-of-mesh load.

Fix #2 must therefore do two things:

- measure x̄ from p2 toward p1, or use the segment's true centroid;
- turn the silent `return []` into a hard error, or into a defined boundary-node assignment.

Removing or guarding the `continue` changes nothing.

*Self-correction:* Rev 1's "x = −0.75 m boundary" explanation was right. My first audit wrongly called it unsupported.

### 3.3 Interpolation axes

**Correct.** `interpolate_udl_magnitude([p1[0], 0, p1[1]])` uses the y component (lines 1713–1714). It must use z: `[p1[0], 0, p1[2]]`.

### 3.4 Patch double-counting — the cause is not identified and the fix is unspecified

Fully bounded cells are processed in the `bound_grid` loop. Edge-intersected cells come from four `_get_line_load_nodes` calls, one per patch edge. **The 4 corner cells are counted twice:**

- 7×17 mesh: 100 evaluations for 96 cells; area 210 m² instead of 204 m², an excess of 4 × 1.5 m².
- 7×13 mesh: area 212 m², an excess of 4 × 2 m².

There is also a second bug: the duplicate-removal loop pops list items while enumerating the same list.

"Replace with exact numerical cell-integration" names no algorithm.

The current per-cell scheme assigns magnitude A_cell × mean(vertex p) at a p-weighted vertex centroid (`utils.get_patch_centroid`). This is:

- **exact** for uniform p (force and moment);
- **approximate** for non-uniform or partially covered cells. That is a discretization error of order |∇p|·h². It is bounded and falls with mesh refinement, but it is not zero.

A 10⁻⁶ gate on non-uniform patches is therefore unattainable on coarse meshes unless the integration is made exact. That means clipping polygons per cell plus analytic integration of a bilinear p, with its first moments. Rev 3 must either specify the exact algorithm or adopt a documented h-dependent tolerance.

### 3.5 Prototype evidence (sandbox only)

I prototyped the corrected line assignment: W·L, centroid measured from p2 toward p1, z index, and a raise on out-of-mesh placement.

**Baseline (current code), force ratio F/F_exact and centroid error x̄_err:**

| Mesh | Uniform barrier | Asymmetric partial, non-uniform | Asymmetric non-uniform |
|---|---|---|---|
| 7×13 | 0.4583 (x̄_err +1.00 m) | 0.6019 (x̄_err +1.46 m) | 0.5635 (x̄_err −0.58 m) |
| 7×17 | 0.6250 (x̄_err +0.75 m) | 0.7708 (x̄_err +1.135 m) | 0.6761 |
| 7×25 | 0.9583 (x̄_err +0.50 m) | 1.1065 (x̄_err +0.785 m) | 1.0139 |

**Prototype:** F/F_exact = 1.000000000 in every case, with |x̄_err| and |z̄_err| ≤ 1e-14 m.

The assignment is therefore **exact to roundoff** for piecewise-linear w, using resultant placement with bilinear shape functions. Force, moment and centroid were tested separately, on asymmetric and non-uniform loading.

**FE solve** (asymmetric non-uniform line load plus a point load, total 143,000 N):

- reaction sum = −143,000.000000 N (relative error 4.1e-16);
- x̄ error 2.9e-13 m; z̄ error 2.7e-13 m.

---

## 4. DEF-19 — full live-load pipeline trace (`analyser.py`)

| Stage | Code | What happens |
|---|---|---|
| Lane reduction | 1797, `alf = list(LANE_REDUCTION_FACTORS)`; `keyfile.py:119` = `[1.0, 0.8, 0.4]` | Indexed **per vehicle within each vehicle type's coordinate list**, not per number of loaded lanes |
| DLA | 1803, `dla = 1.0 + IRC6_2017.cl_208_3_impact_factor(self.L)` | `irc6_2017.py:523` tests `if KEY_VEHICLE[1]:`, where `KEY_VEHICLE[1]` is the string `'Class70R(T)'`. The string is always truthy, so the function returns **0.10 for every vehicle on 9–45 m spans, including Class A**. This is a latent defect. |
| Generation | 1824–1841, `lc.add_load(vehicle, load_factor=lane_factor)` | The lane factor is dropped (DEF-01). The case is added with `model.add_load_case(lc, load_factor=dla)`. |
| Governing selection | Envelope of Mz_i over the vehicle cases | The cases include DLA (1.10) and **exclude** lane factors, so the governing case can be mis-selected |
| Governing LL case | 2025–2027, `LL.add_load(entry["load"])` | Lane and DLA factors are dropped again; `add_load_case(LL, load_factor=psf)` |
| Caller | `plategirderbridge.py:635` | psf = 1.0 |
| Combinations | LL entries are copied | Factors are applied zero times, or once, depending on the path |
| Reporting | `reports/chap3.py` 88–116 | Prints the Class A impact as 9/(13.5 + L) = 0.24 |

**Findings:**

1. **Analysis and report disagree.** Analysis applies 1.10; the report states 1.24 for Class A.
2. **Rev 2's oracle (DLA 1.15) is a third value.** It uses the RCC formula 4.5/(6 + L) for a steel-composite plate-girder bridge. The applicable provision is IRC 6 Cl. 208, and for steel/composite superstructures that must be confirmed by the engineering owner (a new DEC item). It must not be asserted.
3. **The lane-factor constants disagree.** Rev 2 cites "Table 6A: α = 1.0/1.0/0.9". The code uses [1.0, 0.8, 0.4], applied per vehicle. IRC 6 Cl. 205 ("Reduction in the Longitudinal Effect on Bridges Accommodating more than Two Traffic Lanes", the 2017 contents numbering) applies to the total effect by number of lanes. My understanding is no reduction for 2 lanes, 10% for 3 and 20% for 4, but **I have not confirmed this from the code text (UV)**. Rev 2 also cites Cl. 204.4 for this; in IRC 6-2017, 204.4 is the congestion-factor clause. Either way, oracle ≠ code ≠ cited clause. This is an unregistered latent defect (call it DEF-19b).
4. **The oracle "≥ 1.725 × nominal" is one-sided.** It accepts double application (e.g. 1.15² or 1.5² compounding). The exactly-once requirement needs an equality oracle with tolerance at each of three stages:
   - the vehicle case (DLA only);
   - the governing selection (DLA × lane factor);
   - the ULS combination (γQ × DLA × lane factor).
5. **The negative test "short by 15%"** depends on the unconfirmed 1.15 value. Against the code's actual DLA the shortfall is 10%.

*Self-correction:* my first audit's "about 15%" also used the RCC formula. The production analysis applies 10%.

---

## 5. DEF-10 — packaged SQLite challenge

| Question | Result |
|---|---|
| Do the 1,129 records exist? | **Yes.** `schema.sql` has 1,129 INSERT statements: stations 443, temperature_data 443, zone_data 139, windspeed_data 104. |
| Is the build reproducible? | **Logically yes, byte-wise only with a pinned SQLite.** Two builds with SQLite 3.53.1 are byte-identical (`0369ef48…`, 180,224 B). They differ from the device file `1d767658…`, which has header version 3054001 (SQLite 3.54.1). The iterdump content is identical. **The acceptance hash must be a logical-content hash** (e.g. a sha256 of the sorted iterdump), or the SQLite version must be pinned. |
| Journal mode | Header bytes 18/19 = 1, i.e. rollback journal, not WAL |
| `mode=ro` in a read-only directory, non-root | Works. No `-journal`, `-wal` or `-shm` files; directory mtime unchanged; nothing written to CWD; writes refused with "attempt to write a readonly database". |
| Missing file | `OperationalError: unable to open database file`. Rev 2's spec expects `FileNotFoundError`, which needs an explicit `Path.is_file()` pre-check. |
| Corrupt file | `DatabaseError: file is not a database`, raised at the **first query**, not at `connect()` |
| Truncated file | Reported only when missing pages are touched. A `PRAGMA quick_check` (or row-count and content-hash validation) at open is required. |
| URI construction | `f"file:{DB_PATH}?mode=ro"` breaks on `#`, `?` and `%` and on Windows drive paths. Use `Path.resolve().as_uri() + "?mode=ro"`. |
| Other writes on connect | `connect()` also runs `run_schema` → `_bootstrap_stations_if_missing` and a `PRAGMA foreign_keys`. These must be removed or made read-only-safe; the spec covers `executescript` only. |
| Access paths | `ui_fields_project_location.py:24`, `report_generator.py:666`, `desktop/ui/dialogs/project_location.py:932` and `zone_lookup.py:189` (`db_path` parameter). The CWD default is used only in `database.py __main__` (line 356). **Batch 8 lists only two files.** |
| Packaging | `pyproject.toml` package-data `core/data/**/*` ships whatever untracked `weather.sqlite` is present, since `*.sqlite` is gitignored except `Intg_osdag.sqlite`. An explicit build step plus a content-verification gate, or tracking the file, is required. |
| Installed package | **Not verified.** No wheel or installed test was performed; this is UV. |

`mode=ro` alone does not solve the original problem.

---

## 6. The invariants and the 10⁻⁶ tolerance

- **Accumulation error.** The measured accumulation error is ~1e-16 relative (prototype assignment) and ~4e-16 (FE reactions). A relative gate of 1e-9 is safe with five or more orders of margin.
- **The "+1 N" absolute floor is unjustified and masks the defect.** A 1 N/m line load on 24 m (exact 24 N) loses 1 N under the current code, and **passes** the Rev 2 gate (1e-6·24 + 1 = 1.00002 N). Loads of 10 N/m, 6,540 N/m and 5e6 N/m fail correctly. Replace the floor with a magnitude-scaled one, e.g. `abs_tol = 1e-9 · max(ΣP, Σ|P_i|)`, with no constant floor.
- **Centroid gate.** 10⁻⁶·L (0.024 mm) is attainable for line and point loads (measured 1e-13 m). It is **not attainable** for non-uniform patches under the current integration scheme (§3.4).
- **Detecting the original defects.** The gate catches every original defect at realistic magnitudes and at the asymmetric fixtures above, except the small-magnitude case masked by the floor.
- **Rejecting legitimate results.** At 10⁻⁶ the gate rejects no legitimate line or point results. It would reject a correct but approximate patch scheme.
- **Internal contradiction.** DEF-02 and Batch 4 gate BASIC_1 at ±0.05%, which contradicts the 10⁻⁶ invariant. Combined-reaction checks are the same statics, so they need the same tolerance.

---

## 7. DEF-12 — the "3,380×" claim

- **Production result for sealed geometry 1 is 214,533 kN.** It comes from `designer.py` 1645–1690: Euler f_cc with no fy cap, rys from the *stiffener* inertia, A = (b1 + d/2)·tw.
- **The correct value for the same geometry is 63.40 kN** (§2.1).
- **Like-for-like ratio:** 214,533 / 63.40 = **3,384×**. Rev 2 instead writes "214,533 kN → 118.8 kN". 118.8 kN belongs to the *hand* fixture, so that comparison mixes geometries; taken literally it implies 1,806×.
- **The ratio is not universal.** It depends on the stiffener's tq and H, which enter rys. For context, 214,533 kN on 6,030 mm² is about 35,577 MPa, and the squash load is 1,918.8 kN (about 112× overpredicted against squash alone).
- **The safety consequence is overstated.** The row "Brg.Stiff: Web Buckling" runs only in full-verification mode, i.e. when stiffener tq is supplied. It reports a **false "PASS = stiffener not needed"**. The supplied stiffener's own column buckling (curve c, A_eff = 2·H·tq + 2·20tw·tw) is still checked correctly. The defect is a false-pass reporting error that could lead a user to omit a stiffener. "Most dangerous / life-safety" is not established.
- **The traceability wording "overpredicting by thousands of kilonewtons" understates it**; the overprediction is ~214,470 kN.

---

## 8. Inventory, DAG and batch coverage

- **Inventory.** DEF-19 appears consistently in the traceability matrix, the dependency analysis, the blueprint and Batch 3. The unregistered items are:
  - DW full-width application (8.5 m vs 7.5 m);
  - `cl_208_3` truthy-string DLA selection;
  - lane-factor constants and indexing;
  - analysis/report impact mismatch;
  - the silent `return []` drop of out-of-mesh loads (this belongs to DEF-18, but needs its own acceptance test);
  - patch corner double-count and the list-pop bug (also DEF-18).
- **Coverage.** The 8 batches cover all active registered defects: DEF-01, 02, 03, 05, 07, 08, 10, 11, 12, 13, 18 and 19. DEF-09 passes in baseline. DEF-06, 14 and 17 stay correctly behind DEC sign-off.
- **Ordering gap.** Batch 2's fixture total depends on DD 1249.5 (ρ 24.5) and SW at ρ 78.5 with A = 0.0324. Those require DEF-13 (Batch 5) and a DEF-03 fixture mechanism. The Batch 2 gate must use production-default inputs, or Batch 5 must come first.
- **Expected-state matrix.** The row for `TC-REG-A01` merges DEF-01 and DEF-19 into one test, which violates one-defect-per-test traceability. DEF-19 needs its own test.
- **Branch.** `fix/phase-3-engineering-remediation` **does not exist**: `refs/heads` holds only `dev`, and the reflog has 1 entry. It is correctly a future proposal.
- **Rollback.** `git revert` on the fix branch is valid. One defect per commit holds, except Commit 2.1, which bundles three DEF-18 sub-fixes. That is acceptable under one defect, but the sub-fixes should be separately testable.

---

## 9. Preservation (device, 11:19:44 UTC)

| Item | Observed | Status |
|---|---|---|
| HEAD / branch | `ref: refs/heads/dev` → `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`; only `dev`; reflog 1 line; no locks | ✔ |
| Source | 282 files, aggregate `7c9294813b58fb84…` | ✔ unchanged |
| `weather.sqlite` / `Intg_osdag.sqlite` | `1d767658…` / `25f97857…` (270,336 B) | ✔ |
| Trust ledger | `5a9b9273c26ed92f…` | ✔ |
| 6 seals / 184 files | ALL_OK (verified 11:08) | ✔ |
| `bb29f1a4` vs `fe82935a` | Distinct manifests `02e81c07…` / `d0e791ef…` | ✔ |
| Phase 2.15 loss disclosed | Yes, with a wrong file reference (F-PRES-04) | Partial |
| `PHASE_2_FINAL_CLOSURE_AUDIT.md` | `3d5578c2…` | ✔ unchanged |
| My first Phase 3 audit | `088b10fe…` | ✔ unchanged |
| Rev 1 documents | In place and byte-identical in `v1_original/` | ✔ |
| `testing/` changes | Only `testing/scratch/verify_phase_2_17_documentation_only.py` (08:00 UTC, pre-Rev 2, outside evidence) | ✔ |

---

## 10. Self-corrections to my first audit

1. The DEF-18 end-bay drop: Rev 1's "x = −0.75 m" explanation was correct. My suggestion that the `continue` was the likely cause was wrong.
2. "About 15% DLA" used the RCC formula. Production applies 10%; the report prints 24% for Class A.
3. My first audit's header gave the inspection window as 09:20–10:15 UTC. The file was committed at 09:33:04 UTC, so the stated window was inaccurate.

---

## 11. Finding-resolution table — concrete defects and gaps only

| # | Severity | Document / location | Defect | Required correction |
|---|---|---|---|---|
| R2-01 | **Material** | Traceability §2 (l.73), Blueprint l.71, Batch 4 | BASIC_1 = 2788.751 kN is an arithmetic error; the stated inputs give 2818.242 kN | Recompute; gate at the invariant tolerance |
| R2-02 | **Material** | Unified fixture (DW) | Oracle DW over 7.5 m; production applies 8.5 m (sealed: 244.8 kN); no defect registered | Register a DW-extent defect with a provision reference (owner DEC), or set the oracle to production behaviour |
| R2-03 | **Material** | Unified fixture (SW), DEF-13, Batch 5 | Hand-fixture girder A = 0.0324 asserted on the sealed bridge (snapped A = 0.025192) | Pick one geometry; specify how the fixture forces the plates, or use 0.025192 |
| R2-04 | **Material** | DEF-19 oracle | DLA 1.15 (RCC formula) and α 1.0/1.0/0.9 match neither the code (0.10; [1.0, 0.8, 0.4]) nor the report (0.24); one-sided "≥" | Raise a DEC for the applicable Cl. 208 / Cl. 205 values; use exact three-stage equality oracles |
| R2-05 | **Material** | DEF-19 inventory | Unregistered: `cl_208_3` truthy-string defect; lane-factor constants and indexing; analysis/report impact mismatch | Register as separate defects with tests |
| R2-06 | **Material** | DEF-18 fix #2 | Mechanism attributed to a `continue` that never fires | Fix centroid placement relative to p2→p1; replace the silent `return []` with an error |
| R2-07 | **Material** | Invariants | "+1 N" floor passes the original defect at 1 N/m | Use a magnitude-scaled absolute floor; no constant |
| R2-08 | Significant | DEF-18 fix #4 | Patch cause (corner double-count, list-pop bug) not identified; "exact integration" unspecified; non-uniform scheme approximate | Specify the algorithm, or an h-dependent documented tolerance |
| R2-09 | Significant | DEF-02 / Batch 4 | ±0.05% contradicts the 10⁻⁶ invariant | Unify tolerances |
| R2-10 | Significant | DEF-10 spec / Batch 8 | f-string URI; no `quick_check`; `FileNotFoundError` not produced by sqlite; bootstrap/PRAGMA on connect; byte hash SQLite-version-dependent; 2 of 4+ access paths listed; packaging step unspecified; installed-package test absent | Address each item in the spec and gate |
| R2-11 | Significant | Batch plan / DAG | Batch 2 oracle needs DEF-13 (Batch 5) inputs | Reorder, or use production-default oracles |
| R2-12 | Moderate | Batch plan DEF-12 rationale | "3,380× (214,533 → 118.8)" mixes geometries; consequence overstated | 3,384× for sealed geometry 1 (214,533 → 63.40); describe as a false-pass report row |
| R2-13 | Minor | Acceptance DEF-12 | φ = 7.1141 is wrong (7.6130) | Correct the intermediate |
| R2-14 | Minor | Acceptance DEF-01 negative test | "R = 1.09174" for a 1.15× hard-code | R = 1.15 |
| R2-15 | Minor | Preservation §7 | Cites a non-existent `PHASE_2_16_FINAL_INDEPENDENT_GATE_AUDIT.md` | Cite `PHASE_2_16_FINAL_INDEPENDENT_AUDIT.md` |
| R2-16 | Minor | Preservation §2 | "282 python files" | 282 files (205 `.py`) |
| R2-17 | Minor | Traceability historical note | "Preliminary SW 165.28" | Preliminary is 169.8; 165.28 corresponds to A = 0.021932 |
| R2-18 | Minor | Expected-state matrix | DEF-01 and DEF-19 share one test | Separate the tests |
| R2-19 | Evidence gap | F-PRES-03, F-PRES-05 | Package versions and exit-1 cause not evidenced | Attach the source records or mark as UV |

**Batch 1 (DEF-12, DEF-08, DEF-11)** is the least affected by these errors. After a Revision 3 that addresses R2-12 and R2-13, it would be the natural first candidate *if the user chooses to authorize implementation*. Its gates would be:

- F_cdw = 118.79 kN ± 0.01 kN on the hand fixture;
- 63.40 kN on sealed geometry 1;
- the web-buckling row reports FAIL / stiffener required for both;
- unchanged expected states for all other tests;
- preservation of every hash in §9.

This is not an authorization.

*End of re-audit.*
