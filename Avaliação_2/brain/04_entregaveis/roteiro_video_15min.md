# 05. Roteiro Cronometrado para o Vídeo Técnico (15 Minutos Exatos)

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Curso:** Bacharelado em Sistemas de Informação  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)  
**Título:** Estudo Experimental de Desempenho de Protocolos Web (HTTP/1.1 vs HTTPS/TLS vs HTTP/3-QUIC) em Ambiente Emulado com Docker e Python

---

## ⏱ Visão Geral e Distribuição do Tempo (00:00 a 15:00)

O vídeo deve possuir duração de **exatamente 15 minutos** (margem de segurança recomendada: 14:50 a 15:05) e cobrir integralmente a infraestrutura, a implementação do cliente Python, a execução dos ensaios ao vivo, a análise gráfica com barras de erro e o embasamento teórico em Tanenbaum.

| Bloco | Janela de Tempo | Duração | Conteúdo Principal e Ação em Tela |
| :---: | :---: | :---: | :--- |
| **Bloco 1** | 00:00 - 02:00 | 2m 00s | **Abertura e Contextualização:** Apresentação da equipe, tema da 2ª Avaliação, objetivos pedagógicos (Overhead de Handshake, HoL Blocking e perdas). |
| **Bloco 2** | 02:00 - 04:30 | 2m 30s | **Arquitetura e Infraestrutura Docker:** Apresentação do `docker-compose.yml`, rede `net_bench`, NGINX HTTP/1.1, NGINX HTTPS TLS 1.3, Caddy HTTP/3 QUIC e regras de emulação `tc netem`. |
| **Bloco 3** | 04:30 - 07:30 | 3m 00s | **Implementação do Cliente Python:** Código assíncrono com `httpx` e `aioquic`, módulo de controle de viés de sessão (Cold TTFB vs Warm Connection) e orquestrador 1-click. |
| **Bloco 4** | 07:30 - 10:30 | 3m 00s | **Demonstração Experimental ao Vivo:** Disparo do `./run_experiments.sh`, acompanhamento dos testes T01 a T12 em tempo real, aplicação do `tc netem` e exportação do `results.json`. |
| **Bloco 5** | 10:30 - 13:30 | 3m 00s | **Análise de Resultados e Fundamentação Teórica:** Apresentação dos gráficos com barras de erro e discussão teórica profunda com Tanenbaum Seção 6.5.11 (CUBIC) e Seções 6.6.1 e 6.6.2 (QUIC/BBR). |
| **Bloco 6** | 13:30 - 15:00 | 1m 30s | **Conclusões e Encerramento:** Síntese dos achados empíricos, validação das hipóteses e considerações finais. |

---

## 🎬 Roteiro Detalhado Minuto a Minuto

### 📌 Bloco 1: Abertura e Contextualização Pedagógica [00:00 - 02:00]
- **Tela:** Slide de abertura contendo título do trabalho, logo da UFPI/CSHNB, disciplina Redes II, nome do aluno e e-mail.
- **Fala (00:00 - 00:45):**
  > *"Olá a todos! Sejam bem-vindos à apresentação do Trabalho Prático da 2ª Avaliação da disciplina de Redes de Computadores II da Universidade Federal do Piauí, ministrada no Campus de Picos. Meu nome é João Marcos Sousa Rufino Leal e hoje apresentaremos o estudo experimental de desempenho dos protocolos Web: HTTP/1.1 versus HTTPS com TLS 1.3 versus HTTP/3 sobre QUIC, em um ambiente emulado de alta precisão com Docker e Python."*
- **Fala (00:45 - 02:00):**
  > *"O objetivo central deste trabalho é investigar quantitativamente três fenômenos fundamentais que regem a Internet moderna: primeiro, a sobrecarga de handshakes e o impacto no Time to First Byte, comparando o 1 RTT do TCP puro, os 2 RTTs cumulativos do HTTPS com TLS 1.3 e o handshake integrado de 1 RTT do QUIC sobre UDP; segundo, o Bloqueio de Início de Linha (Head-of-Line Blocking), analisando como o HTTP/2 resolveu o problema na camada de aplicação mas transferiu a vulnerabilidade para o transporte TCP, enquanto o HTTP/3 elimina totalmente o HoL em ambas as camadas via streams UDP independentes; e terceiro, a resiliência a perdas de pacotes sob controle de congestionamento, confrontando o algoritmo TCP CUBIC com a arquitetura do QUIC sob uma rede móvel WAN com 2% de descarte estocástico e 50 milissegundos de RTT."*

---

### 🏗 Bloco 2: Arquitetura e Infraestrutura Docker [02:00 - 04:30]
- **Tela:** VS Code exibindo o arquivo `docker/docker-compose.yml` e o diagrama de arquitetura Mermaid.
- **Fala (02:00 - 03:15):**
  > *"Para garantir isolamento absoluto e reprodutibilidade científica, nossa infraestrutura foi modelada em contêineres Docker interconectados pela rede bridge dedicada `net_bench` na sub-rede 172.20.0.0/16. Temos três servidores Web operando simultaneamente: no IP 172.20.0.10, temos o `server_http11`, utilizando NGINX Alpine na porta 8080 para servir HTTP/1.1 em texto claro, sem overhead criptográfico, servindo como nosso baseline de transporte TCP; no IP 172.20.0.20, temos o `server_http2_tls`, também NGINX, servindo HTTPS com HTTP/2 e TLS 1.3 forçado na porta 8443; e no IP 172.20.0.30, temos o `server_http3_quic`, utilizando o servidor Caddy 2.7 Alpine na porta 9443, tanto em TCP quanto em UDP, para oferecer HTTP/3 nativo com suporte a QUIC."*
- **Fala (03:15 - 04:30):**
  > *"Um detalhe crítico de engenharia exigido pelo edital é a declaração `cap_add: [NET_ADMIN]` em todos os contêineres. Sem essa funcionalidade de kernel do Linux, qualquer tentativa de executar o utilitário `tc` para controle de tráfego resultaria no erro fatal `RTNETLINK: Operation not permitted`. Os certificados digitais foram gerados localmente via OpenSSL com extensões Subject Alternative Names (SAN) cobrindo tanto localhost quanto os IPs e hostnames da rede Docker, assegurando que nossos clientes TLS e QUIC estabeleçam conexões seguras sem exceções de validação."*

---

### 💻 Bloco 3: Implementação do Cliente de Benchmark Python [04:30 - 07:30]
- **Tela:** VS Code exibindo `benchmark/client.py` e `benchmark/session_control.py`.
- **Fala (04:30 - 06:00):**
  > *"Como navegadores comerciais utilizam heurísticas agressivas de cache e renderização que mascaram o comportamento da rede, desenvolvemos um cliente de benchmark assíncrono dedicado em Python 3. Utilizamos a biblioteca `httpx` para as requisições assíncronas em HTTP/1.1 e HTTP/2, e o módulo `aioquic` com `asyncio` para gerenciar nativamente os eventos e fluxos de transporte do HTTP/3 QUIC sobre UDP. Todas as medições de tempo utilizam `time.perf_counter()` para precisão de microssegundos."*
- **Fala (06:00 - 07:30):**
  > *"Aqui implementamos com rigor absoluto o **Controle de Viés de Sessão** exigido no edital para evitar a perda de 10 pontos: primeiro, qualquer forma de cache local é totalmente suprimida nos headers. Segundo, no teste de handshake e Cold TTFB, o cliente fecha e destrói explicitamente a sessão com `await client.aclose()` antes de cada requisição individual, proibindo o reaproveitamento de conexões para medir exatamente o custo dos RTTs iniciais de conexão. Terceiro, nos testes da Carga B com 100 objetos pequenos de 10 KB, o cliente estabelece uma única conexão prévia e mantém essa conexão aquecida (Warm Connection), disparando os downloads concorrentes para avaliar com fidelidade a multiplexação de fluxos do HTTP/2 e HTTP/3 sem contaminação de sucessivos handshakes."*

---

### 🧪 Bloco 4: Demonstração Experimental ao Vivo (1-Click Run) [07:30 - 10:30]
- **Tela:** Terminal aberto no diretório raiz do projeto.
- **Fala (07:30 - 08:30):**
  > *"Agora, vamos demonstrar a automação completa do ambiente através do orquestrador mestre `run_experiments.sh`. Com um único comando, o script sobe os contêineres Docker, configura as regras do `tc netem`, dispara os 12 testes experimentais mandatórios da matriz e gera os resultados brutos."*
- **Ação em Tela:** Executar `./run_experiments.sh`. Mostrar os contêineres subindo com `docker compose up -d`.
- **Fala (08:30 - 09:30):**
  > *"O runner inicia aplicando o Cenário 1 (LAN): reparem no comando `docker exec tc qdisc add dev eth0 root netem delay 0.5ms`. Como o atraso no Linux é injetado unidirecionalmente na saída da interface, 0.5ms em cada sentido resulta exatamente no RTT de 1.0 milissegundo de rede local. Em seguida, os testes T01, T02 e T03 da Carga A de 50 MB são executados com 10 repetições independentes cada, seguidos pelos testes T07, T08 e T09 da Carga B com 100 objetos simultâneos."*
- **Ação em Tela:** Mostrar a transição para o Cenário 2 (WAN).
- **Fala (09:30 - 10:30):**
  > *"Agora o script reconfigura a interface via `tc netem delay 25ms loss 2%`, emulando o Cenário 2: RTT total de 50 milissegundos e 2% de perda estocástica de pacotes. Notem imediatamente no terminal o tempo de resposta dos testes T04 e T05 do TCP CUBIC disparando, enquanto o teste T06 e T12 do HTTP/3 progridem com muito mais agilidade. Ao final, a interface é restaurada com `tc qdisc del` e os dados brutos são salvos com sucesso em `data/raw/results.json` e `results.csv`."*

---

### 📊 Bloco 5: Análise dos Resultados e Fundamentação em Tanenbaum [10:30 - 13:30]
- **Tela:** Apresentação dos gráficos científicos gerados em `data/plots/` (exibindo as barras de erro).
- **Fala (10:30 - 11:30):**
  > *"Vamos agora aos resultados obtidos, apresentados com rigor científico. Conforme exigência expressa do edital, todos os nossos gráficos possuem **barras de erro** representando o intervalo de confiança de 95% calculado via distribuição t-Student com 9 graus de liberdade. Na Figura 1, observamos o Cold TTFB: na LAN, o HTTP/1.1 registra cerca de 1.2ms, o HTTPS salta para 2.3ms devido ao handshake cumulativo de 2 RTTs (TCP + TLS 1.3), e o HTTP/3 estabiliza em 1.3ms graças ao handshake unificado de 1 RTT sobre UDP."*
- **Fala (11:30 - 12:30):**
  > *"Na Figura 2, temos a vazão sustentada da Carga A de 50 MB, e aqui reside o ponto alto do embasamento teórico exigido no Eixo 4: no Cenário LAN, o TCP em texto claro atinge mais de 900 Mbps graças às otimizações consolidadas de kernel (TSO e GRO). Contudo, no Cenário WAN sob 2% de perda, observamos o colapso dramático do TCP CUBIC (testes T04 e T05), cuja vazão desaba para menos de 15 Mbps. Conforme explica Tanenbaum na seção 6.5.11, o TCP CUBIC utiliza uma função cúbica de janela $W_{\text{cubic}}(t) = C(t - K)^3 + W_{\text{max}}$. A cada evento de descarte, o CUBIC sofre recuo multiplicativo de 30% em sua janela de congestionamento ($\beta = 0.7$). Como o canal possui 2% de perda aleatória contínua e RTT de 50ms, a janela nunca consegue atingir a fase de crescimento rápido, mantendo o throughput permanentemente estrangulado."*
- **Fala (12:30 - 13:30):**
  > *"Em contrapartida, no teste T06 e T12, o HTTP/3 sustenta vazão e RPS substancialmente superiores. Conforme Tanenbaum detalha nas seções 6.6.1 e 6.6.2 sobre o QUIC e o BBR, o QUIC isola a perda no fluxo UDP específico e utiliza modelos de controle de congestionamento baseados na taxa real de entrega (pacing) e no RTT mínimo físico do canal, sem interpretar perdas de pacotes isoladas como sinal ingênuo de colapso de largura de banda. Na Carga B com 100 objetos (Figura 3 e 4), a perda no HTTP/2 fez o percentil p99 explodir devido ao Head-of-Line Blocking no transporte TCP, enquanto no HTTP/3 os 99 streams restantes continuaram sendo entregues em tempo recorde."*

---

### 🎯 Bloco 6: Conclusões e Encerramento [13:30 - 15:00]
- **Tela:** Slide final com síntese das conclusões e referências bibliográficas.
- **Fala (13:30 - 14:30):**
  > *"Em conclusão, este trabalho prático comprovou empiricamente que o HTTP/3 sobre QUIC representa um salto arquitetural indispensável para a Internet móvel moderna. Enquanto o HTTP/2 sobre TCP é extremamente eficiente em redes locais de altíssima qualidade e sem ruído, ele se torna vulnerável em redes móveis e de longa distância devido ao Head-of-Line Blocking de transporte e à hiper-sensibilidade do TCP CUBIC a perdas estocásticas. O HTTP/3 supera essas limitações ao integrar segurança em 1 RTT, eliminar o HoL blocking via streams UDP independentes e adotar controle de congestionamento moderno."*
- **Fala (14:30 - 15:00):**
  > *"Nosso repositório completo com Docker, cliente Python, scripts e relatório técnico em PDF encontra-se disponível, e o link deste vídeo está registrado na primeira página do artigo conforme as regras do edital. Agradeço a atenção de todos e ao professor pela excelente oportunidade pedagógica. Muito obrigado!"*

---

## 📋 Checklist Pré-Gravação do Vídeo

- [ ] Microfone testado e com volume calibrado sem ruídos de fundo.
- [ ] Resolução de gravação configurada em 1080p (1920x1080) a 30 ou 60 FPS no OBS Studio.
- [ ] Fontes do terminal e do VS Code ampliadas para leitura nítida em telas menores.
- [ ] Cenário de teste pré-executado uma vez para garantir que todos os contêineres e scripts rodam suavemente.
- [ ] Cronômetro visível na tela secundária para manter a fala rigorosamente dentro dos 15 minutos (14:50 a 15:05).
- [ ] Upload efetuado no YouTube em modo "Não listado" ou "Público" e link testado em aba anônima.
