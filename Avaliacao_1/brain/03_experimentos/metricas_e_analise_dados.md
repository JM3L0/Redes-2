# 03. Métricas, Captura de Tráfego e Análise Estatística

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** UFPI — Bacharelado em Sistemas de Informação

Este documento estabelece as fórmulas matemáticas, metodologias de captura com `tshark`/Wireshark e o pipeline estatístico rigoroso exigido pelo professor.

---

## 1. Métricas Obrigatórias e Formulação Matemática

### 1.1. Flow Completion Time (FCT)
O FCT quantifica o tempo total decorrido desde o início da solicitação até a entrega do último byte útil da aplicação.

$$\text{FCT} = t_{\text{fim}} - t_{\text{início}}$$

- **No cURL:** Extraído diretamente com a variável `%{time_total}` (em segundos com resolução de microssegundos).
- **No Wireshark/tshark:**
  - **TCP:** $t_{\text{início}}$ é o timestamp do pacote `SYN` e $t_{\text{fim}}$ é o último pacote de dados com payload HTTP/2 ou ACK correspondente.
  - **QUIC:** $t_{\text{início}}$ é o timestamp do primeiro pacote `Initial` (Client Hello) e $t_{\text{fim}}$ é o último datagrama contendo o frame `STREAM` com flag `FIN`.
- **Estatísticas exigidas:**
  - Média ($\mu$);
  - Desvio Padrão ($\sigma$);
  - Percentis p50 (mediana), p90 e p95;
  - Dispersão temporal (Boxplot ou CDF).

### 1.2. Vazão Efetiva (Goodput)
O Goodput avalia a taxa real de transferência de dados úteis (payload da camada de aplicação), ignorando cabeçalhos de rede e retransmissões.

$$\text{Goodput (Mbps)} = \frac{\text{Bytes Úteis da Aplicação} \times 8}{\text{FCT (segundos)} \times 10^6}$$

> [!NOTE]
> Não confunda **Goodput** com **Throughput**:
> - **Throughput:** Soma total de todos os bits trafegados no canal físico/enlace por segundo (incluindo cabeçalhos IP, TCP/UDP, TLS e retransmissões).
> - **Goodput:** Apenas os dados líquidos entregues à aplicação (ex.: os 100 MB exatos do arquivo baixado).

### 1.3. Sobrecarga de Protocolo (Protocol Overhead)
A sobrecarga quantifica o "custo" em bytes de infraestrutura e controle imposto por cada protocolo para transportar os dados da aplicação.

$$\text{Overhead Absoluto (Bytes)} = \text{Bytes Brutos na Interface} - \text{Bytes Úteis de Aplicação}$$

$$\text{Overhead Relativo (\%)} = \left( \frac{\text{Bytes Brutos na Interface}}{\text{Bytes Úteis de Aplicação}} - 1 \right) \times 100\%$$

- **Bytes Brutos na Interface:** Medidos diretamente pelo `tshark` analisando a interface do contêiner:
  ```bash
  # Total de bytes de todos os frames capturados no arquivo .pcapng
  tshark -r capture.pcapng -q -z io,stat,0,"SUM(frame.len)frame.len"
  ```
- **Fatores que compõem os Bytes Brutos:**
  - Enlace: Ethernet (14 bytes);
  - Rede: IPv4 (20 bytes) ou IPv6 (40 bytes);
  - Transporte: UDP (8 bytes) vs TCP (20 a 60 bytes com opções SACK/TS);
  - Segurança / Sessão: Registros TLS 1.3 (record header, MAC, IV) ou Cabeçalhos QUIC (Short/Long Header, Packet Number, Frame Headers);
  - Retransmissões: Bytes retransmitidos devido a descarte.

### 1.4. Comportamento de Perda e Retransmissão
O documento exige a identificação visual no Wireshark da recuperação de perdas em cada protocolo:

| Fenômeno | Como identificar no TCP (Wireshark) | Como identificar no QUIC (Wireshark) |
| :--- | :--- | :--- |
| **Identificação de Perda** | Filtros: `tcp.analysis.lost_segment` ou `tcp.analysis.duplicate_ack` (3 DUP ACKs disparam Fast Retransmit). | QUIC ACK frames com lacunas de pacotes (Packet Numbers ausentes na faixa reportada no ACK Frame). |
| **Retransmissão** | Filtro: `tcp.analysis.retransmission` ou `tcp.analysis.fast_retransmission`. O número de sequência (`Sequence Number`) é idêntico ao do pacote perdido. | **Atenção:** No QUIC, o número de pacote (`Packet Number`) é **estritamente monotônico crescente**. O dado retransmitido ganha um **NOVO** Packet Number, mas o `Stream Offset` dentro do frame `STREAM` é o mesmo. |
| **Timeout (RTO / PTO)** | `tcp.analysis.rto` (após timeout prolongado). | PTO (Probe Timeout) gerando pacotes de probe para solicitar ACK imediato. |

---

## 2. Rigor Estatístico Obrigatório

Conforme o edital: **"Cada ponto de teste deve ser fruto de pelo menos 10 repetições independentes, com indicação clara de média e desvio padrão ou de intervalo de confiança nos gráficos e nas tabelas."**

### 2.1. Fórmulas de Amostragem ($N = 10$)
- **Média Amostral:**
  $$\bar{x} = \frac{1}{N} \sum_{i=1}^{N} x_i$$
- **Desvio Padrão Amostral:**
  $$s = \sqrt{\frac{1}{N - 1} \sum_{i=1}^{N} (x_i - \bar{x})^2}$$
- **Intervalo de Confiança de 95% (Distribuição t de Student com $N-1 = 9$ graus de liberdade):**
  $$IC_{95\%} = \bar{x} \pm t_{0.975, \, 9} \cdot \frac{s}{\sqrt{N}}$$
  *(Para 9 graus de liberdade, $t_{critico} \approx 2.262$)*

---

## 3. Automação de Capturas com `tshark`

O contêiner `client` deve executar o `tshark` em background sincronizado com o disparo de cada teste:

```bash
# Iniciar captura em segundo plano
tshark -i eth0 -f "host 172.28.0.10" -w /workspace/data/pcaps/cenario_b_h3_rep1.pcapng &
TSHARK_PID=$!

# Aguardar inicialização do tshark
sleep 1

# Disparar teste
curl -k --http3-only -w "%{time_total},%{speed_download},%{size_download}\n" \
     -o /dev/null https://server/100MB.bin >> /workspace/data/raw_logs/cenario_b_h3.csv

# Encerrar captura graciosamente
kill -2 $TSHARK_PID
wait $TSHARK_PID 2>/dev/null || true
```

### Extração Automatizada de Métricas via `tshark`:
```bash
# Extrair total de bytes trafegados no pcapng:
TOTAL_BYTES=$(tshark -r capture.pcapng -T fields -e frame.len | awk '{sum+=$1} END {print sum}')

# Contar retransmissões TCP:
TCP_RETX=$(tshark -r capture.pcapng -Y "tcp.analysis.retransmission" | wc -l)
```

---

## 4. Pipeline de Tratamento e Geração de Gráficos (Python)

Os scripts Python devem residir em `analysis/`:
1. `parse_logs.py`: Consolida CSVs e JSONs de todas as 10 repetições de cada cenário, computa médias, desvios padrões e percentis p90/p95.
2. `generate_plots.py`: Gera os gráficos no formato de publicação (300 DPI, fontes legíveis, tons elegantes, barras de erro).

### Gráficos Obrigatórios para o Relatório:
1. **Gráfico 1 (Cenário A):** Taxa de Injeção vs Goodput e Jitter (UDP Puro em 10, 50, 100, 250, 500 Mbps).
2. **Gráfico 2 (Cenário A):** Comparativo de Sobrecarga de Cabeçalho (UDP 8B vs TCP vs QUIC).
3. **Gráfico 3 (Cenário B):** Goodput e FCT para Arquivo de 100MB e 1GB (Barras comparativas: HTTP/1.1 vs HTTP/2 vs HTTP/3 com barra de erro de $\pm 1$ desvio padrão).
4. **Gráfico 4 (Cenário B):** Consumo de Recursos de CPU durante transferência massiva (Kernel vs User-space).
5. **Gráfico 5 (Cenário C):** FCT Médio e Percentil p95 sob diferentes taxas de perda (0%, 2%, 5%) para os 3 protocolos.
6. **Gráfico 6 (Cenário C):** CDF (Função de Distribuição Cumulativa) do FCT na transferência dos 100 objetos sob perda de 3% (evidenciando a cauda longa causada pelo HoL Blocking no HTTP/2).
