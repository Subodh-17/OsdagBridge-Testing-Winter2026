"""
Phase 2.11 Test Sensitivity Matrix Verification Harness
Workspace: F:\\FOSSEE internship
Frozen baseline commit: d74f56dd7f22925fb8148cabf5740ed8d1e39ff3
Controlling Audit: reports/PHASE_2_10_FINAL_INDEPENDENT_GATE_AUDIT.md

Strict Candidate-Validation Protocol:
  (a) Baseline behavior -> BASELINE_FAIL / BLOCKED
  (b) Minimal correct candidate implementation -> PASS
  (c) Plausible incorrect / naive candidate implementation -> BASELINE_FAIL / FAIL

Key Rules & Guardrails:
  - No output spoofing or constant return overrides.
  - No mock objects without solver participation.
  - Candidates must alter production execution or solver state.
  - Blocked tests (D02 under DEC-015, GEO-SLAB under DEC-013, C02 under DEC-018)
    are marked 'BLOCKED / NOT DEMONSTRATED'.
  - Output directory: testing/evidence/phase_2_11/sensitivity/ (strictly isolated from baseline evidence).
  - Candidate logs: testing/evidence/phase_2_11/candidates/ (distinct per-condition logs: _a_baseline, _b_correct, _c_naive).
  - All writes routed through centralized safe_open_evidence and safe_copy_evidence write gateway.
  - Cryptographic run seal externally registered in reports/PHASE_2_11_RUN_SEALS.json.
  - Candidate function source code SHA-256 hashes recorded in summary.
"""

import sys
import os
import json
import math
import time
import copy
import re
import shutil
import hashlib
import inspect
import datetime
import tempfile
import traceback
import uuid
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
REPO_SRC = os.path.join(WORKSPACE_ROOT, "source", "OsdagBridge", "src")
SENSITIVITY_DIR = os.path.join(WORKSPACE_ROOT, "testing", "evidence", "phase_2_13", "sensitivity")
CANDIDATES_DIR = os.path.join(WORKSPACE_ROOT, "testing", "evidence", "phase_2_13", "candidates")

if REPO_SRC not in sys.path:
    sys.path.insert(0, REPO_SRC)
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from testing.test_cases.baseline_regression.evidence_guard import (
    validate_evidence_directory,
    safe_open_evidence,
    safe_write_evidence,
    safe_copy_evidence,
    generate_and_seal_manifest,
    verify_manifest_integrity,
    sha256_file
)

# Import test functions from baseline regression runner
from testing.test_cases.baseline_regression.run_all_baseline_tests import (
    test_tc_reg_a01,
    test_tc_reg_b01,
    test_tc_reg_c01,
    test_tc_reg_a02,
    test_tc_reg_eq_load_conservation,
    test_tc_reg_d01,
    test_tc_reg_d02,
    test_tc_reg_c02,
    test_tc_reg_rpt_status,
    test_tc_reg_geo_count,
    test_tc_reg_geo_slab,
    test_tc_reg_cap_stiffener,
    test_tc_reg_mat_density,
    test_tc_reg_fs_clean,
    test_tc_reg_cad_export,
    BASE_CFG,
    BASELINE_COMMIT
)


def _fn_sha256(fn):
    """Compute SHA-256 hash of a candidate function source code."""
    if fn is None:
        return None
    try:
        src = inspect.getsource(fn)
        return hashlib.sha256(src.encode("utf-8")).hexdigest()
    except Exception:
        return None


def _preserve_candidate_log(test_id, condition_suffix):
    """Preserve candidate condition logs with distinct file suffixes via safe_copy_evidence."""
    base_log_name = f"{test_id.lower().replace('-', '_')}.log"
    src_path = os.path.join(CANDIDATES_DIR, base_log_name)
    dst_path = os.path.join(CANDIDATES_DIR, f"{test_id.lower().replace('-', '_')}_{condition_suffix}.log")
    if os.path.exists(src_path):
        safe_copy_evidence(src_path, dst_path)


def run_sensitivity_test(test_id, defect_id, test_fn, mut_b_fn, mut_c_fn, is_blocked=False, block_reason=""):
    """
    Run condition (a), (b), and (c) for a given test.
    For blocked tests, conditions (b) and (c) are not manufactured.
    Distinct log files are preserved for each condition:
      - {test_id}_a_baseline.log
      - {test_id}_b_correct.log
      - {test_id}_c_naive.log
    """
    matrix_entry = {
        "test_id": test_id,
        "defect_id": defect_id,
        "is_blocked": is_blocked,
        "conditions": {}
    }

    # (a) Baseline run - logged to candidates dir to NEVER overwrite baseline evidence
    t0 = time.time()
    res_a = test_fn(evidence_dir=CANDIDATES_DIR)
    dur_a = time.time() - t0
    _preserve_candidate_log(test_id, "a_baseline")

    matrix_entry["conditions"]["a_baseline"] = {
        "description": "Frozen baseline behavior",
        "observed_status": res_a["status"],
        "expected_status": res_a["expected_baseline"],
        "duration_sec": round(dur_a, 3),
        "reason": res_a["reason"]
    }

    if is_blocked:
        matrix_entry["conditions"]["b_minimal_correct"] = {
            "description": "Minimal correct candidate implementation",
            "candidate_sha256": None,
            "observed_status": "BLOCKED",
            "expected_status": "BLOCKED",
            "duration_sec": 0.0,
            "reason": block_reason
        }
        matrix_entry["conditions"]["c_plausible_wrong"] = {
            "description": "Plausible incorrect / naive candidate implementation",
            "candidate_sha256": None,
            "observed_status": "BLOCKED",
            "expected_status": "BLOCKED",
            "duration_sec": 0.0,
            "reason": block_reason
        }
        matrix_entry["sensitivity_verified"] = False
        matrix_entry["sensitivity_status"] = "BLOCKED / NOT DEMONSTRATED"
    else:
        # (b) Minimal correct candidate
        t0 = time.time()
        res_b = mut_b_fn()
        dur_b = time.time() - t0
        _preserve_candidate_log(test_id, "b_correct")

        matrix_entry["conditions"]["b_minimal_correct"] = {
            "description": "Minimal correct candidate implementation",
            "candidate_sha256": _fn_sha256(mut_b_fn),
            "observed_status": res_b["status"],
            "expected_status": "PASS",
            "duration_sec": round(dur_b, 3),
            "reason": res_b["reason"]
        }

        # (c) Plausible incorrect / naive candidate
        t0 = time.time()
        res_c = mut_c_fn()
        dur_c = time.time() - t0
        _preserve_candidate_log(test_id, "c_naive")

        matrix_entry["conditions"]["c_plausible_wrong"] = {
            "description": "Plausible incorrect / naive candidate implementation",
            "candidate_sha256": _fn_sha256(mut_c_fn),
            "observed_status": res_c["status"],
            "expected_status": "BASELINE_FAIL",
            "duration_sec": round(dur_c, 3),
            "reason": res_c["reason"]
        }

        # Overall sensitivity verification verdict:
        # (a) matches expected baseline outcome (BASELINE_FAIL or PASS for CAD),
        # (b) PASS, (c) BASELINE_FAIL / FAIL
        verified = (
            res_a["status"] == res_a["expected_baseline"] and
            res_b["status"] == "PASS" and
            res_c["status"] in ("BASELINE_FAIL", "FAIL")
        )
        matrix_entry["sensitivity_verified"] = verified
        matrix_entry["sensitivity_status"] = "VERIFIED" if verified else "UNVERIFIED"

    # Save individual log
    log_file = os.path.join(SENSITIVITY_DIR, f"{test_id.lower().replace('-', '_')}_sensitivity.json")
    with safe_open_evidence(log_file, "w", encoding="utf-8") as f:
        json.dump(matrix_entry, f, indent=2)

    return matrix_entry


# =============================================================================
# Mutation Definitions for Each Test
# =============================================================================

# 1. TC-REG-A01-FACTOR-SCALING
def mut_b_a01():
    """Candidate (b): deepcopy and scale load magnitudes by load_factor in LoadCase.add_load."""
    import ospgrillage as og
    orig_add_load = og.load.LoadCase.add_load
    orig_line_apply = og.load.LineLoading.apply_load_factor
    orig_patch_apply = og.load.PatchLoading.apply_load_factor

    def patched_line_apply(self, factor=1):
        orig_line_apply(self, factor)
        if hasattr(self, "line_end_point") and self.line_end_point is not None:
            self.line_end_point = self.line_end_point._replace(p=factor * self.line_end_point.p)

    def patched_patch_apply(self, factor=1):
        orig_patch_apply(self, factor)
        self._define_patch_edge_lines()

    def patched_add_load(self, load, load_factor=1.0):
        scaled_load = copy.deepcopy(load)
        if hasattr(scaled_load, "apply_load_factor"):
            scaled_load.apply_load_factor(load_factor)
        orig_add_load(self, scaled_load, load_factor=1.0)

    og.load.LineLoading.apply_load_factor = patched_line_apply
    og.load.PatchLoading.apply_load_factor = patched_patch_apply
    og.load.LoadCase.add_load = patched_add_load
    try:
        return test_tc_reg_a01(evidence_dir=CANDIDATES_DIR)
    finally:
        og.load.LoadCase.add_load = orig_add_load
        og.load.LineLoading.apply_load_factor = orig_line_apply
        og.load.PatchLoading.apply_load_factor = orig_patch_apply


def mut_c_a01():
    """Candidate (c): naive partial scaling of 1.15x regardless of load_factor."""
    import ospgrillage as og
    orig_add_load = og.load.LoadCase.add_load
    def wrong_add_load(self, load, load_factor=1.0):
        scaled_load = copy.deepcopy(load)
        if hasattr(scaled_load, "apply_load_factor"):
            scaled_load.apply_load_factor(1.15 if load_factor > 1.0 else 1.0)
        orig_add_load(self, scaled_load, load_factor=1.0)
    og.load.LoadCase.add_load = wrong_add_load
    try:
        return test_tc_reg_a01(evidence_dir=CANDIDATES_DIR)
    finally:
        og.load.LoadCase.add_load = orig_add_load


# 2. TC-REG-B01-SECTION-PROPERTY-SYNC
def mut_b_b01():
    """
    Candidate (b): Genuine solver synchronization:
    Overrides _girder_section so setup_grillage() builds solver elements with
    dynamically derived snapped properties (Iz, A, Iy, J) reading both top and bottom flange dimensions,
    and aligns dw in input_dict.
    Then 100 kN midspan deflection drops to 7.218 mm (matching snapped grillage oracle within 1%).
    """
    from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge, SectionProperties
    from osdagbridge.core.utils.common import (
        KEY_MP_GIRDER_DEPTH, KEY_MP_GIRDER_TOP_FLANGE_THICKNESS,
        KEY_MP_GIRDER_BOTTOM_FLANGE_THICKNESS, KEY_MP_GIRDER_TOP_FLANGE_WIDTH,
        KEY_MP_GIRDER_BOTTOM_FLANGE_WIDTH, KEY_MP_GIRDER_WEB_THICKNESS
    )
    orig_girder_section = PlateGirderBridge._girder_section
    orig_validate = PlateGirderBridge._validate_inputs

    def patched_girder_section(self, i=0):
        # Section properties dynamically derived from snapped plate dimensions (general asymmetric formulation):
        D = self._girder_value(KEY_MP_GIRDER_DEPTH)
        tf_top = self._girder_value(KEY_MP_GIRDER_TOP_FLANGE_THICKNESS)
        tf_bot = self._girder_value(KEY_MP_GIRDER_BOTTOM_FLANGE_THICKNESS)
        bf_top = self._girder_value(KEY_MP_GIRDER_TOP_FLANGE_WIDTH)
        bf_bot = self._girder_value(KEY_MP_GIRDER_BOTTOM_FLANGE_WIDTH) if hasattr(self, "_girder_value") else bf_top
        tw = self._girder_value(KEY_MP_GIRDER_WEB_THICKNESS)
        dw = D - tf_top - tf_bot
        a_ft = bf_top * tf_top
        a_fb = bf_bot * tf_bot
        a_w = dw * tw
        a_tot = a_ft + a_fb + a_w
        y_fb = tf_bot / 2.0
        y_w = tf_bot + dw / 2.0
        y_ft = tf_bot + dw + tf_top / 2.0
        y_bar = (a_fb * y_fb + a_w * y_w + a_ft * y_ft) / a_tot
        Iz = (bf_bot * (tf_bot**3)) / 12.0 + a_fb * ((y_fb - y_bar)**2) + (tw * (dw**3)) / 12.0 + a_w * ((y_w - y_bar)**2) + (bf_top * (tf_top**3)) / 12.0 + a_ft * ((y_ft - y_bar)**2)
        Iy = (tf_bot * (bf_bot**3)) / 12.0 + (dw * (tw**3)) / 12.0 + (tf_top * (bf_top**3)) / 12.0
        J = (bf_bot * (tf_bot**3) + dw * (tw**3) + bf_top * (tf_top**3)) / 3.0
        return SectionProperties(
            A=a_tot,
            J=J,
            Iz=Iz,
            Iy=Iy,
            Az=dw * tw,
            Ay=a_ft + a_fb
        )

    def patched_validate(self):
        orig_validate(self)
        D = self._girder_value(KEY_MP_GIRDER_DEPTH)
        tf_top = self._girder_value(KEY_MP_GIRDER_TOP_FLANGE_THICKNESS)
        tf_bot = self._girder_value(KEY_MP_GIRDER_BOTTOM_FLANGE_THICKNESS)
        dw = D - tf_top - tf_bot
        for k in list(self.input_dict.keys()):
            if "web_depth" in k:
                self.input_dict[k] = dw

    PlateGirderBridge._girder_section = patched_girder_section
    PlateGirderBridge._validate_inputs = patched_validate
    try:
        return test_tc_reg_b01(evidence_dir=CANDIDATES_DIR)
    finally:
        PlateGirderBridge._girder_section = orig_girder_section
        PlateGirderBridge._validate_inputs = orig_validate


def mut_c_b01():
    """
    Candidate (c): Probe flaw candidate:
    Swaps bgm.girder_props metadata post-setup only, leaving solver elements
    and OpenSees stiffness preliminary (Iz=0.00734 m4, deflection=7.816 mm).
    """
    from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge, SectionProperties
    orig_stage = PlateGirderBridge._stage_grillage_setup
    def wrong_stage(self):
        orig_stage(self)
        self.grillage_model.girder_props = [
            SectionProperties(A=0.025192, J=1.45e-6, Iz=0.00792758, Iy=0.0002734, Az=0.0104, Ay=0.0162)
            for _ in range(4)
        ]
    PlateGirderBridge._stage_grillage_setup = wrong_stage
    try:
        return test_tc_reg_b01(evidence_dir=CANDIDATES_DIR)
    finally:
        PlateGirderBridge._stage_grillage_setup = orig_stage


# 3. TC-REG-C01-SECTIONAL-STRESS-RANGE
def mut_b_c01():
    """
    Candidate (b): Genuine cyclic range calculation (sign-consistent element end evaluation):
    Evaluates section bending moments with consistent sign (M = -Mz_i or +Mz_j).
    Evaluates delta_sigma = (max(M) - min(M)) / Ze across all frequent load cases.
    For static load case (1 LC): max(M) - min(M) = 0.0 MPa on both envelope and per-LC paths.
    For 4-state cyclic history (+200, +500, -1500, +1200 kNm): true range = 2700 kNm -> delta_sigma = 169.358 MPa.
    For sign reversal (-500 to +1500 kNm): true range = 2000 kNm -> delta_sigma = 125.450 MPa.
    """
    import osdagbridge.core.bridge_types.plate_girder.designer as des
    from osdagbridge.core.bridge_types.plate_girder.designer import (
        IRC22_2014, composite_section_properties, KEY_COMP_S_BOT
    )
    orig_extract = des._extract_demands_from_analysis_results

    def patched_extract(analysis_results, bcfg):
        demands, per_lc = orig_extract(analysis_results, bcfg)
        sec, mat, slab, geo = bcfg.section, bcfg.material, bcfg.slab, bcfg.geometry
        beff_mm = min(geo.span * 1000.0 / 4.0, geo.beam_spacing * 1000.0)
        mod = IRC22_2014.cl_604_3_modular_ratio(Ecm=mat.Ecm, Kc=0.5)
        props = composite_section_properties(
            beff_mm=beff_mm, ds_mm=slab.thickness, h_haunch_mm=slab.haunch_depth,
            A_steel_mm2=sec.A_steel, Iz_steel_mm4=sec.Iz_steel,
            y_cg_from_bot_mm=sec.y_cg_from_bot, D_steel_mm=sec.D, n=mod['m_short_term'],
        )
        Ze = float(props.get(KEY_COMP_S_BOT) or 0.0) or float(bcfg.section.Ze_steel)
        lc_groups = analysis_results.classify_loadcases() if hasattr(analysis_results, 'classify_loadcases') else {}
        sls_freq_lcs = lc_groups.get('sls_frequent', [])
        girders, _ = analysis_results.build_girders()

        for g_name, g_info in girders.items():
            if g_name in demands and sls_freq_lcs:
                elements = g_info.get('elements', [])
                max_range_MPa = 0.0
                ds = analysis_results.ds
                for e in elements:
                    m_i = [-float(ds.forces.sel(Loadcase=lc, Element=e, Component='Mz_i').values) for lc in sls_freq_lcs]
                    m_j = [+float(ds.forces.sel(Loadcase=lc, Element=e, Component='Mz_j').values) for lc in sls_freq_lcs]
                    r_i = max(m_i) - min(m_i) if len(m_i) > 1 else 0.0
                    r_j = max(m_j) - min(m_j) if len(m_j) > 1 else 0.0
                    s_i = (r_i / Ze) * 1e3
                    s_j = (r_j / Ze) * 1e3
                    max_range_MPa = max(max_range_MPa, s_i, s_j)
                demands[g_name].stress_range_MPa = max_range_MPa
                if g_name in per_lc:
                    for lc in per_lc[g_name]:
                        per_lc[g_name][lc].stress_range_MPa = max_range_MPa
        return demands, per_lc

    des._extract_demands_from_analysis_results = patched_extract
    try:
        return test_tc_reg_c01(evidence_dir=CANDIDATES_DIR)
    finally:
        des._extract_demands_from_analysis_results = orig_extract


def mut_c_c01():
    """
    Candidate (c): Naive candidate evaluating range only from the first two load cases:
    Evaluates sls_freq_lcs[:2] only. For the 4-state cyclic history (+200, +500, -1500, +1200 kNm),
    it obtains (500 - 200) = 300 kNm -> 18.818 MPa instead of the true 169.358 MPa, failing the cyclic check.
    """
    import osdagbridge.core.bridge_types.plate_girder.designer as des
    from osdagbridge.core.bridge_types.plate_girder.designer import (
        IRC22_2014, composite_section_properties, KEY_COMP_S_BOT
    )
    orig_extract = des._extract_demands_from_analysis_results

    def naive_first_two_extract(analysis_results, bcfg):
        demands, per_lc = orig_extract(analysis_results, bcfg)
        sec, mat, slab, geo = bcfg.section, bcfg.material, bcfg.slab, bcfg.geometry
        beff_mm = min(geo.span * 1000.0 / 4.0, geo.beam_spacing * 1000.0)
        mod = IRC22_2014.cl_604_3_modular_ratio(Ecm=mat.Ecm, Kc=0.5)
        props = composite_section_properties(
            beff_mm=beff_mm, ds_mm=slab.thickness, h_haunch_mm=slab.haunch_depth,
            A_steel_mm2=sec.A_steel, Iz_steel_mm4=sec.Iz_steel,
            y_cg_from_bot_mm=sec.y_cg_from_bot, D_steel_mm=sec.D, n=mod['m_short_term'],
        )
        Ze = float(props.get(KEY_COMP_S_BOT) or 0.0) or float(bcfg.section.Ze_steel)
        lc_groups = analysis_results.classify_loadcases() if hasattr(analysis_results, 'classify_loadcases') else {}
        sls_freq_lcs = lc_groups.get('sls_frequent', [])
        girders, _ = analysis_results.build_girders()

        # Naive flaw: only inspects first 2 load cases instead of all load cases
        eval_lcs = sls_freq_lcs[:2]

        for g_name, g_info in girders.items():
            if g_name in demands and eval_lcs:
                elements = g_info.get('elements', [])
                max_range_MPa = 0.0
                ds = analysis_results.ds
                for e in elements:
                    m_i = [-float(ds.forces.sel(Loadcase=lc, Element=e, Component='Mz_i').values) for lc in eval_lcs]
                    m_j = [+float(ds.forces.sel(Loadcase=lc, Element=e, Component='Mz_j').values) for lc in eval_lcs]
                    r_i = max(m_i) - min(m_i) if len(m_i) > 1 else 0.0
                    r_j = max(m_j) - min(m_j) if len(m_j) > 1 else 0.0
                    s_i = (r_i / Ze) * 1e3
                    s_j = (r_j / Ze) * 1e3
                    max_range_MPa = max(max_range_MPa, s_i, s_j)
                demands[g_name].stress_range_MPa = max_range_MPa
                if g_name in per_lc:
                    for lc in per_lc[g_name]:
                        per_lc[g_name][lc].stress_range_MPa = max_range_MPa
        return demands, per_lc

    des._extract_demands_from_analysis_results = naive_first_two_extract
    try:
        return test_tc_reg_c01(evidence_dir=CANDIDATES_DIR)
    finally:
        des._extract_demands_from_analysis_results = orig_extract


# 4. TC-REG-A02-ULS-COMBINATION-SUM
def mut_b_a02():
    """
    Candidate (b): Genuine ULS combination creation (Phase 2.10):
    1. Fixes upstream ospgrillage apply_load_factor for LineLoading and PatchLoading.
    2. Deepcopies and scales load magnitudes in LoadCase.add_load.
    3. Invokes create_sidl_combination before create_dead_load_combination in add_dead_loads.
    4. Propagates user steel and deck density, and carriageway edge clearance for overlay.
    5. Implements FEM bilinear patch and non-collinear line load distribution.
    6. Vertical reaction matches factored target 2711.74 kN within 0.001%, all component reactions pass independent oracles.
    """
    from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import (
        PlateGirderBridge, deck_thickness_from_inputs, _DEFAULT_DECK_THICKNESS_MM,
        crash_barrier_load_from_inputs, railing_load_from_inputs
    )
    from osdagbridge.core.utils.common import KEY_WC_THICKNESS, KEY_WC_DENSITY
    import osdagbridge.core.bridge_types.plate_girder.analyser as analyser_mod
    import ospgrillage as og
    from ospgrillage.load import PatchLoading, LineLoading

    orig_add_dead = PlateGirderBridge.add_dead_loads
    orig_add_load = og.load.LoadCase.add_load
    orig_line_apply = og.load.LineLoading.apply_load_factor
    orig_patch_apply = og.load.PatchLoading.apply_load_factor
    orig_dist = og.osp_grillage.OspGrillage._distribute_load_types_to_model

    def patched_line_apply(self, factor=1):
        orig_line_apply(self, factor)
        if hasattr(self, "line_end_point") and self.line_end_point is not None:
            self.line_end_point = self.line_end_point._replace(p=factor * self.line_end_point.p)

    def patched_patch_apply(self, factor=1):
        orig_patch_apply(self, factor)
        self._define_patch_edge_lines()

    def patched_add_load(self, load, **kwargs):
        load_factor = kwargs.get("load_factor", 1.0)
        cld = copy.deepcopy(load)
        if load_factor != 1.0 and hasattr(cld, "apply_load_factor"):
            cld.apply_load_factor(load_factor)
        orig_add_load(self, cld, **kwargs)

    def patched_dist(self, load_case_obj):
        load_groups = getattr(load_case_obj, "load_groups", [])
        has_patch = any(isinstance(lg.get("load"), PatchLoading) for lg in load_groups)
        has_line_non_collinear = any(
            isinstance(lg.get("load"), LineLoading)
            and not any([lg["load"].long_beam_ele_load_flag, lg["load"].trans_beam_ele_load_flag])
            for lg in load_groups
        )
        if has_patch or has_line_non_collinear:
            cmds = []
            for lg in load_groups:
                ld = lg["load"]
                if isinstance(ld, PatchLoading):
                    cmds.extend(_distribute_patch_load_fem(self, ld))
                elif isinstance(ld, LineLoading):
                    if any([ld.long_beam_ele_load_flag, ld.trans_beam_ele_load_flag]):
                        cmds.extend(self._assign_beam_ele_line_load(ld))
                    else:
                        cmds.extend(_distribute_line_load_fem(self, ld))
                else:
                    cmds.extend(orig_dist(self, load_case_obj))
            return cmds
        return orig_dist(self, load_case_obj)

    def patched_add_dead(self):
        deck_t_m = deck_thickness_from_inputs(self.input_dict, _DEFAULT_DECK_THICKNESS_MM)
        wc_t_m = float(self.input_dict[KEY_WC_THICKNESS]) / 1000.0
        wc_rho = float(self.input_dict[KEY_WC_DENSITY])
        barrier_load_kN_m = crash_barrier_load_from_inputs(self.input_dict)
        railing_load_kN_m = railing_load_from_inputs(self.input_dict)

        user_density = float(self.input_dict.get("material.girder.density", 78.5))
        orig_density = analyser_mod.STEEL_UNIT_WEIGHT_kN_m3
        analyser_mod.STEEL_UNIT_WEIGHT_kN_m3 = user_density
        try:
            model = self.grillage_model
            model.create_self_weight_load()
            rho_c = float(self.input_dict.get("material.deck.density", 25.0))
            model.create_deck_load(slab_thickness_m=deck_t_m, concrete_density_kN_m3=rho_c)
            cw = float(self.input_dict.get("geometry.carriageway_width", 7.5))
            bw = float(getattr(model, "w", 8.5))
            edge_clr = max(0.0, (bw - cw) / 2.0)
            model.create_wearing_course_load(thickness_m=wc_t_m, density_kN_m3=wc_rho, edge_clearance=edge_clr, partial_safety_factor=1.0)
            model.create_footpath_load()
            model.create_crash_barrier_load(barrier_load_kN_per_m=barrier_load_kN_m)
            model.create_railing_load(railing_load_kN_per_m=railing_load_kN_m)
            model.create_median_load()
            model.create_sidl_combination()
            model.create_dead_load_combination(partial_safety_factor=1.0)
        finally:
            analyser_mod.STEEL_UNIT_WEIGHT_kN_m3 = orig_density

    og.load.LineLoading.apply_load_factor = patched_line_apply
    og.load.PatchLoading.apply_load_factor = patched_patch_apply
    og.load.LoadCase.add_load = patched_add_load
    og.osp_grillage.OspGrillage._distribute_load_types_to_model = patched_dist
    PlateGirderBridge.add_dead_loads = patched_add_dead

    try:
        return test_tc_reg_a02(evidence_dir=CANDIDATES_DIR)
    finally:
        og.load.LoadCase.add_load = orig_add_load
        og.load.LineLoading.apply_load_factor = orig_line_apply
        og.load.PatchLoading.apply_load_factor = orig_patch_apply
        og.osp_grillage.OspGrillage._distribute_load_types_to_model = orig_dist
        PlateGirderBridge.add_dead_loads = orig_add_dead


def mut_c_a02():
    """
    Candidate (c): Partial / incorrect candidate:
    Factors SW and DW, but omits crash barrier from BASIC_1.
    Reaction falls short of 2710.17 kN and barrier check fails.
    """
    from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
    import ospgrillage as og
    orig_add_dead = PlateGirderBridge.add_dead_loads

    def wrong_add_dead(self):
        orig_add_dead(self)
        bgm = self.grillage_model
        # BASIC_1 without crash barrier
        b1_lc = og.create_load_case(name="BASIC_1: 1.35DL + 1.75DW")
        sw_lc = getattr(bgm, "self_weight_load_case", None)
        dw_lc = getattr(bgm, "wearing_course_load", None)
        if sw_lc:
            for e in sw_lc.load_groups:
                b1_lc.add_load(e["load"], load_factor=1.35)
        if dw_lc:
            for e in dw_lc.load_groups:
                b1_lc.add_load(e["load"], load_factor=1.75)
        bgm.model.add_load_case(b1_lc)

    PlateGirderBridge.add_dead_loads = wrong_add_dead
    try:
        return test_tc_reg_a02(evidence_dir=CANDIDATES_DIR)
    finally:
        PlateGirderBridge.add_dead_loads = orig_add_dead


def _distribute_patch_load_fem(grillage, patch_load_obj):
    pts = [patch_load_obj.load_point_1, patch_load_obj.load_point_2, patch_load_obj.load_point_3, patch_load_obj.load_point_4]
    xs = [p.x for p in pts]
    zs = [p.z for p in pts]
    x_min, x_max = min(xs), max(xs)
    z_min, z_max = min(zs), max(zs)
    pressure = pts[0].p
    nox = sorted(grillage.Mesh_obj.nox)
    noz = sorted(grillage.Mesh_obj.noz)
    coord_to_tag = {
        (round(spec['coordinate'][0], 4), round(spec['coordinate'][2], 4)): tag
        for tag, spec in grillage.Mesh_obj.node_spec.items()
    }
    load_commands = []
    for i in range(len(nox) - 1):
        x1, x2 = nox[i], nox[i+1]
        cx1 = max(x_min, x1)
        cx2 = min(x_max, x2)
        if cx2 <= cx1:
            continue
        for j in range(len(noz) - 1):
            z1, z2 = noz[j], noz[j+1]
            cz1 = max(z_min, z1)
            cz2 = min(z_max, z2)
            if cz2 <= cz1:
                continue
            area = (cx2 - cx1) * (cz2 - cz1)
            F = pressure * area
            xc = (cx1 + cx2) / 2.0
            zc = (cz1 + cz2) / 2.0
            n1 = coord_to_tag[(round(x1, 4), round(z1, 4))]
            n2 = coord_to_tag[(round(x2, 4), round(z1, 4))]
            n3 = coord_to_tag[(round(x2, 4), round(z2, 4))]
            n4 = coord_to_tag[(round(x1, 4), round(z2, 4))]
            xi = 2.0 * (xc - x1) / (x2 - x1) - 1.0
            eta = 2.0 * (zc - z1) / (z2 - z1) - 1.0
            N1 = 0.25 * (1.0 - xi) * (1.0 - eta)
            N2 = 0.25 * (1.0 + xi) * (1.0 - eta)
            N3 = 0.25 * (1.0 + xi) * (1.0 + eta)
            N4 = 0.25 * (1.0 - xi) * (1.0 + eta)
            for tag, N in [(n1, N1), (n2, N2), (n3, N3), (n4, N4)]:
                load_commands.append(('load', (tag, 0, float(N * F), 0, 0, 0, 0), {}))
    return load_commands


def _distribute_line_load_fem(grillage, line_load_obj):
    p1 = line_load_obj.load_point_1
    p2 = line_load_obj.load_point_2
    x_start, x_end = min(p1.x, p2.x), max(p1.x, p2.x)
    z_val = p1.z
    w = p1.p
    nox = sorted(grillage.Mesh_obj.nox)
    noz = sorted(grillage.Mesh_obj.noz)
    coord_to_tag = {
        (round(spec['coordinate'][0], 4), round(spec['coordinate'][2], 4)): tag
        for tag, spec in grillage.Mesh_obj.node_spec.items()
    }
    for j in range(len(noz) - 1):
        if noz[j] <= z_val <= noz[j+1] + 1e-9:
            z1, z2 = noz[j], noz[j+1]
            break
    else:
        return []
    load_commands = []
    for i in range(len(nox) - 1):
        x1, x2 = nox[i], nox[i+1]
        cx1 = max(x_start, x1)
        cx2 = min(x_end, x2)
        if cx2 <= cx1:
            continue
        seg_len = cx2 - cx1
        F = w * seg_len
        xc = (cx1 + cx2) / 2.0
        n1 = coord_to_tag[(round(x1, 4), round(z1, 4))]
        n2 = coord_to_tag[(round(x2, 4), round(z1, 4))]
        n3 = coord_to_tag[(round(x2, 4), round(z2, 4))]
        n4 = coord_to_tag[(round(x1, 4), round(z2, 4))]
        xi = 2.0 * (xc - x1) / (x2 - x1) - 1.0
        eta = 2.0 * (z_val - z1) / (z2 - z1) - 1.0 if z2 != z1 else 0.0
        N1 = 0.25 * (1.0 - xi) * (1.0 - eta)
        N2 = 0.25 * (1.0 + xi) * (1.0 - eta)
        N3 = 0.25 * (1.0 + xi) * (1.0 + eta)
        N4 = 0.25 * (1.0 - xi) * (1.0 + eta)
        for tag, N in [(n1, N1), (n2, N2), (n3, N3), (n4, N4)]:
            load_commands.append(('load', (tag, 0, float(N * F), 0, 0, 0, 0), {}))
    return load_commands


# 4B. TC-REG-EQ-LOAD-CONSERVATION (DEF-18)
def mut_b_eq_load_conservation():
    """
    Candidate (b): Genuine FEM cell-intersection load distribution:
    - Patches are integrated over grid cells and assigned to 4 corner nodes via bilinear shape functions.
    - Non-collinear line loads (Crash barrier) are integrated over mesh segments and distributed to surrounding nodes.
    - Collinear line loads (SW) continue using beam element loads.
    - Dead load creation uses user steel and concrete densities, and carriageway width for overlay.
    Conserves both vertical force resultant and resultant centroid (x=12.0m, z=4.25m) exactly.
    """
    from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import (
        PlateGirderBridge, deck_thickness_from_inputs, _DEFAULT_DECK_THICKNESS_MM,
        crash_barrier_load_from_inputs, railing_load_from_inputs
    )
    from osdagbridge.core.utils.common import KEY_WC_THICKNESS, KEY_WC_DENSITY
    import osdagbridge.core.bridge_types.plate_girder.analyser as analyser_mod
    import ospgrillage as og
    from ospgrillage.load import PatchLoading, LineLoading

    orig_add_dead = PlateGirderBridge.add_dead_loads
    orig_dist = og.osp_grillage.OspGrillage._distribute_load_types_to_model

    def patched_dist(self, load_case_obj):
        load_groups = getattr(load_case_obj, "load_groups", [])
        has_patch = any(isinstance(lg.get("load"), PatchLoading) for lg in load_groups)
        has_line_non_collinear = any(
            isinstance(lg.get("load"), LineLoading)
            and not any([lg["load"].long_beam_ele_load_flag, lg["load"].trans_beam_ele_load_flag])
            for lg in load_groups
        )
        if has_patch or has_line_non_collinear:
            cmds = []
            for lg in load_groups:
                ld = lg["load"]
                if isinstance(ld, PatchLoading):
                    cmds.extend(_distribute_patch_load_fem(self, ld))
                elif isinstance(ld, LineLoading):
                    if any([ld.long_beam_ele_load_flag, ld.trans_beam_ele_load_flag]):
                        cmds.extend(self._assign_beam_ele_line_load(ld))
                    else:
                        cmds.extend(_distribute_line_load_fem(self, ld))
                else:
                    cmds.extend(orig_dist(self, load_case_obj))
            return cmds
        return orig_dist(self, load_case_obj)

    def patched_add_dead(self):
        deck_t_m = deck_thickness_from_inputs(self.input_dict, _DEFAULT_DECK_THICKNESS_MM)
        wc_t_m = float(self.input_dict[KEY_WC_THICKNESS]) / 1000.0
        wc_rho = float(self.input_dict[KEY_WC_DENSITY])
        barrier_load_kN_m = crash_barrier_load_from_inputs(self.input_dict)
        railing_load_kN_m = railing_load_from_inputs(self.input_dict)

        user_density = float(self.input_dict.get("material.girder.density", 78.5))
        orig_density = analyser_mod.STEEL_UNIT_WEIGHT_kN_m3
        analyser_mod.STEEL_UNIT_WEIGHT_kN_m3 = user_density
        try:
            model = self.grillage_model
            model.create_self_weight_load()
            rho_c = float(self.input_dict.get("material.deck.density", 25.0))
            model.create_deck_load(slab_thickness_m=deck_t_m, concrete_density_kN_m3=rho_c)
            cw = float(self.input_dict.get("geometry.carriageway_width", 7.5))
            bw = float(getattr(model, "w", 8.5))
            edge_clr = max(0.0, (bw - cw) / 2.0)
            model.create_wearing_course_load(thickness_m=wc_t_m, density_kN_m3=wc_rho, edge_clearance=edge_clr, partial_safety_factor=1.0)
            model.create_footpath_load()
            model.create_crash_barrier_load(barrier_load_kN_per_m=barrier_load_kN_m)
            model.create_railing_load(railing_load_kN_per_m=railing_load_kN_m)
            model.create_median_load()
            model.create_sidl_combination()
            model.create_dead_load_combination(partial_safety_factor=1.0)
        finally:
            analyser_mod.STEEL_UNIT_WEIGHT_kN_m3 = orig_density

    og.osp_grillage.OspGrillage._distribute_load_types_to_model = patched_dist
    PlateGirderBridge.add_dead_loads = patched_add_dead
    try:
        return test_tc_reg_eq_load_conservation(evidence_dir=CANDIDATES_DIR)
    finally:
        og.osp_grillage.OspGrillage._distribute_load_types_to_model = orig_dist
        PlateGirderBridge.add_dead_loads = orig_add_dead


def mut_c_eq_load_conservation():
    """
    Candidate (c): Partial candidate:
    Applies FEM distribution to patch loads (DD, DW), but leaves crash barrier line loads
    with the baseline bug, failing total force conservation (-37.5%) and barrier centroid shift (+0.75m).
    """
    import ospgrillage as og
    from ospgrillage.load import PatchLoading
    orig_dist = og.osp_grillage.OspGrillage._distribute_load_types_to_model

    def wrong_dist(self, load_case_obj):
        load_groups = getattr(load_case_obj, "load_groups", [])
        has_patch = any(isinstance(lg.get("load"), PatchLoading) for lg in load_groups)
        if has_patch:
            cmds = []
            for lg in load_groups:
                ld = lg["load"]
                if isinstance(ld, PatchLoading):
                    cmds.extend(_distribute_patch_load_fem(self, ld))
                else:
                    cmds.extend(orig_dist(self, load_case_obj))
            return cmds
        return orig_dist(self, load_case_obj)

    og.osp_grillage.OspGrillage._distribute_load_types_to_model = wrong_dist
    try:
        return test_tc_reg_eq_load_conservation(evidence_dir=CANDIDATES_DIR)
    finally:
        og.osp_grillage.OspGrillage._distribute_load_types_to_model = orig_dist


# 5. TC-REG-D01-WIND-SPEED-PROPAGATION
def mut_b_d01():
    """Candidate (b): propagates user wind speed, height, barrier, and railing height."""
    from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
    from osdagbridge.core.utils.common import (
        KEY_WL_BASIC_WIND_SPEED, KEY_WL_AVG_EXPOSED_HEIGHT, KEY_CB_HEIGHT, KEY_RL_HEIGHT,
        KEY_TS_NO_OF_GIRDERS, KEY_TS_GIRDER_SPACING, KEY_MP_GIRDER_DEPTH
    )
    orig_wind = PlateGirderBridge.add_wind_loads
    def patched_wind(self):
        inp = self.input_dict
        sp = float(inp.get(KEY_WL_BASIC_WIND_SPEED, 33.0))
        ht = float(inp.get(KEY_WL_AVG_EXPOSED_HEIGHT, 10.0))
        cb = float(inp.get(KEY_CB_HEIGHT, 0.0))
        rl = float(inp.get(KEY_RL_HEIGHT, 0.0))
        n_girders = inp[KEY_TS_NO_OF_GIRDERS]
        d_depth = max(
            self._girder_value(KEY_MP_GIRDER_DEPTH, i) for i in range(self._girder_count())
        )
        c_spacing = inp[KEY_TS_GIRDER_SPACING]
        self.grillage_model.create_wind_load(
            railing_height=rl,
            crash_barrier_height=cb,
            height_for_pz=ht,
            basic_wind_speed=sp,
            girder_section="plate",
            number_of_girders=n_girders,
            c_spacing=c_spacing,
            d_depth=d_depth,
            partial_safety_factor=1.0,
        )
    PlateGirderBridge.add_wind_loads = patched_wind
    try:
        return test_tc_reg_d01(evidence_dir=CANDIDATES_DIR)
    finally:
        PlateGirderBridge.add_wind_loads = orig_wind


def mut_c_d01():
    """Candidate (c): reads basic_wind_speed only, leaves height/barrier as defaults."""
    from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
    from osdagbridge.core.utils.common import (
        KEY_WL_BASIC_WIND_SPEED, KEY_TS_NO_OF_GIRDERS, KEY_TS_GIRDER_SPACING, KEY_MP_GIRDER_DEPTH
    )
    orig_wind = PlateGirderBridge.add_wind_loads
    def wrong_wind(self):
        inp = self.input_dict
        sp = float(inp.get(KEY_WL_BASIC_WIND_SPEED, 33.0))
        n_girders = inp[KEY_TS_NO_OF_GIRDERS]
        d_depth = max(
            self._girder_value(KEY_MP_GIRDER_DEPTH, i) for i in range(self._girder_count())
        )
        c_spacing = inp[KEY_TS_GIRDER_SPACING]
        self.grillage_model.create_wind_load(
            railing_height=0.0,
            crash_barrier_height=0.0,
            height_for_pz=10.0,
            basic_wind_speed=sp,
            girder_section="plate",
            number_of_girders=n_girders,
            c_spacing=c_spacing,
            d_depth=d_depth,
            partial_safety_factor=1.0,
        )
    PlateGirderBridge.add_wind_loads = wrong_wind
    try:
        return test_tc_reg_d01(evidence_dir=CANDIDATES_DIR)
    finally:
        PlateGirderBridge.add_wind_loads = orig_wind


# 8. TC-REG-RPT-EXEC-SUMMARY-STATUS
def mut_b_rpt():
    """
    Candidate (b): Semantic verification across all 6 scenarios:
    Dynamically derives component statuses from actual component result dictionaries
    (per_girder across all girders, crossbracing_design_results, end_diaphragm_design_results, deck_design_results).
    """
    import osdagbridge.core.reports.executive_summary as es
    orig_exec = es.executive_summary

    def patched_exec(input_dict, output_dict, fig_paths):
        tex = orig_exec(input_dict, output_dict, fig_paths)

        # 1. Girder: check all non-EB girders
        g_pass = True
        per_girder = output_dict.get("design_results", {}).get("per_girder", {})
        for g_id, g_info in per_girder.items():
            if str(g_id).startswith("EB"):
                continue
            for chk in g_info.get("checks", []):
                if chk.get("status") == "FAIL" or float(chk.get("dcr", chk.get("efficiency", 0.0))) > 1.0:
                    g_pass = False
                    break
            if not g_pass:
                break

        # 2. Cross bracing:
        cb_pass = True
        cb_res = output_dict.get("crossbracing_design_results", {})
        for p, pdata in cb_res.items():
            for m, mdata in pdata.items():
                eff = float(mdata.get("Axial", {}).get("Osdag", {}).get("efficiency", 0.0))
                if eff > 1.0:
                    cb_pass = False

        # 3. End diaphragm:
        ed_pass = True
        ed_res = output_dict.get("end_diaphragm_design_results", {})
        for p, pdata in ed_res.items():
            for m, mdata in pdata.items():
                eff = float(mdata.get("Axial", {}).get("Osdag", {}).get("efficiency", 0.0))
                if eff > 1.0:
                    ed_pass = False

        # 4. Deck:
        dk_pass = True
        dk_res = output_dict.get("deck_design_results", {})
        if float(dk_res.get("ur_moment", 0.0)) > 1.0 or float(dk_res.get("ur_shear", 0.0)) > 1.0:
            dk_pass = False

        g_str = r"\noindent Girder design pass \\" if g_pass else r"\noindent Girder design fail \\"
        cb_str = r"Cross bracing design pass \\" if cb_pass else r"Cross bracing design fail \\"
        ed_str = r"End Diaphragm design pass \\" if ed_pass else r"End Diaphragm design fail \\"
        dk_str = r"Deck design pass" if dk_pass else r"Deck design fail"

        orig_block = (
            r"\noindent Girder design pass \\" + "\n" +
            r"Cross bracing design pass \\" + "\n" +
            r"End Diaphragm design pass \\" + "\n" +
            r"Deck design pass"
        )
        new_block = f"{g_str}\n{cb_str}\n{ed_str}\n{dk_str}"
        tex = tex.replace(orig_block, new_block)

        # 5. Table Overall Design Status (audit §2, §10):
        # Synchronize whole-bridge overall design status with all components
        all_pass = g_pass and cb_pass and ed_pass and dk_pass
        if not all_pass:
            tex = re.sub(
                r"(\\textbf\{Overall Design Status\}\s*&\s*)([^\\]+)(\\\\)",
                r"\g<1>Fail\g<3>",
                tex
            )
        else:
            tex = re.sub(
                r"(\\textbf\{Overall Design Status\}\s*&\s*)([^\\]+)(\\\\)",
                r"\g<1>Pass\g<3>",
                tex
            )
        return tex

    es.executive_summary = patched_exec
    try:
        return test_tc_reg_rpt_status(evidence_dir=CANDIDATES_DIR)
    finally:
        es.executive_summary = orig_exec


def mut_c_rpt():
    """
    Candidate (c): Incomplete implementation inspecting only G1:
    Passes all-pass scenario, but fails Scenario 2A where G3 fails and G1 passes.
    """
    import osdagbridge.core.reports.executive_summary as es
    orig_exec = es.executive_summary

    def naive_g1_exec(input_dict, output_dict, fig_paths):
        tex = orig_exec(input_dict, output_dict, fig_paths)

        # Naively inspect only G1
        g_pass = True
        per_girder = output_dict.get("design_results", {}).get("per_girder", {})
        g1_info = per_girder.get("G1", {})
        for chk in g1_info.get("checks", []):
            if chk.get("status") == "FAIL" or float(chk.get("dcr", chk.get("efficiency", 0.0))) > 1.0:
                g_pass = False
                break

        cb_pass = True
        cb_res = output_dict.get("crossbracing_design_results", {})
        for p, pdata in cb_res.items():
            for m, mdata in pdata.items():
                if float(mdata.get("Axial", {}).get("Osdag", {}).get("efficiency", 0.0)) > 1.0:
                    cb_pass = False

        ed_pass = True
        ed_res = output_dict.get("end_diaphragm_design_results", {})
        for p, pdata in ed_res.items():
            for m, mdata in pdata.items():
                if float(mdata.get("Axial", {}).get("Osdag", {}).get("efficiency", 0.0)) > 1.0:
                    ed_pass = False

        dk_pass = True
        dk_res = output_dict.get("deck_design_results", {})
        if float(dk_res.get("ur_moment", 0.0)) > 1.0 or float(dk_res.get("ur_shear", 0.0)) > 1.0:
            dk_pass = False

        g_str = r"\noindent Girder design pass \\" if g_pass else r"\noindent Girder design fail \\"
        cb_str = r"Cross bracing design pass \\" if cb_pass else r"Cross bracing design fail \\"
        ed_str = r"End Diaphragm design pass \\" if ed_pass else r"End Diaphragm design fail \\"
        dk_str = r"Deck design pass" if dk_pass else r"Deck design fail"

        orig_block = (
            r"\noindent Girder design pass \\" + "\n" +
            r"Cross bracing design pass \\" + "\n" +
            r"End Diaphragm design pass \\" + "\n" +
            r"Deck design pass"
        )
        new_block = f"{g_str}\n{cb_str}\n{ed_str}\n{dk_str}"
        return tex.replace(orig_block, new_block)

    es.executive_summary = naive_g1_exec
    try:
        return test_tc_reg_rpt_status(evidence_dir=CANDIDATES_DIR)
    finally:
        es.executive_summary = orig_exec


# 9. TC-REG-GEO-GIRDER-COUNT-ALIGNMENT
def mut_b_geo_count():
    """Candidate (b): bcfg.geometry.n_girders = bridge._girder_count() (4)."""
    from osdagbridge.core.bridge_types.plate_girder.designer import BridgeConfig
    orig_from = BridgeConfig.from_plate_girder_bridge
    def patched_from(bridge):
        bcfg = orig_from(bridge)
        bcfg.geometry.n_girders = bridge._girder_count()
        return bcfg
    BridgeConfig.from_plate_girder_bridge = patched_from
    try:
        return test_tc_reg_geo_count(evidence_dir=CANDIDATES_DIR)
    finally:
        BridgeConfig.from_plate_girder_bridge = orig_from


def mut_c_geo_count():
    """Candidate (c): bcfg.geometry.n_girders = 0."""
    from osdagbridge.core.bridge_types.plate_girder.designer import BridgeConfig
    orig_from = BridgeConfig.from_plate_girder_bridge
    def wrong_from(bridge):
        bcfg = orig_from(bridge)
        bcfg.geometry.n_girders = 0
        return bcfg
    BridgeConfig.from_plate_girder_bridge = wrong_from
    try:
        return test_tc_reg_geo_count(evidence_dir=CANDIDATES_DIR)
    finally:
        BridgeConfig.from_plate_girder_bridge = orig_from


# 11. TC-REG-CAP-STIFFENER-BUCKLING
def mut_b_cap():
    """
    Candidate (b): Genuine dynamic IS 800:2007 Cl. 8.7.3.1 / Cl. 7.1.2.1 web strip buckling calculation:
    Replaces stiffener MI (Iys) with unstiffened web strip radius of gyration r_y = tw / sqrt(12),
    and evaluates Perry-Robertson column buckling curve c.
    """
    from osdagbridge.core.bridge_types.plate_girder.designer import IRC22CapacityCalculator, IS800_2007
    orig_compute = IRC22CapacityCalculator.compute_bearing_stiffener

    def patched_compute(self):
        res = orig_compute(self)
        if res.get("skipped") or res.get("design_guidance"):
            return res
        sec, mat, cfg = self.sec, self.mat, self.cfg.stiffener
        d, tw, fy, E, gm0 = sec.dw, sec.tw, mat.fy, mat.Es, mat.gamma_m0
        b1 = cfg.bs_b1_mm if cfg.bs_b1_mm > 0 else IS800_2007.cl_8_7_1_3_stiff_bearing_length(cfg.bs_R_kN, tw, sec.tf_top, 0.0, fy)
        n1 = d / 2.0
        A_wb = (b1 + n1) * tw
        KL = 0.7 * d
        r_wb = tw / math.sqrt(12.0)
        KL_r_wb = KL / r_wb if r_wb > 0 else 1e9

        fcd_wb = IS800_2007.cl_7_1_2_1_design_compressisive_stress_plategirder(fy, gm0, KL_r_wb, E)
        Fcdw_wb_kN = (fcd_wb * A_wb) / 1000.0
        res["rys_wb_mm"] = round(r_wb, 3)
        res["KL_r_wb"] = round(KL_r_wb, 3)
        res["fcd_wb_MPa"] = round(fcd_wb, 3)
        res["Fcdw_wb_kN"] = round(Fcdw_wb_kN, 3)
        return res

    IRC22CapacityCalculator.compute_bearing_stiffener = patched_compute
    try:
        return test_tc_reg_cap_stiffener(evidence_dir=CANDIDATES_DIR)
    finally:
        IRC22CapacityCalculator.compute_bearing_stiffener = orig_compute


def mut_c_cap():
    """Candidate (c): Squash load formula (fy / gm0) * A_wb / 1000 (ignores buckling)."""
    from osdagbridge.core.bridge_types.plate_girder.designer import IRC22CapacityCalculator
    orig_compute = IRC22CapacityCalculator.compute_bearing_stiffener

    def wrong_compute(self):
        res = orig_compute(self)
        sec, mat, cfg = self.sec, self.mat, self.cfg.stiffener
        d, tw, fy, gm0 = sec.dw, sec.tw, mat.fy, mat.gamma_m0
        b1 = cfg.bs_b1_mm if cfg.bs_b1_mm > 0 else 100.0
        n1 = d / 2.0
        A_wb = (b1 + n1) * tw
        res["Fcdw_wb_kN"] = (fy / gm0) * A_wb / 1000.0
        return res

    IRC22CapacityCalculator.compute_bearing_stiffener = wrong_compute
    try:
        return test_tc_reg_cap_stiffener(evidence_dir=CANDIDATES_DIR)
    finally:
        IRC22CapacityCalculator.compute_bearing_stiffener = orig_compute


# 12. TC-REG-MAT-DENSITY-CONSISTENCY
def mut_b_mat():
    """Candidate (b): Dynamically reads user density from material.girder.density and applies to self-weight line loads."""
    import osdagbridge.core.bridge_types.plate_girder.analyser as analyser_mod
    from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
    orig_add_dl = PlateGirderBridge.add_dead_loads

    def patched_add_dl(self):
        user_density = float(self.input_dict.get("material.girder.density", 78.5))
        orig_density = analyser_mod.STEEL_UNIT_WEIGHT_kN_m3
        analyser_mod.STEEL_UNIT_WEIGHT_kN_m3 = user_density
        try:
            orig_add_dl(self)
        finally:
            analyser_mod.STEEL_UNIT_WEIGHT_kN_m3 = orig_density

    PlateGirderBridge.add_dead_loads = patched_add_dl
    try:
        return test_tc_reg_mat_density(evidence_dir=CANDIDATES_DIR)
    finally:
        PlateGirderBridge.add_dead_loads = orig_add_dl


def mut_c_mat():
    """Candidate (c): Hardcodes 78.5 kN/m3 (database default), ignoring user input."""
    from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
    orig_add_dl = PlateGirderBridge.add_dead_loads
    def wrong_add_dl(self):
        orig_add_dl(self)
    PlateGirderBridge.add_dead_loads = wrong_add_dl
    try:
        return test_tc_reg_mat_density(evidence_dir=CANDIDATES_DIR)
    finally:
        PlateGirderBridge.add_dead_loads = orig_add_dl


# 13. TC-REG-FS-CLEAN-WORKING-TREE
def mut_b_fs():
    """Candidate (b): Anchors DB_PATH and Database default constructor to User AppData, without package writes or cwd side effects."""
    import osdagbridge.core.bridge_types.plate_girder.ui_fields_project_location as ui_loc
    from osdagbridge.core.data.project_location.database import Database
    orig_db_path = ui_loc.DB_PATH
    orig_init = Database.__init__
    user_appdata_dir = os.path.join(tempfile.gettempdir(), "OsdagBridgeAppData")
    os.makedirs(user_appdata_dir, exist_ok=True)
    user_appdata_db = os.path.join(user_appdata_dir, "weather.sqlite")
    ui_loc.DB_PATH = user_appdata_db

    def patched_init(self, db_name='weather.sqlite'):
        if db_name == 'weather.sqlite' or db_name is None:
            db_name = user_appdata_db
        orig_init(self, db_name=db_name)

    Database.__init__ = patched_init

    candidate_patch = f"""import os, tempfile
import osdagbridge.core.bridge_types.plate_girder.ui_fields_project_location as ui_loc
from osdagbridge.core.data.project_location.database import Database

user_appdata_dir = {repr(user_appdata_dir)}
user_appdata_db = {repr(user_appdata_db)}
os.makedirs(user_appdata_dir, exist_ok=True)
ui_loc.DB_PATH = user_appdata_db

orig_init = Database.__init__
def patched_init(self, db_name='weather.sqlite'):
    if db_name == 'weather.sqlite' or db_name is None:
        db_name = user_appdata_db
    orig_init(self, db_name=db_name)
Database.__init__ = patched_init
"""

    try:
        return test_tc_reg_fs_clean(evidence_dir=CANDIDATES_DIR, candidate_patch=candidate_patch)
    finally:
        ui_loc.DB_PATH = orig_db_path
        Database.__init__ = orig_init


def mut_c_fs():
    """Candidate (c): Anchors ui module DB_PATH, but leaves Database.__init__ unanchored, failing cwd check."""
    import osdagbridge.core.bridge_types.plate_girder.ui_fields_project_location as ui_loc
    orig_db_path = ui_loc.DB_PATH
    user_appdata_dir = os.path.join(tempfile.gettempdir(), "OsdagBridgeAppData")
    os.makedirs(user_appdata_dir, exist_ok=True)
    user_appdata_db = os.path.join(user_appdata_dir, "weather.sqlite")
    ui_loc.DB_PATH = user_appdata_db

    candidate_patch = f"""import os
import osdagbridge.core.bridge_types.plate_girder.ui_fields_project_location as ui_loc

user_appdata_dir = {repr(user_appdata_dir)}
user_appdata_db = {repr(user_appdata_db)}
os.makedirs(user_appdata_dir, exist_ok=True)
ui_loc.DB_PATH = user_appdata_db
"""

    try:
        return test_tc_reg_fs_clean(evidence_dir=CANDIDATES_DIR, candidate_patch=candidate_patch)
    finally:
        ui_loc.DB_PATH = orig_db_path


# 14. TC-REG-CAD-EXPORT-VS-SCREENSHOT
def mut_b_cad():
    """Candidate (b): Baseline CAD export already passes."""
    return test_tc_reg_cad_export(evidence_dir=CANDIDATES_DIR)


def mut_c_cad():
    """Candidate (c): Export produces a blank uniform image (std=0.0)."""
    from OCC.Display.OCCViewer import Viewer3d
    from PIL import Image
    orig_export = Viewer3d.ExportToImage

    def wrong_export(self, filepath):
        img = Image.new("RGB", (656, 519), color=(200, 200, 200))
        img.save(filepath)

    Viewer3d.ExportToImage = wrong_export
    try:
        return test_tc_reg_cad_export(evidence_dir=CANDIDATES_DIR)
    finally:
        Viewer3d.ExportToImage = orig_export


class TeeStream:
    """Captures live stream output into memory while preserving original terminal output."""
    def __init__(self, original):
        self.original = original
        self.buffer = []

    def write(self, s):
        self.original.write(s)
        self.buffer.append(s)

    def flush(self):
        self.original.flush()

    def get_value(self):
        return "".join(self.buffer)

    def getvalue(self):
        return "".join(self.buffer)


# =============================================================================
# Main Sensitivity Matrix Orchestrator
# =============================================================================
def main():
    stdout_tee = TeeStream(sys.stdout)
    stderr_tee = TeeStream(sys.stderr)
    sys.stdout = stdout_tee
    sys.stderr = stderr_tee

    global SENSITIVITY_DIR, CANDIDATES_DIR
    import argparse
    parser = argparse.ArgumentParser(description="Phase 2.12 Sensitivity Matrix Harness")
    parser.add_argument("--evidence-dir", default=None,
                        help="Target directory for sensitivity matrix summary and logs.")
    parser.add_argument("--candidates-dir", default=None,
                        help="Target directory for candidate condition logs.")
    args = parser.parse_args()

    # Fail-closed evidence directory handling:
    # If not supplied, generate an isolated timestamped run directory under testing/evidence/runs/
    if args.evidence_dir:
        SENSITIVITY_DIR = os.path.abspath(args.evidence_dir)
    else:
        run_ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
        SENSITIVITY_DIR = os.path.abspath(os.path.join(WORKSPACE_ROOT, "testing", "evidence", "runs", f"sensitivity_{run_ts}"))

    if args.candidates_dir:
        CANDIDATES_DIR = os.path.abspath(args.candidates_dir)
    else:
        run_ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
        CANDIDATES_DIR = os.path.abspath(os.path.join(WORKSPACE_ROOT, "testing", "evidence", "runs", f"candidates_{run_ts}"))

    # Fail-closed evidence directory validation
    validate_evidence_directory(SENSITIVITY_DIR, phase_label="Phase 2.11 Sensitivity", allow_creation=True)
    validate_evidence_directory(CANDIDATES_DIR, phase_label="Phase 2.11 Candidates", allow_creation=True)

    # Provenance tracking
    guard_path = os.path.join(SCRIPT_DIR, "evidence_guard.py")
    baseline_runner_path = os.path.join(SCRIPT_DIR, "run_all_baseline_tests.py")
    guard_self_hash = sha256_file(guard_path) if os.path.exists(guard_path) else "UNKNOWN"
    runner_self_hash = sha256_file(os.path.abspath(__file__)) if os.path.exists(os.path.abspath(__file__)) else "UNKNOWN"
    baseline_runner_self_hash = sha256_file(baseline_runner_path) if os.path.exists(baseline_runner_path) else "UNKNOWN"

    t_start = time.time()
    print("=" * 80)
    print("PHASE 2.11 SENSITIVITY MATRIX HARNESS — STRICT CANDIDATE VALIDATION")
    print(f"Workspace Root:            {WORKSPACE_ROOT}")
    print(f"Sensitivity Dir:           {SENSITIVITY_DIR}")
    print(f"Candidates Dir:            {CANDIDATES_DIR}")
    print(f"Baseline Commit:           {BASELINE_COMMIT}")
    print(f"evidence_guard.py SHA256:  {guard_self_hash}")
    print(f"runner SHA256:             {runner_self_hash}")
    print(f"baseline runner SHA256:    {baseline_runner_self_hash}")
    print("=" * 80)

    # Registry of 15 regression tests: (test_id, defect_id, fn_a, fn_b, fn_c, is_blocked, block_reason)
    test_registry = [
        ("TC-REG-A01-FACTOR-SCALING", "DEF-01 (Upstream)", test_tc_reg_a01, mut_b_a01, mut_c_a01, False, ""),
        ("TC-REG-B01-SECTION-PROPERTY-SYNC", "DEF-03", test_tc_reg_b01, mut_b_b01, mut_c_b01, False, ""),
        ("TC-REG-C01-SECTIONAL-STRESS-RANGE", "DEF-07", test_tc_reg_c01, mut_b_c01, mut_c_c01, False, ""),
        ("TC-REG-A02-ULS-COMBINATION-SUM", "DEF-01 / DEF-02", test_tc_reg_a02, mut_b_a02, mut_c_a02, False, ""),
        ("TC-REG-EQ-LOAD-CONSERVATION", "DEF-18", test_tc_reg_eq_load_conservation, mut_b_eq_load_conservation, mut_c_eq_load_conservation, False, ""),
        ("TC-REG-D01-WIND-SPEED-PROPAGATION", "DEF-05", test_tc_reg_d01, mut_b_d01, mut_c_d01, False, ""),
        ("TC-REG-D02-TEMPERATURE-PROPAGATION", "DEF-06", test_tc_reg_d02, None, None, True, "DEC-015 Pending: Thermal modeling undecided under IRC 6 Cl. 215"),
        ("TC-REG-C02-FATIGUE-VEHICLE-ANALYSIS", "DEF-17", test_tc_reg_c02, None, None, True, "DEC-018 Pending: IRC 6 Cl. 204.6 fatigue vehicle moving load not implemented in analysis/design pipeline"),
        ("TC-REG-RPT-EXEC-SUMMARY-STATUS", "DEF-08", test_tc_reg_rpt_status, mut_b_rpt, mut_c_rpt, False, ""),
        ("TC-REG-GEO-GIRDER-COUNT-ALIGNMENT", "DEF-11", test_tc_reg_geo_count, mut_b_geo_count, mut_c_geo_count, False, ""),
        ("TC-REG-GEO-SLAB-SECTION-PROPERTIES", "DEF-14", test_tc_reg_geo_slab, None, None, True, "DEC-013 Pending: Transverse deck slab representation model undecided"),
        ("TC-REG-CAP-STIFFENER-BUCKLING", "DEF-12", test_tc_reg_cap_stiffener, mut_b_cap, mut_c_cap, False, ""),
        ("TC-REG-MAT-DENSITY-CONSISTENCY", "DEF-13", test_tc_reg_mat_density, mut_b_mat, mut_c_mat, False, ""),
        ("TC-REG-FS-CLEAN-WORKING-TREE", "DEF-10", test_tc_reg_fs_clean, mut_b_fs, mut_c_fs, False, ""),
        ("TC-REG-CAD-EXPORT-VS-SCREENSHOT", "DEF-09 (Harness)", test_tc_reg_cad_export, mut_b_cad, mut_c_cad, False, ""),
    ]

    matrix_results = []
    actionable_verified_count = 0
    blocked_count = 0

    for test_id, defect_id, fn_a, fn_b, fn_c, is_blocked, block_reason in test_registry:
        entry = run_sensitivity_test(test_id, defect_id, fn_a, fn_b, fn_c, is_blocked, block_reason)
        matrix_results.append(entry)

        v_str = entry["sensitivity_status"]
        conds = entry["conditions"]
        st_a = conds["a_baseline"]["observed_status"]
        st_b = conds["b_minimal_correct"]["observed_status"]
        st_c = conds["c_plausible_wrong"]["observed_status"]

        print(f"[{v_str:<26}] {test_id:<36} | (a) {st_a:<13} | (b) {st_b:<7} | (c) {st_c:<13}")
        if is_blocked:
            blocked_count += 1
        elif entry["sensitivity_verified"]:
            actionable_verified_count += 1

    total_duration = time.time() - t_start
    total_actionable = len(test_registry) - blocked_count
    all_actionable_verified = (actionable_verified_count == total_actionable)

    print("\n" + "=" * 80)
    print(f"SENSITIVITY MATRIX EXECUTION COMPLETED ({total_duration:.2f} s)")
    print(f"Actionable Tests Verified:       {actionable_verified_count} / {total_actionable}")
    print(f"Blocked (Undecided Specs):       {blocked_count} / {len(test_registry)}")
    print(f"Overall Actionable Gate Status:  {'PASSED' if all_actionable_verified else 'FAILED'}")
    print("=" * 80)

    summary_file = os.path.join(SENSITIVITY_DIR, "phase_2_13_sensitivity_matrix_summary.json")
    with safe_open_evidence(summary_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "total_duration_sec": round(total_duration, 2),
            "baseline_commit": BASELINE_COMMIT,
            "provenance": {
                "guard_self_hash": guard_self_hash,
                "runner_self_hash": runner_self_hash,
                "baseline_runner_self_hash": baseline_runner_self_hash
            },
            "actionable_tests_verified": actionable_verified_count,
            "actionable_tests_total": total_actionable,
            "blocked_tests_count": blocked_count,
            "all_actionable_verified": all_actionable_verified,
            "matrix": matrix_results
        }, f, indent=2)
    print(f"Saved complete sensitivity summary to: {summary_file}")

    exit_code = 0 if all_actionable_verified else 1
    with safe_open_evidence(os.path.join(SENSITIVITY_DIR, "sensitivity_exit_code.txt"), "w", encoding="utf-8") as f:
        f.write(str(exit_code) + "\n")

    # Write live console logs before sealing manifest (F-12)
    sys.stdout = stdout_tee.original
    sys.stderr = stderr_tee.original
    safe_write_evidence(os.path.join(SENSITIVITY_DIR, "console_output.txt"), stdout_tee.getvalue())
    safe_write_evidence(os.path.join(SENSITIVITY_DIR, "console_error.txt"), stderr_tee.getvalue())

    # Generate and seal manifest for SENSITIVITY_DIR and CANDIDATES_DIR
    print("Generating and sealing cryptographic manifests for sensitivity and candidate directories...")
    sens_manifest, sens_seal = generate_and_seal_manifest(SENSITIVITY_DIR, runner_id="sensitivity_runner", phase_label="Phase 2.13 Sensitivity")
    cand_manifest, cand_seal = generate_and_seal_manifest(CANDIDATES_DIR, runner_id="candidates_runner", phase_label="Phase 2.13 Candidates")
    print(f"Sensitivity manifest sealed: {sens_seal.get('run_uuid')}")
    print(f"Candidates manifest sealed: {cand_seal.get('run_uuid')}")

    # Manifest integrity verification
    print("Verifying manifest integrity across sensitivity and candidates directories...")
    sens_ok, sens_errs, _ = verify_manifest_integrity(SENSITIVITY_DIR)
    cand_ok, cand_errs, _ = verify_manifest_integrity(CANDIDATES_DIR)
    if not (sens_ok and cand_ok):
        print(f"CRITICAL: Manifest integrity verification failed: {sens_errs} {cand_errs}")
        sys.exit(1)
    print("Manifest integrity verification: SUCCESS")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
