# 00. Visão Geral, Objetivos Pedagógicos e Regras Críticas — 3ª Avaliação (N3)

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Curso:** Bacharelado em Sistemas de Informação  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)  
**Trabalho:** Terceira Avaliação (N3) — Análise Experimental de Controle de Congestionamento (TCP CUBIC vs. BBR) e Retomada de Sessão (0-RTT) em Redes Degradadas  
**Pontuação Total:** 100 Pontos

---

## 1. Visão Geral do Problema e Objetivos Pedagógicos

Este Trabalho Prático — correspondente à **3ª Avaliação (N3)** — dá continuidade direta à bancada experimental desenvolvida na avaliação anterior (N2), aproveitando a infraestrutura em contêineres Docker e a emulação de canal via Linux Traffic Control (`tc netem`). Dado o cronograma condensado de duas semanas, a arquitetura e o escopo foram otimizados para focar na análise empírica rigorosa de **dois mecanismos avançados da camada de transporte moderna**:

### 1.1. Mecanismo 1 (Bloco A): Controle de Congestionamento Baseado em Perda vs. Baseado em Modelo (TCP CUBIC vs. TCP BBR)
- **TCP CUBIC (Baseado em Perda — *Loss-Based*):** Algoritmo padrão nas distribuições Linux modernas (**Tanenbaum 6ª Ed., Seção 6.5.11**). O CUBIC interpreta **qualquer descarte de pacote** na rede como um sinal inequívoco de congestionamento nos buffers dos roteadores. Diante de uma perda estocástica (como os 2% do Cenário 2 WAN), o algoritmo aplica uma retração multiplicativa imediata na janela de congestionamento ($cwnd \leftarrow cwnd \times \beta$, onde $\beta \approx 0.7$). Em enlaces de alto Produto Largura de Banda-Atraso (BDP) com perdas aleatórias contínuas, a função cúbica $W_{\text{cubic}}(t) = C(t - K)^3 + W_{\text{max}}$ jamais consegue recuperar o platô $W_{\text{max}}$ antes do próximo descarte, provocando o colapso severo da vazão útil.
- **TCP BBR (*Bottleneck Bandwidth and Round-trip propagation time* — Baseado em Modelo):** Algoritmo desenvolvido pelo Google (**Tanenbaum 6ª Ed., Seção 6.6.2**) que abandona a premissa de que perda equivale a congestionamento. Em vez de reagir cegamente a descartes isolados, o BBR constrói um modelo explícito do caminho de rede estimando continuamente dois parâmetros físicos ortogonais:
  1. **Largura de banda máxima do gargalo ($BtlBw$ — *Bottleneck Bandwidth*)**, obtida pela taxa máxima recente de entrega de pacotes confirmados;
  2. **RTT mínimo de propagação ($RTprop$ — *Round-trip propagation time*)**, obtido pelo menor atraso de ida e volta observado na janela temporal.
- **Ponto de Operação Ótimo (Kleinrock):** Ao regular o ritmo de injeção de pacotes (*pacing rate*) em torno de $BtlBw$ e limitar os dados em voo (*inflight*) a um múltiplo estrito do Produto Largura de Banda-Atraso ($BDP = BtlBw \times RTprop$), o BBR mantém a tubulação cheia sem encher as filas dos roteadores (*bufferbloat*) e sustenta alta vazão mesmo sob 2% de perda estocástica.

### 1.2. Mecanismo 2 (Bloco B): Estabelecimento Rápido de Conexão e Retomada de Sessão no QUIC (1-RTT vs. 0-RTT)
- **HTTPS / HTTP/2 Tradicional (sobre TCP + TLS 1.3):** O estabelecimento de uma nova conexão segura requer handshakes em camadas separadas e sequenciais: primeiro o *3-way handshake* do TCP (**1 RTT**) e, em seguida, a negociação criptográfica do TLS 1.3 (**1 RTT**), totalizando **2 RTTs de espera pura** antes que o cliente possa enviar a requisição HTTP e mais **1 RTT** para receber o primeiro byte da resposta (**total de ~3 RTTs até o TTFB**).
- **HTTP/3 Cold Connection (QUIC 1-RTT):** Conforme detalhado em **Tanenbaum 6ª Ed., Seção 6.6.1**, o protocolo QUIC funde o handshake de transporte com o handshake criptográfico TLS 1.3 em um único passo sobre UDP. Em uma conexão fria (*Cold*), o estabelecimento completo consome apenas **1 RTT**, reduzindo o TTFB para **~2 RTTs** (1 RTT de handshake integrado + 1 RTT da requisição/resposta do objeto de 1 KB).
- **HTTP/3 Warm / Session Resumption (QUIC 0-RTT / Reaproveitamento):** Em reconexões subsequentes a um mesmo servidor (utilizando *Session Tickets* criptográficos do TLS 1.3 para *0-RTT Early Data* ou reaproveitamento de sessão estabelecida na mesma chamada do `curl`), o cliente envia os dados da requisição HTTP já no primeiro pacote (**0 RTT de espera de handshake**), reduzindo o TTFB para apenas **~1 RTT** de propagação do pedido/resposta.

---

## 2. Quadro Comparativo Teórico dos Mecanismos Avaliados

### 2.1. Bloco A — Algoritmos de Controle de Congestionamento TCP
| Característica | TCP CUBIC (Seção 6.5.11) | TCP BBR (Seção 6.6.2) |
| :--- | :--- | :--- |
| **Paradigma de Controle** | Baseado em Perda (*Loss-Based* / AIMD Cúbico) | Baseado em Modelo (*Model-Based* / Pacing por BDP) |
| **Sinal de Congestionamento** | Descarte de pacotes (ACKs duplicados / Timeout) | Aumento do RTT além de $RTprop$ e saturação de $BtlBw$ |
| **Ponto de Operação** | Enche os buffers até ocorrer descarte (*Bufferbloat*) | Opera no ponto ótimo de Kleinrock ($Inflight \approx BDP$) |
| **Reação a 2% de Perda em WAN (50ms)** | **Colapso severo de vazão** (reduções sucessivas de $cwnd$) | **Alta resiliência** (ignora perdas estocásticas não-congestionais) |

### 2.2. Bloco B — Modos de Conexão e Handshake Web (Cenário WAN: RTT = 50 ms, Perda = 0%)
| Modo de Conexão | Protocolo Base | RTTs de Handshake | RTTs até o 1º Byte (TTFB) | Latência Teórica Esperada (RTT = 50 ms) |
| :--- | :---: | :---: | :---: | :---: |
| **E04: HTTPS (HTTP/2)** | TCP + TLS 1.3 | **2 RTTs** (1 TCP + 1 TLS 1.3) | **3 RTTs** (2 Handshake + 1 Req/Resp) | $\approx 150\text{ ms} + t_{\text{proc}}$ |
| **E05: HTTP/3 Cold (1-RTT)** | QUIC (UDP + TLS 1.3) | **1 RTT** (QUIC+TLS Integrado) | **2 RTTs** (1 Handshake + 1 Req/Resp) | $\approx 100\text{ ms} + t_{\text{proc}}$ |
| **E06: HTTP/3 Warm / Resumption** | QUIC (0-RTT / Reuso) | **0 RTT** (Sem espera de Handshake) | **1 RTT** (Apenas 1 Req/Resp) | $\approx 50\text{ ms} + t_{\text{proc}}$ |

---

## 3. Requisitos Mandatórios do Ambiente Experimental

1. **Arquitetura Simplificada via `docker-compose.yml`:**
   - **Reuso de Infraestrutura:** Utilizam-se apenas **dois contêineres de servidor**:
     - `server_tcp_cc` (`networkstatic/iperf3` em modo `-s`, IP `172.20.0.10`) para os testes de CUBIC vs. BBR (Bloco A);
     - `server_http3_quic` (`caddy:2.7-alpine`, IP `172.20.0.30`) servindo HTTP/2 e HTTP/3 para os testes de Handshake e Session Resumption (Bloco B).
   - **Cliente Padronizado via Contêiner:** Dispensa-se o desenvolvimento de um cliente assíncrono complexo em Python (`aioquic`). Utiliza-se `curl` (com suporte nativo a `--http3`) e `iperf3` diretamente de contêiner cliente padronizado (`client_bench`, IP `172.20.0.50`), orquestrados por um script automatizado (`run_n3.py` / `run_n3.sh`).
2. **Permissão `cap_add: - NET_ADMIN` Obrigatória:**
   - Todos os contêineres devem declarar `cap_add: - NET_ADMIN` para permitir a injeção e limpeza de regras `tc netem` nas interfaces virtuais (`eth0`).
3. **Três Cenários de Emulação `tc netem`:**
   - **Cenário 1 (LAN - Canal Ideal):** Atraso unidirecional de `0.5ms` ($\text{RTT} = 1\text{ ms}$) e `0%` de perda.
   - **Cenário 2 (WAN - Canal Degradado):** Atraso unidirecional de `25ms` ($\text{RTT} = 50\text{ ms}$) e `2%` de perda estocástica.
   - **Cenário 3 (WAN sem Perda - Isolamento de Latência para Handshake):** Atraso unidirecional de `25ms` ($\text{RTT} = 50\text{ ms}$) e `0%` de perda.
   - **Limpeza da Interface:** Remoção obrigatória da disciplina com `tc qdisc del dev eth0 root`.
4. **Rigor Estatístico ($N \ge 5$):**
   - Execução de no **mínimo 5 repetições por teste** (E01 a E06) para extração de média ($\bar{x}$), desvio padrão ($s$) e total de retransmissões.

---

## 4. Matriz Experimental Reduzida (6 Testes Essenciais)

### Bloco A: Impacto do Controle de Congestionamento (Fluxo de 15s via `iperf3`)
Alterando o algoritmo de controle de congestionamento TCP via parâmetro `-C cubic` e `-C bbr` no `iperf3` (ex.: `iperf3 -c 172.20.0.10 -t 15 -C bbr -J`):

| ID | Algoritmo / Protocolo | Cenário `tc netem` | Métrica Principal | Foco Analítico Principal |
| :---: | :---: | :---: | :---: | :--- |
| **E01** | TCP CUBIC | LAN (1 ms, 0% perda) | Vazão (Mbps) e Retransmissões | Baseline de capacidade máxima |
| **E02** | TCP CUBIC | WAN (50 ms, 2% perda) | Vazão (Mbps) e Retransmissões | Colapso da janela *cwnd* por perda |
| **E03** | TCP BBR | WAN (50 ms, 2% perda) | Vazão (Mbps) e Retransmissões | Resiliência do modelo baseado em BDP |

### Bloco B: Latência de Handshake e Session Resumption no HTTP/3 (`curl`)
Medindo o tempo até o início da transferência (`%{time_starttransfer}`) para um objeto pequeno de **1 KB** sob cenário **WAN sem perda (50 ms RTT, 0% perda)**, isolando o custo puro dos RTTs:

| ID | Modo de Conexão | Cenário `tc netem` | Métrica Principal | Foco Analítico Principal |
| :---: | :---: | :---: | :---: | :--- |
| **E04** | HTTPS (HTTP/2 sobre TCP+TLS) | WAN (50 ms, 0% perda) | TTFB (`time_starttransfer`) | Custo cumulativo de handshakes (TCP + TLS) |
| **E05** | HTTP/3 Cold (1-RTT) | WAN (50 ms, 0% perda) | TTFB (`time_starttransfer`) | Handshake integrado QUIC |
| **E06** | HTTP/3 Warm / Resumption | WAN (50 ms, 0% perda) | TTFB (`time_starttransfer`) | Redução de latência via reaproveitamento / 0-RTT |

---

## 5. Rubrica Detalhada de Avaliação (100 Pontos)

| Eixo de Avaliação | Pontuação | Critérios de Correção |
| :--- | :---: | :--- |
| **1. Infraestrutura Docker e Automação `tc netem`** | **10 Pontos** | Funcionamento dos contêineres, precisão sintática na configuração de RTT e perda via `tc netem`, limpeza das interfaces e execução automatizada dos testes (`run_n3.sh` ou `run_n3.py`). |
| **2. Coleta Estatística e Visualização Gráfica** | **10 Pontos** | Execução de 5 amostras por teste, exportação dos dados brutos (CSV/JSON) e geração programática de **2 gráficos comparativos, com barras de erro** (desvio padrão) e eixos devidamente rotulados. |
| **3. Relatório Técnico e Articulação Teórica** | **50 Pontos** | Clareza e concisão textual; fundamentação rigorosa dos resultados empíricos com base nos mecanismos do CUBIC, BBR e QUIC (**Tanenbaum 6ª Ed., Seções 6.5.11, 6.6.1 e 6.6.2**). **Utilizar o formato de artigo da SBRC. Enviar no formato PDF (mínimo 4, máximo 6 páginas).** |
| **4. Vídeo (Link)** | **30 Pontos** | Vídeo carregado no YouTube com explicação do projeto e dos resultados; **o vídeo deve ter entre 15 e 25 minutos**. |

---

## 6. Tabela de Penalidades Previstas no Edital

| Infração Técnica / Acadêmica | Penalidade Direta |
| :--- | :---: |
| Ausência de **barras de erro (desvio padrão)** nos gráficos | **-10 Pontos** |
| Relatório puramente descritivo (sem explicar os porquês teóricos com base nos protocolos — Tanenbaum 6ª Ed.) | **-20 Pontos** |
| Plágio de código ou de texto entre equipes | **NOTA ZERO (0,0) para todos os envolvidos** |
| Envios sem o vídeo (explicando o projeto), relatório (PDF do projeto com os resultados) e os arquivos-fonte | **NOTA ZERO (0,0)** |

---

## 7. 🚨 REGRA ELIMINATÓRIA CRÍTICA (NOTA ZERO)

> [!CAUTION]
> ### CRITÉRIO EXCLUDENTE DA 3ª AVALIAÇÃO:
> A submissão via SIGAA em arquivo único `.zip` (`TP3_Redes2_JoaoMarcosSousaRufinoLeal.zip`) exige obrigatoriamente os três pilares abaixo:
> 1. **Repositório de Código e Automação Completo:** `docker-compose.yml` configurado, scripts de automação (`run_n3.py` / `run_n3.sh`), scripts de gráficos e dados brutos exportados (CSV/JSON);
> 2. **Relatório Técnico Conciso em PDF (mínimo 4, máximo 6 páginas):** No formato de artigo da **SBRC**, contendo os 2 gráficos com barras de erro, a Tabela Resumo e a discussão fundamentada em Tanenbaum (6ª Ed., Seções 6.5.11, 6.6.1 e 6.6.2);
> 3. **Link Funcional do Vídeo no YouTube (entre 15 e 25 minutos):** Posicionado de forma visível e clicável logo na **primeira página do relatório técnico**.
>
> **Envios sem o vídeo, sem o relatório em PDF ou sem os arquivos-fonte recebem automaticamente NOTA 0,0.**

---

## 8. Instruções de Submissão Final (SIGAA)

- **Canal de Submissão:** Exclusivamente via **SIGAA**.
- **Formato do Arquivo:** Arquivo único compactado `.zip`.
- **Nomenclatura Obrigatória:**
  `TP3_Redes2_JoaoMarcosSousaRufinoLeal.zip`
