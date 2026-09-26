#!/bin/bash
# ==============================================================================
# run_experiments.sh - Orquestrador Mestre de Todos os Experimentos
# ==============================================================================
# Suporta execucao direta no Host (Linux/WSL/macOS) ou dentro do container Docker.
# ==============================================================================
set -e

# Se executado no Host, sobe os containers e delega para o container client
if [ ! -f "/.dockerenv" ] && [ ! -d "/workspace" ]; then
    echo "======================================================================"
    echo "  INICIANDO ORQUESTRACAO PELO HOST (DOCKER COMPOSE)"
    echo "======================================================================"
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -f "${SCRIPT_DIR}/../docker/docker-compose.yml" ]; then
        PROJECT_ROOT="${SCRIPT_DIR}/.."
    else
        PROJECT_ROOT="${SCRIPT_DIR}"
    fi

    # 1. Gerar cargas estaticas se ausentes
    if [ ! -f "${PROJECT_ROOT}/data/static/100MB.bin" ] || [ ! -f "${PROJECT_ROOT}/data/static/1GB.bin" ]; then
        echo "[*] Gerando cargas estaticas sinteticas..."
        python3 "${PROJECT_ROOT}/scripts/generate_static_data.py" 2>/dev/null || \
        python "${PROJECT_ROOT}/scripts/generate_static_data.py" 2>/dev/null || true
    fi

    # 2. Iniciar ambiente Docker Compose
    echo "[*] Subindo servicos com docker compose up -d --build..."
    docker compose -f "${PROJECT_ROOT}/docker/docker-compose.yml" up -d --build

    # 3. Aguardar o servidor NGINX
    echo "[*] Aguardando prontidao do redes2_server..."
    sleep 3

    # 4. Executar os ensaios dentro do container client
    echo "[*] Executando ensaios no container redes2_client..."
    docker exec redes2_client /workspace/scripts/run_experiments.sh

    echo ""
    echo "======================================================================"
    echo "  BATERIA COMPLETA FINALIZADA COM SUCESSO NO HOST!"
    echo "  Artefatos disponiveis em data/ (raw, pcaps, processed, plots)"
    echo "======================================================================"
    exit 0
fi

# ==============================================================================
# Execucao dentro do Container Docker redes2_client
# ==============================================================================
echo "======================================================================"
echo "  INICIANDO BATERIA CIENTIFICA COMPLETA DE REDES II (UFPI - 2026-2)"
echo "  Aluno: Joao Marcos Sousa Rufino Leal"
echo "  Protocolos: TCP (TLS 1.3), UDP Puro e QUIC (HTTP/3)"
echo "======================================================================"

# Garantir permissoes de execucao nos scripts
chmod +x /workspace/scripts/*.sh

# Limpar regras residuais de qdisc
/workspace/scripts/setup_netem.sh clear

START_ALL=$(date +%s)

# 1. Executar Cenario A
echo ""
echo "[ETAPA 1/3] Executando Cenario A (UDP Puro)..."
/workspace/scripts/test_scenario_a.sh

# 2. Executar Cenario B
echo ""
echo "[ETAPA 2/3] Executando Cenario B (TCP vs QUIC Massivo)..."
/workspace/scripts/test_scenario_b.sh

# 3. Executar Cenario C
echo ""
echo "[ETAPA 3/3] Executando Cenario C (QUIC & HoL Blocking)..."
/workspace/scripts/test_scenario_c.sh

# Limpar regras netem ao finalizar
/workspace/scripts/setup_netem.sh clear

END_ALL=$(date +%s)
TOTAL_TIME=$((END_ALL - START_ALL))

echo ""
echo "======================================================================"
echo "  TODOS OS ENSAIOS CONCLUIDOS COM SUCESSO!"
echo "  Tempo total de execucao: ${TOTAL_TIME} segundos."
echo "  Dados brutos salvos em /workspace/data/raw/"
echo "  Capturas pcapng salvas em /workspace/data/pcaps/"
echo "======================================================================"

# Extrair metricas de overhead dos pcaps via tshark
if [ -f /workspace/scripts/process_pcaps.sh ]; then
    echo ""
    echo "[PCAPS] Extraindo metricas de overhead de protocolo dos pcapng..."
    /workspace/scripts/process_pcaps.sh
fi

# Executar pipeline de analise e geracao de graficos Python
if [ -f /workspace/analysis/parse_logs.py ]; then
    echo ""
    echo "[ANALISE] Consolidando estatisticas com parse_logs.py..."
    python3 /workspace/analysis/parse_logs.py \
        --raw-dir /workspace/data/raw \
        --out-dir /workspace/data/processed
fi

if [ -f /workspace/analysis/generate_plots.py ]; then
    echo ""
    echo "[ANALISE] Gerando graficos cientificos com generate_plots.py..."
    python3 /workspace/analysis/generate_plots.py
fi

echo ""
echo "======================================================================"
echo "  PIPELINE COMPLETO ENCERRADO COM SUCESSO!"
echo "  Graficos salvos em /workspace/data/plots/"
echo "  Dados processados em /workspace/data/processed/"
echo "======================================================================"
