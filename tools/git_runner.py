"""
Git automation helpers.

This module provides guarded wrappers around common Git operations.
It does not push or commit unless explicitly called by the user-facing tool.
"""

from __future__ import annotations

from pathlib import Path
import subprocess


def run_git(repo_root: str | Path, args: list[str]) -> str:
    repo = Path(repo_root)
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed:\n{output}")
    return output.strip()


def status(repo_root: str | Path) -> str:
    return run_git(repo_root, ["status", "--short"])


def add_all(repo_root: str | Path) -> str:
    return run_git(repo_root, ["add", "."])


def commit(repo_root: str | Path, message: str) -> str:
    return run_git(repo_root, ["commit", "-m", message])


def tag(repo_root: str | Path, tag_name: str, message: str) -> str:
    return run_git(repo_root, ["tag", "-a", tag_name, "-m", message])


def push(repo_root: str | Path, remote: str = "origin", branch: str = "main") -> str:
    return run_git(repo_root, ["push", remote, branch])


def push_tag(repo_root: str | Path, tag_name: str, remote: str = "origin") -> str:
    return run_git(repo_root, ["push", remote, tag_name])
