# Automation

The automation system now supports roadmap-derived commit context.

You no longer need every future commit listed in `commit_plan.yml`.

## Preview

```powershell
python tools/run_commit.py 0054 --preview
```

## Generate

```powershell
python tools/run_commit.py 0054 --generate
```

If `0054` is not listed in `commit_plan.yml`, the tool derives its context from the frozen roadmap.

## Frozen roadmap

- 0001–0053 — Foundation & Automation
- 0054–0090 — Volume I — The Listener
- 0091–0130 — Volume II — The Instruments
- 0131–0170 — Volume III — Composition
- 0171–0195 — Volume IV — The Workbook
