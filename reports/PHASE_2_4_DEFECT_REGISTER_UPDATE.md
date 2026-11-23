# PHASE 2.4 — Defect Register Formal Update

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Software Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Repository Baseline:** `source/OsdagBridge` (`dev` at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`)  
**Controlling Audit:** `reports/PHASE_2_3_FINAL_INDEPENDENT_GATE_AUDIT.md`  
**Date:** 2026-11-16  

---

## 1. Overview of Defect Register Amendments

This document formalizes all updates to the OsdagBridge Defect Register resulting from the Phase 2.3 Independent Gate Audit and the Phase 2.4 regression suite remediation campaign.

### Key Modifications in Phase 2.4:
1. **Registration of DEF-18 (Static Equilibrium Non-Conservation):** Formally cataloged critical defect DEF-18 discovered during independent audit §1 & §2, where `ospgrillage` finite element load distribution drops $37.5\%$ of crash barrier load and inflates deck/wearing course loads by $+3.088\%$, causing a net loss of $70.78\text{ kN}$ of dead load.
2. **Defect Status Ratification (DEF-17 / DEC-018):** Formally updated DEF-17 to reflect that OsdagBridge has no implementation linking the IRC 6 Cl. 204.6 fatigue vehicle moving load to finite element analysis or `designer.py` demand extraction, establishing DEC-018 as a formal blocker.
3. **Defect Oracle Clarifications (DEF-03, DEF-07, DEF-08, DEF-10, DEF-13):** Replaced preliminary or proxy thresholds with rigorous structural mechanics oracles and verified production keys.

---

## 2. New Defect Registration: DEF-18

### DEF-18: Non-Conservation of Static Load Equilibrium in FE Grillage Load Distribution
- **Defect Identifier:** `DEF-18`
- **Associated Test Case:** `TC-REG-EQ-LOAD-CONSERVATION`
- **Severity:** **Critical**
- **Classification:** **CONFIRMED** (Empirically verified via OpenSees node reaction extraction)
- **Module / Subsystem:** `ospgrillage.osp_grillage.OspGrillage` (vendored fork)
- **Source Location:** `src/ospgrillage/osp_grillage.py:910–1080` (`_assign_line_to_four_node` and `_assign_patch_load`)
- **Upstream vs. Application Origin:** Upstream library defect (`ospgrillage`) residing within OsdagBridge's modified vendored fork.

#### Source-Level Mechanism Evidence:
1. **Line Load Magnitude & Segment Assignment Failure (`_assign_line_to_four_node`):**
   - For line loads not exactly colinear with longitudinal grid lines (such as crash barrier lines located at $z = 0.25\text{ m}$ and $z = 8.25\text{ m}$ across a $24.0\text{ m}$ span), the function intersects line segments with the mesh grid.
   - For each intersected grid cell, the load magnitude assigned to equivalent point loads is set to `mag = W` (force per unit length in N/m) instead of multiplying by the segment length $L_i$ ($W \times L_i$).
   - End-point offset coordinate subtraction places boundary load coordinates at $x = -0.75\text{ m}$, outside the mesh boundary ($x \in [0.0, 24.0]$), causing OpenSees to drop boundary segments.
   - For two crash barriers applied at $6.54\text{ kN/m}$ across $24.0\text{ m}$ ($P_{\text{applied}} = 313.92\text{ kN}$), exactly 30 segments $\times 6.54\text{ kN} = 196.20\text{ kN}$ are assigned to OpenSees. The support reaction is $196.20\text{ kN}$, losing $-117.72\text{ kN}$ ($-37.5\%$).
2. **Patch Load Polygon Area Integration Failure (`_assign_patch_load`):**
   - Bounded and intersecting polygon tributary integration over the mesh grid sums to an effective integration area of $210.3\text{ m}^2$ instead of the true geometric bridge deck area of $204.0\text{ m}^2$ ($24.0\text{ m} \times 8.5\text{ m}$).
   - This scales deck slab load ($P_{\text{applied}} = 1275.00\text{ kN}$) upwards to $R_{DD} = 1314.38\text{ kN}$ ($+3.088\%$).
   - This scales wearing course load ($P_{\text{applied}} = 244.80\text{ kN}$) upwards to $R_{DW} = 252.36\text{ kN}$ ($+3.088\%$).

#### Behavioral Runtime Evidence:
- Under pristine baseline execution, the total physical dead load applied across all four components is:
  $$\sum P_{\text{applied}} = P_{SW} + P_{DD} + P_{DW} + P_{Barrier} = 169.82 + 1275.00 + 244.80 + 313.92 = 2003.54\text{ kN}$$
- The sum of vertical support reactions extracted from OpenSees nodes is:
  $$\sum R_y = R_{SW} + R_{DD} + R_{DW} + R_{Barrier} = 169.82 + 1314.38 + 252.36 + 196.20 = 1932.76\text{ kN}$$
- **Net Lost Load:** $70.78\text{ kN}$ ($3.53\%$ of total bridge dead weight). Static equilibrium ($\sum F_y = 0$) is violated.

---

## 3. Detailed Status & Oracle Updates for Existing Defects

### DEF-01 / DEF-02: ULS Combination Load Factor Omission & Barrier SIDL Omission
- **Associated Tests:** `TC-REG-A01-FACTOR-SCALING`, `TC-REG-A02-ULS-COMBINATION-SUM`
- **Status:** **CONFIRMED**
- **Updates in Phase 2.4:**
  - `TC-REG-A02` reaction target updated: replaced circular self-referential target ($2710.17\text{ kN}$) with theoretical applied dead load resultant ($2802.70\text{ kN}$) and dynamic run-time component superposition target ($1.35 \times [R_{SW} + R_{DD} + R_{Barrier}] + 1.75 \times R_{DW} = 2710.17\text{ kN}$).
  - Added direct barrier load force differential check:
    $$\Delta R_{\text{barrier}} = R_{\text{BASIC\_1}} - [1.35 \times (R_{SW} + R_{DD}) + 1.75 \times R_{DW}] = 0.0\text{ kN (Baseline)} \quad \text{vs} \quad 264.87\text{ kN (Expected)}$$
  - Added element internal shear ($V_{y, B1} = 1.35 V_{y, DL} + 1.75 V_{y, DW}$) and moment ($M_{z, B1} = 1.35 M_{z, DL} + 1.75 M_{z, DW}$) superposition assertions. Baseline confirms solver evaluates un-factored $1.0\text{DL} + 1.0\text{DW}$ ($V_y \text{ error} = 0.0\text{ N}$).

### DEF-03: Section Property Synchronization & Structural Grillage Oracle
- **Associated Test:** `TC-REG-B01-SECTION-PROPERTY-SYNC`
- **Status:** **CONFIRMED**
- **Updates in Phase 2.4:**
  - Clarified theoretical single-beam Euler-Bernoulli reference: $\delta = P L^3 / (48 E I_z) = 18.164\text{ mm}$.
  - Clarified calibrated 3D grillage structural oracle: $\delta_{\text{grillage}} = 7.218\text{ mm}$ (accounting for load distribution across 4 longitudinal girders, 7 cross-beams, and diaphragm boundary conditions).
  - In baseline: solver elements retain preliminary sizing ($I_z = 0.0073409\text{ m}^4 \ne 0.0079276\text{ m}^4$), resulting in $7.816\text{ mm}$ deflection ($+8.3\%$ discrepancy).

### DEF-07: Sectional Stress Range Doubling & Fatigue Capacity Alignment
- **Associated Test:** `TC-REG-C01-SECTIONAL-STRESS-RANGE`
- **Status:** **CONFIRMED**
- **Updates in Phase 2.4:**
  - Removed arbitrary magic divisor $31.77\text{ MPa}$.
  - Linked test to authentic application capacity calculator `IRC22CapacityCalculator.compute_fatigue()`, yielding code-defined capacity $f_{fd,eff} = 92.491\text{ MPa}$ under IRC 22:2014 Cl. 605.4 ($N_{sc} = 5,000,000$ cycles).
  - Evaluated static load case ($M_0 = 1000\text{ kNm}$): physical stress range is $0.0\text{ MPa}$ ($\text{DCR} = 0.0$). Baseline yields envelope range $125.46\text{ MPa}$ (sign doubling) and per-LC range $62.73\text{ MPa}$ (evaluating static moment as range).
  - Evaluated positive cyclic load case ($M_{min} = 500\text{ kNm}$, $M_{max} = 1500\text{ kNm}$): true cyclic range is $62.729\text{ MPa}$ ($\text{DCR} = 0.6782$).

### DEF-08: Executive Summary Hardcoded Outcomes & Multi-Girder Masking
- **Associated Test:** `TC-REG-RPT-EXEC-SUMMARY-STATUS`
- **Status:** **CONFIRMED**
- **Updates in Phase 2.4:**
  - `test_tc_reg_rpt_status` systematically sanitizes all girders (G1–G6) in `per_girder` across all 6 scenarios, eliminating masked G2–G6 Phase 1D failure records.
  - Candidate (b) dynamically evaluates girder status across all non-EB girders and all 3 substructure components.

### DEF-10: Untracked `weather.sqlite` Creation & Package Directory Mutation
- **Associated Test:** `TC-REG-FS-CLEAN-WORKING-TREE`
- **Status:** **CONFIRMED**
- **Updates in Phase 2.4:**
  - Dropped static path-string checks (`is_inside_package`).
  - Implemented empirical before/after SHA-256 hash comparisons across all package files under production `@_with_db` query execution.
  - Asserted unanchored `Database()` default constructor creating `weather.sqlite` in `os.getcwd()`.

### DEF-13: Hardcoded Material Density and Barrier Load Conflicts
- **Associated Test:** `TC-REG-MAT-DENSITY-CONSISTENCY`
- **Status:** **CONFIRMED**
- **Updates in Phase 2.4:**
  - Injected density through authentic production key `material.girder.density` ($70.0\text{ kN/m}^3$).
  - Derived independent expected resultant: $P_{SW} = 4 \times 24.0 \times 0.0225344 \times 70.0 = 151.431\text{ kN}$.
  - Baseline execution confirms hardcoded $78.5\text{ kN/m}^3 \implies 169.819\text{ kN}$.

### DEF-17: Fatigue Vehicle Defined but Never Analysed in Grillage (DEC-018)
- **Associated Test:** `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS`
- **Status:** **CONFIRMED (FORMAL BLOCKER under DEC-018)**
- **Updates in Phase 2.4:**
  - Verified that OsdagBridge has no implementation to generate a moving load case for the IRC 6 fatigue vehicle, nor does `designer.py` extract fatigue demands from moving load cases.
  - Formally classified as `BLOCKED` on baseline and `BLOCKED / NOT DEMONSTRATED` in sensitivity matrix.

---

## 4. Complete Defect Inventory Table (Phase 2.4 Baseline)

| Defect ID | Defect Title | Severity | Upstream / OsdagBridge | Baseline Test Case | Baseline Observed Status | Sensitivity Verification |
| :---: | :--- | :---: | :---: | :--- | :---: | :---: |
| **DEF-01** | Load factors omitted in `ospgrillage` combination solve | Critical | Upstream (`ospgrillage`) | `TC-REG-A01-FACTOR-SCALING` | `BASELINE_FAIL` | **VERIFIED** |
| **DEF-02** | Crash barrier SIDL omitted from combinations | High | OsdagBridge | `TC-REG-A02-ULS-COMBINATION-SUM` | `BASELINE_FAIL` | **VERIFIED** |
| **DEF-03** | Grillage analysis section differs from designed section | Critical | OsdagBridge | `TC-REG-B01-SECTION-PROPERTY-SYNC` | `BASELINE_FAIL` | **VERIFIED** |
| **DEF-04** | Mesh geometry & edge beam stiffness discrepancy | High | OsdagBridge | `TC-REG-B01-SECTION-PROPERTY-SYNC` | `BASELINE_FAIL` | **VERIFIED** |
| **DEF-05** | Wind parameters ignored (fallback to 33 m/s) | High | OsdagBridge | `TC-REG-D01-WIND-SPEED-PROPAGATION` | `BASELINE_FAIL` | **VERIFIED** |
| **DEF-06** | Temperature load input key missing (silent skip) | High | OsdagBridge | `TC-REG-D02-TEMPERATURE-PROPAGATION` | `BLOCKED` | **BLOCKED (DEC-015)** |
| **DEF-07** | Fatigue stress range doubled via member sign flip | Critical | OsdagBridge | `TC-REG-C01-SECTIONAL-STRESS-RANGE` | `BASELINE_FAIL` | **VERIFIED** |
| **DEF-08** | LaTeX report hardcoded outcomes & figure gap | Medium | OsdagBridge | `TC-REG-RPT-EXEC-SUMMARY-STATUS` | `BASELINE_FAIL` | **VERIFIED** |
| **DEF-09** | Blank CAD screenshot via Qt buffer grab | Medium | Test Harness | `TC-REG-CAD-EXPORT-VS-SCREENSHOT` | `PASS` | **VERIFIED** |
| **DEF-10** | Untracked `weather.sqlite` created in source tree | Low | OsdagBridge | `TC-REG-FS-CLEAN-WORKING-TREE` | `BASELINE_FAIL` | **VERIFIED** |
| **DEF-11** | Grillage edge lines included in girder design loop | High | OsdagBridge | `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` | `BASELINE_FAIL` | **VERIFIED** |
| **DEF-12** | Bearing stiffener web buckling capacity anomaly | Medium | OsdagBridge | `TC-REG-CAP-STIFFENER-BUCKLING` | `BASELINE_FAIL` | **VERIFIED** |
| **DEF-13** | Hardcoded material density and barrier load conflicts | Medium | OsdagBridge | `TC-REG-MAT-DENSITY-CONSISTENCY` | `BASELINE_FAIL` | **VERIFIED** |
| **DEF-14** | Deck slab transverse members take steel properties | High | OsdagBridge | `TC-REG-GEO-SLAB-SECTION-PROPERTIES` | `BLOCKED` | **BLOCKED (DEC-013)** |
| **DEF-15** | Report Table 5.12 girder labels mapped to grillage lines | Medium | OsdagBridge | Report Generator Audit | `STATIC_CONFIRMED` | Planned Phase 3 |
| **DEF-16** | Live load combination term discrepancy | Medium | OsdagBridge | Combination Math Audit | `STATIC_CONFIRMED` | Planned Phase 3 |
| **DEF-17** | Fatigue vehicle defined but never analysed in grillage | Critical | OsdagBridge | `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS` | `BLOCKED` | **BLOCKED (DEC-018)** |
| **DEF-18** | Non-conservation of static load equilibrium | Critical | Upstream (`ospgrillage`) | `TC-REG-EQ-LOAD-CONSERVATION` | `BASELINE_FAIL` | **VERIFIED** |
