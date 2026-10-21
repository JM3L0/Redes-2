# 00. Visão Geral, Objetivos e Regras Críticas

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Curso:** Bacharelado em Sistemas de Informação  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)  
**Trabalho:** 2ª Avaliação Prática: Estudo Experimental de Desempenho de Protocolos Web (HTTP/1.1 vs HTTPS/TLS vs HTTP/3-QUIC) em Ambiente Emulado com Docker e Python  
**Peso Acadêmico:** 50% da pontuação total da 2ª Avaliação (N2) — Valor total: 100 pontos

---

## 1. Visão Geral do Problema e Objetivos Pedagógicos

Este trabalho prático foi elaborado para conduzir o aluno da abstração conceitual à análise experimental rigorosa dos protocolos das camadas de aplicação e de transporte que estruturam a Web contemporânea. A avaliação empírica sob condições estritamente controladas de rede permite compreender como decisões arquiteturais de projeto de protocolos impactam a latência, a vazão e a entrega de dados em escala global.

Com base no referencial teórico clássico de redes (Tanenbaum, Kurose & Ross, RFCs do IETF), os ensaios investigam três fenômenos fundamentais:

### 1.1. Overhead de Handshakes e Latência Inicial (Cold TTFB)
- **HTTP/1.1 (sobre TCP em texto claro):** O estabelecimento da conexão exige a troca de mensagens de controle em 3 vias (*3-way handshake*: SYN, SYN-ACK, ACK), consumindo exatamente **1 RTT** antes do envio do primeiro byte de dados da aplicação.
- **HTTPS / HTTP/2 (sobre TCP + TLS 1.3):** Acopla a camada criptográfica de segurança sobre a conexão TCP já estabelecida. São necessários **2 RTTs cumulativos** de latência inicial (1 RTT para o handshake TCP + 1 RTT para a negociação de parâmetros e chaves do TLS 1.3).
- **HTTP/3-QUIC (sobre datagramas UDP):** O protocolo QUIC funde o handshake de transporte com o handshake criptográfico do TLS 1.3 em um único procedimento integrado de **1 RTT** (ou **0-RTT** em cenários de reconexão via *session resumption*).
- **Impacto Avaliado:** Mensuração do *Time to First Byte* (TTFB) e seus reflexos diretos na Qualidade de Experiência (*Quality of Experience* - QoE).

### 1.2. Bloqueio de Início de Linha (*Head-of-Line* - HoL Blocking)
- **HTTP/1.1:** O HoL blocking manifesta-se prioritariamente na **Camada de Aplicação**. As requisições enviadas sobre o mesmo canal TCP precisam ser processadas e respondidas em ordem estritamente sequencial (ou mitigadas de forma custosa pela abertura de múltiplas conexões TCP paralelas).
- **HTTPS (HTTP/2):** Resolve o HoL blocking na aplicação ao introduzir a multiplexação por quadros binários sobre uma única conexão TCP. No entanto, desloca o gargalo para a **Camada de Transporte TCP**: como o TCP exige entrega sequencial ininterrupta do buffer, a perda de um único segmento TCP força o sistema operacional a reter todos os dados de todos os fluxos multiplexados até a retransmissão do pacote perdido ser confirmada.
- **HTTP/3-QUIC:** Elimina o HoL blocking em ambas as camadas ao estruturar fluxos (*streams*) independentes e isolados encapsulados em datagramas UDP. A perda de um pacote afeta única e exclusivamente o stream ao qual pertence, permitindo a progressão livre dos demais.

### 1.3. Efeito das Condições de Canal e Controle de Congestionamento
- **TCP CUBIC:** A injeção de latência de 50ms com 2% de perda estocástica expõe as fragilidades do controle de congestionamento do TCP no kernel. O CUBIC interpreta qualquer descarte como congestionamento severo, colapsando a janela de congestionamento (*cwnd*) e congelando buffers de aplicação durante as retransmissões.
- **QUIC / BBR:** O QUIC desacopla o controle de perdas da trava de fluxo e utiliza estimativas de largura de banda de gargalo e RTT mínimo (BBR), sustentando vazão e taxas de requisição por segundo (RPS) substancialmente superiores.

---

## 2. Tabela Comparativa Arquitetural dos Protocolos

| Protocolo Web | Protocolo de Transporte Base | Mecanismo de Segurança | Mecanismo de Multiplexação | Suscetibilidade ao HoL Blocking |
| :--- | :---: | :---: | :---: | :--- |
| **HTTP/1.1** | TCP | Opcional (TLS sobre TCP) | Inexistente (requer conexões TCP paralelas) | **Alta** (Restrita à Camada de Aplicação) |
| **HTTPS (HTTP/2)** | TCP | Obrigatório (TLS 1.3) | Multiplexação por quadros em conexão única | **Média/Alta** (Transferida para a Camada de Transporte TCP) |
| **HTTP/3** | UDP (QUIC) | Integrado (TLS 1.3 sobre QUIC) | Fluxos (*streams*) nativos e independentes | **Nula** (Eliminado nas camadas de Aplicação e Transporte) |

---

## 3. Requisitos Mandatórios do Ambiente Experimental

1. **Isolamento Total em Contêineres:** Toda a infraestrutura deve executar em contêineres Docker orquestrados exclusivamente por `docker-compose.yml`, eliminando interferências de cache do SO host, DNS externo ou oscilações de provedor.
2. **Topologia de Três Servidores Distintos:**
   - `server-http1`: `nginx:alpine` servindo HTTP/1.1 em texto claro (Porta interna 80 / Host 8080).
   - `server-http2`: `nginx:alpine` servindo HTTPS/HTTP/2 com TLS 1.3 (Porta interna 443 / Host 8443).
   - `server-http3`: `caddy:2.7-alpine` servindo HTTP/3 sobre QUIC nativo (Porta interna 443 TCP/UDP / Host 9443).
3. **Rede Docker Dedicada:** Rede bridge `net_bench` com bloco estático `172.20.0.0/16`.
4. **Permissões de Manipulação de Kernel:** Todos os contêineres de serviço devem possuir obrigatoriamente a flag `cap_add: [NET_ADMIN]` no `docker-compose.yml` para evitar erros `RTNETLINK: Operation not permitted` ao executar comandos `tc`.
5. **Cliente de Benchmark Assíncrono em Python:**
   - Módulos mandatórios: `httpx` (para HTTP/1.1 e HTTP/2) e `aioquic` + `asyncio` (para HTTP/3).
   - **Controle de Viés de Sessão (Client-Side Bias Control):**
     - Desativação total de caches locais HTTP.
     - **Cold TTFB (Teste de Handshake):** Fechamento explícito da sessão (`client.close()`) antes de cada requisição individual, proibindo connection pooling para capturar a latência real de 1 RTT (TCP), 2 RTTs (TCP+TLS) e 1 RTT (QUIC).
     - **Warm Connection (Multiplexação):** Manutenção explícita de uma única conexão persistente nos testes com 100 objetos para avaliar a multiplexação real sem sucessivos custos de conexão.
6. **Automação 1-Click Runner (`run_experiments.sh` e `run_experiments.ps1`):** Script mestre que executa os 12 testes de ponta a ponta sem intervenção manual.
7. **Exportação Obrigatória de Dados:** Gravação dos resultados brutos com timestamp em `data/raw/results.json` ou `results.csv`.
8. **Visualização Gráfica com Barras de Erro Obrigatórias:** Gráficos gerados programaticamente com `matplotlib` ou `seaborn` contendo barras de erro (desvio padrão ou IC 95%). Gráficos planos perdem 10 pontos.

---

## 4. Síntese dos Dois Cenários de Rede (`tc netem`)

- **Cenário 1 (Rede Local - LAN):**
  - Condições ideais: atraso unidirecional de `0.5ms` (resultando em **RTT total de 1.0ms**), 0% de perda sintética de pacotes.
- **Cenário 2 (Rede Longa/Móvel - WAN):**
  - Condições adversas: atraso unidirecional de `25ms` (resultando em **RTT total de 50.0ms**), taxa de perda estocástica de **2% de pacotes**.

> [!NOTE]
> **Cálculo de RTT no Linux Traffic Control (`tc netem`):**  
> O comando `tc netem delay Xms` aplica o atraso unidirecionalmente na saída da interface de rede (`eth0`). Portanto, para emular um RTT de $N$ ms entre cliente e servidor, o atraso injetado na interface do contêiner deve ser exatamente $N/2$ ms.

---

## 5. Matriz Experimental Obrigatória (12 Testes)

| ID | Perfil de Carga | Protocolo Alvo | Servidor Alvo | Cenário de Rede | Foco Analítico Principal |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **T01** | Carga A (50 MB) | HTTP/1.1 | `server_http11` | Cenário 1 (LAN: 1ms, 0%) | Vazão máxima TCP em canal ideal sem criptografia |
| **T02** | Carga A (50 MB) | HTTPS / TLS 1.3 | `server_http2_tls` | Cenário 1 (LAN: 1ms, 0%) | Custo computacional de cifragem simétrica do TLS 1.3 |
| **T03** | Carga A (50 MB) | HTTP/3 (QUIC) | `server_http3_quic` | Cenário 1 (LAN: 1ms, 0%) | Eficiência do protocolo QUIC em user-space sem perdas |
| **T04** | Carga A (50 MB) | HTTP/1.1 | `server_http11` | Cenário 2 (WAN: 50ms, 2%) | Sensibilidade do TCP CUBIC a perdas e latência (Tanenbaum §6.5.11) |
| **T05** | Carga A (50 MB) | HTTPS / TLS 1.3 | `server_http2_tls` | Cenário 2 (WAN: 50ms, 2%) | Degradação do TCP CUBIC + TLS sob perdas estocásticas |
| **T06** | Carga A (50 MB) | HTTP/3 (QUIC) | `server_http3_quic` | Cenário 2 (WAN: 50ms, 2%) | Controle de congestionamento do QUIC sob perdas (Tanenbaum §6.6.1/§6.6.2) |
| **T07** | Carga B (100x10KB) | HTTP/1.1 | `server_http11` | Cenário 1 (LAN: 1ms, 0%) | Overhead de múltiplos handshakes TCP paralelos |
| **T08** | Carga B (100x10KB) | HTTPS / TLS 1.3 | `server_http2_tls` | Cenário 1 (LAN: 1ms, 0%) | Eficiência da multiplexação HTTP/2 em canal de baixa latência |
| **T09** | Carga B (100x10KB) | HTTP/3 (QUIC) | `server_http3_quic` | Cenário 1 (LAN: 1ms, 0%) | Desempenho de fluxos QUIC independentes em rede ideal |
| **T10** | Carga B (100x10KB) | HTTP/1.1 | `server_http11` | Cenário 2 (WAN: 50ms, 2%) | Severidade do HoL blocking na Camada de Aplicação |
| **T11** | Carga B (100x10KB) | HTTPS / TLS 1.3 | `server_http2_tls` | Cenário 2 (WAN: 50ms, 2%) | Severidade do HoL blocking na Camada de Transporte TCP |
| **T12** | Carga B (100x10KB) | HTTP/3 (QUIC) | `server_http3_quic` | Cenário 2 (WAN: 50ms, 2%) | Mitigação total do HoL blocking via fluxos UDP isolados |

---

## 6. Rubrica Detalhada de Avaliação (100 Pontos)

| Eixo de Avaliação | Pontuação Máxima | Critérios Detalhados de Correção |
| :--- | :---: | :--- |
| **1. Infraestrutura Docker e Emulação `tc netem`** | **25 Pontos** | Funcionamento correto dos 3 servidores (HTTP/1.1, HTTPS/TLS 1.3, HTTP/3). Uso correto de `cap_add: NET_ADMIN`. Precisão sintática nos comandos `tc netem` garantindo RTT de 1ms (LAN) e 50ms com 2% de perda (WAN). Automação de limpeza da interface. |
| **2. Cliente de Benchmark em Python** | **25 Pontos** | Código assíncrono com `httpx` e `aioquic`. Implementação estrita do controle de viés de sessão (fechamento para cold TTFB vs canal persistente para multiplexação). Execução perfeita das Cargas A e B. Exportação obrigatória para `results.json`/`results.csv`. |
| **3. Qualidade da Coleta e Visualização Gráfica** | **20 Pontos** | Rigor estatístico nas medições ($N \ge 10$). Cálculo preciso de TTFB, RPS, p50 e p99. Gráficos construídos em Python (`matplotlib`/`seaborn`) exibindo **obrigatoriamente barras de erro** (desvio padrão / intervalos de confiança de 95%), eixos rotulados e legendas claras. |
| **4. Relatório Técnico e Discussão Teórica** | **30 Pontos** | Profundidade analítica formal. Capacidade de explicar os gargalos empíricos com base na teoria. **Citação obrigatória e articulação detalhada com Tanenbaum §6.5.11 (TCP CUBIC) e §6.6.1/§6.6.2 (QUIC e BBR)** para justificativa dos cenários WAN. |

---

## 7. Tabela de Penalidades Previstas no Edital

| Infração Técnica | Penalidade Direta |
| :--- | :---: |
| Ausência de execução automatizada por meio de um único comando (`run_experiments.sh`) | **Subtração de 15 pontos** |
| Falta de controle de vício de sessão no cliente Python (reuso indevido de conexões no teste de TTFB) | **Subtração de 10 pontos** |
| Ausência de barras de erro nos gráficos gerados | **Subtração de 10 pontos** |
| Relatório puramente descritivo (sem fundamentação nos capítulos teóricos do Tanenbaum) | **Subtração de até 20 pontos no Eixo 4** |
| Faltando os códigos, o relatório técnico ou o vídeo | **NOTA ZERO (0,0)** |

---

## 8. 🚨 REGRA ELIMINATÓRIA CRÍTICA (NOTA ZERO)

> [!CAUTION]
> ### CRITÉRIO EXCLUDENTE DA AVALIAÇÃO:
> A submissão regular desta avaliação exige, impreterivelmente:
> 1. Os arquivos de **código-fonte completos** (Docker, shell scripts, cliente Python e notebooks/scripts de plot);
> 2. O arquivo **PDF do relatório técnico** com formatação de publicação científica;
> 3. O **link funcional para o vídeo explicativo de exatamente 15 minutos** gravado e hospedado no YouTube (Público ou Não-Listado), posicionado **obrigatoriamente na primeira página do relatório técnico**.
>
> **A ausência do código, a ausência do relatório em PDF ou a ausência/inoperância do link de vídeo implicará a atribuição automática de NOTA ZERO (0,0) à equipe, sem possibilidade de entrega posterior ou de recurso.**

---

## 9. Instruções de Submissão Final

- **Canal de Submissão:** Exclusivamente pelo sistema SIGAA da UFPI.
- **Formato do Arquivo:** Arquivo compactado único `.zip`.
- **Padrão Obrigatório de Nomenclatura:**  
  `TP2_Redes2_NomeAluno1_NomeAluno2.zip`  
  *(Para submissão individual: `TP2_Redes2_JoaoMarcosSousa.zip`)*.
- **Conteúdo do Arquivo ZIP:** Diretório do código-fonte completo e o Relatório Técnico em PDF (com link público do vídeo no YouTube na primeira página).
