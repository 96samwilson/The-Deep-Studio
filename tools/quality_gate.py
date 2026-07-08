"""Quality gate for The Deep Studio publishing pipeline.

Evaluates build status and determines whether a commit may proceed.
"""

from pathlib import Path

def evaluate(build_success: bool, expected_files=None):
    expected_files = expected_files or []
    missing = [f for f in expected_files if not Path(f).exists()]
    return {
        "passed": build_success and not missing,
        "missing_files": missing,
        "build_success": build_success,
    }
