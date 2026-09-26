#!/bin/bash
# ==============================================================================
# run_experiments.sh - Ponto de Entrada de Execucao Automatizada (Host)
# ==============================================================================
# Conforme Requisito do Professor:
# "O projeto deve conter um script (run_experiments.sh ou similar) capaz de
# iniciar o ambiente via 'docker compose up -d', disparar as baterias de testes,
# recolher os ficheiros .pcapng e logs, e exportar os graficos finais sem
# intervencao manual."
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "${SCRIPT_DIR}/scripts/run_experiments.sh" "$@"
