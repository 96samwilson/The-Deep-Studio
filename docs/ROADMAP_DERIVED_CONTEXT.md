# Roadmap-Derived Commit Context

This upgrade means `commit_plan.yml` no longer needs to contain every future commit.

If a commit exists in `commit_plan.yml`, the explicit entry is used.

If it does not exist, the tooling derives the correct context from the frozen roadmap:

| Range | Context |
|---|---|
| 0001–0053 | Foundation & Automation |
| 0054–0090 | Volume I — The Listener |
| 0091–0130 | Volume II — The Instruments |
| 0131–0170 | Volume III — Composition |
| 0171–0195 | Volume IV — The Workbook |

Commits outside `0001–0195` are rejected.
