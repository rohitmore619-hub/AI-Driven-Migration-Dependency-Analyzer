import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

scripts = [
    "blast_radius_score.py",
    "decision_engine.py",
    "recommendation_engine.py",
    "code_analysis_engine.py",
    "sca_engine.py",
    "report_generator.py",
    "notepad_dashboard.py"
]

for script in scripts:
    script_path = os.path.join(BASE_DIR, script)

    if not os.path.exists(script_path):
        print(f"[SKIP] {script} not found")
        continue

    print(f"\n[RUNNING] {script}")

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"[SUCCESS] {script}")
        print(result.stdout)

    else:
        print(f"[FAILED] {script}")
        print(result.stderr)
        break

print("\nPipeline execution completed.")