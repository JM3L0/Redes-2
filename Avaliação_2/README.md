# 🧠 CÉREBRO DO PROJETO: 2ª Avaliação Prática Redes II (2026-2)
## Estudo Experimental de Desempenho de Protocolos Web (HTTP/1.1 vs HTTPS/TLS vs HTTP/3-QUIC) em Ambiente Emulado com Docker e Python

**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Curso:** Bacharelado em Sistemas de Informação  
**Disciplina:** Redes de Computadores II (2026-2)  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)  
**Peso da Avaliação:** 50% da pontuação total da 2ª Avaliação (N2) — 100 pontos totais

---

## 📌 Visão Rápida e Navegação do Cérebro

Este repositório centraliza toda a base de conhecimento arquitetural, científica, experimental e operacional necessária para o cumprimento integral das exigências do Trabalho Prático da 2ª Avaliação.

Qualquer desenvolvedor ou agente de inteligência artificial que for operar neste projeto **DEVE** consultar os módulos do cérebro abaixo antes de implementar códigos ou relatórios:

| Módulo do Cérebro | Finalidade e Conteúdo |
| :--- | :--- |
| 📖 [**`brain/README.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/README.md) | Mapa de navegação e índice temático completo do diretório do cérebro. |
| 📋 [**`brain/01_diretrizes/visao_geral_e_regras.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/01_diretrizes/visao_geral_e_regras.md) | Visão executiva, fundamentação pedagógica, 3 fenômenos-chave, rubrica de 100 pontos, penalidades e critérios eliminatórios (Nota 0,0). |
| ✅ [**`brain/01_diretrizes/checklist_progresso.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/01_diretrizes/checklist_progresso.md) | Quadro kanban das 8 fases de desenvolvimento com checklist de validação pré-submissão. |
| 🏗️ [**`brain/02_arquitetura/arquitetura_e_docker.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/02_arquitetura/arquitetura_e_docker.md) | Topologia em Docker Compose, rede `net_bench` (172.20.0.0/16), 3 servidores (Nginx HTTP/1.1, Nginx HTTPS TLS 1.3, Caddy HTTP/3 QUIC), certificados TLS locais e diretiva `cap_add: NET_ADMIN`. |
| 🧪 [**`brain/03_experimentos/cenarios_de_teste.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/03_experimentos/cenarios_de_teste.md) | Cenário 1 (LAN: delay 0.5ms = RTT 1ms, 0% perda) vs Cenário 2 (WAN: delay 25ms = RTT 50ms, 2% perda), Cargas A (50 MB) e B (100x10 KB), e a matriz experimental exaustiva dos 12 testes (T01 a T12). |
| 📊 [**`brain/03_experimentos/metricas_e_analise_dados.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/03_experimentos/metricas_e_analise_dados.md) | Definição matemática de TTFB, Total Load Time, RPS, percentis p50/p99, rigor estatístico ($N \ge 10$, IC 95%, desvio padrão), controle de vício de sessão e regras de gráficos com **barras de erro obrigatórias**. |
| 📄 [**`brain/04_entregaveis/relatorio_tecnico_academico.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/04_entregaveis/relatorio_tecnico_academico.md) | Estrutura formal do relatório em PDF (padrão SBC/LaTeX), link mandatório do vídeo na 1ª página e articulação teórica obrigatória com Tanenbaum §6.5.11 (TCP CUBIC) e §6.6.1/§6.6.2 (QUIC/BBR). |
| 🎥 [**`brain/04_entregaveis/roteiro_video_15min.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/04_entregaveis/roteiro_video_15min.md) | Roteiro estruturado e cronometrado minuto a minuto para gravação do vídeo técnico de 15 minutos (código, execução ao vivo, gráficos e fundamentação teórica). |
| 🤖 [**`brain/05_prompts_ia/guia_de_prompts_ia.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/05_prompts_ia/guia_de_prompts_ia.md) | Prompts modulares prontos para delegar tarefas a agentes de IA em Docker, Shell, Python assíncrono (`httpx` + `aioquic`), tratamento estatístico e redação LaTeX. |
| 📑 [**`brain/06_relatorios_de_fases/README.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/06_relatorios_de_fases/README.md) | Diário de bordo detalhado com relatórios de engenharia e decisões de projeto registrados a cada fase. |

---

## 🚨 REGRAS CRÍTICAS E CRITÉRIOS DE NOTA ZERO

> [!CAUTION]
> ### 🛑 AVISO IMPORTANTE — CRITÉRIO EXCLUDENTE (NOTA ZERO)
> A avaliação prescreve que a entrega final deve conter impreterivelmente:
> 1. O **código-fonte completo e funcional** da infraestrutura Docker e do cliente Python de benchmark;
> 2. O **Relatório Técnico em PDF** com rigor de publicação acadêmica;
> 3. O **link público funcional para o vídeo de exatamente 15 minutos** gravado e hospedado no YouTube (Público/Não-listado), inserido **obrigatoriamente na 1ª página do relatório técnico**.
>
> **A ausência do código, a ausência do relatório em PDF ou a ausência/inoperância do link do vídeo implicará a atribuição automática de NOTA ZERO (0,0), sem possibilidade de recuperação ou recurso.**

### ⚠️ Tabela de Penalidades Diretas do Edital

| Infração Técnica | Penalidade na Nota |
| :--- | :---: |
| Ausência de execução automatizada via comando único (`run_experiments.sh`) | **-15 Pontos** |
| Falta de controle de vício de sessão no cliente Python (reuso indevido de conexões no teste de TTFB) | **-10 Pontos** |
| Ausência de barras de erro (desvio padrão / IC 95%) nos gráficos gerados | **-10 Pontos** |
| Relatório puramente descritivo (sem fundamentação explícita em Tanenbaum §6.5.11 e §6.6.1) | **-20 Pontos** |
| Falta de código, relatório ou vídeo | **NOTA ZERO (0.0)** |

---

## 🎯 Síntese da Matriz Experimental dos 12 Testes

| Teste | Perfil de Carga | Protocolo Alvo | Servidor Docker | Cenário de Rede | Foco Analítico Principal |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **T01** | Carga A (50 MB) | HTTP/1.1 | `server_http11` (Porta 8080) | Cenário 1 (LAN: 1ms, 0%) | Vazão máxima TCP em canal ideal sem segurança |
| **T02** | Carga A (50 MB) | HTTPS / TLS 1.3 | `server_http2_tls` (Porta 8443) | Cenário 1 (LAN: 1ms, 0%) | Custo de cifragem simétrica TLS 1.3 em regime permanente |
| **T03** | Carga A (50 MB) | HTTP/3 (QUIC) | `server_http3_quic` (Porta 9443) | Cenário 1 (LAN: 1ms, 0%) | Eficiência do protocolo QUIC em user-space sem perdas |
| **T04** | Carga A (50 MB) | HTTP/1.1 | `server_http11` (Porta 8080) | Cenário 2 (WAN: 50ms, 2%) | Sensibilidade do TCP CUBIC a perdas e latência (Tanenbaum §6.5.11) |
| **T05** | Carga A (50 MB) | HTTPS / TLS 1.3 | `server_http2_tls` (Porta 8443) | Cenário 2 (WAN: 50ms, 2%) | Degradação do TCP CUBIC + TLS 1.3 sob perdas estocásticas |
| **T06** | Carga A (50 MB) | HTTP/3 (QUIC) | `server_http3_quic` (Porta 9443) | Cenário 2 (WAN: 50ms, 2%) | Controle de congestionamento QUIC/BBR sob perdas (Tanenbaum §6.6.1/§6.6.2) |
| **T07** | Carga B (100x10KB) | HTTP/1.1 | `server_http11` (Porta 8080) | Cenário 1 (LAN: 1ms, 0%) | Overhead de múltiplos handshakes TCP e conexões paralelas |
| **T08** | Carga B (100x10KB) | HTTPS / TLS 1.3 | `server_http2_tls` (Porta 8443) | Cenário 1 (LAN: 1ms, 0%) | Eficiência da multiplexação HTTP/2 em canal de baixa latência |
| **T09** | Carga B (100x10KB) | HTTP/3 (QUIC) | `server_http3_quic` (Porta 9443) | Cenário 1 (LAN: 1ms, 0%) | Desempenho de fluxos QUIC independentes em rede ideal |
| **T10** | Carga B (100x10KB) | HTTP/1.1 | `server_http11` (Porta 8080) | Cenário 2 (WAN: 50ms, 2%) | Severidade do HoL blocking na Camada de Aplicação |
| **T11** | Carga B (100x10KB) | HTTPS / TLS 1.3 | `server_http2_tls` (Porta 8443) | Cenário 2 (WAN: 50ms, 2%) | Severidade do HoL blocking na Camada de Transporte TCP |
| **T12** | Carga B (100x10KB) | HTTP/3 (QUIC) | `server_http3_quic` (Porta 9443) | Cenário 2 (WAN: 50ms, 2%) | Mitigação total do HoL blocking via fluxos UDP isolados |

---

## 📁 Estrutura de Diretórios Recomendada para o Projeto

```text
Avaliação_2/
├── Segunda Avaliação Redes 2.pdf   # Edital oficial da 2ª Avaliação
├── README.md                       # Este arquivo (Dashboard e Índice Central)
├── AGENTS.md                       # Instruções de contexto para agentes de IA
├── run_experiments.sh              # Orquestrador mestre 1-click (Linux / WSL / Mac)
├── run_experiments.ps1             # Orquestrador mestre 1-click (Windows PowerShell)
├── brain/                          # Cérebro técnico e científico do projeto
│   ├── README.md                   # Mapa do cérebro
│   ├── 01_diretrizes/              # Regras, visão geral e checklist kanban
│   │   ├── visao_geral_e_regras.md
│   │   └── checklist_progresso.md
│   ├── 02_arquitetura/             # Docker Compose, Caddy, NGINX, certs e tc netem
│   │   └── arquitetura_e_docker.md
│   ├── 03_experimentos/            # Cenários de teste, cargas e análise de dados
│   │   ├── cenarios_de_teste.md
│   │   └── metricas_e_analise_dados.md
│   ├── 04_entregaveis/             # Relatório técnico e roteiro do vídeo de 15min
│   │   ├── relatorio_tecnico_academico.md
│   │   └── roteiro_video_15min.md
│   ├── 05_prompts_ia/              # Prompts cirúrgicos para automação de IA
│   │   └── guia_de_prompts_ia.md
│   └── 06_relatorios_de_fases/     # Diário de bordo detalhado por fase
│       ├── README.md
│       └── fase_01_analise_e_estruturacao.md
├── docker/                         # Infraestrutura dos 3 servidores Web
│   ├── docker-compose.yml          # Topologia com net_bench (172.20.0.0/16) e cap_add: NET_ADMIN
│   ├── certs/                      # Certificados TLS 1.3 locais com SANs válidos
│   ├── server-http1/               # Configuração Nginx HTTP/1.1 (porta 80 / 8080)
│   │   └── nginx.conf
│   ├── server-http2/               # Configuração Nginx HTTPS / HTTP/2 (porta 443 / 8443)
│   │   └── nginx.conf
│   └── server-http3/               # Configuração Caddy HTTP/3 QUIC (porta 443 TCP/UDP / 9443)
│       └── Caddyfile
├── benchmark/                      # Cliente de benchmark em Python
│   ├── client.py                   # Cliente assíncrono httpx + aioquic
│   ├── session_control.py          # Controle de viés de sessão (Cold TTFB vs Warm)
│   └── requirements.txt            # Dependências Python (httpx, aioquic, etc.)
├── scripts/                        # Scripts de automação e emulação
│   ├── setup_netem.sh              # Aplicação e limpeza de tc netem (LAN vs WAN)
│   └── generate_payloads.py        # Geração das cargas sintéticas (50MB e 100x10KB)
├── data/                           # Armazenamento de dados do experimento
│   ├── static/                     # Objetos de teste (50MB.bin e objects/obj_*.bin)
│   ├── raw/                        # results.json e results.csv com timestamps
│   ├── processed/                  # Tabelas consolidadas (médias, medianas, p50, p99, IC95%)
│   └── plots/                      # Figuras científicas com barras de erro obrigatórias
├── analysis/                       # Pipeline estatístico e de visualização
│   ├── process_data.py             # Consolidação dos resultados brutos
│   └── plot_results.py             # Geração de gráficos com matplotlib/seaborn e barras de erro
├── relatorio/                      # Artigo técnico científico em padrão SBC (LaTeX)
│   ├── sbc-template.tex            # Documento principal
│   ├── sbc.sty                     # Folha de estilo SBC
│   ├── referencias.bib             # Referências bibliográficas (Tanenbaum, RFCs)
│   └── figures/                    # Figuras e diagramas exportados
└── video/                          # Materiais de suporte ao vídeo de 15 minutos
    ├── slide_deck/                 # Slides de apoio
    └── roteiro_cronometrado.md     # Roteiro detalhado para apresentação
```
