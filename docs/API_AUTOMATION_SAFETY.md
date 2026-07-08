# API Automation Safety

The automation system should remain semi-automatic until it is proven reliable.

## Rules

1. Do not auto-commit without explicit confirmation.
2. Do not write files outside the repository root.
3. Do not overwrite existing files unless the commit plan expects it.
4. Do not push automatically unless requested.
5. Always allow dry-run mode.
6. Always keep generated output inspectable before applying it.

## Recommended workflow

```powershell
python tools/generate_commit.py 0043 --dry-run
python tools/generate_commit.py 0043
# inspect generated output
# apply files only after review
```
