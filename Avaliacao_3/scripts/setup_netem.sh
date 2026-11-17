#!/usr/bin/env bash
# ==============================================================================
# Emulação de Rede com Linux Traffic Control (tc netem) — 3ª Avaliação (N3)
# ==============================================================================
set -euo pipefail

MODE="${1:-clean}"

clean_netem() {
    echo "[*] Limpando regras tc netem das interfaces eth0..."
    docker exec --privileged server_tcp_cc tc qdisc del dev eth0 root 2>/dev/null || true
    docker exec --privileged server_http3_quic tc qdisc del dev eth0 root 2>/dev/null || true
    docker exec --privileged client_bench tc qdisc del dev eth0 root 2>/dev/null || true
}

case "$MODE" in
    lan|1)
        clean_netem
        echo "[*] Aplicando Cenário 1 (LAN - Canal Ideal: delay 0.5ms -> RTT total = 1 ms, 0% perda)..."
        docker exec --privileged server_tcp_cc tc qdisc add dev eth0 root netem delay 0.5ms
        docker exec --privileged server_http3_quic tc qdisc add dev eth0 root netem delay 0.5ms
        docker exec --privileged client_bench tc qdisc add dev eth0 root netem delay 0.5ms
        ;;
    wan_loss|wan|2)
        clean_netem
        echo "[*] Aplicando Cenário 2 (WAN - Canal Degradado: delay 25ms loss 2% -> RTT total = 50 ms, 2% perda)..."
        docker exec --privileged server_tcp_cc tc qdisc add dev eth0 root netem delay 25ms loss 2%
        docker exec --privileged server_http3_quic tc qdisc add dev eth0 root netem delay 25ms loss 2%
        docker exec --privileged client_bench tc qdisc add dev eth0 root netem delay 25ms loss 2%
        ;;
    wan_noloss|handshake|3)
        clean_netem
        echo "[*] Aplicando Cenário 3 (WAN sem Perda - Isolamento Handshake: delay 25ms -> RTT total = 50 ms, 0% perda)..."
        docker exec --privileged server_http3_quic tc qdisc add dev eth0 root netem delay 25ms
        docker exec --privileged client_bench tc qdisc add dev eth0 root netem delay 25ms
        ;;
    clean|clear|del)
        clean_netem
        ;;
    *)
        echo "Uso: $0 {lan|wan_loss|wan_noloss|clean}"
        exit 1
        ;;
esac
