# Avaliação 3 (N3) — Análise Experimental de Controle de Congestionamento (TCP CUBIC vs. BBR) e Retomada de Sessão (0-RTT) em Redes Degradadas

**Universidade Federal do Piauí (UFPI)** — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Curso:** Bacharelado em Sistemas de Informação  
**Disciplina:** Redes de Computadores II (2026-2)  
**Equipe:** João Marcos Sousa Rufino Leal & Marcos Willian de Sousa e Silva  
**E-mails:** `jsousarufinoleal@ufpi.edu.br` | `marcos.sousa@ufpi.edu.br`  
**Pontuação Total:** 100 Pontos (3ª Avaliação — N3)

---

## 🧭 Visão Geral do Projeto

Este repositório implementa a bancada experimental automatizada da **3ª Avaliação (N3)** de Redes de Computadores II, dando continuidade direta à infraestrutura em contêineres Docker e à emulação física de canal via Linux Traffic Control (`tc netem`) desenvolvidas na avaliação anterior.

O trabalho investiga empiricamente dois mecanismos avançados da camada de transporte moderna:
1. **Controle de Congestionamento Baseado em Perda vs. Baseado em Modelo (Bloco A — TCP CUBIC vs. TCP BBR):** Avaliação em fluxos contínuos de 15 segundos via `iperf3` comparando a retração drástica da janela de congestionamento (*cwnd*) do TCP CUBIC diante de descartes estocásticos (**Tanenbaum 6ª Ed., Seção 6.5.11**) contra o modelo proativo do algoritmo BBR (*Bottleneck Bandwidth and Round-trip propagation time*), que estima continuamente a banda de gargalo e o RTT mínimo para operar no ponto ótimo do Produto Largura de Banda-Atraso (BDP) (**Tanenbaum 6ª Ed., Seção 6.6.2**).
2. **Estabelecimento Rápido de Conexão e Retomada de Sessão no QUIC (Bloco B — HTTP/2 vs. HTTP/3 1-RTT Cold vs. HTTP/3 0-RTT Warm/Resumption):** Medição do *Time to First Byte* (`%{time_starttransfer}`) via `curl` para um objeto estático de 1 KB sob canal WAN de 50 ms de RTT sem perdas, isolando matematicamente o custo cumulativo dos handshakes TCP + TLS 1.3 no HTTP/2 contra o handshake integrado de 1-RTT e a retomada de sessão 0-RTT/reaproveitamento do protocolo QUIC (**Tanenbaum 6ª Ed., Seção 6.6.1**).

---

## ⚡ Execução Automatizada (1-Click Runner)

Conforme especificado na Seção 5 e no Eixo 1 da Rubrica, toda a bateria experimental é executada de ponta a ponta sem intervenção manual:

### Opção 1 — Orquestrador Python Multiplataforma (Recomendado):
```bash
python run_n3.py
```

### Opção 2 — Linux, macOS ou WSL 2 (Bash):
```bash
chmod +x run_n3.sh
./run_n3.sh
```

### Opção 3 — Windows (PowerShell):
```powershell
.\run_n3.ps1
```

### O que o Orquestrador (`run_n3`) executa automaticamente:
1. Gera os certificados TLS 1.3 com SANs válidos (`scripts/generate_certs.py`) e o objeto sintético de 1 KB (`scripts/generate_payloads.py`);
2. Sobe os contêineres Docker (`server_tcp_cc`, `server_http3_quic`, `client_bench`) na rede isolada `net_bench` (`172.20.0.0/16`) com `cap_add: [NET_ADMIN]`;
3. Verifica e habilita os algoritmos de controle de congestionamento `cubic` e `bbr` no kernel;
4. **Bloco A (Fluxo de 15s via `iperf3`, $N \ge 5$ repetições por teste):**
   - Aplica o **Cenário 1 (LAN: delay 0.5ms $\implies$ RTT = 1 ms, 0% perda)** e executa **E01** (`TCP CUBIC`);
   - Aplica o **Cenário 2 (WAN Degradada: delay 25ms, loss 2% $\implies$ RTT = 50 ms, 2% perda)** e executa **E02** (`TCP CUBIC`) e **E03** (`TCP BBR`);
5. **Bloco B (Transferência de 1 KB via `curl`, $N \ge 5$ repetições por teste):**
   - Aplica o **Cenário 3 (WAN sem Perda: delay 25ms $\implies$ RTT = 50 ms, 0% perda)** e executa **E04** (`HTTPS / HTTP/2`), **E05** (`HTTP/3 Cold 1-RTT`) e **E06** (`HTTP/3 Warm / Resumption 0-RTT`);
6. Limpa todas as interfaces de rede (`tc qdisc del dev eth0 root`);
7. Exporta os dados brutos estruturados em `data/raw/results.csv` e `data/raw/results.json`;
8. Executa a consolidação estatística (`analysis/process_data.py`) e gera programaticamente os **2 gráficos comparativos com barras de erro de desvio padrão** (`analysis/plot_results.py`).

---

## 📂 Estrutura do Repositório

```text
Avaliacao_3/
├── run_n3.py                 # Orquestrador mestre multiplataforma em Python
├── run_n3.sh                 # Orquestrador mestre em Bash (Linux / WSL / macOS)
├── run_n3.ps1                # Orquestrador mestre em PowerShell (Windows)
├── docker-compose.yml        # Especificação declarativa dos contêineres (server-tcp, server-http3, client-bench)
├── requirements.txt          # Dependências Python para análise e plotagem (pandas, numpy, matplotlib, cryptography)
├── AGENTS.md                 # Diretrizes operacionais e regras de conformidade para agentes
├── README.md                 # Este manual técnico completo
│
├── brain/                    # Cérebro do Projeto (Arquitetura de Conhecimento e Planejamento)
│   ├── README.md             # Mapa de navegação do Cérebro da 3ª Avaliação
│   ├── 01_diretrizes/        # Visão geral, regras críticas, checklist kanban e auditoria de conformidade
│   ├── 02_arquitetura/       # Topologia Docker, Caddyfile, certificados TLS 1.3 e comandos tc netem
│   ├── 03_experimentos/      # Cenários 1, 2 e 3, matriz reduzida (E01 a E06) e modelagem estatística
│   ├── 04_entregaveis/       # Guia do Relatório SBRC (4–6 págs) e Roteiro do Vídeo (15–25 min)
│   ├── 05_prompts_ia/        # Prompts modulares para automação e verificação das fases
│   ├── 06_relatorios_de_fases/ # Diário de bordo detalhado por fase de execução
│   └── video/                # Material completo de apoio à gravação do vídeo no YouTube
│
├── certs/                    # Certificados TLS 1.3 (cert.pem, key.pem) montados no Caddy
├── site/                     # Conteúdo estático servido pelo Caddy (objeto de 1 KB para o Bloco B)
├── docker/                   # Configurações auxiliares de contêineres (Caddyfile, Dockerfile cliente)
├── scripts/                  # Scripts modulares de geração de certificados, payload e regras tc netem
├── analysis/                 # Processamento estatístico (process_data.py) e gráficos (plot_results.py)
├── data/                     # Dados brutos (raw/), tabelas processadas (processed/) e figuras (plots/)
└── relatorio/                # Artigo Técnico no formato SBRC / SBC em LaTeX (4 a 6 páginas)
```

---

## 🧪 Matriz Experimental Reduzida (6 Testes Essenciais — $N \ge 5$)

### Bloco A: Impacto do Controle de Congestionamento (Fluxo de 15s via `iperf3`)

| ID | Algoritmo / Protocolo | Cenário `tc netem` | Métrica Principal | Foco Analítico Principal |
| :---: | :---: | :---: | :---: | :--- |
| **E01** | **TCP CUBIC** | Cenário 1: LAN (`1 ms` RTT, `0%` perda) | Vazão (Mbps) e Retransmissões | Baseline de capacidade máxima em canal ideal |
| **E02** | **TCP CUBIC** | Cenário 2: WAN (`50 ms` RTT, `2%` perda) | Vazão (Mbps) e Retransmissões | Colapso severo da janela *cwnd* por perda estocástica (Tanenbaum Seção 6.5.11) |
| **E03** | **TCP BBR** | Cenário 2: WAN (`50 ms` RTT, `2%` perda) | Vazão (Mbps) e Retransmissões | Resiliência do modelo baseado em BDP e RTT mínimo (Tanenbaum Seção 6.6.2) |

### Bloco B: Latência de Handshake e Session Resumption no HTTP/3 (`curl` — Objeto de 1 KB)

| ID | Modo de Conexão | Cenário `tc netem` | Métrica Principal | Foco Analítico Principal |
| :---: | :---: | :---: | :---: | :--- |
| **E04** | **HTTPS (HTTP/2 sobre TCP+TLS)** | Cenário 3: WAN (`50 ms` RTT, `0%` perda) | TTFB (`time_starttransfer`) | Custo cumulativo de handshakes sequenciais (TCP 1-RTT + TLS 1.3 1-RTT) |
| **E05** | **HTTP/3 Cold (1-RTT)** | Cenário 3: WAN (`50 ms` RTT, `0%` perda) | TTFB (`time_starttransfer`) | Handshake integrado QUIC + TLS 1.3 em apenas 1 RTT (Tanenbaum Seção 6.6.1) |
| **E06** | **HTTP/3 Warm / Resumption** | Cenário 3: WAN (`50 ms` RTT, `0%` perda) | TTFB (`time_starttransfer`) | Redução de latência via reaproveitamento de sessão / 0-RTT |

---

## 🎯 Rubrica de Avaliação (100 Pontos) e Blindagem contra Penalidades

| Eixo / Critério do Edital | Pontuação / Sanção | Blindagem Implementada no Projeto |
| :--- | :---: | :--- |
| **1. Infraestrutura Docker e Automação `tc netem`** | **10 Pontos** | `docker-compose.yml` padronizado com `NET_ADMIN`, comandos exatos de `tc netem`, limpeza de interfaces e script `run_n3`. |
| **2. Coleta Estatística e Visualização Gráfica** | **10 Pontos** | $\ge 5$ amostras por teste, exportação CSV/JSON e 2 gráficos a 300 DPI com **barras de erro (desvio padrão)**. |
| **3. Relatório Técnico e Articulação Teórica** | **50 Pontos** | Artigo em formato **SBRC (PDF, 4 a 6 páginas)** com Tabela Resumo e fundamentação em **Tanenbaum 6ª Ed. (Seções 6.5.11, 6.6.1 e 6.6.2)**. |
| **4. Vídeo Explicativo no YouTube (Link)** | **30 Pontos** | Roteiro cronometrado de **15 a 25 minutos** com link público inserido na 1ª página do relatório em PDF. |
| **Penalidade: Ausência de barras de erro** | **-10 Pontos** | Parâmetro `yerr=std_dev` e `capsize=6` obrigatório nos Gráficos 1 e 2. |
| **Penalidade: Relatório puramente descritivo** | **-20 Pontos** | Dedução teórica explícita dos mecanismos de janela cúbica, BDP/pacing do BBR e contagem de RTTs no QUIC. |
| **Penalidade: Falta de vídeo, PDF ou código-fonte** | **NOTA 0,0** | Checklist de verificação pré-submissão garantindo os 3 entregáveis no pacote `.zip`. |

---

## 📦 Padrão de Submissão (SIGAA)

A entrega final é empacotada em arquivo único compactado `.zip` nomeado segundo o padrão oficial:
```text
TP3_Redes2_JoaoMarcosSousaRufinoLeal_MarcosWilliandeSousaeSilva.zip
```
Contendo o repositório de código/automação completo e o Relatório Técnico em PDF (4 a 6 páginas, formato SBRC) com o link do vídeo no YouTube (15 a 25 minutos).
