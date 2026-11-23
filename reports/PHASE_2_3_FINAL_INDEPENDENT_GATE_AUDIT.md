# Phase 2.3 Final Independent Gate Audit: OsdagBridge Regression Suite

**Purpose:** decide whether Phase 2.3 resolves the rejection findings in `reports/PHASE_2_2_FINAL_INDEPENDENT_GATE_AUDIT.md`, and whether Phase 3 remediation can be authorised.

**Frozen baseline:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (branch `dev`)

**Material examined:**
- `run_all_baseline_tests.py` (77,850 B, SHA-256 `ac6da5ee…4952c`) and `run_sensitivity_matrix.py` (38,662 B, `6ed1510e…7d`), both read in full.
- Every file under `testing/evidence/phase_2_3/{baseline,sensitivity,candidates}`.
- The three Phase 2.3 reports.
- The application source and vendored ospgrillage at the baseline.

**Independent execution.** I ran both harnesses unchanged on a clean baseline clone in a cloud reference environment: Linux, Python 3.12, pythonocc-core 8.0.1.2, openseespy 3.8.0.0, numpy 2.5.4, Xvfb. I also ran three probe scripts of my own: component reactions for A02, and correct-implementation candidates for RPT, C02, MAT and A01. Nothing was run, edited, installed, branched or committed on your machine, apart from saving this report.

**Labels:**
- Evidence: CONFIRMED / PLAUSIBLE / UNVERIFIED / CONTRADICTED.

---

## 1. Executive verdict

**Phase 2.3 fixed several things:**
- **Evidence handling:**
  - baseline, sensitivity and candidate logs are in separate folders;
  - the baseline ran *after* the final edits and *after* the sensitivity run;
  - full console transcripts were captured;
  - the runner hash and real package versions are recorded (OCC 8.0.1, OpenSeesPy 3.8.0.0, numpy 2.5.5).
- **A02** now analyses BASIC_1 case-specifically, with no load-case re-ordering, median injection or `__eq__` patch.
- **A01** now needs the line and patch scaling fixes. A stock-`apply_load_factor` fix FAILs (my probe: ratio 1.214).
- **CAP** reads b1 from the application's real `bs_b1_mm` input.
- **RPT** restored the all-pass mirror.
- **D02 and GEO-SLAB** remain blocked and uncounted.
- The repository is untouched.

**But at least four tests would still fail a correct implementation, and the key claims of A02, C01 and C02 are not what the code does.** In my probes, correct implementations FAIL on A02, RPT, C02 and MAT:

1. **A02's "independent" 2,710.17 kN target is the model's own output.** It bakes in an **equilibrium violation**:
   - the crash-barrier load case applies 313.92 kN but its supports react only 196.20 kN (−37.5%);
   - the deck reacts 1,314.38 kN against 1,275.00 kN applied (+3.1%);
   - the wearing course reacts 252.36 kN against 244.80 kN applied (+3.1%).

   I measured these directly. The reports explain the gap as "mesh tributary scaling", but a static analysis must conserve load, so that explanation is CONTRADICTED. A fix that restores equilibrium would FAIL A02: reaction 2,802.7 kN, which is 3.4% off, and barrier "contribution" 357.4 kN against an expected 264.87 kN.
2. **RPT's "All Pass" scenario still contains failing girders.** It overrides only G1. G2–G6 keep their real Phase 1D failures: fatigue DCR 1.95–1.97 and stiffener leg 1.18. The test therefore *requires* the summary to ignore G2–G6. An implementation that evaluates every girder, as the application's own `overall_design_status` already does, **FAILs** (probe).
3. **C02's wheel-placement check reads the vehicle's local vertex coordinates.** It does not read the global position on the deck. A production-style fix using the vendored IRC `FATIGUE` model on a path centred at z = 4.25 m **FAILs** as "outside deck" (probe). Also, `fatigue_demand_linked` and `peak_reaction_matched` are set to True by the same `max force > 10 N` condition, so **fatigue utilisation is not verified**.
4. **MAT now injects density under an invented key,** `cfg["materials"]["density"]`. The real UI key `material.girder.density` stays at 76.4. A fix reading the real key **FAILs** (probe: 165.3 kN against the expected 151.4 kN).
5. **C01's "correct" candidate still injects stress ranges.** It hard-codes 62.729 MPa or 0.0 by load-case count. The "fatigue DCR = 1.9746" is `range / 31.77`, where 31.77 MPa is an unsourced constant chosen so the result reproduces Phase 1D's DCR. That DCR is actually 182.63 / 92.49 MPa. The application's DCR is never computed.
6. **B01's "hand oracle" is arithmetically false.** The test comment's formula PL³/48EI gives **18.16 mm**, not 7.218 mm. 7.218 mm is the grillage result obtained with the candidate section.

**Verdict: REJECT PHASE 2.3 REGRESSION SUITE.** §9 lists the remaining work. It is now narrow: four oracles, three candidates and one missing defect registration. A01, CAP, D01, GEO-COUNT and CAD are sound, and B01 is usable once its oracle is relabelled.

---

## 2. A02 reaction audit

| Question | Finding | Status |
|---|---|---|
| Does `analyze(load_case=b1_name)` analyse only BASIC_1? | Yes. `OspGrillage.analyze` filters `load_case_list` by name (`osp_grillage.py:2124–2133`) and runs only the matching `Analysis`. | CONFIRMED |
| Is the state reset between cases? | Yes. BASIC_1 alone and BASIC_1 after "1.0 DL" both give **1,736.55 kN**. | CONFIRMED (probe) |
| Do the reactions belong to BASIC_1? | Yes. Baseline BASIC_1 = 1.0 DL (1,484.19) + 1.0 DW (252.36) = 1,736.55 kN, so the factors are dropped. **Erratum to my Phase 2.2 audit:** at baseline, `SEISMIC_4` happens to produce the same 1,736.55 kN, so that number did not by itself show which case was read. The objection to the extraction method stood, and is now resolved. | CONFIRMED |
| No median | Fixture `geometry.include_median = "No"`, median width 0; the median term has been removed. | CONFIRMED |
| Load cases included | SW, DD (deck), "1.0 DW", "Crash barrier load", and "1.0 DL" = SW + DD + footpath (none) + `sidl_combination` (None at baseline) | CONFIRMED |

**Component reactions (my probe) against the load applied:**

| Case | Support reaction | Applied (load objects) | Δ |
|---|---|---|---|
| SW | 169.82 kN | 169.82 kN | 0 |
| DD | **1,314.38 kN** | 1,275.00 kN | **+3.1%** |
| 1.0 DW | **252.36 kN** | 244.80 kN | **+3.1%** |
| Crash barrier | **196.20 kN** | 313.92 kN | **−37.5%** |

- **The oracle constants are exactly these reactions.** They are not independent of the application.
- The barriers sit at z = 0.25 m and 8.25 m, inside the 0–8.5 m mesh. A load "lost" or "gained" by distribution violates statics. This is an **unregistered load-distribution/equilibrium defect**, which matches the barrier shortfall noted in Phase 1D. It must be registered and tested, not absorbed into the A02 target.

**Expected values:**
- The test's target 2,710.17 kN = 1.35 × (169.82 + 1,314.38 + 196.20) + 1.75 × 252.36. Reproduced; the candidate gives 2,710.16 kN.
- The value consistent with equilibrium is 1.35 × (169.82 + 1,275.00 + 313.92) + 1.75 × 244.80 = **2,802.7 kN**. The SIDL factor of 1.35 still needs confirming against IRC 6 Annex B.

**Barrier differential:** 264.87 kN = 1.35 × 196.20. It is computed as *total reaction minus hard-coded non-barrier constants*, so it is not an independent measurement of the barrier.

**What the test detects** (reasoned from the code with the probe values):

| Fault | Detected? |
|---|---|
| Dropped factors | Yes: 1,736.55 kN, and a force error of 72,392 N |
| Missing barrier | Yes: 2,445.29 kN is −9.8% |
| Wrong case selected (e.g. `SEISMIC_4`) | Yes: about 1,932.8 kN |
| Duplicated DW or barrier | Yes: +441.6 / +264.9 kN |
| Barrier included but unfactored | Yes, by the barrier check only. The reaction (2,641 kN) is within the 3% tolerance. |

**But a correct, equilibrium-restoring implementation FAILs**, as noted in §1.

**Candidate (b):** no re-ordering, median injection or `__eq__` patch remains (CONFIRMED). It does still:
- replace `add_dead_loads` wholesale;
- monkeypatch `LoadCase.add_load`, `LineLoading.apply_load_factor` and `PatchLoading.apply_load_factor`.

Those are production-equivalent fixes, not output substitution.

---

## 3. C02 fatigue integration audit

| Stage | Finding |
|---|---|
| Vehicle creation | Candidate (b) hand-builds 6 point loads: wheels of 58.86 / 68.67 / 68.67 kN at x = 0, 4.5, 5.9 m and **absolute** z = 3.41 / 5.09 m. Total 392.4 kN = 40 t; axle forces 117.72 / 137.34 / 137.34 kN from masses of 12 / 14 / 14 t × 9.81. CONFIRMED. It does not use the application's `cl_204_6_fatigue_load` or the vendored `create_fatigue_vehicle`, and it ignores the `KEY_LL_IRC_CLASS_FATIGUE` toggle. |
| Transverse placement | The test checks `load_point_1.z` of each component in [0, 8.5]. Those are the **vehicle's local** coordinates. The candidate passes only because it writes absolute z into the vertices on a path at z = 0. **A correct vendored-model fix** (local wheels at ±0.84 m, path at z = 4.25 m) **FAILs** as "outside deck" (probe). |
| Moving positions | Path from x = −10 to 34 m, analysed by `model.analyze()`. CONFIRMED. |
| Solver analysis and force extraction | `get_results(load_case=name)` returns a maximum force above 10 N. CONFIRMED. |
| Fatigue stress range and utilisation | **Not tested.** `analyzed_response_nonzero`, `peak_reaction_matched` and `fatigue_demand_linked` are all set True by the single `max_f > 10.0` condition (runner lines 891–895). No reaction against the vehicle weight is computed, and no fatigue range or DCR is read. |

**Classification:** the scope is *vehicle generation and non-zero solver response*. **Fatigue participation and utilisation: NOT VERIFIED.** The placement check rejects correct implementations.

---

## 4. C01 DCR audit

- **Both paths are exercised.** `_extract_demands_from_analysis_results` is run on synthetic static and cyclic datasets: the envelope path (`designer.py:2970–2988`) and the per-load-case path (`:3082`).
  - Baseline static: envelope 125.46 MPa, per-LC 62.73 MPa; expected 0.
  - Cyclic expectation: 62.729 MPa on both paths.
  - The per-load-case positive assertion is new and resolves my Phase 2.2 finding.
- **Fixing only one path fails (CONFIRMED).** The (c) candidate zeroes the envelope only and FAILs. A per-LC-only fix fails the envelope static check.
- **The candidate is output injection (CONFIRMED).** `mut_b_c01` overwrites every `stress_range_MPa` with 0.0 if there is one load case and 62.729 otherwise (sensitivity script lines 283–298). That is exactly the criterion the brief says to reject. Its PASS proves nothing about a real implementation.
- **The DCR is not traced:**
  - `dcr_c = range_c_env / 31.77`, with `f_fat = 31.77` hard-coded and unsourced. `dcr_ok` is algebraically identical to `cyclic_env_ok`.
  - 62.729 / 31.77 = 1.9745 reproduces the *number* 1.9746. But Phase 1D's 1.9746 is G3's "Fatigue Normal Stress": 182.63 MPa / 92.49 MPa, where 182.63 = 2 × 1,455.73 kNm / 15.94×10⁶ mm³.
  - **No application fatigue capacity or DCR is computed** by the test.
- The sign companion (2D OpenSees) is asserted; it is still not an ospgrillage 3D result. PLAUSIBLE.

---

## 5. Candidate-by-candidate sensitivity findings

**Execution.**
- Both harnesses reproduce in my environment: baseline 11 BASELINE_FAIL / 2 BLOCKED / 1 PASS with process exit 0; sensitivity 12/12 with exit 0.
- The results are executed, not pre-populated.
- The original assertions and oracles are unchanged: candidates call the same `test_*` functions with `evidence_dir=CANDIDATES_DIR`.
- Each test writes a single candidate log, so `candidates/*.log` keeps only the **last** condition, (c). Per-condition logs and per-candidate hashes don't exist; only the JSON reasons and the console transcript remain.

| # | Test | (b) "correct" candidate: actual change | Real implementation? | (c) naive candidate | Correct implementation can FAIL? | Status |
|---|---|---|---|---|---|---|
| 1 | A01 | `LineLoading.apply_load_factor` also scales `line_end_point`; `PatchLoading` rebuilds the interpolator; `add_load` scales a copy | **Yes** (upstream-originated defect in the OsdagBridge vendored fork) | 1.15× scaling → FAIL (ratio 1.09) | No. The stock fix now fails (probe) | **Verified** |
| 2 | B01 | `_girder_section` returns hard-coded snapped constants (I<sub>y</sub>, J, A<sub>y</sub>, A<sub>z</sub> invented) | Partly: it changes solver input, but the values are constants, not derived | metadata swap → FAIL | Low. A derived section differing in I<sub>y</sub>/J barely changes deflection. | **Verified** (oracle mislabelled, §6) |
| 3 | C01 | overwrites the ranges with 0.0 or 62.729 by load-case count | **No: output injection** | envelope-only zeroing → FAIL | — | **NOT DEMONSTRATED** |
| 4 | A02 | upstream factor fixes; SIDL built before DL; production `create_median_load` | **Yes** | BASIC_1 without barrier → FAIL | **Yes:** an equilibrium-correct fix | **Demonstrated, but the oracle is wrong** |
| 5 | D01 | reads the 4 real UI keys | **Yes** | speed only → FAIL | No | **Verified** |
| 6 | D02 | BLOCKED (DEC-015) | — | — | — | **Blocked, not counted** |
| 7 | C02 | hand-built 6-wheel compound at absolute z, unconditional | Partly (no toggle, not the production vehicle) | mock with no loads → FAIL | **Yes:** the vendored-model fix (probe) | **Scope-limited; utilisation not verified** |
| 8 | RPT | wraps the output and replaces the hard-coded block using G1-only checks and component efficiencies | **Output post-processing** (decisions derived from results, but outside the function) | hard-coded "Girder fail" → FAIL scenario 1 | **Yes:** the all-girder implementation (probe) | **NOT DEMONSTRATED; oracle wrong** |
| 9 | GEO-COUNT | `n_girders = _girder_count()` | **Yes** | `n = 0` | No | **Verified** (weak naive case) |
| 10 | GEO-SLAB | BLOCKED (DEC-013) | — | — | — | **Blocked, not counted** |
| 11 | CAP | recomputes `Fcdw_wb` with the application's own `IS800_2007.cl_7_1_2_1_…` (curve c, α = 0.49), r = t<sub>w</sub>/√12, b1 from `bs_b1_mm` | **Yes** (a post-hoc overwrite, but from inputs with production helpers) | squash load → FAIL | No | **Verified** |
| 12 | MAT | swaps the module constant to `materials.density` (invented key), falling back to the real key | Only for the invented key | identical to baseline | **Yes:** a real-key fix (probe) | **NOT DEMONSTRATED; input wrong** |
| 13 | FS | repoints `DB_PATH` and the default constructor to a temporary app-data folder | Yes | `DB_PATH` only → FAIL | Partly (§6) | **Verified within limits** |
| 14 | CAD | = baseline | n/a | uniform image → FAIL | n/a | **Verified** (environment check) |

**Genuinely verified:** A01, B01, D01, GEO-COUNT, CAP, FS (limited) and CAD = **7 of 12**. **"12/12" is CONTRADICTED.**

---

## 6. Remaining test validity

- **RPT:**
  - The six scenarios use schemas the application actually parses: `_max_member_efficiency` for cross-bracing and end-diaphragm efficiency, and `ur_*` deck keys (`executive_summary.py:30–55, 104–124`). That part is correct.
  - Each status is derived from the component results.
  - **But G2–G6 retain real FAIL checks in every scenario** (fatigue 1.948–1.975, Int.Stiff 1.183, shear 1.061), so "All Pass" is not all-pass.
  - The (b) candidate reads G1 only. Fix: override every per-girder entry, or use a dictionary with no failing girders.
- **B01:**
  - Valid in structure. It checks the solver-consumed `girder_sections`, D = d<sub>w</sub> + 2t<sub>f</sub>, and the response.
  - **The 7.218 mm "hand oracle" is CONTRADICTED.** P·L³/(48·E·I) = 100 kN × 24³ / (48 × 2×10¹¹ × 0.00792758) = **18.16 mm**. The baseline figure is 19.62 mm for I<sub>z</sub> = 0.00734 m⁴. 7.218 mm is the grillage's distributed result; its ratio 7.816 / 7.218 = 1.083 matches the I<sub>z</sub> ratio of 1.080.
  - Relabel it as a calibrated model oracle, or derive it from the application's section routine.
- **CAP:**
  - Reproduced: 63.40 kN (t<sub>w</sub> 8 mm, d 1,304 mm, b1 101.81 mm) and 158.50 kN (t<sub>w</sub> 10 mm, d 1,000 mm, b1 100 mm).
  - A hard-coded single value fails, and the squash or clamp value fails.
  - The (c) candidate in the harness is the squash formula. My Phase 2.1 / 2.2 hard-code and clamp checks still hold: 63.4 kN fails geometry 2, and 1,918.8 / 1,909.1 kN fail both geometries.
  - The ±15% tolerance still doesn't discriminate the buckling curve; this is stated.
- **FS:**
  - The status now includes an **observed write**: `connect()` creates `weather.sqlite` in a missing-file sandbox. A packaged read-only database whose `connect()` never creates files would **pass**, which resolves part of my objection.
  - **Remaining gaps:**
    - Test A's before/after hashes are computed but **never compared**, so rewriting an existing packaged database goes undetected.
    - The status still requires the path-string check `is_inside_package`.
    - The production `_with_db` path is not exercised.
- **A01:** valid. It now covers line and patch loads, and needs the `line_end_point` and patch-interpolator fixes. **Ownership:** the defect originates upstream (PyPI 0.6.0 has the same `apply_load_factor` structure) but sits in OsdagBridge's **modified vendored fork** (`src/ospgrillage`, which adds the CLASSA / CLASS70R / FATIGUE vehicles). Fix it there and report it upstream.
- **D01, GEO-COUNT, CAD:** valid, unchanged.

---

## 7. Evidence integrity

| Check | Finding | Status |
|---|---|---|
| Sequence | Scripts edited 14:21:35 / 14:21:56. Sensitivity run 14:22:23–14:23:19. Baseline run 14:23:27–14:24:21. Reports 14:25–14:26. | CONFIRMED |
| Baseline complete and unoverwritten | 14 baseline logs, summary, exit file and console log all written in the baseline window, after the sensitivity run. The sensitivity condition (a) now writes to `candidates/`. The SHA-256 values in `PHASE_2_3_EXECUTION_EVIDENCE_AUDIT.md` match the files. | CONFIRMED |
| Runner provenance | The summary's `runner_self_hash` = `ac6da5ee…` = the current runner. Fixture hashes `31ae62dc…0191` and `429a3198…a5ab` match. | CONFIRMED |
| Environment | `osdagbridge-py312`, Python 3.12.16, OCC 8.0.1, OpenSeesPy 3.8.0.0, numpy 2.5.5, scipy 1.18.1, xarray 2026.9.0. This corrects the Phase 2.2 misreport. | CONFIRMED |
| Exit codes | `baseline_exit_code.txt` = 0 and `sensitivity_exit_code.txt` = 0 are still **written by the scripts** before `sys.exit`. The console transcripts (UTF-16 PowerShell redirects, which contain a `NativeCommandError` stderr banner) don't record the shell's `$LASTEXITCODE`. My reproduction gave a process exit of 0 for both. Baseline exit 0 means 14/14 manifest alignment, not that the application passes. | Consistent; not independently captured on Windows |
| Candidate logs and hashes | Only condition (c) survives in `candidates/`. No per-candidate code hashes or diffs are recorded. | Gap |
| Report values against logs | The A02, B01, C01, CAP and MAT figures match the logs. Explanations that **don't** hold: "92.5 kN mesh tributary" (§2), the "7.218 mm hand oracle" (§6), "DCR = 1.9746" (§4), and "fatigue utilisation linked" (§3). | Partly CONTRADICTED |
| `testing/fixtures/` | Still absent; the fixtures stay in `testing/evidence/phase_1d/`. | Unchanged |

---

## 8. Repository integrity

| Check | Result |
|---|---|
| Commit and branch | `.git/HEAD` → `refs/heads/dev` → `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`. No lock files. `.git/index` mtime 2026-11-15 12:26:18 UTC, unchanged. |
| Source | The aggregate SHA-256 of all 282 non-ignored files under `src/` (CR-normalised) is `c6d61d03…a89d`, identical to the clean baseline and to all previous audits. No source file changed after 13:00 UTC. |
| Databases | `Intg_osdag.sqlite` `25f97857…`, byte-identical. Untracked `weather.sqlite` `1d767658…`, mtime 05:48 UTC, unchanged. |
| Workspace changes | The two harness scripts, `phase_2_3/` evidence, three reports, and `CHANGELOG.md`, `DECISIONS.md` and `PROGRESS.md`. `reports/PHASE_2_2_FINAL_INDEPENDENT_GATE_AUDIT.md` is my previous deliverable, byte-identical (`0dbb5a4b…`). |
| Branches | No Phase 3 branch observed. |

**Conclusion:** the application repository is clean at the frozen baseline (CONFIRMED).

---

## 9. Outstanding actions

1. **Register a new defect: load-distribution equilibrium.**
   - Crash barrier reaction is 196.20 kN against 313.92 kN applied.
   - Deck is 1,314.38 kN against 1,275.00 kN.
   - DW is 252.36 kN against 244.80 kN.
   - Add a test asserting Σ reactions = Σ applied load, within 0.5%, for each dead-load case.
2. **A02:** base the target on applied resultants (2,802.7 kN, pending IRC 6 Annex B confirmation of the SIDL factor) or on Σγᵢ·Rᵢ computed *at run time* from the analysed component cases, not hard-coded model outputs. Measure the barrier contribution directly: analyse BASIC_1 with and without the barrier term, or compare against 1.35 × the analysed barrier case.
3. **RPT:** make "All Pass" genuinely all-pass by overriding or removing G2–G6 failures. Make the girder status depend on every girder. Implement the (b) candidate inside the summary logic instead of as a text post-processor.
4. **C02:**
   - Check placement in **global** coordinates (path position plus local offsets) against the carriageway.
   - Drive generation through `KEY_LL_IRC_CLASS_FATIGUE` and the production vehicle definition.
   - Compute the peak reaction against the vehicle weight.
   - Either link the case to the fatigue stress range or DCR, or rename the test's scope and remove the `fatigue_demand_linked` / `peak_reaction_matched` labels.
5. **C01:** replace the injecting candidate with a genuine range implementation. Remove `f_fat = 31.77`, or compute the DCR through the application's fatigue capacity and cite where it comes from. Don't present 1.9746 as reproduced.
6. **MAT:** set the density through the real key `material.girder.density`. Add a naive candidate that differs from the baseline, for example one that reads the database value.
7. **B01:** correct the "hand oracle" comment and report wording. 18.16 mm is the single-beam value; 7.218 mm is a calibrated grillage value. Optionally derive the target from the application's section routine.
8. **FS:** compare the before/after hashes in Test A. Exercise a `_with_db`-wrapped production call. Drop the path-string condition from the status.
9. **Evidence:** keep one log per condition per test (a, b, c), with candidate source hashes. Capture the shell's real exit status alongside the self-written files. Create `testing/fixtures/` or stop referring to it.
10. **Governance:** obtain ratification of DEC-013, DEC-014 and DEC-015 and of the SIDL factor.
11. **Re-audit** limited to A02, RPT, C02, C01, MAT, FS, B01's oracle and the new equilibrium test.

The tests for DEF-01 (A01), DEF-05 (D01), DEF-11 (GEO-COUNT), DEF-12 (CAP) and DEF-03 (B01) are sound enough to gate their own fixes. Whether to start those in parallel is a decision for the project lead; this audit does not authorise it.

**Phase 3 has not been started, and no branch was created.**

---

## Verdict

**REJECT PHASE 2.3 REGRESSION SUITE**
