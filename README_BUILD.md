# Building The Deep Studio

Run all commands from the repository root.

## Install dependencies

```powershell
pip install -r requirements.txt
```

## Build the full draft

```powershell
python build.py --all
```

or:

```powershell
.\build.ps1 -All
```

Output:

```text
exports/pdf/The-Deep-Studio-Draft.pdf
```

## Build Chapter 1 only

```powershell
python build.py --chapter 1
```

or:

```powershell
.\build.ps1 -Chapter 1
```

Output:

```text
exports/pdf/chapter-01-listening-before-equipment.pdf
```

## Build manifest

The build order is controlled by:

```text
book/book.yml
```

Add new chapters there when they are ready to be included in the generated PDF.
