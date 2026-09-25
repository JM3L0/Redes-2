#!/bin/bash
# ==============================================================================
# test_scenario_c.sh - Bateria Experimental do Cenário C (QUIC & HoL Blocking)
# ==============================================================================
set -e

SERVER_URL="https://server/objects"
OUTPUT_DIR="/workspace/data/raw"
PCAP_DIR="/workspace/data/pcaps"
CSV_FILE="${OUTPUT_DIR}/scenario_c_results.csv"

mkdir -p "${OUTPUT_DIR}" "${PCAP_DIR}"

# Cabecalho do CSV
echo "scenario,loss_percent,protocol,iteration,total_batch_fct_sec,total_bytes_downloaded,goodput_mbps" > "${CSV_FILE}"

LOSS_SCENARIOS=("scenario_c_loss0" "scenario_c_loss2" "scenario_c_loss5")
PROTOCOLS=("--http1.1" "--http2" "--http3-only")
REPETITIONS=10

echo "=========================================================="
echo " [CENARIO C] Bateria Web Concorrente (100 objetos x 3 perdas x 3 protos x 10 reps)"
echo "=========================================================="

for SCENARIO in "${LOSS_SCENARIOS[@]}"; do
    case "${SCENARIO}" in
        scenario_c_loss0) LOSS_LABEL="0" ;;
        scenario_c_loss2) LOSS_LABEL="2" ;;
        scenario_c_loss5) LOSS_LABEL="5" ;;
    esac

    echo "[*] Configurando canal para: ${SCENARIO} (Perda = ${LOSS_LABEL}%)..."
    /workspace/scripts/setup_netem.sh "${SCENARIO}"

    for PROTO in "${PROTOCOLS[@]}"; do
        PROTO_NAME=$(echo "${PROTO}" | sed 's/--//; s/-only//')
        echo "  [+] Avaliando: ${PROTO_NAME} com ${LOSS_LABEL}% de perda..."

        for i in $(seq 1 ${REPETITIONS}); do
            START_TIME=$(date +%s.%N)
            
            # Baixar os 100 objetos usando curl
            # Para medir o tempo do lote completo sob o protocolo especificado:
            # Geramos a lista de URLs
            URL_LIST=()
            for obj in $(seq -w 1 100); do
                URL_LIST+=("${SERVER_URL}/obj_${obj}.bin")
            done

            # Executa o download de todos os 100 objetos
            curl -k -s -o /dev/null ${PROTO} "${URL_LIST[@]}"
            
            END_TIME=$(date +%s.%N)
            BATCH_FCT=$(awk "BEGIN {print ${END_TIME} - ${START_TIME}}")
            
            # 100 objetos de 50 KB = 5,000 KB = 5,120,000 bytes = 40,960,000 bits
            TOTAL_BYTES=5120000
            GOODPUT_MBPS=$(awk "BEGIN {print (${TOTAL_BYTES} * 8) / (${BATCH_FCT} * 1000000)}")

            echo "scenario_c,${LOSS_LABEL},${PROTO_NAME},${i},${BATCH_FCT},${TOTAL_BYTES},${GOODPUT_MBPS}" >> "${CSV_FILE}"
            echo "      -> Repeticao ${i}/${REPETITIONS}: Lote FCT=${BATCH_FCT}s, Goodput=${GOODPUT_MBPS} Mbps"
            sleep 0.5
        done
    done
done

echo "[CENARIO C] Bateria concluida. Resultados em: ${CSV_FILE}"
