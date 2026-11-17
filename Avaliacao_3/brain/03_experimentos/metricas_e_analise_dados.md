# 03. Métricas Operacionais, Análise Estatística e Especificação dos Gráficos — 3ª Avaliação (N3)

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Curso:** Bacharelado em Sistemas de Informação  
**Equipe:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`) & Marcos Willian de Sousa e Silva (`marcos.sousa@ufpi.edu.br`)

Este documento define as fórmulas matemáticas de extração das métricas do `iperf3` (Bloco A) e do `curl` (Bloco B), o tratamento estatístico das $N \ge 5$ amostras, o esquema de exportação de dados brutos (CSV e JSON) e as regras obrigatórias para geração dos **2 gráficos comparativos com barras de erro**.

---

## 1. Extração e Modelagem das Métricas Operacionais

### 1.1. Bloco A (`iperf3 -J`): Vazão (Mbps) e Retransmissões
Ao executar `iperf3 -c 172.20.0.10 -t 15 -C <algoritmo> -J`, o utilitário retorna um objeto JSON contendo o sumário da transmissão em `end.sum_sent` e `end.sum_received`:

1. **Vazão Média por Amostra ($\text{Throughput}_i$, em Mbps):**
   Extraída de `end.sum_received.bits_per_second` (vazão efetivamente entregue ao receptor durante os 15 segundos) ou `end.sum_sent.bits_per_second`, convertida para Megabits por segundo ($\text{Mbps}$):
   $$\text{Vazão}_i\text{ (Mbps)} = \frac{\text{bits\_per\_second}_i}{10^6}$$

2. **Número de Retransmissões TCP por Amostra ($\text{Retrans}_i$):**
   Extraído diretamente do contador de segmentos retransmitidos pelo emissor no JSON do `iperf3`:
   $$\text{Retrans}_i = \texttt{end.sum\_sent.retransmits}$$
   - Para a **Tabela Resumo** exigida na Seção 5 do edital, reportam-se tanto a **média e desvio padrão de retransmissões por fluxo de 15s** quanto o **Total Acumulado de Retransmissões** nas 5 repetições:
     $$\text{Total de Retransmissões} = \sum_{i=1}^{N} \text{Retrans}_i$$

3. **Produto Largura de Banda-Atraso ($BDP$) e Limite de Mathis:**
   - Para fundamentar a análise teórica do Bloco A:
     $$BDP = BtlBw \times RTprop$$
   - No TCP CUBIC sob perda estocástica $p = 0.02$ (2%) e $RTT = 0.050\text{ s}$ (50 ms), a vazão estacionária é severamente limitada pelas sucessivas reduções de janela ($cwnd \leftarrow 0.7 \times cwnd$), ao passo que o BBR mantém os dados em voo próximos a $1 \sim 2 \times BDP$.

---

### 1.2. Bloco B (`curl`): Time to First Byte (`time_starttransfer` em ms)
O utilitário `curl` possui a variável de formatação nativa `%{time_starttransfer}`, que mede o tempo exato (em segundos, com precisão de microssegundos) desde o início da operação até o instante imediatamente anterior à recepção do primeiro byte de resposta HTTP vindo do servidor.

1. **Conversão para Milissegundos ($\text{TTFB}_i$):**
   $$\text{TTFB}_i\text{ (ms)} = \texttt{time\_starttransfer}_i \times 1000$$

2. **Decomposição Analítica dos RTTs no Cenário 3 ($\text{RTT} = 50\text{ ms}$, $\text{Perda} = 0\%$):**
   - **E04 — HTTPS (HTTP/2 sobre TCP + TLS 1.3):**
     $$\text{TTFB}_{\text{E04}} = \underbrace{1\text{ RTT}}_{\text{TCP SYN/SYN-ACK}} + \underbrace{1\text{ RTT}}_{\text{TLS 1.3 Handshake}} + \underbrace{1\text{ RTT}}_{\text{HTTP/2 GET } \to \text{ 1º Byte}} + t_{\text{proc}} \approx 3 \times 50\text{ ms} = 150\text{ ms}$$
   - **E05 — HTTP/3 Cold (QUIC 1-RTT):**
     $$\text{TTFB}_{\text{E05}} = \underbrace{1\text{ RTT}}_{\text{QUIC + TLS 1.3 Integrado}} + \underbrace{1\text{ RTT}}_{\text{HTTP/3 GET } \to \text{ 1º Byte}} + t_{\text{proc}} \approx 2 \times 50\text{ ms} = 100\text{ ms}$$
   - **E06 — HTTP/3 Warm / Session Resumption (0-RTT / Reaproveitamento):**
     Na chamada sequencial do `curl` (`curl ... URL1 URL2`), a primeira transferência realiza o handshake (equivalente a E05) e a segunda transferência reutiliza a sessão QUIC/TLS já estabelecida (ou ticket 0-RTT), de modo que o tempo até o início da transferência da segunda requisição ($t_{\text{starttransfer}, 2}$) contabiliza apenas o RTT da requisição/resposta:
     $$\text{TTFB}_{\text{E06}} = \underbrace{0\text{ RTT}}_{\text{Handshake Eliminado}} + \underbrace{1\text{ RTT}}_{\text{HTTP/3 GET } \to \text{ 1º Byte}} + t_{\text{proc}} \approx 1 \times 50\text{ ms} = 50\text{ ms}$$

---

## 2. Tratamento Estatístico ($N \ge 5$ Repetições por Teste)

Para cada teste $k \in \{\text{E01}, \text{E02}, \text{E03}, \text{E04}, \text{E05}, \text{E06}\}$ com $N \ge 5$ amostras independentes $\{x_1, x_2, \dots, x_N\}$:

1. **Média Amostral ($\bar{x}$):**
   $$\bar{x} = \frac{1}{N} \sum_{i=1}^{N} x_i$$
2. **Desvio Padrão Amostral ($s$ — usado nas Barras de Erro conforme Seção 5 do Edital):**
   $$s = \sqrt{\frac{1}{N - 1} \sum_{i=1}^{N} (x_i - \bar{x})^2}$$
3. **Coeficiente de Variação ($CV\%$):**
   $$CV(\%) = \left(\frac{s}{\bar{x}}\right) \times 100$$

---

## 3. Esquema de Exportação dos Dados Brutos (`data/raw/`)

O script de automação (`run_n3.py` / `run_n3.sh`) exporta todos os resultados brutos para `data/raw/results.csv` e `data/raw/results.json`:

### 3.1. Colunas de `data/raw/results.csv`
```csv
test_id,block,repetition,timestamp,protocol_mode,scenario,rtt_ms,loss_pct,metric_name,throughput_mbps,retransmits,ttfb_ms
E01,A,1,2026-11-17T18:00:00Z,TCP CUBIC,LAN (1ms 0%),1.0,0.0,throughput_mbps,3450.25,0,
E02,A,1,2026-11-17T18:01:20Z,TCP CUBIC,WAN (50ms 2%),50.0,2.0,throughput_mbps,3.42,48,
E03,A,1,2026-11-17T18:02:40Z,TCP BBR,WAN (50ms 2%),50.0,2.0,throughput_mbps,84.60,195,
E04,B,1,2026-11-17T18:04:00Z,HTTPS (HTTP/2 TCP+TLS),WAN (50ms 0%),50.0,0.0,ttfb_ms,,,154.20
E05,B,1,2026-11-17T18:04:05Z,HTTP/3 Cold (1-RTT),WAN (50ms 0%),50.0,0.0,ttfb_ms,,,103.80
E06,B,1,2026-11-17T18:04:10Z,HTTP/3 Warm / Resumption,WAN (50ms 0%),50.0,0.0,ttfb_ms,,,52.10
```

---

## 4. Especificação Obrigatória dos 2 Gráficos Comparativos (`analysis/plot_results.py`)

> [!CAUTION]
> ### PENALIDADE DIRETA DO EDITAL (-10 PONTOS):
> **"Ausência de barras de erro nos gráficos: -10 pontos."**  
> Ambos os gráficos gerados pelo script Python DEVEM exibir **barras de erro representando o desvio padrão ($s$)** (`yerr=std_values, capsize=6, ecolor='black'`) e possuir títulos, unidades e eixos devidamente rotulados.

### 4.1. Gráfico 1 (Bloco A): `data/plots/fig1_bloco_a_vazao_cc.png`
- **Título:** Impacto do Controle de Congestionamento na Vazão TCP (Fluxo de 15s via `iperf3`)
- **Séries Comparadas (Eixo X):**
  1. `E01: TCP CUBIC (LAN: 1ms, 0% perda)`
  2. `E02: TCP CUBIC (WAN: 50ms, 2% perda)`
  3. `E03: TCP BBR (WAN: 50ms, 2% perda)`
- **Eixo Y:** Vazão Média em Mbps ($\bar{x} \pm s$), com **barras de erro de desvio padrão**.
- **Detalhe de Engenharia Visual:** Como a vazão na LAN (E01, sem perda e com 1 ms de RTT) pode ser ordens de grandeza superior à vazão na WAN (E02 e E03), o Gráfico 1 pode apresentar dois subpainéis lado a lado:
  - **Painel (a):** Comparação global (E01 vs. E02 vs. E03) com anotações dos valores exatos ($\bar{x} \pm s\text{ Mbps}$) e barras de erro;
  - **Painel (b):** Zoom direto no Cenário WAN Degradado (50 ms, 2% perda) confrontando `E02 (TCP CUBIC)` vs. `E03 (TCP BBR)` com barras de erro de desvio padrão e indicação do total de retransmissões, permitindo visualizar com nitidez absoluta a diferença entre CUBIC e BBR na WAN!

### 4.2. Gráfico 2 (Bloco B): `data/plots/fig2_bloco_b_ttfb_handshake.png`
- **Título:** Latência de Handshake e Session Resumption — TTFB para Objeto de 1 KB (WAN: 50 ms RTT, 0% Perda)
- **Séries Comparadas (Eixo X):**
  1. `E04: HTTPS / HTTP/2 (TCP + TLS 1.3 — 3 RTTs até TTFB)`
  2. `E05: HTTP/3 Cold (QUIC 1-RTT — 2 RTTs até TTFB)`
  3. `E06: HTTP/3 Warm / Resumed (QUIC 0-RTT / Reuso — 1 RTT até TTFB)`
- **Eixo Y:** TTFB Médio (`time_starttransfer`) em milissegundos ($\bar{x} \pm s$), com **barras de erro de desvio padrão** e linhas horizontais tracejadas de referência teórica em $50\text{ ms}$ (1 RTT), $100\text{ ms}$ (2 RTTs) e $150\text{ ms}$ (3 RTTs).
