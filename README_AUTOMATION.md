# Automation

The goal is to reduce the manual ZIP workflow and eventually generate repository commits locally.

## Current capability

Commit 0042 introduces:

- OpenAI API client scaffold
- `commit_plan.yml`
- dry-run mode
- raw output generation
- generated output folder

## Setup

From the repository root:

```powershell
pip install -r requirements.txt
```

Set your API key:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

Or copy `.env.example` to `.env` and manage the variable with your preferred environment loader.

## Dry run

```powershell
python tools/generate_commit.py 0042 --dry-run
```

This writes a preview to:

```text
generated/commit-0042/raw-output.md
```

## Real API call

```powershell
python tools/generate_commit.py 0042
```

This will call the OpenAI API and write the raw model output to:

```text
generated/commit-0042/raw-output.md
```

## Important

This stage does **not** automatically write generated files into the repository or run Git commands.

That is intentional.

The next automation stages add structure, safety checks, and review mode before any automatic commits are allowed.
