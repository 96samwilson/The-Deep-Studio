# Automation Roadmap

## 0041 — Automation Foundation

Completed.

- Commit plan introduced
- Basic generator scaffold

## 0042 — OpenAI API Integration

This commit.

- Add OpenAI API client
- Add dry-run mode
- Write raw output to `generated/`
- Update documentation

## 0043 — Structured File Generation

Next.

- Require JSON file manifest output
- Validate file paths
- Validate file contents
- Reject unsafe paths

## 0044 — Repository Writer

- Write generated files directly into the repository
- Preview changes
- Support overwrite protection

## 0045 — Git Automation

- Optional `git add`
- Optional `git commit`
- Optional `git tag`
- Optional `git push`
- Confirmation required

## 0046 — Interactive Review Mode

- Approve file
- Skip file
- Regenerate file
- Edit before commit

## 0047 — Batch Mode

- Generate multiple pending commits
- Stop on validation failure
- Produce summary report

## 0048 — End-to-End Pipeline

- Generate
- Validate
- Review
- Build PDF
- Commit
- Push
