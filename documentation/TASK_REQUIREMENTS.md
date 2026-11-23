# Task Requirements: FOSSEE Winter Internship 2026

## 1. Problem Statement
OsdagBridge features a specialized module dedicated to the analysis and design of short-span steel girder bridges (specifically composite plate girder bridges according to IRC standards). Ensuring the computational reliability, UI responsiveness, and data integrity of this module requires exhaustive functional testing across various design scenarios, material customizations, and consecutive design runs.

---

## 2. Mandatory Technical Requirements Breakdown

### 2.1 Rigorous Input & Customization Testing
- **Basic Geometric Parameters:**
  - Clear Span ($L$): Testing across recommended ranges ($20\text{ m} \le L \le 45\text{ m}$) as well as boundary/edge values ($<20\text{ m}$, $>45\text{ m}$).
  - Carriageway Width ($CW$): Testing single-lane, two-lane ($7.5\text{ m}$), multi-lane ($>10\text{ m}$), with and without medians/footpaths.
  - Skew Angle ($\theta$): Straight ($0^\circ$), moderate skew ($10^\circ, 15^\circ$), and severe skew ($30^\circ$).
- **Additional Design Parameters:**
  - Girder spacing, overhang width, slab thickness, wearing course thickness, crash barrier geometry.
  - Intermediate stiffener spacing, end stiffener arrangements, cross-bracing spacing and patterns.
- **Custom Material Properties:**
  - **Custom Steel:** Must explicitly enter user-defined values for Yield Strength ($f_y$), Ultimate Tensile Strength ($f_u$), Elastic Modulus ($E$), Poisson's Ratio ($\nu$), and Density ($\rho$).
  - **Custom Concrete:** User-defined Characteristic Compressive Strength ($f_{ck}$), Tensile Strength ($f_{ctm}$), Elastic Modulus ($E_{cm}$), and Density ($\rho$).
  - **State Retention Audit:** Verify whether entered custom properties survive GUI state transitions, `.osi` save/load cycles, and execution without silently reverting to defaults.

---

### 2.2 Multi-Run & State Persistence Testing
- **Consecutive Sequence:**
  - Execute a minimum of **3 consecutive design runs** within the same application session without restarting the process.
  - Sequence: Run 1 $\rightarrow$ Click Padlock (Unlock) $\rightarrow$ Modify Parameters $\rightarrow$ Run 2 $\rightarrow$ Unlock $\rightarrow$ Modify Parameters $\rightarrow$ Run 3.
- **Persistence & Teardown Verification:**
  - GUI widgets: Do input docks, display labels, and check cards update dynamically?
  - Internal dictionaries: Are `input_dict` and `output_dict` properly flushed or updated, or do they leak stale data from prior runs?
  - Graphical viewports: Does the 3D CAD viewer render the newly sized geometry or blank out (Issue #85)? Do 2D BMD/SFD plots update correctly?

---

### 2.3 Comprehensive Output Verification
- **3D CAD Model Verification:**
  - Inspect generation of all physical bridge components: Girders (top flange, web, bottom flange), Transverse Stiffeners, Bearing Stiffeners, Cross Bracing, End Diaphragms, and Concrete Deck Slab.
  - Validate interactive features: Component visibility checkboxes, zoom/pan/rotate, and navigation cube.
- **Structural Plots & Results:**
  - Bending Moment Diagram (BMD) and Shear Force Diagram (SFD) envelopes across all main girders.
  - Dynamic reaction labels and support reaction summaries.
- **Data Dictionary Integrity Audit:**
  - Extract and compare:
    1. Entered UI parameters.
    2. Internal `input_dict` captured by backend.
    3. Calculation results in internal `output_dict`.
    4. Displayed values on GUI Output Dock tabs (Girder, Deck, Stiffeners, Cross Bracing, End Diaphragm).
    5. Final values in generated LaTeX/PDF reports.
  - Flag any discrepancies, roundoff errors, unit mismatches, or missing keys.

---

### 2.4 Test-Case Documentation & Logging
- Standardized documentation for every executed test case:
  - Unique Test ID (e.g., `TC_PG_01`, `TC_CUSTOM_MAT_02`, `TC_MULTIRUN_03`).
  - Objective and input parameter set (tabular format).
  - Expected behavior vs. Actual observed behavior.
  - Execution Status: PASS / FAIL.
  - Attached evidence: Saved `.osi` project file, raw dictionary JSON dumps, error tracebacks, and screenshots.

---

### 2.5 GitHub Issue Creation & Code-Level Bug Reporting
For every anomaly, crash, or calculation error:
- **Exhaustive De-duplication:** Verify against existing GitHub issues (see `documentation/EXISTING_ISSUES_REGISTER.md`) before filing. If an existing issue covers the bug, contribute commentary rather than duplicating.
- **Issue Structure Requirements:**
  - **Detailed Description:** Clear reproduction steps, trigger conditions, working vs. failing boundaries.
  - **Logs & Proof:** Console traceback, screenshots, and attached input/output dictionaries.
  - **Code-Level Root Cause:** Identify exact source files, classes, methods, and line numbers in `src/osdagbridge/`.
  - **Suggested Fix:** Concrete code patch / unified diff proposal resolving the issue without regressions.

---

### 2.6 Final Deliverables Checklist
1. **GitHub Repository:** Private repository with documentation, test scripts, logs, and evidence. Maintainer `Nidhikhare12` added as collaborator.
2. **Comprehensive PDF Testing Report:** Professional document compiling methodology, test matrix, side-by-side dictionary comparisons, CAD evaluations, bug registers, and conclusions.
3. **Submission ZIP Archive:** Self-contained bundle with all test `.osi` files, raw dictionary dumps, tracebacks, and scripts.
4. **Candidate Resume:** `Subodh_Resume.pdf`.
5. **Video Screencast:** High-definition video showing custom material entry, consecutive multi-run sequence, and 3D CAD rendering. Hosted on accessible cloud drive or unlisted YouTube link.
