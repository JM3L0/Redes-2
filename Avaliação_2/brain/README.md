# 🧠 Mapa de Navegação do Cérebro — 2ª Avaliação

Este diretório centraliza todo o conhecimento técnico, arquitetural, científico e operacional da **2ª Avaliação Prática de Redes de Computadores II (UFPI - 2026-2)**:
*Estudo Experimental de Desempenho de Protocolos Web (HTTP/1.1 vs HTTPS/TLS vs HTTP/3-QUIC) em Ambiente Emulado com Docker e Python*.

- **Aluno:** João Marcos Sousa Rufino Leal
- **E-mail:** `jsousarufinoleal@ufpi.edu.br`
- **Curso:** Bacharelado em Sistemas de Informação
- **Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)
- **Peso:** 50% da nota da 2ª Avaliação (N2) — 100 pontos totais

---

## 🗺️ Estrutura Temática do Cérebro

```text
brain/
├── README.md                                  # Este mapa de navegação
│
├── 01_diretrizes/                             # Regras, escopo, rubricas e checklist
│   ├── visao_geral_e_regras.md                # Fundamentação, 3 fenômenos, rubrica 100pts, penalidades e Nota Zero
│   ├── checklist_progresso.md                 # Quadro kanban com as 8 fases do projeto e validação pré-submissão
│   └── auditoria_cerebro.md                   # Relatório formal da auditoria independente (100% de conformidade)
│
├── 02_arquitetura/                            # Infraestrutura e redes
│   └── arquitetura_e_docker.md                # Docker Compose, net_bench, NGINX HTTP/1.1, NGINX HTTPS TLS 1.3, Caddy HTTP/3, certs e tc netem
│
├── 03_experimentos/                           # Especificações práticas e dados
│   ├── cenarios_de_teste.md                   # Cenário 1 (LAN 1ms, 0%), Cenário 2 (WAN 50ms, 2%), Cargas A (50MB) e B (100x10KB), Matriz T01 a T12
│   └── metricas_e_analise_dados.md            # Fórmulas de TTFB, Load Time, RPS, p50/p99, bias control, rigor estatístico (IC 95%) e gráficos com barras de erro
│
├── 04_entregaveis/                            # Materiais de avaliação final
│   ├── relatorio_tecnico_academico.md         # Estrutura do artigo LaTeX SBC, citação de Tanenbaum §6.5.11 (CUBIC) e §6.6.1/§6.6.2 (QUIC/BBR), link do vídeo
│   └── roteiro_video_15min.md                 # Roteiro cronometrado minuto a minuto (00:00 a 15:00) para apresentação e demo ao vivo
│
├── 05_prompts_ia/                             # Aceleração e automação com IAs
│   └── guia_de_prompts_ia.md                  # Prompts prontos para delegar tarefas a agentes de IA em Docker, Shell, Python e LaTeX
│
└── 06_relatorios_de_fases/                    # Diário de bordo detalhado fase a fase
    ├── README.md                              # Índice das fases registradas
    ├── fase_01_analise_e_estruturacao.md      # Relatório da Fase 1 (Cérebro do Projeto)
    ├── fase_02_e_03_infra_e_cargas.md         # Relatório das Fases 2 e 3 (Docker, Certificados e Cargas)
    ├── fase_04_e_05_cliente_e_runner.md       # Relatório das Fases 4 e 5 (Cliente Python e Runner 1-Click)
    ├── fase_06_e_07_analise_e_relatorio.md    # Relatório das Fases 6 e 7 (Estatística, Plots e Artigo SBC)
    └── fase_08_video_e_submissao.md           # Relatório da Fase 8 (Slides, Roteiro do Vídeo e Submissão)
```

---

## 🔗 Links Rápidos para os Documentos

### 📌 1. Diretrizes & Planejamento
- [**`01_diretrizes/visao_geral_e_regras.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/01_diretrizes/visao_geral_e_regras.md): Leia primeiro para entender o problema, os 3 fenômenos investigados, os critérios eliminatórios (Nota Zero) e a tabela de penalidades.
- [**`01_diretrizes/checklist_progresso.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/01_diretrizes/checklist_progresso.md): Acompanhe o status e tarefas das 8 fases do projeto.
- [**`01_diretrizes/auditoria_cerebro.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/01_diretrizes/auditoria_cerebro.md): Parecer formal da auditoria técnica com verificação de 100% de conformidade.

### 🏗️ 2. Arquitetura & Docker
- [**`02_arquitetura/arquitetura_e_docker.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/02_arquitetura/arquitetura_e_docker.md): Topologia de contêineres na rede `net_bench` (172.20.0.0/16), configuração dos 3 servidores (Nginx e Caddy), certificados TLS 1.3 locais e permissão `cap_add: NET_ADMIN`.

### 🧪 3. Experimentos & Métricas
- [**`03_experimentos/cenarios_de_teste.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/03_experimentos/cenarios_de_teste.md): Configurações de canal (`tc/netem`), cargas estáticas (50 MB e 100x10 KB) e detalhamento exaustivo dos 12 testes (T01 a T12).
- [**`03_experimentos/metricas_e_analise_dados.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/03_experimentos/metricas_e_analise_dados.md): Definições de TTFB, RPS, Load Time, p50/p99, controle de vício de sessão (Cold TTFB vs Warm) e obrigatoriedade de barras de erro.

### 📄 4. Entregáveis Oficiais
- [**`04_entregaveis/relatorio_tecnico_academico.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/04_entregaveis/relatorio_tecnico_academico.md): Guia de redação no padrão SBC, modelo de citação obrigatória de Tanenbaum §6.5.11 (CUBIC) e §6.6.1/§6.6.2 (QUIC/BBR), e posicionamento do link do vídeo na 1ª página.
- [**`04_entregaveis/roteiro_video_15min.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/04_entregaveis/roteiro_video_15min.md): Divisão cronometrada de 15 minutos para apresentação, código, demonstração ao vivo e discussão dos gráficos.

### 🤖 5. Prompts para IAs
- [**`05_prompts_ia/guia_de_prompts_ia.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/05_prompts_ia/guia_de_prompts_ia.md): Prompts modulares de alta precisão para orquestrar e acelerar o desenvolvimento com agentes de IA.

### 📑 6. Relatórios de Execução por Fase (Diário de Bordo)
- [**`06_relatorios_de_fases/README.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/06_relatorios_de_fases/README.md): Índice consolidado do diário de bordo.
- [**`06_relatorios_de_fases/fase_01_analise_e_estruturacao.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/06_relatorios_de_fases/fase_01_analise_e_estruturacao.md): Relatório da Fase 1 (Cérebro do Projeto).
- [**`06_relatorios_de_fases/fase_02_e_03_infra_e_cargas.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/06_relatorios_de_fases/fase_02_e_03_infra_e_cargas.md): Relatório das Fases 2 e 3 (Docker, Certificados e Cargas).
- [**`06_relatorios_de_fases/fase_04_e_05_cliente_e_runner.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/06_relatorios_de_fases/fase_04_e_05_cliente_e_runner.md): Relatório das Fases 4 e 5 (Cliente Python e Runner 1-Click).
- [**`06_relatorios_de_fases/fase_06_e_07_analise_e_relatorio.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/06_relatorios_de_fases/fase_06_e_07_analise_e_relatorio.md): Relatório das Fases 6 e 7 (Estatística, Plots e Artigo SBC).
- [**`06_relatorios_de_fases/fase_08_video_e_submissao.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/06_relatorios_de_fases/fase_08_video_e_submissao.md): Relatório da Fase 8 (Slides, Roteiro e Preparação da Submissão).
