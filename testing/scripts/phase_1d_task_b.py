"""
Phase 1D Task B — Read-Only Database Investigation Script
Examines:
1. Installed osdag_core database
2. OsdagBridge local database under src/osdagbridge/core/data/ResourceFiles/
Dumps table names, record counts, table columns/schemas, and answers all source audit questions.
Saves results into testing/evidence/phase_1d/task_b_database_audit.json.
"""

import os
import sqlite3
import json

OSDAG_CORE_DB = r"C:\Users\Subodh\miniconda3\envs\osdagbridge-py312\Lib\site-packages\osdag_core\data\ResourceFiles\Database\Intg_osdag.sqlite"
OSDAGBRIDGE_LOCAL_DB = r"F:\FOSSEE internship\source\OsdagBridge\src\osdagbridge\core\data\ResourceFiles\Intg_osdag.sqlite"

def inspect_database(db_path):
    info = {
        "path": db_path,
        "exists": os.path.exists(db_path),
        "size_bytes": os.path.getsize(db_path) if os.path.exists(db_path) else 0,
        "tables": {}
    }
    if not info["exists"]:
        return info

    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [row[0] for row in cursor.fetchall()]

    for t in tables:
        cursor.execute(f'SELECT COUNT(*) FROM "{t}";')
        count = cursor.fetchone()[0]

        cursor.execute(f'PRAGMA table_info("{t}");')
        columns = [{"cid": col[0], "name": col[1], "type": col[2], "notnull": col[3], "dflt_value": col[4], "pk": col[5]} for col in cursor.fetchall()]

        cursor.execute('SELECT sql FROM sqlite_master WHERE type="table" AND name=?;', (t,))
        schema_sql = cursor.fetchone()[0]

        info["tables"][t] = {
            "record_count": count,
            "columns": columns,
            "schema_sql": schema_sql
        }

    conn.close()
    return info

def main():
    print("Inspecting Database 1: osdag_core...")
    core_info = inspect_database(OSDAG_CORE_DB)
    print(f"  Found {len(core_info['tables'])} tables.")

    print("Inspecting Database 2: osdagbridge local...")
    local_info = inspect_database(OSDAGBRIDGE_LOCAL_DB)
    print(f"  Found {len(local_info['tables'])} tables.")

    audit_summary = {
        "osdag_core_database": core_info,
        "osdagbridge_local_database": local_info,
        "source_code_findings": {
            "modules_opening_osdag_core_db": [
                "osdag_core.Common (Common.py)",
                "osdag_core.design_type.connection.connection",
                "osdag_core.export_ifc.database_connector",
                "osdag_core.utils.common.component",
                "osdag_core.utils.common.material",
                "osdag_core.utils.common.other_standards",
                "osdagbridge.desktop.__main__.ensure_osdag_core_db (populates from Intg_osdag.sql if empty)"
            ],
            "modules_opening_osdagbridge_local_db": [
                "osdagbridge.core.bridge_types.plate_girder.plategirderbridge (_DB_PATH)",
                "osdagbridge.core.utils.common (_DB_PATH & DB_PATH)",
                "osdagbridge.core.ifc_export_bridge.metadata_mapper (_DB_PATH)",
                "osdagbridge.desktop.__main__.create_sqlite (creates/updates from Intg_osdag.sql)",
                "osdagbridge.desktop.ui.dialogs.material_properties (db_path)",
                "osdagbridge.desktop.ui.dialogs.transverse_member_design (DB_PATH)",
                "osdagbridge.desktop.ui.widgets.section_viewer (DB_PATH)"
            ],
            "material_information_provider": {
                "general_steel_materials": "osdag_core database ('Material' table, 10 records: E 165 to E 450)",
                "bridge_materials": "osdagbridge local database ('Concrete_Grade_Properties', 'Rebar_Grade_Properties', 'Steel_Grade_Properties')"
            },
            "concrete_steel_rebar_grade_properties_provider": "osdagbridge local database. These three tables (Concrete_Grade_Properties [16 rows], Rebar_Grade_Properties [7 rows], Steel_Grade_Properties [28 rows]) exist exclusively in osdagbridge local database and do NOT exist in osdag_core.",
            "path_resolution": {
                "osdag_core": "Uses importlib.resources.files('osdag_core.data.ResourceFiles.Database').joinpath('Intg_osdag.sqlite'), yielding absolute/resolved site-packages path.",
                "osdagbridge": "Uses Path(__file__).resolve().parents[2] / 'data' / 'ResourceFiles' / 'Intg_osdag.sqlite' or importlib.resources.files('osdagbridge.core.data.ResourceFiles').joinpath('Intg_osdag.sqlite'), resolving to local package resource directory."
            },
            "data_initialization_copy_seed_overwrite": {
                "osdagbridge.desktop.__main__.create_sqlite": "Checks if sqlite exists; if missing or 0-byte or mtime < sql mtime, builds/updates from Intg_osdag.sql.",
                "osdagbridge.desktop.__main__.ensure_osdag_core_db": "Checks if osdag_core sqlite is missing, 0 bytes, or has no tables; if so, populates from osdag_core's Intg_osdag.sql."
            },
            "can_application_accidentally_read_wrong_db": "No. PlateGirderBridge and OsdagBridge core utilities hardcode their path specifically to the local repository ResourceFiles directory (_DB_PATH). osdag_core uses importlib.resources anchored to the osdag_core namespace in site-packages. The namespaces and paths are completely isolated."
        }
    }

    out_file = r"F:\FOSSEE internship\testing\evidence\phase_1d\task_b_database_audit.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(audit_summary, f, indent=2)

    print(f"Database investigation report saved to: {out_file}")

if __name__ == "__main__":
    main()
