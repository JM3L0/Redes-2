# 🧠 Mapa de Navegação do Cérebro

Este diretório centraliza todo o conhecimento técnico, arquitetural, científico e operacional da **1ª Avaliação Prática de Redes de Computadores II (UFPI - 2026-2)**.

- **Aluno:** João Marcos Sousa Rufino Leal
- **E-mail:** `jsousarufinoleal@ufpi.edu.br`
- **Curso:** Bacharelado em Sistemas de Informação
- **Instituição:** Universidade Federal do Piauí (UFPI)

A estrutura foi subdividida em categorias temáticas para facilitar o acesso por desenvolvedores e inteligências artificiais:

```text
brain/
├── README.md                                  # Este mapa de navegação
│
├── 01_diretrizes/                             # Regras, escopo e acompanhamento
│   ├── visao_geral_e_regras.md                # Escopo do trabalho, regras eliminatórias (Nota 0,0)
│   └── checklist_progresso.md                 # Quadro kanban com todas as etapas do projeto
│
├── 02_arquitetura/                            # Infraestrutura e redes
│   └── arquitetura_e_docker.md                # Docker Compose, NGINX HTTP/3, TLS 1.3, tc/netem
│
├── 03_experimentos/                           # Especificações práticas e dados
│   ├── cenarios_de_teste.md                   # Cenários A (UDP), B (TCP) e C (QUIC / Concorrência)
│   └── metricas_e_analise_dados.md            # Fórmulas (FCT, Goodput, Overhead), tshark e estatística
│
├── 04_entregaveis/                            # Materiais de avaliação final
│   ├── artigo_sbc_sbrc.md                     # Estrutura do artigo LaTeX, RFCs mandatórias (793, 768, 9000, 9001, 8446)
│   └── roteiro_video_15min.md                 # Roteiro cronometrado minuto a minuto para o vídeo de 15 minutos
│
└── 05_prompts_ia/                             # Aceleração e automação com IAs
    └── guia_de_prompts_ia.md                  # Prompts prontos para geração de Docker, scripts, Python e LaTeX
```

---

## 🔗 Links Rápidos para os Documentos

### 📌 1. Diretrizes & Planejamento
- [**`01_diretrizes/visao_geral_e_regras.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/01_diretrizes/visao_geral_e_regras.md): Leia primeiro para entender o problema e os critérios de nota zero.
- [**`01_diretrizes/checklist_progresso.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/01_diretrizes/checklist_progresso.md): Acompanhe o status das 8 fases do projeto.

### 🏗️ 2. Arquitetura & Docker
- [**`02_arquitetura/arquitetura_e_docker.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/02_arquitetura/arquitetura_e_docker.md): Detalhes de configuração dos contêineres e parâmetros do Linux.

### 🧪 3. Experimentos & Métricas
- [**`03_experimentos/cenarios_de_teste.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/03_experimentos/cenarios_de_teste.md): Configurações de canal (`tc/netem`), cargas e protocolos.
- [**`03_experimentos/metricas_e_analise_dados.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/03_experimentos/metricas_e_analise_dados.md): Definições de Goodput, FCT, Overhead e rigor estatístico ($N=10$).

### 📄 4. Entregáveis Oficiais
- [**`04_entregaveis/artigo_sbc_sbrc.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/04_entregaveis/artigo_sbc_sbrc.md): Guia de redação científica no formato SBC/SBRC e referências BibTeX.
- [**`04_entregaveis/roteiro_video_15min.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/04_entregaveis/roteiro_video_15min.md): Divisão dos 15 minutos de apresentação e demonstração prática.

### 🤖 5. Prompts para IAs
- [**`05_prompts_ia/guia_de_prompts_ia.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/05_prompts_ia/guia_de_prompts_ia.md): Prompts modulares prontos para orquestrar e acelerar o desenvolvimento.
