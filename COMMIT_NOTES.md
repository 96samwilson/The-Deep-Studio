# Commit 0015 — Improved Publishing Pipeline

## Commit message

```text
0015: Improve publishing pipeline
```

## Files Added or Updated

- `book/book.yml`
- `build.py`
- `build.ps1`
- `README_BUILD.md`
- `requirements.txt`
- `CHANGELOG.md`

## Purpose

This commit replaces the minimal PDF exporter with a more structured publishing pipeline.

The new build system introduces:

- a book manifest;
- ordered chapter assembly;
- full-book build mode;
- single-chapter build mode;
- basic Markdown formatting support;
- clearer build instructions.

## Next Commit

Commit 0016 — Integrate SVG diagrams into the build system.
