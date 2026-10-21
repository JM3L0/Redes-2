# 06. Guia de Prompts Prontos para IAs

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Curso:** Bacharelado em Sistemas de Informação  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)

Utilize os prompts estruturados abaixo para orientar agentes de inteligência artificial em cada uma das fases subsequentes do desenvolvimento, garantindo conformidade estrita com o edital e prevenindo penalidades.

---

## 🚀 Prompt 1: Criação da Infraestrutura Docker e Configuração dos 3 Servidores

```text
Você é um engenheiro de redes e especialista em Linux e Docker. Estamos implementando a 2ª Avaliação Prática de Redes de Computadores II da UFPI (2026-2): Estudo Experimental de Desempenho de Protocolos Web (HTTP/1.1 vs HTTPS/TLS vs HTTP/3-QUIC).

Consulte os arquivos de contexto no cérebro do projeto:
- brain/01_diretrizes/visao_geral_e_regras.md
- brain/02_arquitetura/arquitetura_e_docker.md

Sua tarefa é criar a infraestrutura completa de contêineres e configurações dos servidores:
1. `docker/docker-compose.yml`:
   - Rede bridge dedicada `net_bench` (172.20.0.0/16).
   - Serviço `server-http1`: imagem `nginx:alpine`, porta "8080:80", IP estático 172.20.0.10, `cap_add: [NET_ADMIN]`.
   - Serviço `server-http2`: imagem `nginx:alpine`, porta "8443:443", IP estático 172.20.0.20, `cap_add: [NET_ADMIN]`, volumes para certificados e config.
   - Serviço `server-http3`: imagem `caddy:2.7-alpine`, portas "9443:443/tcp" e "9443:443/udp", IP estático 172.20.0.30, `cap_add: [NET_ADMIN]`, volumes para certificados e Caddyfile.
2. `docker/server-http1/nginx.conf`: NGINX servindo HTTP/1.1 em texto claro na porta 80, com sendfile on, tcp_nopush on, tcp_nodelay on e cabeçalhos desativando cache.
3. `docker/server-http2/nginx.conf`: NGINX servindo HTTPS/HTTP/2 com TLS 1.3 forçado (`ssl_protocols TLSv1.3;`), certificados locais e cabeçalhos sem cache.
4. `docker/server-http3/Caddyfile`: Caddy servindo HTTP/3 sobre QUIC na porta 443 TCP/UDP com TLS local e cabeçalho `Alt-Svc "h3=\":9443\"; ma=86400"`.
5. `docker/certs/generate_certs.sh`: Script OpenSSL que gera chaves RSA 2048 e certificado autoassinado com Subject Alternative Names (SANs) cobrindo localhost, 127.0.0.1, 172.20.0.20, 172.20.0.30, server_http2_tls e server_http3_quic.

Gere os arquivos com sintaxe impecável e quebras de linha padrão Unix (LF).
```

---

## 📦 Prompt 2: Cargas Estáticas, Scripts `tc netem` e Orquestrador 1-Click

```text
Você é um especialista em automação e emulação de redes no Linux. Estamos implementando a automação da 2ª Avaliação Prática de Redes II da UFPI.

Consulte:
- brain/02_arquitetura/arquitetura_e_docker.md
- brain/03_experimentos/cenarios_de_teste.md

Sua tarefa é criar os scripts de suporte, emulação e o runner mestre:
1. `scripts/generate_payloads.py`:
   - Gera `data/static/50MB.bin` (arquivo binário determinístico de exatamente 50 * 1024 * 1024 bytes para a Carga A).
   - Gera `data/static/objects/obj_001.bin` a `obj_100.bin` (100 arquivos binários de exatamente 10 * 1024 bytes cada para a Carga B).
2. `scripts/setup_netem.sh`:
   - Função `apply_lan`: aplica nos 3 contêineres `tc qdisc add dev eth0 root netem delay 0.5ms` (RTT = 1.0ms, perda 0%).
   - Função `apply_wan`: aplica nos 3 contêineres `tc qdisc add dev eth0 root netem delay 25ms loss 2%` (RTT = 50.0ms, perda 2%).
   - Função `clean_netem`: executa `tc qdisc del dev eth0 root` em todos os contêineres.
3. `run_experiments.sh` e `run_experiments.ps1`:
   - Orquestrador mestre 1-click (exigido pelo edital para evitar penalidade de -15 pontos).
   - Executa sequencialmente: subida dos contêineres -> setup LAN -> testes T01 a T03 (Carga A) e T07 a T09 (Carga B) -> setup WAN -> testes T04 a T06 (Carga A) e T10 a T12 (Carga B) -> limpeza netem -> disparo do script de análise e gráficos -> encerramento do ambiente.

Garanta tratamento de erros e logs coloridos e informativos no terminal.
```

---

## 🐍 Prompt 3: Cliente de Benchmark em Python Assíncrono (`httpx` + `aioquic`)

```text
Você é um desenvolvedor sênior em Python especializado em sistemas assíncronos e redes de alta performance. Estamos implementando o cliente de medição da 2ª Avaliação Prática de Redes II da UFPI.

Consulte:
- brain/03_experimentos/cenarios_de_teste.md
- brain/03_experimentos/metricas_e_analise_dados.md

Implemente a aplicação cliente em `benchmark/`:
1. `benchmark/requirements.txt`: `httpx[http2]`, `aioquic`, `asyncio`, `pandas`, `scipy`.
2. `benchmark/client.py`:
   - Suporte a HTTP/1.1 e HTTP/2 via `httpx.AsyncClient`.
   - Suporte nativo a HTTP/3 QUIC via `aioquic`.
   - Coleta de métricas com precisão de microssegundos via `time.perf_counter()`: TTFB, Total Load Time, Goodput (Mbps), RPS, Status Code.
3. **Controle Rigoroso de Viés de Sessão (Client-Side Bias Control - OBRIGATÓRIO PARA EVITAR -10 PONTOS)**:
   - Modo Cold TTFB: deve criar e fechar explicitamente a sessão com `await client.aclose()` antes de cada requisição individual, proibindo connection pooling / reuso de conexões.
   - Modo Warm Connection: deve estabelecer previamente uma única conexão persistente e disparar as 100 requisições simultâneas da Carga B sobre o mesmo canal aquecido para avaliar a multiplexação real.
4. Exportação dos dados brutos com timestamp detalhado para `data/raw/results.json` e `data/raw/results.csv`.
5. Parâmetros de CLI (`argparse`) permitindo rodar repetições individuais ou lotes completos com $N=10$.

Código limpo, com tipagem e tratamento de exceções de conexão e timeouts.
```

---

## 📊 Prompt 4: Pipeline de Tratamento Estatístico e Visualização Gráfica

```text
Você é um cientista de dados especializado em redes e medições experimentais. Estamos implementando a análise estatística da 2ª Avaliação Prática de Redes II da UFPI.

Consulte:
- brain/03_experimentos/metricas_e_analise_dados.md

Implemente:
1. `analysis/process_data.py`:
   - Carrega `data/raw/results.json` ou `results.csv`.
   - Calcula média, mediana, desvio padrão, percentis p50 e p99, e Intervalo de Confiança de 95% via t-Student ($t_{0.025, 9} \approx 2.262$ para $N=10$) para TTFB, Goodput, Total Load Time e RPS em cada um dos 12 testes (T01 a T12).
   - Exporta tabelas consolidadas em CSV e código de tabelas formatadas em LaTeX para inclusão no artigo.
2. `analysis/plot_results.py`:
   - Gera gráficos científicos de alta qualidade visual a 300 DPI salvos em `data/plots/`.
   - **EXIGÊNCIA MANDATÓRIA (PENALIDADE DE -10 PONTOS SE FALTAR): TODOS os gráficos de barras e de linhas DEVEM conter barras de erro explícitas (`yerr=ci95` ou `yerr=std`) com capas visíveis (`capsize=5`)**.
   - Gráfico 1: Cold TTFB vs Warm TTFB por Protocolo (LAN vs WAN).
   - Gráfico 2: Vazão Sustentada (Goodput Mbps) na Carga A de 50MB (T01 a T06).
   - Gráfico 3: Tempo Total de Carregamento dos 100 objetos na Carga B (T07 a T12).
   - Gráfico 4: Requisições por Segundo (RPS) sob Perdas no Cenário WAN (T10 vs T11 vs T12).
   - Gráfico 5: Curva CDF de latência dos fluxos demonstrando a mitigação do HoL blocking no HTTP/3.
```

---

## 📝 Prompt 5: Redação do Relatório Técnico Científico (Padrão SBC / LaTeX)

```text
Você é um pesquisador em ciência da computação e especialista em redação científica. Estamos redigindo o artigo da 2ª Avaliação Prática de Redes de Computadores II da UFPI (2026-2).

Consulte:
- brain/04_entregaveis/relatorio_tecnico_academico.md
- brain/03_experimentos/cenarios_de_teste.md
- data/processed/ (tabelas e métricas)

Sua tarefa é redigir o documento completo em LaTeX no modelo oficial da SBC (`relatorio/artigo.tex` e `sbc.sty`):
1. **PÁGINA 1 OBRIGATÓRIA (CRITÉRIO ELIMINATÓRIO - NOTA ZERO SE FALTAR):**
   - Inserir o link público funcional do vídeo explicativo de 15 minutos no YouTube logo abaixo do resumo ou nos dados do autor.
2. Resumo e Abstract em inglês com palavras-chave formais.
3. Introdução e Metodologia detalhando a topologia Docker, parâmetros `tc netem` e o cliente Python com controle de viés.
4. Tabelas consolidadas e figuras científicas com barras de erro inseridas nos floats.
5. **FUNDAMENTAÇÃO TEÓRICA MANDATÓRIA (EXIGÊNCIA EXPRESSA DO EDITAL - ATÉ -20 PONTOS SE FALTAR):**
   - Confronte e articule formalmente os resultados dos testes WAN com:
     - **Tanenbaum Seção 6.5.11 (TCP CUBIC)**: demonstrar a fórmula da janela cúbica $W_{\text{cubic}}(t) = C(t - K)^3 + W_{\text{max}}$, explicar o recuo multiplicativo por perda ($\beta = 0.7$) e o colapso de throughput sob 2% de perda estocástica e RTT de 50ms nos testes T04 e T05.
     - **Tanenbaum Seção 6.6.1 (QUIC) e Seção 6.6.2 (BBR)**: explicar por que T06 e T12 mantêm alto desempenho, detalhando o desacoplamento de perdas por stream UDP e o modelo de pacing baseado em taxa de gargalo e RTT mínimo sem retração ingênua de janela.
6. Conclusões e bibliografia completa com referências formais (Tanenbaum, RFC 793, RFC 768, RFC 7540, RFC 8446, RFC 9000, RFC 9001, RFC 9114).
```

---

## 🔍 Prompt 6: Auditoria Final Pré-Submissão e Empacotamento

```text
Você é um auditor de conformidade técnica e acadêmica.
Sua missão é realizar uma checagem rigorosa de todos os critérios eliminatórios e penalidades do edital da 2ª Avaliação Prática de Redes II da UFPI:

1. Checar se todos os contêineres no `docker-compose.yml` possuem `cap_add: [NET_ADMIN]`.
2. Checar se o orquestrador `run_experiments.sh` executa de ponta a ponta sem comandos manuais intermediários.
3. Checar se o cliente Python implementou o fechamento de conexão para o teste de Cold TTFB.
4. Checar se todos os gráficos em `data/plots/` contêm barras de erro visíveis.
5. Checar se o PDF do relatório contém o link do YouTube na 1ª página e as seções citando Tanenbaum Seção 6.5.11 e Seção 6.6.1.
6. Gerar o arquivo ZIP final no padrão exigido: `TP2_Redes2_NomeAluno1_NomeAluno2.zip`.
```
