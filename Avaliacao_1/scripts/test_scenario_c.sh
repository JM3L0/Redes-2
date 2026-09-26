#!/bin/bash
# ==============================================================================
# test_scenario_c.sh - Bateria Experimental do Cenario C (QUIC & HoL Blocking)
# ==============================================================================
# Hipotese: QUIC elimina o HoL Blocking no nivel de transporte e supera TCP/HTTP2
# em cenarios de alta latencia (RTT >= 100ms) com perda aleatoria de pacotes.
#
# Metodologia:
#   - 3 niveis de perda: 0%, 2%, 5% (tc/netem, RTT ~100ms)
#   - 3 protocolos: HTTP/1.1, HTTP/2, HTTP/3 (QUIC)
#   - 100 objetos independentes de ~50 KB cada (lote web concorrente)
#   - Requisicoes concorrentes em paralelo (--parallel --parallel-max 100)
#   - 10 repeticoes independentes por combinacao (N=10)
#   - Captura tshark (.pcapng) para cada nivel de perda com snaplen 160B
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
echo " [CENARIO C] Bateria Web Concorrente"
echo "   100 objetos x 3 niveis de perda x 3 protocolos x 10 reps"
echo "   Total de medicoes planejadas: 90 (cada medicao baixa 100 objetos concorrentes)"
echo "=========================================================="

for SCENARIO in "${LOSS_SCENARIOS[@]}"; do
    case "${SCENARIO}" in
        scenario_c_loss0) LOSS_LABEL="0" ;;
        scenario_c_loss2) LOSS_LABEL="2" ;;
        scenario_c_loss5) LOSS_LABEL="5" ;;
    esac

    echo ""
    echo "[*] ============================================================"
    echo "[*] Configurando canal: ${SCENARIO} (RTT ~100ms, Perda=${LOSS_LABEL}%)"
    echo "[*] ============================================================"
    /workspace/scripts/setup_netem.sh "${SCENARIO}"

    # -----------------------------------------------------------------
    # Iniciar captura tshark para este nivel de perda (TCP + UDP/QUIC)
    # -----------------------------------------------------------------
    PCAP_FILE="${PCAP_DIR}/scenario_c_loss${LOSS_LABEL}.pcapng"
    rm -f "${PCAP_FILE}"
    echo "[CENARIO C] Iniciando captura tshark em: ${PCAP_FILE}..."
    tshark -i eth0 -s 160 -f "tcp port 443 or udp port 443" -w "${PCAP_FILE}" > /dev/null 2>&1 &
    TSHARK_PID=$!

    # Aguardar o processo tshark subir (polling por PID)
    for _ in $(seq 1 10); do
        if kill -0 "${TSHARK_PID}" 2>/dev/null; then
            break
        fi
        sleep 0.2
    done

    # -----------------------------------------------------------------
    # Rodar as baterias de protocolo para este nivel de perda
    # -----------------------------------------------------------------
    for PROTO in "${PROTOCOLS[@]}"; do
        PROTO_NAME="${PROTO#--}"
        PROTO_NAME="${PROTO_NAME%-only}"
        echo "  [+] Protocolo: ${PROTO_NAME} | Perda: ${LOSS_LABEL}%"

        for i in $(seq 1 ${REPETITIONS}); do
            START_TIME=$(date +%s.%N)

            # Baixar todos os 100 objetos via curl concorrente usando globbing de URL;
            # -w "%{size_download}\n" extrai bytes recebidos por objeto
            REAL_BYTES=$(curl -k -s --parallel --parallel-max 100 -o /dev/null \
                --connect-timeout 10 --max-time 120 \
                -w "%{size_download}\n" ${PROTO} "${SERVER_URL}/obj_[001-100].bin" 2>/dev/null \
                | awk '{s+=$1} END {print s+0}' || echo 0)

            END_TIME=$(date +%s.%N)
            BATCH_FCT=$(awk "BEGIN {printf \"%.4f\", ${END_TIME} - ${START_TIME}}")

            if [ "${REAL_BYTES:-0}" -eq 0 ] 2>/dev/null; then
                echo "      [-] Rep ${i}/${REPETITIONS}: Nenhum byte recebido - descartando medicao."
                continue
            fi

            GOODPUT_MBPS=$(awk "BEGIN {printf \"%.2f\", (${REAL_BYTES} * 8) / (${BATCH_FCT} * 1000000)}")

            echo "scenario_c,${LOSS_LABEL},${PROTO_NAME},${i},${BATCH_FCT},${REAL_BYTES},${GOODPUT_MBPS}" >> "${CSV_FILE}"
            echo "      -> Rep ${i}/${REPETITIONS}: FCT=${BATCH_FCT}s | Bytes=${REAL_BYTES} | Goodput=${GOODPUT_MBPS} Mbps"
            sleep 0.5
        done
    done

    # -----------------------------------------------------------------
    # Parar tshark ao finalizar este nivel de perda
    # -----------------------------------------------------------------
    kill -INT ${TSHARK_PID} 2>/dev/null || true
    wait ${TSHARK_PID} 2>/dev/null || true
    echo "[CENARIO C] Captura salva em: ${PCAP_FILE}"

done

echo ""
echo "=========================================================="
echo "[CENARIO C] Bateria concluida. Resultados em: ${CSV_FILE}"
echo "  PCaps salvos em: ${PCAP_DIR}/scenario_c_loss{0,2,5}.pcapng"
echo "=========================================================="
