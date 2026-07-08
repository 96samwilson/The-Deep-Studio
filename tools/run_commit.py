"""
The Deep Studio — Consolidated Commit Runner

This is the recommended daily automation command.

It coordinates:
- preview
- generation
- manifest application
- PDF build
- quality gate
- release report
- optional guarded Git workflow

The command remains semi-automatic by design.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
from datetime import datetime


ROOT = Path(__file__).resolve().parent.parent
GENERATED = ROOT / "generated"


def run(command: list[str], allow_fail: bool = False) -> int:
    print("\n> " + " ".join(command))
    result = subprocess.call(command, cwd=ROOT)
    if result != 0 and not allow_fail:
        raise SystemExit(result)
    return result


def write_release_report(commit_id: str, build_ok: bool, quality_ok: bool) -> Path:
    out_dir = GENERATED / f"commit-{commit_id}"
    out_dir.mkdir(parents=True, exist_ok=True)
    report = out_dir / "release-report.md"
    report.write_text(
        f"""# Commit {commit_id} Release Report

Generated: {datetime.utcnow().isoformat()}Z

## Status

| Stage | Result |
|---|---|
| Build | {"PASS" if build_ok else "FAIL"} |
| Quality Gate | {"PASS" if quality_ok else "FAIL"} |

## Next Step

If all checks pass, review the repository changes and run the guarded Git workflow.

""",
        encoding="utf-8",
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run The Deep Studio commit pipeline.")
    parser.add_argument("commit_id", help="Commit ID, e.g. 0054")
    parser.add_argument("--preview", action="store_true", help="Preview the prompt only.")
    parser.add_argument("--generate", action="store_true", help="Generate raw API output.")
    parser.add_argument("--apply-manifest", help="Path to structured manifest JSON to apply.")
    parser.add_argument("--build", action="store_true", help="Build the PDF.")
    parser.add_argument("--quality-gate", action="store_true", help="Run the quality gate.")
    parser.add_argument("--commit", action="store_true", help="Run guarded Git workflow.")
    parser.add_argument("--message", help="Git commit message.")
    parser.add_argument("--tag", help="Optional Git tag.")
    parser.add_argument("--push", action="store_true", help="Push after commit.")
    args = parser.parse_args()

    build_ok = False
    quality_ok = False

    if args.preview:
        run([sys.executable, "tools/generate_commit.py", args.commit_id, "--dry-run"])

    if args.generate:
        run([sys.executable, "tools/generate_commit.py", args.commit_id])

    if args.apply_manifest:
        run([sys.executable, "tools/apply_cli.py", args.apply_manifest, "--apply"])

    if args.build:
        build_code = run([sys.executable, "tools/build_cli.py"], allow_fail=True)
        build_ok = build_code == 0
        if not build_ok:
            print("Build failed. Stop and inspect generated/build-summary.md.")
            raise SystemExit(build_code)

    if args.quality_gate:
        quality_code = run([
            sys.executable,
            "tools/quality_gate_cli.py",
            "--build-success",
            "--expect",
            "exports/pdf/The-Deep-Studio-Draft.pdf",
        ], allow_fail=True)
        quality_ok = quality_code == 0
        if not quality_ok:
            print("Quality gate failed. Do not commit until fixed.")
            raise SystemExit(quality_code)

    report = write_release_report(args.commit_id, build_ok, quality_ok)
    print(f"\nRelease report written: {report}")

    if args.commit:
        if not args.message:
            raise SystemExit("--message is required with --commit")
        command = [
            sys.executable,
            "tools/commit_workflow.py",
            "--commit-id", args.commit_id,
            "--message", args.message,
        ]
        if args.tag:
            command.extend(["--tag", args.tag])
        if args.push:
            command.append("--push")
        run(command)


if __name__ == "__main__":
    main()
