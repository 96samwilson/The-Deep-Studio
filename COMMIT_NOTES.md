# Commit 0042 — OpenAI API Integration

## Commit message

```text
0042: Add OpenAI API integration
```

## Files Added or Updated

- `tools/openai_client.py`
- `tools/generate_commit.py`
- `commit_plan.yml`
- `.env.example`
- `requirements.txt`
- `README_AUTOMATION.md`
- `docs/AUTOMATION_ROADMAP.md`
- `docs/API_AUTOMATION_SAFETY.md`
- `.gitignore`
- `CHANGELOG.md`

## Purpose

This commit adds the first real API integration layer for automating future Deep Studio commits.

It supports:

- reading the commit plan;
- selecting a commit by ID;
- building a generation prompt;
- dry-run mode;
- calling the OpenAI Responses API;
- writing raw output to `generated/commit-XXXX/raw-output.md`.

## Next Commit

Commit 0043 — Structured file generation.
