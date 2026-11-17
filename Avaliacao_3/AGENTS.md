# Avaliação 3 (N3) — Controle de Congestionamento (TCP CUBIC vs. BBR) e Retomada de Sessão (0-RTT) em Redes Degradadas

Repositório experimental para análise empírica de mecanismos avançados da camada de transporte moderna: Controle de Congestionamento Baseado em Perda vs. Baseado em Modelo (**TCP CUBIC vs. TCP BBR**) e Estabelecimento Rápido de Conexão / Retomada de Sessão no QUIC (**HTTPS/HTTP/2 vs. HTTP/3 1-RTT Cold vs. HTTP/3 0-RTT Warm/Resumption**) sob condições controladas de rede com Docker e Linux Traffic Control (`tc netem`).

- **Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)
- **Disciplina:** Redes de Computadores II (2026-2)
- **Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)

---

## Estrutura do Módulo

- `run_n3.py` / `run_n3.sh` / `run_n3.ps1`: Orquestradores mestres 1-click que sobem a infraestrutura, aplicam as regras `tc netem` dos 3 cenários, executam as $N \ge 5$ repetições dos 6 testes essenciais (E01 a E06), exportam os dados brutos (`CSV`/`JSON`), geram os gráficos com barras de erro e limpam o ambiente ao final.
- `docker/`:
  - `docker-compose.yml`: Topologia declarativa na rede `net_bench` (`172.20.0.0/16`) contendo `server_tcp_cc` (`172.20.0.10`), `server_http3_quic` (`172.20.0.30`) e `client_bench` (`172.20.0.50`) com `cap_add: [NET_ADMIN]`.
  - `Caddyfile`: Configuração do servidor Caddy 2.7 Alpine para HTTP/2 (TLS 1.3 sobre TCP) e HTTP/3 (QUIC sobre UDP) com suporte a Session Resumption / 0-RTT.
  - `certs/`: Certificados TLS 1.3 autoassinados com Subject Alternative Names (SANs) para `172.20.0.30`, `server_http3_quic` e `localhost`.
  - `site/`: Diretório estático contendo o objeto de teste de 1 KB (`1KB.bin` / `index.html`) para os ensaios do Bloco B.
- `scripts/`:
  - `generate_certs.py`: Geração automatizada de certificados X.509 v3 TLS 1.3.
  - `generate_payloads.py`: Geração determinística do objeto estático de 1 KB (`1024` bytes) para os testes E04, E05 e E06.
  - `setup_netem.py` / `setup_netem.sh` / `setup_netem.ps1`: Aplicação e limpeza das regras `tc netem` (Cenário 1 LAN, Cenário 2 WAN com perda, Cenário 3 WAN sem perda).
- `analysis/`:
  - `process_data.py`: Consolidação estatística das $\ge 5$ repetições por teste (média, desvio padrão amostral, IC 95% e total de retransmissões), exportando `summary_table.csv` e `summary_table.tex`.
  - `plot_results.py`: Geração programática a 300 DPI dos 2 gráficos obrigatórios com **barras de erro (desvio padrão)**.
- `data/`:
  - `raw/`: Dados brutos dos 6 testes (`results.json`, `results.csv` e logs JSON do `iperf3`).
  - `processed/`: Tabelas resumo estatísticas (`summary_table.csv`, `summary_table.tex`).
  - `plots/`: Gráfico 1 (`fig1_bloco_a_vazao_cc.png`) e Gráfico 2 (`fig2_bloco_b_ttfb_handshake.png`).
- `relatorio/`: Artigo técnico conciso no formato oficial **SBRC / SBC (LaTeX)** (4 a 6 páginas) compilado em PDF com o link do vídeo na 1ª página.
- `brain/`: Cérebro do projeto contendo diretrizes, modelagem arquitetural, matriz experimental, teoria de Tanenbaum (6ª Ed.), roteiro de vídeo (15 a 25 min), prompts e relatórios de fases.

---

## Comandos Essenciais

### Execução Completa Automatizada (1-Click Run)

Via Python (Multiplataforma — Windows, Linux, macOS, WSL):
```bash
python run_n3.py
```

No Linux / macOS / WSL / Git Bash:
```bash
chmod +x run_n3.sh
./run_n3.sh
```

No Windows PowerShell:
```powershell
.\run_n3.ps1
```

---

## Regras Críticas de Conformidade (Edital N3)

1. **Permissão `NET_ADMIN` Obrigatória**: Todos os contêineres (`server_tcp_cc`, `server_http3_quic`, `client_bench`) devem declarar `cap_add: - NET_ADMIN` no `docker-compose.yml` e ser manipulados com `docker exec --privileged` nos comandos `tc qdisc`.
2. **Precisão Sintática do `tc netem`**:
   - **Cenário 1 (LAN - Canal Ideal):** `delay 0.5ms` (RTT total = 1 ms, 0% perda) — usado em **E01**.
   - **Cenário 2 (WAN - Canal Degradado):** `delay 25ms loss 2%` (RTT total = 50 ms, 2% perda estocástica) — usado em **E02** e **E03**.
   - **Cenário 3 (WAN sem Perda - Isolamento de Handshake):** `delay 25ms` (RTT total = 50 ms, 0% perda) — usado em **E04**, **E05** e **E06**.
   - **Limpeza Obrigatória:** `tc qdisc del dev eth0 root` ao término de cada cenário e ao final da bateria.
3. **Rigor Estatístico e Gráficos com Barras de Erro (-10 Pontos se ausentes)**:
   - Mínimo de **5 repetições independentes** ($N \ge 5$) para cada um dos 6 testes (E01 a E06).
   - **Gráfico 1 (Bloco A)** e **Gráfico 2 (Bloco B)** gerados programaticamente DEVEM exibir **barras de erro representando o desvio padrão** e eixos devidamente rotulados.
4. **Articulação Teórica com Tanenbaum 6ª Edição (-20 Pontos se puramente descritivo)**:
   - **Seção 6.5.11 (TCP CUBIC) e Seção 6.6.2 (BBR):** Fundamentar por que o CUBIC colapsa a janela `cwnd` com 2% de perda estocástica enquanto o BBR mantém alta vazão estimando continuamente a largura de banda de gargalo ($BtlBw$) e o RTT mínimo ($RTprop$) para operar no ponto ótimo do BDP.
   - **Seção 6.6.1 (QUIC):** Explicar em milissegundos a diferença empírica entre HTTP/2 (E04), HTTP/3 Cold 1-RTT (E05) e HTTP/3 Warm/Resumed 0-RTT (E06) em função do número de RTTs consumidos no handshake.
5. **Formato e Extensão do Relatório Técnico (50 Pontos)**:
   - Padrão de artigo da **SBRC / SBC** em PDF, contendo **mínimo de 4 e máximo de 6 páginas**.
6. **Critério Eliminatório (Nota 0,0)**:
   - A entrega no SIGAA (`TP3_Redes2_JoaoMarcosSousaRufinoLeal.zip`) exige obrigatoriamente: **(1) arquivos-fonte e scripts de automação**, **(2) relatório técnico em PDF (4–6 páginas)** e **(3) link funcional do vídeo no YouTube (15 a 25 minutos)** inserido no relatório. A ausência de qualquer um destes itens ou plágio implica **Nota 0,0**.
