param(
    [string]$Compiler = 'tectonic',
    [string]$Python = 'python',
    [switch]$Final
)
$ErrorActionPreference = 'Stop'
$paperRoot = $PSScriptRoot
$repoRoot = Split-Path -Parent $paperRoot
$buildRoot = Join-Path $paperRoot 'build'
New-Item -ItemType Directory -Force -Path $buildRoot | Out-Null
Push-Location $repoRoot
try {
    & $Python -m src.check_paper
    if ($LASTEXITCODE -ne 0) { throw 'Paper source validation failed' }
    Push-Location $paperRoot
    try {
        & $Compiler --keep-logs --outdir $buildRoot main.tex
        if ($LASTEXITCODE -ne 0) { throw 'LaTeX compilation failed' }
    } finally { Pop-Location }
    if ($Final) {
        & $Python -m src.check_paper --final --pdf (Join-Path $buildRoot 'main.pdf')
        if ($LASTEXITCODE -ne 0) { throw 'Final paper validation failed' }
    }
    Write-Output "Compiled PDF: $(Join-Path $buildRoot 'main.pdf')"
} finally { Pop-Location }
