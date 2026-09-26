#!/bin/bash
# ==============================================================================
# process_pcaps.sh - Extracao de Metricas de Overhead de Protocolo via tshark
# ==============================================================================
# Processa todos os arquivos .pcapng em data/pcaps/ e extrai para cada um:
#   - Total de pacotes e bytes brutos capturados na interface (passada unica)
#   - Retransmissoes TCP (indicador de perda e recuperacao)
#   - Contagem de pacotes UDP e pacotes QUIC especificamente
#   - Estimativa de bytes de overhead de cabecalho (IP + TCP/UDP)
#   - Percentual de overhead em relacao aos bytes totais capturados
#
# Saida: /workspace/data/processed/pcap_overhead_analysis.csv
#
# Uso:
#   ./process_pcaps.sh [diretorio_pcaps] [diretorio_saida]
#   ./process_pcaps.sh  (usa defaults: /workspace/data/pcaps e /workspace/data/processed)
# ==============================================================================
set -e

PCAP_DIR="${1:-/workspace/data/pcaps}"
OUTPUT_DIR="${2:-/workspace/data/processed}"
OUTPUT_CSV="${OUTPUT_DIR}/pcap_overhead_analysis.csv"

mkdir -p "${OUTPUT_DIR}"

echo "======================================================================"
echo " [PROCESS_PCAPS] Iniciando analise de overhead via tshark"
echo " Diretorio de entrada : ${PCAP_DIR}"
echo " Arquivo de saida     : ${OUTPUT_CSV}"
echo "======================================================================"

# Verificar se tshark esta disponivel
if ! command -v tshark &> /dev/null; then
    echo "[ERRO] tshark nao encontrado. Instale com: apt-get install -y tshark"
    exit 1
fi

# Verificar se existem pcaps para processar
PCAP_COUNT=$(find "${PCAP_DIR}" -name "*.pcapng" 2>/dev/null | wc -l)
if [ "${PCAP_COUNT}" -eq 0 ]; then
    echo "[AVISO] Nenhum arquivo .pcapng encontrado em ${PCAP_DIR}."
    echo "        Execute os experimentos primeiro com run_experiments.sh"
    exit 0
fi

echo "scenario,pcap_file,total_packets,total_bytes_raw,tcp_packets,tcp_retransmissions,udp_packets,quic_packets,ip_header_bytes_est,overhead_percent" > "${OUTPUT_CSV}"

echo ""
echo "Encontrados ${PCAP_COUNT} arquivo(s) pcapng para processar..."
echo ""

for PCAP_FILE in "${PCAP_DIR}"/*.pcapng; do
    [ -f "${PCAP_FILE}" ] || continue
    BASENAME=$(basename "${PCAP_FILE}" .pcapng)

    # Inferir nome do cenario a partir do nome do arquivo
    case "${BASENAME}" in
        scenario_a*) SCENARIO="A - UDP Puro" ;;
        scenario_b*) SCENARIO="B - TCP/QUIC Massivo" ;;
        scenario_c*) SCENARIO="C - QUIC HoL Blocking" ;;
        *)           SCENARIO="desconhecido" ;;
    esac

    echo "[*] Processando: ${BASENAME}.pcapng  (Cenario: ${SCENARIO})"

    # Extracao de metricas em passada unica (streamline single-pass)
    METRICS=$( (tshark -r "${PCAP_FILE}" \
        -T fields \
        -e frame.len \
        -e ip.proto \
        -e tcp.analysis.retransmission \
        -e udp.dstport \
        -e udp.srcport 2>/dev/null || true) | awk -F'\t' '
        BEGIN {
            pkts=0; bytes=0; tcp=0; retrans=0; udp=0; quic=0;
        }
        {
            len = $1 + 0;
            proto = $2;
            ret = $3;
            udport_dst = $4;
            udport_src = $5;

            pkts++;
            bytes += len;

            if (proto == "6") {
                tcp++;
                if (ret != "") retrans++;
            } else if (proto == "17") {
                udp++;
                if (udport_dst == "443" || udport_src == "443") quic++;
            }
        }
        END {
            header_bytes = (tcp * 40) + (udp * 28);
            ovh_pct = (bytes > 0) ? (header_bytes / bytes) * 100 : 0;
            printf "%d,%d,%d,%d,%d,%d,%d,%.2f", pkts, bytes, tcp, retrans, udp, quic, header_bytes, ovh_pct;
        }
    ')

    IFS=',' read -r TOTAL_PACKETS TOTAL_BYTES TCP_PACKETS TCP_RETRANS UDP_PACKETS QUIC_PACKETS IP_HEADER_BYTES OVERHEAD_PCT <<< "${METRICS}"

    echo "\"${SCENARIO}\",${BASENAME}.pcapng,${TOTAL_PACKETS},${TOTAL_BYTES},${TCP_PACKETS},${TCP_RETRANS},${UDP_PACKETS},${QUIC_PACKETS},${IP_HEADER_BYTES},${OVERHEAD_PCT}" >> "${OUTPUT_CSV}"

    echo "    Pacotes totais  : ${TOTAL_PACKETS}"
    echo "    Bytes brutos    : ${TOTAL_BYTES}"
    echo "    TCP / Retrans   : ${TCP_PACKETS} / ${TCP_RETRANS}"
    echo "    UDP / QUIC      : ${UDP_PACKETS} / ${QUIC_PACKETS}"
    echo "    Overhead est.   : ${OVERHEAD_PCT}%"
    echo ""
done

echo "======================================================================"
echo " [PROCESS_PCAPS] Analise concluida!"
echo " Resultados salvos em: ${OUTPUT_CSV}"
echo "======================================================================"
