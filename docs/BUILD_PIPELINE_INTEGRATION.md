# Build Pipeline Integration

Commit 0039 connects several previously scaffolded systems directly into `build.py`.

## Integrated

- Improved typography
- Markdown table rendering
- Callout block rendering
- Pull quote rendering

## Test

Run:

```powershell
python build.py --chapter 1
```

Then inspect:

```text
exports/pdf/chapter-01-listening-before-equipment.pdf
```

Tables should no longer appear as ASCII text.
Callouts should appear as styled boxes.
Pull quotes should appear as highlighted quotation panels.
