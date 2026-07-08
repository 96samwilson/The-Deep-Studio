"""
The Deep Studio — End-to-End Automation CLI

This is the main automation entry point.

Current workflow:

    python tools/deep_studio.py 0049 --preview
    python tools/deep_studio.py 0049 --generate
    python tools/deep_studio.py 0049 --apply
    python tools/deep_studio.py 0049 --build
    python tools/deep_studio.py 0049 --commit --tag v0.5.1

The tool remains deliberately semi-automatic. Review and explicit user action
are required before repository writes and Git operations.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent


def run(command: list[str]) -> int:
    print(" ".join(command))
    return subprocess.call(command, cwd=ROOT)


def main() -> None:
    parser = argparse.ArgumentParser(description="The Deep Studio automation tool.")
    parser.add_argument("commit_id", help="Commit ID, e.g. 0049")
    parser.add_argument("--preview", action="store_true", help="Preview the planned generation prompt.")
    parser.add_argument("--generate", action="store_true", help="Generate raw model output.")
    parser.add_argument("--apply", action="store_true", help="Apply approved structured files to the repository.")
    parser.add_argument("--build", action="store_true", help="Build the current PDF draft.")
    parser.add_argument("--commit", action="store_true", help="Run guarded Git commit workflow.")
    parser.add_argument("--message", help="Commit message for Git workflow.")
    parser.add_argument("--tag", help="Optional Git tag.")
    parser.add_argument("--push", action="store_true", help="Push after commit.")
    args = parser.parse_args()

    if args.preview:
        return_code = run([sys.executable, "tools/generate_commit.py", args.commit_id, "--dry-run"])
        if return_code:
            raise SystemExit(return_code)

    if args.generate:
        return_code = run([sys.executable, "tools/generate_commit.py", args.commit_id])
        if return_code:
            raise SystemExit(return_code)

    if args.apply:
        print("Apply mode is reserved for structured manifests after review.")
        print("Use the repository writer once Commit 0049 connects manifest application.")

    if args.build:
        return_code = run([sys.executable, "build.py", "--all"])
        if return_code:
            raise SystemExit(return_code)

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
        return_code = run(command)
        if return_code:
            raise SystemExit(return_code)

    if not any([args.preview, args.generate, args.apply, args.build, args.commit]):
        print("No action selected. Use --preview, --generate, --apply, --build or --commit.")


if __name__ == "__main__":
    main()
