# End-to-End Automation Pipeline

Commit 0048 introduces the main automation entry point:

```powershell
python tools/deep_studio.py <commit_id> [options]
```

## Preview

```powershell
python tools/deep_studio.py 0049 --preview
```

## Generate

```powershell
python tools/deep_studio.py 0049 --generate
```

## Build PDF

```powershell
python tools/deep_studio.py 0049 --build
```

## Commit

```powershell
python tools/deep_studio.py 0049 --commit --message "0049: Continue Volume I manuscript"
```

## Commit, tag and push

```powershell
python tools/deep_studio.py 0049 --commit --message "0049: Continue Volume I manuscript" --tag v0.5.1 --push
```

## Status check

```powershell
python tools/pipeline_status.py
```

## Philosophy

The pipeline is semi-automatic by design.

It should remove repetitive file handling while preserving review, judgement and editorial control.
