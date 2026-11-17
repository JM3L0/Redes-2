# 06. Guia de Prompts Prontos para IAs — 3ª Avaliação (N3)

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Curso:** Bacharelado em Sistemas de Informação  
**Equipe:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`) & Marcos Willian de Sousa e Silva (`marcos.sousa@ufpi.edu.br`)

Utilize os prompts estruturados abaixo para orientar agentes de inteligência artificial em cada uma das fases subsequentes do desenvolvimento da 3ª Avaliação (N3), garantindo conformidade estrita com o edital (`Terceira Avaliacao.pdf`) e prevenindo todas as penalidades.

---

## 🚀 Prompt 1: Infraestrutura Docker (`docker-compose.yml`), Certificados TLS 1.3 e Objeto de 1 KB

```text
Você é um engenheiro de redes sênior especialista em Linux, Docker, Caddy e iperf3. Estamos implementando a 3ª Avaliação Prática (N3) de Redes de Computadores II da UFPI (2026-2): Análise Experimental de Controle de Congestionamento (TCP CUBIC vs. BBR) e Retomada de Sessão (0-RTT) em Redes Degradadas.

Consulte os arquivos de contexto no cérebro do projeto:
- brain/01_diretrizes/visao_geral_e_regras.md
- brain/02_arquitetura/arquitetura_e_docker.md

Sua tarefa é criar a infraestrutura declarativa e os scripts de preparação:
1. `docker-compose.yml` na raiz do projeto:
   - Rede bridge `net_bench` com subnet `172.20.0.0/16`.
   - Serviço `server-tcp` (`container_name: server_tcp_cc`): imagem `networkstatic/iperf3`, `cap_add: [NET_ADMIN]`, `command: -s`, IP `172.20.0.10`.
   - Serviço `server-http3` (`container_name: server_http3_quic`): imagem `caddy:2.7-alpine`, `cap_add: [NET_ADMIN]`, volumes `./certs:/etc/caddy/certs`, `./site:/usr/share/caddy` e `./docker/Caddyfile:/etc/caddy/Caddyfile:ro`, IP `172.20.0.30`.
   - Serviço `client-bench` (`container_name: client_bench`): `cap_add: [NET_ADMIN]`, `entrypoint: ["sleep", "infinity"]`, IP `172.20.0.50`, garantindo suporte simultâneo a `curl --http3-only`, `curl --http2`, `iperf3` e `tc`.
2. `docker/Caddyfile`: configurado para servir `/usr/share/caddy` via HTTPS na porta 443 com TLS 1.3 (`protocols h1 h2 h3` e `allow_0rtt`), usando `/etc/caddy/certs/cert.pem` e `key.pem`.
3. `scripts/generate_certs.py`: gera certificado X.509 v3 autoassinado em `./certs/cert.pem` e `./certs/key.pem` com Subject Alternative Names (SANs) cobrindo `localhost`, `server_http3_quic`, `127.0.0.1` e `172.20.0.30`.
4. `scripts/generate_payloads.py`: gera o objeto estático de exatamente 1 KB (`1024` bytes) em `./site/1KB.bin` e `./site/index.html`.
```

---

## 🌐 Prompt 2: Emulação de Rede `tc netem` (3 Cenários + Limpeza) e Script de Automação (`run_n3`)

```text
Você é um especialista em automação de experimentos de redes no Linux com `tc netem`, `iperf3` e `curl`. Estamos implementando a automação da 3ª Avaliação (N3) de Redes II da UFPI.

Consulte:
- brain/02_arquitetura/arquitetura_e_docker.md
- brain/03_experimentos/cenarios_de_teste.md

Sua tarefa é implementar os módulos de controle de canal e o orquestrador mestre:
1. `scripts/setup_netem.py`, `scripts/setup_netem.sh` e `scripts/setup_netem.ps1`:
   - `lan`: aplica o Cenário 1 (atraso unidirecional de 0.5ms -> RTT total de 1ms, 0% perda).
   - `wan_loss`: aplica o Cenário 2 (atraso unidirecional de 25ms -> RTT total de 50ms, 2% perda estocástica).
   - `wan_noloss`: aplica o Cenário 3 (atraso unidirecional de 25ms -> RTT total de 50ms, 0% perda).
   - `clean`: limpa as interfaces com `tc qdisc del dev eth0 root`.
2. `run_n3.py`, `run_n3.sh` e `run_n3.ps1`:
   - Garante módulos `tcp_cubic` e `tcp_bbr` ativos no kernel.
   - Executa no mínimo 5 repetições independentes (N >= 5) dos 6 testes essenciais:
     * Bloco A (fluxo de 15s via `iperf3 -c 172.20.0.10 -t 15 -C <cubic|bbr> -J`):
       - E01: TCP CUBIC sob Cenário 1 (LAN: 1ms, 0% perda)
       - E02: TCP CUBIC sob Cenário 2 (WAN: 50ms, 2% perda)
       - E03: TCP BBR sob Cenário 2 (WAN: 50ms, 2% perda)
     * Bloco B (transferência de 1 KB via `curl -w "%{time_starttransfer}"` sob Cenário 3 WAN: 50ms, 0% perda):
       - E04: HTTPS (HTTP/2 sobre TCP+TLS)
       - E05: HTTP/3 Cold (1-RTT)
       - E06: HTTP/3 Warm / Resumption (requisições sequenciais / session tickets 0-RTT)
   - Exporta os dados brutos para `data/raw/results.csv` e `data/raw/results.json`.
   - Limpa o ambiente ao final e aciona os scripts de processamento e gráficos.
```

---

## 📊 Prompt 3: Coleta Estatística, Tabela Resumo e os 2 Gráficos com Barras de Erro

```text
Você é um cientista de dados especializado em avaliação de desempenho de redes. Estamos implementando o pipeline analítico da 3ª Avaliação (N3) de Redes II da UFPI.

Consulte:
- brain/03_experimentos/metricas_e_analise_dados.md

Implemente:
1. `analysis/process_data.py`:
   - Lê `data/raw/results.csv` / `results.json`.
   - Para o Bloco A (E01, E02, E03): calcula média e desvio padrão de Vazão (Mbps), média e desvio padrão de retransmissões e o TOTAL de retransmissões nas 5 repetições.
   - Para o Bloco B (E04, E05, E06): calcula média e desvio padrão de TTFB (`time_starttransfer` em ms).
   - Exporta `data/processed/summary_table.csv` e `data/processed/summary_table.tex`.
2. `analysis/plot_results.py`:
   - Gera programaticamente a 300 DPI os 2 gráficos obrigatórios com BARRAS DE ERRO (desvio padrão) para evitar a penalidade de -10 pontos:
     * Gráfico 1 (`data/plots/fig1_bloco_a_vazao_cc.png`): Vazão média (Mbps) comparando TCP CUBIC (LAN/WAN) e TCP BBR (WAN), com barras de erro (desvio padrão) e rótulos completos.
     * Gráfico 2 (`data/plots/fig2_bloco_b_ttfb_handshake.png`): TTFB médio (ms) comparando HTTP/2 vs. HTTP/3 Cold vs. HTTP/3 Warm/Resumed, com barras de erro (desvio padrão) e linhas de referência de 1 RTT (50ms), 2 RTTs (100ms) e 3 RTTs (150ms).
```

---

## 📝 Prompt 4: Redação do Relatório Técnico Conciso (SBRC — 4 a 6 Páginas)

```text
Você é um pesquisador em redes de computadores e especialista em LaTeX no padrão SBC/SBRC. Estamos redigindo o Relatório Técnico Conciso da 3ª Avaliação (N3) de Redes II da UFPI (vale 50 pontos na rubrica).

Consulte:
- brain/04_entregaveis/relatorio_tecnico_academico.md
- data/processed/summary_table.csv

Redija `relatorio/sbc-template.tex` e compile `relatorio/sbc-template.pdf` observando estritamente:
1. EXTENSÃO OBRIGATÓRIA: mínimo de 4 páginas e máximo de 6 páginas no formato de artigo da SBRC (`sbc.sty`).
2. PÁGINA 1: incluir o link do vídeo no YouTube (15 a 25 min) logo abaixo da identificação dos autores (João Marcos Sousa Rufino Leal e Marcos Willian de Sousa e Silva).
3. ELEMENTOS VISUAIS E TABULARES:
   - Inserir o Gráfico 1 (Bloco A) e o Gráfico 2 (Bloco B) com barras de erro de desvio padrão.
   - Inserir a Tabela Resumo completa com médias, desvios-padrão e total de retransmissões (Bloco A) e médias/desvios-padrão de TTFB (Bloco B).
4. DISCUSSÃO TEÓRICA FUNDAMENTADA EM TANENBAUM 6ª EDIÇÃO (EVITA PENALIDADE DE -20 PONTOS):
   - Seção 6.5.11 (TCP CUBIC) e Seção 6.6.2 (BBR): explicar matematicamente e conceitualmente por que o CUBIC sofre degradação severa com 2% de perda na WAN (função cúbica e retração multiplicativa de cwnd), enquanto o BBR mantém alta vazão ao estimar o BDP (BtlBw x RTprop) e o RTT mínimo.
   - Seção 6.6.1 (QUIC): explicar a diferença empírica em milissegundos entre HTTP/2 (~150 ms = 3 RTTs), HTTP/3 Cold (~100 ms = 2 RTTs) e HTTP/3 Resumed (~50 ms = 1 RTT) em função do número de RTTs exigidos em cada handshake.
```

---

## 🔍 Prompt 5: Auditoria Pré-Submissão e Empacotamento SIGAA

```text
Você é um auditor independente de conformidade acadêmica. Verifique todos os entregáveis da 3ª Avaliação (N3) antes da submissão no SIGAA:
1. O arquivo `docker-compose.yml` contém `server_tcp_cc` (172.20.0.10), `server_http3_quic` (172.20.0.30) e `client_bench` (172.20.0.50) com `cap_add: [NET_ADMIN]`?
2. O script `run_n3.py` / `run_n3.sh` aplica os 3 cenários `tc netem`, executa >= 5 repetições dos 6 testes (E01 a E06), exporta `results.csv` e `results.json` e limpa as interfaces ao final?
3. Os Gráficos 1 e 2 possuem barras de erro (desvio padrão) visíveis e eixos rotulados?
4. O PDF do relatório (`relatorio/sbc-template.pdf`) está no formato SBRC, possui entre 4 e 6 páginas, inclui a Tabela Resumo, fundamenta os resultados nas Seções 6.5.11, 6.6.1 e 6.6.2 de Tanenbaum (6ª Ed.) e traz o link do vídeo na 1ª página?
5. Gere o pacote final `TP3_Redes2_JoaoMarcosSousaRufinoLeal_MarcosWilliandeSousaeSilva.zip`.
```
