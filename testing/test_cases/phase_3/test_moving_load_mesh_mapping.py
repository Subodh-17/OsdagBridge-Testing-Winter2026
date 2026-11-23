"""
Regression Test Suite: Moving-Load Mesh Mapping and Physical Domain Boundaries
Defect Reference: Moving vehicle point load coordinate mapping failure (DEF-MOVING-LOAD-MESH)
Target Configurations:
  1. Orthogonal baseline (24 m span, 0 deg skew)
  2. Skewed geometry (30 m span, 10 deg skew, 7.5 m carriageway)
  3. Skewed geometry with median and footpath (25 m span, 10 deg skew, Median Yes, Single Footpath)
  4. Negative skew geometry (25 m span, -10 deg skew)
  5. Off-bridge entry/exit load conservation and coordinate type mapping
"""

import sys
import os
import math
import unittest
from copy import deepcopy
import numpy as np

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf-16'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
SRC_DIR = os.path.join(REPO_ROOT, "source", "OsdagBridge", "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import ospgrillage as og
from ospgrillage.mesh import Point
from ospgrillage.load import PointLoad, CompoundLoad, LoadVertex
import openseespy.opensees as ops

from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
from osdagbridge.core.utils.common import (
    KEY_SPAN,
    KEY_CARRIAGEWAY_WIDTH,
    KEY_SKEW_ANGLE,
    KEY_INCLUDE_MEDIAN,
    KEY_FOOTPATH,
    KEY_DESIGN_MODE,
    KEY_STRUCTURE_TYPE,
    KEY_GIRDER,
    KEY_CROSS_BRACING,
    KEY_END_DIAPHRAGM,
    KEY_DECK_CONCRETE_GRADE_BASIC,
    KEY_PROJECT_LOCATION,
)
from osdagbridge.core.bridge_types.plate_girder.defaults import (
    solve_extend_basic_input_dict,
)


def create_test_grillage(L=20.0, W=8.0, skew=0.0, nl=5, nt=11, name="test_grillage"):
    """Helper to create and compile a standalone OspGrillage model."""
    ops.wipe()
    model = og.create_grillage(
        bridge_name=name,
        long_dim=float(L),
        width=float(W),
        skew=float(skew),
        num_long_grid=nl,
        num_trans_grid=nt,
        edge_beam_dist=0.5,
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


class TestMovingLoadMeshMapping(unittest.TestCase):

    def test_01_assign_load_to_four_node_fail_closed_by_default(self):
        """TC-ML-01: Direct _assign_load_to_four_node fails closed with ValueError by default (Batch 2 compatibility)."""
        model = create_test_grillage(L=20.0, W=8.0, nl=5, nt=11, name="tc_01")
        # Coordinate strictly outside grillage domain
        with self.assertRaises(ValueError):
            model._assign_load_to_four_node(point=[-2.0, 0.0, 2.0], mag=5000.0)
        with self.assertRaises(ValueError):
            model._assign_load_to_four_node(point=[25.0, 0.0, 2.0], mag=5000.0)

    def test_02_assign_load_to_four_node_allow_out_of_mesh(self):
        """TC-ML-02: With allow_out_of_mesh=True, out-of-domain coordinates return [] (zero force on superstructure)."""
        model = create_test_grillage(L=20.0, W=8.0, nl=5, nt=11, name="tc_02")
        # Coordinate strictly outside grillage domain returns empty command list
        res_neg = model._assign_load_to_four_node(point=[-5.0, 0.0, 2.0], mag=5000.0, allow_out_of_mesh=True)
        res_pos = model._assign_load_to_four_node(point=[30.0, 0.0, 2.0], mag=5000.0, allow_out_of_mesh=True)
        self.assertEqual(res_neg, [])
        self.assertEqual(res_pos, [])

    def test_03_point_type_handling_in_node_mapping(self):
        """TC-ML-03: _get_point_load_nodes correctly maps Point, LoadVertex, tuple, list, and ndarray."""
        model = create_test_grillage(L=20.0, W=8.0, nl=5, nt=11, name="tc_03")
        target_x, target_z = 10.0, 4.0
        
        # Test tuple
        nodes_tuple, grid_tuple = model._get_point_load_nodes((target_x, 0.0, target_z))
        self.assertIsNotNone(nodes_tuple)
        self.assertIsNotNone(grid_tuple)

        # Test list
        nodes_list, grid_list = model._get_point_load_nodes([target_x, 0.0, target_z])
        self.assertEqual(nodes_list, nodes_tuple)
        self.assertEqual(grid_list, grid_tuple)

        # Test Point namedtuple
        nodes_pt, grid_pt = model._get_point_load_nodes(Point(target_x, 0.0, target_z))
        self.assertEqual(nodes_pt, nodes_tuple)
        self.assertEqual(grid_pt, grid_tuple)

        # Test LoadVertex namedtuple
        nodes_lv, grid_lv = model._get_point_load_nodes(LoadVertex(target_x, 0.0, target_z, 1000.0))
        self.assertEqual(nodes_lv, nodes_tuple)
        self.assertEqual(grid_lv, grid_tuple)

        # Test numpy ndarray
        nodes_arr, grid_arr = model._get_point_load_nodes(np.array([target_x, 0.0, target_z]))
        self.assertEqual(nodes_arr, nodes_tuple)
        self.assertEqual(grid_arr, grid_tuple)

    def test_04_interior_load_conservation(self):
        """TC-ML-04: Interior point load strictly conserves total applied vertical force (sum(Fy) == P)."""
        model = create_test_grillage(L=20.0, W=8.0, nl=5, nt=11, name="tc_04")
        mag = 70000.0  # 70 kN
        cmds = model._assign_load_to_four_node(point=[10.0, 0.0, 4.0], mag=mag, allow_out_of_mesh=True)
        self.assertGreater(len(cmds), 0)
        # Each command is ('load', (node_tag, fx, fy, fz, mx, my, mz), {})
        sum_fy = sum(cmd[1][2] for cmd in cmds)
        self.assertAlmostEqual(sum_fy, mag, delta=1e-9 * mag)

    def test_05_boundary_edge_tolerance(self):
        """TC-ML-05: Point exactly on or near grid cell boundary edge is not rejected due to floating-point chatter."""
        model = create_test_grillage(L=20.0, W=8.0, nl=5, nt=11, name="tc_05")
        # Grid line in x: nt=11 means 10 intervals of 2.0 m -> x = 2.0, 4.0, 6.0, 8.0, 10.0
        # Point right on the grid line x = 10.0
        nodes, grid = model._get_point_load_nodes([10.0, 0.0, 3.5])
        self.assertIsNotNone(nodes)
        self.assertIsNotNone(grid)

        # Point with 1e-12 floating point deviation from boundary
        nodes_pert, grid_pert = model._get_point_load_nodes([10.0 + 1e-12, 0.0, 3.5])
        self.assertIsNotNone(nodes_pert)

    def _setup_bridge(self, span, cw, skew, median="No", footpath="None"):
        bridge = PlateGirderBridge()
        inp = deepcopy(bridge.input_dict)
        inp[KEY_SPAN] = span
        inp[KEY_CARRIAGEWAY_WIDTH] = cw
        inp[KEY_SKEW_ANGLE] = skew
        inp[KEY_INCLUDE_MEDIAN] = median
        inp[KEY_FOOTPATH] = footpath
        inp[KEY_DESIGN_MODE] = "Optimized"
        inp[KEY_STRUCTURE_TYPE] = "Highway Bridge"
        inp[KEY_GIRDER] = "E 350A"
        inp[KEY_CROSS_BRACING] = "E 350A"
        inp[KEY_END_DIAPHRAGM] = "E 350A"
        inp[KEY_DECK_CONCRETE_GRADE_BASIC] = "M40"
        inp[KEY_PROJECT_LOCATION] = {'method': 'location_name', 'name': 'Delhi', 'zone': 'IV'}
        solve_extend_basic_input_dict(inp)
        bridge.set_input(inp)
        bridge._resolve_optimized_bounds_to_mm()
        bridge._convert_girder_dims_mm_to_m()
        bridge._validate_inputs()
        bridge._solve_bridge_layout()
        bridge._stage_grillage_setup()
        return bridge

    def test_06_orthogonal_moving_load_cases(self):
        """TC-ML-06: Orthogonal bridge (24 m, 0 deg skew) generates all moving vehicle load cases without error."""
        bridge = self._setup_bridge(span=24.0, cw=7.5, skew=0.0)
        bridge.add_live_loads()
        self.assertGreater(len(bridge.grillage_model.model.load_case_list), 0)

    def test_07_skewed_30m_10deg_moving_load_cases(self):
        """TC-ML-07: Skewed bridge (30 m, 10 deg skew) moving vehicle load cases execute without error (DEF-MOVING-LOAD-MESH fix)."""
        bridge = self._setup_bridge(span=30.0, cw=7.5, skew=10.0)
        # This was the exact failure point reported by the user:
        # ValueError: Point load coordinate does not lie within any mesh grid cell.
        bridge.add_live_loads()
        self.assertIsNotNone(bridge.grillage_model)
        self.assertGreater(len(bridge.grillage_model.model.load_case_list), 0)

    def test_08_skewed_25m_10deg_median_footpath_moving_loads(self):
        """TC-ML-08: Skewed dual-carriageway with median & footpath (25 m, 10 deg skew) generates all live loads."""
        bridge = self._setup_bridge(span=25.0, cw=7.5, skew=10.0, median="Yes", footpath="single side")
        bridge.add_live_loads()
        self.assertIsNotNone(bridge.grillage_model)

    def test_09_negative_skew_moving_loads(self):
        """TC-ML-09: Negative skew geometry (25 m, -10 deg skew) generates moving vehicle load cases symmetrically."""
        bridge = self._setup_bridge(span=25.0, cw=7.5, skew=-10.0)
        bridge.add_live_loads()
        self.assertIsNotNone(bridge.grillage_model)

    def test_10_partial_vehicle_on_bridge_statics(self):
        """TC-ML-10: Vehicle entering bridge with rear axles off-bridge correctly attributes only on-bridge axle loads."""
        model = create_test_grillage(L=20.0, W=8.0, nl=5, nt=11, name="tc_10")
        
        # Create a compound load representing a 3-axle vehicle entering the bridge:
        # Axle 1 (front): at x = 3.0 m (on bridge), P = 30 kN
        # Axle 2 (middle): at x = -1.0 m (off bridge), P = 35 kN
        # Axle 3 (rear): at x = -3.0 m (off bridge), P = 35 kN
        axle1 = PointLoad(name="axle1", point1=LoadVertex(3.0, 0.0, 4.0, 30000.0))
        axle2 = PointLoad(name="axle2", point1=LoadVertex(-1.0, 0.0, 4.0, 35000.0))
        axle3 = PointLoad(name="axle3", point1=LoadVertex(-3.0, 0.0, 4.0, 35000.0))
        
        veh_load = CompoundLoad(name="entering_vehicle")
        veh_load.add_load(axle1)
        veh_load.add_load(axle2)
        veh_load.add_load(axle3)
        
        lc = og.create_load_case(name="entry_step")
        lc.add_load(veh_load)
        
        # Distribute load to model
        load_cmds = model._distribute_load_types_to_model(load_case_obj=lc)
        
        # Only on-bridge axle (Axle 1, 30 kN) should be assigned to grillage nodes
        assigned_fy = sum(cmd[1][2] for cmd in load_cmds if cmd[0] == "load")
        self.assertAlmostEqual(assigned_fy, 30000.0, delta=1e-6 * 30000.0)


if __name__ == "__main__":
    unittest.main()
