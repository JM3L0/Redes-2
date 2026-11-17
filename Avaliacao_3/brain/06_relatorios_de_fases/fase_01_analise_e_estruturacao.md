# Relatório de Execução — Fase 1: Análise Minuciosa do Edital e Estruturação do Cérebro (N3)

**Data:** 17 de Novembro de 2026  
**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)  
**Status da Fase:** ✅ CONCLUÍDA COM SUCESSO

---

## 1. Contexto e Objetivos da Fase

A Fase 1 teve como objetivo o exame exaustivo e rigoroso do edital oficial da **Terceira Avaliação (N3)** (`Terceira Avaliacao.pdf`), valendo **100 pontos totais**, e a construção completa do **Cérebro do Projeto (`brain/`)** seguindo a mesma excelência metodológica empregada na 1ª e na 2ª Avaliações.

---

## 2. Levantamento Detalhado dos Requisitos do Edital N3

A partir da análise completa das 9 páginas de `Terceira Avaliacao.pdf`, foram mapeados todos os requisitos técnicos, científicos e formais:

1. **Dois Mecanismos Avançados da Camada de Transporte Moderna:**
   - **Bloco A — Controle de Congestionamento Baseado em Perda vs. Baseado em Modelo (TCP CUBIC vs. TCP BBR):** Fluxos contínuos de 15 segundos via `iperf3` (`-C cubic` vs. `-C bbr`) avaliando a vazão (Mbps) e o número de retransmissões sob LAN ideal (E01) e WAN degradada com 50 ms de RTT e 2% de perda estocástica (E02 e E03).
   - **Bloco B — Estabelecimento Rápido de Conexão e Session Resumption no QUIC (1-RTT vs. 0-RTT):** Transferência de um objeto pequeno de **1 KB** via `curl` (`%{time_starttransfer}`) sob WAN sem perda (50 ms de RTT, 0% de perda — Cenário 3), isolando o custo de handshakes entre HTTPS/HTTP/2 sobre TCP+TLS (E04), HTTP/3 Cold 1-RTT (E05) e HTTP/3 Warm/Resumption 0-RTT (E06).
2. **Arquitetura Simplificada no Docker (`docker-compose.yml`):**
   - Sub-rede bridge `net_bench` (`172.20.0.0/16`) com `cap_add: - NET_ADMIN` obrigatório em todos os contêineres:
     - `server_tcp_cc` (`networkstatic/iperf3 -s`, IP `172.20.0.10`);
     - `server_http3_quic` (`caddy:2.7-alpine`, IP `172.20.0.30`);
     - `client_bench` (IP `172.20.0.50`, com `curl` suportando `--http3` e `iperf3`).
3. **Três Cenários `tc netem` + Limpeza:**
   - Cenário 1 (LAN): `delay 0.5ms` (RTT = 1 ms, 0% perda);
   - Cenário 2 (WAN Degradada): `delay 25ms loss 2%` (RTT = 50 ms, 2% perda);
   - Cenário 3 (WAN sem Perda): `delay 25ms` (RTT = 50 ms, 0% perda);
   - Limpeza: `tc qdisc del dev eth0 root`.
4. **Rigor Estatístico e Entregáveis:**
   - Mínimo de **5 repetições por teste** ($N \ge 5$) para os 6 testes essenciais (E01 a E06);
   - Exportação de dados brutos (CSV/JSON) e geração programática de **2 gráficos comparativos com barras de erro (desvio padrão)**;
   - **Relatório Técnico Conciso em PDF (mínimo 4, máximo 6 páginas)** no formato de artigo da **SBRC**, contendo a Tabela Resumo e a Discussão Teórica fundamentada em **Tanenbaum 6ª Edição (Seções 6.5.11, 6.6.1 e 6.6.2)**;
   - **Vídeo no YouTube (entre 15 e 25 minutos)** explicando o projeto e os resultados, com link inserido no relatório.

---

## 3. Mapeamento da Rubrica (100 Pontos) e Blindagem contra Penalidades

| Eixo / Regra do Edital | Pontuação / Penalidade | Blindagem Estruturada no Cérebro |
| :--- | :---: | :--- |
| **Eixo 1: Infraestrutura Docker e Automação `tc netem`** | **10 Pontos** | Especificação completa em `02_arquitetura/arquitetura_e_docker.md` e automação via `run_n3.py` / `run_n3.sh`. |
| **Eixo 2: Coleta Estatística e Visualização Gráfica** | **10 Pontos** | Protocolo de $N \ge 5$ amostras, exportação CSV/JSON e especificação dos Gráficos 1 e 2 em `03_experimentos/metricas_e_analise_dados.md`. |
| **Eixo 3: Relatório Técnico e Articulação Teórica (SBRC)** | **50 Pontos** | Estrutura de 4 a 6 páginas e deduções de Tanenbaum 6ª Ed. detalhadas em `04_entregaveis/relatorio_tecnico_academico.md`. |
| **Eixo 4: Vídeo no YouTube (15 a 25 minutos)** | **30 Pontos** | Roteiro cronometrado de 18 minutos em `04_entregaveis/roteiro_video_15_a_25min.md` e `brain/video/`. |
| **Penalidade: Ausência de barras de erro nos gráficos** | **-10 Pontos** | Obrigatoriedade de `yerr=std` (desvio padrão) com `capsize=6` nos Gráficos 1 e 2. |
| **Penalidade: Relatório puramente descritivo** | **-20 Pontos** | Fundamentação teórica obrigatória nas Seções 6.5.11 (CUBIC), 6.6.2 (BBR) e 6.6.1 (QUIC) de Tanenbaum (6ª Ed.). |
| **Penalidade: Sem vídeo, sem PDF ou sem arquivos-fonte / Plágio** | **NOTA 0,0** | Checklist de verificação pré-submissão para o pacote `TP3_Redes2_JoaoMarcosSousaRufinoLeal.zip`. |

---

## 4. Artefatos Criados na Fase 1

1. [`AGENTS.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/AGENTS.md)
2. [`README.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/README.md)
3. [`brain/README.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/README.md)
4. [`brain/01_diretrizes/visao_geral_e_regras.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/01_diretrizes/visao_geral_e_regras.md)
5. [`brain/01_diretrizes/checklist_progresso.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/01_diretrizes/checklist_progresso.md)
6. [`brain/01_diretrizes/auditoria_cerebro.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/01_diretrizes/auditoria_cerebro.md)
7. [`brain/02_arquitetura/arquitetura_e_docker.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/02_arquitetura/arquitetura_e_docker.md)
8. [`brain/03_experimentos/cenarios_de_teste.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/03_experimentos/cenarios_de_teste.md)
9. [`brain/03_experimentos/metricas_e_analise_dados.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/03_experimentos/metricas_e_analise_dados.md)
10. [`brain/04_entregaveis/relatorio_tecnico_academico.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/04_entregaveis/relatorio_tecnico_academico.md)
11. [`brain/04_entregaveis/roteiro_video_15_a_25min.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/04_entregaveis/roteiro_video_15_a_25min.md)
12. [`brain/05_prompts_ia/guia_de_prompts_ia.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/05_prompts_ia/guia_de_prompts_ia.md)
13. [`brain/06_relatorios_de_fases/README.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/06_relatorios_de_fases/README.md)
14. [`brain/06_relatorios_de_fases/fase_01_analise_e_estruturacao.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/06_relatorios_de_fases/fase_01_analise_e_estruturacao.md)
15. [`brain/video/README.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/video/README.md), [`brain/video/roteiro_video_15_a_25min.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/video/roteiro_video_15_a_25min.md) e [`brain/video/CHECKLIST_GRAVACAO.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_3/brain/video/CHECKLIST_GRAVACAO.md)
