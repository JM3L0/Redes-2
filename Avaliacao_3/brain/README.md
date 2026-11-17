# 🧠 Mapa de Navegação do Cérebro — 3ª Avaliação (N3)

Este diretório centraliza todo o conhecimento técnico, arquitetural, científico e operacional da **3ª Avaliação Prática (N3) de Redes de Computadores II (UFPI — 2026-2)**:
*Análise Experimental de Controle de Congestionamento (TCP CUBIC vs. BBR) e Retomada de Sessão (0-RTT) em Redes Degradadas*.

- **Equipe:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`) & Marcos Willian de Sousa e Silva (`marcos.sousa@ufpi.edu.br`)
- **Curso:** Bacharelado em Sistemas de Informação
- **Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)
- **Pontuação:** 100 pontos totais da 3ª Avaliação (N3)

---

## 🗺 Estrutura Temática do Cérebro

```text
brain/
├── README.md                                  # Este mapa de navegação
│
├── 01_diretrizes/                             # Regras, escopo, rubricas, checklist e auditoria
│   ├── visao_geral_e_regras.md                # Fundamentação dos 2 blocos (CUBIC vs BBR e QUIC 1-RTT vs 0-RTT), rubrica 100pts, penalidades e Nota Zero
│   ├── checklist_progresso.md                 # Quadro kanban com as fases do projeto e checklist de blindagem pré-submissão
│   └── auditoria_cerebro.md                   # Relatório formal da auditoria independente do Cérebro (100% de conformidade com o PDF da N3)
│
├── 02_arquitetura/                            # Infraestrutura Docker, serviços e emulação de canal
│   └── arquitetura_e_docker.md                # Topologia net_bench (172.20.0.0/16), server_tcp_cc (iperf3), server_http3_quic (Caddy), client_bench, certs e 3 cenários tc netem
│
├── 03_experimentos/                           # Especificações práticas, matriz E01-E06 e análise estatística
│   ├── cenarios_de_teste.md                   # Cenários 1 (LAN), 2 (WAN 2% perda) e 3 (WAN 0% perda), Bloco A (iperf3 15s) e Bloco B (curl 1KB), Testes E01 a E06
│   └── metricas_e_analise_dados.md            # Fórmulas de Vazão, Retransmissões, TTFB (time_starttransfer), média, desvio padrão (N>=5) e especificação dos 2 Gráficos com Barras de Erro
│
├── 04_entregaveis/                            # Materiais formais de avaliação (Relatório SBRC 50pts + Vídeo 30pts)
│   ├── relatorio_tecnico_academico.md         # Estrutura do artigo SBRC/SBC (4 a 6 páginas), Tabela Resumo, Gráficos 1 e 2 e fundamentação Tanenbaum 6ª Ed. (Seções 6.5.11, 6.6.1 e 6.6.2)
│   └── roteiro_video_15_a_25min.md            # Roteiro cronometrado em dupla (15 a 25 minutos) com demonstração prática e análise teórica
│
├── 05_prompts_ia/                             # Aceleração e orquestração com Agentes de IA
│   └── guia_de_prompts_ia.md                  # 6 prompts cirúrgicos para Docker, Runner (run_n3), Coleta Estatística, Gráficos, Artigo SBRC e Auditoria Final
│
├── 06_relatorios_de_fases/                    # Diário de bordo detalhado fase a fase
│   ├── README.md                              # Índice consolidado das fases registradas
│   └── fase_01_analise_e_estruturacao.md      # Relatório da Fase 1 (Análise do Edital N3 e Construção do Cérebro)
│
└── video/                                     # Kit operacional para gravação do vídeo no OBS Studio
    ├── README.md                              # Instruções rápidas da pasta de vídeo
    ├── roteiro_video_15_a_25min.md            # Roteiro Mestre All-in-One com falas, links clicáveis e comandos de terminal
    └── CHECKLIST_GRAVACAO.md                  # Checklist rápido pré, durante e pós-gravação
```

---

## 🔗 Links Rápidos para os Documentos

### 📌 1. Diretrizes, Regras e Auditoria
- [**`01_diretrizes/visao_geral_e_regras.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/01_diretrizes/visao_geral_e_regras.md): Objetivos pedagógicos, comparação CUBIC vs. BBR e HTTP/2 vs. HTTP/3 (1-RTT e 0-RTT), rubrica de 100 pontos, penalidades (-10 e -20 pts) e critérios de Nota Zero.
- [**`01_diretrizes/checklist_progresso.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/01_diretrizes/checklist_progresso.md): Acompanhamento kanban de todas as fases do projeto e checklist final de empacotamento `.zip`.
- [**`01_diretrizes/auditoria_cerebro.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/01_diretrizes/auditoria_cerebro.md): Parecer formal de auditoria verificando 100% de aderência ao arquivo [`Terceira Avaliacao.pdf`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/Terceira%20Avaliacao.pdf).

### 🏗 2. Arquitetura & Emulação `tc netem`
- [**`02_arquitetura/arquitetura_e_docker.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/02_arquitetura/arquitetura_e_docker.md): Topologia dos contêineres na sub-rede `172.20.0.0/16`, `docker-compose.yml`, requisitos de kernel para TCP BBR, suporte HTTP/3 + Session Resumption no `curl` e Caddy, e comandos exatos de `tc netem`.

### 🧪 3. Matriz Experimental (E01–E06) & Métricas
- [**`03_experimentos/cenarios_de_teste.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/03_experimentos/cenarios_de_teste.md): Detalhamento dos 3 cenários de rede (LAN, WAN com 2% de perda, WAN sem perda) e especificações dos 6 testes essenciais (Bloco A: E01–E03; Bloco B: E04–E06).
- [**`03_experimentos/metricas_e_analise_dados.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/03_experimentos/metricas_e_analise_dados.md): Extração de métricas no `iperf3 -J` e `curl`, equacionamento estatístico ($N \ge 5$, média e desvio padrão) e especificação dos Gráficos 1 e 2 com barras de erro obrigatórias.

### 📄 4. Entregáveis Oficiais (Relatório SBRC + Vídeo)
- [**`04_entregaveis/relatorio_tecnico_academico.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/04_entregaveis/relatorio_tecnico_academico.md): Guia completo para o artigo em padrão SBRC/SBC (4 a 6 páginas), estrutura da Tabela Resumo e fundamentação teórica em Tanenbaum 6ª Edição (Seções 6.5.11, 6.6.1 e 6.6.2).
- [**`04_entregaveis/roteiro_video_15_a_25min.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/04_entregaveis/roteiro_video_15_a_25min.md): Roteiro cronometrado para o vídeo explicativo (15 a 25 minutos, valendo 30 pontos na rubrica).

### 🤖 5. Prompts para IAs
- [**`05_prompts_ia/guia_de_prompts_ia.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/05_prompts_ia/guia_de_prompts_ia.md): Prompts modulares prontos para orientar a construção e validação de cada etapa do projeto.

### 📑 6. Relatórios de Fases (Diário de Bordo)
- [**`06_relatorios_de_fases/README.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/06_relatorios_de_fases/README.md): Índice geral do diário de bordo.
- [**`06_relatorios_de_fases/fase_01_analise_e_estruturacao.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/06_relatorios_de_fases/fase_01_analise_e_estruturacao.md): Relatório detalhado da Fase 1 (Cérebro do Projeto).
