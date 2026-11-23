"""
Phase 3 Batch 2 Comprehensive Verification Suite (17/17 Tests)
Defect: DEF-18 (Grillage Load Distribution Statics & Conservation)
Specification: reports/phase_3/batch_2_readiness/DEF_18_PROPOSED_TEST_MATRIX.md
"""

import math
import sys
import os
import unittest

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
)
from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
from osdagbridge.core.bridge_types.plate_girder.designer import BridgeConfig
from osdagbridge.core.reports.executive_summary import executive_summary


def create_standard_grillage(L, W, nl, nt, edge_dist=0.5, name="std_grillage"):
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


class TestBatch2Comprehensive(unittest.TestCase):

    def test_tc_b2_01_line_scale_uniform(self):
        """TC-B2-01: Line force conservation across mesh densities (dx = 1.0, 2.0 m)."""
        L = 20.0
        w = 10000.0
        P_exp = w * L
        for nt in [21, 11]:
            model = create_standard_grillage(L, 8.0, nl=5, nt=nt, name=f"mesh_{nt}")
            p1 = og.create_load_vertex(x=0.0, z=2.0, p=w)
            p2 = og.create_load_vertex(x=L, z=2.0, p=w)
            line = og.create_load(loadtype="line", name="line", point1=p1, point2=p2)
            lc = og.create_load_case(name="LC")
            lc.add_load(line)
            model.add_load_case(lc)
            model.analyze(load_case="LC")
            ops.reactions()
            ry_tot = sum(-float(ops.nodeReaction(node, 2)) for node in ops.getNodeTags())
            self.assertAlmostEqual(ry_tot, P_exp, delta=1e-9 * P_exp)

    def test_tc_b2_02_line_small_mag(self):
        """TC-B2-02: Micro-load magnitude scaling and first-bay inclusion (w = 1.0 N/m)."""
        L = 24.0
        w = 1.0
        P_exp = w * L
        model = create_standard_grillage(L, 8.5, nl=5, nt=17, name="micro")
        p1 = og.create_load_vertex(x=0.0, z=2.0, p=w)
        p2 = og.create_load_vertex(x=L, z=2.0, p=w)
        line = og.create_load(loadtype="line", name="micro_line", point1=p1, point2=p2)
        lc = og.create_load_case(name="LC")
        lc.add_load(line)
        model.add_load_case(lc)
        model.analyze(load_case="LC")
        ops.reactions()
        ry_tot = 0.0
        sum_x = 0.0
        for node in ops.getNodeTags():
            ry = -float(ops.nodeReaction(node, 2))
            c = ops.nodeCoord(node)
            ry_tot += ry
            sum_x += ry * c[0]
        self.assertAlmostEqual(ry_tot, P_exp, delta=1e-6 * P_exp)
        self.assertAlmostEqual(sum_x / ry_tot, 12.0, delta=1e-5)

    def test_tc_b2_03_line_asymmetric_partial(self):
        """TC-B2-03: Partial line load equilibrium and centroid (x in [4, 16] m)."""
        model = create_standard_grillage(24.0, 8.5, nl=5, nt=17, name="part")
        p1 = og.create_load_vertex(x=4.0, z=2.0, p=5000.0)
        p2 = og.create_load_vertex(x=16.0, z=2.0, p=5000.0)
        line = og.create_load(loadtype="line", name="part", point1=p1, point2=p2)
        lc = og.create_load_case(name="LC")
        lc.add_load(line)
        model.add_load_case(lc)
        model.analyze(load_case="LC")
        ops.reactions()
        ry_tot = 0.0
        sum_x = 0.0
        for node in ops.getNodeTags():
            ry = -float(ops.nodeReaction(node, 2))
            c = ops.nodeCoord(node)
            ry_tot += ry
            sum_x += ry * c[0]
        self.assertAlmostEqual(ry_tot, 60000.0, delta=1e-6 * 60000.0)
        self.assertAlmostEqual(sum_x / ry_tot, 10.0, delta=1e-5)

    def test_tc_b2_04_line_trapezoidal(self):
        """TC-B2-04: Trapezoidal intensity integration (w1 = 2000, w2 = 8000 N/m)."""
        model = create_standard_grillage(20.0, 8.0, nl=5, nt=11, name="trap")
        p1 = og.create_load_vertex(x=0.0, z=2.0, p=2000.0)
        p2 = og.create_load_vertex(x=20.0, z=2.0, p=8000.0)
        line = og.create_load(loadtype="line", name="trap", point1=p1, point2=p2)
        lc = og.create_load_case(name="LC")
        lc.add_load(line)
        model.add_load_case(lc)
        model.analyze(load_case="LC")
        ops.reactions()
        ry_tot = 0.0
        sum_x = 0.0
        for node in ops.getNodeTags():
            ry = -float(ops.nodeReaction(node, 2))
            c = ops.nodeCoord(node)
            ry_tot += ry
            sum_x += ry * c[0]
        self.assertAlmostEqual(ry_tot, 100000.0, delta=1e-6 * 100000.0)
        self.assertAlmostEqual(sum_x / ry_tot, 12.0, delta=1e-5)

    def test_tc_b2_05_line_skew_varying(self):
        """TC-B2-05: Skew line varying intensity force, 2D centroid, and reaction equilibrium."""
        L_skew = math.sqrt(20.0**2 + 4.0**2)
        P_exp = 8000.0 * L_skew
        model = create_standard_grillage(20.0, 8.0, nl=9, nt=11, edge_dist=1.0, name="skew")
        p1 = og.create_load_vertex(x=0.0, z=1.0, p=4000.0)
        p2 = og.create_load_vertex(x=20.0, z=5.0, p=12000.0)
        line = og.create_load(loadtype="line", name="skew", point1=p1, point2=p2)
        lc = og.create_load_case(name="LC")
        lc.add_load(line)
        model.add_load_case(lc)
        model.analyze(load_case="LC")
        ops.reactions()
        ry_tot = 0.0
        sum_x = 0.0
        sum_z = 0.0
        for node in ops.getNodeTags():
            ry = -float(ops.nodeReaction(node, 2))
            c = ops.nodeCoord(node)
            ry_tot += ry
            sum_x += ry * c[0]
            sum_z += ry * c[2]
        self.assertAlmostEqual(ry_tot, P_exp, delta=1e-6 * P_exp)
        self.assertAlmostEqual(sum_x / ry_tot, 11.666667, delta=1e-5)
        self.assertAlmostEqual(sum_z / ry_tot, 3.333333, delta=1e-5)

    def test_tc_b2_06_line_first_bay_offset(self):
        """TC-B2-06: First end-bay load point placed inside cell [0, 1.5] at x = 0.75 m."""
        model = create_standard_grillage(24.0, 8.5, nl=5, nt=17, name="fb")
        p1 = og.create_load_vertex(x=0.0, z=0.5, p=6540.0)
        p2 = og.create_load_vertex(x=24.0, z=0.5, p=6540.0)
        line = og.create_load(loadtype="line", name="line", point1=p1, point2=p2)
        assigned = []
        orig = model._assign_load_to_four_node
        def rec(point, mag, shape_func='linear'):
            assigned.append((point, mag))
            return orig(point, mag, shape_func)
        model._assign_load_to_four_node = rec
        lc = og.create_load_case(name="LC")
        lc.add_load(line)
        model.add_load_case(lc)
        self.assertAlmostEqual(float(assigned[0][0][0]), 0.75, places=3)
        self.assertAlmostEqual(assigned[0][1], 6540.0 * 1.5, places=3)

    def test_tc_b2_07_patch_corner_dedup(self):
        """TC-B2-07: Uniform patch eliminates corner duplication (A = 200 m2, P = 400 kN)."""
        model = create_standard_grillage(20.0, 10.0, nl=11, nt=21, name="cdedup")
        p1 = og.create_load_vertex(x=0.0, z=0.0, p=2000.0)
        p2 = og.create_load_vertex(x=20.0, z=0.0, p=2000.0)
        p3 = og.create_load_vertex(x=20.0, z=10.0, p=2000.0)
        p4 = og.create_load_vertex(x=0.0, z=10.0, p=2000.0)
        patch = og.create_load(loadtype="patch", name="patch", point1=p1, point2=p2, point3=p3, point4=p4)
        lc = og.create_load_case(name="LC")
        lc.add_load(patch)
        model.add_load_case(lc)
        model.analyze(load_case="LC")
        ops.reactions()
        ry_tot = sum(-float(ops.nodeReaction(node, 2)) for node in ops.getNodeTags())
        self.assertAlmostEqual(ry_tot, 400000.0, delta=1e-6 * 400000.0)

    def test_tc_b2_08_patch_interior_partial(self):
        """TC-B2-08: Partial interior patch equilibrium and centroid (A = 54 m2, P = 81 kN)."""
        model = create_standard_grillage(24.0, 10.0, nl=11, nt=25, name="part_patch")
        p1 = og.create_load_vertex(x=6.0, z=2.0, p=1500.0)
        p2 = og.create_load_vertex(x=18.0, z=2.0, p=1500.0)
        p3 = og.create_load_vertex(x=18.0, z=6.5, p=1500.0)
        p4 = og.create_load_vertex(x=6.0, z=6.5, p=1500.0)
        patch = og.create_load(loadtype="patch", name="patch", point1=p1, point2=p2, point3=p3, point4=p4)
        lc = og.create_load_case(name="LC")
        lc.add_load(patch)
        model.add_load_case(lc)
        model.analyze(load_case="LC")
        ops.reactions()
        ry_tot = 0.0
        sum_x = 0.0
        sum_z = 0.0
        for node in ops.getNodeTags():
            ry = -float(ops.nodeReaction(node, 2))
            c = ops.nodeCoord(node)
            ry_tot += ry
            sum_x += ry * c[0]
            sum_z += ry * c[2]
        self.assertAlmostEqual(ry_tot, 81000.0, delta=1e-6 * 81000.0)
        self.assertAlmostEqual(sum_x / ry_tot, 12.0, delta=1e-5)
        self.assertAlmostEqual(sum_z / ry_tot, 4.25, delta=1e-5)

    def test_tc_b2_09_negative_out_of_mesh(self):
        """TC-B2-09: Fail-closed out-of-mesh exception (raises ValueError)."""
        model = create_standard_grillage(20.0, 8.0, nl=5, nt=11, name="out_mesh")
        with self.assertRaises(ValueError):
            model._assign_load_to_four_node(point=[-1.0, 0.0, 2.0], mag=5000.0)
        with self.assertRaises(ValueError):
            model._assign_load_to_four_node(point=[25.0, 0.0, 2.0], mag=5000.0)

    def test_tc_b2_10_fe_barrier_equilibrium(self):
        """TC-B2-10: Full-bridge crash barrier static equilibrium (313.920 kN)."""
        bridge = PlateGirderBridge()
        bridge.set_input(dict(BASE_CFG))
        bridge._resolve_optimized_bounds_to_mm()
        bridge._convert_girder_dims_mm_to_m()
        bridge._validate_inputs()
        bridge._solve_bridge_layout()
        bridge._stage_grillage_setup()
        bridge.add_dead_loads()
        bgm = bridge.grillage_model

        bgm.model.analyze(load_case="Crash barrier load")
        ops.reactions()
        r_y_tot_N = sum(-float(ops.nodeReaction(node, 2)) for node in ops.getNodeTags())
        self.assertAlmostEqual(r_y_tot_N / 1000.0, 313.920, delta=1e-6 * 313.920)

    def test_tc_b2_11_fe_deck_slab_equil(self):
        """TC-B2-11: Full-bridge deck slab static equilibrium (1275.000 kN)."""
        bridge = PlateGirderBridge()
        bridge.set_input(dict(BASE_CFG))
        bridge._resolve_optimized_bounds_to_mm()
        bridge._convert_girder_dims_mm_to_m()
        bridge._validate_inputs()
        bridge._solve_bridge_layout()
        bridge._stage_grillage_setup()
        bridge.add_dead_loads()
        bgm = bridge.grillage_model

        bgm.model.analyze(load_case="DD")
        ops.reactions()
        r_y_tot_N = sum(-float(ops.nodeReaction(node, 2)) for node in ops.getNodeTags())
        self.assertAlmostEqual(r_y_tot_N / 1000.0, 1275.000, delta=1e-6 * 1275.000)

    def test_tc_b2_12_fe_overlay_equil(self):
        """TC-B2-12: Full-bridge wearing course static equilibrium (244.800 kN)."""
        bridge = PlateGirderBridge()
        bridge.set_input(dict(BASE_CFG))
        bridge._resolve_optimized_bounds_to_mm()
        bridge._convert_girder_dims_mm_to_m()
        bridge._validate_inputs()
        bridge._solve_bridge_layout()
        bridge._stage_grillage_setup()
        bridge.add_dead_loads()
        bgm = bridge.grillage_model

        bgm.model.analyze(load_case="1.0 DW")
        ops.reactions()
        r_y_tot_N = sum(-float(ops.nodeReaction(node, 2)) for node in ops.getNodeTags())
        self.assertAlmostEqual(r_y_tot_N / 1000.0, 244.800, delta=1e-6 * 244.800)

    def test_tc_b2_13_regression_batch1(self):
        """TC-B2-13: Invariance of Batch 1 defect remediations (DEF-12, DEF-08, DEF-11)."""
        # DEF-12
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            res_def12 = test_tc_reg_cap_stiffener(evidence_dir=td)
            self.assertEqual(res_def12.get("status"), "PASS")

        # DEF-08
        out_pass = {'design_results': {'per_girder': {'G1': {'checks': [{'name': 'Shear', 'dcr': 0.8}]}}}}
        s_pass = executive_summary({'bridge': {'type': 'plate_girder'}}, out_pass, {})
        self.assertIn("Girder design pass", s_pass)
        out_fail = {'design_results': {'per_girder': {'G1': {'checks': [{'name': 'Shear', 'dcr': 1.2}]}}}}
        s_fail = executive_summary({'bridge': {'type': 'plate_girder'}}, out_fail, {})
        self.assertIn("Girder design fail", s_fail)

        # DEF-11
        bridge = PlateGirderBridge()
        bridge.set_input(dict(BASE_CFG))
        bridge._resolve_optimized_bounds_to_mm()
        bridge._convert_girder_dims_mm_to_m()
        bridge._validate_inputs()
        bridge._solve_bridge_layout()
        bridge._stage_grillage_setup()
        bcfg = BridgeConfig.from_plate_girder_bridge(bridge, 0)
        self.assertEqual(bcfg.geometry.n_girders, 4)

    def test_tc_b2_14_line_all_bays(self):
        """TC-B2-14: Complete 16/16 bay force contribution for uniform longitudinal line load."""
        model = create_standard_grillage(24.0, 8.5, nl=5, nt=17, name="allbays")
        p1 = og.create_load_vertex(x=0.0, z=0.5, p=10000.0)
        p2 = og.create_load_vertex(x=24.0, z=0.5, p=10000.0)
        line = og.create_load(loadtype="line", name="line", point1=p1, point2=p2)
        assigned = []
        orig = model._assign_load_to_four_node
        def rec(point, mag, shape_func='linear'):
            assigned.append((point, mag))
            return orig(point, mag, shape_func)
        model._assign_load_to_four_node = rec
        lc = og.create_load_case(name="LC")
        lc.add_load(line)
        model.add_load_case(lc)
        self.assertEqual(len(assigned), 16)
        self.assertAlmostEqual(sum(p[1] for p in assigned), 240000.0, delta=1e-6 * 240000.0)

    def test_tc_b2_15_line_triangle(self):
        """TC-B2-15: Triangular load peak at p2 centroid at 2/3 L."""
        model = create_standard_grillage(15.0, 8.0, nl=5, nt=11, name="tri")
        p1 = og.create_load_vertex(x=0.0, z=2.0, p=0.0)
        p2 = og.create_load_vertex(x=15.0, z=2.0, p=12000.0)
        line = og.create_load(loadtype="line", name="line", point1=p1, point2=p2)
        lc = og.create_load_case(name="LC")
        lc.add_load(line)
        model.add_load_case(lc)
        model.analyze(load_case="LC")
        ops.reactions()
        ry_tot = 0.0
        sum_x = 0.0
        for node in ops.getNodeTags():
            ry = -float(ops.nodeReaction(node, 2))
            c = ops.nodeCoord(node)
            ry_tot += ry
            sum_x += ry * c[0]
        self.assertAlmostEqual(ry_tot, 90000.0, delta=1e-6 * 90000.0)
        self.assertAlmostEqual(sum_x / ry_tot, 10.0, delta=1e-5)

    def test_tc_b2_16_patch_nonaligned(self):
        """TC-B2-16: Non-grid-aligned patch load area and force conservation (239.4 kN)."""
        model = create_standard_grillage(20.0, 10.0, nl=11, nt=21, name="nonaligned")
        p1 = og.create_load_vertex(x=3.7, z=1.2, p=2500.0)
        p2 = og.create_load_vertex(x=16.3, z=1.2, p=2500.0)
        p3 = og.create_load_vertex(x=16.3, z=8.8, p=2500.0)
        p4 = og.create_load_vertex(x=3.7, z=8.8, p=2500.0)
        patch = og.create_load(loadtype="patch", name="patch", point1=p1, point2=p2, point3=p3, point4=p4)
        lc = og.create_load_case(name="LC")
        lc.add_load(patch)
        model.add_load_case(lc)
        model.analyze(load_case="LC")
        ops.reactions()
        ry_tot = sum(-float(ops.nodeReaction(node, 2)) for node in ops.getNodeTags())
        self.assertAlmostEqual(ry_tot, 239400.0, delta=1e-6 * 239400.0)

    def test_tc_b2_17_zero_crossing_failsafe(self):
        """TC-B2-17: Zero-crossing partitioning, force neutrality, and moment conservation."""
        model = create_standard_grillage(20.0, 8.0, nl=5, nt=11, name="zc")
        p1 = og.create_load_vertex(x=5.0, z=2.0, p=5000.0)
        p2 = og.create_load_vertex(x=15.0, z=2.0, p=-5000.0)
        line = og.create_load(loadtype="line", name="line", point1=p1, point2=p2)
        lc = og.create_load_case(name="LC")
        lc.add_load(line)
        model.add_load_case(lc)
        model.analyze(load_case="LC")
        ops.reactions()
        ry_tot = 0.0
        moment_about_p1 = 0.0
        for node in ops.getNodeTags():
            ry = -float(ops.nodeReaction(node, 2))
            c = ops.nodeCoord(node)
            ry_tot += ry
            moment_about_p1 += ry * (c[0] - 5.0)
        self.assertAlmostEqual(ry_tot, 0.0, delta=1e-5)
        self.assertAlmostEqual(moment_about_p1, -83333.333333, delta=1e-4)


if __name__ == "__main__":
    unittest.main()
