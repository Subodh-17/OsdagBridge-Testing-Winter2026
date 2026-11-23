"""
Diagnostic test script to run PlateGirderBridge backend design directly.
"""

import sys
import copy
import traceback

from osdagbridge.desktop.__main__ import (
    _register_conda_dll_directories,
    _ensure_std_streams,
    create_sqlite,
    ensure_osdag_core_db,
)

_register_conda_dll_directories()
_ensure_std_streams()
create_sqlite()
ensure_osdag_core_db()

from osdagbridge.core.bridge_types.plate_girder.defaults import (
    BASIC_INPUT_DICT,
    solve_extend_basic_input_dict,
)
from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
from osdagbridge.core.utils.common import (
    KEY_SPAN,
    KEY_CARRIAGEWAY_WIDTH,
    KEY_PROJECT_LOCATION,
    KEY_SKEW_ANGLE,
    KEY_INCLUDE_MEDIAN,
    KEY_FOOTPATH,
    KEY_DESIGN_MODE,
    KEY_STRUCTURE_TYPE,
    KEY_GIRDER,
    KEY_CROSS_BRACING,
    KEY_END_DIAPHRAGM,
)

def run():
    print("Preparing input dictionary...")
    inp = copy.deepcopy(BASIC_INPUT_DICT)
    inp[KEY_SPAN] = 24.0
    inp[KEY_CARRIAGEWAY_WIDTH] = 7.5
    inp[KEY_SKEW_ANGLE] = 0.0
    inp[KEY_INCLUDE_MEDIAN] = "No"
    inp[KEY_FOOTPATH] = "None"
    inp[KEY_DESIGN_MODE] = "Optimized"
    inp[KEY_STRUCTURE_TYPE] = "Highway Bridge"

    inp[KEY_PROJECT_LOCATION] = {
        'method': 'location_name',
        'data': {
            'state': 'Maharashtra',
            'district': 'Ahmednagar',
        },
        'weather_data': {
            'wind_speed': 39.0,
            'zone': 'III',
            'z_value': 0.16,
            'max_temp': 48.2,
            'min_temp': 2.2,
            'latitude': 19.0948,
            'longitude': 74.748,
        },
        'display_text': 'Ahmednagar, Maharashtra',
        'show_display': True,
    }

    # Prime materials from MaterialPropertiesDialog or base values
    from osdagbridge.desktop.ui.dialogs.material_properties import MaterialPropertiesDialog
    for member_key, selected_mat in [
        (KEY_GIRDER, inp[KEY_GIRDER]),
        (KEY_CROSS_BRACING, inp[KEY_CROSS_BRACING]),
        (KEY_END_DIAPHRAGM, inp[KEY_END_DIAPHRAGM]),
    ]:
        dlg = MaterialPropertiesDialog(read_only=True, selected_material=selected_mat, member=member_key)
        fields = dlg.get_export_fields() or {}
        inp.update(fields)
    
    # Also deck material
    from osdagbridge.core.utils.common import KEY_DECK_CONCRETE_GRADE_BASIC
    deck_mat = inp[KEY_DECK_CONCRETE_GRADE_BASIC]
    dlg_deck = MaterialPropertiesDialog(read_only=True, selected_material=deck_mat, member=KEY_DECK_CONCRETE_GRADE_BASIC)
    inp.update(dlg_deck.get_export_fields() or {})
    
    # Also default rebar
    from osdagbridge.core.utils.common import KEY_DS_REINF_MATERIAL
    inp[KEY_DS_REINF_MATERIAL] = "Fe 500"

    print("Running solve_extend_basic_input_dict...")
    solve_extend_basic_input_dict(inp)

    print("\nInstantiating PlateGirderBridge...")
    bridge = PlateGirderBridge()
    print("Setting input dictionary...")
    bridge.set_input(inp)

    print("\nStarting bridge.design()...")
    try:
        bridge.design()
        print("\nSUCCESS: bridge.design() completed!")
        print("Output dict keys count:", len(bridge.output_dict))
        print("DCR summary check:")
        # Look for DCR keys
        for k, v in bridge.output_dict.items():
            if "dcr" in k.lower() or "ratio" in k.lower() or "status" in k.lower():
                print(f"  {k}: {v}")
    except Exception as e:
        print("\nERROR during bridge.design():", e)
        traceback.print_exc()

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        import traceback
        with open(r"F:\FOSSEE internship\testing\scripts\diag_err.txt", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        traceback.print_exc()
        sys.exit(1)
