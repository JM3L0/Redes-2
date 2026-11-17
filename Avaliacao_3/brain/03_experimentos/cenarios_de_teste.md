# 02. Especificação dos Cenários e Matriz Experimental Reduzida (E01 a E06) — 3ª Avaliação (N3)

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Curso:** Bacharelado em Sistemas de Informação  
**Equipe:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`) & Marcos Willian de Sousa e Silva (`marcos.sousa@ufpi.edu.br`)

Este documento detalha os três cenários de rede emulados via `tc netem`, a estrutura dos dois blocos experimentais e a especificação técnica e científica de cada um dos **6 testes essenciais (E01 a E06)** definidos na Seção 4 do edital da 3ª Avaliação.

---

## 1. Condições dos Três Canais de Rede Emulados (`tc netem`)

Diferentemente da N2 (que possuía apenas dois cenários), a 3ª Avaliação introduz um **terceiro cenário específico sem perda** para isolar com precisão cirúrgica o custo em milissegundos dos RTTs de handshake no Bloco B sem interferência de timeouts de retransmissão.

### 1.1. Cenário 1: LAN — Canal Ideal (Usado em E01)
- **Atraso Unidirecional (`tc netem`):** `0.5 ms` ($\implies \textbf{RTT total = 1.0 ms}$).
- **Perda de Pacotes:** `0%`.
- **Comandos de Aplicação:**
  ```bash
  docker exec --privileged server_tcp_cc tc qdisc add dev eth0 root netem delay 0.5ms
  docker exec --privileged server_http3_quic tc qdisc add dev eth0 root netem delay 0.5ms
  docker exec --privileged client_bench tc qdisc add dev eth0 root netem delay 0.5ms
  ```
- **Finalidade Científica:** Estabelecer o *baseline* de capacidade máxima de vazão da pilha TCP (CUBIC) em ambiente virtualizado livre de descartes e com latência mínima.

### 1.2. Cenário 2: WAN — Canal Degradado (Usado em E02 e E03)
- **Atraso Unidirecional (`tc netem`):** `25 ms` ($\implies \textbf{RTT total = 50.0 ms}$).
- **Perda de Pacotes:** `2%` estocástica.
- **Comandos de Aplicação:**
  ```bash
  docker exec --privileged server_tcp_cc tc qdisc add dev eth0 root netem delay 25ms loss 2%
  docker exec --privileged server_http3_quic tc qdisc add dev eth0 root netem delay 25ms loss 2%
  docker exec --privileged client_bench tc qdisc add dev eth0 root netem delay 25ms loss 2%
  ```
- **Finalidade Científica:** Submeter os algoritmos de controle de congestionamento **TCP CUBIC** (E02) e **TCP BBR** (E03) a um enlace de alto Produto Largura de Banda-Atraso (BDP) combinado com perdas aleatórias não-congestionais (2%), expondo o colapso da janela `cwnd` do CUBIC versus a resiliência do modelo baseado em BDP do BBR.

### 1.3. Cenário 3: WAN sem Perda — Isolamento de Latência para Handshake (Usado em E04, E05 e E06)
- **Atraso Unidirecional (`tc netem`):** `25 ms` ($\implies \textbf{RTT total = 50.0 ms}$).
- **Perda de Pacotes:** `0%`.
- **Comandos de Aplicação:**
  ```bash
  docker exec --privileged server_http3_quic tc qdisc add dev eth0 root netem delay 25ms
  docker exec --privileged client_bench tc qdisc add dev eth0 root netem delay 25ms
  ```
- **Finalidade Científica:** Isolar o custo determinístico dos RTTs de estabelecimento de conexão e transferência de um objeto pequeno de **1 KB** (`1KB.bin`), eliminando a variância estocástica de descartes de pacotes durante o handshake. Com $\text{RTT} = 50\text{ ms}$, cada RTT adicional de handshake acrescenta exatamente $\approx 50\text{ ms}$ ao *Time to First Byte* (`time_starttransfer`).

---

## 2. Detalhamento dos Dois Blocos Experimentais e dos 6 Testes (E01 a E06)

### 2.1. Bloco A: Impacto do Controle de Congestionamento (Fluxo de 15s via `iperf3`)

Nos testes E01, E02 e E03, o cliente `iperf3` gera um fluxo contínuo de dados TCP durante **15 segundos** (`-t 15`) contra o contêiner `server_tcp_cc` (`172.20.0.10`), alternando o algoritmo de controle de congestionamento via flag `-C cubic` ou `-C bbr` e exportando o relatório estruturado em JSON (`-J`):

| ID | Algoritmo / Protocolo | Cenário `tc netem` | Comando Executado no Cliente | Métrica Principal | Foco Analítico e Hipótese Científica |
| :---: | :---: | :---: | :--- | :---: | :--- |
| **E01** | **TCP CUBIC** | **Cenário 1: LAN** (`1 ms` RTT, `0%` perda) | `iperf3 -c 172.20.0.10 -t 15 -C cubic -J` | Vazão (Mbps) e Retransmissões | **Baseline de capacidade máxima:** Sem perdas e com RTT de 1 ms, a janela `cwnd` do CUBIC cresce rapidamente até saturar a capacidade da bridge virtual Docker (tipicamente na casa de centenas de Mbps a múltiplos Gbps), com número de retransmissões nulo ou residual. |
| **E02** | **TCP CUBIC** | **Cenário 2: WAN** (`50 ms` RTT, `2%` perda) | `iperf3 -c 172.20.0.10 -t 15 -C cubic -J` | Vazão (Mbps) e Retransmissões | **Colapso da janela *cwnd* por perda (Tanenbaum 6ª Ed., Seção 6.5.11):** O CUBIC interpreta cada perda estocástica de 2% como congestionamento e reduz $cwnd$ em 30% ($\beta = 0.7$). Como o RTT é elevado (50 ms), a recuperação pós-perda é lenta e interrompida por novos descartes antes de atingir $W_{\max}$, derrubando drasticamente a vazão para poucos Mbps. |
| **E03** | **TCP BBR** | **Cenário 2: WAN** (`50 ms` RTT, `2%` perda) | `iperf3 -c 172.20.0.10 -t 15 -C bbr -J` | Vazão (Mbps) e Retransmissões | **Resiliência do modelo baseado em BDP (Tanenbaum 6ª Ed., Seção 6.6.2):** O BBR estima continuamente a largura de banda de gargalo ($BtlBw$) e o RTT mínimo ($RTprop = 50\text{ ms}$), mantendo a taxa de envio (*pacing*) alinhada ao BDP real sem reduzir cegamente a janela a cada perda estocástica de 2%, alcançando vazão muitas vezes superior ao CUBIC na WAN. |

---

### 2.2. Bloco B: Latência de Handshake e Session Resumption no HTTP/3 (`curl`)

Nos testes E04, E05 e E06, o contêiner cliente requisita um objeto estático de **1 KB** (`https://172.20.0.30/1KB.bin`) hospedado no servidor Caddy (`server_http3_quic`, `172.20.0.30`) sob o **Cenário 3 (WAN sem perda: 50 ms RTT, 0% perda)**, extraindo a métrica `%{time_starttransfer}` (TTFB) do `curl`:

| ID | Modo de Conexão | Cenário `tc netem` | Modo de Execução no `curl` | Métrica Principal | Foco Analítico e Hipótese Científica |
| :---: | :---: | :---: | :--- | :---: | :--- |
| **E04** | **HTTPS (HTTP/2 sobre TCP+TLS)** | **Cenário 3: WAN** (`50 ms` RTT, `0%` perda) | `curl -k --http2 -o /dev/null -s -w "%{time_starttransfer}\n" https://172.20.0.30/1KB.bin` | TTFB (`time_starttransfer` em ms) | **Custo cumulativo de handshakes (TCP + TLS):** Exige 1 RTT para o 3-way handshake TCP (`SYN` / `SYN-ACK`) + 1 RTT para o handshake TLS 1.3 + 1 RTT para enviar o `GET` e receber o 1º byte da resposta $\implies \mathbf{3\text{ RTTs} \approx 150\text{ ms}}$. |
| **E05** | **HTTP/3 Cold (1-RTT)** | **Cenário 3: WAN** (`50 ms` RTT, `0%` perda) | `curl -k --http3-only -o /dev/null -s -w "%{time_starttransfer}\n" https://172.20.0.30/1KB.bin` (nova invocação limpa) | TTFB (`time_starttransfer` em ms) | **Handshake integrado QUIC (Tanenbaum 6ª Ed., Seção 6.6.1):** O QUIC unifica o estabelecimento de transporte e a negociação criptográfica TLS 1.3 em apenas 1 RTT sobre UDP + 1 RTT para requisição/resposta $\implies \mathbf{2\text{ RTTs} \approx 100\text{ ms}}$ (economia de ~50 ms / 1 RTT frente ao HTTP/2). |
| **E06** | **HTTP/3 Warm / Resumption** | **Cenário 3: WAN** (`50 ms` RTT, `0%` perda) | Requisições sequenciais na mesma chamada do `curl` / reutilização de sessão: `curl -k --http3-only -o /dev/null -s -w "%{time_starttransfer}\n" https://172.20.0.30/1KB.bin https://172.20.0.30/1KB.bin` (extraindo o TTFB da 2ª requisição) | TTFB (`time_starttransfer` em ms) | **Redução de latência via reaproveitamento / 0-RTT:** Seguindo a dica oficial da página 7 do edital, na requisição subsequente (Warm / Resumed) o custo do handshake é completamente eliminado (**0 RTT de handshake**), restando apenas 1 RTT de propagação do pedido/resposta $\implies \mathbf{1\text{ RTT} \approx 50\text{ ms}}$. |

---

## 3. Protocolo de Execução e Repetibilidade Estatística ($N \ge 5$)

1. **Mínimo de 5 Repetições por Teste:** Conforme exigido na Seção 4 e no Eixo 2 da Rubrica, cada um dos 6 testes (E01 a E06) é executado no mínimo **5 vezes de forma independente** ($N = 5$), totalizando:
   - **Bloco A:** $3\text{ testes} \times 5\text{ repetições} \times 15\text{ s} = 15\text{ fluxos TCP de 15 segundos}$ (225 segundos de tráfego `iperf3`);
   - **Bloco B:** $3\text{ testes} \times 5\text{ repetições} = 15\text{ medições independentes de TTFB via curl}$.
2. **Isolamento entre Repetições:**
   - Entre cada amostra do Bloco A, aguarda-se 1 a 2 segundos e limpa-se o cache de métricas de rota TCP do kernel (`ip route flush cache`) para que o cache de `ssthresh` de uma execução anterior não contamine a próxima repetição.
   - No Bloco B, cada repetição de **E04** e **E05** é invocada em um processo `curl` recém-inicializado (garantindo *Cold Connection* real sem tickets prévios), enquanto em **E06** mede-se explicitamente a requisição subsequente conforme a dica de execução do edital.
