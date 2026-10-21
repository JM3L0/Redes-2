<#
.SYNOPSIS
    Orquestrador Mestre 1-Click de Experimentos Web (Windows PowerShell).
.DESCRIPTION
    Executa de ponta a ponta a avaliação experimental dos protocolos Web
    (HTTP/1.1 vs HTTPS/TLS 1.3 vs HTTP/3-QUIC):
    1. Verifica e gera certificados TLS 1.3 e payloads sintéticos (50MB e 100x10KB);
    2. Sobe os 3 contêineres Docker isolados via docker-compose;
    3. Aplica o Cenário 1 (LAN: delay 0.5ms = RTT 1ms, perda 0%) via tc netem;
    4. Executa os testes de LAN: T01, T02, T03 (Carga A) e T07, T08, T09 (Carga B);
    5. Aplica o Cenário 2 (WAN: delay 25ms = RTT 50ms, perda 2%) via tc netem;
    6. Executa os testes de WAN: T04, T05, T06 (Carga A) e T10, T11, T12 (Carga B);
    7. Restaura as interfaces e limpa as disciplinas tc netem;
    8. Executa o pipeline estatístico (process_data.py) e de gráficos científicos (plot_results.py);
    9. Encerra os contêineres Docker de forma limpa.
.PARAMETER Iterations
    Número de repetições por teste (padrão do edital: 10).
.PARAMETER KeepAlive
    Mantém os contêineres em execução após a conclusão dos testes.
.PARAMETER Quick
    Executa 2 iterações para validação rápida de pipeline.
#>

[CmdletBinding()]
param (
    [int]$Iterations = 10,
    [switch]$KeepAlive,
    [switch]$Quick
)

$ErrorActionPreference = "Stop"

if ($Quick) {
    $Iterations = 2
}

$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $baseDir

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "   ORQUESTRADOR MESTRE DE EXPERIMENTOS DE REDES II (UFPI - CSHNB)             " -ForegroundColor Cyan
Write-Host "   Estudo Experimental: HTTP/1.1 vs HTTPS/TLS 1.3 vs HTTP/3-QUIC              " -ForegroundColor Cyan
Write-Host "   Aluno: João Marcos Sousa Rufino Leal                                       " -ForegroundColor Cyan
Write-Host "   Iterações por teste: $Iterations ($([math]::Max($Iterations, 10)) no edital)" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

# 1. Determina porta para HTTP/1.1 (8080 padrão ou 8081 se ocupada)
$http1Port = 8080
$occupied = Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue
if ($occupied) {
    Write-Host "[!] Porta 8080 ocupada no Host por outro processo. Usando fallback automático: 8081." -ForegroundColor Yellow
    $http1Port = 8081
}
$env:HTTP1_PORT = "$http1Port"

# 2. Gera certificados TLS se ausentes
if (-not (Test-Path "docker\certs\cert.pem") -or -not (Test-Path "docker\certs\key.pem")) {
    Write-Host "[*] Gerando certificados TLS 1.3 com SANs..." -ForegroundColor Cyan
    python scripts\generate_certs.py
}

# 3. Gera payloads sintéticos se ausentes
if (-not (Test-Path "data\static\50MB.bin") -or -not (Test-Path "data\static\objects\obj_100.bin")) {
    Write-Host "[*] Gerando payloads sintéticos (50MB e 100x10KB)..." -ForegroundColor Cyan
    python scripts\generate_payloads.py
}

# 4. Sobe contêineres Docker
Write-Host "[*] Iniciando infraestrutura Docker Compose..." -ForegroundColor Cyan
docker compose -f docker\docker-compose.yml up -d

# Garante presença do pacote iproute2 nos contêineres Alpine
$containers = @("server_http11", "server_http2_tls", "server_http3_quic")
foreach ($c in $containers) {
    docker exec $c which tc 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[*] Instalando iproute2 em $c..." -ForegroundColor Gray
        docker exec $c apk add --no-cache iproute2 | Out-Null
    }
}

try {
    # 5. CENÁRIO 1: REDE LOCAL (LAN) - RTT 1ms, 0% perda
    Write-Host "`n================================================================================" -ForegroundColor Green
    Write-Host " ETAPA 1/2: CENÁRIO 1 (LAN) - RTT 1.0ms, Perda 0.0%" -ForegroundColor Green
    Write-Host "================================================================================" -ForegroundColor Green
    & ".\scripts\setup_netem.ps1" lan

    Write-Host "[*] Executando testes T01 a T03 (Carga A) e T07 a T09 (Carga B)..." -ForegroundColor Cyan
    python benchmark\client.py --scenario lan --iterations $Iterations --http1-port $http1Port

    # 6. CENÁRIO 2: REDE GEOGRÁFICA (WAN) - RTT 50ms, 2% perda
    Write-Host "`n================================================================================" -ForegroundColor Magenta
    Write-Host " ETAPA 2/2: CENÁRIO 2 (WAN) - RTT 50.0ms, Perda 2.0%" -ForegroundColor Magenta
    Write-Host "================================================================================" -ForegroundColor Magenta
    & ".\scripts\setup_netem.ps1" wan

    Write-Host "[*] Executando testes T04 a T06 (Carga A) e T10 a T12 (Carga B)..." -ForegroundColor Cyan
    python benchmark\client.py --scenario wan --iterations $Iterations --http1-port $http1Port

    # 7. Limpeza do tc netem
    Write-Host "`n[*] Restaurando interfaces virtuais (remoção de regras netem)..." -ForegroundColor Cyan
    & ".\scripts\setup_netem.ps1" clean

    # 8. Pipeline de Análise Estatística e Visualização Gráfica
    Write-Host "`n================================================================================" -ForegroundColor Yellow
    Write-Host " CONSOLIDAÇÃO ESTATÍSTICA E GERAÇÃO DE FIGURAS CIENTÍFICAS" -ForegroundColor Yellow
    Write-Host "================================================================================" -ForegroundColor Yellow
    python analysis\process_data.py
    python analysis\plot_results.py

} finally {
    # 9. Encerramento limpo
    if ($KeepAlive) {
        Write-Host "`n[!] Flag -KeepAlive ativa: mantendo contêineres Docker em execução." -ForegroundColor Yellow
    } else {
        Write-Host "`n[*] Encerrando contêineres Docker de forma limpa (docker compose down)..." -ForegroundColor Cyan
        docker compose -f docker\docker-compose.yml down
        Write-Host "[+] Ambiente Docker encerrado com sucesso." -ForegroundColor Green
    }
}

Write-Host "`n================================================================================" -ForegroundColor Green
Write-Host "   TODOS OS EXPERIMENTOS FORAM CONCLUÍDOS COM SUCESSO!                          " -ForegroundColor Green
Write-Host "   Dados Brutos:    data\raw\results.json & results.csv                         " -ForegroundColor Green
Write-Host "   Tabelas Finais:  data\processed\summary_table.csv & summary_table.tex        " -ForegroundColor Green
Write-Host "   Gráficos:        data\plots\ (5 figuras com barras de erro obrigatórias)     " -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
