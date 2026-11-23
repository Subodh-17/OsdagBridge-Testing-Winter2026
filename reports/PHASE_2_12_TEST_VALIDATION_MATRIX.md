# Phase 2.12 — Test Validation and Sensitivity Matrix

**Date:** 2026-11-17  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`, 100% clean)  
**Controlling Document:** `reports/PHASE_2_11_FINAL_INDEPENDENT_GATE_AUDIT.md` (by independent auditor Claude)  
**Execution Mode:** Baseline Regression & Sensitivity Matrix (Mode: Strict Tri-State)  
**Evidence Root:** `testing\evidence\phase_2_12\`  
**Authoritative Trust Store:** `~/.osdagbridge_trust` (`C:\Users\Subodh\.osdagbridge_trust`)  

---

## 1. Master Validation Matrix (All 15 Tests)

| # | Test Identifier | Defect ID | Baseline Expected | Baseline Observed | Manifest Match | Cand. (b) Correct | Cand. (c) Naive | Sensitivity Verdict | Gate Status |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | `TC-REG-A01-FACTOR-SCALING` | DEF-01 (Upstream) | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 2 | `TC-REG-B01-SECTION-PROPERTY-SYNC` | DEF-03 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 3 | `TC-REG-C01-SECTIONAL-STRESS-RANGE` | DEF-07 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 4 | `TC-REG-A02-ULS-COMBINATION-SUM` | DEF-01 / DEF-02 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 5 | `TC-REG-EQ-LOAD-CONSERVATION` | DEF-18 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 6 | `TC-REG-D01-WIND-SPEED-PROPAGATION` | DEF-05 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 7 | `TC-REG-D02-TEMPERATURE-PROPAGATION` | DEF-06 | BLOCKED | BLOCKED | MATCH | BLOCKED | BLOCKED | **BLOCKED** | DEC-015 |
| 8 | `TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS` | DEF-17 | BLOCKED | BLOCKED | MATCH | BLOCKED | BLOCKED | **BLOCKED** | DEC-018 |
| 9 | `TC-REG-RPT-EXEC-SUMMARY-STATUS` | DEF-08 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 10 | `TC-REG-GEO-GIRDER-COUNT-ALIGNMENT` | DEF-11 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 11 | `TC-REG-GEO-SLAB-SECTION-PROPERTIES` | DEF-14 | BLOCKED | BLOCKED | MATCH | BLOCKED | BLOCKED | **BLOCKED** | DEC-013 |
| 12 | `TC-REG-CAP-STIFFENER-BUCKLING` | DEF-12 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 13 | `TC-REG-MAT-DENSITY-CONSISTENCY` | DEF-13 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 14 | `TC-REG-FS-CLEAN-WORKING-TREE` | DEF-10 | BASELINE_FAIL | BASELINE_FAIL | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |
| 15 | `TC-REG-CAD-EXPORT-VS-SCREENSHOT` | DEF-09 (Harness) | PASS | PASS | MATCH | PASS | BASELINE_FAIL | **VERIFIED** | PASSED |

### Summary Statistics
- **Total Registered Regression Tests:** **15**
- **Actionable Tests Evaluated:** **12**
- **Actionable Tests Verified (100% Tri-State Discrimination):** **12 / 12 (100.0%)**
- **Actionable Tests Unverified:** **0 / 12 (0.0%)**
- **Formally Blocked Specifications:** **3 / 15** (`TC-REG-D02`, `TC-REG-C02`, `TC-REG-GEO-SLAB`)
- **Manifest Alignment Accuracy:** **15 / 15 (100.0% Exact Match)**
- **Baseline Execution Duration:** **25.59 s**
- **Sensitivity Matrix Duration:** **66.80 s**
- **Post-Manifest Verification:** **SUCCESS (0 file drift across all directories)**
- **Overall Actionable Sensitivity Gate:** **PASSED**

---

## 2. Technical Sensitivity Profiles for Verified Priority Tests

### 1. TC-REG-EQ-LOAD-CONSERVATION (DEF-18)
- **Defect Mechanism:** Baseline grillage load distribution violates vertical static equilibrium and transverse tributary load sharing. Barrier lines deviate by $-37.5\%$ ($98.1\text{ kN}$ vs $157.0\text{ kN}$ per line), with centroid shifted longitudinally by $+0.750\text{ m}$. Deck slab (DD) and wearing course (DW) deviate from tributary nodal vectors.
- **Oracle Formulation:**
  - Barrier load magnitude derived from genuine input key `bridge.input_dict.get("crash_barrier_load")` (or $6.54\text{ kN/m}$ default).
  - Barrier width derived from production `DEFAULT_CRASH_BARRIER_WIDTH = 0.50\text{ m}`.
  - Expected barrier line coordinates: $z_{\text{left}} = 0.250\text{ m}$, $z_{\text{right}} = 8.250\text{ m}$.
  - Expected tributary line shares: Line 0 ($z=0.00\text{ m}$) = $76.19\%$, Line 1 ($z=1.05\text{ m}$) = $23.81\%$.
  - Tributary nodal vector error tolerance: $\le 0.5\%$ ($0.005$).
- **Tri-State Sensitivity:**
  - **(a) Baseline:** `BASELINE_FAIL` — Force shortfall $-37.5\%$, centroid shift $+0.75\text{ m}$, DW rel_err $19.43\%$.
  - **(b) Minimal Correct (`6bba254e4943`):** `PASS` — Both vertical resultants and moment centroids conserved exactly ($x = 12.0\text{ m}$, $z = 4.25\text{ m}$), transverse shares match ($76.19\% / 23.81\%$), nodal vector error $0.00\%$.
  - **(c) Plausible Wrong (`3e3aee4700eb`):** `BASELINE_FAIL` — Corrects patch loads (DD, DW), but omits barrier distribution, failing barrier force ($-37.5\%$) and centroid.
- **Verdict:** **VERIFIED**

### 2. TC-REG-C01-SECTIONAL-STRESS-RANGE (DEF-07)
- **Defect Mechanism:** Evaluates static load case as cyclic fatigue load, producing false cyclic stress ranges ($\Delta\sigma = 125.46\text{ MPa}$ on static load).
- **Oracle Formulation:**
  - Dynamic multi-girder fixture:
    - Girder 1 Element 1 End $i$: Static $M_z = 2900\text{ kNm}$, stress range $\Delta\sigma = 181.914\text{ MPa}$.
    - Girder 2 Element 5 End $j$: Static $M_z = 3200\text{ kNm}$, stress range $\Delta\sigma = 200.733\text{ MPa}$ (governing envelope).
  - Tolerance: Tightened to `rel_tol = 0.008` (0.8%).
- **Tri-State Sensitivity:**
  - **(a) Baseline:** `BASELINE_FAIL` — Non-zero stress range on static load case.
  - **(b) Minimal Correct (`fed2e878b2a0`):** `PASS` — Evaluates static load to $0.0\text{ MPa}$; evaluates G1 End $i$ to $181.91\text{ MPa}$ and G2 End $j$ to $200.73\text{ MPa}$.
  - **(c) Plausible Wrong (`3603a779d3a2`):** `BASELINE_FAIL` — Evaluates only Girder 1 ($181.91\text{ MPa}$), missing governing G2 ($200.73\text{ MPa}$).
- **Verdict:** **VERIFIED**

### 3. TC-REG-B01-SECTION-PROPERTY-SYNC (DEF-03)
- **Defect Mechanism:** Solver-side girder sections deviate from dynamically snapped plate properties ($I_z, A, I_y, J$). Inconsistent depth geometry: $D = 1340.0\text{ mm} \ne d_w + t_{ft} + t_{fb} = 1342.0\text{ mm}$.
- **Oracle Formulation:**
  - Dynamic derivation from snapped plate dimensions: $A = 0.022534\text{ m}^2$, $I_z = 0.0073409\text{ m}^4$, $I_y = 0.0001963\text{ m}^4$, $J = 1.3414\times 10^{-6}\text{ m}^4$.
  - Verification includes bottom flange width ($b_{fb} = 410\text{ mm}$).
- **Tri-State Sensitivity:**
  - **(a) Baseline:** `BASELINE_FAIL` — Depth discrepancy and unsynchronized sections.
  - **(b) Minimal Correct (`f68b30ff8056`):** `PASS` — All sectional properties synchronize within $0.01\%$.
  - **(c) Plausible Wrong (`b564a14cef5a`):** `BASELINE_FAIL` — Synchronizes depth but leaves flange width out of sync.
- **Verdict:** **VERIFIED**

### 4. TC-REG-A02-ULS-COMBINATION-SUM (DEF-01 / DEF-02)
- **Defect Mechanism:** Dead load combinations omit load factor scaling, resulting in un-factored load combination resultants.
- **Oracle Formulation:**
  - Dynamic independent physical derivation:
    $$W_{\text{applied,ULS}} = 1.35(W_{SW} + W_{DD} + W_{CB}) + 1.75(W_{DW}) = 2711.74\text{ kN}$$
  - Evaluates genuine `crash_barrier_load` directly from `bridge.input_dict`.
- **Tri-State Sensitivity:**
  - **(a) Baseline:** `BASELINE_FAIL` — Total resultant is un-factored ($1944.70\text{ kN}$).
  - **(b) Minimal Correct (`a46aeb4db0f8`):** `PASS` — Scaled resultant equals $2711.74\text{ kN}$.
  - **(c) Plausible Wrong (`fd02171e9f08`):** `BASELINE_FAIL` — Partial combination omitting component factor.
- **Verdict:** **VERIFIED**
