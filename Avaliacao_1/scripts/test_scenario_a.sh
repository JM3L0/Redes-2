#!/bin/bash
# ==============================================================================
# test_scenario_a.sh - Bateria Experimental do Cenário A (UDP Puro)
# ==============================================================================
set -e

SERVER_IP="172.28.0.10"
OUTPUT_DIR="/workspace/data/raw"
PCAP_DIR="/workspace/data/pcaps"
CSV_FILE="${OUTPUT_DIR}/scenario_a_results.csv"

mkdir -p "${OUTPUT_DIR}" "${PCAP_DIR}"

# Cabecalho do CSV
echo "scenario,protocol,target_rate_mbps,iteration,duration_sec,bytes_sent,bytes_received,goodput_mbps,jitter_ms,lost_packets,total_packets,loss_percent" > "${CSV_FILE}"

# Configurar canal para Cenario A
/workspace/scripts/setup_netem.sh scenario_a

# Iniciar captura de pcap de amostra com tshark em segundo plano
PCAP_SAMPLE="${PCAP_DIR}/scenario_a_udp_sample.pcapng"
rm -f "${PCAP_SAMPLE}"
echo "[CENARIO A] Iniciando captura de amostra tshark em ${PCAP_SAMPLE}..."
tshark -i eth0 -f "udp port 5201" -w "${PCAP_SAMPLE}" > /dev/null 2>&1 &
TSHARK_PID=$!
sleep 1

RATES=("10M" "50M" "100M" "250M" "500M")
REPETITIONS=10

echo "=========================================================="
echo " [CENARIO A] Iniciando Bateria de Testes UDP (5 taxas x 10 repeticoes)"
echo "=========================================================="

for RATE in "${RATES[@]}"; do
    RATE_NUM=$(echo "${RATE}" | sed 's/M//')
    echo "[*] Testando Taxa de Injecao: ${RATE}bps..."
    
    for i in $(seq 1 ${REPETITIONS}); do
        # Executa iperf3 cliente UDP em formato JSON
        JSON_OUT=$(iperf3 -c "${SERVER_IP}" -u -b "${RATE}" -t 5 -J 2>/dev/null)
        
        # Extrair metricas com jq
        BYTES_SENT=$(echo "${JSON_OUT}" | jq '.end.sum.bytes // 0')
        BYTES_RECV=$(echo "${JSON_OUT}" | jq '.end.sum_received.bytes // 0')
        DURATION=$(echo "${JSON_OUT}" | jq '.end.sum_received.seconds // 5')
        BITS_PER_SEC=$(echo "${JSON_OUT}" | jq '.end.sum_received.bits_per_second // 0')
        GOODPUT_MBPS=$(awk "BEGIN {print ${BITS_PER_SEC} / 1000000}")
        JITTER_MS=$(echo "${JSON_OUT}" | jq '.end.sum_received.jitter_ms // 0')
        LOST_PKTS=$(echo "${JSON_OUT}" | jq '.end.sum_received.lost_packets // 0')
        TOTAL_PKTS=$(echo "${JSON_OUT}" | jq '.end.sum_received.packets // 0')
        LOSS_PCT=$(echo "${JSON_OUT}" | jq '.end.sum_received.lost_percent // 0')
        
        echo "scenario_a,UDP,${RATE_NUM},${i},${DURATION},${BYTES_SENT},${BYTES_RECV},${GOODPUT_MBPS},${JITTER_MS},${LOST_PKTS},${TOTAL_PKTS},${LOSS_PCT}" >> "${CSV_FILE}"
        echo "    -> Repeticao ${i}/${REPETITIONS} (${RATE}): Goodput=${GOODPUT_MBPS} Mbps, Jitter=${JITTER_MS} ms, Perda=${LOSS_PCT}%"
        sleep 0.5
    done
done

# Parar tshark
kill -INT ${TSHARK_PID} 2>/dev/null || true
wait ${TSHARK_PID} 2>/dev/null || true
echo "[CENARIO A] Bateria concluida. Resultados em: ${CSV_FILE}"
