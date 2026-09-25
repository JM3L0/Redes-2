#!/bin/bash
# ==============================================================================
# test_scenario_b.sh - Bateria Experimental do Cenário B (TCP Massivo vs QUIC)
# ==============================================================================
set -e

SERVER_URL="https://server"
OUTPUT_DIR="/workspace/data/raw"
PCAP_DIR="/workspace/data/pcaps"
CSV_FILE="${OUTPUT_DIR}/scenario_b_results.csv"

mkdir -p "${OUTPUT_DIR}" "${PCAP_DIR}"

# Cabecalho do CSV
echo "scenario,file_size_label,file_size_bytes,protocol,iteration,dns_time_sec,connect_time_sec,tls_time_sec,ttfb_sec,total_time_sec,speed_download_bps,goodput_mbps" > "${CSV_FILE}"

# Configurar canal para Cenario B
/workspace/scripts/setup_netem.sh scenario_b

# Iniciar captura de pcap de amostra
PCAP_SAMPLE="${PCAP_DIR}/scenario_b_sample.pcapng"
rm -f "${PCAP_SAMPLE}"
echo "[CENARIO B] Iniciando captura de amostra tshark em ${PCAP_SAMPLE}..."
tshark -i eth0 -f "tcp port 443 or udp port 443" -w "${PCAP_SAMPLE}" > /dev/null 2>&1 &
TSHARK_PID=$!

# Aguarda confirmacao do processo tshark ativo
for _ in $(seq 1 10); do
    if kill -0 "${TSHARK_PID}" 2>/dev/null; then
        break
    fi
    sleep 0.2
done

FILES=("100MB.bin" "1GB.bin")
PROTOCOLS=("--http1.1" "--http2" "--http3-only")
REPETITIONS=10

echo "=========================================================="
echo " [CENARIO B] Bateria Massiva (100MB e 1GB em H1, H2 e H3 x 10 repeticoes)"
echo "=========================================================="

# Formato customizado incluindo codigo HTTP para validar sucesso
CURL_FORMAT="%{http_code};%{time_namelookup};%{time_connect};%{time_appconnect};%{time_starttransfer};%{time_total};%{speed_download};%{size_download}\n"

for FILE in "${FILES[@]}"; do
    FILE_LABEL="${FILE%.bin}"
    echo "[*] Iniciando testes com arquivo: ${FILE}..."

    for PROTO in "${PROTOCOLS[@]}"; do
        PROTO_NAME="${PROTO#--}"
        PROTO_NAME="${PROTO_NAME%-only}"
        echo "  [+] Protocolo: ${PROTO_NAME}..."

        for i in $(seq 1 ${REPETITIONS}); do
            RES=$(curl -k -s -o /dev/null -w "${CURL_FORMAT}" ${PROTO} "${SERVER_URL}/${FILE}" || true)
            
            IFS=';' read -r HTTP_CODE DNS CONN TLS TTFB TOTAL SPEED SIZE <<< "${RES}"
            
            if [ "${HTTP_CODE}" != "200" ]; then
                echo "      [-] Falha na repeticao ${i}/${REPETITIONS} (HTTP ${HTTP_CODE:-falha_conexao}). Descartando registro."
                continue
            fi

            GOODPUT_MBPS=$(awk "BEGIN {printf \"%.2f\", (${SPEED} * 8) / 1000000}")
            
            echo "scenario_b,${FILE_LABEL},${SIZE},${PROTO_NAME},${i},${DNS},${CONN},${TLS},${TTFB},${TOTAL},${SPEED},${GOODPUT_MBPS}" >> "${CSV_FILE}"
            echo "      -> Repeticao ${i}/${REPETITIONS}: FCT=${TOTAL}s, Goodput=${GOODPUT_MBPS} Mbps"
            sleep 0.5
        done
    done
done

# Parar tshark
kill -INT ${TSHARK_PID} 2>/dev/null || true
wait ${TSHARK_PID} 2>/dev/null || true
echo "[CENARIO B] Bateria concluida. Resultados em: ${CSV_FILE}"
