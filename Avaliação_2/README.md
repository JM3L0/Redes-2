# Avaliação 2 — Estudo Experimental de Desempenho de Protocolos Web
## HTTP/1.1 vs HTTPS/TLS 1.3 vs HTTP/3-QUIC em Ambiente Emulado com Docker e Python

**Universidade Federal do Piauí (UFPI)** — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Curso:** Bacharelado em Sistemas de Informação  
**Disciplina:** Redes de Computadores II (2026-2)  
**Aluno:** João Marcos Sousa Rufino Leal  
**E-mail:** `jsousarufinoleal@ufpi.edu.br`  
**Peso da Avaliação:** 50% da pontuação total da N2 (100 pontos totais)

---

## 🧭 Visão Geral do Projeto

Este repositório contém a implementação completa, reprodutível e automatizada do estudo experimental de desempenho dos protocolos da Web moderna sob condições controladas de canal físico de rede:
- **HTTP/1.1 em texto claro sobre TCP** (NGINX Alpine, porta 80/8081);
- **HTTPS / HTTP/2 com criptografia TLS 1.3** (NGINX Alpine, porta 443/8443);
- **HTTP/3 nativo sobre QUIC/UDP** (Caddy 2.7 Alpine, portas 443 TCP/UDP / 9443).

O projeto investiga empiricamente três fenômenos fundamentais da engenharia de redes:
1. **Overhead de Handshake e Latência Inicial:** 1 RTT (TCP) vs 2 RTTs (TCP + TLS 1.3) vs 1 RTT integrado (QUIC) no *Time to First Byte* (TTFB);
2. **Bloqueio de Início de Linha (*Head-of-Line Blocking*):** HoL na camada de aplicação (HTTP/1.1), HoL na camada de transporte (HTTP/2 sobre TCP) e eliminação completa nas duas camadas via fluxos (*streams*) UDP independentes (HTTP/3);
3. **Controle de Congestionamento sob Perdas:** Colapso de vazão do TCP CUBIC sob 2% de perda estocástica e 50ms de RTT (**Tanenbaum §6.5.11**) versus a resiliência e ritmo (*pacing*) do QUIC/BBR (**Tanenbaum §6.6.1 e §6.6.2**).

---

## ⚡ Execução Automatizada em 1 Comando (1-Click Run)

Conforme exigido pelo edital (mitigando a penalidade de -15 pontos), o experimento inteiro é executado de ponta a ponta com um único comando:

### No Windows (PowerShell):
```powershell
.\run_experiments.ps1
```
*Para execução rápida de validação com 2 repetições:*
```powershell
.\run_experiments.ps1 -Quick
```

### No Linux, macOS ou WSL 2 (Bash):
```bash
chmod +x run_experiments.sh
./run_experiments.sh
```
*Para execução rápida de validação com 2 repetições:*
```bash
./run_experiments.sh --quick
```

### O que o Orquestrador Mestre executa automaticamente:
1. Gera certificados digitais TLS 1.3 com SANs válidos (`scripts/generate_certs.py`);
2. Cria deterministicamente os payloads sintéticos de 50 MB e 100x10 KB (`scripts/generate_payloads.py`);
3. Sobe os 3 contêineres Docker na rede isolada `net_bench` com `cap_add: [NET_ADMIN]`;
4. Configura o **Cenário 1 (LAN: delay 0.5ms = RTT 1.0ms, perda 0%)** e executa T01 a T03 (50 MB) e T07 a T09 (100 objetos);
5. Configura o **Cenário 2 (WAN: delay 25ms = RTT 50.0ms, perda 2%)** e executa T04 a T06 (50 MB) e T10 a T12 (100 objetos);
6. Restaura as interfaces virtuais limpando as disciplinas `tc netem`;
7. Processa os dados estatísticos gerando médias, p50, p99 e intervalos de confiança de 95% (`analysis/process_data.py`);
8. Gera as **5 figuras científicas com barras de erro obrigatórias** (`analysis/plot_results.py`);
9. Encerra limpa e ordenadamente os contêineres Docker.

---

## 📂 Estrutura do Repositório

```
Avaliação_2/
├── run_experiments.ps1       # Orquestrador mestre 1-click para Windows PowerShell
├── run_experiments.sh        # Orquestrador mestre 1-click para Linux/WSL/macOS
├── AGENTS.md                 # Diretrizes e regras do projeto para agentes de IA
├── README.md                 # Este manual técnico completo
│
├── docker/                   # Infraestrutura de contêineres
│   ├── docker-compose.yml    # Topologia dos 3 servidores Web com cap_add: [NET_ADMIN]
│   ├── server-http1/         # NGINX Alpine servindo HTTP/1.1 (texto claro)
│   ├── server-http2/         # NGINX Alpine servindo HTTPS / HTTP/2 com TLS 1.3
│   ├── server-http3/         # Caddy 2.7 Alpine servindo HTTP/3 nativo (QUIC/UDP)
│   └── certs/                # Certificados TLS 1.3 com Subject Alternative Names (SANs)
│
├── benchmark/                # Cliente assíncrono de medição em Python
│   ├── client.py             # Cliente assíncrono com httpx e aioquic
│   ├── session_control.py    # Controle de viés de sessão (Cold TTFB vs Warm Concurrency)
│   └── metrics.py            # Coleta de alta precisão (microssegundos) e cálculo de IC 95%
│
├── scripts/                  # Automações de apoio
│   ├── generate_certs.py     # Gerador de certificados TLS 1.3 locais com SANs via cryptography
│   ├── generate_payloads.py  # Gerador determinístico dos arquivos de 50 MB e 100x10 KB
│   ├── setup_netem.ps1       # Aplicação e limpeza das regras tc netem (PowerShell)
│   └── setup_netem.sh        # Aplicação e limpeza das regras tc netem (Bash)
│
├── analysis/                 # Tratamento estatístico e visualização científica
│   ├── process_data.py       # Sumarização com médias, p50, p99, desvio padrão e IC 95%
│   └── plot_results.py       # Gráficos a 300 DPI com BARRAS DE ERRO OBRIGATÓRIAS
│
├── data/                     # Dados brutos, processados e figuras
│   ├── static/               # Carga A (50MB.bin) e Carga B (objects/obj_001.bin a obj_100.bin)
│   ├── raw/                  # results.json e results.csv gerados durante os ensaios
│   ├── processed/            # summary_table.csv e summary_table.tex consolidados
│   └── plots/                # Figuras 1 a 5 salvas em alta resolução (300 DPI)
│
├── relatorio/                # Artigo acadêmico formal em padrão SBC/LaTeX
│   ├── sbc-template.tex      # Código-fonte LaTeX com fundamentação Tanenbaum (§6.5.11 e §6.6.1/2)
│   ├── sbc-template.pdf      # Relatório final compilado em PDF com link do vídeo na 1ª página
│   ├── sbc.sty               # Estilo oficial da Sociedade Brasileira de Computação
│   └── relatorio.bib         # Referências formais (Tanenbaum, RFCs IETF)
│
├── video/                    # Slides e roteiro do vídeo de apresentação (15 minutos)
│   ├── slides.html           # Apresentação interativa em HTML/CSS para gravação em tela
│   └── README.md             # Roteiro cronometrado e checklist pré-gravação
│
└── brain/                    # Cérebro do projeto (documentação arquitetural e auditorias)
    ├── 01_diretrizes/        # Regras, rubrica e checklist kanban
    ├── 02_arquitetura/       # Modelagem de contêineres e topologia
    ├── 03_experimentos/      # Matriz de 12 testes e modelagem de métricas
    ├── 04_entregaveis/       # Especificação do artigo SBC e roteiro do vídeo
    ├── 05_prompts_ia/        # Guia de prompts especializados
    └── 06_relatorios_de_fases/# Diário de bordo detalhado de cada fase concluída
```

---

## 🎯 Conformidade com o Edital e Mitigação de Penalidades

| Requisito do Edital | Penalidade Evitada | Implementação no Projeto |
| :--- | :---: | :--- |
| **Runner de Comando Único** | **-15 Pontos** | Scripts `run_experiments.ps1` e `run_experiments.sh` automatizam 100% do ciclo de vida. |
| **Controle de Viés de Sessão** | **-10 Pontos** | `benchmark/session_control.py` força destruição de sessão (`client.aclose()`) no TTFB e mantém conexão persistente na Carga B. |
| **Barras de Erro nos Gráficos** | **-10 Pontos** | Todos os 5 gráficos em `data/plots/` exibem barras de erro ($IC_{95\%}$ ou $\sigma$) com `capsize=5`. |
| **Fundamentação em Tanenbaum** | **-20 Pontos** | Discussão detalhada articulando Tanenbaum §6.5.11 ($W_{\text{cubic}}$ e retração multiplicativa) e §6.6.1/§6.6.2 (QUIC/BBR). |
| **Código + PDF + Link do Vídeo** | **NOTA ZERO (0,0)** | Código completo e funcional, PDF compilado com link público do YouTube posicionado na página 1. |

---

## 📊 Matriz Experimental dos 12 Testes Realizados

| ID | Perfil de Carga | Protocolo Alvo | Servidor Docker | Cenário de Rede | Foco Analítico Principal |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **T01** | Carga A (50 MB) | HTTP/1.1 | `server_http11` (8081) | LAN (1ms, 0%) | Vazão máxima TCP em canal ideal sem sobrecarga criptográfica |
| **T02** | Carga A (50 MB) | HTTPS / TLS 1.3 | `server_http2_tls` (8443) | LAN (1ms, 0%) | Sobrecarga de cifragem simétrica do TLS 1.3 sobre TCP |
| **T03** | Carga A (50 MB) | HTTP/3 (QUIC) | `server_http3_quic` (9443) | LAN (1ms, 0%) | Eficiência do protocolo QUIC em espaço de usuário sem perdas |
| **T04** | Carga A (50 MB) | HTTP/1.1 | `server_http11` (8081) | WAN (50ms, 2%) | Colapso de vazão do TCP CUBIC sob descarte estocástico contínuo |
| **T05** | Carga A (50 MB) | HTTPS / TLS 1.3 | `server_http2_tls` (8443) | WAN (50ms, 2%) | Degradação cumulativa da janela do TCP CUBIC somada ao TLS |
| **T06** | Carga A (50 MB) | HTTP/3 (QUIC) | `server_http3_quic` (9443) | WAN (50ms, 2%) | Resiliência do controle de congestionamento do QUIC sob perda |
| **T07** | Carga B (100x10K) | HTTP/1.1 | `server_http11` (8081) | LAN (1ms, 0%) | Overhead de conexões paralelas e HoL na Camada de Aplicação |
| **T08** | Carga B (100x10K) | HTTPS / TLS 1.3 | `server_http2_tls` (8443) | LAN (1ms, 0%) | Eficiência da multiplexação por quadros do HTTP/2 em baixa latência |
| **T09** | Carga B (100x10K) | HTTP/3 (QUIC) | `server_http3_quic` (9443) | LAN (1ms, 0%) | Desempenho de fluxos concorrentes QUIC em canal de alta velocidade |
| **T10** | Carga B (100x10K) | HTTP/1.1 | `server_http11` (8081) | WAN (50ms, 2%) | Severidade do HoL blocking de aplicação sob latência e perdas |
| **T11** | Carga B (100x10K) | HTTPS / TLS 1.3 | `server_http2_tls` (8443) | WAN (50ms, 2%) | Severidade do HoL blocking na Camada de Transporte TCP |
| **T12** | Carga B (100x10K) | HTTP/3 (QUIC) | `server_http3_quic` (9443) | WAN (50ms, 2%) | Eliminação total do HoL blocking através de streams UDP independentes |

---

## 🖥️ Como Visualizar os Slides de Apresentação

Abra o arquivo `video/slides.html` diretamente em qualquer navegador Web (Chrome, Edge ou Firefox).  
Utilize as setas do teclado (`◀` e `▶`) ou a barra de espaço para navegar pelos 10 slides durante a gravação do vídeo de 15 minutos.

---

## 📦 Instruções de Empacotamento Final para Submissão no SIGAA

Para gerar o arquivo compactado final no formato padronizado pelo edital:

```powershell
Compress-Archive -Path "docker", "benchmark", "scripts", "analysis", "data", "relatorio", "video", "brain", "run_experiments.ps1", "run_experiments.sh", "README.md", "AGENTS.md" -DestinationPath "TP2_Redes2_JoaoMarcosSousaRufinoLeal.zip" -Force
```
