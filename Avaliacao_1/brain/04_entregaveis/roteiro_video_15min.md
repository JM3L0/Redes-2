# 05. Roteiro de Gravação do Vídeo Técnico (15 Minutos Exatos)

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Bacharelado em Sistemas de Informação  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)  
**Trabalho:** Avaliação Prática: Avaliação de Desempenho e Sobrecarga de Transporte — TCP, UDP e QUIC com NGINX e Linux NetEm

---

## ⏱️ Cronograma Planejado (Minuto a Minuto)

O edital exige uma apresentação técnica de **exatamente 15 minutos**. Mantenha o cronômetro visível no celular ou monitor secundário para cravar a gravação entre **14:50 e 15:05**.

```text
00:00 ───┬── 01:30 [1m 30s] : Bloco 1 - Apresentação Pessoal, Contexto e Hipóteses
01:30 ───┼── 05:00 [3m 30s] : Bloco 2 - Demonstração Guiada do Código-Fonte e Infraestrutura
05:00 ───┼── 09:30 [4m 30s] : Bloco 3 - Execução ao Vivo, Testes de Protocolo e Wireshark
09:30 ───┼── 13:45 [4m 15s] : Bloco 4 - Apresentação dos Gráficos Gerados e Discussão Científica
13:45 ───┴── 15:00 [1m 15s] : Bloco 5 - Síntese dos Trade-offs e Conclusão Final
```

---

## 🎬 Roteiro Completo de Apresentação

---

### BLOCO 1: Apresentação Pessoal e Contexto Geral
**Duração:** 00:00 até 01:30 (1 minuto e 30 segundos)

* **O que mostrar na tela:**
  * Slide inicial ou a primeira página do artigo [sbc-template.pdf](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/artigo/sbc-template.pdf) em tela cheia, destacando título, instituição (UFPI), curso e seu nome. Câmera ligada no canto da tela (opcional, mas recomendada).
* **O que falar (Roteiro sugerido):**
  > *"Olá a todos, olá professor. Meu nome é João Marcos Sousa Rufino Leal, aluno do curso de Bacharelado em Sistemas de Informação da Universidade Federal do Piauí (UFPI). Esta é a apresentação técnica da Avaliação 1 da disciplina de Redes de Computadores II (período 2026-2).*  
  > *O objetivo desta atividade é realizar uma investigação experimental e empírica comparando três paradigmas de transporte na Internet: o TCP tradicional com TLS 1.3 (avaliado via HTTP/1.1 e HTTP/2), o UDP Puro sem confirmação (avaliado via iperf3), e o protocolo moderno QUIC, executado sobre UDP com criptografia integrada (avaliado via HTTP/3 no NGINX).*  
  > *Para garantir total rigor científico e reprodutibilidade, todo o ambiente de testes foi construído sobre o ecossistema Linux em contêineres Docker isolados. Um detalhe importante de conformidade com o edital: embora a minha máquina host de desenvolvimento seja Windows, a execução atende 100% à exigência do edital porque o Docker Desktop opera integrado ao motor WSL 2 (Windows Subsystem for Linux), utilizando um kernel Linux real mantido pela Microsoft. Assim, os contêineres cliente e servidor executam imagens Linux nativas (Ubuntu e Alpine), e todas as regras de controle de tráfego, filas do kernel e medições via tc/netem operam nativamente sobre a pilha de rede do Linux.*  
  > *Os ensaios foram organizados em três cenários planejados: o Cenário A favorável ao UDP puro, o Cenário B favorável ao TCP e o Cenário C favorável ao QUIC. Vamos agora à inspeção detalhada do código-fonte e da arquitetura do projeto."*
* **Como evidenciar o edital:**
  * Apresentação individual explícita do aluno.
  * Citação formal dos três protocolos e da metodologia com Docker e Linux NetEm.
  * Esclarecimento prévio e transparente sobre a conformidade de ambiente: Host Windows com Docker Desktop sobre WSL 2 (kernel Linux real e contêineres Linux nativos).

---

### BLOCO 2: Demonstração Guiada do Código-Fonte
**Duração:** 01:30 até 05:00 (3 minutos e 30 segundos)

* **O que mostrar na tela:**
  * VS Code aberto na pasta do projeto com fonte aumentada (16pt a 18pt para legibilidade nítida no vídeo).

#### 1. Orquestração com Docker (`docker/docker-compose.yml`) — [01:30 a 02:45]
* **Arquivo a abrir:** [docker/docker-compose.yml](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/docker/docker-compose.yml)
* **O que destacar e falar:**
  > *"Aqui no `docker-compose.yml`, definimos dois serviços essenciais conectados por uma rede bridge isolada `redes2_net` com sub-rede estática `172.28.0.0/16`:*  
  > *1. O serviço `server` (IP 172.28.0.10), que expõe a porta 443 TCP para HTTP/1.1 e HTTP/2, a porta 443 UDP para HTTP/3 QUIC, e a porta 5201 UDP para o iperf3.*  
  > *2. O serviço `client` (IP 172.28.0.20), montando os volumes de scripts, dados e análises.*  
  > *Um ponto crítico exigido pelo edital é a diretiva `cap_add: [NET_ADMIN]` em ambos os contêineres. Essa capacidade concede permissão administrativa ao contêiner para interagir diretamente com as filas de rede (`qdisc`) do kernel Linux, viabilizando o uso do utilitário `tc` sem precisar de modo privilegiado irrestrito."*

#### 2. Configuração do Servidor NGINX e Certificados — [02:45 a 03:50]
* **Arquivos a abrir:** [docker/server/nginx.conf](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/docker/server/nginx.conf) e [docker/server/entrypoint.sh](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/docker/server/entrypoint.sh)
* **O que destacar e falar:**
  > *"No arquivo `nginx.conf`, temos a configuração da mesma porta 443 atendendo às três versões:*  
  > *Na linha 39, `listen 443 ssl;` com `http2 on;` para TCP.*  
  > *Na linha 43, `listen 443 quic reuseport;` habilitando o módulo nativo `ngx_http_v3_module`.*  
  > *Na linha 30, forçamos o protocolo criptográfico moderno `ssl_protocols TLSv1.3;` e habilitamos `ssl_early_data on;` para dar suporte à retomada de sessão em 0-RTT.*  
  > *Na linha 49, inserimos o cabeçalho obrigatório `add_header Alt-Svc 'h3=\":443\"; ma=86400' always;`. Esse cabeçalho é o mecanismo oficial pelo qual o servidor anuncia aos navegadores e clientes cURL que o serviço HTTP/3 está disponível via UDP.*  
  > *No script `entrypoint.sh`, mostramos a geração automática de certificados TLS 1.3 via OpenSSL utilizando chave elíptica ECDSA na curva P-256 (`prime256v1`) com extensões SAN para `server`, `localhost` e `172.28.0.10`, além da inicialização do `iperf3 -s` em background."*

#### 3. Emulação de Canal de Rede (`scripts/setup_netem.sh`) — [03:50 a 05:00]
* **Arquivo a abrir:** [scripts/setup_netem.sh](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/scripts/setup_netem.sh)
* **O que destacar e falar:**
  > *"Para emular os canais de rede de forma determinística, criamos o script modular `setup_netem.sh`, manipulando a interface virtual `eth0` do cliente:*  
  > *No Cenário A (UDP em tempo real): aplicamos `netem delay 2ms`, gerando RTT de aproximadamente 4 ms sem perda.*  
  > *No Cenário B (TCP massivo em canal limpo): aplicamos `netem delay 10ms`, gerando RTT de 20 ms e 0% de descarte.*  
  > *No Cenário C (QUIC sob rede instável): aplicamos `netem delay 50ms loss X%`, gerando RTT de 100 ms com descartes aleatórios de 0%, 2% e 5%.*  
  > *O script conta ainda com a função `clear` que executa `tc qdisc del dev eth0 root` para garantir que um teste nunca herde condições residuais do teste anterior."*

---

### BLOCO 3: Execução ao Vivo, Testes de Protocolo e Wireshark
**Duração:** 05:00 até 09:30 (4 minutos e 30 segundos)

* **O que mostrar na tela:**
  * Terminal Linux (WSL 2 / Ubuntu / PowerShell) e Wireshark aberto.

#### 1. Subida dos Contêineres e Validação de Conectividade — [05:00 a 06:15]
* **Comandos no Terminal:**
  ```bash
  # No terminal do host (Windows PowerShell ou WSL):
  docker compose -f docker/docker-compose.yml up -d
  docker ps
  ```
* **O que falar:**
  > *"Vamos subir os serviços. Executo `docker compose up -d`. Vemos no `docker ps` que os contêineres `redes2_server` e `redes2_client` estão ativos e saudáveis.*  
  > *Agora vamos entrar no contêiner cliente para testar a conectividade direta dos três protocolos."*
* **Comando dentro do cliente:**
  ```bash
  docker exec -it redes2_client bash
  
  # Teste rápido de HTTP/3 nativo com curl
  curl -k --http3-only https://server/health -I
  ```
* **O que falar:**
  > *"Observem que estamos diretamente dentro do terminal nativo Linux Ubuntu (`root@client:/workspace#`). A resposta do cURL confirma: `HTTP/3 200` e o cabeçalho `alt-svc: h3=\":443\"`. Isso comprova de imediato que o handshake QUIC sobre UDP na porta 443 foi concluído com sucesso e que toda a execução roda sob o kernel Linux."*

#### 2. Disparo de Amostra dos Cenários — [06:15 a 07:30]
* **Comandos no Terminal:**
  ```bash
  # 1. Testar UDP Puro (Cenário A):
  iperf3 -c 172.28.0.10 -u -b 100M -t 3 -l 128
  
  # 2. Testar HTTP/2 vs HTTP/3 no Cenário B:
  curl -k --http2 https://server/100MB.bin -o /dev/null
  curl -k --http3-only https://server/100MB.bin -o /dev/null
  ```
* **O que falar:**
  > *"No Cenário A com iperf3, enviamos datagramas UDP pequenos de 128 bytes a 100 Mbps. Vemos que a taxa atinge exatamente os 100 Mbps com jitter inferior a 0,1 ms e 0% de perda.*  
  > *Para os testes científicos completos, o orquestrador `run_experiments.sh` executa cada bateria 10 vezes consecutivas para cada protocolo, capturando métricas de FCT, goodput, TTFB, tempo de CPU e gerando arquivos de captura `.pcapng` via `tshark`."*

#### 3. Demonstração Visual das Capturas no Wireshark — [07:30 a 09:30]
* **O que mostrar:**
  * Abra o Wireshark com um dos arquivos salvos em `data/pcaps/` (ex: `scenario_c_loss5.pcapng` ou `scenario_b_sample.pcapng`).
* **Filtros e Análise no Wireshark:**
  1. **Filtro TCP:** Digite no filtro `tcp.analysis.retransmission` ou `tcp.analysis.flags`.
     * **O que falar:**
       > *"Aqui no Wireshark, ao filtrar por `tcp.analysis.retransmission` na captura do Cenário C com 5% de perda, vemos as linhas pretas e vermelhas de retransmissão de segmentos TCP (foram registradas 330 retransmissões no lote). O cliente detecta o gap nos números de sequência, gera Duplicate ACKs, e a janela deslizante do TCP trava. Como o HTTP/2 multiplexa todos os objetos sobre a mesma conexão TCP, esse segmento perdido bloqueia a fila inteira no kernel, gerando o Bloqueio de Cabeça de Linha (Head-of-Line Blocking)."*
  2. **Filtro QUIC:** Digite no filtro `quic`.
     * **O que falar:**
       > *"Agora, ao filtrar por `quic` ou `udp.port == 443`, vemos pacotes QUIC protegidos por TLS 1.3. Observem os pacotes `Initial`, `Handshake` e `1-RTT`. No QUIC, os números de pacote são estritamente monotônicos e cada requisição roda em uma `stream` independente. Se um pacote do stream A for perdido pelo canal com 5% de perda, o stream B continua sendo entregue à aplicação imediatamente sem esperar por A. Não há travamento de fila na camada de transporte."*

---

### BLOCO 4: Apresentação dos Gráficos Gerados e Discussão Científica
**Duração:** 09:30 até 13:45 (4 minutos e 15 segundos)

* **O que mostrar na tela:**
  * Slides ou imagens dos gráficos de alta resolução (300 DPI) localizados em `artigo/imagens/` ou no PDF do artigo.

#### 1. Cenário A — UDP Puro em Baixa Latência (09:30 a 10:45)
* **Gráficos a mostrar:** [graf1a_goodput_vs_taxa.png](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/artigo/imagens/graf1a_goodput_vs_taxa.png), [graf1b_jitter_vs_taxa.png](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/artigo/imagens/graf1b_jitter_vs_taxa.png) e [graf2_overhead_cabecalho.png](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/artigo/imagens/graf2_overhead_cabecalho.png).
* **O que falar:**
  > *"No Cenário A, avaliamos o UDP puro injetando taxas de 10 a 500 Mbps com RTT de 4 ms:*  
  > *Na Figura 2, vemos que o goodput acompanhou linearmente a taxa teórica até 250 Mbps, atingindo média de 498,31 Mbps na taxa máxima de 500 Mbps.*  
  > *O jitter na Figura 3 permaneceu microscópico, sempre abaixo de 0,13 ms.*  
  > *Na Figura 4, comparamos a sobrecarga de cabeçalho: o UDP tem overhead fixo imbatível de apenas 8 bytes. O TCP exige no mínimo 20 bytes (chegando a 32 ou 40 bytes com SACK e Timestamps), e o QUIC impõe sobrecarga moderada para acomodar identificadores de conexão e criptografia. Conclui-se que para fluxos contínuos de sensores IoT e telemetria onde perder pacotes é preferível a sofrer atrasos, o UDP puro continua sendo a escolha mais leve."*

#### 2. Cenário B — Transferências Massivas e Vitória do TCP (10:45 a 12:15)
* **Gráficos e Tabelas a mostrar:** Tabela 2 do artigo, [graf3a_fct_cenario_b.png](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/artigo/imagens/graf3a_fct_cenario_b.png), [graf3b_goodput_cenario_b.png](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/artigo/imagens/graf3b_goodput_cenario_b.png) e [graf4a_handshake.png](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/artigo/imagens/graf4a_handshake.png).
* **O que falar:**
  > *"O Cenário B testou arquivos massivos de 100 MB e 1 GB em canal limpo com RTT de 20 ms:*  
  > *Nas Figuras 5 e 6, vemos que o TCP (HTTP/1.1 e HTTP/2) superou amplamente o HTTP/3 em vazão bruta, sustentando médias de ~594 Mbps em 100 MB e ~596 Mbps em 1 GB, enquanto o HTTP/3 ficou limitado a ~46 Mbps.*  
  > *Por que isso ocorre? Essa é uma evidência clássica da literatura: o TCP opera diretamente no espaço de kernel do Linux e utiliza mecanismos de descarregamento de hardware consolidados há décadas, como o TSO (TCP Segmentation Offload) e o GRO (Generic Receive Offload). O kernel agrega pacotes e poupa ciclos de CPU.*  
  > *Já o QUIC roda em user-space (espaço de usuário), gerando centenas de milhares de chamadas de sistema (syscalls) e executando criptografia por pacote. Nossa medição de CPU (Tabela 3) comprova isso: para transferir 1 GB, o HTTP/3 consumiu 9,23 segundos de tempo de CPU, contra apenas 1,89 s do HTTP/2.*  
  > *Em contrapartida, na Figura 7 vemos a vitória do QUIC no estabelecimento de conexão: o aperto de mão do HTTP/3 levou apenas 16,78 ms contra 25,02 ms do HTTP/2 (redução de 33%), comprovando o benefício do handshake TLS 1.3 integrado em 1-RTT."*

#### 3. Cenário C — Redes Instáveis, Concorrência e Bloqueio HoL (12:15 a 13:45)
* **Gráficos e Tabelas a mostrar:** Tabela 4 do artigo, [graf5a_fct_medio_perdas.png](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/artigo/imagens/graf5a_fct_medio_perdas.png), [graf6_cdf_hol_blocking.png](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/artigo/imagens/graf6_cdf_hol_blocking.png) e [graf7b_pcap_retransmissoes.png](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/artigo/imagens/graf7b_pcap_retransmissoes.png).
* **O que falar:**
  > *"No Cenário C, avaliamos 100 objetos concorrentes sob RTT de 100 ms e perdas de 0%, 2% e 5%:*  
  > *Sob 5% de perda, o HTTP/1.1 sofre grande degradação, saltando o FCT para 1,85 s com p95 de 2,30 s devido à disputa de múltiplas conexões TCP.*  
  > *O gráfico da CDF na Figura 9 é o ponto alto deste cenário: observem a cauda longa no TCP. Quando segmentos são perdidos, a entrega dos objetos sofre alta variância no HTTP/2. Já o HTTP/3, graças aos streams independentes, apresenta uma curva de distribuição muito mais agrupada e com menor desvio padrão (apenas ±0,08 s sob 5% de perda, com p95 de 1,51 s contra 2,30 s do HTTP/1.1).*  
  > *A Figura 10 e a Tabela 4 mostram que o Wireshark registrou 330 retransmissões no TCP, ao passo que no QUIC a recuperação é gerenciada internamente na aplicação por frames ACK, sem retransmissões no nível de transporte do kernel."*

---

### BLOCO 5: Síntese dos Trade-offs e Conclusão Final
**Duração:** 13:45 até 15:00 (1 minuto e 15 segundos)

* **O que mostrar na tela:**
  * Slide de conclusão ou a seção de Considerações Finais do relatório técnico.
* **O que falar (Fechamento):**
  > *"Como considerações finais, a avaliação experimental comprova que não existe uma bala de prata nem um protocolo universalmente superior:*  
  > *1. O UDP puro é o mais eficiente para fluxos em tempo real com cargas pequenas e tolerância a descarte, impondo o menor custo computacional.*  
  > *2. O TCP continua imbatível para transferências massivas em redes estáveis, aproveitando a maturidade do kernel e acelerações de hardware como TSO e GRO.*  
  > *3. O QUIC (HTTP/3) é a arquitetura ideal para a Web moderna: reduz em mais de 30% a latência de abertura de sessão com TLS 1.3 integrado e mitiga o bloqueio de cabeça de linha em redes sem fio e instáveis.*  
  > *Todos os artefatos, scripts, dados brutos, capturas `.pcapng` e o relatório técnico completo no padrão SBC estão disponibilizados no repositório do projeto.*  
  > *Agradeço a atenção de todos e encerro aqui esta apresentação. Muito obrigado!"*  
  *(Concluir na marca exata entre 14:55 e 15:02)*.

---

## 🛠️ Checklist Prático para Antes da Gravação

1. **Subir o ambiente com antecedência:**
   Execute `./run_experiments.sh` (Linux/WSL) ou `.\run_experiments.ps1` (PowerShell) para garantir que todos os dados e gráficos estejam previamente gerados na pasta `data/`.
2. **Preparar as abas no Windows/Linux:**
   * Aba 1: VS Code com os arquivos `docker-compose.yml`, `nginx.conf` e `setup_netem.sh`.
   * Aba 2: Terminal limpo (`clear`) pronto para rodar os testes rápidos.
   * Aba 3: Wireshark aberto com o arquivo `data/pcaps/scenario_c_loss5.pcapng` já carregado.
   * Aba 4: Visualizador de PDF com o relatório `artigo/sbc-template.pdf` aberto nas páginas dos gráficos.
3. **Resolução de Gravação no OBS Studio:**
   * Resolução: 1920x1080 (1080p).
   * Taxa de quadros: 30 FPS ou 60 FPS.
   * Formato de saída: MP4 (com áudio AAC estéreo).
4. **Após a gravação:**
   * Suba o vídeo no YouTube (como **"Não listado"** ou **"Público"**).
   * Copie o link do vídeo, cole na **linha 27** de [artigo/sbc-template.tex](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/artigo/sbc-template.tex).
   * Recompile o PDF final (`pdflatex sbc-template.tex`).
