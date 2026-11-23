"""
Run a complete OsdagBridge plate-girder design headlessly from a saved .osi project file.
This runs the same PlateGirderBridge.design() pipeline the GUI's Design button uses.

Usage (from the package root, inside the project's Python environment):
    python testing/scripts/run_full_design_from_osi.py [OSI_FILE] [--out results.json]
              [--span 30 --skew 10]

Defaults to submission/osi/sample_24m_composite_plate_girder.osi. It prints a one-line
status and the key design demands and checks. With --out, the full output dictionary is
written to a JSON file of your choice; nothing is written inside the package.
Exit code 0 means design() completed; 1 means it raised (the exception is printed).
"""
import argparse
import contextlib
import io
import json
import os
import sys
import time

KEYS = [
    "steeldesign.details.moment.mu_applied",
    "steeldesign.details.shear_check.vu_applied",
    "steeldesign.details.bearing_stiffener.fcdw_wb",
    "steeldesign.details.bearing_stiffener.reaction",
    "util.flexure", "util.shear", "util.fatigue", "util.deflection_crack",
    "steeldesign.deflection.total_mm",
]


def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    ap = argparse.ArgumentParser()
    ap.add_argument("osi", nargs="?",
                    default=os.path.join(root, "submission", "osi", "sample_24m_composite_plate_girder.osi"))
    ap.add_argument("--out")
    ap.add_argument("--span", type=float)
    ap.add_argument("--skew", type=float)
    ap.add_argument("--src", default=os.path.join(root, "source", "OsdagBridge", "src"),
                    help="application source to test (default: the packaged source)")
    a = ap.parse_args()
    sys.path.insert(0, os.path.abspath(a.src))

    import yaml
    from osdagbridge.desktop.__main__ import create_sqlite, ensure_osdag_core_db
    with contextlib.redirect_stdout(io.StringIO()):
        create_sqlite()
        ensure_osdag_core_db()
    from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
    from osdagbridge.core.bridge_types.plate_girder.defaults import solve_extend_basic_input_dict

    with open(a.osi, encoding="utf-8") as f:
        inp = yaml.safe_load(f)
    over = {}
    if a.span is not None:
        over["geometry.span"] = a.span
    if a.skew is not None:
        over["geometry.skew_angle"] = a.skew
    if over:
        inp.update(over)
        solve_extend_basic_input_dict(inp)

    bridge = PlateGirderBridge()
    bridge.set_input(inp)
    t0 = time.time()
    ok, err = True, None
    class _SafeIO(io.StringIO):
        def reconfigure(self, *args, **kwargs):
            pass

    try:
        with contextlib.redirect_stdout(_SafeIO()):
            bridge.design()
    except Exception as e:  # report, do not hide
        ok, err = False, f"{type(e).__name__}: {e}"
    od = bridge.output_dict or {}
    try:
        n_lc = len(bridge.grillage_model.model.load_case_list)
    except Exception:
        n_lc = None
    print(f"source : {os.path.abspath(a.src)}")
    print(f"input  : {os.path.basename(a.osi)} {over or ''}")
    print(f"design : {'COMPLETED' if ok else 'FAILED'} in {time.time() - t0:.1f} s"
          + ("" if ok else f" -> {err[:200]}"))
    print(f"grillage load cases: {n_lc}   output keys: {len(od)}")
    dr = od.get("design_results")
    if isinstance(dr, dict) and "n_girders" in dr:
        print(f"  design_results.n_girders = {dr['n_girders']}")
    for k in KEYS:
        if k in od:
            print(f"  {k} = {od[k]}")
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump({"source": os.path.abspath(a.src), "input": os.path.basename(a.osi), "overrides": over,
                       "completed": ok, "error": err, "load_cases": n_lc,
                       "output": {str(k): str(v) for k, v in od.items()}}, f, indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
