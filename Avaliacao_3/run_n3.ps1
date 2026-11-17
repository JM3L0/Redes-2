<#
.SYNOPSIS
Orquestrador Mestre 1-Click (run_n3.ps1) — 3ª Avaliação (N3) Redes de Computadores II (UFPI).
#>
param(
    [int]$Repetitions = 5,
    [int]$Duration = 15
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
python "$PSScriptRoot\run_n3.py" --repetitions $Repetitions --duration $Duration
