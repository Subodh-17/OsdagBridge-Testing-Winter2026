# PHASE 2.5 — Remaining Engineering Blockers & Decision Roadmap

**Date:** 2026-11-16  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`)  
**Controlling Document:** `reports/PHASE_2_4_FINAL_INDEPENDENT_GATE_AUDIT.md`  

---

## 1. Executive Summary

During Phase 2, the test-infrastructure and regression-harness work successfully isolated and reproduced 11 application defects, verified offscreen 3D CAD rendering, and demonstrated 100% sensitivity across all actionable regression tests.

However, three structural engineering items cannot be tested or remediated through test-suite corrections alone because they represent **undecided specifications or unbuilt architectural pipelines**. These items are formally documented as project blockers under decisions **DEC-013**, **DEC-015**, and **DEC-018**. In addition, the **SIDL load factor convention** requires formal engineering ratification before Phase 3 code modification commences.

This document details the mechanical reality, codal context, open design questions, and recommended resolution pathways for each item.

---

## 2. Detailed Technical Profiles of Formal Blockers

### 2.1 DEC-013: Transverse Concrete Deck Slab Representation (`TC-REG-GEO-SLAB`)
- **Associated Defect:** DEF-14
- **Current Baseline Implementation:**
  - `plategirderbridge.py` models transverse grillage members by assigning them half the section properties of the main longitudinal steel girders (`girder/2`, $I_z \approx 0.00367\text{ m}^4$).
  - This is structurally and mechanically invalid: a reinforced concrete deck slab has completely different material stiffness ($E_c \approx 31.6\text{ GPa}$ vs $E_s = 200\text{ GPa}$), Poisson's ratio ($\nu_c = 0.2$ vs $\nu_s = 0.3$), and cross-sectional geometry ($b_{eff} \times t_{slab}$) compared to an I-girder.
- **Open Architectural Questions:**
  1. *Transformed Steel vs. Concrete Section:* Should transverse grillage members be modeled as equivalent transformed steel sections (using modular ratio $m = E_s / E_c \approx 6.33$), or should `ospgrillage` define distinct material models for longitudinal (steel) and transverse (concrete) members?
  2. *Cracked vs. Uncracked Section Modulus:* In composite bridge deck analysis (IRC:22 / IRC:112), should transverse slab stiffness account for tension cracking (e.g., $0.5 I_{gross}$) or use uncracked gross concrete inertia ($I_{gross} = b_{eff} t_{slab}^3 / 12$)?
  3. *Torsional Constant ($J$):* Should the transverse member torsional inertia use the Saint-Venant thin plate approximation ($J = b_{eff} t_{slab}^3 / 6$) or a reduced torsional factor (e.g., 10-20% of gross) to prevent fictitious torsional load paths in 2D grillage?
- **Recommended Phase 3 Resolution:**
  - Adopt standard bridge engineering transformed section properties:
    $$E_{eff} = E_s = 200,000\text{ MPa}$$
    $$b_{eff} = \text{grillage transverse node spacing (e.g., } 1.0\text{ m or } 2.0\text{ m)}$$
    $$I_{trans} = \frac{1}{m} \left( \frac{b_{eff} t_{slab}^3}{12} \right), \quad A_{trans} = \frac{1}{m} (b_{eff} t_{slab})$$
  - Document and ratify this formulation in a formal project decision before implementing in `analyser.py`.

---

### 2.2 DEC-015: Thermal Load Modeling & Interface (`TC-REG-D02`)
- **Associated Defect:** DEF-06
- **Current Baseline Implementation:**
  - `analyser.py:add_temperature_load` attempts to retrieve a key `'temperature_load_kN_m2'` from the thermal analysis dictionary.
  - This key is never populated by `plategirderbridge.py` or the UI input schema.
  - As a result, `temperature_load_case` remains `None`, and thermal effects are never applied to the grillage or combined in ULS/SLS load combinations.
- **Open Codal & Modeling Questions (IRC 6:2017 Cl. 215):**
  1. *Uniform Temperature Range vs. Temperature Gradient:*
     - IRC 6 Cl. 215.2 specifies overall bridge expansion/contraction ($\Delta T = T_{max} - T_{min}$, typically $30^\circ\text{C}$ to $40^\circ\text{C}$ in India).
     - IRC 6 Cl. 215.3 / Fig. 17 specifies non-linear vertical temperature gradient across the composite section (deck heating vs. soffit cooling, $\Delta T_{top} \approx 17.8^\circ\text{C}$).
  2. *Grillage Application Mechanism:*
     - A 2D grillage model cannot directly simulate axial expansion against longitudinal expansion joints unless bearing restraints (fixed vs. free guided) are explicitly defined at abutment nodes.
     - For temperature gradient, the thermal curvature $\kappa = \alpha \Delta T / D$ induces self-equilibrating secondary bending moments and primary hogging/sagging curvatures.
- **Recommended Phase 3 Resolution:**
  - Phase 3 specification must define whether Phase 3 implements:
    - *Option A:* Temperature Gradient secondary moments computed analytically and applied as equivalent nodal moment pairs; or
    - *Option B:* Overall thermal expansion force calculated based on bearing restraint stiffness.
  - Until the structural design lead ratifies the mathematical formulation, `TC-REG-D02` must remain formally blocked.

---

### 2.3 DEC-018: Fatigue Vehicle Moving Load Analysis Pipeline (`TC-REG-C02`)
- **Associated Defect:** DEF-17
- **Current Baseline Implementation:**
  - `designer.py:465-485` erroneously evaluated fatigue stress range $\Delta \sigma$ by subtracting minimum static element moment from maximum static element moment, doubling static values.
  - No code exists in `analyser.py` or `plategirderbridge.py` to create the IRC 6 Cl. 204.6 fatigue vehicle or run moving load influence line analyses for fatigue.
- **Codal Requirements (IRC 6:2017 Cl. 204.6 & IRC 24 / IS 800):**
  - **Vehicle Configuration:** 4-axle 400 kN fatigue truck (Axles: 60 kN, 120 kN, 110 kN, 110 kN; Spacings: 3.6 m, 1.2 m, 4.3 m).
  - **Dynamic Amplification Factor:** Must be explicitly included based on span ($1.0 + 0.15 \times \text{span factor}$).
  - **Analysis:** Vehicle must be moved along critical transverse load lanes across the span to generate maximum and minimum bending moment envelopes ($M_{max,fat}$ and $M_{min,fat}$).
  - **Stress Range:**
    $$\Delta \sigma = \frac{M_{max,fat} - M_{min,fat}}{Z_{composite}}$$
  - **Fatigue Check:**
    $$\Delta \sigma \leq \frac{f_{fd}}{\gamma_{mf}}$$
- **Recommended Phase 3 Resolution:**
  - Implement a dedicated `create_fatigue_load_case()` method in `analyser.py` utilizing `ospgrillage` moving load path capability.
  - Interface the envelope output to `designer.py` for section modulus division.
  - Formally unblock `TC-REG-C02` once this pipeline is designed.

---

### 2.4 SIDL Factor Convention Ratification Status
- **Current Issue:**
  - In `TC-REG-A02-ULS-COMBINATION-SUM`, the ULS combination factor for Superimposed Dead Load (SIDL: Wearing Course, Crash Barrier, Median) was discussed in independent audits:
    - IRC 6:2017 Table B.1 (Basic Combination 1, Ultimate Limit State): Factor $= 1.35$ (for concrete wearing coat) or $1.75$ (for surfacing under adverse condition).
    - Table B.2 specifies varying factors depending on whether SIDL acts as relieving or destabilizing.
  - Baseline `analyser.py` attempted to apply $1.35$ or $1.75$ in `create_uls_combinations()`, but upstream `ospgrillage` ignored the scaling factor.
- **Resolution Path:**
  - In Phase 3, the design configuration dictionary must explicitly allow specifying SIDL factor ($1.35$ vs $1.75$ per project design basis), with $1.35$ as the default verified target in `TC-REG-A02`.

---

## 3. Decision Sign-Off Summary Table

| Blocker ID | Associated Defect | Codal Basis | Resolution Requirement | Prerequisite for Phase 3 Start |
|:---:|:---:|:---:|:---|:---:|
| **DEC-013** | DEF-14 | IRC:22 / IRC:112 | Engineering sign-off on transformed steel section vs concrete material grillage modeling | Architectural Design Complete |
| **DEC-015** | DEF-06 | IRC 6 Cl. 215 | Specification of uniform temperature vs vertical gradient formulation and bearing boundary conditions | Feature Design Complete |
| **DEC-018** | DEF-17 | IRC 6 Cl. 204.6 | Implementation of 40-tonne 4-axle moving load analysis pipeline in `analyser.py` | Pipeline Architecture Designed |
| **SIDL Convention** | DEF-02 | IRC 6 Annex B | Formal ratification of default 1.35 vs 1.75 SIDL factor | Config Parameter Confirmed |
