# 02. Especificação Detalhada dos Cenários e Matriz Experimental

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Curso:** Bacharelado em Sistemas de Informação  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)

Este documento estabelece as condições físicas e sintéticas de canal de rede, a modelagem dos perfis de carga e o detalhamento minucioso dos 12 testes experimentais obrigatórios estabelecidos no edital da 2ª Avaliação.

---

## 1. Condições dos Canais de Rede Emulados (`tc netem`)

A emulação do canal é injetada diretamente na interface de rede virtual (`eth0`) dos contêineres Docker através do utilitário `tc` com o módulo `netem` (*Network Emulator*).

### 1.1. Cenário 1: Rede Local (LAN) — Canal Ideal de Alta Performance
- **Atraso Unidirecional Injetado:** `0.5 ms` ($\implies \textbf{RTT total de 1.0 ms}$).
- **Taxa de Descarte Sintético (Packet Loss):** `0.0%` (Canal sem ruído ou interferência).
- **Largura de Banda:** Sem limitação artificial de taxa (vazão nativa do Docker bridge > 1 Gbps).
- **Comando de Aplicação:**
  ```bash
  docker exec --privileged <container_name> tc qdisc add dev eth0 root netem delay 0.5ms
  ```
- **Finalidade Científica:** Isolar o desempenho ótimo de cada protocolo em regime livre de perdas, permitindo mensurar a sobrecarga pura de processamento de cabeçalhos, custos de cifragem criptográfica do TLS 1.3 e eficiência das pilhas de software em espaço de usuário (*user space*) versus núcleo do sistema operacional (*kernel space*).

### 1.2. Cenário 2: Rede Geográfica / Móvel (WAN) — Canal Degradado e Ruidoso
- **Atraso Unidirecional Injetado:** `25.0 ms` ($\implies \textbf{RTT total de 50.0 ms}$).
- **Taxa de Descarte Sintético (Packet Loss):** `2.0%` (Taxa estocástica de perda de pacotes).
- **Comando de Aplicação:**
  ```bash
  docker exec --privileged <container_name> tc qdisc add dev eth0 root netem delay 25ms loss 2%
  ```
- **Finalidade Científica:** Expor os limites operacionais e os mecanismos de controle de congestionamento e recuperação de perdas. Demonstra empiricamente o colapso de vazão do algoritmo TCP CUBIC sob descarte contínuo e a superioridade de resiliência do QUIC / BBR ao manter fluxos independentes desacoplados.

---

## 2. Perfis de Carga Sintética

Para testar as duas dimensões fundamentais de desempenho na Web (largura de banda e concorrência/latência), o cliente automatizado submeterá os servidores a dois perfis padronizados de carga:

### 2.1. Carga A: Gargalo de Banda / Regime Permanente (Transferência Massiva)
- **Tamanho do Payload:** 1 arquivo binário estático de **50 MB** (`50MB.bin`).
- **Dimensão Analisada:** Vazão sustentada (*Throughput* / *Goodput*), saturação do canal, tempo total de carregamento e evolução da janela de congestionamento em transferências contínuas.
- **Hipótese Central:** No Cenário 1 (LAN), o TCP se sobressai devido às otimizações maduras de kernel (TSO, GRO e menor uso de CPU) contra o QUIC em user space. No Cenário 2 (WAN com 2% de perda), o TCP CUBIC colapsa violentamente sua janela de congestionamento (Tanenbaum Seção 6.5.11), enquanto o QUIC/BBR sustenta alta taxa de entrega.

### 2.2. Carga B: Gargalo de Latência e Multiplexação (Página Web Rica)
- **Tamanho do Payload:** Download concorrente de **100 objetos pequenos e independentes de 10 KB cada** (`obj_001.bin` a `obj_100.bin`), totalizando 1 MB transferido.
- **Dimensão Analisada:** Capacidade de multiplexação sobre canal persistente (*warm connection*), impacto do Bloqueio de Início de Linha (*Head-of-Line Blocking*), dispersão de percentis de latência (p50 e p99) e taxa de requisições por segundo (RPS).
- **Hipótese Central:** No HTTP/1.1, ocorre severo HoL blocking na aplicação ou sobrecarga de abertura paralela de sockets. No HTTP/2 (HTTPS), a multiplexação funciona perfeitamente na LAN, mas no Cenário WAN a perda de um único segmento TCP retém todos os 100 fluxos simultâneos no buffer do kernel. No HTTP/3, a perda atinge apenas o fluxo individual afetado, eliminando completamente o HoL blocking.

---

## 3. Matriz Experimental Obrigatória (Detalhamento dos 12 Testes)

| ID | Carga | Protocolo Alvo | Servidor Alvo | Cenário de Rede | Foco Analítico e Hipótese Científica |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **T01** | Carga A (50 MB) | HTTP/1.1 | `server_http11` (Porta 8080) | Cenário 1 (LAN: 1ms, 0%) | **Vazão máxima TCP em canal ideal:** Linha de base de throughput sem o overhead de criptografia TLS. Avalia a saturação pura da pilha de rede do kernel Linux. |
| **T02** | Carga A (50 MB) | HTTPS / TLS 1.3 | `server_http2_tls` (Porta 8443) | Cenário 1 (LAN: 1ms, 0%) | **Custo computacional de cifragem TLS 1.3:** Mensura a penalidade imposta pela cifra simétrica AES-GCM / ChaCha20-Poly1305 sobre o TCP em regime permanente. |
| **T03** | Carga A (50 MB) | HTTP/3 (QUIC) | `server_http3_quic` (Porta 9443) | Cenário 1 (LAN: 1ms, 0%) | **Eficiência do QUIC em user-space sem perdas:** Avalia a sobrecarga de context-switches e processamento UDP no espaço de usuário do Caddy/QUIC em comparação com o kernel TCP. |
| **T04** | Carga A (50 MB) | HTTP/1.1 | `server_http11` (Porta 8080) | Cenário 2 (WAN: 50ms, 2%) | **Sensibilidade do TCP CUBIC a perdas estocásticas:** Colapso drástico de vazão decorrente da redução severa de *cwnd* provocada pela função cúbica pós-perda (Tanenbaum Seção 6.5.11). |
| **T05** | Carga A (50 MB) | HTTPS / TLS 1.3 | `server_http2_tls` (Porta 8443) | Cenário 2 (WAN: 50ms, 2%) | **Degradação cumulativa de TCP CUBIC + TLS sob perdas:** Combinação da retração da janela do TCP com a latência de retransmissão de blocos cifrados. |
| **T06** | Carga A (50 MB) | HTTP/3 (QUIC) | `server_http3_quic` (Porta 9443) | Cenário 2 (WAN: 50ms, 2%) | **Resiliência do controle de congestionamento QUIC/BBR:** Sustentação de vazão e recuperação ágil de perdas em canal de alta latência e descarte contínuo (Tanenbaum Seções 6.6.1 e 6.6.2). |
| **T07** | Carga B (100x10KB) | HTTP/1.1 | `server_http11` (Porta 8080) | Cenário 1 (LAN: 1ms, 0%) | **Overhead de concorrência no HTTP/1.1:** Custo de sucessivos handshakes ou paralelização ineficiente na requisição de múltiplos pequenos recursos na LAN. |
| **T08** | Carga B (100x10KB) | HTTPS / TLS 1.3 | `server_http2_tls` (Porta 8443) | Cenário 1 (LAN: 1ms, 0%) | **Eficiência da multiplexação HTTP/2 em canal ideal:** Excelente aproveitamento do canal persistente aquecido com divisão de recursos em quadros sobre uma única conexão TCP. |
| **T09** | Carga B (100x10KB) | HTTP/3 (QUIC) | `server_http3_quic` (Porta 9443) | Cenário 1 (LAN: 1ms, 0%) | **Desempenho de múltiplos fluxos QUIC em rede limpa:** Comportamento da abertura instantânea de streams em paralelo sobre o canal QUIC inicializado. |
| **T10** | Carga B (100x10KB) | HTTP/1.1 | `server_http11` (Porta 8080) | Cenário 2 (WAN: 50ms, 2%) | **Severidade do HoL blocking na Camada de Aplicação:** Desempenho crítico decorrente da espera sequencial de respostas e da latência de 50ms acrescida de descarte de 2%. |
| **T11** | Carga B (100x10KB) | HTTPS / TLS 1.3 | `server_http2_tls` (Porta 8443) | Cenário 2 (WAN: 50ms, 2%) | **Severidade do HoL blocking na Camada de Transporte TCP:** Perda de pacotes isolados força a retenção de todos os fluxos multiplexados no buffer TCP, elevando violentamente o percentil p99. |
| **T12** | Carga B (100x10KB) | HTTP/3 (QUIC) | `server_http3_quic` (Porta 9443) | Cenário 2 (WAN: 50ms, 2%) | **Mitigação total do HoL blocking via fluxos UDP isolados:** A perda de datagramas atrasa exclusivamente o stream afetado, garantindo que os 99 demais continuem sendo entregues imediatamente. |

---

## 4. Rigor Experimental e Repetibilidade

Para assegurar validade científica aos testes e atender às exigências do edital:
1. **Número Mínimo de Repetições:** Cada um dos 12 testes será executado no mínimo **10 vezes de forma independente** ($N \ge 10$).
2. **Total de Amostragens da Bateria:**
   - Carga A (T01 a T06): $6 \text{ testes} \times 10 \text{ repetições} = 60 \text{ execuções de download de 50MB}$.
   - Carga B (T07 a T12): $6 \text{ testes} \times 10 \text{ repetições} = 60 \text{ execuções de lotes de 100 objetos}$.
   - Totalizando **120 ensaios experimentais completos**.
3. **Isolamento entre Amostras:** Entre cada repetição, haverá um intervalo de dissipação de buffers de 1 segundo (`sleep 1`) para evitar contaminação por pacotes remanescentes na interface virtual.
