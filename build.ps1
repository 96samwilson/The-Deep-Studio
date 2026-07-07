param(
    [switch]$All,
    [int]$Chapter
)

Write-Host "Building The Deep Studio..."

if ($Chapter) {
    python build.py --chapter $Chapter
}
else {
    python build.py --all
}

if ($LASTEXITCODE -ne 0) {
    Write-Error "Build failed."
    exit $LASTEXITCODE
}

Write-Host "Done."
