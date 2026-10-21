#!/usr/bin/env bash
# ==============================================================================
# Script de Gerenciamento do Linux Traffic Control (tc netem)
# Disciplina: Redes de Computadores II (UFPI - CSHNB)
# Aluno: João Marcos Sousa Rufino Leal
# ==============================================================================

set -euo pipefail

CONTAINERS=("server_http11" "server_http2_tls" "server_http3_quic")

clean_qdisc() {
    echo "[*] Limpando regras de enfileiramento (qdisc) anteriores em todos os servidores..."
    for c in "${CONTAINERS[@]}"; do
        docker exec --privileged "$c" tc qdisc del dev eth0 root 2>/dev/null || true
    done
    echo "[+] Interfaces restauradas para estado padrão limpo."
}

apply_lan() {
    clean_qdisc
    echo "[*] Aplicando Cenário 1 (LAN): Delay unidirecional 0.5ms (RTT = 1.0ms), Perda = 0%..."
    for c in "${CONTAINERS[@]}"; do
        docker exec --privileged "$c" tc qdisc add dev eth0 root netem delay 0.5ms
        echo "    [✓] $c configurado com delay 0.5ms."
    done
    echo "[+] Cenário 1 (LAN) aplicado com sucesso!"
}

apply_wan() {
    clean_qdisc
    echo "[*] Aplicando Cenário 2 (WAN): Delay unidirecional 25.0ms (RTT = 50.0ms), Perda = 2%..."
    for c in "${CONTAINERS[@]}"; do
        docker exec --privileged "$c" tc qdisc add dev eth0 root netem delay 25ms loss 2%
        echo "    [✓] $c configurado com delay 25ms loss 2%."
    done
    echo "[+] Cenário 2 (WAN) aplicado com sucesso!"
}

show_status() {
    echo "================================================================================"
    echo " STATUS DAS INTERFACES DE REDE (tc qdisc show dev eth0)"
    echo "================================================================================"
    for c in "${CONTAINERS[@]}"; do
        echo -n "[$c] -> "
        docker exec "$c" tc qdisc show dev eth0 || echo "Falha ao obter status"
    done
    echo "================================================================================"
}

case "${1:-status}" in
    lan|cenario1|1)
        apply_lan
        show_status
        ;;
    wan|cenario2|2)
        apply_wan
        show_status
        ;;
    clean|restore|reset)
        clean_qdisc
        show_status
        ;;
    status|show)
        show_status
        ;;
    *)
        echo "Uso: $0 {lan|wan|clean|status}"
        exit 1
        ;;
esac
