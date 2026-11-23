# Phase 2.5 Final Independent Gate Audit: OsdagBridge Regression Suite

**Auditor role:** independent QA and structural-verification audit, by the same auditor as Phase 2.4.

**Date:** 2026-11-16

**Repository:** `F:\FOSSEE internship\source\OsdagBridge`, branch `dev`, frozen baseline `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`.

**Controlling document:** `reports\PHASE_2_4_FINAL_INDEPENDENT_GATE_AUDIT.md`, SHA-256 `496ca7ce…`. It is unchanged since I wrote it.

**Material examined:**
- `run_all_baseline_tests.py` (91,192 B, `e09a82c9…`) and `run_sensitivity_matrix.py` (48,054 B, `9fb37f80…`), both read in full.
- All five Phase 2.5 reports.
- All 94 files under `testing\evidence\phase_2_5\`.
- The application source at the baseline commit.

**Evidence labels:**
- **CONFIRMED:** independently reproduced.
- **PLAUSIBLE:** consistent with the evidence but not reproduced.
- **CONTRADICTED:** independent evidence disagrees with the claim.
- **MISSING:** the evidence does not exist.

---

## 0. Reproduction method

**Environment:**
- A clean checkout of `d74f56d` into an isolated cloud workspace (`/tmp/ws25`), with the Phase 2.5 scripts copied in byte-for-byte.
- Phase 1D fixtures: input `31ae62dc…0191`, output `429a3198…a5ab`.
- Linux, Python 3.12, pythonocc-core 8.0.1.2, openseespy 3.8.0.0, numpy 2.5.4, Xvfb.

Commands, run unmodified:
```
cd /tmp/ws25
xvfb-run -a python testing/test_cases/baseline_regression/run_sensitivity_matrix.py              # exit 0, 12/12 "VERIFIED"
xvfb-run -a python testing/test_cases/baseline_regression/run_all_baseline_tests.py --mode baseline   # exit 0, 15/15 manifest match
```

**Results:**
- Per-test statuses and diagnostic values match the evidence on your machine. Examples:
  - EQ: DD +39.375 kN, DW +7.560 kN, barrier −117.720 kN, barrier centroid shift Δx = +0.750 m.
  - A02: 1,736.6 kN against 2,710.2 kN.
  - B01: 7.816 mm baseline, 7.239 mm for candidate (b).
- Baseline reproduction: **CONFIRMED**.

**Adversarial probes:**
- Scripts `/tmp/p25/probe25a…e.py`: in-process monkeypatching only, in the cloud workspace, with nothing run on your machine.
- They drive the real test functions with mutated implementations (§1–§6).

**What the exit codes mean:**
- Exit code 0 from either harness means only that the manifest aligned, or that the matrix ran.
- It is not taken as evidence of correctness anywhere in this audit.

---

## 1. Priority 1: EQ-LOAD-CONSERVATION (DEF-18)

### 1.1 Defect

**Reproduced exactly:**

| Case | Declared | Distributed to nodes and reacted | Error | Reaction centroid (x, z) |
|---|---|---|---|---|
| DD | 1,275.000 kN | 1,314.375 kN | +3.09% | 12.000, 4.250 |
| 1.0 DW | 244.800 kN | 252.360 kN | +3.09% | 12.000, 4.250 |
| Barrier | 313.920 kN | 196.200 kN | −37.50% | **12.750**, 4.250 |
| SW | 169.819 kN | 169.819 kN | 0 | 12.000, 4.250 |

The defect is real and is located in the load-distribution step, not the solver. **CONFIRMED.**

### 1.2 Candidate (b): mathematical check

The candidate implements `_distribute_patch_load_fem` and `_distribute_line_load_fem`, at `run_sensitivity_matrix.py` lines 501–586.

**How it works:**
- For each mesh cell [x₁,x₂]×[z₁,z₂], it intersects the cell with the patch to get R = [max(x_min,x₁), min(x_max,x₂)] × [max(z_min,z₁), min(z_max,z₂)].
- It sets F = q·|R|.
- It assigns F·Nₐ(ξ_c, η_c) to the four corner nodes. Here Nₐ are the bilinear shape functions, evaluated at the centroid of R.

**Exactness for uniform q.** For each node, the consistent nodal load is fₐ = ∫_R q·Nₐ dA.
- Nₐ = ½(1±ξ)·½(1±η) is a product of functions that are linear in x and in z separately.
- On a rectangle, the integral of such a product is |R| times its value at the centroid (each linear factor averages to its midpoint value).
- So fₐ = q·|R|·Nₐ(centroid), which is exactly what the code computes.

**Consequences:**
- **Force:** ΣNₐ = 1, so Σfₐ = q·|R| for every cell, and the total equals q × patch area.
- **First moments:** bilinear interpolation reproduces linear fields (ΣNₐxₐ = x, ΣNₐzₐ = z), so Σfₐxₐ = ∫q·x dA. The same holds in z.
- **Boundary cells:** these are handled by the clipping to R. The probe that drops the first node column is detected (DD 1,235.16 kN, x̄ = 12.387 m).
- **Line loads:** the same construction in one dimension, with η fixed by z_line.

**Conclusion:** candidate (b) is a **physically valid consistent-load distributor, not a normalisation**. It contains no magic totals, no rescaling and no reference to expected values. **CONFIRMED.**

**Limitations of the candidate itself:**
- It assumes an orthogonal tensor mesh. Node lookup by rounded (x, z) raises `KeyError` on skewed meshes.
- It uses a single intensity, `pts[0].p`, so it cannot handle varying patch intensity.
- Loads outside the mesh are dropped silently.
- In a mixed load case, its `else: orig_dist(self, load_case_obj)` branch would redistribute the entire case once for each non-matching load group.
- The docstring is inaccurate: it says collinear SW lines use beam element loads, but in practice they also go through the line distributor. The result is still exact.

### 1.3 The test: adversarial probes

From `/tmp/p25/probe25a.py`. Every mutant except M1 and M6 conserves total force exactly.

| Probe | What the distribution does wrong | Test result | Correct? |
|---|---|---|---|
| M0 | Nothing: candidate (b) as written | PASS | ✓ |
| M1 | Drops the first longitudinal node column (missing boundary cells) | BASELINE_FAIL (DD −3.1%, x̄ 12.387) | ✓ detected |
| **M2** | **Equal nodal lumping**: every patch node gets the same share, ignoring tributary area | **PASS** | ✗ |
| **M3** | **Wrong mesh dimensions**: assumes uniform transverse spacing on the non-uniform mesh z = [0, 1.05, 3.183, 5.317, 7.45, 8.5] | **PASS** | ✗ |
| **M4** | **Barrier lines moved 0.80 m inboard** (from z = 0.25/8.25 to 1.05/7.45) | **PASS** | ✗ |
| **M5** | **Both barrier lines placed on the centreline**, z = 4.25 | **PASS** | ✗ |
| M6 | Barrier shifted 1.5 m longitudinally | BASELINE_FAIL (x̄ 13.453) | ✓ |
| M7 | Correct distributor plus the DEF-03 section fix (A = 0.025192 m²) | PASS (SW 189.85 kN, both sides) | ✓ coupling to DEF-03 removed |
| **M8** | Correct distributor plus a DEF-13 density fix (input 76.4 kN/m³) | **BASELINE_FAIL**: SW 165.28 kN reacted against 169.82 kN "declared" (−2.7%) | ✗ false failure |
| M9 | Correct distributor, but the application builds the deck load with a wrong slab thickness (0.20 m) | PASS (DD 1,020 kN declared and reacted) | out of scope (see below) |

**Why M2–M5 pass:**
- The test checks only the *total* force and the *whole-case* first-moment centroid.
- Both barrier lines are in one case, symmetric about z = 4.25, and the mesh is symmetric. Any symmetric misplacement of load therefore keeps x̄ = 12.000 and z̄ = 4.250.
- The z-centroid check is structurally blind to transverse barrier position: its expected value, 4.25 m, is the same as the deck's.

The brief requires the test to reject plausible incorrect distributions whose totals match. **It does not.**

**Why M8 fails falsely:**
- The declared self-weight uses `bridge.material_props.steel_prop.rho / 1000`, which is **78.5**. It does not use the user's `material.girder.density`, which is 76.4 in the fixture.
- Probe output: "EQ oracle density source: … = 78.5 | fixture material.girder.density = 76.4".
- So EQ remains coupled to DEF-13. A correct DEF-13 fix would be reported as a DEF-18 regression.

**M9 is a scope note, not a defect.**
- The report says expected loads are "dynamically computed directly from model inputs".
- In the code (runner lines 788–847), they are read from the application's own `PatchLoading` and `LineLoading` objects, not from the input dictionary.
- That is adequate for conservation, but it means EQ cannot detect a wrong load intensity, and the report's wording overstates this.

**Other observations:**
- Silent literal fallbacks remain: `24.0*8.5*0.25*25.0`, `24.0*8.5*0.050*24.0` and `48.0*6.54` at lines 797–799, 818–820 and 845–847, plus `78.5` and `4.25`. They are used if a load case is not found.
- Reactions are summed as `abs(nodeReaction)` (lines 869–873), which would hide any uplift reaction.
- The tolerance has been tightened to 0.05% on force and 0.05 m on centroids, which is appropriate.

### 1.4 Verdict

- **Test: REJECTED.**
- **Defect: CONFIRMED.**
- **Candidate (b): genuine.**

**Mandatory corrections:**
- Check the centroid of each load group: each barrier line separately, at its own z.
- Check the transverse distribution, for example the share of each load reaching each longitudinal line, against tributary-width expectations. Alternatively, compare the nodal load vector against an independently computed consistent vector.
- Derive the declared self-weight from `material.girder.density`.
- Remove the literal fallbacks.

---

## 2. Priority 2: RPT executive-summary status (DEF-08)

**Test structure:**
- Seven scenarios: S1 all-pass, S2A G3 fails, S2B G1 fails, S3 cross bracing, S4 end diaphragm, S5 deck, S6 G3 plus deck.
- Girder failures are always G1 (a moment check) or G3 (a fatigue check, DCR 1.9746).

**Probe results** (`/tmp/p25/probe25b.py`, `probe25b2.py`):

| Probe | Result |
|---|---|
| **Candidate (b), restricted to inspecting only G1 and G3** | **PASS** (all 7 scenarios). Brief: "reject a candidate that only checks selected girders." Not achieved. |
| Candidate (b), using the `status` string only (ignoring DCR) | PASS. The test never presents a DCR > 1 failure labelled `PASS`. |
| A candidate that uses the application's own `design_results['overall_status']` | **BASELINE_FAIL in S1**. The fixture keeps the snapshot value `"FAIL"` even in the all-pass scenario, so a fix that defers to the designer's verdict is rejected falsely. |
| Candidate (b) on 24 independent single failures (G1–G6 × moment / shear / stiffener / fatigue) | Narrative correct in 24 of 24; table correct in 24 of 24. The baseline narrative is wrong in 24 of 24. |
| A failure where status says `PASS` but DCR = 1.30 (G5 shear), under candidate (b) | Reported as FAIL. Correct. |
| Cross bracing, end diaphragm or deck failing alone | The table "Overall Design Status" shows **"Pass"** in all three. `executive_summary.py:77` computes the overall status from **girder checks only**, and the test does not assert the table in S3–S5. |

**Candidate (b):**
- It derives status from the result dictionaries, not from scenario names. That is acceptable.
- It is identical to the Phase 2.4 candidate, despite the report describing changes. Its function source is byte-identical apart from directory names.
- It is still a text post-processor wrapped around `executive_summary`.

**Verdict: REJECTED.**

**Mandatory corrections:**
- Inject a failure into each girder, G1–G6, independently. A parametrised loop is enough.
- Include a DCR-only failure.
- Assert the table in every scenario, and decide and document whether the overall status should include non-girder components.
- Keep `design_results.overall_status` consistent with the injected state.

---

## 3. Priority 3: FS filesystem behaviour (DEF-10)

**What the test actually does** (runner lines 1524–1624):

| Claimed check | Implementation | Assessment |
|---|---|---|
| 1. DB_PATH anchored outside the package and writable | `commonpath` comparison and `os.access(dir, W_OK)` | real but minimal |
| 2. `Database()` default anchored | `db_name == "weather.sqlite"` or dirname == cwd | attribute and string check |
| 3. No package mutation during production queries | Hashes the **top level of `core/data/project_location/` only**, before and after `get_state_list` and `get_weather`. **Query exceptions are caught and logged; results are never asserted.** | partial |
| 4. Clean package without the database | `wrote_inside_clean_pkg = prod_db_in_package`, a **copy of Check 1** | **not a test** |
| 5. Read-only package resilience | `ro_package_vulnerable = prod_db_in_package or not prod_dir_writable`. **No `chmod`, no read-only attribute, no OS permission change anywhere in the test** (grep: only line 1545 uses `os.access`) | **not a test** |

**Probes** (`/tmp/p25/probe25c.py`, `probe25c2.py`):
- **F1:** candidate (b), starting from a brand-new user-data location, **PASSes**, and production queries genuinely work: 31 states; Ahmednagar weather returned. `Database.connect()` seeds the new database from `schema.sql` (180,224 B). The candidate is functionally sound.
- **F2:** candidate (b), plus a production call that **writes files into the package** at `core/data/project_location/shapefiles/_index_cache.tmp` and `core/data/ResourceFiles/_weather_cache.tmp`, still **PASSes**, because only one directory level is monitored.
- **The test writes into the application repository.** In a clean checkout, without the untracked `weather.sqlite`, the condition (a) and baseline runs execute production queries against the real source tree. **This created `src/osdagbridge/core/data/project_location/weather.sqlite` in my clean clone.** It reproduced on two runs.
  - On your machine the untracked file already exists (mtime 05:48 UTC, unchanged), so no new file appeared.
  - Check 3's outcome therefore still depends on whether that untracked file is present: "mutated" is True in a clean clone and False on your machine.
- The dependence on folder names has been removed. **CONFIRMED.**

**Verdict: REJECTED.**

**Mandatory corrections:**
- Run production calls against a **copy** of the package, never the real source tree.
- Make the read-only scenario real: OS permissions on that copy (Windows read-only attribute or ACL, POSIX `chmod`, run without root).
- Hash the package tree recursively.
- Assert the query results.
- Delete Checks 4 and 5, or implement them as real experiments.

---

## 4. Priority 4: B01 section synchronisation (DEF-03)

**Valid parts:**
- The D = d<sub>w</sub> + 2t<sub>f</sub> consistency check.
- The solver-side `girder_sections` I<sub>z</sub> and A checks.
- Detection of a candidate that only changes metadata (c).

**The deflection oracle (7.218 mm ± 3%) is not independent, and the stated bounds are wrong for this load.**

The probe load is 100 kN at x = 12 m, **z = 1.05 m**, which is girder G1, an *edge* girder. The tested quantity is `max|dy|` over all nodes.

**B5 probe findings:**
1. **The measured maximum is not under the load.** It is at the **overhang edge line, z = 0** (7.239 mm). Under the load at z = 1.05 m the deflection is 6.213 mm.
2. **The edge lines are modelled as full steel girders.** The two overhang edge lines (z = 0 and 8.5 m) carry the full girder section: `edge_longitudinal=self._girder_section()` at `plategirderbridge.py:1115`. The grillage is therefore a **six-girder** system, while DEF-11 states the bridge has four girders.
3. **The 7.218 mm target is a rigid-deck (Courbon) result for that six-line model:**
   - Girder line offsets from the centreline: ±4.25, ±3.20, ±1.067 m. Σx² = 58.88 m².
   - Load at e = −3.20 m. Share at the edge line x = −4.25: 1/6 + (3.20 × 4.25)/58.88 = **0.3977**, giving 0.3977 × 18.164 = **7.22 mm**.
   - Share at G1: 1/6 + 3.20²/58.88 = 0.3406, giving **6.19 mm** (model: 6.213 mm).
   - The comment's "η₂ ≈ 0.397" is this six-line Courbon factor, not a Hendry–Jaeger coefficient. **CONFIRMED** by calculation against the probe output.
4. **The documented bounds are wrong:**
   - The "Courbon lower bound 4.541 mm" (18.164/4) applies only to a central load.
   - For a four-girder deck with the load on G1, Courbon gives 0.25 + 3.2²/22.756 = 0.700, so **12.71 mm**. The "bounds" therefore do not bracket the target for this load position.
5. **Transverse-stiffness sensitivity:**
   - Using a transformed 250 mm concrete slab strip (n = 6.45) instead of the girder/2 transverse members gives **6.501 mm, which FAILs** (−9.9%). The girder/2 members are DEF-14, blocked under DEC-013.
   - Scaling the girder/2 members ×0.5 or ×2, or girder J ×10 or ÷10, changes the result by less than 0.3%. The deck behaves as effectively rigid.
6. **Mesh convergence and independent numerical validation:** not performed by the suite. MISSING.

**Candidate (b):**
- Its section values are correct plate-formula values. I checked them:
  - A = 0.025192 m²; I<sub>z</sub> = 7.928×10⁻³ m⁴; I<sub>y</sub> = 2.068×10⁻⁴ m⁴; J = 1.817×10⁻⁶ m⁴; A<sub>z</sub> = 0.010432 m²; A<sub>y</sub> = 0.01476 m².
- They are still entered as literals, not computed from the snapped design.

**Verdict: ACCEPTED WITH LIMITATIONS.**
- Only the D-consistency and solver-section checks carry the verdict.
- The deflection sub-check must not be cited as an independent oracle. It will fail falsely when the edge-beam stiffness or DEF-14 is corrected.
- Correct the documented bounds.

---

## 5. Priority 5: C01 fatigue stress range (DEF-07)

**Candidate (b)** (`run_sensitivity_matrix.py` lines 319–371):
- It **no longer injects 62.729 MPa**.
- It computes section moments −Mz<sub>i</sub> and +Mz<sub>j</sub> from `analysis_results.ds.forces`, then max − min across the SLS-frequent cases, divided by the composite Z<sub>e</sub> from `composite_section_properties`. **CONFIRMED.**

**Stress history source:**
- A **synthetic xarray** fed through the real `_extract_demands_from_analysis_results`.
- Only the sign proof uses a real (2D) OpenSees model. Claims that it comes "from actual solver output" are CONTRADICTED.
- That the 3D ospgrillage sign convention matches the 2D proof is PLAUSIBLE but not verified.

**The sign convention is not exercised.** In `/tmp/p25/probe25e.py`, candidates with **no sign flip** (+Mz<sub>i</sub>, +Mz<sub>j</sub>) or **both ends flipped** also **PASS**. The reasons:
- A range taken across load cases at one element end is sign-invariant.
- A single static case gives range 0 under any convention.
- No load case reverses the moment sign.

The test therefore cannot tell a sign-consistent implementation from an inconsistent one.

**Capacity, recomputed from the values the application actually uses** (`FatigueConfig`: Nsc = 2,000,000, welded, ffn = 92, tfn = 59; γ<sub>mft</sub> = 1.35; t<sub>p</sub> = 18 mm, so μ<sub>r</sub> = 1.0):

| Quantity | Calculation | Value | Application output |
|---|---|---|---|
| f<sub>f</sub> | 92 × (5×10⁶ / 2×10⁶)^(1/3) = 92 × 1.35721 | 124.863 MPa | 124.863 |
| f<sub>fd</sub> | 1.0 × 124.863 / 1.35 | **92.491 MPa** | 92.491 |
| DCR | 62.729 / 92.491 | **0.6782** | 0.6782 (computed in the test) |

All three CONFIRMED. N<sub>sc</sub> = 2,000,000 is genuinely used in `compute_fatigue()`, which returns `'Nsc': 2000000`.

The log label is now correct, but it is a hard-coded string. A missing `f_fd_eff_MPa` now raises `KeyError` (CONFIRMED).

**Verdict: ACCEPTED WITH LIMITATIONS.**
- Add a sign-reversal case, for example −500 → +1,500 kNm with ΔM = 2,000 kNm, and an envelope that combines both element ends.
- Read the application's own fatigue DCR.

---

## 6. Priority 6: A02 and MAT

### A02

- **The 2,802.70 kN applied resultant:** 1.35 × (169.819 + 1,275.000 + 313.920) + 1.75 × 244.800 = 2,374.298 + 428.400 = **2,802.70 kN**.
  - It is a literal that does not depend on solver reactions (line 662). It is logged only and never asserted. **CONFIRMED.**
  - Its components equal the declared input loads: deck 24 × 8.5 × 6.25; DW 24 × 8.5 × 1.2; barrier 48 × 6.54.
- **The superposition target:** 1.35 × (169.819 + 1,314.375 + 196.200) + 1.75 × 252.360 = **2,710.16 kN**.
  - Built from component reactions measured at run time.
  - Combination correctness is kept separate from equilibrium (EQ). **CONFIRMED.**
- **Load factors and barrier:** baseline reaction 1,736.6 kN; shear error against the factored combination 72,392.5 N, against the unfactored 1.6×10⁻⁷ N; barrier contribution about 0. Reproduced.
- **Silent fallbacks:** the Phase 2.4 silent fallback to 0 has been replaced by `RuntimeError` (CONFIRMED). Component case names are still literals.
- **Candidate (b):** unchanged from Phase 2.4 (byte-identical function). It is a genuine, production-equivalent fix.

**Verdict: ACCEPTED WITH LIMITATIONS.**
- The SIDL factor of 1.35 still needs ratification.
- The reaction tolerance (3%, about 81 kN) is loose.

### MAT

- **Trace:** `material.girder.density` reaches `input_dict` (70.0) but is consumed only by `validator.py:85`. Self-weight is built at `analyser.py:416` from the module constant `STEEL_UNIT_WEIGHT_kN_m3`, which is 78.5. That is DEF-13. **CONFIRMED.**
- **Expected value:** Σ A × ρ × L = 4 × 0.0225344 × 70 × 24 = **151.43 kN**. Observed **169.82 kN** (= 78.5 × …).
- **Candidate (b)** changes real application behaviour (the constant used by `add_dead_loads`). It is not a fixture-only change.

**Limitations:**
- `L_span = input_dict.get("span", 24.0)`, but the key is `geometry.span`, so L is **always the literal 24.0** (probe: `'span' in input_dict → False`).
- Candidate (c) is byte-equivalent to the baseline.

**Verdict: ACCEPTED WITH LIMITATIONS.**

---

## 7. Priority 7: evidence integrity

| Item | Finding | Status |
|---|---|---|
| File count | 94 on disk: 93 inventoried files plus `hashes/manifest_hashes.json`. Breakdown: 19 baseline, 19 sensitivity, 54 candidates, 1 environment, 1 manifest. The `audit/` directory is empty. | CONFIRMED |
| `hashes/manifest_hashes.json` | **93 of 93 SHA-256 values and sizes match the files on disk** (recomputed on your machine) | CONFIRMED |
| `PHASE_2_5_EVIDENCE_MANIFEST.md` | **45 of the 46 printed SHA-256 values are wrong.** The only correct one is `baseline_exit_code.txt`, whose hash is that of the single character "0". 12 of the wrong values share **exactly the first 16 hex characters** with the true hash and then diverge (e.g. console output: printed `c771144619ab2427a14e…`, actual `c771144619ab24279194…`). The rest differ completely (e.g. EQ log: printed `e59a4bb5…`, actual `e01c7e64…`). Sizes are correct. The pattern is consistent with truncated hashes padded with invented characters. | **CONTRADICTED** |
| Other hashes in the reports | Runner: printed `e26a0cae…`, actual `e09a82c9…` (which equals `runner_self_hash` in the baseline summary). Sensitivity script: printed `d9270bb3…`, actual `9fb37f80…`. Baseline summary: `cbbde09d…` in the remediation report, `7cb59298…` in the manifest; actual `7cb5929822a13d2a9890…`. Sensitivity summary: printed `41a69a21…`, actual `9e65122c…`. `Intg_osdag.sqlite`: printed `25f97857d4cbe205…`, actual `25f978575be64a11…`. `weather.sqlite`: printed `1d7676587372cf93…`, actual `1d767658099bef9d…`. | **CONTRADICTED** |
| Fixtures | The manifest lists `base_config.json` as 1,846 B / `31ae62dc…`. That hash belongs to the Phase 1D input (44,653 B). The actual file is 922 B / `fe11bfce…`, has different content (carriageway 7.5 m), and **is never loaded by the runner**, which reads `phase_1d/input_configuration.json`. `fixture_manifest.json`: listed as 565 B, actually 635 B. | CONTRADICTED / cosmetic |
| stdout / stderr | Restored: `baseline/console_output.txt` (42,848 B) and `sensitivity/console_output.txt` (94,030 B) are UTF-16 PowerShell transcripts. They contain no tracebacks. The command line is only partly visible (truncated by PowerShell error-record wrapping). | CONFIRMED; provenance partial |
| Exit codes | `shell_exit_code.txt` = "0" (UTF-16) for both runs, captured by the shell. The script-written exit-code files also read 0. | CONFIRMED |
| Timeline (UTC) | Sensitivity script edited 16:29:40, runner edited 16:37:50. Sensitivity run 16:38:19–16:39:15; **baseline run 16:39:25–16:40:02 (after it)**. Hash manifest 16:40:40; reports 16:41:39–16:43:54; `CHANGELOG.md`, `DECISIONS.md`, `PROGRESS.md` 16:44–16:45. | CONFIRMED |
| Baseline not overwritten by candidates | Condition (a) in the sensitivity run logs to `candidates/` (lines 109–113), and the baseline ran later into `baseline/`. The runner hash in the summary equals the current runner. | CONFIRMED |
| Earlier evidence | Nothing under `phase_2_3/` or `phase_2_4/` has changed since my Phase 2.4 audit. The Phase 2.3 overwrite is acknowledged as a limitation, and **no recovery is claimed**. | CONFIRMED |
| Misquotation | The remediation report says my Phase 2.4 audit cited a "5%" tolerance. It cited 0.5%. | minor |

---

## 8. Priority 8: remaining tests and blockers

**Unchanged tests:**
- A01, D01, GEO-COUNT and MAT changed only by an added `ops.wipe()`.
- CAP and CAD tests are byte-identical to Phase 2.4, and all their candidates are identical.
- All reproduce: A01 ratio 1.00000; D01 P<sub>z</sub> 463.7 vs 1,039.6 N/m²; GEO-COUNT 6 vs 4; CAP 214,533 / 370,184 kN against oracles of 63.4 / 158.5 kN; CAD std 66.6.
- Their Phase 2.4 acceptance therefore stands.

**Blocked tests:**
- **D02** (DEC-015), **C02** (DEC-018) and **GEO-SLAB** (DEC-013) return BLOCKED unconditionally. No candidates are manufactured, `sensitivity_verified = false`, and none is counted as verified.
- C02 is now correctly labelled DEF-17.
- No real fatigue-vehicle analysis path exists, and DEC-013 is unresolved. **Kept BLOCKED.**
- Minor inconsistency: DEF-17 is "High" in the update report and "Critical" in the register.

---

## 9. Final test classification

| Test ID | Previous finding (Phase 2.4) | Phase 2.5 correction | Independent reproduction | Candidate mutation quality | Remaining risk | Final verdict |
|---|---|---|---|---|---|---|
| A01 | Accepted | `ops.wipe()` only | ratio 1.00000; (b) PASS, (c) FAIL | genuine | none material | **ACCEPTED** |
| D01 | Accepted | `ops.wipe()` only | 463.7 vs 1,039.6 N/m² | genuine | — | **ACCEPTED** |
| GEO-COUNT | Accepted | `ops.wipe()` only | 6 vs 4 | genuine; naive case trivial | weak naive case | **ACCEPTED** |
| CAP | Accepted | none | 63.4 / 158.5 kN oracles | genuine, using IS 800 helpers | ±15% is insensitive to the buckling curve | **ACCEPTED** |
| CAD | Accepted (environment) | none | PASS; blank image FAILs | n/a | not the application's export path | **ACCEPTED** (environment verification) |
| A02 | Accepted with limitations | `RuntimeError` replaces silent 0; documentation | 1,736.6 vs 2,710.2 kN; 2,802.70 kN informational and independent | genuine (unchanged) | literal case names; 3% tolerance; SIDL factor | **ACCEPTED WITH LIMITATIONS** |
| MAT | Accepted with limitations | `ops.wipe()`; documentation | 169.82 vs 151.43 kN | genuine behavioural change; (c) identical to baseline | span is a literal 24.0 via the wrong key | **ACCEPTED WITH LIMITATIONS** |
| C01 | Accepted with limitations (candidate injected values) | genuine candidate; N<sub>sc</sub> label; `KeyError` | 92.491 MPa and 0.6782 recomputed; candidate computes, does not inject | genuine | sign convention unexercised (sign-wrong candidates PASS); synthetic history; DCR computed in the test | **ACCEPTED WITH LIMITATIONS** |
| B01 | Accepted with limitations (self-calibrated oracle) | bounds documented; plate-formula constants | 7.816 / 7.239 mm; 7.218 explained as six-line Courbon | literal constants (now correct values) | target tied to edge-beam modelling and DEF-14; bounds wrong; a transformed-slab variant fails falsely | **ACCEPTED WITH LIMITATIONS** |
| EQ (DEF-18) | Rejected | derived loads; centroids; 0.05% / 0.05 m; real distributor | defect reproduced; candidate (b) mathematically exact | **genuine** consistent-load distributor | equal lumping, wrong spacing and both barrier relocations PASS; false failure after a DEF-13 fix | **REJECTED** |
| RPT | Rejected | G1 and G3 scenarios; table check | baseline reproduced; 24-case matrix correct under (b) | genuine wrapper (unchanged) | a G1+G3-only candidate PASSes; table blind to non-girder components; stale fixture status | **REJECTED** |
| FS | Rejected | dropped Test B; five checks | baseline reproduced; **the test writes `weather.sqlite` into the clean source tree** | genuine anchoring | Checks 4 and 5 are path aliases; no OS permissions; one directory monitored; queries not asserted | **REJECTED** |
| D02 | Blocked | unchanged | BLOCKED | none | DEC-015 | **BLOCKED** |
| C02 | Blocked | relabelled DEF-17 | BLOCKED | none | DEC-018 | **BLOCKED** |
| GEO-SLAB | Blocked | unchanged | BLOCKED | none | DEC-013 | **BLOCKED** |

---

## 10. Mandatory corrections

1. **EQ:**
   - Per-load-group centroid assertions, at least each barrier line separately.
   - A transverse-distribution assertion: per-longitudinal-line load shares, or comparison of the nodal load vector against an independently computed consistent vector.
   - Declared self-weight from `material.girder.density`.
   - Remove the literal fallbacks.
2. **RPT:**
   - A loop that injects a failure into each girder, G1–G6.
   - A DCR-only failure.
   - Assert the table in every scenario, and record the decision on whether the overall status includes non-girder components.
   - A fixture whose `design_results.overall_status` matches the injected state.
3. **FS:**
   - Run against a copied package tree, never the repository.
   - A real read-only scenario using OS permissions, with the test running without elevation.
   - Recursive before/after hashing of the package tree.
   - Assert the query results.
   - Remove the alias checks.
4. **B01:**
   - Correct the documented bounds.
   - Re-label the deflection check as a model-consistency check tied to the edge-beam and DEF-14 assumptions.
   - Or measure deflection under the loaded girder against an independently built model.
5. **C01:** add a sign-reversal case and a combined-ends envelope.
6. **Evidence:**
   - Regenerate `PHASE_2_5_EVIDENCE_MANIFEST.md` and the hash lines of the remediation report from `manifest_hashes.json` or recomputed values. Never retype or extend hashes by hand.
   - Fix or remove `testing/fixtures/`.

---

## 11. Repository status verification

| Check | Result |
|---|---|
| `.git/HEAD` | `ref: refs/heads/dev` → `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` |
| Branches and tags | only `dev`; no tags; no Phase 3 branch |
| Locks and index | No `*.lock` files. `.git/index` mtime 2026-11-15 12:26:18 UTC, unchanged. The `.git` directory mtime is 16:45:05 UTC, after the reports, which suggests a Git command was run then. No persistent change resulted. |
| Source content | 282 files under `src/` (excluding `__pycache__`, `*.pyc`, `*.sqlite`, `egg-info`), CR-normalised. Aggregate SHA-256 `7c9294813b58fb84ecd965643daec240276747d1788b13187c0e0f46c52b024c` on your machine **and** in a clean checkout of `d74f56d`: **identical**. |
| Files changed after 2026-11-15 14:30 UTC (outside `.git`, excluding caches) | Only the untracked `weather.sqlite`, mtime 2026-11-16 05:48:51 UTC, which predates Phase 2.4 and is unchanged. |
| Databases | `Intg_osdag.sqlite` `25f978575be64a11…` (270,336 B), unchanged. `weather.sqlite` `1d767658099bef9d…` (180,224 B), unchanged. |
| Prior audits | Phase 2.3 (`00ed39d0…`) and Phase 2.4 (`496ca7ce…`) audit files are byte-identical to what I issued. |

**`source\OsdagBridge` remains unchanged at the frozen baseline commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`.**

I modified nothing in the workspace apart from saving this report. All probes ran in an isolated cloud copy.

---

## Final decision

**CONDITIONAL ACCEPTANCE**

| Status | Tests |
|---|---|
| **Accepted** | A01, D01, GEO-COUNT, CAP, CAD (environment check) |
| **Accepted with limitations** | A02, MAT, C01, B01, with the limitations in §4–§6 |
| **Rejected** (corrections in §10 mandatory) | EQ-LOAD-CONSERVATION, RPT, FS |
| **Blocked** (not counted as verified) | D02, C02, GEO-SLAB |

The claim that Phase 2.5 "resolved every outstanding finding" is **not justified**. The three Priority 1–3 tests still accept plausible incorrect implementations, and the human-readable evidence manifest contains incorrect hashes. The underlying evidence is intact; only the manifest text is wrong.

This decision accepts tests only. **It does not authorise application source-code changes, and it does not authorise Phase 3 planning or branch creation.**
