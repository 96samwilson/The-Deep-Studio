# Automation

The Deep Studio automation system is designed to reduce manual repetition while keeping editorial control.

## Current stages

1. `commit_plan.yml` defines upcoming work.
2. `tools/generate_commit.py` prepares model output.
3. `tools/file_manifest.py` validates structured file manifests.
4. `tools/repository_writer.py` writes approved files into the repository.
5. `tools/commit_workflow.py` performs guarded Git operations.

## Git workflow

After applying generated files, run:

```powershell
python tools/commit_workflow.py --status
```

Then commit:

```powershell
python tools/commit_workflow.py --commit-id 0045 --message "0045: Add Git automation"
```

Optionally tag and push:

```powershell
python tools/commit_workflow.py --commit-id 0045 --message "0045: Add Git automation" --tag v0.5.0-alpha5 --push
```

The workflow remains semi-automatic by design. Review comes before commit.
