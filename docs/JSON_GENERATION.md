# JSON Generation

Commit 0049 changes the automation strategy.

Instead of requesting Markdown descriptions, the model should return
only JSON describing repository files.

This allows deterministic validation before any file is written.
