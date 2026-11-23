"""
Test script to run a full design through CustomWindow in osdagbridge-py312.
"""

import sys
import os
import time
import traceback
import json

from osdagbridge.desktop.__main__ import (
    _register_conda_dll_directories,
    _ensure_std_streams,
    create_sqlite,
    ensure_osdag_core_db,
    load_stylesheet,
    _set_windows_app_id,
    _app_icon
)

_register_conda_dll_directories()
_ensure_std_streams()
create_sqlite()
ensure_osdag_core_db()

from PySide6.QtWidgets import QApplication, QLineEdit, QComboBox
from PySide6.QtCore import Qt

from osdagbridge.desktop.ui.template_page import CustomWindow
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
)

def main():
    print("Initializing QApplication...")
    app = QApplication.instance() or QApplication(sys.argv)

    print("Constructing CustomWindow...")
    window = CustomWindow("OsdagBridge", PlateGirderBridge)
    window.resize(1600, 950)
    window.show()

    # Process events to let widgets layout and prime
    for _ in range(30):
        app.processEvents()
        time.sleep(0.01)

    print("Setting basic input fields...")
    # 1. Span
    span_w = window.input_dock._w(KEY_SPAN)
    if isinstance(span_w, QLineEdit):
        span_w.setText("24.0")
    window.input_dock._update_input_dict(KEY_SPAN, 24.0)

    # 2. Carriageway Width
    cw_w = window.input_dock._w(KEY_CARRIAGEWAY_WIDTH)
    if isinstance(cw_w, QLineEdit):
        cw_w.setText("7.5")
    window.input_dock._update_input_dict(KEY_CARRIAGEWAY_WIDTH, 7.5)

    # 3. Skew Angle
    skew_w = window.input_dock._w(KEY_SKEW_ANGLE)
    if isinstance(skew_w, QLineEdit):
        skew_w.setText("0.0")
    window.input_dock._update_input_dict(KEY_SKEW_ANGLE, 0.0)

    # 4. Project Location
    loc = {
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
    window.input_dock._update_input_dict(KEY_PROJECT_LOCATION, loc)
    info_lbl = window.input_dock._w(f"{KEY_PROJECT_LOCATION}_info_label")
    if info_lbl:
        info_lbl.setText("Ahmednagar, Maharashtra")
    info_row = window.input_dock._w(f"{KEY_PROJECT_LOCATION}_info_row")
    if info_row:
        info_row.setVisible(True)

    window.input_dock.is_require_field_changed = True

    for _ in range(20):
        app.processEvents()
        time.sleep(0.01)

    print("\nValidating required inputs...")
    val_ok = window.validate_required_inputs()
    print(f"Validation result: {val_ok}")
    if not val_ok:
        print("ERROR: validate_required_inputs failed!")
        return

    print("\nTriggering Design via window.common_design_func('Design')...")
    window.common_design_func("Design")

    # Monitor design progress
    start_time = time.time()
    print("Waiting for design worker thread to complete...")
    while getattr(window, "_design_running", False):
        app.processEvents()
        time.sleep(0.05)
        if time.time() - start_time > 180: # 3 min timeout
            print("TIMEOUT waiting for design to complete!")
            break

    # Let UI settle
    for _ in range(50):
        app.processEvents()
        time.sleep(0.02)

    elapsed = time.time() - start_time
    print(f"\nDesign run finished in {elapsed:.2f} seconds.")

    backend = window.backend
    out_dict = getattr(backend, "output_dict", {})
    print(f"Output dict size: {len(out_dict)}")

    # Check for DCR / design results
    dcr_keys = [k for k in out_dict.keys() if "dcr" in k.lower() or "ratio" in k.lower() or "status" in k.lower()]
    print(f"Found {len(dcr_keys)} DCR / status keys in output_dict.")
    for k in dcr_keys[:10]:
        print(f"  {k}: {out_dict[k]}")

    # Check 3D CAD widget
    cad_w = getattr(window, "cad_3d_widget", None)
    if cad_w:
        print(f"3D CAD Widget Visible: {cad_w.isVisible()}")
        has_model = getattr(cad_w, "generator", None) is not None and getattr(cad_w.generator, "model_data", None) is not None
        print(f"3D CAD Model Generated: {has_model}")

    # Capture screenshots
    evidence_dir = r"F:\FOSSEE internship\testing\evidence\phase_1d"
    os.makedirs(evidence_dir, exist_ok=True)
    ss_path = os.path.join(evidence_dir, "01_end_to_end_design_full_window.png")
    window.grab().save(ss_path, "PNG")
    print(f"Saved full window screenshot: {ss_path}")

    if cad_w and cad_w.isVisible():
        cad_ss_path = os.path.join(evidence_dir, "02_3d_cad_bridge_model.png")
        cad_w.grab().save(cad_ss_path, "PNG")
        print(f"Saved 3D CAD screenshot: {cad_ss_path}")

    # Test report generation
    print("\nTesting design report generation...")
    try:
        from osdagbridge.core.reports.report_generator import ReportRequest
        req = ReportRequest(
            project_title="Phase 1D E2E Verification Bridge",
            client_name="FOSSEE Diagnostic Campaign",
            engineer_name="Antigravity Test Agent",
            company_name="IIT Bombay / FOSSEE",
            output_dir=evidence_dir,
            file_stem="phase_1d_design_report",
            include_drawings=True
        )
        cad_gen = getattr(cad_w, "generator", {}) if cad_w else {}
        res = backend.generate_design_report(req, cad_gen)
        print("Report generation returned:", res)
        if hasattr(res, "pdf_path") and res.pdf_path and os.path.exists(res.pdf_path):
            print(f"SUCCESS: PDF Report generated at {res.pdf_path} ({os.path.getsize(res.pdf_path)} bytes)")
        elif hasattr(res, "tex_path") and res.tex_path and os.path.exists(res.tex_path):
            print(f"TeX file generated at {res.tex_path}")
    except Exception as e:
        print(f"Report generation error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
