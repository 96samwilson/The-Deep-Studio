# Automation

The automation layer now has a primary CLI:

```powershell
python tools/deep_studio.py <commit_id> [options]
```

## Example workflow

Preview the generation prompt:

```powershell
python tools/deep_studio.py 0049 --preview
```

Generate output:

```powershell
python tools/deep_studio.py 0049 --generate
```

Build the book:

```powershell
python tools/deep_studio.py 0049 --build
```

Commit after reviewing files:

```powershell
python tools/deep_studio.py 0049 --commit --message "0049: Continue Volume I manuscript"
```

## Safety

The system remains semi-automatic.

- Preview before generation.
- Review before applying.
- Confirm before Git operations.
- Push only when explicitly requested.
