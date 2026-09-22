# 02. Especificação Detalhada dos Cenários de Teste

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** UFPI — Bacharelado em Sistemas de Informação

Este documento estabelece as configurações exatas de rede, comandos de disparo, tamanhos de carga e hipóteses científicas para os três cenários mandatórios de avaliação.

---

## 🔬 Cenário A: Favorável ao UDP Puro
**Tema:** Aplicações em Tempo Real e Latência Mínima (IoT, Telemetria, VoIP/Áudio)

### 1. Condições do Canal de Rede
- **RTT:** Menor que 5 ms (emulação com atraso de 1 a 2 ms no `netem`).
- **Taxa de Descarte (Packet Loss):** 0.0% (Canal fiável e sem interferência).
- **Largura de Banda:** Sem gargalo artificial (1 Gbps+).
- **Comando `tc` no cliente:**
  ```bash
  tc qdisc del dev eth0 root 2>/dev/null || true
  tc qdisc add dev eth0 root netem delay 1.5ms
  ```

### 2. Padrão de Carga e Parâmetros
- **Carga:** Transmissão de pequenos datagramas a taxas sintéticas crescentes.
- **Tamanho do Datagrama:** 128 bytes e 256 bytes (simulando payloads típicos de telemetria MQTT/CoAP ou pacotes de codec de voz Opus).
- **Taxas avaliadas:** 10 Mbps, 50 Mbps, 100 Mbps, 250 Mbps e 500 Mbps.
- **Duração de cada teste:** 10 segundos por rodada.
- **Repetições:** 10 repetições por taxa de transmissão.
- **Comandos de Execução:**
  - **UDP Puro (via iperf3):**
    ```bash
    iperf3 -c 172.28.0.10 -u -b ${BANDWIDTH}M -l 128 -t 10 --json > udp_${BANDWIDTH}m_rep${REP}.json
    ```
  - **Comparativo com TCP e QUIC (para contraste de sobrecarga):**
    Envio contínuo de pequenos registros via stream TCP/TLS e QUIC com medição de latência unidirecional e jitter.

### 3. Métricas e Comportamentos Esperados
- **Ausência de Controle de Congestionamento:** O UDP injeta tráfego na taxa solicitada sem recuo exponencial (AIMD / CUBIC / BBR).
- **Sobrecarga de Cabeçalho Mínima:** Cabeçalho de transporte fixo em **8 bytes** (vs. 20-60 bytes no TCP e headers variáveis com criptografia no QUIC).
- **Menor consumo de ciclos de CPU:** Quase zero overhead computacional de processamento de ACKs e timers.

---

## 📦 Cenário B: Favorável ao TCP
**Tema:** Transferência Massiva de Dados em Canal Estável (Download de Grandes Arquivos)

### 1. Condições do Canal de Rede
- **RTT:** ~ 20 ms constante e uniforme (atraso de 10 ms em cada sentido).
- **Taxa de Descarte (Packet Loss):** 0.0% (Canal fiável).
- **Largura de Banda:** 200 Mbps a 500 Mbps configurada via `tbf` ou banda livre de contêiner.
- **Comando `tc` no cliente:**
  ```bash
  tc qdisc del dev eth0 root 2>/dev/null || true
  tc qdisc add dev eth0 root netem delay 10ms
  ```

### 2. Padrão de Carga e Parâmetros
- **Carga:** Ficheiros de grande porte:
  - Ficheiro Médio: `100MB.bin`
  - Ficheiro Grande: `500MB.bin` ou `1GB.bin`
- **Protocolos Comparados:**
  1. **HTTP/1.1 (TCP + TLS 1.3):** Conexão única mantida (Keep-Alive).
  2. **HTTP/2 (TCP + TLS 1.3):** Fluxo multiplexado sobre TCP.
  3. **HTTP/3 (QUIC + UDP):** Fluxo único em user-space.
- **Repetições:** 10 repetições completas para cada combinação (Protocolo x Tamanho de Ficheiro).
- **Comandos de Execução:**
  ```bash
  # HTTP/1.1
  curl -k --http1.1 -w "%{time_total},%{speed_download},%{size_download}\n" \
       -o /dev/null https://server/100MB.bin

  # HTTP/2
  curl -k --http2 -w "%{time_total},%{speed_download},%{size_download}\n" \
       -o /dev/null https://server/100MB.bin

  # HTTP/3 (QUIC)
  curl -k --http3-only -w "%{time_total},%{speed_download},%{size_download}\n" \
       -o /dev/null https://server/100MB.bin
  ```

### 3. Métricas e Comportamentos Esperados
- **Otimizações de Kernel do TCP (TSO / GRO / LRO):** O TCP é processado diretamente no subsistema de rede do kernel Linux com auxílio de offloading de placa de rede virtual, gerando menos interrupções e trocas de contexto.
- **Overhead de CPU do QUIC em User-Space:** Como o QUIC roda majoritariamente no espaço do usuário (user-space), a criptografia por pacote e a emissão via syscalls UDP (`sendmsg`/`sendmmsg`) impõem maior custo de CPU e leve desvantagem de vazão frente ao TCP maduro em canal limpo.
- **Goodput e Saturação:** Saturação máxima e consistente da banda pelo TCP.

---

## ⚡ Cenário C: Favorável ao QUIC
**Tema:** Ligação Móvel / Instável com Concorrência de Objetos e Alta Latência

### 1. Condições do Canal de Rede
- **RTT:** Alto, igual ou superior a 100 ms (atraso de 50 ms a 75 ms no `netem`, simulando conexão intercontinental ou 4G/5G com bufferbloat).
- **Taxa de Descarte (Packet Loss):** Perda aleatória controlada entre **2% e 5%** (ex: baterias com 2%, 3.5% e 5%).
- **Comando `tc` no cliente:**
  ```bash
  tc qdisc del dev eth0 root 2>/dev/null || true
  tc qdisc add dev eth0 root netem delay 50ms loss 3%
  ```

### 2. Padrão de Carga e Parâmetros
- **Carga 1 (Concorrência Web):** Requisições simultâneas a um conjunto de **50 a 100 objetos independentes** (recursos web simulados de 50 KB a 500 KB, totalizando uma página web moderna de ~10 MB).
- **Carga 2 (Reconexão e Handshake):** Teste de reconexão sequencial com e sem 0-RTT Session Resumption.
- **Protocolos Comparados:**
  1. **HTTP/1.1 (TCP + TLS 1.3):** Paralelismo via múltiplas conexões TCP (pool de até 6 conexões simultâneas).
  2. **HTTP/2 (TCP + TLS 1.3):** Multiplexação em conexão TCP única (expondo o problema do Head-of-Line Blocking de transporte).
  3. **HTTP/3 (QUIC):** Multiplexação nativa em streams independentes sobre QUIC.
- **Repetições:** 10 repetições por cenário de perda e protocolo.
- **Comando de Carga Paralela (via curl / xargs / script Python):**
  ```bash
  # Disparo paralelo de 50 objetos
  cat objects_list.txt | xargs -n 1 -P 10 curl -k --http3-only -s -o /dev/null
  ```

### 3. Métricas e Comportamentos Esperados
- **Eliminação do Head-of-Line (HoL) Blocking:**
  - No HTTP/2 sobre TCP: A perda de 1 único segmento na fila TCP congela **todos** os streams multiplexados até que ocorra a retransmissão e ordenação pelo kernel.
  - No HTTP/3 (QUIC): Apenas o stream que perdeu o pacote sofre atraso; todos os outros 99 objetos continuam sendo consumidos imediatamente pela aplicação.
- **Handshake Integrado TLS 1.3 (1-RTT e 0-RTT):**
  - TCP + TLS 1.3 requer 2 RTTs para o primeiro byte útil (1 RTT TCP SYN/ACK + 1 RTT TLS Client/Server Hello).
  - QUIC combina o handshake de transporte e criptográfico em **1 RTT** (e **0-RTT** em reconexões com Session Tickets). Com RTT de 100ms, isso economiza 100ms a 200ms só na conexão!
- **Goodput Superior sob Perda Contínua:** QUIC mantém FCT significativamente menor que HTTP/2 sob taxa de perda de 3% a 5%.

---

## 📋 Matriz Resumo dos Testes

| ID | Cenário | Protocolo | Métricas Primárias | Repetições | Arquivos de Saída |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A1** | UDP Baixa Latência | UDP (iperf3) | Vazão, Perda, Jitter, CPU | 10 por taxa (10 a 500M) | `cenario_a_udp.json`, `.pcapng` |
| **B1** | TCP Massivo | HTTP/1.1 (TCP) | FCT, Goodput, CPU Kernel | 10 por arquivo (100M, 1G) | `cenario_b_h1.csv`, `.pcapng` |
| **B2** | TCP Massivo | HTTP/2 (TCP) | FCT, Goodput, CPU Kernel | 10 por arquivo (100M, 1G) | `cenario_b_h2.csv`, `.pcapng` |
| **B3** | TCP Massivo | HTTP/3 (QUIC) | FCT, Goodput, CPU User-space | 10 por arquivo (100M, 1G) | `cenario_b_h3.csv`, `.pcapng` |
| **C1** | QUIC Concorrência | HTTP/1.1 (Multi-TCP) | FCT Total, p90, p95 FCT | 10 por perda (2%, 3%, 5%) | `cenario_c_h1.csv`, `.pcapng` |
| **C2** | QUIC Concorrência | HTTP/2 (HoL TCP) | FCT Total, p90, p95 FCT | 10 por perda (2%, 3%, 5%) | `cenario_c_h2.csv`, `.pcapng` |
| **C3** | QUIC Concorrência | HTTP/3 (QUIC Streams) | FCT Total, p90, p95 FCT | 10 por perda (2%, 3%, 5%) | `cenario_c_h3.csv`, `.pcapng` |
