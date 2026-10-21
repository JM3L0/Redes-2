<#
.SYNOPSIS
    Script de Gerenciamento do Linux Traffic Control (tc netem) para Windows PowerShell.
.DESCRIPTION
    Aplica as regras de atraso e perda nos contêineres Docker do benchmark.
    Cenário 1 (LAN): delay 0.5ms (RTT = 1.0ms), perda 0%
    Cenário 2 (WAN): delay 25ms (RTT = 50.0ms), perda 2%
#>

param (
    [Parameter(Position=0)]
    [ValidateSet("lan", "wan", "clean", "status")]
    [string]$Action = "status"
)

$containers = @("server_http11", "server_http2_tls", "server_http3_quic")

function Clean-Qdisc {
    Write-Host "[*] Limpando regras de enfileiramento (qdisc) anteriores em todos os servidores..." -ForegroundColor Cyan
    foreach ($c in $containers) {
        docker exec --privileged $c tc qdisc del dev eth0 root 2>$null
    }
    Write-Host "[+] Interfaces restauradas para estado padrão limpo." -ForegroundColor Green
}

function Apply-Lan {
    Clean-Qdisc
    Write-Host "[*] Aplicando Cenário 1 (LAN): Delay 0.5ms (RTT 1.0ms), Perda 0%..." -ForegroundColor Cyan
    foreach ($c in $containers) {
        docker exec --privileged $c tc qdisc add dev eth0 root netem delay 0.5ms
        Write-Host "    [OK] $c configurado com delay 0.5ms." -ForegroundColor Gray
    }
    Write-Host "[+] Cenário 1 (LAN) aplicado com sucesso!" -ForegroundColor Green
}

function Apply-Wan {
    Clean-Qdisc
    Write-Host "[*] Aplicando Cenário 2 (WAN): Delay 25ms (RTT 50.0ms), Perda 2%..." -ForegroundColor Cyan
    foreach ($c in $containers) {
        docker exec --privileged $c tc qdisc add dev eth0 root netem delay 25ms loss 2%
        Write-Host "    [OK] $c configurado com delay 25ms loss 2%." -ForegroundColor Gray
    }
    Write-Host "[+] Cenário 2 (WAN) aplicado com sucesso!" -ForegroundColor Green
}

function Show-Status {
    Write-Host "================================================================================" -ForegroundColor Yellow
    Write-Host " STATUS DAS INTERFACES DE REDE (tc qdisc show dev eth0)" -ForegroundColor Yellow
    Write-Host "================================================================================" -ForegroundColor Yellow
    foreach ($c in $containers) {
        Write-Host "[$c] -> " -NoNewline -ForegroundColor White
        docker exec $c tc qdisc show dev eth0
    }
    Write-Host "================================================================================" -ForegroundColor Yellow
}

switch ($Action.ToLower()) {
    "lan"   { Apply-Lan; Show-Status }
    "wan"   { Apply-Wan; Show-Status }
    "clean" { Clean-Qdisc; Show-Status }
    "status" { Show-Status }
}
