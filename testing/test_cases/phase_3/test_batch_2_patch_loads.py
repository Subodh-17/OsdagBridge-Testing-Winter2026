"""
Phase 3 Batch 2 Verification: Patch Load Statics & Deduplication Conservation (Commit 2 / DEF-18-PATCH)
Tests:
- TC-B2-07-PATCH-CORNER-DEDUP: Patch area and force conservation without corner duplication
- TC-B2-08-PATCH-INTERIOR-PARTIAL: Interior partial patch boundedness and centroid
- TC-B2-11-FE-DECK-SLAB-EQUIL: Full bridge deck slab static equilibrium (1275.000 kN)
- TC-B2-12-FE-OVERLAY-EQUIL: Full bridge wearing course static equilibrium (244.800 kN)
- TC-B2-16-PATCH-NONALIGNED: Arbitrary boundary non-grid-aligned patch conservation
"""

import math
import sys
import os
import unittest

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


def create_standard_grillage(L, W, nl, nt, edge_dist=0.5, name="std_patch_grillage"):
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


class TestBatch2PatchLoads(unittest.TestCase):

    def test_tc_b2_07_patch_corner_dedup(self):
        """TC-B2-07: Uniform patch on rectangular deck eliminates corner duplication (A = 200 m2, P = 400 kN)."""
        L = 20.0
        W = 10.0
        p_val = 2000.0  # N/m2
        A_exp = L * W  # 200 m2
        P_exp = A_exp * p_val  # 400,000 N

        model = create_standard_grillage(L, W, nl=11, nt=21, name="corner_dedup")
        p1 = og.create_load_vertex(x=0.0, z=0.0, p=p_val)
        p2 = og.create_load_vertex(x=L, z=0.0, p=p_val)
        p3 = og.create_load_vertex(x=L, z=W, p=p_val)
        p4 = og.create_load_vertex(x=0.0, z=W, p=p_val)
        patch = og.create_load(loadtype="patch", name="full_deck", point1=p1, point2=p2, point3=p3, point4=p4)
        lc = og.create_load_case(name="LC_DEDUP")
        lc.add_load(patch)
        model.add_load_case(lc)

        model.analyze(load_case="LC_DEDUP")
        ops.reactions()
        ry_tot = sum(-float(ops.nodeReaction(node, 2)) for node in ops.getNodeTags())

        self.assertAlmostEqual(ry_tot, P_exp, delta=1e-6 * P_exp)

    def test_tc_b2_08_patch_interior_partial(self):
        """TC-B2-08: Partial interior patch bounded equilibrium and centroid (x in [6, 18], z in [2, 6.5])."""
        L = 24.0
        W = 10.0
        x1, x2 = 6.0, 18.0
        z1, z2 = 2.0, 6.5
        p_val = 1500.0  # N/m2
        A_exp = (x2 - x1) * (z2 - z1)  # 12 * 4.5 = 54.0 m2
        P_exp = A_exp * p_val  # 81,000 N
        x_exp = (x1 + x2) / 2.0  # 12.0 m
        z_exp = (z1 + z2) / 2.0  # 4.25 m

        model = create_standard_grillage(L, W, nl=11, nt=25, name="interior_partial")
        p1 = og.create_load_vertex(x=x1, z=z1, p=p_val)
        p2 = og.create_load_vertex(x=x2, z=z1, p=p_val)
        p3 = og.create_load_vertex(x=x2, z=z2, p=p_val)
        p4 = og.create_load_vertex(x=x1, z=z2, p=p_val)
        patch = og.create_load(loadtype="patch", name="part_patch", point1=p1, point2=p2, point3=p3, point4=p4)
        lc = og.create_load_case(name="LC_PART_PATCH")
        lc.add_load(patch)
        model.add_load_case(lc)

        model.analyze(load_case="LC_PART_PATCH")
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

    def test_tc_b2_11_fe_deck_slab_equil(self):
        """TC-B2-11: Full-bridge deck slab static equilibrium (P = 1275.000 kN, x_bar = 12 m, z_bar = 4.25 m)."""
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

        bgm.model.analyze(load_case="DD")
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

        P_exp = 1275.000  # kN (24 * 8.5 * 0.25 * 25.0)
        x_exp = 12.000    # m
        z_exp = 4.250     # m

        self.assertAlmostEqual(r_y_kN, P_exp, delta=1e-6 * P_exp)
        self.assertAlmostEqual(x_bar, x_exp, delta=1e-5)
        self.assertAlmostEqual(z_bar, z_exp, delta=1e-5)

    def test_tc_b2_12_fe_overlay_equil(self):
        """TC-B2-12: Full-bridge wearing course static equilibrium (P = 244.800 kN, x_bar = 12 m, z_bar = 4.25 m)."""
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

        bgm.model.analyze(load_case="1.0 DW")
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

        P_exp = 244.800  # kN (24 * 8.5 * 0.05 * 24.0)
        x_exp = 12.000   # m
        z_exp = 4.250    # m

        self.assertAlmostEqual(r_y_kN, P_exp, delta=1e-6 * P_exp)
        self.assertAlmostEqual(x_bar, x_exp, delta=1e-5)
        self.assertAlmostEqual(z_bar, z_exp, delta=1e-5)

    def test_tc_b2_16_patch_nonaligned(self):
        """TC-B2-16: Non-grid-aligned patch load area and force conservation (A = 95.76 m2, P = 239.4 kN)."""
        L = 20.0
        W = 10.0
        x1, x2 = 3.7, 16.3
        z1, z2 = 1.2, 8.8
        p_val = 2500.0  # N/m2
        A_exp = (x2 - x1) * (z2 - z1)  # 12.6 * 7.6 = 95.76 m2
        P_exp = A_exp * p_val  # 239,400.0 N

        model = create_standard_grillage(L, W, nl=11, nt=21, name="nonaligned")
        p1 = og.create_load_vertex(x=x1, z=z1, p=p_val)
        p2 = og.create_load_vertex(x=x2, z=z1, p=p_val)
        p3 = og.create_load_vertex(x=x2, z=z2, p=p_val)
        p4 = og.create_load_vertex(x=x1, z=z2, p=p_val)
        patch = og.create_load(loadtype="patch", name="nonaligned_patch", point1=p1, point2=p2, point3=p3, point4=p4)
        lc = og.create_load_case(name="LC_NONALIGNED")
        lc.add_load(patch)
        model.add_load_case(lc)

        model.analyze(load_case="LC_NONALIGNED")
        ops.reactions()
        ry_tot = sum(-float(ops.nodeReaction(node, 2)) for node in ops.getNodeTags())

        self.assertAlmostEqual(ry_tot, P_exp, delta=1e-6 * P_exp)


if __name__ == "__main__":
    unittest.main()
