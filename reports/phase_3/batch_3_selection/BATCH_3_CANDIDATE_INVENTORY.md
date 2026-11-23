# PHASE 3 BATCH 3 — CANDIDATE DEFECT INVENTORY

**Document ID:** P3-B3-INV-001  
**Project:** FOSSEE OsdagBridge — Software Testing & Issue Reporting  
**Phase:** Phase 3 — Engineering Remediation  
**Activity:** Batch 3 Candidate Selection Reconnaissance  
**Date:** 19 November 2026  
**Status:** READ-ONLY RECONNAISSANCE (UNAUTHORIZED)  
**Remediation Branch:** `fix/phase-3-engineering-remediation`  
**Current HEAD:** `9e0b5883a247c8c0fb74b0890915600c7ab4a896`  
**Baseline Anchor:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (`dev`)  
**Batch 2 Status:** FORMALLY CLOSED ([P3-CR-002](file:///F:/FOSSEE%20internship/reports/phase_3/PHASE_3_BATCH_2_CLOSURE_RECORD.md))  

---

## 1. Executive Summary & Objective

This document establishes the comprehensive candidate inventory for **Phase 3 Batch 3**. The objective is to extract, filter, and categorize all remaining unresolved defects from the Phase 3 Defect Traceability Matrix ([PHASE_3_DEFECT_TRACEABILITY_MATRIX_REV3.md](file:///F:/FOSSEE%20internship/reports/phase_3/PHASE_3_DEFECT_TRACEABILITY_MATRIX_REV3.md)), applying rigorous exclusion criteria to identify credible candidates for the next engineering remediation batch.

This investigation is conducted under strict **read-only reconnaissance constraints**. No application source files, test fixtures, or evidence repositories are modified.

---

## 2. Baseline Repository State & Prior Batch Closures

The repository state was forensically verified prior to candidate inventory extraction:

| Parameter | Current Value / Commit Hash | Verification Status |
|:---|:---|:---:|
| **Git Working Tree** | Clean (`nothing to commit, working tree clean`) | **CONFIRMED** |
| **Active Branch** | `fix/phase-3-engineering-remediation` | **CONFIRMED** |
| **Current HEAD** | `9e0b5883a247c8c0fb74b0890915600c7ab4a896` | **CONFIRMED** |
| **Baseline Anchor** | `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (`dev`) | **CONFIRMED** |
| **Batch 1 Status** | Formally Closed ([P3-CR-001](file:///F:/FOSSEE%20internship/reports/phase_3/PHASE_3_BATCH_1_CLOSURE_REPORT.md)) | **CONFIRMED** |
| **Batch 2 Status** | Formally Closed ([P3-CR-002](file:///F:/FOSSEE%20internship/reports/phase_3/PHASE_3_BATCH_2_CLOSURE_RECORD.md)) | **CONFIRMED** |
| **Phase 2 Evidence** | 184 files across 6 HMAC manifests verified intact (27/27 OK) | **CONFIRMED** |

### Commit Chain Preceding Batch 3:
```text
* 9e0b588 (HEAD) fix(ospgrillage): eliminate patch load corner overcounting and iteration mutation bug (DEF-18-PATCH)
* 34cd4bf fix(ospgrillage): correct line load magnitude scaling, vector centroid, and coordinate index (DEF-18-LINE)
* eaba076 fix(designer): align BridgeConfig girder count with physical girders (DEF-11)
* 12493c9 fix(reports): dynamically evaluate component DCRs in executive summary (DEF-08)
* 418fd75 fix(designer): correct bearing stiffener web buckling capacity formula (DEF-12)
* d74f56d (dev) fix: Z,Sa/g,Ah,Av in Report
```

---

## 3. Master Defect Register Status (18 Cataloged Items)

The Phase 3 master defect register currently contains 18 cataloged defects, sub-defects, and latent issues:

| Defect ID | Defect Title | Primary Source Module | Line Range | Current Status |
|:---:|:---|:---|:---:|:---:|
| **DEF-01** | Load Factor Scaling Omission in `ospgrillage` Load Combinations | `src/ospgrillage/osp_grillage.py`<br>`src/ospgrillage/load.py` | 1952–2042<br>1161–1168 | `UNRESOLVED` |
| **DEF-02** | Crash Barrier Superimposed Dead Load Omission in Combinations | `analyser.py`<br>`plategirderbridge.py` | 1532–1558<br>1336–1339 | `UNRESOLVED` |
| **DEF-03** | Section Property Desynchronization Between Snapped Plates and Grillage | `plategirderbridge.py`<br>`initial_sizing.py` | 1260–1277<br>Unverified | `UNRESOLVED` |
| **DEF-05** | Wind Parameter Propagation Loss (Basic Wind Speed, Heights & Terrain) | `plategirderbridge.py`<br>`analyser.py` | 1380–1416<br>1310–1370 | `UNRESOLVED` |
| **DEF-06** | Temperature Load Modeling Omission / Vertical Pressure Fallback | `plategirderbridge.py`<br>`analyser.py` | 1869–1877<br>905–938 | `BLOCKED` (DEC-015) |
| **DEF-07** | Sectional Fatigue Stress Range End-Sign Doubling & Zero-Clamping | `designer.py` | 2976–2996 | `UNRESOLVED` |
| **DEF-08** | Executive Summary Emits Hardcoded Static "Pass" Narrative | `executive_summary.py` | 233–236 | **CLOSED** (Batch 1) |
| **DEF-09** | Offscreen OpenCASCADE Viewport Image Export Verification | Test Environment Harness | 2950–2995 | **PASS** (Harness) |
| **DEF-10** | Reference Database Runtime Materialization & Package Tree Mutation | `database.py`<br>`ui_fields_project_location.py` | 12–30, 356<br>16–29 | `UNRESOLVED` |
| **DEF-11** | Girder Count Geometry Misalignment (Edge Lines Counted in Config) | `designer.py`<br>`plategirderbridge.py` | 401, 413<br>1112–1115 | **CLOSED** (Batch 1) |
| **DEF-12** | Bearing Stiffener Web Buckling Capacity Formula Anomaly | `designer.py` | 1664–1672 | **CLOSED** (Batch 1) |
| **DEF-13** | Hardcoded Structural Steel and Deck Concrete Density Propagation | `analyser.py`<br>`plategirderbridge.py` | 10, 416<br>1332–1333 | `UNRESOLVED` |
| **DEF-14** | Transverse Concrete Deck Slab Assigned Steel Girder Properties | `plategirderbridge.py` | 1279–1291 | `BLOCKED` (DEC-013) |
| **DEF-17** | Fatigue Vehicle Moving Load Analysis Pipeline Omission | `analyser.py`<br>`designer.py` | 1612–1660<br>2972–2985 | `BLOCKED` (DEC-018) |
| **DEF-18** | Non-Conservation of Static Load Equilibrium & End-Bay Drop | `src/ospgrillage/osp_grillage.py` | 1576–1579<br>1674–1729, 1795–1858 | **CLOSED** (Batch 2) |
| **DEF-19a** | `cl_208_3` Truthy String Check Hardcoding 0.10 Impact for All Vehicles | `irc6_2017.py` | 534, 543 | `UNRESOLVED` |
| **DEF-19b** | Lane Reduction Factors Indexed Per-Vehicle Within Type, Not Per Lane | `analyser.py`<br>`keyfile.py` | 1827–1828<br>119 | `UNRESOLVED` |
| **DEF-19c** | Analysis Code (0.10) vs Report Chapter 3 (0.24) Impact Discrepancy | `analyser.py`<br>`chap3.py` | 1803<br>88–116 | `BLOCKED` (DEC-019) |
| **DEF-20** | Wearing Course Transverse Extent (Full Deck vs Carriageway Clear Width) | `plategirderbridge.py`<br>`load_placement.py` | 1334<br>133–139 | `BLOCKED` (DEC-020) |
| **DEF-LATENT-ZP** | Transverse Coordinate Indexing in Line Load Intensity Interpolation | `src/ospgrillage/load.py` | 710 | `UNRESOLVED` (Latent) |

---

## 4. Exclusion Analysis

To ensure strict focus and risk mitigation, defects must be systematically evaluated against the project exclusion criteria:

### 4.1 Category A: Closed Defects (Excluded)
The following defects were remediated, verified by independent audit, and formally closed:
- **DEF-12:** Bearing stiffener web buckling formula anomaly (closed in Batch 1 via commit `418fd75`).
- **DEF-08:** Dynamic executive summary status derivation (closed in Batch 1 via commit `12493c9`).
- **DEF-11:** BridgeConfig girder count alignment (closed in Batch 1 via commit `eaba076`).
- **DEF-18:** Grillage statics conservation (closed in Batch 2 via commits `34cd4bf` and `9e0b588`).

### 4.2 Category B: Non-Defect Passing Verification (Excluded)
- **DEF-09:** Offscreen OpenCASCADE Viewport Image Export is a test-environment verification item that already evaluated to `PASS` in baseline regression. No source code changes are required.

### 4.3 Category C: Blocked by Unratified Engineering Decisions (Excluded)
In accordance with Project Governance Protocol, defects requiring architectural or standards decisions cannot be scheduled into an engineering implementation batch until formal written sign-off is granted by the human engineering director:
- **DEF-06 (Temperature Load Modeling):** Blocked pending **DEC-015** (thermal action specification for composite superstructures).
- **DEF-14 (Transverse Concrete Deck Slab Properties):** Blocked pending **DEC-013** (transverse slab stiffness modeling, effective width, and modular ratio).
- **DEF-17 (Fatigue Vehicle Moving Load Pipeline):** Blocked pending **DEC-018** (fatigue vehicle moving load pass specification).
- **DEF-19c (Impact Formula Discrepancy):** Blocked pending **DEC-019** (Class A composite superstructure impact factor alignment).
- **DEF-20 (Wearing Course Transverse Extent):** Blocked pending **DEC-020** (carriageway clear width $7.5\text{ m}$ vs total deck width $8.5\text{ m}$).

---

## 5. Eligible Candidate Pool for Phase 3 Batch 3

Applying the exclusion filters yields a clean candidate pool of **9 distinct candidates / sub-defects (C1 through C9)**:

| Candidate ID | Defect Title | Target Module | Severity | DAG Step | Primary Prerequisite |
|:---:|:---|:---|:---:|:---:|:---|
| **C1: DEF-01** | Load Factor Scaling Omission in `ospgrillage` Load Combinations | `src/ospgrillage/osp_grillage.py`<br>`src/ospgrillage/load.py` | **Critical** | Step 3 | DEF-18 (Batch 2, CLOSED) |
| **C2: DEF-LATENT-ZP** | Transverse Coordinate Indexing in Line Load Intensity Interpolation | `src/ospgrillage/load.py` | **Medium** (Latent) | Post-B2 | None (Isolated line in `load.py`) |
| **C3: DEF-02** | Crash Barrier Superimposed Dead Load Omission in Combinations | `analyser.py`<br>`plategirderbridge.py` | **Critical** | Step 4 | Independent for DL; DEF-01 for multi-factor ULS |
| **C4: DEF-03** | Section Property Desynchronization (Snapped vs Initial) | `plategirderbridge.py` | **Critical** | Step 5 | DEF-02, DEF-13 |
| **C5: DEF-05** | Wind Parameter Propagation Loss | `analyser.py`<br>`plategirderbridge.py` | **High** | Step 6 | None |
| **C6: DEF-07** | Sectional Fatigue Stress Range Sign Doubling & Zero-Clamping | `designer.py` | **Critical** | Step 7 | Analysis forces |
| **C7: DEF-10** | Reference Database Read-Only Packaging & Access Paths | `database.py` (5 paths) | **Medium** | Step 8 | None (Decoupled from FE) |
| **C8: DEF-13** | Hardcoded Structural Steel and Concrete Densities | `analyser.py`<br>`plategirderbridge.py` | **Medium** | Step 5 | DEF-03 |
| **C9: DEF-19** (19a/b) | Live-Load Factor Composition (Lane Reduction & Impact) | `analyser.py`<br>`irc6_2017.py` | **High** | Step 3 | DEF-01 (Component factor preservation) |

---

## 6. Next Steps

These eligible candidates will be evaluated in [BATCH_3_DEFECT_PRIORITIZATION.md](file:///F:/FOSSEE%20internship/reports/phase_3/batch_3_selection/BATCH_3_DEFECT_PRIORITIZATION.md) using the 5-dimension weighted scoring rubric to identify the primary and backup recommendations for Phase 3 Batch 3.
