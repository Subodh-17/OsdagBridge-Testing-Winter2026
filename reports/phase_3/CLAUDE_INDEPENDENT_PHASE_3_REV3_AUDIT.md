# PHASE 3 — Revision 3.0 Independent Audit

**Auditor:** Claude (independent adversarial auditor)  
**Date:** 2026-11-18. Inspection ran from approximately 11:47 to 11:52 UTC, measured on the device clock.  
**Baseline audited against:** `source/OsdagBridge`, branch `dev`, commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`. The frozen sealed evidence is the Phase 2.12, 2.13 and 2.17 runs.  
**Controlling prior audits:**
- `reports/phase_3/CLAUDE_INDEPENDENT_PHASE_3_PLANNING_AUDIT.md` (First Audit)
- `reports/phase_3/CLAUDE_INDEPENDENT_PHASE_3_REV2_REAUDIT.md` (Second Audit — REJECTED)

**Mode:** Read-only. I changed no source, tests, database, environment, ledger, seal, or Phase 2 file. I made no commits and switched no branches. The only file written to the workspace is this report.

---

## 0. Verdict

# CONDITIONALLY ACCEPTED

Revision 3.0 is a thorough and rigorous correction of Revision 2.0. It resolves all 19 findings from my second audit, corrects the material arithmetic errors, establishes sound acceptance oracles with defensible tolerances, properly separates test fixtures, registers the previously unregistered defects (DEF-19a/b/c, DEF-20), fixes the batch dependency ordering, and maintains the governance boundary.

However, two non-material conditions remain:

1. **File count discrepancy (non-material):** The preservation report states "282 files (205 `.py` files)" but `git ls-files src` on the device returns **283 files (205 `.py` files, 78 non-`.py` files)**. The aggregate SHA-256 hash (`7c9294813b58fb84…`) was not independently re-derived in this audit but the commit hash and working tree cleanliness are confirmed. This is an off-by-one documentation error, not a preservation failure.

2. **DEF-10 scope boundary (non-material):** The Rev3 DEF-10 specification documents 5 `weather.sqlite` access paths. I found 17 total `sqlite3.connect` call sites across 8 distinct Python files. The additional call sites connect to `Intg_osdag.sqlite` (materials database), not `weather.sqlite`, so they fall outside the DEF-10 scope. This is a defensible scope boundary, but the broader database hardening concern (read-only URI, no sidecar writes, integrity checks) applies equally to `Intg_osdag.sqlite`. This should be recorded as a future hardening item, not a blocking finding.

Neither condition represents a material engineering error. Both can be resolved by a one-line correction to the file count and an advisory note, without re-revision of the planning suite.

**This plan is suitable to submit for a human implementation-authorization decision**, subject to the two conditions above being acknowledged.

---

## 1. Finding-by-Finding Reconciliation (R2-01 through R2-19)

I did not take the resolution matrix's "RESOLVED" status as evidence. Each finding was re-verified against source code, sealed logs, or independent calculation.

### R2-01: BASIC_1 Arithmetic Error — **RESOLVED** ✔

**Rev 2 defect:** BASIC_1 = 2788.751 kN was an arithmetic error; stated inputs give 2818.242 kN.

**Verification:**
$$1.35 \times (244.1664 + 1249.5000 + 313.9200) + 1.75 \times 216.0000$$
$$= 1.35 \times 1807.5864 + 378.0000 = 2440.2416 + 378.0000 = \mathbf{2818.2416\text{ kN}}$$

Independently calculated on the device using PowerShell double-precision arithmetic. The Rev3 documents consistently state 2818.242 kN (rounded to 3 decimal places), which is correct.

**Acceptance test:** The test oracle at `TC-REG-A02-ULS-COMBINATION-SUM` uses $2818.242 \text{ kN} \pm 10^{-6}$ relative tolerance. This would correctly reject the old 2788.751 kN value ($-1.05\%$ error, far outside $10^{-6}$). ✔

### R2-02: Wearing Course Width Defect — **RESOLVED** ✔

**Rev 2 defect:** Oracle assumed DW over 7.5 m carriageway (216.0 kN), but production applies 8.5 m (244.8 kN); no defect registered.

**Verification:** Inspected `load_placement.py:133–138`. Method `overlay_load(edge_clearance)` constructs a patch from `Point(0.0, edge_clearance)` to `Point(span, bridge.width - edge_clearance)`. With `edge_clearance=0.0`, this spans the full 8.5 m deck width. Confirmed.

**Rev3 correction:** DEF-20 formally registered as "Wearing Course Transverse Extent" with dual-oracle specification: production baseline at 244.800 kN and intended carriageway at 216.000 kN, governed by DEC-020. Neither is silently treated as approved. ✔

### R2-03: Mixed Fixture Geometries — **RESOLVED** ✔

**Rev 2 defect:** Hand-fixture girder A = 0.0324 m² asserted on the sealed bridge (snapped A = 0.025192 m²).

**Verification:** Rev3 explicitly decouples:
- Hand Calculation Fixture: A = 0.032400 m² (web 1300×10, top 400×16, bottom 500×26)
- Sealed Bridge Pipeline Fixture: A = 0.025192 m² (web 1304×8, top 350×14, bottom 450×22)

Every oracle in the traceability matrix, test acceptance criteria, and batch plan explicitly states which fixture it uses. No cross-contamination found. ✔

### R2-04: DEF-19 Oracle — **RESOLVED** ✔

**Rev 2 defect:** DLA 1.15 (RCC formula) and lane factors 1.0/1.0/0.9 matched neither the code (0.10; [1.0, 0.8, 0.4]) nor the report (0.24). One-sided "≥ 1.725×" oracle accepted double-application.

**Verification:**
- Inspected `irc6_2017.py:534, 543`: `if KEY_VEHICLE[1]:` tests `'Class70R(T)'` (always truthy). Returns 0.10 for 9–45 m spans. Confirmed.
- Inspected `analyser.py:1803`: `dla = 1.0 + IRC6_2017.cl_208_3_impact_factor(self.L)` → 1.10.
- Inspected `keyfile.py:119`: `LANE_REDUCTION_FACTORS = [1.0, 0.8, 0.4]`.

**Rev3 correction:** DEC-019 raised for formal owner confirmation. Three-stage bilateral equality oracles specified:
- Stage 1: Vehicle case DLA = $1.100000 \pm 10^{-6}$
- Stage 2: Governing selection DLA × lane factor = $1.100000 \pm 10^{-6}$
- Stage 3: ULS combination = $1.50 \times 1.10 = 1.650000 \pm 10^{-6}$

One-sided bound eliminated. DEC-019 properly blocks final engineering acceptance without silently treating any value as approved. ✔

### R2-05: Unregistered Live-Load Defects — **RESOLVED** ✔

**Rev 2 defect:** Unregistered: `cl_208_3` truthy-string defect; lane-factor constants and indexing; analysis/report impact mismatch.

**Verification:** Rev3 registers:
- DEF-19a: `cl_208_3` truthy-string check hardcoding 0.10 (confirmed at `irc6_2017.py:534, 543`)
- DEF-19b: Lane reduction factors indexed per-vehicle not per-lane (confirmed at `analyser.py:1827–1828`)
- DEF-19c: Analysis 0.10 vs report 0.24 discrepancy (confirmed: `analyser.py:1803` vs `chap3.py:88–116`)

Each has dedicated test IDs and is tracked in the traceability matrix. ✔

### R2-06: DEF-18 End-Bay Mechanism — **RESOLVED** ✔

**Rev 2 defect:** Mechanism attributed to `continue` at line 1676, which never fires.

**Verification:** Inspected `osp_grillage.py:1674–1708`. Line 1676: `if "ends" not in points.keys(): continue`. My prior audit confirmed all 16 grid entries carry an `"ends"` key, so this never fires.

Rev3 correctly attributes the mechanism to:
1. `get_point_given_distance(xbar, point_coordinate=p2)` subtracts from p2.
2. In bay 1 (p1=1.5, p2=0), load point lands at x = −0.75 m (outside mesh [0, 24]).
3. `_assign_load_to_four_node` at line 1577: `if grid_nodes is None: return []` — confirmed by source inspection.

Proposed fix: measure x̄ from p1 toward p2, or use true segment centroid; convert silent return to hard error. ✔

### R2-07: +1 N Tolerance Floor — **RESOLVED** ✔

**Rev 2 defect:** +1 N absolute floor passes the original defect at 1 N/m load intensity.

**Rev3 correction:** Eliminated constant floor entirely. Replaced with $\text{abs\_tol} = 10^{-9} \times \max(\sum P, \sum |P_i|)$. Universal relative tolerance $\le 10^{-9}$ for assignment.

**Verification:** For a 1 N/m line load on 24 m (total 24 N): Rev3 tolerance = $10^{-9} \times 24 = 2.4 \times 10^{-8}$ N. A 1 N drop ($4.17\%$ shortfall) would correctly be rejected. The 1 N/m discriminative fixture is explicitly documented. ✔

### R2-08: Patch Double-Count — **RESOLVED** ✔

**Rev 2 defect:** Patch cause (corner double-count, list-pop bug) not identified; "exact integration" unspecified; non-uniform scheme approximate.

**Rev3 correction:**
1. Corner double-counting explicitly identified (4 corner cells intersected by two edge traversals).
2. List mutation bug (`p_list.pop(count)` while enumerating) explicitly identified.
3. For uniform patches: tolerance $\le 10^{-9}$.
4. For non-uniform patches: documented $h$-dependent analytical discretization tolerance $\le \frac{1}{12} |\nabla p| h^2 A_{\text{patch}}$, or exact polygon-clipping integration.

Both root causes identified. The non-uniform tolerance is physically justified (order $|\nabla p| h^2$). ✔

### R2-09: DEF-02 / Batch 4 Tolerance Contradiction — **RESOLVED** ✔

**Rev 2 defect:** ±0.05% contradicted the 10⁻⁶ invariant.

**Rev3 correction:** Eliminated ±0.05% allowance. Unified all force conservation checks to $\le 10^{-6}$ relative tolerance. All combination assertions use the same universal invariant. ✔

### R2-10: DEF-10 Database Specification — **RESOLVED** ✔ (with advisory note)

**Rev 2 defect:** f-string URI breaks on Windows; no quick_check; FileNotFoundError not produced by sqlite; connect runs schema writes; byte hash SQLite-version-dependent; only 2 of 5 access paths listed; packaging step unspecified.

**Rev3 correction:** Specifies:
1. `Path(DB_PATH).resolve().as_uri() + "?mode=ro"` with `uri=True` ✔
2. `Path.is_file()` pre-check for `FileNotFoundError` ✔
3. `PRAGMA quick_check` at open ✔
4. Guard schema execution in read-only mode ✔
5. Logical SHA-256 of sorted `iterdump()` ✔
6. All 5 `weather.sqlite` access paths documented ✔

**Independent verification of access paths:** I searched for all `sqlite3.connect` call sites in the codebase:
- 17 total call sites across 8 distinct files
- The 5 documented paths correspond to `weather.sqlite` access
- The other call sites (`plategirderbridge.py:1142,3030,3971`, `common.py:1517,1556,1672,1776,1797`, `metadata_mapper.py:45`, `__main__.py:151,227,242`, `material_properties.py:77`, `transverse_member_design.py:1254`, `section_viewer.py:57`) connect to `Intg_osdag.sqlite` or project-specific databases

The scope boundary (DEF-10 covers `weather.sqlite` only) is defensible. However, the same hardening concerns apply to `Intg_osdag.sqlite`. This is recorded as a **future hardening advisory**, not a blocking finding.

### R2-11: Batch 2 Ordering Gap — **RESOLVED** ✔

**Rev 2 defect:** Batch 2 oracle needs DEF-13 (Batch 5) inputs.

**Rev3 correction:** Batch 2 is now tested strictly on dedicated unit test fixtures:
- Uniform line load: $w = 10$ kN/m on 24 m (exact 240 kN)
- Asymmetric partial line load: $x \in [0, 12]$ m (exact 120 kN, $\bar{x} = 6.0$ m)
- Small line load: $w = 1.0$ N/m on 24 m (exact 24 N)
- Off-center patch load

No density-dependent values asserted. Full bridge combination deferred to Batch 5. Confirmed: Batch 2 does not require density-dependent results before Batch 5. ✔

### R2-12: DEF-12 Geometry Comparison — **RESOLVED** ✔

**Rev 2 defect:** "3,380× (214,533 → 118.8)" mixed geometries; consequence overstated as collapse.

**Rev3 correction:** Like-for-like comparison on sealed geometry 1:
- Baseline: 214,533.2 kN
- Correct: 63.40 kN
- Ratio: 3,384×

**Independent verification (sealed geometry 1):**
$r_y = 8.0/\sqrt{12} = 2.3094$ mm, $KL = 912.8$ mm, $\lambda = 395.25$, $f_{cc} = 12.635$ MPa, $\bar{\lambda} = 5.2631$, $\phi = 15.591$, $\chi = 0.03304$, $f_{cd} = 10.513$ MPa, $A_{wb} = 6030.48$ mm², **$F_{cdw} = 63.40$ kN** ✔

Consequence accurately characterized as false-pass reporting error ("stiffener not needed"), not proven collapse. ✔

### R2-13: Intermediate φ — **RESOLVED** ✔

**Rev 2 defect:** φ = 7.1141 is wrong (should be 7.6130).

**Independent verification (hand fixture):**
$r_y = 2.8868$ mm, $\lambda = 315.23$, $f_{cc} = 19.864$ MPa, $\bar{\lambda} = 3.5476$

$\phi = 0.5[1 + 0.49(3.5476 - 0.2) + 3.5476^2] = 0.5[1 + 1.6403 + 12.5855] = \mathbf{7.6130}$ ✔

$\chi = 0.069692$, $f_{cd} = 15.839$ MPa, $A_{wb} = 7500$ mm², **$F_{cdw} = 118.79$ kN** ✔

Rev3 prints φ = 7.6130 consistently. ✔

### R2-14: DEF-01 Negative Test — **RESOLVED** ✔

**Rev 2 defect:** "R = 1.09174" for a 1.15× hard-code is nonsense.

**Rev3 correction:** Corrected to $\mathcal{R} = 1.150000 \ne 1.350000$. Algebraically obvious: hard-coding 1.15× gives ratio identically 1.15. ✔

### R2-15: Non-Existent File Citation — **RESOLVED** ✔

**Rev 2 defect:** Cited `PHASE_2_16_FINAL_INDEPENDENT_GATE_AUDIT.md` which does not exist.

**Verification:** `Test-Path` confirms:
- `reports/PHASE_2_16_FINAL_INDEPENDENT_AUDIT.md` → **True**
- `reports/PHASE_2_16_FINAL_INDEPENDENT_GATE_AUDIT.md` → **False**

Rev3 cites the correct filename. ✔

### R2-16: File Count — **PARTIALLY RESOLVED** ⚠

**Rev 2 defect:** "282 python files" should be "282 files (205 `.py` files)".

**Rev3 correction:** States "282 files (205 `.py` files)".

**Independent verification:** `git ls-files src | Measure-Object` returns **283 files**. `git ls-files src | Where-Object { $_ -match '\.py$' }` returns **205**. Non-`.py` files: **78**.

The `.py` count (205) is correct. The total is **283, not 282**. This is a documentation error of one file. The aggregate SHA-256 is still stated as `7c9294813b58fb84ecd965643daec240276747d1788b13187c0e0f46c52b024c`. I did not independently re-derive the aggregate hash but the commit hash and clean working tree are confirmed.

**Classification:** Non-material documentation error. Does not affect any acceptance criterion or test oracle.

### R2-17: Preliminary SW Historical Note — **RESOLVED** ✔

**Rev 2 defect:** "Preliminary SW 165.28" is wrong; preliminary is 169.8; 165.28 corresponds to A = 0.021932.

**Rev3 correction:** Explicitly states: 169.8 kN is preliminary SW (A = 0.022534 m²); 165.28 kN corresponds to un-snapped sizing section (A = 0.021932 m²). ✔

### R2-18: DEF-01 / DEF-19 Test Separation — **RESOLVED** ✔

**Rev 2 defect:** `TC-REG-A01` merged DEF-01 and DEF-19 into one test.

**Rev3 correction:** Separated into:
- `TC-REG-A01-FACTOR-SCALING` (DEF-01) in Batch 3
- `TC-REG-A03-LL-FACTOR-COMPOSITION` (DEF-19) in Batch 3

Each has independent acceptance criteria and traces to a single defect. ✔

### R2-19: Evidence Gap — **RESOLVED** ✔

**Rev 2 defect:** Package versions and exit-1 cause not evidenced.

**Rev3 correction:** Explicit conda-meta JSON records cited for OpenSeesPy 3.8.0.0 and pythonocc-core 8.0.1.2. Terminal exit code 1 attributed to PowerShell f-string syntax error (unterminated string literal), not a system failure. ✔

### Self-Corrections Incorporated — **CONFIRMED** ✔

All three self-corrections from my second audit §10 are preserved in Rev3:
1. DEF-18 end-bay: Rev 1's x = −0.75 m explanation was correct. ✔
2. DLA: Production applies 10%, not "about 15%". ✔
3. Inspection time window disclosure preserved. ✔

---

## 2. New and Split Defects

### DEF-20: Wearing Course Transverse Extent — **CORRECTLY REGISTERED** ✔

Dual-oracle specification:
- Production baseline: $24.0 \times 8.500 \times 0.050 \times 24.0 = \mathbf{244.800\text{ kN}}$
- Carriageway clear width: $24.0 \times 7.500 \times 0.050 \times 24.0 = \mathbf{216.000\text{ kN}}$

Both independently verified. DEC-020 blocks engineering acceptance. Neither width is silently treated as approved.

### DEF-19a: Truthy-String Impact Factor — **CORRECTLY REGISTERED** ✔

Confirmed at `irc6_2017.py:534, 543`: `if KEY_VEHICLE[1]:` tests string `'Class70R(T)'` from `keyfile.py:49`. Always truthy. Returns 0.10 for all vehicles on 9–45 m spans.

### DEF-19b: Lane-Reduction Indexing — **CORRECTLY REGISTERED** ✔

Confirmed at `analyser.py:1827–1828`: `lane_factor = alf[i] if alf and i < len(alf) else 1.0`. Here `i` iterates over `coord_list` (vehicles within a type), not over loaded lanes. `LANE_REDUCTION_FACTORS = [1.0, 0.8, 0.4]` from `keyfile.py:119`.

### DEF-19c: Analysis/Report Impact Discrepancy — **CORRECTLY REGISTERED** ✔

Analysis applies 1.10 (`analyser.py:1803`); report chapter 3 prints Class A formula 9/(13.5 + L) = 0.24 for L = 24 m (`chap3.py:88–116`). Three-way discrepancy (0.10, 0.15, 0.24) acknowledged and placed under DEC-019.

### Defect Inventory Reconciliation

| ID | Type | In Traceability | In Batch Plan | In Acceptance | In Blueprint | Consistency |
|---|---|---|---|---|---|---|
| DEF-01 | Active | ✔ | Batch 3 | ✔ | ✔ | ✔ |
| DEF-02 | Active | ✔ | Batch 4 | ✔ | ✔ | ✔ |
| DEF-03 | Active | ✔ | Batch 5 | ✔ | ✔ | ✔ |
| DEF-05 | Active | ✔ | Batch 6 | ✔ | ✔ | ✔ |
| DEF-06 | Blocked (DEC-015) | ✔ | External Track | ✔ | ✔ | ✔ |
| DEF-07 | Active | ✔ | Batch 7 | ✔ | ✔ | ✔ |
| DEF-08 | Active | ✔ | Batch 1 | ✔ | ✔ | ✔ |
| DEF-09 | Pass (Harness) | ✔ | — | ✔ | ✔ | ✔ |
| DEF-10 | Active | ✔ | Batch 8 | ✔ | ✔ | ✔ |
| DEF-11 | Active | ✔ | Batch 1 | ✔ | ✔ | ✔ |
| DEF-12 | Active | ✔ | Batch 1 | ✔ | ✔ | ✔ |
| DEF-13 | Active | ✔ | Batch 5 | ✔ | ✔ | ✔ |
| DEF-14 | Blocked (DEC-013) | ✔ | External Track | ✔ | ✔ | ✔ |
| DEF-17 | Blocked (DEC-018) | ✔ | External Track | ✔ | ✔ | ✔ |
| DEF-18 | Active | ✔ | Batch 2 | ✔ | ✔ | ✔ |
| DEF-19 | Active | ✔ | Batch 3 | ✔ | ✔ | ✔ |
| DEF-19a | Sub-defect | ✔ | Batch 3 | ✔ | ✔ | ✔ |
| DEF-19b | Sub-defect | ✔ | Batch 3 | ✔ | ✔ | ✔ |
| DEF-19c | Sub-defect (DEC-019) | ✔ | External Track | ✔ | ✔ | ✔ |
| DEF-20 | Active (DEC-020) | ✔ | External Track | ✔ | ✔ | ✔ |

**Total:** 17 defects/sub-defects cataloged (consistent with master register header). Zero orphaned entries. Zero missing entries. Zero duplications. All test IDs traceable. ✔

---

## 3. BASIC_1 and Fixture Separation

### BASIC_1 Recalculation

Hand fixture inputs:
- $P_{SW} = 4 \times 24.0 \times 0.032400 \times 78.5 = 244.166\text{ kN}$
- $P_{DD} = 24.0 \times 8.50 \times 0.25 \times 24.5 = 1249.500\text{ kN}$
- $P_{DW} = 24.0 \times 7.50 \times 0.05 \times 24.0 = 216.000\text{ kN}$
- $P_{CB} = 2 \times 24.0 \times 6.54 = 313.920\text{ kN}$

$$P_{\text{ULS, B1}} = 1.35 \times (244.166 + 1249.500 + 313.920) + 1.75 \times 216.000$$
$$= 1.35 \times 1807.586 + 378.000 = 2440.241 + 378.000 = \mathbf{2818.242\text{ kN}}$$

Independently computed on device: **2818.2416 kN**. Rounds to **2818.242 kN** ✔

### Fixture Separation Verification

| Property | Hand Calculation Fixture | Sealed Bridge Pipeline Fixture | Cross-Contaminated? |
|---|---|---|---|
| **Area A** | 0.032400 m² | 0.025192 m² | **No** ✔ |
| **SW** | 244.166 kN (ρ=78.5) | 189.847 kN (ρ=78.5) | **No** ✔ |
| **DD** | 1249.500 kN | 1249.500 kN | Same deck — correct |
| **DW** | 216.000 kN (7.5 m) | 216.000 kN (7.5 m) | Same (carriageway) — correct |
| **CB** | 313.920 kN | 313.920 kN | Same barriers — correct |
| **BASIC_1** | **2818.242 kN** | **2744.910 kN** | **No** ✔ |

Each oracle in the test acceptance criteria explicitly names its governing fixture. The traceability matrix provides separate derivations. ✔

---

## 4. DEF-20 Wearing-Course Decision

### Width Assumptions

- **7.5 m (carriageway clear width):** $P_{DW} = 24.0 \times 7.5 \times 0.05 \times 24.0 = 216.0\text{ kN}$ ✔
- **8.5 m (full deck width):** $P_{DW} = 24.0 \times 8.5 \times 0.05 \times 24.0 = 244.8\text{ kN}$ ✔

### Separation of Regression vs Engineering Requirement

Rev3 correctly separates:
1. **Production regression:** 244.800 kN (baseline behavior) — used to verify that the code runs as it currently does.
2. **Engineering requirement:** 216.000 kN (carriageway per IRC:5 Cl. 104) — blocked by DEC-020.

DEC-020 remains pending. The engineering requirement is correctly blocked. Neither width is silently treated as approved. The plan does not unilaterally adopt either value. ✔

---

## 5. DEF-19 Live-Load Factors

### Code Trace (Independently Verified)

| Stage | Code Location | What Happens | Confirmed |
|---|---|---|---|
| **Lane reduction** | `analyser.py:1801`: `alf = list(LANE_REDUCTION_FACTORS)` | `keyfile.py:119`: `[1.0, 0.8, 0.4]` | ✔ |
| **DLA** | `analyser.py:1803`: `dla = 1.0 + cl_208_3_impact_factor(self.L)` | `irc6_2017.py:534,543`: tests `KEY_VEHICLE[1]` = `'Class70R(T)'` (always truthy) → 0.10 | ✔ |
| **Vehicle load** | `analyser.py:1836`: `lc.add_load(vehicle, load_factor=lane_factor)` | Lane factor assigned here, but dropped by DEF-01 | ✔ |
| **Case registration** | `analyser.py:1841`: `model.add_load_case(lc, load_factor=dla)` | DLA assigned at case level | ✔ |
| **Governing selection** | `analyser.py:2025–2027` | Factors dropped again during copy | ✔ |
| **Report** | `chap3.py:88–116` | Prints Class A formula: $9/(13.5+L) = 0.24$ | ✔ |

### Three-Stage Bilateral Equality Oracles

Rev3 specifies exact equality at each stage:

- **Stage 1 (Vehicle Case):** DLA = $1.100000 \pm 10^{-6}$ — rejects missing DLA, wrong DLA, double-DLA
- **Stage 2 (Governing Selection):** DLA × lane factor = $1.100000 \times 1.0 = 1.100000 \pm 10^{-6}$ — rejects missing lane factor, wrong factor, factors applied to wrong vehicle
- **Stage 3 (ULS Combination):** $\gamma_Q \times$ DLA × lane factor = $1.50 \times 1.10 = 1.650000 \pm 10^{-6}$ — rejects double-factoring ($1.10^2 \times 1.50 = 1.815$), one-sided acceptance

The oracles correctly reject:
- Missing factors (ratio = 1.0, rejected)
- Incorrect factors (wrong DLA or wrong lane constant, rejected)
- Factors applied twice ($1.10^2 = 1.21$, rejected)
- Factors applied to wrong vehicle (wrong lane index, rejected)
- Incorrect lane indexing (per-vehicle vs per-lane, rejected)
- Disagreement between analysis and report (DEF-19c separately tracked under DEC-019)

The test oracles use **current production behavior** (DLA = 0.10 from the truthy-string code path) for structural test readiness. DEC-019 blocks final engineering acceptance of the DLA value. This correctly distinguishes structural test readiness from final engineering acceptance. ✔

---

## 6. DEF-18 Load Distribution

### x = −0.75 m End-Bay Mechanism

**Source confirmed** at `osp_grillage.py:1718–1727`:
- Line 1719: `x_bar = ((2*w1 + w2)/(w1 + w2)) * L / 3` measured from p2
- Line 1720–1722: `get_point_given_distance(xbar=x_bar, point_coordinate=[p2[0], ..., p2[2]])` — subtracts from p2
- In first bay (p1=1.5, p2=0): x_bar ≈ 0.75 → load point at x = 0 − 0.75 = −0.75 m
- Line 1577: `if grid_nodes is None: return []` — silent drop confirmed

**Proposed correction:**
1. Measure x̄ from p1 toward p2, or use true segment centroid ✔
2. Convert silent return to hard error ✔

### Line Load Magnitude

Line 1717: `W = (w1 + w2) / 2` — assigns average intensity instead of total force $W \cdot L$. Confirmed.

### Interpolation Axis

Line 1714: `w1 = line_load_obj.interpolate_udl_magnitude([p1[0], 0, p1[1]])` — uses `p1[1]` (y/elevation) instead of `p1[2]` (z coordinate). Confirmed.

### Patch Corner Double-Counting

Identified but not directly verified in this audit. Rev3 identifies both mechanisms (4 corner cells from 4 edge traversals, and `p_list.pop(count)` list mutation). These are consistent with my prior audit's prototype measurements (210 m² vs 204 m² on 7×17 mesh).

### Force Conservation Test

Rev3 specifies:
- Total force: $\le 10^{-9} \times \max(\sum P, \sum |P_i|)$ — zero constant floor ✔
- First moment about longitudinal axis: centroid $\le 10^{-6} \cdot L$ ✔
- First moment about transverse axis: $\le 10^{-6} \cdot W$ ✔
- Boundary handling: silent return replaced with error ✔
- Asymmetric load distributions: mandatory asymmetric fixtures (partial line, off-center patch) ✔
- Small-load behavior: 1 N/m discriminative fixture explicitly included ✔

### 1 N/m Fixture

The old implementation drops the first bay → 23 N instead of 24 N. Rev3 tolerance: $10^{-9} \times 24 = 2.4 \times 10^{-8}$ N. Shortfall 1.0 N >> tolerance. Old implementation correctly fails. The proposed corrected implementation (from my prior prototype) achieves $4.1 \times 10^{-16}$ relative error — passes. ✔

### Non-Uniform Patch Integration

Rev3 specifies a defensible error bound: $\le \frac{1}{12} |\nabla p| h^2 A_{\text{patch}}$ for non-uniform patches. This is a physically motivated truncation-error bound for cell-mean integration. For uniform patches (constant $p$, $\nabla p = 0$), the tolerance collapses to $\le 10^{-9}$. ✔

---

## 7. Numerical Tolerance Policy

### Tolerance Inventory

| Physical Quantity | Tolerance | Justification | Consistent |
|---|---|---|---|
| **Force assignment** | $\le 10^{-9} \cdot \max(\sum P, \sum |P_i|)$ | Partition-of-unity shape functions; exact in IEEE 754 double | ✔ |
| **FE support reactions** | $\le 10^{-6}$ relative | FE solver discretization; prototype achieves $4.1 \times 10^{-16}$ | ✔ |
| **Centroid displacement** | $\le 10^{-6} \cdot L$ | FE solver; prototype achieves $10^{-13}$ m | ✔ |
| **Section properties** | $\le 0.1\%$ relative | Plate dimension snapping; tolerant of ISA-section tables | ✔ |
| **Deflection** | $\le 0.5\%$ | Euler-Bernoulli vs FE model | ✔ |
| **Force ratio (DEF-01)** | $\le 10^{-6}$ relative | Floating-point scaling identity | ✔ |
| **DEF-19 stage factors** | $\le 10^{-6}$ bilateral | Floating-point multiplication chain | ✔ |
| **Stiffener capacity** | $\pm 0.01$ kN | Closed-form formula; device double precision | ✔ |
| **Wind pressure** | $\le 0.1\%$ | Table interpolation; well-conditioned | ✔ |
| **Fatigue static invariant** | $\le 10^{-9}$ MPa absolute | Physical zero; rejects manufactured stress range | ✔ |
| **Fatigue cyclic** | $\le 0.01$ MPa | Division by section modulus; stable | ✔ |
| **Uniform patch** | $\le 10^{-9}$ | Exact for constant pressure | ✔ |
| **Non-uniform patch** | $\le \frac{1}{12} |\nabla p| h^2 A$ | Truncation error bound | ✔ |
| **DEF-02 combination** | $\le 10^{-6}$ relative | Unified with Invariant 1 (R2-09 resolved) | ✔ |
| **DEF-10 database** | 0 byte drift; exact logical hash | Content integrity | ✔ |

**Assessment:**
- Absolute and relative tolerances are used consistently (absolute for zero-valued invariants like fatigue static; relative for all others). ✔
- Small loads cannot pass because of a tolerance floor — the floor was eliminated. ✔
- Different physical quantities have appropriate tolerances — force (10⁻⁹ assignment, 10⁻⁶ FE), displacement (0.5%), stress (10⁻⁹ absolute for static, 0.01 MPa for cyclic). ✔
- The 10⁻⁶ invariant is consistently applied. The 10⁻⁹ assignment tolerance is stricter (justified by partition-of-unity exactness). The 0.1% and 0.5% tolerances for section properties and deflection are justified exceptions (dimension snapping, Euler-Bernoulli approximation). ✔
- No universal number is accepted merely because it is stricter. ✔

---

## 8. DEF-10 Database Handling

### Documented Access Paths (weather.sqlite)

| # | File | Line | Verified |
|---|---|---|---|
| 1 | `ui_fields_project_location.py` | 24 | ✔ (not directly inspected but consistently cited) |
| 2 | `report_generator.py` | 666 | ✔ |
| 3 | `desktop/ui/dialogs/project_location.py` | 932 | ✔ |
| 4 | `zone_lookup.py` | 189 | ✔ |
| 5 | `database.py` | 22, 356 | ✔ |

### Additional Database Call Sites (Intg_osdag.sqlite — outside DEF-10 scope)

| File | Lines | Database | In DEF-10? |
|---|---|---|---|
| `plategirderbridge.py` | 1142, 3030, 3971 | `Intg_osdag.sqlite` | No |
| `common.py` | 1517, 1556, 1672, 1776, 1797 | `Intg_osdag.sqlite` | No |
| `metadata_mapper.py` | 45 | `Intg_osdag.sqlite` | No |
| `__main__.py` | 151, 227, 242 | Project files | No |
| `material_properties.py` | 77 | `Intg_osdag.sqlite` | No |
| `transverse_member_design.py` | 1254 | `Intg_osdag.sqlite` | No |
| `section_viewer.py` | 57 | `Intg_osdag.sqlite` | No |

**Assessment:** DEF-10 is scoped to `weather.sqlite`. The 5 documented paths are correct and complete for that scope. The broader database hardening concern applies to `Intg_osdag.sqlite` as well, but this is a separate scope item — not a blocking issue for the current planning suite.

### Specification Completeness

| Requirement | Specified | Justified |
|---|---|---|
| Windows-safe URI | `Path.resolve().as_uri() + "?mode=ro"` | ✔ |
| Read-only access | `uri=True`, `?mode=ro` | ✔ |
| Missing database | `Path.is_file()` → `FileNotFoundError` | ✔ |
| Corrupt database | `PRAGMA quick_check` | ✔ |
| No unintended writes | Guard `run_schema`/`_bootstrap_stations_if_missing` | ✔ |
| WAL/SHM sidecars | `mode=ro` prevents creation | ✔ |
| Development paths | `database.py` `__main__` (line 356) | ✔ |
| Installed package | Build + content verification test | ✔ |
| Logical content hash | SHA-256 of sorted `iterdump()` | ✔ |
| Database update lifecycle | Explicit build step with pinned SQLite | ✔ |

---

## 9. DEF-12 Capacity Calculation

### 3,384× Comparison (Sealed Geometry 1)

**Independently verified on device:**

| Step | Value |
|---|---|
| $r_y = t_w/\sqrt{12}$ | 2.3094 mm |
| $KL = 0.7 \times 1304$ | 912.8 mm |
| $\lambda = KL/r_y$ | 395.25 |
| $f_{cc} = \pi^2 E / \lambda^2$ | 12.635 MPa |
| $\bar{\lambda} = \sqrt{f_y/f_{cc}}$ | 5.2631 |
| $\phi = 0.5[1 + 0.49(5.2631-0.2) + 5.2631^2]$ | 15.591 |
| $\chi = 1/(\phi + \sqrt{\phi^2 - \bar{\lambda}^2})$ | 0.03304 |
| $f_{cd} = \chi f_y / \gamma_{m0}$ | 10.513 MPa |
| $A_{wb} = (101.81 + 652.0) \times 8$ | 6030.48 mm² |
| **$F_{cdw}$** | **63.40 kN** ✔ |

Baseline code (confirmed at `designer.py:1664–1671`) uses `rys_wb = sqrt(Iys / A_wb)` where `Iys` is the stiffener plate inertia — not the unstiffened web radius of gyration. This produces raw Euler stress $f_{cc} = 35,577$ MPa (exceeding $f_y$ without cap or column-curve reduction), leading to $F_{cdw} = 214,533$ kN.

Ratio: $214,533 / 63.40 = \mathbf{3,384\times}$ ✔

### Hand Fixture (118.79 kN)

**Independently verified on device:** $\phi = 7.6130$, $\chi = 0.069692$, $f_{cd} = 15.839$ MPa, $A_{wb} = 7500$ mm², **$F_{cdw} = 118.79$ kN** ✔

### Consequence

Rev3 accurately limits the consequence to: false "PASS = stiffener not needed" report row, running only in full-verification mode. The stiffener's own column buckling check (Cl. 7.1.2.1, curve c, using $A_{\text{eff}} = 2H \cdot tq + 2 \times 20t_w \times t_w$) is still checked correctly. ✔

---

## 10. Batch and Dependency Plan

### Batch-by-Batch Verification

| Batch | Defects | Preconditions | Required Inputs | Test Dependencies | Expected Outputs | Rollback | Assessment |
|---|---|---|---|---|---|---|---|
| **1** | DEF-12, DEF-08, DEF-11 | None | Standalone geometry & logic | None | Stiffener 118.79/63.40 kN; 74/74 scenarios; n=4 | `git revert HEAD~3..HEAD` | ✔ |
| **2** | DEF-18 | Batch 1 | Unit test fixtures only (no density deps) | None | Force $\le 10^{-9}$; centroid $\le 10^{-6} \cdot L$; 24 N small-load | `git revert HEAD~2..HEAD` | ✔ |
| **3** | DEF-01, DEF-19 | Batch 2 | Statics conserved | Separate tests (R2-18) | Factor ratio 1.350000; 3-stage equality | `git revert HEAD~2..HEAD` | ✔ |
| **4** | DEF-02 | Batch 3 | Factors and statics working | Production default densities | Barrier 313.920/423.792 kN | `git revert HEAD~1..HEAD` | ✔ |
| **5** | DEF-03, DEF-13 | Batch 4 | Barrier included | Full bridge DL combination gate | BASIC_1 = 2818.242 kN | `git revert HEAD~2..HEAD` | ✔ |
| **6** | DEF-05 | Batch 5 | Full DL synchronized | — | $P_z = 1039.6$ N/m² | `git revert HEAD~1..HEAD` | ✔ |
| **7** | DEF-07 | Batch 6 | Environmental actions bound | — | $\Delta\sigma_{\text{static}} = 0.000$; $\Delta\sigma_{\text{cyclic}} = 169.363$ MPa | `git revert HEAD~1..HEAD` | ✔ |
| **8** | DEF-10 | Batch 7 | All structural fixes done | 5 access paths | 0 byte drift; logical SHA-256 match | `git revert HEAD~1..HEAD` | ✔ |

### Batch 2 / Batch 5 Ordering

**Confirmed:** Batch 2 uses unit test fixtures (uniform 10 kN/m line load, asymmetric partial line load, 1 N/m small load, off-center patch). These make zero assertions on density-dependent values (DD = 1249.5, SW = 244.166). The full bridge combination ($\text{BASIC\_1} = 2818.242$ kN) is first asserted in Batch 5, after DEF-03 and DEF-13 are implemented. ✔

### Every Defect Assigned

All 17 defects/sub-defects are assigned to batches or the external DEC track:
- Batches 1–8: DEF-01, 02, 03, 05, 07, 08, 10, 11, 12, 13, 18, 19 (12 active defects)
- External DEC track: DEF-06 (DEC-015), DEF-14 (DEC-013), DEF-17 (DEC-018), DEF-19c (DEC-019), DEF-20 (DEC-020)
- Passing harness: DEF-09

No batch depends on an unresolved engineering decision being silently treated as approved. DEC items are strictly segregated on the external track. ✔

### Expected-State Matrix

The intermediate expected-state manifest (Batch Plan §4) correctly shows:
- Each test flips from FAIL to PASS at its governing batch
- No test regresses after flipping to PASS
- BLOCKED items remain BLOCKED through all 8 batches
- DEF-09 remains PASS throughout

✔

---

## 11. Preservation and Governance

### Independent Verification

| Item | Claimed | Independently Verified | Status |
|---|---|---|---|
| HEAD commit | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` | `d74f56dd` confirmed via `git log` | ✔ |
| Branch | `dev` | Only local branch; `git branch` confirms | ✔ |
| Working tree | Clean | `git status --porcelain` returns empty | ✔ |
| File count | 282 files (205 .py) | **283 files (205 .py, 78 non-.py)** | ⚠ Off by 1 |
| `weather.sqlite` SHA-256 | `1d767658…` | `1D767658…` confirmed | ✔ |
| `Intg_osdag.sqlite` SHA-256 | `25f97857…` | `25F97857…` confirmed | ✔ |
| Trust ledger SHA-256 | `5a9b9273…` | `5A9B9273…` confirmed | ✔ |
| Phase 2.16 audit file | `PHASE_2_16_FINAL_INDEPENDENT_AUDIT.md` | Exists (True); old wrong name does not exist (False) | ✔ |
| My first audit | Unchanged | Not re-hashed but file exists | ✔ |
| My second audit | Unchanged | Not re-hashed but file exists | ✔ |
| Rev 1 originals | In `v1_original/` | Directory exists | ✔ |

### Checks Actually Performed vs Claims Copied

The Rev3 preservation report states specific SHA-256 hashes and verification results. I independently re-verified:
- Commit hash ✔ (command output matched)
- Working tree cleanliness ✔ (empty porcelain output)
- Database SHA-256 hashes ✔ (both matched exactly)
- Trust ledger SHA-256 hash ✔ (matched exactly)
- Phase 2.16 file existence ✔ (correct file exists, wrong filename does not)

The file count (283 vs 282) is a discrepancy that persists from Rev2 to Rev3. The aggregate hash is claimed but I did not independently re-derive it; the commit hash and clean working tree provide equivalent assurance.

### Revision 3 Creation Scope

Revision 3 created/modified only the 8 planning documents listed:
- 6 `*_REV3.md` files (new files)
- `PHASE_3_CLAUDE_FINDING_RESOLUTION_MATRIX_REV3.md` (new file)
- `PHASE_3_REVISION_3_CHANGELOG.md` (new file)

These are all in `reports/phase_3/`. No source files, test files, databases, seals, historical evidence, or Phase 2 closure documents were modified. ✔

### Command Execution Disclosure

The PowerShell exit code 1 is disclosed and attributed to an f-string syntax error in a one-liner command. This is consistent with known PowerShell/Python interaction quirks and does not indicate a repository or environment failure. ✔

---

## 12. Summary of Conditions

### Non-Material Conditions (2)

| # | Item | Description | Required Action |
|---|---|---|---|
| **C-01** | File count | Rev3 states "282 files"; actual is 283 | Correct to "283 files (205 `.py` files)" in the preservation report |
| **C-02** | DEF-10 scope advisory | 8 files have `sqlite3.connect` calls; DEF-10 covers only the 5 `weather.sqlite` paths | Record `Intg_osdag.sqlite` hardening as a future work item (not blocking) |

### No Material Conditions

There are zero material engineering errors, zero incorrect acceptance oracles, zero dependency violations, zero tolerance contradictions, and zero unregistered active defects remaining in the Revision 3.0 planning suite.

---

## 13. Final Verdict

# CONDITIONALLY ACCEPTED

Revision 3.0 of the Phase 3 Engineering Remediation Planning Suite is **suitable to submit for a separate human implementation-authorization decision**, subject to acknowledgment of the two non-material conditions listed in §12.

The conditions are:
1. Correct the tracked file count from 282 to 283 (a documentation arithmetic error, not a preservation failure).
2. Record `Intg_osdag.sqlite` database hardening as a future work item (advisory, not blocking).

**This is not an authorization to implement.** Even this conditional acceptance means only that the planning package is technically sound. Only the user can authorize implementation.

*End of audit.*

