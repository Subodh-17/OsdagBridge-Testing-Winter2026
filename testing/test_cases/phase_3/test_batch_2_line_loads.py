"""
Phase 3 Batch 2 Verification: Line Load Statics & Centroid Conservation (Commit 1 / DEF-18-LINE)
Tests:
- TC-B2-01-LINE-SCALE-UNIFORM: Invariance of force across mesh densities
- TC-B2-02-LINE-SMALL-MAG: Micro-load magnitude scaling and first-bay inclusion
- TC-B2-03-LINE-ASYMMETRIC-PARTIAL: Partial span line load force and centroid
- TC-B2-04-LINE-TRAPEZOIDAL: Non-uniform trapezoidal load integration
- TC-B2-05-LINE-SKEW-VARYING: Skew line load force, 2D centroid, and magnitude scaling
- TC-B2-06-LINE-FIRST-BAY-OFFSET: First bay coordinate placement inside cell
- TC-B2-09-NEGATIVE-OUT-OF-MESH: Fail-closed ValueError on out-of-mesh load
- TC-B2-10-FE-BARRIER-EQUILIBRIUM: Full bridge crash barrier static equilibrium
- TC-B2-14-LINE-ALL-BAYS: Complete 16/16 bay force contribution
- TC-B2-15-LINE-TRIANGLE: Triangular load centroid mechanics
- TC-B2-17-ZERO-CROSSING-FAILSAFE: Zero-crossing partitioning and moment conservation
"""

import math
import sys
import os
import unittest
import numpy as np

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Ensure source paths are imported
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
SRC_DIR = os.path.join(REPO_ROOT, "source", "OsdagBridge", "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import ospgrillage as og
import openseespy.opensees as ops


def create_standard_grillage(L, W, nl, nt, edge_dist=0.5, name="std_grillage"):
    """Helper to create a standard solved grillage model."""
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


class TestBatch2LineLoads(unittest.TestCase):

    def test_tc_b2_01_line_scale_uniform(self):
        """TC-B2-01: Force conservation invariant across mesh densities (dx = 1.0, 2.0 m)."""
        L = 20.0
        W = 8.0
        w = 10000.0  # N/m
        P_exp = w * L  # 200,000 N

        for nt in [21, 11]:  # dx = 1.0 m, dx = 2.0 m
            model = create_standard_grillage(L, W, nl=5, nt=nt, name=f"mesh_nt_{nt}")
            p1 = og.create_load_vertex(x=0.0, z=2.0, p=w)
            p2 = og.create_load_vertex(x=L, z=2.0, p=w)
            line = og.create_load(loadtype="line", name="line", point1=p1, point2=p2)
            lc = og.create_load_case(name=f"LC_{nt}")
            lc.add_load(line)
            model.add_load_case(lc)

            model.analyze(load_case=f"LC_{nt}")
            ops.reactions()
            ry_tot = sum(-float(ops.nodeReaction(node, 2)) for node in ops.getNodeTags())
            dx = L / (nt - 1)
            rel_err = abs(ry_tot - P_exp) / P_exp
            self.assertLessEqual(rel_err, 1e-9, f"Force non-conservation on mesh dx={dx:.1f}m: {ry_tot} vs {P_exp}")

    def test_tc_b2_02_line_small_mag(self):
        """TC-B2-02: Micro-load magnitude scaling and first-bay inclusion (w = 1.0 N/m)."""
        L = 24.0
        W = 8.5
        w = 1.0  # 1 N/m
        P_exp = w * L  # 24.0 N
        x_exp = L / 2.0  # 12.0 m

        model = create_standard_grillage(L, W, nl=5, nt=17, name="micro_load")  # 16 bays of 1.5m
        p1 = og.create_load_vertex(x=0.0, z=2.0, p=w)
        p2 = og.create_load_vertex(x=L, z=2.0, p=w)
        line = og.create_load(loadtype="line", name="micro_line", point1=p1, point2=p2)
        lc = og.create_load_case(name="LC_MICRO")
        lc.add_load(line)
        model.add_load_case(lc)

        model.analyze(load_case="LC_MICRO")
        ops.reactions()
        ry_tot = 0.0
        sum_x = 0.0
        for node in ops.getNodeTags():
            ry = -float(ops.nodeReaction(node, 2))
            c = ops.nodeCoord(node)
            ry_tot += ry
            sum_x += ry * c[0]

        x_bar = sum_x / ry_tot
        self.assertAlmostEqual(ry_tot, P_exp, delta=1e-6 * P_exp)
        self.assertAlmostEqual(x_bar, x_exp, delta=1e-5)

    def test_tc_b2_03_line_asymmetric_partial(self):
        """TC-B2-03: Partial line load equilibrium and centroid (x in [4, 16] m)."""
        L = 24.0
        W = 8.5
        x1, x2 = 4.0, 16.0
        w = 5000.0  # N/m
        L_w = x2 - x1  # 12 m
        P_exp = w * L_w  # 60,000 N
        x_exp = (x1 + x2) / 2.0  # 10.0 m

        model = create_standard_grillage(L, W, nl=5, nt=17, name="partial_line")
        p1 = og.create_load_vertex(x=x1, z=2.0, p=w)
        p2 = og.create_load_vertex(x=x2, z=2.0, p=w)
        line = og.create_load(loadtype="line", name="partial", point1=p1, point2=p2)
        lc = og.create_load_case(name="LC_PARTIAL")
        lc.add_load(line)
        model.add_load_case(lc)

        model.analyze(load_case="LC_PARTIAL")
        ops.reactions()
        ry_tot = 0.0
        sum_x = 0.0
        for node in ops.getNodeTags():
            ry = -float(ops.nodeReaction(node, 2))
            c = ops.nodeCoord(node)
            ry_tot += ry
            sum_x += ry * c[0]

        x_bar = sum_x / ry_tot
        self.assertAlmostEqual(ry_tot, P_exp, delta=1e-6 * P_exp)
        self.assertAlmostEqual(x_bar, x_exp, delta=1e-5)

    def test_tc_b2_04_line_trapezoidal(self):
        """TC-B2-04: Trapezoidal non-uniform intensity integration."""
        L = 20.0
        W = 8.0
        w1, w2 = 2000.0, 8000.0
        P_exp = ((w1 + w2) / 2.0) * L  # 100,000 N
        t = (w1 + 2 * w2) / (3 * (w1 + w2))
        x_exp = 0.0 + t * L  # 12.0 m

        model = create_standard_grillage(L, W, nl=5, nt=11, name="trapezoidal")
        p1 = og.create_load_vertex(x=0.0, z=2.0, p=w1)
        p2 = og.create_load_vertex(x=L, z=2.0, p=w2)
        line = og.create_load(loadtype="line", name="trap", point1=p1, point2=p2)
        lc = og.create_load_case(name="LC_TRAP")
        lc.add_load(line)
        model.add_load_case(lc)

        model.analyze(load_case="LC_TRAP")
        ops.reactions()
        ry_tot = 0.0
        sum_x = 0.0
        for node in ops.getNodeTags():
            ry = -float(ops.nodeReaction(node, 2))
            c = ops.nodeCoord(node)
            ry_tot += ry
            sum_x += ry * c[0]

        x_bar = sum_x / ry_tot
        self.assertAlmostEqual(ry_tot, P_exp, delta=1e-6 * P_exp)
        self.assertAlmostEqual(x_bar, x_exp, delta=1e-5)

    def test_tc_b2_05_line_skew_varying(self):
        """TC-B2-05: Skew line varying intensity force, 2D centroid, and reaction equilibrium."""
        L = 20.0
        W = 8.0
        p1_coord = (0.0, 0.0, 1.0)
        p2_coord = (20.0, 0.0, 5.0)
        w1, w2 = 4000.0, 12000.0
        L_skew = math.sqrt((p2_coord[0] - p1_coord[0])**2 + (p2_coord[2] - p1_coord[2])**2)
        P_exp = ((w1 + w2) / 2.0) * L_skew  # 163,168.624435 N
        t = (w1 + 2 * w2) / (3 * (w1 + w2))  # 7/12
        x_exp = p1_coord[0] + t * (p2_coord[0] - p1_coord[0])  # 11.666667 m
        z_exp = p1_coord[2] + t * (p2_coord[2] - p1_coord[2])  # 3.333333 m

        model = create_standard_grillage(L, W, nl=9, nt=11, edge_dist=1.0, name="skew_line")
        p1 = og.create_load_vertex(x=p1_coord[0], z=p1_coord[2], p=w1)
        p2 = og.create_load_vertex(x=p2_coord[0], z=p2_coord[2], p=w2)
        line = og.create_load(loadtype="line", name="skew", point1=p1, point2=p2)
        lc = og.create_load_case(name="LC_SKEW")
        lc.add_load(line)
        model.add_load_case(lc)

        model.analyze(load_case="LC_SKEW")
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

        x_bar = sum_x / ry_tot
        z_bar = sum_z / ry_tot
        self.assertAlmostEqual(ry_tot, P_exp, delta=1e-6 * P_exp)
        self.assertAlmostEqual(x_bar, x_exp, delta=1e-5)
        self.assertAlmostEqual(z_bar, z_exp, delta=1e-5)

    def test_tc_b2_06_line_first_bay_offset(self):
        """TC-B2-06: First end-bay load point placed inside cell [0, 1.5] at x = 0.75 m."""
        L = 24.0
        W = 8.5
        model = create_standard_grillage(L, W, nl=5, nt=17, name="first_bay")
        p1 = og.create_load_vertex(x=0.0, z=0.5, p=6540.0)
        p2 = og.create_load_vertex(x=24.0, z=0.5, p=6540.0)
        line = og.create_load(loadtype="line", name="bays", point1=p1, point2=p2)

        assigned_points = []
        orig_assign = model._assign_load_to_four_node
        def recording_assign(point, mag, shape_func='linear'):
            assigned_points.append((point, mag))
            return orig_assign(point, mag, shape_func)
        model._assign_load_to_four_node = recording_assign

        lc = og.create_load_case(name="LC_FB")
        lc.add_load(line)
        model.add_load_case(lc)

        self.assertGreater(len(assigned_points), 0)
        first_pt, first_mag = assigned_points[0]
        self.assertAlmostEqual(float(first_pt[0]), 0.75, places=3)
        self.assertAlmostEqual(float(first_pt[2]), 0.50, places=3)
        self.assertAlmostEqual(first_mag, 6540.0 * 1.5, places=3)

    def test_tc_b2_09_negative_out_of_mesh(self):
        """TC-B2-09: Fail-closed out-of-mesh exception (raises ValueError)."""
        model = create_standard_grillage(20.0, 8.0, nl=5, nt=11, name="out_of_mesh")
        with self.assertRaises(ValueError):
            model._assign_load_to_four_node(point=[-1.0, 0.0, 2.0], mag=5000.0)
        with self.assertRaises(ValueError):
            model._assign_load_to_four_node(point=[25.0, 0.0, 2.0], mag=5000.0)

    def test_tc_b2_10_fe_barrier_equilibrium(self):
        """TC-B2-10: Full-bridge crash barrier static equilibrium (313.920 kN)."""
        from testing.test_cases.baseline_regression.run_all_baseline_tests import BASE_CFG
        from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge

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
        r_y_tot_N = 0.0
        sum_rx = 0.0
        sum_rz = 0.0
        for node in ops.getNodeTags():
            ry = -float(ops.nodeReaction(node, 2))
            coords = ops.nodeCoord(node)
            r_y_tot_N += ry
            sum_rx += ry * coords[0]
            sum_rz += ry * coords[2]

        r_y_kN = r_y_tot_N / 1000.0
        x_bar = sum_rx / r_y_tot_N
        z_bar = sum_rz / r_y_tot_N

        P_exp = 313.920  # kN
        x_exp = 12.000   # m
        z_exp = 4.250    # m

        self.assertAlmostEqual(r_y_kN, P_exp, delta=1e-6 * P_exp)
        self.assertAlmostEqual(x_bar, x_exp, delta=1e-5)
        self.assertAlmostEqual(z_bar, z_exp, delta=1e-5)

    def test_tc_b2_14_line_all_bays(self):
        """TC-B2-14: Complete 16/16 bay force contribution for uniform longitudinal line load."""
        L = 24.0
        W = 8.5
        model = create_standard_grillage(L, W, nl=5, nt=17, name="all_bays")
        p1 = og.create_load_vertex(x=0.0, z=0.5, p=10000.0)
        p2 = og.create_load_vertex(x=24.0, z=0.5, p=10000.0)
        line = og.create_load(loadtype="line", name="bays16", point1=p1, point2=p2)

        assigned_points = []
        orig_assign = model._assign_load_to_four_node
        def recording_assign(point, mag, shape_func='linear'):
            assigned_points.append((point, mag))
            return orig_assign(point, mag, shape_func)
        model._assign_load_to_four_node = recording_assign

        lc = og.create_load_case(name="LC_16")
        lc.add_load(line)
        model.add_load_case(lc)

        self.assertEqual(len(assigned_points), 16, f"Expected 16 bays, got {len(assigned_points)}")
        tot_force = sum(p[1] for p in assigned_points)
        self.assertAlmostEqual(tot_force, 240000.0, delta=1e-6 * 240000.0)

    def test_tc_b2_15_line_triangle(self):
        """TC-B2-15: Triangular load peak at p2 centroid at 2/3 L."""
        L = 15.0
        W = 8.0
        w1, w2 = 0.0, 12000.0
        P_exp = ((w1 + w2) / 2.0) * L  # 90,000 N
        x_exp = (2.0 / 3.0) * L  # 10.0 m

        model = create_standard_grillage(L, W, nl=5, nt=11, name="triangle")
        p1 = og.create_load_vertex(x=0.0, z=2.0, p=w1)
        p2 = og.create_load_vertex(x=L, z=2.0, p=w2)
        line = og.create_load(loadtype="line", name="tri", point1=p1, point2=p2)
        lc = og.create_load_case(name="LC_TRI")
        lc.add_load(line)
        model.add_load_case(lc)

        model.analyze(load_case="LC_TRI")
        ops.reactions()
        ry_tot = 0.0
        sum_x = 0.0
        for node in ops.getNodeTags():
            ry = -float(ops.nodeReaction(node, 2))
            c = ops.nodeCoord(node)
            ry_tot += ry
            sum_x += ry * c[0]

        x_bar = sum_x / ry_tot
        self.assertAlmostEqual(ry_tot, P_exp, delta=1e-6 * P_exp)
        self.assertAlmostEqual(x_bar, x_exp, delta=1e-5)

    def test_tc_b2_17_zero_crossing_failsafe(self):
        """TC-B2-17: Zero-crossing partitioning, force neutrality, and moment conservation."""
        L = 20.0
        W = 8.0
        # Line from x=5 to x=15 (L_seg = 10m) with w1=+5000, w2=-5000 N/m
        model = create_standard_grillage(L, W, nl=5, nt=11, name="zero_crossing")
        p1 = og.create_load_vertex(x=5.0, z=2.0, p=5000.0)
        p2 = og.create_load_vertex(x=15.0, z=2.0, p=-5000.0)
        line = og.create_load(loadtype="line", name="zc", point1=p1, point2=p2)
        lc = og.create_load_case(name="LC_ZC")
        lc.add_load(line)
        model.add_load_case(lc)

        model.analyze(load_case="LC_ZC")
        ops.reactions()
        ry_tot = 0.0
        moment_about_p1 = 0.0
        for node in ops.getNodeTags():
            ry = -float(ops.nodeReaction(node, 2))
            c = ops.nodeCoord(node)
            ry_tot += ry
            moment_about_p1 += ry * (c[0] - 5.0)

        M_exp = -83333.333333  # N*m
        self.assertAlmostEqual(ry_tot, 0.0, delta=1e-5)
        self.assertAlmostEqual(moment_about_p1, M_exp, delta=1e-4)


if __name__ == "__main__":
    unittest.main()
