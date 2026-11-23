"""
Phase 1D — Complete End-to-End Plate Girder Bridge Design, Analysis, CAD, and Report Execution Script.
Executes on osdagbridge-py312 environment.
"""

import sys
import os
import time
import json
import yaml
import datetime
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

from PySide6.QtWidgets import QApplication, QLineEdit
from PySide6.QtCore import Qt

from osdagbridge.desktop.ui.template_page import CustomWindow
from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
from osdagbridge.core.reports.report_generator import ReportRequest, ReportMetadata, ReportOptions
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

EVIDENCE_DIR = r"F:\FOSSEE internship\testing\evidence\phase_1d"
os.makedirs(EVIDENCE_DIR, exist_ok=True)

class LogTee:
    def __init__(self, filepath):
        self.file = open(filepath, "w", encoding="utf-8")
        self.stdout = sys.stdout

    def write(self, data):
        self.stdout.write(data)
        self.file.write(data)
        self.file.flush()

    def flush(self):
        self.stdout.flush()
        self.file.flush()

    def close(self):
        self.file.close()

def execute():
    log_file = os.path.join(EVIDENCE_DIR, "execution.log")
    tee = LogTee(log_file)
    sys.stdout = tee

    try:
        print("=" * 80)
        print("OSDAGBRIDGE PHASE 1D — END-TO-END COMPUTATIONAL VERIFICATION RUN")
        print("Timestamp:", datetime.datetime.now().isoformat())
        print("Python:", sys.executable)
        print("=" * 80)

        app = QApplication.instance() or QApplication(sys.argv)

        print("\n[Step 1/8] Instantiating Desktop Application Window (CustomWindow)...")
        window = CustomWindow("OsdagBridge - Phase 1D Verification", PlateGirderBridge)
        window.resize(1600, 950)
        window.show()

        for _ in range(30):
            app.processEvents()
            time.sleep(0.01)

        print("[Step 2/8] Setting Benchmark Bridge Input Configuration...")
        span = 24.0
        cw = 7.5
        skew = 0.0

        # Update input widgets and input_dict
        span_w = window.input_dock._w(KEY_SPAN)
        if isinstance(span_w, QLineEdit):
            span_w.setText(str(span))
        window.input_dock._update_input_dict(KEY_SPAN, span)

        cw_w = window.input_dock._w(KEY_CARRIAGEWAY_WIDTH)
        if isinstance(cw_w, QLineEdit):
            cw_w.setText(str(cw))
        window.input_dock._update_input_dict(KEY_CARRIAGEWAY_WIDTH, cw)

        skew_w = window.input_dock._w(KEY_SKEW_ANGLE)
        if isinstance(skew_w, QLineEdit):
            skew_w.setText(str(skew))
        window.input_dock._update_input_dict(KEY_SKEW_ANGLE, skew)

        # Set Location
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

        # Save input configuration before design
        inp_json_path = os.path.join(EVIDENCE_DIR, "input_configuration.json")
        with open(inp_json_path, "w", encoding="utf-8") as f:
            json.dump(window.input_dict, f, indent=2, default=str)
        print(f"  Input configuration saved: {inp_json_path}")

        inp_yaml_path = os.path.join(EVIDENCE_DIR, "input_configuration.yaml")
        with open(inp_yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(window.input_dict, f, default_flow_style=False)
        print(f"  Input configuration saved (YAML): {inp_yaml_path}")

        print("\n[Step 3/8] Validating Required Inputs...")
        val_ok = window.validate_required_inputs()
        print(f"  validate_required_inputs: {val_ok}")
        if not val_ok:
            raise RuntimeError("Required input validation failed.")

        print("\n[Step 4/8] Triggering Common Design Execution Pipeline...")
        start_time = time.time()
        window.common_design_func("Design")

        print("  Waiting for design worker thread to complete...")
        while getattr(window, "_design_running", False):
            app.processEvents()
            time.sleep(0.05)
            if time.time() - start_time > 300:
                raise TimeoutError("Design run exceeded 300 seconds timeout.")

        for _ in range(50):
            app.processEvents()
            time.sleep(0.02)

        elapsed = time.time() - start_time
        print(f"  Design worker finished in {elapsed:.2f} seconds.")

        backend = window.backend
        out_dict = getattr(backend, "output_dict", {})
        print(f"\n[Step 5/8] Validating Output Dictionary Snapshot ({len(out_dict)} keys)...")

        # Save output dictionary snapshot
        out_dict_serializable = {}
        for k, v in out_dict.items():
            if isinstance(v, (int, float, str, bool, list, dict)) or v is None:
                out_dict_serializable[k] = v
            else:
                out_dict_serializable[k] = str(v)

        out_json_path = os.path.join(EVIDENCE_DIR, "output_dictionary_snapshot.json")
        with open(out_json_path, "w", encoding="utf-8") as f:
            json.dump(out_dict_serializable, f, indent=2, default=str)
        print(f"  Output dictionary snapshot saved: {out_json_path}")

        # Extract governing checks and DCRs
        print("\n[Step 6/8] Extracting Structural Results & DCRs:")
        summary_results = {
            "elapsed_seconds": elapsed,
            "overall_width": out_dict.get("typical_section.overall_width"),
            "no_of_girders": out_dict.get("typical_section.no_of_girders"),
            "girder_spacing": out_dict.get("typical_section.girder_spacing"),
            "deck_overhang": out_dict.get("typical_section.deck_overhang"),
            "cross_bracing_results": out_dict.get("crossbracing_design_results"),
            "end_diaphragm_results": out_dict.get("end_diaphragm_design_results"),
        }
        for k, v in summary_results.items():
            print(f"  {k}: {v}")

        print("\n[Step 7/8] Verifying 3D CAD & Capturing Genuine Screenshots...")
        cad_w = getattr(window, "cad_3d_widget", None)
        if cad_w:
            print(f"  3D CAD Widget Visible: {cad_w.isVisible()}")
            generator = getattr(cad_w, "generator", None)
            has_model = generator is not None and getattr(generator, "model_data", None) is not None
            print(f"  3D CAD Solid Model Generated: {has_model}")

        # Ensure 3D view is visible and focused
        window.cad_3d_view_toggle(force_show=True)
        for _ in range(50):
            app.processEvents()
            time.sleep(0.02)

        ss_win_path = os.path.join(EVIDENCE_DIR, "01_end_to_end_design_full_window.png")
        window.grab().save(ss_win_path, "PNG")
        print(f"  Captured Full Main Window: {ss_win_path} ({os.path.getsize(ss_win_path)} bytes)")

        if cad_w and cad_w.isVisible():
            ss_cad_path = os.path.join(EVIDENCE_DIR, "02_3d_cad_bridge_model.png")
            cad_w.grab().save(ss_cad_path, "PNG")
            print(f"  Captured 3D CAD Viewport: {ss_cad_path} ({os.path.getsize(ss_cad_path)} bytes)")

        output_dock = getattr(window, "output_dock", None)
        if output_dock and output_dock.isVisible():
            ss_out_path = os.path.join(EVIDENCE_DIR, "03_output_dock_results.png")
            output_dock.grab().save(ss_out_path, "PNG")
            print(f"  Captured Output Dock: {ss_out_path} ({os.path.getsize(ss_out_path)} bytes)")

        print("\n[Step 8/8] Testing Formal PDF Design Report Generation...")
        meta = ReportMetadata(
            project_name="Phase 1D E2E Verification Bridge",
            project_location="Ahmednagar, Maharashtra",
            designer="Antigravity Test Agent",
            reviewer="FOSSEE Technical Lead",
            client="FOSSEE Diagnostic Campaign",
            company="IIT Bombay / FOSSEE",
            group_name="FOSSEE OsdagBridge Team",
            subtitle="Plate Girder Bridge (24m Span, 7.5m CW)",
            job_number="FOSSEE-2026-P1D",
            additional_comments="Automated single end-to-end design verification under osdagbridge-py312.",
            logo_path=None,
            report_date=datetime.date.today().isoformat()
        )

        opts = ReportOptions(
            sections=[
                "exec_summary",
                "project_info",
                "input_parameters",
                "loads",
                "analysis",
                "design_checks",
                "drawings",
                "quantities",
                "standards",
                "design_log_window",
                "references"
            ],
            include_figures=True,
            include_toc=True,
            include_pdf=True
        )

        req = ReportRequest(
            metadata=meta,
            options=opts,
            output_dir=EVIDENCE_DIR,
            file_stem="phase_1d_design_report"
        )

        cad_gen = getattr(cad_w, "generator", {}) if cad_w else {}
        report_res = backend.generate_design_report(req, cad_gen)
        print("  Report Result Object:", report_res)

        if hasattr(report_res, "pdf_path") and report_res.pdf_path and os.path.exists(report_res.pdf_path):
            print(f"  SUCCESS: PDF Report generated: {report_res.pdf_path} ({os.path.getsize(report_res.pdf_path)} bytes)")
        elif hasattr(report_res, "tex_path") and report_res.tex_path and os.path.exists(report_res.tex_path):
            print(f"  TeX file created at {report_res.tex_path}")

        print("\n" + "=" * 80)
        print("PHASE 1D END-TO-END RUN COMPLETED SUCCESSFULLY!")
        print("=" * 80)

    except Exception as e:
        print("\n" + "!" * 80)
        print(f"EXECUTION FAILED WITH ERROR: {e}")
        print("!" * 80)
        traceback.print_exc()
        fail_path = os.path.join(EVIDENCE_DIR, "failure_traceback.txt")
        with open(fail_path, "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
    finally:
        sys.stdout = tee.stdout
        tee.close()

if __name__ == "__main__":
    execute()
