# Daily Automation Workflow

This is the recommended workflow once the automation commits are installed.

## 1. Preview

```powershell
python tools/run_commit.py 0054 --preview
```

## 2. Generate

```powershell
python tools/run_commit.py 0054 --generate
```

This writes output into:

```text
generated/commit-0054/
```

## 3. Apply a manifest

When a structured manifest exists:

```powershell
python tools/run_commit.py 0054 --apply-manifest generated/commit-0054/manifest.json
```

## 4. Build the PDF

```powershell
python tools/run_commit.py 0054 --build
```

## 5. Run the quality gate

```powershell
python tools/run_commit.py 0054 --quality-gate
```

## 6. Commit

```powershell
python tools/run_commit.py 0054 --commit --message "0054: Continue Volume I manuscript"
```

## 7. Commit, tag and push

```powershell
python tools/run_commit.py 0054 --commit --message "0054: Continue Volume I manuscript" --tag v0.5.2 --push
```

## Current limitation

The pipeline is now consolidated, but the model output still needs to be reviewed and shaped into a valid manifest. The next practical improvement is to make generated API output produce `manifest.json` directly and reliably.
