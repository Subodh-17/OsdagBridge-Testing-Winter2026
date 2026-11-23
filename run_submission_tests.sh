#!/usr/bin/env bash
# OsdagBridge screening task: verification suites (Linux/macOS).
# Steps 1-5 need only: pip install -r testing/requirements-tests.txt
# Step 6 (full pipeline) also needs the conda environment from source/OsdagBridge/environment.yml.
set -u
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
fail=0
run() { echo; echo "== $1"; shift; "$@" || fail=1; }
run "[1/6] Evidence governance (27 tests; 3 are Windows-only and skip elsewhere)" "$PY" testing/test_cases/baseline_regression/test_evidence_governance.py
run "[2/6] Batch 2 - FE load conservation (17)" "$PY" -m unittest testing/test_cases/phase_3/test_batch_2_comprehensive.py
run "[3/6] Batch 2 - line / patch load detail (11 + 5)" "$PY" -m unittest testing/test_cases/phase_3/test_batch_2_line_loads.py testing/test_cases/phase_3/test_batch_2_patch_loads.py
run "[4/6] Batch 3 - load factor scaling (15)" "$PY" -m unittest testing/test_cases/phase_3/test_batch_3_factor_scaling.py
run "[5/6] Moving-load mesh mapping, bbfe14c (10)" "$PY" -m unittest testing/test_cases/phase_3/test_moving_load_mesh_mapping.py
if "$PY" -c "import PySide6, osdag_core" >/dev/null 2>&1; then
  run "[6/6] Full-pipeline live-load conservation (3)" "$PY" -m unittest testing/test_cases/phase_3/test_full_pipeline_live_load_conservation.py
else
  echo; echo "== [6/6] Full-pipeline suite SKIPPED: needs the conda environment (PySide6 + osdag). See README."
fi
echo
if [ $fail -eq 0 ]; then echo "All suites passed."; else echo "At least one suite failed - see output above."; fi
exit $fail
