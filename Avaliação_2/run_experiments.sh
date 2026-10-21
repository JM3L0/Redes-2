#!/usr/bin/env bash
# ==============================================================================
# Orquestrador Mestre 1-Click de Experimentos Web (Bash / Linux / WSL / macOS)
# Disciplina: Redes de Computadores II (UFPI - CSHNB)
# Aluno: João Marcos Sousa Rufino Leal (jsousarufinoleal@ufpi.edu.br)
# ==============================================================================

set -euo pipefail

ITERATIONS=10
KEEP_ALIVE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        -i|--iterations)
            ITERATIONS="$2"
            shift 2
            ;;
        -q|--quick)
            ITERATIONS=2
            shift
            ;;
        -k|--keep-alive)
            KEEP_ALIVE=true
            shift
            ;;
        *)
            echo "Opção desconhecida: $1"
            echo "Uso: $0 [--iterations N] [--quick] [--keep-alive]"
            exit 1
            ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "================================================================================"
echo "   ORQUESTRADOR MESTRE DE EXPERIMENTOS DE REDES II (UFPI - CSHNB)             "
echo "   Estudo Experimental: HTTP/1.1 vs HTTPS/TLS 1.3 vs HTTP/3-QUIC              "
echo "   Aluno: João Marcos Sousa Rufino Leal                                       "
echo "   Iterações por teste: $ITERATIONS                                            "
echo "================================================================================"

# 1. Determina porta HTTP/1.1
HTTP1_PORT=${HTTP1_PORT:-8080}
if ss -tuln | grep -q ":8080 " 2>/dev/null || netstat -tuln | grep -q ":8080 " 2>/dev/null; then
    echo "[!] Porta 8080 ocupada no host. Usando fallback automático: 8081."
    HTTP1_PORT=8081
fi
export HTTP1_PORT

# 2. Certificados TLS
if [[ ! -f "docker/certs/cert.pem" || ! -f "docker/certs/key.pem" ]]; then
    echo "[*] Gerando certificados TLS 1.3 com SANs..."
    python3 scripts/generate_certs.py
fi

# 3. Payloads Sintéticos
if [[ ! -f "data/static/50MB.bin" || ! -f "data/static/objects/obj_100.bin" ]]; then
    echo "[*] Gerando payloads sintéticos (50MB e 100x10KB)..."
    python3 scripts/generate_payloads.py
fi

# 4. Sobe contêineres Docker
echo "[*] Iniciando contêineres Docker via docker-compose..."
docker compose -f docker/docker-compose.yml up -d

# Instala iproute2 se necessário
for c in server_http11 server_http2_tls server_http3_quic; do
    if ! docker exec "$c" which tc >/dev/null 2>&1; then
        echo "[*] Instalando iproute2 em $c..."
        docker exec "$c" apk add --no-cache iproute2 >/dev/null 2>&1
    fi
done

cleanup() {
    echo ""
    if [[ "$KEEP_ALIVE" == "true" ]]; then
        echo "[!] Flag --keep-alive ativa: mantendo contêineres Docker em execução."
    else
        echo "[*] Encerrando contêineres Docker de forma limpa (docker compose down)..."
        docker compose -f docker/docker-compose.yml down
        echo "[+] Ambiente encerrado com sucesso."
    fi
}
trap cleanup EXIT

# 5. CENÁRIO 1: LAN (RTT 1ms, 0% perda)
echo ""
echo "================================================================================"
echo " ETAPA 1/2: CENÁRIO 1 (LAN) - RTT 1.0ms, Perda 0.0%"
echo "================================================================================"
bash scripts/setup_netem.sh lan
echo "[*] Executando testes T01 a T03 (Carga A) e T07 a T09 (Carga B)..."
python3 benchmark/client.py --scenario lan --iterations "$ITERATIONS" --http1-port "$HTTP1_PORT"

# 6. CENÁRIO 2: WAN (RTT 50ms, 2% perda)
echo ""
echo "================================================================================"
echo " ETAPA 2/2: CENÁRIO 2 (WAN) - RTT 50.0ms, Perda 2.0%"
echo "================================================================================"
bash scripts/setup_netem.sh wan
echo "[*] Executando testes T04 a T06 (Carga A) e T10 a T12 (Carga B)..."
python3 benchmark/client.py --scenario wan --iterations "$ITERATIONS" --http1-port "$HTTP1_PORT"

# 7. Limpeza tc netem
echo ""
echo "[*] Restaurando interfaces virtuais (remoção de regras netem)..."
bash scripts/setup_netem.sh clean

# 8. Análise Estatística e Gráficos
echo ""
echo "================================================================================"
echo " CONSOLIDAÇÃO ESTATÍSTICA E GERAÇÃO DE FIGURAS CIENTÍFICAS"
echo "================================================================================"
python3 analysis/process_data.py
python3 analysis/plot_results.py

echo ""
echo "================================================================================"
echo "   TODOS OS EXPERIMENTOS FORAM CONCLUÍDOS COM SUCESSO!                          "
echo "   Dados Brutos:    data/raw/results.json & results.csv                         "
echo "   Tabelas Finais:  data/processed/summary_table.csv & summary_table.tex        "
echo "   Gráficos:        data/plots/ (5 figuras com barras de erro obrigatórias)     "
echo "================================================================================"
