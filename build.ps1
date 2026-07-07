param(
    [switch]$All,
    [int]$Chapter
)

Write-Host "Generating book metadata..."
python scripts/generate_toc.py

Write-Host "Preparing SVG assets..."
python scripts/build_diagrams.py

if ($Chapter) {
    python build.py --chapter $Chapter
} else {
    python build.py --all
}
