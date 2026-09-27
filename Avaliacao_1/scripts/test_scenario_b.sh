#!/bin/bash
# ==============================================================================
# test_scenario_b.sh - Bateria Experimental do Cenario B (TCP Massivo vs QUIC)
# ==============================================================================
set -e

SERVER_URL="https://server"
OUTPUT_DIR="/workspace/data/raw"
PCAP_DIR="/workspace/data/pcaps"
CSV_FILE="${OUTPUT_DIR}/scenario_b_results.csv"

mkdir -p "${OUTPUT_DIR}" "${PCAP_DIR}"

# Cabecalho do CSV
echo "scenario,file_size_label,file_size_bytes,protocol,iteration,dns_time_sec,connect_time_sec,tls_time_sec,ttfb_sec,total_time_sec,speed_download_bps,goodput_mbps,cpu_user_sec,cpu_sys_sec" > "${CSV_FILE}"

# Configurar canal para Cenario B
/workspace/scripts/setup_netem.sh scenario_b

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

        PCAP_SAMPLE="${PCAP_DIR}/scenario_b_${FILE_LABEL}_${PROTO_NAME}.pcapng"
        rm -f "${PCAP_SAMPLE}"
        tshark -i eth0 -s 160 -f "tcp port 443 or udp port 443" -w "${PCAP_SAMPLE}" > /dev/null 2>&1 &
        TSHARK_PID=$!
        for _ in $(seq 1 10); do
            if kill -0 "${TSHARK_PID}" 2>/dev/null; then break; fi
            sleep 0.2
        done

        for i in $(seq 1 ${REPETITIONS}); do
            CPU_STATS_FILE=$(mktemp)
            RES=$(/usr/bin/time -f "%U;%S" -o "${CPU_STATS_FILE}" \
                curl -k -s -o /dev/null -w "${CURL_FORMAT}" ${PROTO} "${SERVER_URL}/${FILE}" || true)
            IFS=';' read -r CPU_USER_SEC CPU_SYS_SEC < "${CPU_STATS_FILE}" || true
            rm -f "${CPU_STATS_FILE}"
            
            IFS=';' read -r HTTP_CODE DNS CONN TLS TTFB TOTAL SPEED SIZE <<< "${RES}"
            
            if [ "${HTTP_CODE}" != "200" ]; then
                echo "      [-] Falha na repeticao ${i}/${REPETITIONS} (HTTP ${HTTP_CODE:-falha_conexao}). Descartando registro."
                continue
            fi

            GOODPUT_MBPS=$(awk "BEGIN {printf \"%.2f\", (${SPEED} * 8) / 1000000}")
            
            echo "scenario_b,${FILE_LABEL},${SIZE},${PROTO_NAME},${i},${DNS},${CONN},${TLS},${TTFB},${TOTAL},${SPEED},${GOODPUT_MBPS},${CPU_USER_SEC:-0},${CPU_SYS_SEC:-0}" >> "${CSV_FILE}"
            echo "      -> Repeticao ${i}/${REPETITIONS}: FCT=${TOTAL}s, Goodput=${GOODPUT_MBPS} Mbps"
            sleep 0.5
        done

        kill -INT "${TSHARK_PID}" 2>/dev/null || true
        wait "${TSHARK_PID}" 2>/dev/null || true
    done
done
echo "[CENARIO B] Bateria concluida. Resultados em: ${CSV_FILE}"
