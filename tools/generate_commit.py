"""
The Deep Studio — Commit Generator

This version first checks commit_plan.yml. If the requested commit is not
listed there, it derives context from the frozen roadmap in tools/roadmap.py.

Usage:

    python tools/generate_commit.py 0054 --dry-run
    python tools/generate_commit.py 0054
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re

from openai_client import generate_text
from roadmap import get_commit_context, commit_block_as_text


ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "commit_plan.yml"
GENERATED = ROOT / "generated"


def load_plan_text() -> str:
    if not PLAN.exists():
        return ""
    return PLAN.read_text(encoding="utf-8")


def find_commit_block(plan_text: str, commit_id: str) -> str:
    """
    Look for an explicit commit entry in commit_plan.yml.
    If missing, derive the context from the frozen roadmap.
    """
    if plan_text:
        pattern = rf"(?ms)^\s*-\s+id:\s*[\"']?{re.escape(commit_id)}[\"']?.*?(?=^\s*-\s+id:|\Z)"
        match = re.search(pattern, plan_text)
        if match:
            return match.group(0).strip()

    context = get_commit_context(commit_id)
    return commit_block_as_text(context)


def build_prompt(commit_id: str, commit_block: str) -> str:
    return f"""
You are generating files for The Deep Studio repository.

Commit ID: {commit_id}

Commit context:

{commit_block}

Return a clear Markdown response describing the files that should be created.
Do not invent unrelated scope.
Preserve the project's editorial standards:
- British English
- Markdown-first
- SVG diagrams when requested
- Commit metadata
- No filler
- Stay within the frozen roadmap through Commit 0195
""".strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Deep Studio commit using the OpenAI API.")
    parser.add_argument("commit_id", help="Commit ID, e.g. 0054")
    parser.add_argument("--dry-run", action="store_true", help="Do not call the API; write the prompt preview instead.")
    args = parser.parse_args()

    plan_text = load_plan_text()
    commit_block = find_commit_block(plan_text, args.commit_id)
    prompt = build_prompt(args.commit_id, commit_block)

    output = generate_text(prompt, dry_run=args.dry_run)

    out_dir = GENERATED / f"commit-{args.commit_id}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "raw-output.md"
    out_file.write_text(output, encoding="utf-8")

    print(f"Wrote {out_file}")


if __name__ == "__main__":
    main()
