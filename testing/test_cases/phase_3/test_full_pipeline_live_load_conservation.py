"""
Integration test: vehicle live-load conservation through the real OsdagBridge pipeline.

Why this exists
---------------
The Batch 2 / Batch 3 acceptance suites test ospgrillage load distribution in isolation.
They did not catch that Batch 2 broke moving-load generation for every full design
(report section 5.1). This suite closes that gap. It builds the bridge from the submitted
sample project file through the same PlateGirderBridge stages the GUI uses, and checks
an engineering result, not just that the code runs:

    For every vehicle live-load case, the vertical force assigned to grillage nodes must
    equal the sum of the axle loads (times their group factors) whose positions lie on the
    deck. Axles on the deck must never be lost, and axles off the deck must contribute zero.

This checks that the distribution matches the factors the analysis defines. It does not
judge whether those factors are right: the per-vehicle lane factor of 0.8 is open defect
DEF-19b. The partly-on-deck vehicle case is covered at unit level by TC-ML-10.

Discrimination, measured on 23 Nov 2026:
  - d74f56d baseline: fails, because the 0.8 group factor is ignored (DEF-01);
  - f555075: errors, because of the out-of-mesh ValueError (section 5.1 regression);
  - bbfe14c: passes.

The on-deck classification is independent of ospgrillage's own grid search. It uses the
convex hull of the mesh node coordinates, which is a rectangle for straight decks and a
parallelogram for skewed ones.

Configurations: the sample .osi as saved (24 m, 0 deg), and the same file with
30 m / +10 deg and 25 m / -10 deg skew.
"""
import contextlib
import io
import os
import sys
import unittest

import yaml

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SRC_DIR = os.path.join(REPO_ROOT, "source", "OsdagBridge", "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
OSI_PATH = os.path.join(REPO_ROOT, "submission", "osi", "sample_24m_composite_plate_girder.osi")

from osdagbridge.desktop.__main__ import create_sqlite, ensure_osdag_core_db  # noqa: E402

with contextlib.redirect_stdout(io.StringIO()):
    create_sqlite()
    ensure_osdag_core_db()

from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge  # noqa: E402
from osdagbridge.core.bridge_types.plate_girder.defaults import solve_extend_basic_input_dict  # noqa: E402
from ospgrillage.load import CompoundLoad, PointLoad  # noqa: E402

REL_TOL = 1e-9


def _convex_hull(points):
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]  # counter-clockwise


def _inside(hull, x, z, tol=1e-9):
    n = len(hull)
    for i in range(n):
        (x1, z1), (x2, z2) = hull[i], hull[(i + 1) % n]
        if (x2 - x1) * (z - z1) - (z2 - z1) * (x - x1) < -tol:
            return False
    return True


def _build(overrides):
    with open(OSI_PATH, encoding="utf-8") as f:
        inp = yaml.safe_load(f)
    if overrides:
        inp.update(overrides)
        solve_extend_basic_input_dict(inp)
    bridge = PlateGirderBridge()
    bridge.set_input(inp)
    with contextlib.redirect_stdout(io.StringIO()):
        bridge._resolve_optimized_bounds_to_mm()
        bridge._convert_girder_dims_mm_to_m()
        bridge._validate_inputs()
        bridge._solve_bridge_layout()
        bridge._stage_grillage_setup()
        bridge.add_dead_loads()
        bridge.add_live_loads()
    return bridge.grillage_model.model


def _check_vehicle_cases(test, model):
    nodes = [(float(v["coordinate"][0]), float(v["coordinate"][2]))
             for v in model.Mesh_obj.node_spec.values()]
    hull = _convex_hull(nodes)
    n_cases = n_on = n_off = 0
    for entry in model.load_case_list:
        groups = entry["loadcase"].load_groups
        if not groups or not all(isinstance(g["load"], (CompoundLoad, PointLoad)) for g in groups):
            continue  # only vehicle (point / compound) cases
        expected = 0.0
        for g in groups:
            factor = float(g.get("factor", 1.0))
            loads = g["load"].compound_load_obj_list if isinstance(g["load"], CompoundLoad) else [g["load"]]
            for pl in loads:
                v = pl.load_point_1
                if _inside(hull, float(v.x), float(v.z)):
                    expected += float(v.p) * factor
                    n_on += 1
                else:
                    n_off += 1
        assigned = sum(float(c[1][2]) for c in entry["load_command"] if c[0] == "load")
        with test.subTest(case=entry["name"]):
            test.assertAlmostEqual(assigned, expected, delta=REL_TOL * max(abs(expected), 1.0))
        n_cases += 1
    test.assertGreater(n_cases, 0, "no vehicle load cases found")
    test.assertGreater(n_on, 0, "no on-deck axles found")
    return n_cases, n_on, n_off


class TestFullPipelineLiveLoadConservation(unittest.TestCase):

    def test_01_sample_osi_24m_straight(self):
        """FP-01: sample .osi as saved (24 m, 0 deg): every vehicle case conserves its on-deck axle loads."""
        _check_vehicle_cases(self, _build({}))

    def test_02_30m_positive_skew(self):
        """FP-02: 30 m, +10 deg skew: vehicle load conservation on a skewed (parallelogram) deck."""
        _check_vehicle_cases(self, _build({"geometry.span": 30.0, "geometry.skew_angle": 10.0}))

    def test_03_25m_negative_skew(self):
        """FP-03: 25 m, -10 deg skew: vehicle load conservation on a mirrored skewed deck."""
        _check_vehicle_cases(self, _build({"geometry.span": 25.0, "geometry.skew_angle": -10.0}))


if __name__ == "__main__":
    unittest.main()
