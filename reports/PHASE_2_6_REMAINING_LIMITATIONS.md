# PHASE 2.6 — Remaining Engineering Limitations & Architectural Roadmap

**Date:** 2026-11-16  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Branch `dev`)  
**Controlling Document:** `reports/PHASE_2_5_FINAL_INDEPENDENT_GATE_AUDIT.md`  

---

## 1. Executive Summary

With the completion of Phase 2.6, all 12 actionable regression tests are mathematically rigorous, structurally defensible, and 100% sensitive to subtle structural errors (rejecting naive implementations and accepting genuine fixes).

However, structural engineering software QA requires transparently documenting remaining engineering boundaries. Several items cannot and must not be resolved through test-suite corrections alone because they represent **undecided specifications, unbuilt architectural pipelines, or model-bound assumptions**.

This document transparently records all remaining limitations, their physical and codal context, and the path forward for Phase 3.

---

## 2. Formal Architectural Blockers

The following three tests remain formally classified as **BLOCKED** and are excluded from the actionable sensitivity verification count:

### 2.1 DEC-013: Transverse Concrete Deck Slab Representation (`TC-REG-GEO-SLAB`)
- **Associated Defect:** DEF-14
- **Limitation:** In baseline `plategirderbridge.py`, transverse grillage members are assigned half the section properties of longitudinal steel girders (`girder/2`, $I_z \approx 0.00367\text{ m}^4$).
- **Engineering Reality:** A reinforced concrete slab has completely different material stiffness ($E_c \approx 31.6\text{ GPa}$ vs $E_s = 200\text{ GPa}$), Poisson's ratio ($\nu_c = 0.2$ vs $\nu_s = 0.3$), and cross-sectional geometry ($b_{\text{eff}} \times t_{\text{slab}}$).
- **Undecided Specifications:**
  1. *Transformed Steel vs Concrete Section:* Should transverse members be modeled as transformed steel sections ($m = E_s / E_c \approx 6.33$), or should `ospgrillage` instantiate distinct concrete materials?
  2. *Cracked vs Uncracked Modulus:* Should transverse slab stiffness account for tension cracking (e.g., $0.5 I_{\text{gross}}$) per IRC:112, or use uncracked gross inertia ($I_{\text{gross}} = b_{\text{eff}} t_{\text{slab}}^3 / 12$)?
  3. *Torsional Inertia ($J$):* Should torsional stiffness use Saint-Venant thin-plate approximation ($J = b_{\text{eff}} t_{\text{slab}}^3 / 6$) or a reduced factor to prevent fictitious torsional load paths in 2D grillage?
- **Phase 3 Path:** Formally ratify a project decision adopting transformed steel section properties before modifying `analyser.py`.

### 2.2 DEC-015: Thermal Load Modeling & Boundary Conditions (`TC-REG-D02`)
- **Associated Defect:** DEF-06
- **Limitation:** `analyser.py:add_temperature_load` looks for nonexistent key `'temperature_load_kN_m2'`. As a result, thermal effects are never modeled or combined in load combinations.
- **Undecided Specifications (IRC 6:2017 Cl. 215):**
  1. *Uniform Temperature vs Vertical Gradient:* IRC 6 Cl. 215.2 specifies overall thermal expansion/contraction ($\Delta T \approx 30^\circ\text{C}$ to $40^\circ\text{C}$), whereas Cl. 215.3 / Fig. 17 specifies non-linear vertical temperature gradients across the composite section ($\Delta T_{\text{top}} \approx 17.8^\circ\text{C}$).
  2. *Boundary Restraints:* A 2D grillage model cannot simulate axial thermal expansion unless bearing boundary conditions (fixed vs elastomeric sliding bearings) are defined at abutment nodes.
- **Phase 3 Path:** Define whether Phase 3 implements analytical secondary moments from temperature gradients or axial expansion forces based on bearing stiffness. Keep `TC-REG-D02` blocked until design ratification.

### 2.3 DEC-018: Fatigue Vehicle Moving Load Pipeline (`TC-REG-C02`)
- **Associated Defect:** DEF-17
- **Limitation:** Baseline `designer.py` doubled static moments to evaluate fatigue stress ranges. The authentic IRC 6 Cl. 204.6 fatigue vehicle moving load pipeline does not exist in `analyser.py`.
- **Undecided Specifications:**
  1. *Moving Load Generation:* Dedicated method `create_fatigue_load_case()` must instantiate the 400 kN 4-axle fatigue vehicle (axles: 60, 120, 110, 110 kN) and run influence line analyses.
  2. *Dynamic Amplification:* Span-dependent dynamic impact factor must be applied.
  3. *Resultant Envelope Mapping:* Maximum and minimum moment envelopes ($M_{\text{max,fat}}$ and $M_{\text{min,fat}}$) must be mapped to composite section modulus $Z_e$ in `designer.py`.
- **Phase 3 Path:** Architect and implement the moving load pipeline in Phase 3. Keep `TC-REG-C02` blocked until the pipeline is designed.

---

## 3. Accepted Test-Level Model Limitations

### 3.1 TC-REG-B01: Grillage Deflection Model Consistency
- **Limitation:** The target deflection ($7.218\text{ mm}$) is a calibrated grillage model consistency check tied to the current 6-girder configuration and baseline DEF-14 assumptions (`girder/2` transverse members).
- **Physical Context:**
  - Single-beam isolated upper bound: $18.164\text{ mm}$.
  - Courbon 4-girder central load lower bound: $4.541\text{ mm}$.
  - Courbon 4-girder eccentric load bound: $12.71\text{ mm}$.
  - Courbon 6-line rigid factor: $0.3977 \implies 7.22\text{ mm}$ at outer edge girder, $0.3406 \implies 6.19\text{ mm}$ under load line.
  - Transformed concrete deck slab model (DEC-013): $\approx 6.501\text{ mm}$.
- **Status:** Explicitly documented and accepted as an internal consistency check between section properties and OpenSees grillage response, not as an absolute closed-form universal constant.

### 3.2 TC-REG-A02: SIDL Factor Convention
- **Limitation:** In ULS combination `BASIC_1`, the superimposed dead load (SIDL) factor varies between IRC 6:2017 Table B.1 ($1.35$) and Table B.2 ($1.75$ for surfacing under adverse conditions).
- **Status:** The test verifies factoring and assembly using $1.35$. In Phase 3, the application schema should allow user configuration of this factor.

### 3.3 TC-REG-CAD-EXPORT-VS-SCREENSHOT: Test Scope
- **Limitation:** The test exercises the headless `pythonocc-core` offscreen rendering pipeline rather than triggering the interactive desktop GUI widget.
- **Status:** Accepted as an environment and CAD kernel verification check.

---

## 4. Historical Evidence Provenance Limitation

- In Phase 2.3, the candidate sensitivity runner inadvertently overwrote condition (b) logs with condition (c) logs for certain tests.
- **Resolution:** This historical artifact remains immutable in `testing/evidence/phase_2_3/`. Complete three-way candidate logs (`{test_id}_a_baseline.log`, `{test_id}_b_correct.log`, `{test_id}_c_naive.log`) are permanently preserved in `testing/evidence/phase_2_4/`, `testing/evidence/phase_2_5/`, and `testing/evidence/phase_2_6/`.

---

## 5. Summary Table of Boundaries

| Item | Nature of Limitation | Controlling Policy | Action Required for Resolution |
|:---|:---|:---:|:---|
| `TC-REG-D02` | Undecided specification | DEC-015 | Ratify uniform vs gradient thermal modeling in Phase 3 |
| `TC-REG-C02` | Unbuilt feature pipeline | DEC-018 | Build IRC 6 Cl. 204.6 moving load pipeline in Phase 3 |
| `TC-REG-GEO-SLAB` | Undecided specification | DEC-013 | Ratify transformed concrete slab formulation in Phase 3 |
| `TC-REG-B01` | Model-bound deflection | Accepted | Retain $7.218\text{ mm}$ for current 6-line model; update when DEF-14 is fixed |
| `TC-REG-A02` | Specification choice | Accepted | Add SIDL factor config parameter in Phase 3 |
| CAD Export | Headless verification | Accepted | GUI desktop automation deferred to Phase 3/5 |
