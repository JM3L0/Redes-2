#!/bin/bash
# test_reconnection_http3.sh - Baseline de reconexao HTTP/3
# Mede novas conexoes HTTP/3 em processos curl independentes.
# Este teste nao declara 0-RTT: a confirmacao de 0-RTT exige
# instrumentacao de handshake ou cliente que exponha esse evento.
set -e

SERVER_URL="https://server/health"
OUTPUT_DIR="/workspace/data/raw"
CSV_FILE="${OUTPUT_DIR}/http3_reconnection_results.csv"
REPETITIONS=10

mkdir -p "${OUTPUT_DIR}"
echo "protocol,iteration,http_code,time_connect_sec,time_appconnect_sec,time_starttransfer_sec,time_total_sec" > "${CSV_FILE}"

for i in $(seq 1 "${REPETITIONS}"); do
    RES=$(curl -k -s --http3-only --no-keepalive -o /dev/null \
        -w "%{http_code};%{time_connect};%{time_appconnect};%{time_starttransfer};%{time_total}\n" \
        "${SERVER_URL}" || true)

    IFS=';' read -r HTTP_CODE CONNECT APPCONNECT TTFB TOTAL <<< "${RES}"
    if [ "${HTTP_CODE}" != "200" ]; then
        echo "[-] Reconexao ${i}/${REPETITIONS} falhou (HTTP ${HTTP_CODE:-erro})."
        continue
    fi

    echo "http3,${i},${HTTP_CODE},${CONNECT},${APPCONNECT},${TTFB},${TOTAL}" >> "${CSV_FILE}"
done

echo "[OK] Resultados de reconexao HTTP/3 salvos em ${CSV_FILE}"
