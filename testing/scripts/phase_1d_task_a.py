import sys
import os
import subprocess
import json
import importlib.metadata
import platform

def resolve_metadata():
    print("=" * 65)
    print("TASK A: RESOLVE ENVIRONMENT & PACKAGE METADATA")
    print("=" * 65)

    py_exe = sys.executable
    py_ver = sys.version
    print(f"Python Executable: {py_exe}")
    print(f"Python Version:    {py_ver}")

    # 1. osdag module
    import osdag
    osdag_dunder = getattr(osdag, "__version__", "Undefined")
    osdag_file = getattr(osdag, "__file__", "Undefined")
    print(f"osdag.__version__: {osdag_dunder}")
    print(f"osdag.__file__:    {osdag_file}")

    # 2. importlib metadata
    try:
        dist_ver = importlib.metadata.version("osdag")
    except Exception as e:
        dist_ver = str(e)
    print(f"importlib.metadata.version('osdag'): {dist_ver}")

    # 3. osdag_core module
    try:
        import osdag_core
        osdag_core_file = getattr(osdag_core, "__file__", None)
        osdag_core_path = getattr(osdag_core, "__path__", None)
        print(f"osdag_core.__file__: {osdag_core_file}")
        print(f"osdag_core.__path__: {list(osdag_core_path) if osdag_core_path else 'None'}")
    except Exception as e:
        print(f"osdag_core import error: {e}")
        osdag_core_file = None
        osdag_core_path = None

    # 4. Conda package list / provenance
    conda_meta = {}
    conda_bat = r"C:\Users\Subodh\miniconda3\condabin\conda.bat"
    try:
        res = subprocess.check_output(
            [conda_bat, "list", "-n", "osdagbridge-py312", "osdag", "--json"],
            text=True
        )
        data = json.loads(res)
        for item in data:
            conda_meta[item["name"]] = item
            print(f"Conda package: {item.get('name')} | Version: {item.get('version')} | Build: {item.get('build_string')} | Channel: {item.get('channel')}")
    except Exception as e:
        print(f"Conda list error: {e}")

    # Save to evidence
    evidence = {
        "python_executable": py_exe,
        "python_version": py_ver,
        "osdag_dunder_version": osdag_dunder,
        "osdag_file": osdag_file,
        "osdag_dist_metadata_version": dist_ver,
        "osdag_core_path": list(osdag_core_path) if osdag_core_path else str(osdag_core_file),
        "conda_packages": conda_meta
    }

    out_file = r"F:\FOSSEE internship\testing\evidence\phase_1d\task_a_metadata.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(evidence, f, indent=2)
    print(f"\nMetadata saved to: {out_file}")

if __name__ == "__main__":
    resolve_metadata()
