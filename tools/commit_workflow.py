"""
Interactive Git workflow for The Deep Studio.

Usage examples:

    python tools/commit_workflow.py --status
    python tools/commit_workflow.py --commit-id 0045 --message "0045: Add Git automation"
    python tools/commit_workflow.py --commit-id 0045 --message "0045: Add Git automation" --tag v0.5.0-alpha5
    python tools/commit_workflow.py --commit-id 0045 --message "0045: Add Git automation" --tag v0.5.0-alpha5 --push

All write operations ask for confirmation unless --yes is supplied.
"""

from __future__ import annotations

from pathlib import Path
import argparse
import sys

from git_runner import status, add_all, commit, tag, push, push_tag


ROOT = Path(__file__).resolve().parent.parent


def confirm(prompt: str, yes: bool = False) -> bool:
    if yes:
        return True
    answer = input(f"{prompt} [y/N] ").strip().lower()
    return answer in {"y", "yes"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run guarded Git operations for The Deep Studio.")
    parser.add_argument("--status", action="store_true", help="Show git status and exit.")
    parser.add_argument("--commit-id", help="Commit ID, e.g. 0045.")
    parser.add_argument("--message", help="Git commit message.")
    parser.add_argument("--tag", help="Optional annotated tag name.")
    parser.add_argument("--tag-message", help="Optional annotated tag message.")
    parser.add_argument("--push", action="store_true", help="Push main branch and tag if provided.")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompts.")
    args = parser.parse_args()

    current_status = status(ROOT)
    print("Git status:")
    print(current_status or "Clean working tree.")

    if args.status:
        return

    if not args.message:
        raise SystemExit("--message is required for commit workflow.")

    if not current_status:
        raise SystemExit("No changes to commit.")

    if not confirm("Stage all changes?", args.yes):
        raise SystemExit("Aborted before staging.")
    print(add_all(ROOT))

    if not confirm(f"Create commit: {args.message!r}?", args.yes):
        raise SystemExit("Aborted before commit.")
    print(commit(ROOT, args.message))

    if args.tag:
        tag_message = args.tag_message or args.message
        if not confirm(f"Create tag {args.tag!r}?", args.yes):
            raise SystemExit("Aborted before tagging.")
        print(tag(ROOT, args.tag, tag_message))

    if args.push:
        if not confirm("Push main branch?", args.yes):
            raise SystemExit("Aborted before push.")
        print(push(ROOT))
        if args.tag:
            if not confirm(f"Push tag {args.tag!r}?", args.yes):
                raise SystemExit("Aborted before tag push.")
            print(push_tag(ROOT, args.tag))


if __name__ == "__main__":
    main()
