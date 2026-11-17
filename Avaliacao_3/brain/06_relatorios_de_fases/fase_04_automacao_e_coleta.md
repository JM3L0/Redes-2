# Relatório de Execução — Fase 4: Automação (`run_n3`) e Execução Experimental dos 6 Testes (E01 a E06)

**Data:** 17 de Novembro de 2026  
**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Equipe:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`) & Marcos Willian de Sousa e Silva (`marcos.sousa@ufpi.edu.br`)  
**Status da Fase:** ✅ CONCLUÍDA COM SUCESSO

---

## 1. Execução Automatizada (`run_n3.py` / `run_n3.sh` / `run_n3.ps1`)

O script de automação executou de ponta a ponta as **5 repetições independentes** ($N = 5$) para cada um dos 6 testes essenciais (totalizando 30 ensaios), exportando os dados brutos para `data/raw/results.csv` e `data/raw/results.json`:

| ID | Algoritmo / Modo | Cenário `tc netem` | Resultado Médio $\pm$ Desvio Padrão ($s$) | Total de Retransmissões |
| :---: | :--- | :--- | :---: | :---: |
| **E01** | TCP CUBIC | LAN (1 ms, 0% perda) | $21945{,}80 \pm 2486{,}81\text{ Mbps}$ | $182$ ($36{,}4/\text{fluxo}$) |
| **E02** | TCP CUBIC | WAN (50 ms, 2% perda) | $2{,}63 \pm 0{,}56\text{ Mbps}$ | $390$ ($78{,}0/\text{fluxo}$) |
| **E03** | TCP BBR | WAN (50 ms, 2% perda) | $303{,}13 \pm 18{,}87\text{ Mbps}$ | $39095$ ($7819{,}0 \pm 527{,}2/\text{fluxo}$) |
| **E04** | HTTPS (HTTP/2 sobre TCP+TLS) | WAN (50 ms, 0% perda) | $163{,}57 \pm 2{,}73\text{ ms}$ (TTFB) | --- |
| **E05** | HTTP/3 Cold (1-RTT) | WAN (50 ms, 0% perda) | $112{,}36 \pm 0{,}99\text{ ms}$ (TTFB) | --- |
| **E06** | HTTP/3 Warm / Resumption | WAN (50 ms, 0% perda) | $61{,}46 \pm 0{,}95\text{ ms}$ (TTFB) | --- |
