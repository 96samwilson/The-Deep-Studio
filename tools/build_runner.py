"""Build runner for The Deep Studio.

Runs the publishing build and records a simple result summary.
"""

from pathlib import Path
import subprocess
import time

def run_build(repo_root="."):
    start=time.time()
    result=subprocess.run(
        ["python","build.py","--all"],
        cwd=repo_root,
        text=True,
        capture_output=True
    )
    duration=round(time.time()-start,2)
    return {
        "success": result.returncode==0,
        "duration_seconds": duration,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }

def write_summary(report, output):
    out=Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        f"# Build Summary\n\n"
        f"- Success: {report['success']}\n"
        f"- Duration: {report['duration_seconds']} seconds\n",
        encoding="utf-8"
    )
