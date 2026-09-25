# 📘 Fase 3: Scripts de Automação, Emulação de Canal e Capturas

**Status:** ✅ CONCLUÍDA  
**Data:** 25/09/2026  
**Responsável:** João Marcos Sousa Rufino Leal  

---

## 1. Objetivos da Fase

Criar o conjunto completo de scripts de automação que orquestram:
1. A configuração e limpeza das condições de canal via `tc/netem`;
2. A execução automatizada das baterias de testes dos Cenários A, B e C com N=10 repetições cada;
3. A captura sincronizada de tráfego com `tshark`;
4. A persistência dos dados brutos em CSV e `.pcapng`.

---

## 2. O que foi Feito

### 2.1. Script de Emulação de Canal (`setup_netem.sh`)
- **Arquivo:** [`scripts/setup_netem.sh`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/scripts/setup_netem.sh)
- Implementa os 6 perfis de canal exigidos:
  - `scenario_a`: Atraso 2ms (RTT ~4ms, 0% perda) para Cenário A.
  - `scenario_b`: Atraso 10ms (RTT ~20ms, 0% perda) para Cenário B.
  - `scenario_c_loss0/2/5`: Atraso 50ms (RTT ~100ms) com 0%, 2% e 5% de perda para Cenário C.
- **Melhoria de robustez (no-workarounds):** `clear_rules()` verifica se existe regra `netem` ativa antes de deletar, eliminando o silenciamento cego com `|| true`. Interface configurável via `$NETEM_IFACE`.

### 2.2. Cenário A — UDP Puro (`test_scenario_a.sh`)
- **Arquivo:** [`scripts/test_scenario_a.sh`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/scripts/test_scenario_a.sh)
- 50 execuções de `iperf3 -u` (5 taxas × 10 repetições): 10M, 50M, 100M, 250M e 500M.
- Saída: [`data/raw/scenario_a_results.csv`] + [`data/pcaps/scenario_a_udp_sample.pcapng`].
- **Melhorias aplicadas:**
  - Sincronização do `tshark` por polling de PID (elimina `sleep 1` arbitrário).
  - Validação do JSON do `iperf3` com `jq -e` antes de gravar no CSV (descarta medições corrompidas).
  - `awk printf "%.2f"` para formatação consistente do Goodput.
  - Substituição de `sed 's/M//'` por expansão nativa `${RATE%M}` (deslop).

### 2.3. Cenário B — TCP Massivo vs QUIC (`test_scenario_b.sh`)
- **Arquivo:** [`scripts/test_scenario_b.sh`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/scripts/test_scenario_b.sh)
- 60 execuções de `curl` (3 protocolos × 2 arquivos × 10 repetições): HTTP/1.1, HTTP/2, HTTP/3 com 100MB e 1GB.
- Saída: [`data/raw/scenario_b_results.csv`] + [`data/pcaps/scenario_b_sample.pcapng`].
- **Melhorias aplicadas:**
  - `%{http_code}` adicionado ao formato do cURL; requisições com HTTP ≠ 200 são descartadas explicitamente.
  - Sincronização do `tshark` por polling de PID.
  - Substituição de `sed` por expansões nativas `${FILE%.bin}` e `${PROTO#--}` (deslop).

### 2.4. Cenário C — QUIC & HoL Blocking (`test_scenario_c.sh`)
- **Arquivo:** [`scripts/test_scenario_c.sh`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/scripts/test_scenario_c.sh)
- 90 execuções (3 perdas × 3 protocolos × 10 repetições) baixando 100 objetos de 50 KB.
- Saída: [`data/raw/scenario_c_results.csv`].
- **Melhorias aplicadas:**
  - `TOTAL_BYTES=5120000` hardcoded removido. Agora mede bytes **realmente recebidos** via `-w "%{size_download}"` somados com `awk`. Lotes com zero bytes recebidos são descartados.
  - Substituição de `sed` por expansões nativas (deslop).

### 2.5. Orquestrador Mestre (`run_experiments.sh`)
- **Arquivo:** [`scripts/run_experiments.sh`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/scripts/run_experiments.sh)
- Executa a bateria completa (A → B → C) com limpeza de canal antes e depois.
- Invoca `analysis/generate_plots.py` automaticamente ao final, se disponível.

---

## 3. Artefatos Produzidos

| Arquivo | Descrição |
|---|---|
| [`scripts/setup_netem.sh`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/scripts/setup_netem.sh) | Emulação de canal via `tc/netem` — 6 perfis |
| [`scripts/test_scenario_a.sh`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/scripts/test_scenario_a.sh) | Bateria UDP com iperf3 (Cenário A) |
| [`scripts/test_scenario_b.sh`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/scripts/test_scenario_b.sh) | Bateria HTTP/1.1 vs HTTP/2 vs HTTP/3 (Cenário B) |
| [`scripts/test_scenario_c.sh`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/scripts/test_scenario_c.sh) | Bateria 100 objetos com perda de pacotes (Cenário C) |
| [`scripts/run_experiments.sh`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/scripts/run_experiments.sh) | Orquestrador mestre ponta a ponta |
