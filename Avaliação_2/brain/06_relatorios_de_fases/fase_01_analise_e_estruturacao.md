# Relatório de Execução — Fase 1: Análise Minuciosa do Edital e Estruturação do Cérebro

**Data:** 21 de Outubro de 2026  
**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)  
**Status da Fase:** ✅ CONCLUÍDA COM SUCESSO

---

## 1. Contexto e Objetivos da Fase

A Fase 1 teve como meta o exame exaustivo e rigoroso do documento oficial de especificação do Trabalho Prático da 2ª Avaliação (`Segunda Avaliação Redes 2.pdf`), com peso de **50% da pontuação total da N2 (100 pontos totais)**. 

A finalidade primordial foi conceber e estruturar a arquitetura de informação do projeto — o chamado **Cérebro do Projeto (`brain/`)** —, estabelecendo diretrizes técnicas, modelagem arquitetural de contêineres, definição da matriz experimental de 12 testes, equacionamento estatístico das métricas, checklist kanban e planejamento detalhado para evitar penalidades e a atribuição de nota zero.

---

## 2. Levantamento Detalhado dos Requisitos e Fenômenos Investigados

Do estudo do edital foram extraídos os pilares conceituais do trabalho:

1. **Overhead de Handshake e Latência Inicial (Cold TTFB):**
   - *HTTP/1.1:* 1 RTT para o handshake TCP de 3 vias.
   - *HTTPS (HTTP/2):* 2 RTTs cumulativos (1 RTT TCP + 1 RTT TLS 1.3).
   - *HTTP/3-QUIC:* 1 RTT conjunto sobre UDP com TLS 1.3 integrado (ou 0-RTT com resumption).
2. **Bloqueio de Início de Linha (Head-of-Line Blocking):**
   - *HTTP/1.1:* HoL na aplicação (respostas sequenciais sobre o canal TCP).
   - *HTTP/2:* HoL no transporte TCP (a perda de 1 segmento congela todo o buffer de fluxos multiplexados).
   - *HTTP/3:* HoL totalmente eliminado em ambas as camadas (streams UDP independentes).
3. **Efeito das Condições de Canal:**
   - *Cenário 1 (LAN):* 0.5ms delay (RTT = 1ms), 0% perda — canal ideal.
   - *Cenário 2 (WAN):* 25ms delay (RTT = 50ms), 2% perda estocástica — canal móvel/longa distância degradado.
   - Demonstração do colapso do TCP CUBIC sob 2% de perda versus a resiliência do QUIC/BBR.

---

## 3. Mapeamento das Penalidades e Critérios Críticos de Avaliação

Foi realizado o mapeamento das penalidades diretas para garantir conformidade estrita durante as fases de implementação:

| Penalidade Prevista | Sanção | Medida Adotada no Cérebro |
| :--- | :---: | :--- |
| Ausência de execução automatizada 1-click (`run_experiments.sh`) | **-15 Pontos** | Especificação e planejamento de `run_experiments.sh` e `run_experiments.ps1`. |
| Falta de controle de viés de sessão no cliente Python | **-10 Pontos** | Modelagem de modos estritos: fechamento explícito de sessão (`client.close()`) para Cold TTFB vs canal persistente para Carga B. |
| Ausência de barras de erro nos gráficos | **-10 Pontos** | Regra mandatória no pipeline Python de plotar barras de erro com desvio padrão ou IC 95% ($t=2.262, N=10$). |
| Relatório descritivo sem fundamentação em Tanenbaum | **-20 Pontos** | Diretriz com modelos matemáticos de Tanenbaum §6.5.11 (TCP CUBIC) e §6.6.1/§6.6.2 (QUIC/BBR). |
| Falta de código, relatório ou vídeo de 15 minutos com link na 1ª página | **NOTA ZERO (0,0)** | Inclusão de checklist de validação pré-submissão e posicionamento mandatório do link no template LaTeX. |

---

## 4. Decisões de Arquitetura de Engenharia Adotadas

1. **Topologia Docker Declarativa:**
   - Rede bridge isolada `net_bench` (172.20.0.0/16).
   - Três servidores Web independentes:
     - `server_http11` (172.20.0.10, Nginx Alpine, porta 8080);
     - `server_http2_tls` (172.20.0.20, Nginx Alpine, porta 8443, TLS 1.3);
     - `server_http3_quic` (172.20.0.30, Caddy 2.7 Alpine, porta 9443 TCP/UDP, HTTP/3 nativo).
   - Diretiva obrigatória `cap_add: [NET_ADMIN]` em todos os nós.
2. **Certificados Criptográficos:**
   - Par OpenSSL autoassinado com Subject Alternative Names (SANs) abrangendo localhost, IPs dos contêineres e nomes de host internos.
3. **Cliente de Benchmark Python:**
   - Utilização assíncrona de `httpx` (HTTP/1.1 e HTTP/2) e `aioquic` (HTTP/3).
   - Temporização monotônica de microssegundos com `time.perf_counter()`.
   - Exportação estruturada para `results.json` e `results.csv`.
4. **Matriz Experimental dos 12 Testes:**
   - Estruturação completa dos testes T01 a T12 com $N \ge 10$ repetições para rigor estatístico.

---

## 5. Artefatos Criados na Fase 1

Todos os documentos foram criados com profundidade e rigor em `c:\Users\jsous\Desktop\Redes 2\Avaliação_2\`:

1. [`AGENTS.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/AGENTS.md): Guia de contexto operacional e regras de conformidade para agentes de IA.
2. [`README.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/README.md): Dashboard principal do projeto com matriz dos 12 testes, resumo de penalidades e árvore de diretórios.
3. [`brain/README.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/README.md): Mapa temático de navegação do cérebro.
4. [`brain/01_diretrizes/visao_geral_e_regras.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/01_diretrizes/visao_geral_e_regras.md): Visão geral, objetivos, 3 fenômenos, tabela comparativa, rubrica e regras de nota zero.
5. [`brain/01_diretrizes/checklist_progresso.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/01_diretrizes/checklist_progresso.md): Quadro kanban com as 8 fases e checklist pré-submissão.
6. [`brain/02_arquitetura/arquitetura_e_docker.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/02_arquitetura/arquitetura_e_docker.md): Topologia de rede, docker-compose, configs de servidores e sintaxe do `tc netem`.
7. [`brain/03_experimentos/cenarios_de_teste.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/03_experimentos/cenarios_de_teste.md): Configurações dos cenários LAN/WAN, Cargas A e B, e detalhamento exaustivo dos testes T01 a T12.
8. [`brain/03_experimentos/metricas_e_analise_dados.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/03_experimentos/metricas_e_analise_dados.md): Fórmulas de TTFB, Goodput, RPS, percentis p50/p99, controle de viés e barras de erro obrigatórias.
9. [`brain/04_entregaveis/relatorio_tecnico_academico.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/04_entregaveis/relatorio_tecnico_academico.md): Modelo acadêmico SBC, link de vídeo na 1ª página e fundamentação teórica obrigatória Tanenbaum §6.5.11 e §6.6.1/§6.6.2.
10. [`brain/04_entregaveis/roteiro_video_15min.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/04_entregaveis/roteiro_video_15min.md): Roteiro minuto a minuto (00:00 a 15:00) com falas prontas e transições.
11. [`brain/05_prompts_ia/guia_de_prompts_ia.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/05_prompts_ia/guia_de_prompts_ia.md): 6 prompts estruturados para orientar o desenvolvimento com IAs nas fases seguintes.
12. [`brain/06_relatorios_de_fases/README.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/06_relatorios_de_fases/README.md): Índice do diário de bordo.
13. [`brain/06_relatorios_de_fases/fase_01_analise_e_estruturacao.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avalia%C3%A7%C3%A3o_2/brain/06_relatorios_de_fases/fase_01_analise_e_estruturacao.md): Este relatório conclusivo da Fase 1.

---

## 6. Próximos Passos (Fase 2)

Com a fundação do Cérebro 100% estabelecida e documentada, o projeto está pronto para a **Fase 2: Construção da Infraestrutura Docker e Configuração dos Servidores Web** (`docker-compose.yml`, configs do NGINX, Caddyfile e certificados TLS).
