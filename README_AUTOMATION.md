# Automation

Commit 0052 introduces a quality gate.

Example:

```powershell
python tools/quality_gate_cli.py --build-success --expect exports/pdf/The-Deep-Studio-Draft.pdf
```

A non-zero exit code indicates the pipeline should stop before committing.
