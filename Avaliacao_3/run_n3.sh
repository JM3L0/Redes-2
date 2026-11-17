#!/usr/bin/env bash
# ==============================================================================
# Orquestrador de Automação (run_n3.sh) — 3ª Avaliação (N3) Redes II UFPI
# Aplica as regras tc netem, executa as 5 repetições dos 6 testes (E01 a E06),
# exporta os dados brutos (CSV/JSON), gera os gráficos com barras de erro e
# limpa o ambiente ao final.
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if command -v python3 >/dev/null 2>&1; then
    python3 run_n3.py "$@"
else
    python run_n3.py "$@"
fi
