# ==============================================================================
# run_experiments.ps1 - Ponto de Entrada para PowerShell no Windows
# ==============================================================================
# Executa a orquestracao automatizada via Docker Compose no Windows
# ==============================================================================
$ErrorActionPreference = "Stop"

$RootDir = $PSScriptRoot
$ComposeFile = Join-Path $RootDir "docker\docker-compose.yml"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  AVALIACAO 1 - REDES DE COMPUTADORES II (UFPI - 2026-2)" -ForegroundColor Cyan
Write-Host "  Orquestracao Automatizada de Ensaios (TCP vs UDP vs QUIC)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# 1. Gerar cargas estaticas se ausentes
$Static100MB = Join-Path $RootDir "data\static\100MB.bin"
$Static1GB = Join-Path $RootDir "data\static\1GB.bin"
if (-not (Test-Path $Static100MB) -or -not (Test-Path $Static1GB)) {
    Write-Host "[*] Gerando cargas estaticas sinteticas..." -ForegroundColor Yellow
    python (Join-Path $RootDir "scripts\generate_static_data.py")
}

# 2. Subir o ambiente Docker
Write-Host "[*] Subindo infraestrutura via Docker Compose..." -ForegroundColor Green
docker compose -f $ComposeFile up -d --build

# 3. Aguardar o servidor
Write-Host "[*] Aguardando prontidao do redes2_server..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# 4. Disparar os testes dentro do container
Write-Host "[*] Disparando baterias experimentais no redes2_client..." -ForegroundColor Green
docker exec redes2_client /workspace/scripts/run_experiments.sh

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  EXPERIMENTOS CONCLUIDOS COM SUCESSO!" -ForegroundColor Green
Write-Host "  Resultados disponiveis em data/ (raw, pcaps, processed, plots)" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
