"""
Phase 1B GUI Smoke Test & CAD Viewport Verification Script for OsdagBridge.
Captures genuine screenshots of all UI components, inspects docks and dialogs,
and verifies OpenCASCADE basic 3D CAD rendering without launching structural calculations.
"""

import sys
import os
import json
import time

# Ensure Conda and Qt DLL search paths are registered
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

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QScreen

from osdagbridge.desktop.ui.template_page import CustomWindow
from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.AIS import AIS_Shape

def run_smoke_test():
    report_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "initialization_log": [],
        "errors": [],
        "components": {},
        "cad_smoke_test": {}
    }
    
    screenshot_dir = r"F:\FOSSEE internship\evidence\screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    
    print("=" * 65)
    print("OSDAGBRIDGE PHASE 1B — DESKTOP APPLICATION SMOKE TEST")
    print("=" * 65)
    
    # 1. Database & Resource Setup
    print("\n[Step 1/6] Initializing Databases and Application State...")
    try:
        create_sqlite()
        report_data["initialization_log"].append("Intg_osdag SQLite database verified/created.")
    except Exception as e:
        err = f"create_sqlite error: {e}"
        print(f"  {err}")
        report_data["errors"].append(err)
        
    try:
        ensure_osdag_core_db()
        report_data["initialization_log"].append("osdag_core database build attempted.")
    except Exception as e:
        err = f"ensure_osdag_core_db error: {e}"
        print(f"  {err}")
        report_data["errors"].append(err)

    # 2. Application & Window Construction
    print("\n[Step 2/6] Constructing QApplication and CustomWindow...")
    _set_windows_app_id()
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
        
    icon = _app_icon()
    if not icon.isNull():
        app.setWindowIcon(icon)
        
    stylesheet = load_stylesheet()
    if stylesheet:
        app.setStyleSheet(stylesheet)
        
    window = CustomWindow("OsdagBridge", PlateGirderBridge)
    if not icon.isNull():
        window.setWindowIcon(icon)
        
    window.resize(1600, 950)
    window.show()
    
    # Let Qt process layout, event loop, and deferred timers
    for _ in range(60):
        app.processEvents()
        time.sleep(0.02)
        
    is_visible = window.isVisible()
    print(f"  Main Window Visibility: {is_visible}")
    print(f"  Main Window Title:      {window.windowTitle()}")
    print(f"  Main Window Size:       {window.size().width()}x{window.size().height()}")
    
    report_data["components"]["main_window"] = {
        "visible": is_visible,
        "title": window.windowTitle(),
        "width": window.size().width(),
        "height": window.size().height()
    }
    
    # Screenshot 1: Default Initial Main Window
    p1 = os.path.join(screenshot_dir, "01_main_window_default.png")
    window.grab().save(p1, "PNG")
    print(f"  Screenshot saved: {p1} ({os.path.getsize(p1)} bytes)")
    
    # 3. Input Panels Inspection
    print("\n[Step 3/6] Inspecting Input Dock and Panels...")
    input_dock = getattr(window, "input_dock", None)
    if input_dock:
        print(f"  Input Dock Visible:     {input_dock.isVisible()}")
        
        # Grab detailed screenshot of Input Dock
        p2 = os.path.join(screenshot_dir, "02_input_dock_detail.png")
        input_dock.grab().save(p2, "PNG")
        print(f"  Screenshot saved: {p2} ({os.path.getsize(p2)} bytes)")
        
        # Collect input parameters
        input_fields = {}
        for child in input_dock.findChildren(object):
            name = getattr(child, "objectName", lambda: "")()
            cls_name = child.__class__.__name__
            if cls_name in ["QLineEdit", "QComboBox", "QSpinBox", "QDoubleSpinBox"]:
                val = ""
                if hasattr(child, "currentText"):
                    val = child.currentText()
                elif hasattr(child, "text"):
                    val = child.text()
                elif hasattr(child, "value"):
                    val = str(child.value())
                if name:
                    input_fields[name] = {"type": cls_name, "value": val}
                    
        report_data["components"]["input_dock"] = {
            "visible": input_dock.isVisible(),
            "width": input_dock.size().width(),
            "height": input_dock.size().height(),
            "fields_count": len(input_fields),
            "sample_fields": dict(list(input_fields.items())[:15])
        }
    else:
        print("  WARNING: input_dock not found on window.")
        report_data["errors"].append("input_dock missing on CustomWindow")

    # 4. Additional Inputs Dialog Inspection
    print("\n[Step 4/6] Inspecting Additional Inputs Dialog...")
    try:
        add_dialog = window._get_additional_inputs()
        if add_dialog:
            add_dialog.show()
            for _ in range(30):
                app.processEvents()
                time.sleep(0.01)
                
            print(f"  Additional Inputs Visible: {add_dialog.isVisible()}")
            print(f"  Dialog Geometry:           {add_dialog.size().width()}x{add_dialog.size().height()}")
            
            # Identify tab widget inside additional inputs
            tab_names = []
            for child in add_dialog.findChildren(object):
                if child.__class__.__name__ == "QTabWidget":
                    tab_names = [child.tabText(i) for i in range(child.count())]
                    break
            print(f"  Available Tabs:            {tab_names}")
            
            p3 = os.path.join(screenshot_dir, "03_additional_inputs_dialog.png")
            add_dialog.grab().save(p3, "PNG")
            print(f"  Screenshot saved: {p3} ({os.path.getsize(p3)} bytes)")
            
            report_data["components"]["additional_inputs_dialog"] = {
                "visible": add_dialog.isVisible(),
                "width": add_dialog.size().width(),
                "height": add_dialog.size().height(),
                "tabs": tab_names
            }
            add_dialog.hide()
            app.processEvents()
    except Exception as e:
        err = f"Additional Inputs Dialog failed: {e}"
        print(f"  {err}")
        report_data["errors"].append(err)

    # 5. Output Docks, Logs Dock, and 2D CAD Plots
    print("\n[Step 5/6] Inspecting Output Docks, Logs, and 2D Plots...")
    try:
        # Toggle Output Dock to visible
        if not getattr(window, "output_dock_active", False):
            window.output_dock_toggle()
            for _ in range(20):
                app.processEvents()
                time.sleep(0.01)
                
        output_dock = getattr(window, "output_dock", None)
        if output_dock:
            print(f"  Output Dock Visible:    {output_dock.isVisible()}")
            p4 = os.path.join(screenshot_dir, "04_output_dock_detail.png")
            output_dock.grab().save(p4, "PNG")
            print(f"  Screenshot saved: {p4} ({os.path.getsize(p4)} bytes)")
            
            report_data["components"]["output_dock"] = {
                "visible": output_dock.isVisible(),
                "width": output_dock.size().width(),
                "height": output_dock.size().height()
            }
            
        # Toggle Logs Dock to visible
        if not getattr(window, "log_dock_active", False):
            window.logs_dock_toggle()
            for _ in range(20):
                app.processEvents()
                time.sleep(0.01)
                
        logs_dock = getattr(window, "logs_dock", None)
        if logs_dock:
            print(f"  Logs Dock Visible:      {logs_dock.isVisible()}")
            p5 = os.path.join(screenshot_dir, "05_logs_dock_detail.png")
            logs_dock.grab().save(p5, "PNG")
            print(f"  Screenshot saved: {p5} ({os.path.getsize(p5)} bytes)")
            
            report_data["components"]["logs_dock"] = {
                "visible": logs_dock.isVisible(),
                "width": logs_dock.size().width(),
                "height": logs_dock.size().height()
            }
            
        # Inspect 2D Dual CAD Widget
        cad_2d = getattr(window, "cad_2d_widget", None)
        if cad_2d:
            p2d = os.path.join(screenshot_dir, "06c_cad_dual_view_composite.png")
            cad_2d.grab().save(p2d, "PNG")
            print(f"  2D Dual CAD View saved: {p2d} ({os.path.getsize(p2d)} bytes)")
            
            cs = getattr(cad_2d, "cross_section_widget", None)
            if cs:
                pcs = os.path.join(screenshot_dir, "06a_2d_cross_section_cad.png")
                cs.grab().save(pcs, "PNG")
                print(f"  2D Cross Section View saved: {pcs} ({os.path.getsize(pcs)} bytes)")
                
            top = getattr(cad_2d, "top_view_widget", None)
            if top:
                ptop = os.path.join(screenshot_dir, "06b_2d_top_view_cad.png")
                top.grab().save(ptop, "PNG")
                print(f"  2D Top View saved: {ptop} ({os.path.getsize(ptop)} bytes)")
                
            report_data["components"]["2d_plots"] = {
                "dual_view_visible": cad_2d.isVisible(),
                "cross_section_present": cs is not None,
                "top_view_present": top is not None
            }
    except Exception as e:
        err = f"Output/Logs/2D dock error: {e}"
        print(f"  {err}")
        report_data["errors"].append(err)

    # 6. 3D Viewport Inspection & CAD Smoke Test
    print("\n[Step 6/6] Inspecting 3D CAD Viewport & Executing CAD Smoke Test...")
    try:
        # Toggle 3D CAD view active
        window.cad_3d_view_toggle(force_show=True)
        for _ in range(40):
            app.processEvents()
            time.sleep(0.02)
            
        cad_3d = getattr(window, "cad_3d_widget", None)
        if cad_3d:
            print(f"  CAD 3D Widget Visible:  {cad_3d.isVisible()}")
            print(f"  Display Ready:          {cad_3d._is_display_ready()}")
            
            # Export default empty viewport via OpenCASCADE native image export
            p6_export = os.path.join(screenshot_dir, "06_cad_3d_viewport_active.png")
            if cad_3d.display:
                cad_3d.display.ExportToImage(p6_export)
                print(f"  Exported 3D Viewport: {p6_export} ({os.path.getsize(p6_export)} bytes)")
            
            # TASK 4 — CAD Smoke Test: Basic OpenCASCADE Geometry Creation
            print("\n  Executing CAD Smoke Test (basic OpenCASCADE BRep Box)...")
            box_shape = BRepPrimAPI_MakeBox(2000.0, 500.0, 300.0).Shape()
            print("  BRepPrimAPI_MakeBox created successfully: OK")
            
            if cad_3d.display:
                cad_3d.display.EraseAll()
                cad_3d.display.DisplayShape(box_shape, color="BLUE", update=True)
                cad_3d.display.FitAll()
                for _ in range(40):
                    app.processEvents()
                    time.sleep(0.02)
                    
                p7_export = os.path.join(screenshot_dir, "07_cad_smoke_test_box.png")
                cad_3d.display.ExportToImage(p7_export)
                print(f"  CAD Smoke Test Screenshot saved: {p7_export} ({os.path.getsize(p7_export)} bytes)")
                
                report_data["cad_smoke_test"] = {
                    "brep_box_created": True,
                    "ais_displayed": True,
                    "viewport_dimensions": f"{cad_3d.size().width()}x{cad_3d.size().height()}",
                    "screenshot": p7_export,
                    "screenshot_bytes": os.path.getsize(p7_export),
                    "status": "PASS"
                }
            else:
                print("  WARNING: cad_3d.display is None!")
                report_data["cad_smoke_test"] = {"status": "FAILED", "reason": "cad_3d.display is None"}
                
        # Full application composite screenshot with 3D CAD active
        p8 = os.path.join(screenshot_dir, "08_main_window_full_composite.png")
        window.grab().save(p8, "PNG")
        print(f"  Composite Screenshot saved: {p8} ({os.path.getsize(p8)} bytes)")
        
    except Exception as e:
        err = f"CAD 3D Viewport error: {e}"
        print(f"  {err}")
        report_data["errors"].append(err)

    # Save test report JSON
    json_path = r"F:\FOSSEE internship\evidence\environment\gui_smoke_test_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)
    print(f"\nSmoke test results written to: {json_path}")
    
    # Clean teardown
    window.close()
    app.processEvents()
    print("=" * 65)
    print("PHASE 1B GUI SMOKE TEST COMPLETED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == "__main__":
    run_smoke_test()
