# Commit 0045 — Git Automation

## Commit message

```text
0045: Add Git automation
```

## Files Added or Updated

- `tools/git_runner.py`
- `tools/commit_workflow.py`
- `docs/GIT_AUTOMATION.md`
- `docs/AUTOMATION_ROADMAP.md`
- `README_AUTOMATION.md`
- `CHANGELOG.md`

## Purpose

This commit adds guarded Git automation so you can stage, commit, tag and push from a controlled command-line workflow.

The system remains semi-automatic:

- shows status first;
- confirms before staging;
- confirms before committing;
- confirms before tagging;
- confirms before pushing.

## Next Commit

Commit 0046 — Interactive review mode.
