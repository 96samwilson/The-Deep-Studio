# Git Automation

Commit 0045 introduces guarded Git automation.

## Status

```powershell
python tools/commit_workflow.py --status
```

## Commit only

```powershell
python tools/commit_workflow.py --commit-id 0045 --message "0045: Add Git automation"
```

## Commit and tag

```powershell
python tools/commit_workflow.py --commit-id 0045 --message "0045: Add Git automation" --tag v0.5.0-alpha5
```

## Commit, tag and push

```powershell
python tools/commit_workflow.py --commit-id 0045 --message "0045: Add Git automation" --tag v0.5.0-alpha5 --push
```

## Non-interactive mode

Use with care:

```powershell
python tools/commit_workflow.py --commit-id 0045 --message "0045: Add Git automation" --tag v0.5.0-alpha5 --push --yes
```

## Safety principles

- The tool shows `git status` first.
- It asks before staging.
- It asks before committing.
- It asks before tagging.
- It asks before pushing.
- Nothing happens silently unless `--yes` is supplied.
