# Phase 2.12 Technical Report: Unresolved Issues, Architectural Gaps, and Project Boundaries

**Project:** FOSSEE Winter Internship 2026 — OsdagBridge Software Testing & Issue Reporting  
**Workspace:** `F:\FOSSEE internship`  
**Application Repository:** `source\OsdagBridge`  
**Baseline Commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`  
**Controlling Audit:** `reports/PHASE_2_11_FINAL_INDEPENDENT_GATE_AUDIT.md`  
**Date:** 2026-11-17  

---

## 1. Overview & Classification Principles

In accordance with strict QA governance principles, test suites must never invent requirements, guess unratified design parameters, or manufacture passing results for undecided engineering specifications.

This report documents the three architectural specifications that remain formally undecided, the Linux unprivileged containment boundary condition, and the Phase 3 boundary restrictions.

---

## 2. Undecided Engineering Specifications (Tri-State BLOCKED Tests)

### 2.1 TC-REG-D02-TEMPERATURE-PROPAGATION (Defect DEF-06)
- **Status:** **BLOCKED**
- **Underlying Defect:** In `bridge_types/plate_girder/analyser.py`, temperature differential load cases are stubbed or non-operational.
- **Specification Dilemma:**
  - IRC 6:2017 Clause 215 specifies non-linear vertical temperature gradient curves (positive and reverse temperature differentials) across the slab and composite steel girder.
  - The OpenSees grillage beam-element formulation natively supports uniform axial temperature change (`thermal_load`), but non-linear temperature gradient stress distribution requires fiber section integration or equivalent thermal moment computation.
- **Why Blocked:** Until the lead bridge engineer ratifies whether the analysis engine should use (a) uniform thermal expansion, (b) equivalent thermal moment approximation, or (c) layered fiber section thermal integration, no test oracle can define the exact expected stress field without guessing.
- **Safe State:** Evaluates as `BLOCKED` in baseline and sensitivity runners with zero false assertions.

### 2.2 TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS (Defect DEF-17)
- **Status:** **BLOCKED**
- **Underlying Defect:** Cyclic moving-load fatigue analysis routine is unintegrated in the baseline solver.
- **Specification Dilemma:**
  - IRC 6:2017 Annex B defines a standard 40-tonne 4-axle fatigue vehicle for cumulative damage assessment.
  - However, alternative project specifications refer to 70R bogie axle trains or simplified Class A loading with a dynamic impact factor.
  - The design life target ($100\text{ years}$ vs $120\text{ years}$) and the permissible stress range category (IRC 24:2010 Detail Category 80 vs 90 for welded flange-to-web joints) require formal client sign-off.
- **Why Blocked:** Candidate implementation and test assertion cannot be authored without ratifying the fatigue design vehicle and rainflow counting envelope.

### 2.3 TC-REG-GEO-SLAB-SECTION-PROPERTIES (Defect DEF-14 / Decision DEC-013)
- **Status:** **BLOCKED**
- **Underlying Defect:** In `designer.py`, transverse slab mesh elements are assigned sectional properties derived from half the steel girder depth (`Iz = 0.00367 m4`), which is mechanically invalid for a reinforced concrete deck slab.
- **Specification Dilemma:**
  - The concrete deck slab provides transverse stiffness to distribute wheel loads.
  - The exact numerical model requires deciding:
    1. Transformed section method ($E_s / E_c$ modular ratio).
    2. Cracked ($0.5 I_{\text{gross}}$) vs uncracked ($1.0 I_{\text{gross}}$) flexural inertia.
    3. Torsional rigidity modification factor ($J_{\text{eff}} = 0.1 J$ to $0.2 J$) to avoid over-stiff transverse torsion transfer in grillage analysis.
- **Why Blocked:** Pending Decision DEC-013 formal ratification by the Project Investigator.

---

## 3. Platform & Environmental Boundaries

### 3.1 Linux Unprivileged Process Containment (Finding F-08)
- **Status:** **DOCUMENTED BOUNDARY**
- **Analysis:**
  - On Windows, the Win32 Job Object assign-before-execute architecture (`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`) guarantees 100% escape-proof process tree termination, empirically verified across all 6 test vectors.
  - On standard Linux, unprivileged processes cannot create cgroups in `/sys/fs/cgroup` without systemd controller delegation (`Delegate=yes`), nor can they create PID namespaces without user namespace cloning permissions (`CLONE_NEWUSER`).
  - Consequently, if a malicious test process calls `setsid()` or `setpgid()`, standard POSIX session termination cannot guarantee containment without kernel privileges.
- **Harness Handling:**
  - `ProcessLifetimeJob` probes `/sys/fs/cgroup` and PID namespace capability. If unavailable, it sets `self.is_contained = False`.
  - In `test_tc_reg_fs_clean`, the runner honestly reports `BLOCKED` on Linux when containment cannot be kernel-guaranteed, preventing false claims.

---

## 4. Phase 3 Scope Restrictions

1. **Zero Edits to Application Source Code:**
   No source code inside `source/OsdagBridge` was modified during Phase 2.12. The working tree remains 100% clean on frozen baseline `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`.
2. **Zero Edits to Databases:**
   `weather.sqlite` and `Intg_osdag.sqlite` remain bit-identical to the frozen baseline.
3. **No Branch Creation or Pushing:**
   Phase 3 branch creation, code fixes, and git commits remain strictly unauthorized pending formal gate acceptance.
