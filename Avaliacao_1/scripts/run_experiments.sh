#!/bin/bash
# ==============================================================================
# run_experiments.sh - Orquestrador Mestre de Todos os Experimentos
# ==============================================================================
set -e

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

# Executar pipeline de analise e geracao de graficos se existir
if [ -f /workspace/analysis/generate_plots.py ]; then
    echo "[ANALISE] Processando estatisticas e gerando graficos cientificos..."
    python3 /workspace/analysis/generate_plots.py
fi
