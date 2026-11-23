# Phase 2.4 Final Independent Gate Audit: OsdagBridge Regression Suite

**Purpose:** decide whether Phase 2.4 resolves the findings of `reports/PHASE_2_3_FINAL_INDEPENDENT_GATE_AUDIT.md`.

**Repository:** `F:\FOSSEE internship\source\OsdagBridge` at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`, branch `dev`.

**Material examined:**
- `run_all_baseline_tests.py` (81,701 B, SHA-256 `dadb27ed…5434`) and `run_sensitivity_matrix.py` (40,973 B, `fd301cc5…a0cc`), both read in full.
- The four Phase 2.4 reports.
- All 88 files under `testing/evidence/phase_2_4/`.
- The application source and vendored ospgrillage at the baseline.

**Independent reproduction.** I ran both harnesses unchanged on a clean baseline clone in a cloud reference environment: Linux, Python 3.12, pythonocc-core 8.0.1.2, openseespy 3.8.0.0, numpy 2.5.4, Xvfb, workspace at `/tmp/ws24`. I also ran five probe scripts of my own (`/tmp/probe24a–e.py`), which monkeypatch in-process only.

Reproduction commands:
```
cd /tmp/ws24
xvfb-run -a python testing/test_cases/baseline_regression/run_sensitivity_matrix.py          # exit 0, 12/12
xvfb-run -a python testing/test_cases/baseline_regression/run_all_baseline_tests.py --mode baseline   # exit 0, 15/15 manifest
```
Nothing was run, edited, branched or committed on your machine, apart from saving this report.

**Labels:**
- Evidence: CONFIRMED (independently reproduced) / PLAUSIBLE / UNVERIFIED / CONTRADICTED.

---

## 1. Executive decision

**CONDITIONAL ACCEPTANCE.**

**Tests accepted:**
- Accepted as they stand: **A01, D01, GEO-COUNT, CAP** and **CAD** (CAD as an environment check).
- Accepted with stated limitations: **A02, B01, C01, MAT**.

**Tests rejected:**
- **EQ-LOAD-CONSERVATION (DEF-18)**
- **RPT**
- **FS**

**Tests correctly blocked:** **D02, C02, GEO-SLAB.**

**Why these three are rejected:**
- **EQ** finds a real defect, but it would raise false DEF-18 failures after correct DEF-03 or DEF-13 fixes (probe: +11.8%). It has no moment or centroid check. Its sensitivity candidate is the forbidden output normalisation: nodal loads are rescaled to hard-coded totals, and the barrier's wrong centroid survives.
- **RPT** passes an incomplete fix that checks only G1 (probe).
- **FS** rejects a legitimate writable user-data design (probe). Its candidate passes only by redirecting paths containing the test's own sandbox folder names (`'pkg_missing'`, `'project_location'`).

**"12/12 verified" is CONTRADICTED.** The candidates for EQ, C01 and FS are output normalisation, output injection and test-specific redirection respectively. C01's own test is nevertheless sound: my genuine implementation passes it (§4).

This decision accepts *tests* only. **It does not authorise any application source change.** Phase 3 planning and branch creation remain a separate, controlled step.

---

## 2. DEF-18: static load equilibrium (highest priority)

### 2.1 Independent measurement

From `/tmp/probe24b.py`. For each case, I summed the nodal loads returned by ospgrillage's `_distribute_load_types_to_model` (that is, the actual `ops.load` commands), then analysed the case alone and read the reactions at every support.

| Case | Declared load (inputs) | Σ nodal loads sent to OpenSees | Σ support reactions | x-centroid: loads → reactions | z-centroid | Loaded nodes |
|---|---|---|---|---|---|---|
| SW, 4 line loads, 1,768.9 N/m × 24 m | 169.819 kN | 169.819 kN | 169.819 kN | 12.000 → 12.000 m | 4.250 → 4.250 m | 256 |
| DD, patch 0–24 × 0–8.5 m, 6,250 N/m² | 1,275.000 kN | **1,314.375 kN** | 1,314.375 kN | 12.000 → 12.000 m | 4.250 → 4.250 m | 336 |
| 1.0 DW, same patch, 1,200 N/m² | 244.800 kN | **252.360 kN** | 252.360 kN | 12.000 → 12.000 m | 4.250 → 4.250 m | 336 |
| Crash barrier, z = 0.25 and 8.25 m, 6,540 N/m × 24 m × 2 | 313.920 kN | **196.200 kN** | 196.200 kN | **12.750** → 12.750 m (should be 12.000) | 4.250 → 4.250 m | 120 |

**Inputs (CONFIRMED from the fixture and load objects):**
- Wearing course: `typical_section.wearing_course.thickness` = 50 mm and `.density` = 24 kN/m³, giving 1.2 kN/m².
- Deck: 250 mm × 25 kN/m³ = 6.25 kN/m².
- Barrier: 6.54 kN/m, in N/m consistently throughout. The units are correct.

**Findings:**
1. **The solver is in exact equilibrium.** Reactions equal the applied nodal loads to machine precision, in both force and moment centroid. **The defect is entirely in the load-to-node distribution step**, before OpenSees. CONFIRMED.
2. **Deck and DW are over-integrated by 3.09%.**
   - 1,314.375 / 6.25 = **210.30 m²** effective, against 24 × 8.5 = **204.00 m²**. The report's 210.3 / 204.0 figures are CONFIRMED.
   - I did not trace the attribution to "polygon tributary integration" in `_assign_patch_load` line by line. It is PLAUSIBLE.
3. **Barrier load is under-distributed by 37.5%** (equivalent to 30 m of the 96 m of barrier line), **and its applied centroid is shifted 0.75 m along the span.** The missing load is therefore unevenly distributed, which distorts moments and shears, not only the total. This moment-equilibrium error is **new** and is not in the report. CONFIRMED.

### 2.2 Is the 0.5% tolerance justified?

- A correct lumping scheme, whether consistent or tributary, conserves the total force **exactly** (to floating point). The measured solver residual here is about 0. Mesh discretisation changes *where* load goes, not *how much*.
- So 0.5% is not a discretisation allowance. It is a loose engineering margin: it would allow about 6.4 kN of lost or added deck load. A relative tolerance near 10⁻⁶ on the nodal-load sum is achievable.
- **More importantly, the test checks totals only.** Distributions that conserve the total but misplace the load, like the barrier's 12.75 m centroid, pass.

### 2.3 Test design defects

| Issue | Evidence |
|---|---|
| **The declared loads are hard-coded constants that duplicate other defects** | `P_applied_SW = 4 × 24 × (0.0225344 × 78.5)` uses the *preliminary* area (DEF-03) and the *hard-coded* density (DEF-13). Deck width 8.5 m, 0.25 m slab, 25 kN/m³, 0.05 × 24 and 6.54 kN/m are also literals. |
| **Correct fixes elsewhere cause false DEF-18 failures** | Probe P2: after only a correct DEF-03 section fix (load still conserved), EQ reports "SW applied 169.8 kN vs reaction 189.8 kN (+11.8%)", **BASELINE_FAIL**. A DEF-13 fix with the fixture density 76.4 would likewise give 165.3 against 169.8 kN (−2.7%). |
| No moment or centroid assertion | The barrier's 0.75 m centroid shift is undetected. |

### 2.4 Candidate (b): rejected

`mut_b_eq_load_conservation` wraps `_distribute_load_types_to_model`, **recognises the case by its magic total** (`abs(total_fy − 1314375.0) < 100`, `252360.0`, `196200.0`), and multiplies every nodal load by `target / total`.

This is exactly the artificial normalisation the brief prohibits:
- **It doesn't correct the distribution mathematics.** Probe P1b: under candidate (b), the barrier total becomes 313.92 kN but the **centroid stays at 12.750 m**.
- It works only for these exact loads.

(c) is the same normalisation with the barrier left out. **EQ sensitivity: NOT DEMONSTRATED.**

### 2.5 Is DEF-18 isolated from A02?

Yes, appropriately:
- A02 now builds its target from component reactions measured at run time and checks the *superposition identity*.
- EQ checks *conservation against the declared loads*.

These are different, independent oracles. A distribution fix moves both sides of A02's identity equally, so A02 is not affected by DEF-18. EQ itself, however, is coupled to DEF-03 and DEF-13 (§2.3).

**EQ verdict: REJECTED.** The test as written; the defect itself is CONFIRMED and real.

---

## 3. A02: load combinations

- **The two figures are now separated correctly:**
  - **2,710.17 kN** = 1.35 × (169.82 + 1,314.38 + 196.20) + 1.75 × 252.36. This is a *superposition target* built at run time from component reactions (runner lines 625–641). It deliberately depends on the model's own reactions, but it tests only that BASIC_1 equals Σ γᵢRᵢ for whatever the model applies. That is a valid linearity identity, independent of DEF-18.
  - **2,802.70 kN** is logged as the theoretical applied resultant and is **not asserted**. Equilibrium is delegated to EQ. Acceptable.
- **BASIC_1 isolation:** `analyze(load_case=b1_name)` filters to that case; state reset was verified in Phase 2.3.
- **Baseline:** 1,736.55 kN = 1,484.19 (1.0 DL) + 252.36 (1.0 DW), which is unfactored. Element Vy error against the unfactored sum is about 10⁻⁷ N, and 72,392 N against the factored sum, so DEF-01 is detected (reproduced). The barrier contribution is about 0, so DEF-02 is detected.
- **Candidate (b) is a production-equivalent fix:** upstream `line_end_point` and patch-interpolator fixes, copy scaling in `add_load`, and SIDL built before DL via the production helpers. There is no re-ordering, injection or `__eq__` patch (CONFIRMED). It passes. (c), with the barrier omitted, fails.

**Limitations:**
- Component case names are literals (`"SW"`, `"DD"`, `"Crash barrier load"`, `"1.0 DW"`). An exception sets a component to 0.0. That fails safe for the barrier check, but obscures the cause.
- The internal-force superposition covers only Vy_i and Mz_i, and only against "1.0 DL" + "1.0 DW".
- The SIDL factor of 1.35 still needs ratification (IRC 6 Annex B).

**Verdict: ACCEPTED WITH LIMITATIONS.**

---

## 4. C01: fatigue stress range and DCR

- **Production path:** the real `_extract_demands_from_analysis_results`, both paths, on synthetic xarray force histories (envelope at `designer.py:2970–2988`; per-load-case at `:3082`). Only `classify_loadcases` and `build_girders` are mocked.
  - Static case expected 0: baseline gives 125.46 MPa (envelope) and 62.73 MPa (per-LC).
  - Cyclic case expected 62.729 MPa on both paths.
- **Capacity:** now taken from the application's `IRC22CapacityCalculator.compute_fatigue()`. Independent recalculation from the actual inputs (`FatigueConfig(Nsc = 2,000,000, welded, ffn = 92, tfn = 59)`, γ<sub>mft</sub> = 1.35, t<sub>p</sub> = 18 mm so μ<sub>r</sub> = 1):

  | Quantity | Formula | Value |
  |---|---|---|
  | f<sub>f</sub> | 92 × (5×10⁶ / 2×10⁶)^(1/3) | **124.863 MPa** |
  | f<sub>fd</sub> | μ<sub>r</sub>·f<sub>f</sub>/γ<sub>mft</sub> = 124.863 / 1.35 | **92.491 MPa** |
  | DCR | 62.729 / 92.491 | **0.6782** |

  All CONFIRMED.
  - Caveat 1: the log text says "Nsc = 5,000,000"; **the actual N<sub>sc</sub> is 2,000,000**.
  - Caveat 2: `fat_cap.get("f_fd_eff_MPa", 92.491)` silently falls back to a constant.
  - Caveat 3: the DCR division is done by the test. The application's own per-girder fatigue check is not read.
  - Caveat 4: the sign companion is a 2D OpenSees beam, not ospgrillage 3D. PLAUSIBLE.
- **The harness candidate is rejected.** `mut_b_c01` still overwrites the ranges with 0.0 or **62.729** by load-case count (sensitivity script lines 323–338).
- **Independent sensitivity (`/tmp/probe24e.py`):** I wrote a genuine, sign-consistent implementation. Section moment = −Mz<sub>i</sub> or +Mz<sub>j</sub> per element end; range = max − min over cases at each location; the governing value goes to both paths. **It PASSES**, giving 62.728 MPa and DCR 0.6782. The harness's own (c), which fixes the envelope only, FAILs.

**Verdict: ACCEPTED WITH LIMITATIONS.** The sensitivity is established by my probe, not by the harness.

---

## 5. C02, D02 and GEO-SLAB: blocked

- **C02 / DEC-018:**
  - The test returns BLOCKED unconditionally. The matrix records (b) and (c) as BLOCKED with `sensitivity_verified = false`, and no synthetic candidate is used (CONFIRMED).
  - The blocking premise is accurate. The vendored `create_fatigue_vehicle()` exists. `cl_204_6_fatigue_load` and `KEY_LL_IRC_CLASS_FATIGUE` are not consumed by the analysis. `designer.py` takes fatigue ranges only from SLS_FREQUENT. So no production path exists to specify a correct oracle against.
  - Note: the test now carries the defect ID **"DEF-08 / DEF-17"**, but DEF-08 is the executive-summary defect. **DEF-17 remains open** and must not be reported as resolved.
- **D02 (DEC-015) and GEO-SLAB (DEC-013):** unconditionally BLOCKED, with no candidates and not counted.
- All three decisions still need ratification by an engineering authority.

---

## 6. B01: section synchronisation

- **What the test checks:** the solver-consumed `girder_sections` (all must have I<sub>z</sub> ≥ 0.0078 and A ≥ 0.024), D = d<sub>w</sub> + 2t<sub>f</sub>, and a 100 kN deflection probe.
  - Baseline: 7.40% / 10.55% gaps and **7.816 mm**, reproduced.
  - The metadata-only (c) candidate stays at 7.816 mm and FAILs. **The test detects real solver-side synchronisation.**
- **The references are now labelled honestly:**
  - single beam: 100×10³ × 24³ / (48 × 2×10¹¹ × 0.00792758) = **18.164 mm** (CONFIRMED);
  - grillage: 7.218 mm, "calibrated".
- **Does 7.218 mm have an independent basis? No.** It is the output of the same grillage model run with the candidate's hard-coded section. That makes it a model-consistency reference, not an independent engineering oracle. The cross-check 7.816 / 7.218 = 1.083 against an I<sub>z</sub> ratio of 1.080 (0.3%) supports it only to that extent.
- **The candidate** still hard-codes the section constants. Its I<sub>y</sub> = 0.0002734 and J = 1.45×10⁻⁶ are invented; I<sub>y</sub> from the plates would be about 0.000207.

**Verdict: ACCEPTED WITH LIMITATIONS.**

---

## 7. RPT: executive summary

- **What improved:** every non-EB girder (G1–G6) is now replaced with the same controlled checks, so a partial override can no longer manufacture an all-pass result. The schemas match what `executive_summary.py` parses (`_max_member_efficiency`, `ur_*`). Fatigue failure is included (DCR 1.9746). The mirror all-pass scenario works.
- **Gap (probe, `/tmp/probe24d.py`):** an **incomplete fix that inspects only G1 PASSES all six scenarios.** Every scenario sets *all* girders identically, so a single-girder failure (for example G3 only, as in Phase 1D's governing G3/G4) is never tested.
- **Not asserted:** that the summary agrees with the application's own `overall_design_status`.
- **The candidate** is still a text post-processor that replaces the hard-coded block.

**Verdict: REJECTED.** Add single-girder and edge-girder failure scenarios and an agreement check with `overall_design_status`.

---

## 8. MAT: material density

- **What the test does:** it uses the real production key `material.girder.density` = 70.0 (the fixture value is 76.4) and the production `add_dead_loads()`.
- **Expected self-weight:** Σ A(girder_sections) × ρ × L.
  - Units: m² × kN/m³ × m = kN.
  - Expected at 70: 4 × 0.0225344 × 70 × 24 = **151.43 kN**.
  - Baseline: **169.82 kN**, which equals the 78.5 value. The test rejects the 78.5 database default and hard-coded constant, and an unused-key fix (CONFIRMED).
- **Limitations:**
  - The naive (c) candidate is identical to the baseline.
  - The expected value uses the same `girder_sections` areas the analysis uses. That is appropriate, and it keeps the test independent of DEF-03.

**Verdict: ACCEPTED WITH LIMITATIONS.**

---

## 9. FS: filesystem behaviour

**Production path (CONFIRMED):** `_with_db` → `Database(DB_PATH).connect()`. `connect()` creates the file, and runs `schema.sql`, if the file is missing or `stations` is absent (`database.py:19–30`).

**What the test does:**
- **Test A** runs production `get_state_list` and `get_weather` against a sandbox copy of the package directory, comparing before/after hashes. That is genuine.
- **But its result depends on the untracked `weather.sqlite` in the developer checkout:**
  - On your machine the sandbox contains it (180,224 B from Phase 1D), so Test A shows *no* mutation.
  - In a clean clone it doesn't exist, so Test A shows *mutation*. My reproduction confirmed this.
  - The baseline outcome therefore depends on a stale local artefact.
- **Test B** calls `Database(explicit_path).connect()` on a missing file and treats file creation as a package write. Any database class honouring an explicit path will create the file there, including the correct design: an anchored, writable user-data database.
  - **Probe:** production `DB_PATH` set to a user-data directory, the default constructor anchored there, explicit paths honoured → **BASELINE_FAIL**, "Database.connect() writes weather.sqlite inside package tree when missing".
- **Not tested:** a writable user-data path, or a read-only packaged database (no read-only permission is set).

**Candidate (b) is test-specific:** `patched_init` redirects any path containing **`'pkg_missing'` or `'project_location'`**. Those are the test's own sandbox folder names. This is a test-specific monkeypatch and must be rejected.

**Verdict: REJECTED.** Classification: filesystem / packaging / reproducibility, not engineering.

---

## 10. Remaining tests

- **A01:** unchanged from Phase 2.3. Covers line and patch loads, and the stock-`apply_load_factor` fix fails (ratio 1.214, Phase 2.3 probe). The candidate is genuine. Ownership: an upstream-originated defect in OsdagBridge's modified vendored ospgrillage fork. **ACCEPTED.**
- **D01:** genuine candidate; all four UI keys. **ACCEPTED.**
- **GEO-COUNT:** genuine candidate; the naive case (n = 0) is trivial. **ACCEPTED.**
- **CAP:** dual geometry, 63.40 / 158.50 kN (reproduced in Phase 2.3). The candidate uses the application's IS 800 helpers. Squash and clamp fail; the ±15% tolerance is curve-insensitive (stated). **ACCEPTED.**
- **CAD:** an environment check of OCC `ExportToImage`, not the application's `_export_cad_figures`. **ACCEPTED as environment verification.**

---

## 11. Evidence integrity

| Check | Finding | Status |
|---|---|---|
| Sequence | Runner edited 15:24:22; sensitivity script 15:34:28; sensitivity run 15:34:38–15:36:54; **baseline run 15:37:23–15:37:48 (after)**; reports 15:39–15:42 | CONFIRMED |
| Separation | `baseline/` (17 files), `sensitivity/` (17), `candidates/` (54: (a), (b) and (c) copies for 12 actionable and 1 environment test, (a) only for 3 blocked). Baseline is not polluted by candidates. | CONFIRMED |
| 88 files | 88 files present (17 + 17 + 54) | CONFIRMED |
| Manifest hashes | **All 34 full SHA-256 entries match** (baseline and sensitivity). Of the 42 truncated candidate-log hashes, **13 do NOT match** the files present: CAD (a, b, c), CAP (a, b, c), D01 (a, b, c), D02 (a), EQ (a, b, c). Example: CAD (a) is listed as `a807cb9d…` but is actually `96039691…`. The manifest was evidently compiled from a different run for those entries. | **Partly CONTRADICTED** |
| Runner provenance | The summary's `runner_self_hash` = `dadb27ed…` = the current runner. Fixture hashes match. Candidate function hashes are recorded in the sensitivity JSON. | CONFIRMED |
| Environment | `osdagbridge-py312`, Python 3.12.16, OCC 8.0.1, OpenSeesPy 3.8.0.0, numpy 2.5.5, scipy 1.18.1, xarray 2026.9.0. "ospgrillage 0.6.0" is the vendored copy's version string. | CONFIRMED |
| stdout / stderr | **No console transcripts exist** for Phase 2.4 (Phase 2.3 had them). | Regression |
| Exit codes | `baseline_exit_code.txt` = 0 (manifest alignment, not an application pass) and `sensitivity_exit_code.txt` = 0 are self-written by the scripts. My reproduction: both processes exited 0. | Consistent; not separately captured |
| Prior evidence | **Five Phase 2.3 archive files were overwritten during Phase 2.4 work** (15:28–15:29 UTC): `testing/evidence/phase_2_3/candidates/tc_reg_{a02,c01,fs,mat,rpt}*.log`, with timestamps inside the files of 15:28–15:29. The Phase 2.3 evidence set is no longer pristine. | **Integrity loss** |
| `testing/fixtures/` | still absent | Unchanged |

---

## 12. Test-by-test table

| Test ID | Phase 2.3 finding | Phase 2.4 claimed correction | Independent reproduction | Remaining concern | Final verdict |
|---|---|---|---|---|---|
| A01 | Resolved in 2.3 | Unchanged | Baseline 1.00000 ratio; (b) PASS, (c) FAIL | none material | **ACCEPTED** |
| B01 | "Hand oracle" 7.218 false | Relabelled: 18.164 single beam, 7.218 calibrated | 7.816 mm baseline; metadata swap FAILs | 7.218 is self-calibrated; candidate constants invented | **ACCEPTED WITH LIMITATIONS** |
| C01 | Candidate injects ranges; DCR from unsourced 31.77 | Capacity from `compute_fatigue()` | f<sub>fd</sub> 92.491 MPa and DCR 0.6782 recomputed; **my genuine implementation PASSES** | Harness candidate still injects 62.729; N<sub>sc</sub> label wrong; silent 92.491 fallback | **ACCEPTED WITH LIMITATIONS** |
| A02 | Oracle absorbed DEF-18 | Run-time superposition; 2,802.70 informational | 1,736.55 against 2,710.17 kN; factor drop and barrier absence detected; (b) genuine PASS | Literal case names; SIDL factor ratification | **ACCEPTED WITH LIMITATIONS** |
| EQ (DEF-18) | Defect unregistered | New conservation test, 0.5% | Defect CONFIRMED at the nodal-load level (deck +3.09%, DW +3.09%, barrier −37.5%, barrier centroid +0.75 m) | Hard-coded declared loads coupled to DEF-03/13 (false fail +11.8%); no moment check; candidate is normalisation by magic totals | **REJECTED** |
| D01 | Valid | Unchanged | (b) PASS, (c) FAIL | — | **ACCEPTED** |
| D02 | Blocked | Blocked (DEC-015) | BLOCKED; not counted | Ratification | **BLOCKED** |
| C02 | Local-coordinate placement; false "utilisation linked" | Blocked (DEC-018) | BLOCKED; no synthetic candidate | Defect ID mislabelled "DEF-08 / DEF-17"; DEF-17 stays open | **BLOCKED** |
| RPT | "All Pass" contained failing G2–G6 | All girders sanitised | All 6 scenarios behave; **a G1-only fix PASSES** | No single-girder failure scenario; no agreement with `overall_design_status` | **REJECTED** |
| GEO-COUNT | Valid | Unchanged | (b) PASS | weak naive case | **ACCEPTED** |
| GEO-SLAB | Blocked | Blocked (DEC-013) | BLOCKED | Ratification | **BLOCKED** |
| CAP | Valid | Unchanged | 63.40 / 158.50 kN; squash and clamp fail | ±15% curve-insensitive | **ACCEPTED** |
| MAT | Invented key | Real `material.girder.density` | 169.82 against 151.43 kN; rejects 78.5 | Naive candidate = baseline | **ACCEPTED WITH LIMITATIONS** |
| FS | Hashes not compared; string check | Production `_with_db` in sandbox; observed effects | Baseline FAIL reproduced; **legitimate user-data design FAILs**; outcome depends on the untracked `weather.sqlite` | Test B contradicts a correct design; candidate keyed on sandbox names | **REJECTED** |
| CAD | Valid (environment) | Unchanged | PASS; blank image FAILs | not the application path | **ACCEPTED** (environment verification) |

---

## 13. Mandatory corrections before full acceptance

1. **EQ:**
   - Compute each declared load at run time from the load objects' own definitions and the input dictionary: patch area × intensity, line length × intensity, and Σ A × ρ × L from `girder_sections` and the input density. Do not use literals.
   - Add moment-equilibrium (centroid) assertions in x and z.
   - Tighten the tolerance, for example 0.01% on the nodal-load sum.
   - Replace the candidate with one that corrects `_assign_patch_load` / line-load segment integration, or leave the test without a demonstrated candidate. Do not use normalisation.
2. **RPT:** add scenarios where exactly one girder fails (an interior and an edge girder). Assert agreement with the application's `overall_design_status`. Move the candidate logic inside `executive_summary`.
3. **FS:** drop Test B's premise that creating a file at an explicit path is a defect. Instead:
   - assert that no file is created or changed under the *package* tree by production calls, starting from a clean package copy with and without the database present;
   - assert that the default and production paths resolve outside the package and are writable;
   - add a read-only package scenario.

   Replace the sandbox-name-keyed candidate.
4. **C01:** replace the injecting harness candidate with a genuine implementation, such as the one in `/tmp/probe24e.py`. Correct the N<sub>sc</sub> log label. Make a missing `f_fd_eff_MPa` key fail the test.
5. **Evidence:**
   - Regenerate the manifest so all 88 hashes match.
   - Restore the console transcripts and the shell's own exit status.
   - Stop writing into `phase_2_3/` and record that 5 of its files were overwritten.
   - Create `testing/fixtures/` or stop referring to it.
6. **Defect register:** keep DEF-17 open and correct C02's defect label. Add the barrier-centroid finding to DEF-18.
7. **Governance:** obtain ratification of DEC-013, DEC-014, DEC-015 and DEC-018 and of the SIDL factor.

---

## 14. Repository status verification

| Check | Result |
|---|---|
| `.git/HEAD` | `ref: refs/heads/dev` → `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` |
| Branches | only `dev` under `.git/refs/heads/`; no Phase 3 branch |
| Lock files and index | none; `.git/index` mtime 2026-11-15 12:26:18 UTC, unchanged since before Phase 2 |
| Source content | The aggregate SHA-256 of all 282 non-ignored files under `src/` (CR-normalised) is `c6d61d03798281dd0571762aff5506cdfdbd5cbbf25e5f484d554529a0bda89d`, **identical to the clean baseline clone** and to every previous audit. No source file changed after 14:30 UTC. |
| Databases | `Intg_osdag.sqlite` `25f97857…`, byte-identical. Untracked `weather.sqlite` `1d767658…`, mtime 05:48 UTC, unchanged. |
| Workspace-only changes | the harness scripts, `phase_2_4/` evidence, four reports, `CHANGELOG.md`, `DECISIONS.md`, `PROGRESS.md`, `documentation/PHASE_1D_DEFECT_REGISTER.md`, and five overwritten `phase_2_3/candidates/*.log` files. My Phase 2.3 audit is byte-identical to what I wrote (`00ed39d0…`). |

**The application repository remains unchanged at the frozen baseline.** I made no fixes.

---

## Decision

**CONDITIONAL ACCEPTANCE**

- **Accepted:** A01, D01, GEO-COUNT, CAP and CAD (environment check); A02, B01, C01 and MAT with the limitations stated above.
- **Rejected; corrections in §13 mandatory:** EQ-LOAD-CONSERVATION, RPT, FS.
- **Blocked:** D02, C02, GEO-SLAB.

This decision accepts tests only. It does not authorise any application source modification.
