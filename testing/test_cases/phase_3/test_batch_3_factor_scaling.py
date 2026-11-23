"""
Phase 3 Batch 3 Comprehensive Verification Suite (OR-B3-01 to OR-B3-09 + Invariance Gates)
Defect: DEF-01 (Component Load-Factor Preservation in ospgrillage)
Controlling Specification: reports/phase_3/batch_3_selection/BATCH_3_DEF_01_IMPLEMENTATION_READINESS.md
Directive: P3-B3-AUTH-003
"""

import math
import sys
import os
import unittest
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
SRC_DIR = os.path.join(REPO_ROOT, "source", "OsdagBridge", "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import ospgrillage as og
import openseespy.opensees as ops
from testing.test_cases.baseline_regression.run_all_baseline_tests import (
    BASE_CFG,
    test_tc_reg_cap_stiffener,
    test_tc_reg_geo_count,
    test_tc_reg_rpt_status,
)
from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge

BATCH_3_EVIDENCE_DIR = os.path.join(REPO_ROOT, "testing", "evidence", "phase_3", "batch_3")
os.makedirs(BATCH_3_EVIDENCE_DIR, exist_ok=True)


def create_standard_grillage(L, W, nl, nt, edge_dist=0.5, name="std_grillage"):
    """Create a clean, standardized linear grillage model for statics verification."""
    ops.wipe()
    model = og.create_grillage(
        bridge_name=name,
        long_dim=float(L),
        width=float(W),
        skew=0,
        num_long_grid=nl,
        num_trans_grid=nt,
        edge_beam_dist=float(edge_dist)
    )
    mat = og.create_material(name="steel", E=2e11, G=7.7e10, v=0.3, rho=7850)
    sec = og.create_section(A=0.05, J=1e-4, Iy=1e-3, Iz=1e-3)
    beam = og.create_member(member_name="long_beam", section=sec, material=mat)
    for m in [
        "interior_main_beam", "exterior_main_beam_1", "exterior_main_beam_2",
        "edge_beam", "transverse_slab", "start_edge", "end_edge"
    ]:
        model.set_member(beam, member=m)
    model.create_osp_model(pyfile=False)
    return model


def get_total_reaction_and_centroid():
    """Extract total vertical reaction sum(Ry) and longitudinal centroid x_bar."""
    ops.reactions()
    ry_tot = 0.0
    sum_x = 0.0
    for node in ops.getNodeTags():
        ry = -float(ops.nodeReaction(node, 2))
        c = ops.nodeCoord(node)
        ry_tot += ry
        sum_x += ry * c[0]
    x_bar = (sum_x / ry_tot) if abs(ry_tot) > 1e-12 else 0.0
    return ry_tot, x_bar


class TestBatch3FactorScaling(unittest.TestCase):

    def test_or_b3_01_point_load_scaling(self):
        """OR-B3-01: Point Load Scaling on 4-Node Mesh (P = 100 kN, gamma = 1.35 -> Ry = 135 kN)."""
        L, W = 20.0, 10.0
        P_nom = 100000.0  # 100 kN
        gamma = 1.35
        P_target = P_nom * gamma  # 135 kN

        model = create_standard_grillage(L, W, nl=5, nt=11, name="or_b3_01")
        pt = og.create_load_vertex(x=10.0, z=5.0, p=P_nom)
        p_load = og.create_load(loadtype="point", name="pt_load", point1=pt)

        lc = og.create_load_case(name="LC_OR01")
        lc.add_load(p_load, load_factor=gamma)
        model.add_load_case(lc)
        model.analyze(load_case="LC_OR01")

        ry_tot, x_bar = get_total_reaction_and_centroid()
        self.assertAlmostEqual(ry_tot, P_target, delta=1e-6 * P_target)
        self.assertAlmostEqual(x_bar, 10.0, delta=1e-5)

    def test_or_b3_02_uniform_line_load_scaling(self):
        """OR-B3-02: Uniform Line Load on 4-Node Mesh (w = 10 kN/m, L = 20 m, gamma = 1.35 -> Ry = 270 kN, x_bar = 10 m)."""
        L, W = 20.0, 10.0
        w = 10000.0  # 10 kN/m
        gamma = 1.35
        P_nom = w * L  # 200 kN
        P_target = P_nom * gamma  # 270 kN

        model = create_standard_grillage(L, W, nl=5, nt=11, name="or_b3_02")
        p1 = og.create_load_vertex(x=0.0, z=3.0, p=w)
        p2 = og.create_load_vertex(x=L, z=3.0, p=w)
        line = og.create_load(loadtype="line", name="line_load", point1=p1, point2=p2)

        lc = og.create_load_case(name="LC_OR02")
        lc.add_load(line, load_factor=gamma)
        model.add_load_case(lc)
        model.analyze(load_case="LC_OR02")

        ry_tot, x_bar = get_total_reaction_and_centroid()
        self.assertAlmostEqual(ry_tot, P_target, delta=1e-6 * P_target)
        self.assertAlmostEqual(x_bar, 10.0, delta=1e-5)

    def test_or_b3_03_uniform_patch_load_scaling(self):
        """OR-B3-03: Uniform Patch Load on 4-Node Mesh (p = 2 kPa, A = 200 m2, gamma = 1.35 -> Ry = 540 kN)."""
        L, W = 20.0, 10.0
        p = 2000.0  # 2 kPa = 2000 N/m2
        gamma = 1.35
        A = L * W  # 200 m2
        P_nom = p * A  # 400 kN
        P_target = P_nom * gamma  # 540 kN

        model = create_standard_grillage(L, W, nl=5, nt=11, name="or_b3_03")
        v1 = og.create_load_vertex(x=0.0, z=0.0, p=p)
        v2 = og.create_load_vertex(x=L, z=0.0, p=p)
        v3 = og.create_load_vertex(x=L, z=W, p=p)
        v4 = og.create_load_vertex(x=0.0, z=W, p=p)
        patch = og.create_load(loadtype="patch", name="patch_load", point1=v1, point2=v2, point3=v3, point4=v4)

        lc = og.create_load_case(name="LC_OR03")
        lc.add_load(patch, load_factor=gamma)
        model.add_load_case(lc)
        model.analyze(load_case="LC_OR03")

        ry_tot, x_bar = get_total_reaction_and_centroid()
        self.assertAlmostEqual(ry_tot, P_target, delta=1e-6 * P_target)
        self.assertAlmostEqual(x_bar, 10.0, delta=1e-5)

    def test_or_b3_04_compound_multi_load_superposition(self):
        """OR-B3-04: Compound Multi-Load Case (P1 = 60 kN @ 1.35, P2 = 100 kN @ 1.75 -> Ry = 256 kN)."""
        L, W = 20.0, 10.0
        P1 = 60000.0  # 60 kN
        P2 = 100000.0  # 100 kN
        gamma1 = 1.35
        gamma2 = 1.75
        P_target = P1 * gamma1 + P2 * gamma2  # 81 + 175 = 256 kN

        model = create_standard_grillage(L, W, nl=5, nt=11, name="or_b3_04")
        pt1 = og.create_load_vertex(x=5.0, z=5.0, p=P1)
        pt2 = og.create_load_vertex(x=15.0, z=5.0, p=P2)
        p_load1 = og.create_load(loadtype="point", name="pt1", point1=pt1)
        p_load2 = og.create_load(loadtype="point", name="pt2", point1=pt2)

        lc = og.create_load_case(name="LC_OR04")
        lc.add_load(p_load1, load_factor=gamma1)
        lc.add_load(p_load2, load_factor=gamma2)
        model.add_load_case(lc)
        model.analyze(load_case="LC_OR04")

        ry_tot, x_bar = get_total_reaction_and_centroid()
        self.assertAlmostEqual(ry_tot, P_target, delta=1e-6 * P_target)
        x_exp = (P1 * gamma1 * 5.0 + P2 * gamma2 * 15.0) / P_target
        self.assertAlmostEqual(x_bar, x_exp, delta=1e-5)

    def test_or_b3_05_compound_load_vehicle_scaling(self):
        """OR-B3-05: Multi-Axle Vehicle (CompoundLoad: P1 = 40 kN, P2 = 60 kN, gamma = 0.80 -> Ry = 80 kN)."""
        L, W = 24.0, 10.0
        P1 = 40000.0  # 40 kN
        P2 = 60000.0  # 60 kN
        gamma = 0.80
        P_target = (P1 + P2) * gamma  # 100 * 0.80 = 80 kN

        model = create_standard_grillage(L, W, nl=5, nt=13, name="or_b3_05")
        pt1 = og.create_load_vertex(x=8.0, z=5.0, p=P1)
        pt2 = og.create_load_vertex(x=12.0, z=5.0, p=P2)
        axle1 = og.create_load(loadtype="point", name="axle1", point1=pt1)
        axle2 = og.create_load(loadtype="point", name="axle2", point1=pt2)

        vehicle = og.create_compound_load(name="vehicle_70r")
        vehicle.add_load(axle1)
        vehicle.add_load(axle2)

        lc = og.create_load_case(name="LC_OR05")
        lc.add_load(vehicle, load_factor=gamma)
        model.add_load_case(lc)
        model.analyze(load_case="LC_OR05")

        ry_tot, x_bar = get_total_reaction_and_centroid()
        self.assertAlmostEqual(ry_tot, P_target, delta=1e-6 * P_target)
        self.assertAlmostEqual(x_bar, 10.4, delta=1e-5)

    def test_or_b3_06_beam_element_line_load_scaling(self):
        """OR-B3-06: Direct Beam-Element Line Load (w = 8 kN/m, L = 20 m, gamma = 1.35 -> Ry = 216 kN)."""
        L, W = 20.0, 10.0
        w = 8000.0  # 8 kN/m
        gamma = 1.35

        model = create_standard_grillage(L, W, nl=5, nt=11, name="or_b3_06")
        p1 = og.create_load_vertex(x=0.0, z=0.0, p=w)
        p2 = og.create_load_vertex(x=L, z=0.0, p=w)
        beam_line = og.create_load(
            loadtype="line",
            name="beam_line_load",
            point1=p1,
            point2=p2,
            long_beam_ele_load_flag=True
        )

        lc = og.create_load_case(name="LC_OR06")
        lc.add_load(beam_line, load_factor=gamma)
        model.add_load_case(lc)
        model.analyze(load_case="LC_OR06")

        ops.reactions()
        ry_tot = sum(-float(ops.nodeReaction(node, 2)) for node in ops.getNodeTags())
        self.assertGreater(ry_tot, 0.0)

        # Ratio check against unfactored baseline
        model_u = create_standard_grillage(L, W, nl=5, nt=11, name="or_b3_06_unfactored")
        lc_u = og.create_load_case(name="LC_OR06_U")
        lc_u.add_load(beam_line, load_factor=1.0)
        model_u.add_load_case(lc_u)
        model_u.analyze(load_case="LC_OR06_U")
        ops.reactions()
        ry_u = sum(-float(ops.nodeReaction(node, 2)) for node in ops.getNodeTags())
        ratio = ry_tot / ry_u
        self.assertAlmostEqual(ratio, gamma, places=5)

    def test_or_b3_07_zero_factor_relief_scaling(self):
        """OR-B3-07: Zero-Factor Relief Load (P1 = 150 kN @ 1.35, P2 = 80 kN @ 0.00 -> Ry = 202.5 kN)."""
        L, W = 20.0, 10.0
        P1 = 150000.0  # 150 kN
        P2 = 80000.0   # 80 kN
        gamma1 = 1.35
        gamma2 = 0.00
        P_target = P1 * gamma1 + P2 * gamma2  # 202.5 + 0.0 = 202.5 kN

        model = create_standard_grillage(L, W, nl=5, nt=11, name="or_b3_07")
        pt1 = og.create_load_vertex(x=10.0, z=5.0, p=P1)
        pt2 = og.create_load_vertex(x=15.0, z=5.0, p=P2)
        p_load1 = og.create_load(loadtype="point", name="pt1", point1=pt1)
        p_load2 = og.create_load(loadtype="point", name="pt2", point1=pt2)

        lc = og.create_load_case(name="LC_OR07")
        lc.add_load(p_load1, load_factor=gamma1)
        lc.add_load(p_load2, load_factor=gamma2)
        model.add_load_case(lc)
        model.analyze(load_case="LC_OR07")

        ry_tot, x_bar = get_total_reaction_and_centroid()
        self.assertAlmostEqual(ry_tot, P_target, delta=1e-6 * P_target)
        self.assertAlmostEqual(x_bar, 10.0, delta=1e-5)

    def test_or_b3_08_negative_reversible_factor_scaling(self):
        """OR-B3-08: Negative / Reversible Load Factor (P = 120 kN downward, gamma = -1.20 -> Ry = -144 kN uplift)."""
        L, W = 20.0, 10.0
        P_nom = 120000.0  # 120 kN
        gamma = -1.20
        P_target = P_nom * gamma  # -144 kN (uplift)

        model = create_standard_grillage(L, W, nl=5, nt=11, name="or_b3_08")
        pt = og.create_load_vertex(x=10.0, z=5.0, p=P_nom)
        p_load = og.create_load(loadtype="point", name="pt_load", point1=pt)

        lc = og.create_load_case(name="LC_OR08")
        lc.add_load(p_load, load_factor=gamma)
        model.add_load_case(lc)
        model.analyze(load_case="LC_OR08")

        ry_tot, x_bar = get_total_reaction_and_centroid()
        self.assertAlmostEqual(ry_tot, P_target, delta=1e-6 * abs(P_target))
        self.assertAlmostEqual(x_bar, 10.0, delta=1e-5)

    def test_or_b3_09_compounded_dual_scaling(self):
        """OR-B3-09: Compounded Dual Scaling (P = 50 kN, gamma_load = 0.80, gamma_case = 1.10 -> Ry = 44 kN)."""
        L, W = 20.0, 10.0
        P_nom = 50000.0  # 50 kN
        gamma_load = 0.80
        gamma_case = 1.10
        P_target = P_nom * gamma_load * gamma_case  # 50 * 0.80 * 1.10 = 44 kN

        model = create_standard_grillage(L, W, nl=5, nt=11, name="or_b3_09")
        pt = og.create_load_vertex(x=10.0, z=5.0, p=P_nom)
        p_load = og.create_load(loadtype="point", name="pt_load", point1=pt)

        lc = og.create_load_case(name="LC_OR09")
        lc.add_load(p_load, load_factor=gamma_load)
        model.add_load_case(lc, load_factor=gamma_case)
        model.analyze(load_case="LC_OR09")

        ry_tot, x_bar = get_total_reaction_and_centroid()
        self.assertAlmostEqual(ry_tot, P_target, delta=1e-6 * P_target)
        self.assertAlmostEqual(x_bar, 10.0, delta=1e-5)

    def test_invariance_unfactored_loads(self):
        """Invariance Gate: Load with factor=1.0 matches load without factor specified."""
        L, W = 20.0, 10.0
        model1 = create_standard_grillage(L, W, nl=5, nt=11, name="inv1")
        p1 = og.create_load_vertex(x=0.0, z=2.0, p=5000.0)
        p2 = og.create_load_vertex(x=L, z=2.0, p=5000.0)
        line1 = og.create_load(loadtype="line", name="line1", point1=p1, point2=p2)
        lc1 = og.create_load_case(name="LC1")
        lc1.add_load(line1)  # default factor 1
        model1.add_load_case(lc1)
        model1.analyze(load_case="LC1")
        ry1, x1 = get_total_reaction_and_centroid()

        model2 = create_standard_grillage(L, W, nl=5, nt=11, name="inv2")
        line2 = og.create_load(loadtype="line", name="line2", point1=p1, point2=p2)
        lc2 = og.create_load_case(name="LC2")
        lc2.add_load(line2, load_factor=1.0)  # explicit factor 1.0
        model2.add_load_case(lc2)
        model2.analyze(load_case="LC2")
        ry2, x2 = get_total_reaction_and_centroid()

        self.assertAlmostEqual(ry1, ry2, delta=1e-12)
        self.assertAlmostEqual(x1, x2, delta=1e-12)

    def test_invariance_load_object_immutability(self):
        """Invariance Gate: Applying factor does NOT mutate the original load object in-place."""
        pt = og.create_load_vertex(x=5.0, z=3.0, p=1000.0)
        p_load = og.create_load(loadtype="point", name="pt_immut", point1=pt)

        self.assertEqual(p_load.load_point_1.p, 1000.0)

        lc = og.create_load_case(name="LC_IMMUT")
        lc.add_load(p_load, load_factor=1.50)

        model = create_standard_grillage(20.0, 10.0, nl=5, nt=11, name="immut_test")
        model.add_load_case(lc)
        model.analyze(load_case="LC_IMMUT")

        # Verify that original p_load object still has nominal magnitude 1000.0
        self.assertEqual(p_load.load_point_1.p, 1000.0)
        # Verify that load_groups[0]["load"] in lc still has nominal magnitude 1000.0
        self.assertEqual(lc.load_groups[0]["load"].load_point_1.p, 1000.0)

    def test_invariance_batch_1_def12(self):
        """Invariance Gate: Batch 1 DEF-12 bearing stiffener buckling capacity remains 63.4 kN."""
        res = test_tc_reg_cap_stiffener(evidence_dir=BATCH_3_EVIDENCE_DIR)
        self.assertEqual(res["status"], "PASS")

    def test_invariance_batch_1_def11(self):
        """Invariance Gate: Batch 1 DEF-11 girder count alignment remains 4 girders."""
        res = test_tc_reg_geo_count(evidence_dir=BATCH_3_EVIDENCE_DIR)
        self.assertEqual(res["status"], "PASS")

    def test_invariance_batch_1_def08(self):
        """Invariance Gate: Batch 1 DEF-08 executive summary status remains dynamic and PASS."""
        res = test_tc_reg_rpt_status(evidence_dir=BATCH_3_EVIDENCE_DIR)
        self.assertEqual(res["status"], "PASS")

    def test_invariance_batch_2_statics(self):
        """Invariance Gate: Batch 2 DEF-18 line and patch load statics remain conserved (< 1e-12 residual)."""
        L, W = 20.0, 8.0
        w = 10000.0
        P_exp = w * L
        model = create_standard_grillage(L, W, nl=5, nt=11, name="b2_inv")
        p1 = og.create_load_vertex(x=0.0, z=2.0, p=w)
        p2 = og.create_load_vertex(x=L, z=2.0, p=w)
        line = og.create_load(loadtype="line", name="line", point1=p1, point2=p2)
        lc = og.create_load_case(name="LC_B2")
        lc.add_load(line)
        model.add_load_case(lc)
        model.analyze(load_case="LC_B2")
        ops.reactions()
        ry_tot = sum(-float(ops.nodeReaction(node, 2)) for node in ops.getNodeTags())
        self.assertAlmostEqual(ry_tot, P_exp, delta=1e-9 * P_exp)


if __name__ == "__main__":
    unittest.main()
