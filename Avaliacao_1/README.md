# 🧠 CÉREBRO DO PROJETO: Avaliação Prática Redes II (2026-2)
## Avaliação de Desempenho e Sobrecarga de Transporte — TCP, UDP e QUIC com NGINX e Linux
**Instituição:** Universidade Federal do Piauí (UFPI) — Bacharelado em Sistemas de Informação  
**Disciplina:** Redes de Computadores II (2026-2)

---

## 📌 Visão Rápida e Navegação do Cérebro

Este diretório contém a base de conhecimento completa, arquitetural, científica e operacional para o desenvolvimento, execução experimental e redação do artigo científico da 1ª Avaliação Prática.

Toda inteligência artificial ou desenvolvedor que for atuar neste repositório **DEVE** consultar os módulos abaixo para garantir aderência aos requisitos e evitar a eliminação do trabalho.

| Subpasta / Arquivo do Cérebro | Finalidade e Conteúdo |
| :--- | :--- |
| 📖 [**`brain/README.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/README.md) | Mapa visual e índice completo de todas as subpastas e documentos. |
| 📋 [**`brain/01_diretrizes/visao_geral_e_regras.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/01_diretrizes/visao_geral_e_regras.md) | Visão executiva, escopo, regras eliminatórias críticas (nota 0,0) e critérios de avaliação. |
| ✅ [**`brain/01_diretrizes/checklist_progresso.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/01_diretrizes/checklist_progresso.md) | Quadro de tarefas, status de cada componente e validação pré-submissão. |
| 🏗️ [**`brain/02_arquitetura/arquitetura_e_docker.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/02_arquitetura/arquitetura_e_docker.md) | Topologia de rede em contêineres, especificação do `docker-compose.yml`, NGINX com HTTP/3 + TLS 1.3, cliente com curl HTTP/3, iperf3 e tshark. |
| 🧪 [**`brain/03_experimentos/cenarios_de_teste.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/03_experimentos/cenarios_de_teste.md) | Especificação detalhada dos Cenários A (UDP Puro), B (TCP Massivo) e C (QUIC / Concorrência sob Perdas), comandos `tc/netem` e cargas. |
| 📊 [**`brain/03_experimentos/metricas_e_analise_dados.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/03_experimentos/metricas_e_analise_dados.md) | Definição matemática de FCT, Goodput, Protocol Overhead via tshark/Wireshark, rigor estatístico (10 repetições, desvio padrão, IC 95%) e pipeline Python. |
| 📄 [**`brain/04_entregaveis/artigo_sbc_sbrc.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/04_entregaveis/artigo_sbc_sbrc.md) | Guia de redação no padrão SBC/SBRC (LaTeX), estrutura obrigatória das seções, fundamentação teórica e RFCs mandatórias (793, 768, 9000, 9001, 8446). |
| 🎥 [**`brain/04_entregaveis/roteiro_video_15min.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/04_entregaveis/roteiro_video_15min.md) | Roteiro passo a passo com cronometria exata para o vídeo de 15 minutos (apresentação, código, demo ao vivo e gráficos). |
| 🤖 [**`brain/05_prompts_ia/guia_de_prompts_ia.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/05_prompts_ia/guia_de_prompts_ia.md) | Prompts modulares prontos para delegar implementações técnicas (Docker, Shell, Python, LaTeX, Análise Wireshark) para IAs subsequentes. |

---

## 🚨 REGRA ELIMINATÓRIA CRÍTICA (NÃO ESQUECER!)

> [!CAUTION]
> **CRITÉRIO EXCLUDENTE DA AVALIAÇÃO:**
> A entrega exige estritamente:
> 1. O **relatório técnico em PDF** formatado rigorosamente no padrão SBC/SBRC.
> 2. O **link público e funcional** para o vídeo gravado de **exatamente 15 minutos** hospedado no YouTube (Não listado/Público) ou Google Drive (Acesso aberto), localizado **obrigatoriamente na 1ª página do relatório** (abaixo do resumo ou na nota de rodapé dos autores).
>
> **A ausência do PDF ou a ausência/inoperância do link de vídeo resulta em NOTA ZERO (0,0) IMEDIATA sem recurso.**

---

## 📁 Estrutura de Diretórios Recomendada para o Projeto

```text
Avaliacao_1/
├── 1_Avaliacao - Redes 2.pdf       # Enunciado original da avaliação
├── README.md                       # Este arquivo (Dashboard e Índice Central)
├── brain/                          # Cérebro do projeto subdividido em módulos
│   ├── README.md                   # Mapa do cérebro
│   ├── 01_diretrizes/
│   │   ├── visao_geral_e_regras.md
│   │   └── checklist_progresso.md
│   ├── 02_arquitetura/
│   │   └── arquitetura_e_docker.md
│   ├── 03_experimentos/
│   │   ├── cenarios_de_teste.md
│   │   └── metricas_e_analise_dados.md
│   ├── 04_entregaveis/
│   │   ├── artigo_sbc_sbrc.md
│   │   └── roteiro_video_15min.md
│   └── 05_prompts_ia/
│       └── guia_de_prompts_ia.md
├── docker/                         # Configurações de infraestrutura Docker
│   ├── docker-compose.yml
│   ├── server/
│   │   ├── Dockerfile
│   │   ├── nginx.conf
│   │   └── certs/
│   └── client/
│       ├── Dockerfile
│       └── requirements.txt
├── scripts/                        # Scripts de automação e emulação
│   ├── run_experiments.sh          # Orquestrador mestre (1-click run)
│   ├── setup_netem.sh              # Aplicação de latência/perda via tc
│   ├── test_scenario_a.sh          # Testes do Cenário A (UDP Puro)
│   ├── test_scenario_b.sh          # Testes do Cenário B (TCP Massivo)
│   ├── test_scenario_c.sh          # Testes do Cenário C (QUIC Concorrência)
│   └── process_pcaps.sh            # Extração de métricas com tshark
├── analysis/                       # Análise estatística e geração de gráficos
│   ├── parse_logs.py
│   ├── generate_plots.py
│   └── output/                     # Gráficos .png e tabelas .csv
├── data/                           # Ficheiros de dados gerados
│   ├── raw_logs/
│   ├── pcaps/
│   └── processed_data/
├── paper/                          # Artigo Científico em LaTeX (Padrão SBC)
│   ├── sbc-template.tex
│   ├── sbc.sty
│   ├── referencias.bib
│   └── figures/
└── video/                          # Materiais de suporte ao vídeo de 15min
    ├── slide_deck/
    └── roteiro_gravacao.md
```
