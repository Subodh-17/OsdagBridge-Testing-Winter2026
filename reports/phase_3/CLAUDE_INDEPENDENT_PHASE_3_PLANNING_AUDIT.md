# Phase 3 — Independent Engineering Blueprint Audit

| | |
|---|---|
| **Auditor** | Claude (independent; did not author the Phase 3 plans) |
| **Date** | 2026-11-18 (inspection 09:20–10:15 UTC) |
| **Subject** | Six Antigravity planning documents in `reports/phase_3/` (written 09:13–09:17 UTC) |
| **Baseline** | `source/OsdagBridge`, branch `dev`, commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` |
| **Mode** | Read-only. No source, test, database, environment, Phase 2 evidence or report was modified. Nothing was committed or pushed. This report is the only file written. |

**Evidence classes used below**

| Code | Meaning |
|---|---|
| **IV** | Independently verified by me: source read at the frozen commit, sealed evidence read, or independent computation |
| **IR** | Independently reproduced by execution in a disposable sandbox (a cloud clone of `d74f56dd`; nothing on the user's machine was executed) |
| **SE** | Confirmed from sealed Phase 2.13 baseline evidence (`testing/evidence/phase_2_13/baseline/*.log`, seal `fb966e81`, verified valid) |
| **UV** | Unverified: Antigravity's claim, not checked or not checkable |

---

## 1. Overall verdict

# REJECTED — MATERIAL ENGINEERING ERRORS

The rejection is of the **plan**, not of the defect inventory.

**What holds up.**

- **Defect existence.** All 12 active defects exist at the frozen baseline (IV/SE).
- **Blocked items.** DEF-06, DEF-14 and DEF-17 are correctly identified as blocked architectural gaps.
- **DEF-09.** Correctly identified as a passing environment check.
- **Source locations.** Most citations are accurate; seven are partly wrong (§3).

**Why the plan is rejected.**

- **Six acceptance oracles are numerically wrong or inconsistent** (DEF-02, DEF-03, DEF-05, DEF-12, DEF-17, DEF-18). They would **fail a correct fix or pass an incorrect one**.
- **The DEF-18 remediation is incomplete.** I reproduced the baseline failure exactly: a line load loses a whole end segment, not only the segment-length factor.
- **The DEF-01 remediation misses factor composition.** Lane-reduction factors and the dynamic load allowance (DLA) are silently lost in the governing live-load case and in every combination. This is a latent defect the plan does not list.
- **The dependency DAG makes the most critical fixes wait on unratified engineering decisions.** DEC-013 gates DEF-18, DEF-01 and DEF-02. DEC-015 and DEC-018 gate DEF-12 and DEF-08. It also contains several dependency edges that do not exist in the code.
- **The preservation report asserts facts that do not match the evidence:** a wrong run UUID, a wrong OS edition and wrong package versions. The preservation state itself is intact; I verified that independently.

None of these errors requires re-discovery. All are planning corrections, listed as exact prerequisites in §9.

**Implementation is not authorized by this audit.** It requires the user's explicit approval after the corrections.

---

## 2. Preservation gate

Verified independently on the device, read-only (IV).

| Item | Result |
|---|---|
| Branch / HEAD | `dev` / `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`. Reflog has 1 entry (clone). Only ref `dev`. No `.git` locks. |
| Working tree | `src` aggregate 282 files / `7c9294813b58fb84ecd965643daec240276747d1788b13187c0e0f46c52b024c`. No file in `source/OsdagBridge` (outside `.git`) newer than 2026-11-17 18:25 UTC. |
| `weather.sqlite` / `Intg_osdag.sqlite` | `1d767658…7e98` / `25f97857…ea91`: unchanged |
| Production ledger | `5a9b9273c26ed92f95a2012ec0b1f890cfee369b2099659da875c00e182f57f1` (mtime 2026-11-17 18:15): unchanged |
| Six official seals | HMAC 6/6 valid, manifests 6/6, **184/184** files re-hash (key read in place) |
| Operator run `bb29f1a4` | containment `c68cbc6c…`, governance `76998aeb…`, manifest `02e81c07…`: unchanged |
| Reference run `fe82935a` | `088eaaae…` / `0a66f7ed…` / `d0e791ef…`: unchanged |
| Runner / launcher | `31f0ea49…` / `57b59de3…`: unchanged |
| Phase 2 reports and evidence | Nothing under `testing/` or `reports/` changed after my closure audit (08:35 UTC) except the six new `reports/phase_3/*` files. `PHASE_2_FINAL_CLOSURE_AUDIT.md` is byte-identical (`3d5578c2…`). |
| `.git` directory mtime | 09:17:40 UTC with no content change. Consistent with a transient lock from Antigravity's `git status`. |

**Preservation status: INTACT.**

### Errors inside `PHASE_3_BASELINE_PRESERVATION_REPORT.md` (IV)

| Claim | Fact |
|---|---|
| `fe82935a` UUID `fe82935a-93f5-4428-98e3-0c463f28cf0d` | Actual `fe82935a-0927-443a-b7be-aa730468d388` (manifest) |
| Platform "Windows 11 Enterprise" | Actual "Windows 11 Home Single Language" (both run manifests) |
| OpenSeesPy 3.5.1.1, pythonOCC-core 7.8.1 | Sealed baseline environment metadata records openseespy 3.8.0.0, OCC 8.0.1 |
| "phase_2_4 … phase_2_17: 100% intact; nothing overwritten" | The Phase 2.15 transcript `cb5c77b9…` was overwritten in Phase 2.16 and declared lost |

These values were evidently not taken from measurement output. The report's attestation therefore cannot be relied upon as evidence. My independent check above stands in its place.

---

## 3. Findings by defect

**Legend for "Exists":**

- ✓ = confirmed at `d74f56dd`
- B = confirmed but correctly BLOCKED pending a decision
- P = passing check, no defect

| ID | Exists | Representation | Source location | Fix spec | Oracle / acceptance | Verdict |
|---|---|---|---|---|---|---|
| DEF-01 | ✓ IV+IR+SE | Accurate | Mostly accurate; the loop at `osp_grillage.py:1934` is in `_distribute_load_types_to_model`, not `_assign_load_to_four_node` | **Incomplete** (factor composition) | Adequate, but needs composition cases | Correct required |
| DEF-02 | ✓ IV+SE | **Inaccurate numbers** | Accurate | Correct in principle | **Coupled and mis-stated** | Correct required |
| DEF-03 | ✓ SE (UV root cause) | Accurate (symptom) | `initial_sizing.py:519–520` is **not** a snapping site | Incomplete (composite stiffness ignored) | **Wrong numbers** | Correct required |
| DEF-05 | ✓ IV+SE | Accurate | Accurate | Incomplete (terrain key) | **Wrong Pz** | Correct required |
| DEF-06 | B IV+SE | Accurate | Accurate | Premature (DEC-015) | **Physically inconsistent** | Keep blocked |
| DEF-07 | ✓ IV+SE | **Conflates two failure modes** | Accurate | Incomplete (shear range; section-sign harmonization; fatigue source) | Partly adequate | Correct required |
| DEF-08 | ✓ IV+SE | Accurate | Accurate | Incomplete ("not evaluated" state; overall status girder-only) | Adequate | Minor corrections |
| DEF-09 | P SE | Accurate | Harness only | None needed | Adequate | Accepted |
| DEF-10 | ✓ IV+SE | Partly overstated | Accurate | **Changes the problem** (AppData) | Tied to the wrong design | Redesign required |
| DEF-11 | ✓ IV+SE | **Consequences overstated** | Accurate | Correct | Adequate | Severity correction |
| DEF-12 | ✓ IV+SE | Accurate | Accurate (±2 lines) | Mostly correct; boundary conditions missing | **Arithmetic wrong** | Correct required |
| DEF-13 | ✓ IV+SE | Accurate | `analyser.py:10` is an import, not `= 78.5` | **Calls a nonexistent parameter**; misses deck density | Coupled to DEF-03 | Correct required |
| DEF-14 | B IV+SE | Accurate | Accurate | Plausible; torsion omitted; needs DEC-013 | Arithmetic correct | Keep blocked |
| DEF-17 | B IV+SE | **Wrong vehicle** | Accurate | Plausible; needs DEC-018 | **Wrong vehicle and moment** | Correct required |
| DEF-18 | ✓ IV+IR+SE | Partly accurate | Accurate | **Incomplete** (end-segment drop) | **Inconsistent totals; tolerances unjustified** | Correct required |

### DEF-01 — load factor ignored

- **Defect (IV+IR).** `LoadCase.add_load()` stores `load_dict["factor"]` (`load.py:1166–1168`). No code in `osp_grillage.py` or `load.py` ever reads it. My sandbox reproduction showed a 100 kN point load added with `load_factor=1.35` assigning 100.000 kN of nodal force.
- **Where the factors actually live.** Case-level factors (`model.add_load_case(lc, load_factor=…)`) *are* applied through the OpenSees time series. Every ULS and SLS combination, however, is built by copying load entries with per-entry factors (`analyser.py:2344–2348`, `2539–2543`) and then registering the combination with factor 1. So every combination is unfactored (SE: BASIC_1 analysed 1736.55 kN vs superposition 2710.16 kN).

**Omission (IV): factor composition.** Fixing only the `osp_grillage.py` loop is not sufficient:

1. **Lane factors are dropped.** Lane-reduction factors are attached per entry (`analyser.py:1836`, `lc.add_load(vehicle, load_factor=lane_factor)`). The governing LL case is rebuilt with `LL.add_load(entry["load"])` (`analyser.py:2025–2027`), which drops them.
2. **DLA is dropped.** DLA is applied only at case level to the vehicle cases (`analyser.py:1841`). The governing `LL` case is registered with `partial_safety_factor=1.0` only (`plategirderbridge.py:635`). **DLA is therefore absent from LL and from every combination.** This is a latent defect not in the inventory; it is unconservative by the impact fraction (about 15% for a 24 m Class A span under Cl. 208).
3. **Copy sites drop entry factors.** `create_dead_load_combination`, `create_sidl_combination` and `create_governing_ll_load_case` all copy `entry["load"]` without its factor.

**Required fix spec.** The effective factor of every load must be the product: entry factor × source-case factor × combination factor. It must be preserved at every copy site. Acceptance must include cases with non-unit lane factors and DLA. Fixing the loop alone would also change which vehicle case is "governing", because lane factors would start acting there but still be lost downstream.

**Double application check.** Sub-cases are registered at case factor 1.0 and combinations at 1.0, so honouring entry factors does not double-factor at pattern level. That stops being true if anyone later passes non-unit `partial_safety_factor` to the sub-cases. Acceptance must include that case.

### DEF-02 — SIDL omitted

- **Defect (IV).** `create_sidl_combination()` is never called (`plategirderbridge.py:1336–1339`), so `sidl_combination` is `None` and is skipped in `create_dead_load_combination` (`analyser.py:1532–1546`). The proposed one-line insertion is correct in principle.
- **Representation errors.** The plan states the baseline barrier contribution is "0.0 kN". The sealed log records **−708.74 kN** "observed barrier contribution" in BASIC_1 (SE). That figure is an artefact of DEF-01 and DEF-18 acting together, which shows the test is not isolated.
- **"Expected 264.87 kN" is not an independent oracle.** It equals 1.35 × 196.20 kN, and 196.20 kN is the *defective* FE barrier reaction (DEF-18). The plan's acceptance criterion instead uses 1.35 × 313.92 = 423.79 kN. That is the correct physical value, but it can only be met after DEF-01 **and** DEF-18 are fixed.
- **Standard (IV).** IRC 6:2017 Table B.2 groups SIDL other than surfacing with dead load at γ = 1.35 adding / 1.0 relieving, and surfacing at 1.75 / 1.0. The plan's factors are consistent with this.
- **Coverage gap.** The BASIC_1 tested is "1.35DL + 1.75DW" only; no variable load is checked.
- **Required.** An isolated DEF-02 oracle at γ = 1: the presence of the barrier, railing and median load objects in `dead_load_combination`, plus their unfactored resultant. The factored check belongs to the combined acceptance after DEF-01 and DEF-18.

### DEF-03 — section properties desynchronized

- **Symptom (SE).** Grillage girders carry A = 0.022534 m², Iz = 0.00734091 m⁴ against 0.025192 / 0.00792758 derived from the snapped plates.
- **Root-cause citation (IV).** `initial_sizing.py:519–520` is the return dictionary of the symmetric-section branch. It is not a snapping site. The actual desynchronisation point is **unverified**.
- **Wrong oracle (IV).** For the plan's own fixture (dw 1300, tw 10, top 400×16, bottom 500×26) I derive A = 0.032400 m², ȳ = **0.539957 m**, Iz = **0.0097174 m⁴**, Iy = **0.0003563 m⁴**. The plan states ȳ = 0.539577, Iz = 0.0088700 (−8.7%) and Iy = 0.0003672 (+3.1%). A correct implementation would fail the plan's 0.1% criterion.
- **Unaddressed assumption (IV).** The longitudinal grillage members use **bare-steel** properties (`_girder_section`). Meanwhile `designer.py` computes stresses with the composite section modulus (`Ze_comp_bot`). Composite action of the deck slab with the girders is not represented in FE stiffness for live load or SIDL. Re-synchronising bare-steel properties does not address this. It must be decided together with DEC-013 (short- and long-term modular ratios; steel-only for construction-stage DL if unpropped).
- **Deflection oracle.** The single-girder PL³/48EI reference is valid only for `elasticBeamColumn`, which is ospgrillage's default and is what the model uses. With a Timoshenko element the shear deflection would be about 4% (my calculation), which exceeds the 0.5% tolerance. The criterion must pin the element type. The B01 test's "6-line Courbon 7.218 mm ±3%" is a distribution heuristic, not a deflection oracle; it must not gate acceptance.

### DEF-05 — wind inputs not propagated

- **Defect (IV).** `add_wind_loads()` reads bare keys (`basic_wind_speed`, `avg_exposed_height`, `railing_height`, `crash_barrier_height`, **`terrain_type`**), while the inputs use namespaced keys (`loading.wind_load.*`, `typical_section.*.height`).
- **Fix-spec omission.** The fix omits `KEY_WL_TERRAIN_TYPE` (`loading.wind_load.terrain_type`). Terrain therefore always falls back to "Plain".
- **Wrong oracle (IV).** The plan's target "Pz = 1386.6 N/m² (Table 12, Vb = 47, H = 15)" contradicts the sealed harness target of **1039.6 N/m²** (SE). Table 12 is tabulated for Vb = 33 m/s and scaled by (Vb/33)²:
  - the sealed baseline value 463.7 N/m² at 10 m reproduces the table;
  - 512.5 × (47/33)² = 1039.6.

  The plan's value is unsupported.

### DEF-06 — temperature (BLOCKED, DEC-015)

- **Defect (IV).** A missing input key, and a gravity-type patch "temperature load" (`analyser.py:905–971`).
- **The proposed oracle is physically inconsistent for the modelled structure.** With pinned–roller supports, a uniform ΔT produces free expansion and no restraint force. "F = k·ΔL with k = 10⁶ kN/m on the fixed bearing" would give about 8,400 kN for 8.4 mm, which is unphysical. Restraint comes from bearing shear stiffness or sliding friction, which the model does not represent.
- **Gradient effects.** A temperature gradient in a determinate span produces self-equilibrating sectional stresses and free curvature only. It is a sectional post-processing check, not a grillage load.
- **Values to verify.** α = 1.17 × 10⁻⁵ and the "Table 10 & 11" references must be checked against IRC 6:2017 Cl. 215 for steel–concrete composite decks (UV).
- **Status.** Keep blocked. Remove acceptance numbers until DEC-015 is ratified by the engineering owner.

### DEF-07 — fatigue stress range

- **Two distinct failure modes (IV+SE).** Code at `designer.py:2976–2985`. The plan describes only the first.
  1. **Mixing element ends and elements.** `Mz_i` and `Mz_j` are concatenated across all elements and load cases, then max − min is taken. With OpenSees end-sign conventions this doubles a static moment to 2M₀ (sealed: **125.46 MPa**, path a).
  2. **Clamping at zero.** `max(max, 0) − min(min, 0)` turns a constant sagging moment into a "range" of M₀ (sealed: **62.73 MPa**, path b). It also gives the wrong value for a genuine sign-reversal history (sealed: 188.19 vs 125.45 MPa expected).

  The plan attributes 62.73 MPa to the end-sign mechanism; that is a conflation.
- **Fix-spec omissions.**
  - The **shear range** (`Vy_i`/`Vy_j`, lines 2987–2993) has the identical defect.
  - Ranges must be taken at a physical **section**: element e end j and element e+1 end i are the same section with opposite sign conventions, so harmonise signs, not just "per element per end".
  - Remove the clamp.
- **Unaddressed engineering point.** A range taken across SLS-frequent *combinations* that all contain permanent load is a surrogate. The IRC fatigue range is the stress variation from the fatigue vehicle passage (DEF-17, DEC-018). It also acts on the composite section only for loads applied after composite action. Until DEC-018 is decided, the corrected extraction must be labelled a surrogate.
- **Oracle arithmetic (IV).** 2700 kNm / 0.015942 m³ = 169.36 MPa ✓.
- **Missing negative control.** Invariant 5 (Δσ ≥ 0, static ≡ 0) is satisfied by an implementation that always returns 0. The cyclic positive case must be mandatory.

### DEF-08 — hardcoded summary narrative

- **Defect (IV).** `executive_summary.py:233–236` are literal strings.
- **Fix-spec gaps.**
  - The proposed `.get("status", "PASS")` defaults turn *missing* results into "pass". Cross-bracing, end-diaphragm and deck results may be absent (`crossbracing_design_results`, `end_diaphragm_design_results`, `deck_design_results`), so the fix needs an explicit "not evaluated" state.
  - The table's "Overall Design Status" is computed from girder checks only (lines 77–110). It can report "Pass" while cross-bracing or the deck fails, and must be extended.
  - The plan's dict keys (`cross_bracing`, `end_diaphragm`, `deck`) do not match the actual keys.
- **DCR boundary.** Code fails at > 1.0; the note says "UR < 1.0 passes". Align them.

### DEF-09 — offscreen CAD export

Passing environment check (SE: std 66.6, 3 colours). No source fix. Accepted.

### DEF-10 — weather.sqlite side effects

- **Facts (IV).**
  - `weather.sqlite` is **untracked and gitignored**. It is generated on first `connect()` from `schema.sql` (1,129 `INSERT` rows) into the package directory.
  - All production callers pass `DB_PATH` inside the package: `ui_fields_project_location.py:24`, `report_generator.py:666`, `project_location.py:932`, `zone_lookup.py:189`.
  - The CWD-relative default (`Database()`) is used only by the module's `__main__` block.
  - Every runtime method is a read query. The application never writes user data.
- **The proposed AppData anchoring changes the problem rather than fixing it.** The real defect is that **static, read-only reference data is materialised by side effect at runtime**. Copying a seed into `%LOCALAPPDATA%` would:
  1. create a mutable per-user copy of immutable reference data;
  2. never refresh after updates, because `connect()` re-runs the schema only if the `stations` table is missing, so station data goes stale silently across releases;
  3. write into the real user profile during tests and CI;
  4. invent a "user custom stations" migration requirement that does not exist;
  5. move the file out of reach of the current preservation baseline. The `weather.sqlite` hash `1d767658…` refers to this untracked generated file; the plan does not say what happens to it.
- **Correct remediation.**
  - Ship the database built deterministically from `schema.sql` as package data, or build it in memory at runtime.
  - Open it read-only (`sqlite3.connect("file:…?mode=ro", uri=True)`).
  - Never create files on `connect()`; fail with a clear error if the data is missing.
  - Remove the CWD default.
  - Acceptance: an immutable install directory, zero writes anywhere (not "writes only in AppData"), and identical query results from the read-only path.

### DEF-11 — girder count

- **Defect (IV).** `designer.py:401` sets `n_girders = geom.n_l`.
- **Consequence overstated (IV).** `GeometryConfig.n_girders` is consumed only for a log line (`designer.py:548`), a report key–value line (`2562`) and the output dictionary (`3394`). Report chapters count girders from `girder_entries`. There are **no index errors** and **no design checks for nonexistent G5/G6** at baseline; per-girder design iterates `_girder_count()`.
- **Severity.** Medium (reporting accuracy), not High. The fix is correct.
- **Dependency.** Its claimed DAG edges to DEF-03 and DEF-18 do not exist (§6).

### DEF-12 — bearing-stiffener web buckling

- **Defect (IV).** `designer.py:1662–1669` uses the stiffener inertia `Iys` for the web strip's radius of gyration. It also uses Euler stress with no buckling-curve reduction. Sealed result: 214,533.2 kN vs oracle 63.4 kN (SE).
- **Fix direction.** r = t_w/√12, KL = 0.7d (consistent with the IS 800 web-buckling slenderness λ ≈ 2.5d/t), area (b₁ + n₁)t_w, and buckling curve c via `cl_7_1_2_1_…`. This is correct in principle.
- **Wrong oracle (IV).** For the plan's inputs (t_w 10, d 1300, b₁ 100, f_y 250, curve c, γ_m0 1.1, E 2×10⁵) I derive:
  - λ = 315.2, f_cd = **15.84 MPa**, F_cdw = **118.8 kN**.
  - The plan's f_cd = 8.45 MPa and 63.38 kN are wrong.
  - **63.4 kN is the sealed oracle for a different geometry:** t_w 8, d 1304, b₁ 101.81 (I reproduce 62.4 kN at f_y 250 and 63.4 kN at f_y 350).

  The plan's criterion "63.4 ± 0.1 kN" with its stated inputs would fail a correct fix.
- **Missing provisions.**
  - **KL = 0.7d presumes a restrained compression flange.** For an unrestrained flange the effective length rises toward d, which halves capacity (my calculation: 60.5 kN for the plan's inputs).
  - **End supports.** n₁ = d/2 dispersion assumes web on the far side; at a girder end only the available web length counts. Likewise the stiffener-column effective web strip (20t_w each side, `designer.py:1683`) must be one-sided at ends.
  - **Use of γ_m0.** Must be stated explicitly.

### DEF-13 — steel density hardcoded

- **Defect (IV).** `create_self_weight_load(self, model=None, L=None)` (`analyser.py:371`) uses the imported constant `STEEL_UNIT_WEIGHT_kN_m3` (defined in `…/plate_girder/geometry.py:10`; `analyser.py:10` is the import line).
- **Fix-spec error.** The plan's call `create_self_weight_load(density_kN_m3=…)` would raise `TypeError` unless the signature is changed; the plan does not say so.
- **Omission (IV).** The deck slab uses the default 25 kN/m³ because `create_deck_load(slab_thickness_m=…)` is called without the user's `material.deck.density` (`KEY_MATERIAL_DECK_DENSITY` exists). This is the same class of defect.
- **Oracle.** 4 × 24 × 0.0225344 × 70 = 151.43 kN ✓. But it uses the *unsynchronised* area, so it changes once DEF-03 is fixed. Define the oracle from the derived area, and sequence DEF-03 first.

### DEF-14 — transverse slab (BLOCKED, DEC-013)

- **Defect (IV).** `_transverse_section` = girder/2 (`plategirderbridge.py:1279–1291`).
- **Oracle arithmetic.** 1.5 × 0.2³ / (12 × 6.45) = 1.550 × 10⁻⁴ m⁴ ✓.
- **Missing from the proposal.**
  - The slab torsion constant: for grillage slabs J ≈ b·d³/6 per Hambly, and the girder/2 value is equally invalid.
  - The choice of modular ratio (short- vs long-term) and cracking.
  - Consistency with composite longitudinal stiffness (DEF-03 note).
- **Status.** Keep blocked; DEC-013 must be decided by the engineering owner, not "ratified" inside an implementation batch.

### DEF-17 — fatigue vehicle (BLOCKED, DEC-018)

- **Wrong vehicle (IV).** The plan repeatedly describes a "40-tonne **4-axle**" vehicle with axles "60, 120, 110, 110 kN", totalling 400 kN. The vendored definition (`load.py:1793–1847`, Cl. 204.6) is **3 axles of 12, 14 and 14 t** (117.7 / 137.3 / 137.3 kN, total 392.4 kN) at 4.5 m and 1.4 m spacing, matching the sealed harness ("40t 3-axle").
- **Wrong moment (IV).** The plan's simply-supported moment oracle (≈1342.5 kNm) does not correspond to this vehicle. My moving-load envelope for the 3-axle truck on 24 m is **1996.4 kNm**.
- **Other gaps.** The DLA treatment and lane placement rule for the fatigue vehicle must be taken from Cl. 204.6 / Cl. 208 by the DEC-018 owner (UV).

### DEF-18 — FE load conservation

**Independent reproduction (IR).** Sandbox clone of `d74f56dd`; vendored ospgrillage driven directly; 24 m × 8.5 m orthogonal mesh, 7 longitudinal lines; nodal force commands summed.

| Load | Mesh | Assigned ΣF | Exact | Centroid x |
|---|---|---|---|---|
| Point 100 kN | 7 × 13, 7 × 17 | 100.000 kN | 100.000 | exact |
| Line 6.54 kN/m, x 0–24 | 7 × 13 | **71.94 kN** (= 11 × 6.54) | 156.96 | 13.000 (12.000) |
| Line 6.54 kN/m, x 0–24 | 7 × 17 | **98.10 kN** (= 15 × 6.54) | 156.96 | **12.750** (12.000) |
| Patch 6.25 kPa, full deck | 7 × 13 / 7 × 17 | 1325.0 / 1312.5 kN (+3.9% / +2.9%) | 1275.0 | 12.000 |

The 7 × 17 row reproduces the sealed baseline exactly (98.100 kN per barrier, x̄ = 12.750 m; SE).

**What this establishes.**

1. **Two separate defects.**
   - Each segment contributes W instead of W·L (confirmed at `osp_grillage.py:1717–1727`).
   - **The first end bay is dropped entirely**, which is what shifts the centroid: the remaining 15 of 16 bays have centroid (1.5 + 24)/2 = 12.75.

   The plan's fix `mag = W*L` alone would give 15 × 6.54 × 1.5 = 147.15 kN (−6.25%) with x̄ still 12.75. The "x = −0.75 m boundary offset" explanation is unsupported. The skip branch (`if "ends" not in points.keys(): continue`, line 1677) and the end-intersection cases are the likely site (UV).
2. **Interpolation index bug.** `interpolate_udl_magnitude([p1[0], 0, p1[1]])` passes the y-coordinate where z is intended (lines 1713–1714). This is harmless for uniform loads and wrong for varying ones.
3. **Mesh-dependent patch inflation** (+2.9% to +3.9%) is confirmed. The plan's mechanism ("overlapping grid integration") is plausible but unverified.

**Oracle inconsistency (IV/SE).** The plan uses three different "applied" dead-load totals:

| Source | SW | DD | DW | CB | Total |
|---|---|---|---|---|---|
| Matrix (from the EQ test) | — | 1275.0 | 244.8 | 313.92 | 2003.54 |
| Acceptance criteria (from the A02 test) | 165.28 | 1249.50 | 216.00 | 313.92 | 1944.70 |
| DEF-13 self-weight (169.82 at 78.5 kN/m³) | 169.82 | — | — | — | — |

The deck width (8.5 vs 8.33 m effective) and wearing-course width (8.5 vs 7.5 m) assumptions differ between the sealed A02 and EQ tests. One fixture geometry with one derivation must be fixed before acceptance numbers are written.

**Tolerances.** See §4.

---

## 4. The five universal invariants

| # | Invariant | Definition / units / sign | Tolerance defensible? | Can pass while wrong | Can fail legitimately | Required change |
|---|---|---|---|---|---|---|
| 1 | ΣR_y = ΣP (0.05%) | Correct form; sign convention of ospgrillage p (positive input → +F_y command) must be fixed in the oracle | **No.** Shape-function load transfer is a partition of unity; point loads conserve exactly (IR: 100.000 kN), and uniform/linear line and patch loads can be integrated exactly. 0.05% of 2,000 kN (1 kN) would hide a dropped wheel fraction or a small patch. | Correct total with wrong transverse distribution (sealed DD shares 6.74% vs 6.18% on edge lines); compensating errors across load types; symmetric fixtures | Loads deliberately placed outside the meshed deck (lost by design, so must be modelled, not tolerated); spring or skew supports if reactions are read only at "support" nodes | Assignment-level check: \|ΣF − ΣP\| ≤ 10⁻⁶·ΣP + 1 N per load object and per load type. FE reaction check ≤ 10⁻⁶·ΣP. Report per-type, not just total. |
| 2 | Centroid of reactions = centroid of loads (0.05 m) | Equivalent to moment equilibrium about two axes; correct for any support layout if all reaction nodes are included | **No.** 0.05 m on 24 m (0.2%) is arbitrary; exact first-moment transfer is achievable (IR: point loads exact) | **Symmetric fixtures** (the plan's) hide equal-and-opposite shifts; correct centroid with wrong share between girders | None, if all reactions are included | ≤ 10⁻⁶·L. Mandatory **asymmetric** fixtures (partial-length line load, off-centre patch). |
| 3 | Σ assigned = ∫w dx (0.05%) | Correct; must also preserve the first moment ∫w·x dx per segment | Same as #1 | Equal segment weights with wrong positions (the actual DEF-18 mechanism); dropped segment compensated elsewhere | Segments exactly on grid lines (must not double-count) | Add a per-segment first-moment check; test non-uniform w(x) (exposes the y/z index bug); vary mesh density (13 / 17 / 25 lines) and skew. |
| 4 | Parallel-axis consistency (0.1%) | Correct only with orientation-aware b_i, t_i (web: b = t_w, t = d_w); covers A, ȳ, I_z only | 0.1% is fine given `round()` to 10⁻¹⁰ m⁴; but the plan's own oracle values are wrong (§3 DEF-03) | **Bare-steel properties pass while composite stiffness is ignored**; J and I_y unchecked; A_y/A_z ad hoc | None for exact arithmetic | Add I_y, J (thin-walled Σbt³/3), shear areas; state whether FE stiffness is bare or composite; use corrected numbers. |
| 5 | Δσ ≥ 0; static ≡ 0 | Dimensionally fine | n/a | **An implementation returning 0 always passes**; per-end ranges without section sign harmonisation; clamp-at-zero can pass static-positive cases | Numerical noise around 0 (use an absolute tolerance, e.g. 10⁻⁶ MPa) | Make the cyclic positive control (169.36 MPa) and a sign-reversal case mandatory parts of the invariant; include shear range. |

**General point.** Equilibrium invariants verify conservation, not distribution. Because DEF-14 (transverse stiffness) and DEF-03 (composite stiffness) are open, no invariant in the set checks that girder load *shares* are right. That must be stated as a coverage limit.

---

## 5. Confirmed vs unverified — summary

**Confirmed, independent of Antigravity:**

- the existence of all 12 active defects and 3 blocked gaps;
- the DEF-01 factor drop (IR);
- the DEF-18 line-load W-not-W·L defect, **plus a dropped end segment**, plus patch over-integration (IR, matches sealed values exactly);
- the DEF-02 missing SIDL call;
- DEF-05 bare keys (plus terrain);
- the DEF-07 concatenation and zero-clamp, and the same pattern in shear;
- DEF-08 literal strings;
- DEF-10: package-directory materialisation of a read-only generated database;
- DEF-11: `n_l` used for a reporting count;
- DEF-12: stiffener `Iys` plus Euler stress;
- DEF-13: hardcoded steel density (plus deck density);
- DEF-14: girder/2;
- DEF-17: no fatigue pass; the vehicle is 3-axle.

**New latent defect found (not in the inventory):**

- Lane-reduction factors and DLA are lost in the governing LL case and all combinations (§3 DEF-01).
- Interpolation y/z index swap in line-load magnitude (§3 DEF-18).

**Unverified Antigravity claims:**

- DEF-03 root-cause location;
- the DEF-18 patch mechanism and the "x = −0.75 m" explanation;
- the DEF-06 code references (α, tables);
- DEF-17 DLA and lane rules;
- OpenSeesPy / pythonOCC versions (contradicted by sealed metadata);
- the 15–20 s runtime estimate for DEF-17.

**Technical errors in the plan:**

- wrong oracles for DEF-03, DEF-05, DEF-12, DEF-17 (vehicle and moment), DEF-06 (restraint physics);
- inconsistent DEF-18 totals;
- the DEF-02 baseline misstatement;
- the DEF-07 mechanism conflation;
- the DEF-11 consequence overstatement;
- the DEF-13 invalid call;
- the DEF-10 redesign that changes the problem;
- preservation-report facts (§2);
- the blueprint's "bit-exact parity between human and automated validation packages" (the two runs are deliberately different fresh executions with different hashes).

---

## 6. Dependency DAG and batch plan

### 6.1 Edges in the plan's DAG that do not exist in the code (IV)

| Edge | Why it is not a real dependency |
|---|---|
| DEF-13 → DEF-03 | Density and section properties are independent inputs; only the DEF-13 *oracle* depends on A |
| DEF-03 → DEF-11 | DEF-11 is a reporting count; no property assignment depends on it |
| DEF-11 → DEF-18 | Load-to-node distribution is purely geometric and independent of the designer's `n_girders` |
| DEF-14 → DEF-18 | Load conservation does not depend on stiffness; only reaction *distribution* does |
| DEF-18 → DEF-12 | The capacity formula is independent of demand; only the pass/fail outcome depends on R |
| DEF-05 / 06 / 17 → DEF-01 | Direction is inverted for verification purposes: DEF-01 is a prerequisite for meaningful combinations of those loads, not their consumer |
| Stage 4 → Stage 5 → Stage 6 | DEF-12 and DEF-08 have no dependency on DEF-17 or DEF-06 |

### 6.2 Missing or hidden dependencies

- **DEF-01 ↔ live-load construction.** Factor composition (lane, DLA) and the governing-case selection change when entry factors start being honoured.
- **DEF-02 acceptance requires DEF-01 and DEF-18.** Its isolated oracle must be unfactored and presence-based.
- **DEF-13 oracle requires DEF-03.**
- **DEF-07 ultimately requires DEF-17 (DEC-018).** The extraction fix is independent and can proceed, labelled as a surrogate.
- **DEF-03 interacts with DEC-013** through composite stiffness.
- **Harness governance.** `evidence_guard.ACTIVE_PHASE = "phase_2_17"` and the per-test baseline/remediation manifests must be updated (a harness change) before any Phase 3 run can produce governed evidence. The plan does not address this.

### 6.3 Structural flaw

With the rule "no downstream consumer may be modified until all upstream are remediated", placing **blocked DEF-14 (DEC-013) in Stage 2** halts DEF-18, DEF-01 and DEF-02, the three most consequential defects. Placing DEF-17 and DEF-06 (DEC-018, DEC-015) before Stage 5 halts DEF-12 and DEF-08.

Each batch also "ratifies" a DEC (Batches 3, 6 and 8). An implementation batch cannot ratify an engineering decision. Ratification belongs to the engineering owner, outside the batch.

### 6.4 Other batch-plan defects

- **Rollback.** "`git checkout HEAD -- <files>`" only discards *uncommitted* edits. After an atomic commit it is a no-op. Rollback of a committed batch is `git revert <batch commits>` on the fix branch, plus re-running the governed suite.
- **"Pass the full 15-test baseline suite" is ill-defined mid-sequence.** Each batch needs an explicit expected-state manifest: which tests flip to PASS, which remain BASELINE_FAIL or BLOCKED.
- **One-defect-per-commit is compatible with the cross-defect dependencies only if** each commit has an isolated unit oracle and the combined oracles are evaluated at defined milestones. As planned, DEF-02's acceptance cannot pass in its own commit.
- **Intermediate states produce misleading design results.**
  - After DEF-18, combinations are still unfactored.
  - Until DEF-12, web-buckling checks are grossly unconservative.
  - Until DEF-08, reports state "pass" regardless.

  No intermediate build may be used for design output. Moving DEF-08 and DEF-12 **first** makes failures visible rather than hidden during the rest of Phase 3; the plan's argument for putting DEF-08 last is backwards.
- **Vendored ospgrillage.** DEF-01 and DEF-18 patch a vendored upstream library. Keep those patches isolated (their own commits) and record them for upstream reporting.

### 6.5 Recommended order

Each step has its own isolated oracle. **Blocked items are off the critical path.**

| Step | Defects | Rationale |
|---|---|---|
| **1 (first batch)** | **DEF-12, DEF-08, DEF-11** | Pure functions or reporting, no FE coupling. Closed-form oracles (corrected). Removes the largest unconservative check and makes failures visible immediately. Low rollback risk. |
| 2 | DEF-18 | ospgrillage line/patch conservation, including the end-segment drop and the index fix; tight tolerances; asymmetric fixtures; mesh and skew variation |
| 3 | DEF-01 | Factor composition at every copy site; lane and DLA cases; ULS and SLS |
| 4 | DEF-02 | SIDL in DL; isolated oracle at γ = 1, then combined factored milestone check with steps 2–3 |
| 5 | DEF-03, then DEF-13 | Derived properties (corrected oracle; bare-steel scope stated), then densities (steel and deck) using the derived area |
| 6 | DEF-05 | Namespaced keys including terrain; Pz oracle 1039.6 N/m² for the sealed fixture |
| 7 | DEF-07 (extraction) | Section sign harmonisation, no clamp, shear included; labelled surrogate until DEC-018 |
| 8 | DEF-10 | Read-only packaged reference DB (not AppData); zero-write acceptance |
| Parallel, outside the chain | DEC-013 → DEF-14; DEC-015 → DEF-06; DEC-018 → DEF-17 | Only after the engineering owner ratifies each decision in writing |
| — | DEF-09 | No change |

---

## 7. Execution irregularities

I do not have Antigravity's activity log. The assessment below is from the artifacts.

| Irregularity | Assessment |
|---|---|
| Google API connection failure | No effect on repository, database, ledger or evidence state (IV). However, several plan values that would normally be looked up from a source are wrong: the IRC Table 12 Pz, the fatigue vehicle axles and the package versions. This is *consistent with* values being supplied without a successful lookup. All externally sourced values must be cited, or re-derived as I have done here. |
| Inspection commands exiting with code 1 | **Incomplete evidence, not a preservation breach.** The final state is intact (§2). The preservation report nevertheless contains values that no successful inspection could have produced (wrong UUID, OS edition, versions). So at least some checks in that report were not actually completed as described. |
| Initial final-preservation assertion failed (exit 1), later run succeeded | **Not a preservation concern on the evidence available.** Between my closure audit (08:35) and now, the only workspace changes are the six `phase_3` reports; the `.git` change is metadata only. A later success does not prove the earlier failing check was later satisfied for the same property. What failed, and why, must be recorded. My independent verification is the controlling preservation evidence for this gate. |

---

## 8. Acceptance-criteria weaknesses (consolidated)

1. **Numerically wrong oracles:**
   - DEF-03 (Iz −8.7%, Iy +3.1%, ȳ digits)
   - DEF-05 (1386.6 vs 1039.6 N/m²)
   - DEF-12 (63.4 vs 118.8 kN for the stated inputs)
   - DEF-17 (4-axle vehicle; 1342.5 vs 1996.4 kNm)
2. **Inconsistent fixture data:** DEF-18 / DEF-02 / DEF-13 (three different dead-load totals and widths); DEF-13 tied to the unsynchronised area.
3. **Non-isolated acceptance:** DEF-02 cannot pass without DEF-01 and DEF-18.
4. **Tolerances not justified by numerical accuracy:** 0.05% force and 0.05 m centroid; achievable accuracy is ~10⁻⁶ relative.
5. **Symmetric fixtures only.** No asymmetric, partial-length, non-uniform, skewed or multi-mesh cases.
6. **Missing negative controls and coverage:**
   - "always zero" for DEF-07;
   - "missing → pass" for DEF-08;
   - lane and DLA composition for DEF-01;
   - shear range for DEF-07;
   - terrain for DEF-05;
   - deck density for DEF-13.
7. **Element-type dependence of the DEF-03 deflection oracle** not pinned.
8. **Blocked items given acceptance numbers** (DEF-06 restraint force) before the governing decision exists.
9. **Tri-state discriminative tests (baseline / minimal-correct / naive) are asserted but not specified** for any defect. Each needs the concrete "naive fix" that must fail. Examples:
   - `mag = W*L` without the end-segment fix (DEF-18);
   - loop-only factor fix (DEF-01);
   - `Iys` → `tw/√12` with Euler stress retained (DEF-12).

---

## 9. Exact prerequisites before implementation

1. **Correct the oracles** in `PHASE_3_TEST_ACCEPTANCE_CRITERIA.md` for DEF-02, DEF-03, DEF-05, DEF-12, DEF-17 and DEF-18, using shown independent derivations. Provide **one fixture specification**:
   - span, deck width, carriageway width;
   - girder plates and derived A / I;
   - densities;
   - barrier, railing and median loads;
   - mesh densities.

   All oracles must be derived from it.
2. **Correct the fix specifications:**
   - DEF-01 factor composition (entry × case × combination; lane; DLA) at every copy site, plus the new DLA / lane latent defect;
   - DEF-18 end-segment drop and y/z index;
   - DEF-13 signature change and deck density;
   - DEF-05 terrain key;
   - DEF-07 shear, section sign harmonisation, clamp removal and surrogate labelling;
   - DEF-08 "not evaluated" state, real result keys, overall status scope;
   - DEF-10 read-only packaged reference data instead of an AppData copy (or a written justification);
   - DEF-12 boundary conditions and end-support dispersion.
3. **Replace the tolerances** with justified values (§4). Add asymmetric, non-uniform, mesh-variation and skew cases. Specify the naive-fix negative control per defect.
4. **Rebuild the DAG** per §6.1–6.5. Remove blocked DEC items from the critical path. Name the engineering owner for DEC-013, DEC-015 and DEC-018; record that ratification happens outside implementation batches.
5. **Define harness governance for Phase 3:**
   - a new active evidence phase (an `evidence_guard` change, reviewed as a harness change);
   - per-batch expected-state manifests;
   - work only on `fix/phase-3-engineering-remediation`, never on `dev`;
   - rollback by `git revert`;
   - what happens to the `weather.sqlite` preservation hash after DEF-10.
6. **Correct `PHASE_3_BASELINE_PRESERVATION_REPORT.md`** (UUID, OS edition, package versions, Phase 2.15 loss). Record what the failed (exit 1) inspection and assertion commands were.
7. **Explicit written approval from the user** to begin implementation, after the corrected plan is re-reviewed.

**Recommended first batch, once 1–7 are satisfied:** DEF-12 + DEF-08 + DEF-11 (§6.5, step 1).

---

## 10. Reproduction notes (for re-checking)

- **Source.** Fresh clone of the frozen commit `d74f56dd` into a disposable cloud directory (`/tmp/src3`). Nothing executed on the user's machine.
- **DEF-18 / DEF-01 probe.** `/tmp/p3probe/eq.py`: vendored ospgrillage only, 24 × 8.5 m orthogonal mesh, nodal load commands from `_distribute_load_types_to_model` summed for force and first moments. Results in §3.
- **Closed-form checks** (Python): DEF-03 section properties; DEF-12 IS 800 curve c (α = 0.49, γ_m0 = 1.1, E = 2 × 10⁵ MPa); DEF-17 moving-load moment envelope (0.01 m steps). Results in §3.
- **Sealed evidence read:** `testing/evidence/phase_2_13/baseline/phase_2_13_baseline_summary.json` and the 15 `tc_reg_*.log` files (read-only, seal valid).

**Phase 3 implementation is not authorized by this report.** It requires the user's explicit approval.
