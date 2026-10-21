# ✅ Checklist de Progresso e Validação do Projeto

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Projeto:** Estudo Experimental de Desempenho de Protocolos Web (HTTP/1.1 vs HTTPS/TLS vs HTTP/3-QUIC) em Ambiente Emulado com Docker e Python  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)

---

## 🧭 Quadro Geral de Fases

| Fase | Descrição da Fase | Status |
| :--- | :--- | :---: |
| **Fase 1** | Análise minuciosa do edital e estruturação completa do Cérebro do Projeto | ✅ CONCLUÍDA |
| **Fase 2** | Infraestrutura Docker (Nginx HTTP/1.1, Nginx HTTPS TLS 1.3, Caddy HTTP/3 QUIC) | ✅ CONCLUÍDA |
| **Fase 3** | Geração de Cargas Estáticas (50 MB e 100x10 KB) e Scripts `tc netem` | ✅ CONCLUÍDA |
| **Fase 4** | Desenvolvimento do Cliente de Benchmark Python Assíncrono (`httpx` + `aioquic`) | ✅ CONCLUÍDA |
| **Fase 5** | Automação Runner 1-Click (`run_experiments.sh` / `.ps1`) e Execução dos 12 Testes | ✅ CONCLUÍDA |
| **Fase 6** | Pipeline de Análise Estatística e Visualização com Barras de Erro Obrigatórias | ✅ CONCLUÍDA |
| **Fase 7** | Redação do Relatório Técnico com Fundamentação Tanenbaum (Seção 6.5.11 e Seções 6.6.1 e 6.6.2) | ✅ CONCLUÍDA |
| **Fase 8** | Gravação do Vídeo de 15 Minutos, Auditoria Pré-Submissão e Empacotamento | ⏳ EM ANDAMENTO |

---

## 📋 Itens Detalhados por Fase

### Fase 1: Análise e Estruturação do Cérebro
- [x] Leitura completa e extração textual de `Segunda Avaliação Redes 2.pdf`.
- [x] Mapeamento dos 3 fenômenos: Overhead de Handshake (1 RTT vs 2 RTTs vs 1 RTT), HoL Blocking (aplicação vs transporte vs eliminação em fluxos UDP), e Controle de Congestionamento (CUBIC vs BBR sob 2% de perda).
- [x] Identificação de todas as penalidades (-15pts sem runner 1-click, -10pts sem controle de viés de sessão, -10pts sem barras de erro, -20pts relatório puramente descritivo).
- [x] Identificação do critério eliminatório crítico (falta de código, relatório em PDF ou link do vídeo de 15min = NOTA ZERO 0,0).
- [x] Criação do diretório `brain/` e documentação técnica modular completa.
- [x] Elaboração do guia de prompts de IA para execução acelerada das próximas etapas.
- [x] Auditoria técnica independente de conformidade (100% de aprovação comprovada).

### Fase 2: Infraestrutura Docker & Servidores Web
- [x] Validar ambiente Docker Desktop com suporte a motor WSL 2 no host Windows.
- [x] Criar arquivo `docker/docker-compose.yml` com rede dedicada `net_bench` (172.20.0.0/16).
- [x] Configurar serviço `server-http1`: imagem `nginx:alpine`, porta 8080/8081:80, IP 172.20.0.10, `cap_add: [NET_ADMIN]`.
- [x] Configurar serviço `server-http2`: imagem `nginx:alpine`, porta 8443:443, IP 172.20.0.20, `cap_add: [NET_ADMIN]`, suporte TLS 1.3 e HTTP/2.
- [x] Configurar serviço `server-http3`: imagem `caddy:2.7-alpine`, portas 9443:443/tcp e 9443:443/udp, IP 172.20.0.30, `cap_add: [NET_ADMIN]`, suporte nativo a HTTP/3 QUIC.
- [x] Criar script Python `scripts/generate_certs.py` para gerar certificados locais com Subject Alternative Names (SANs) válidos (`localhost`, `172.20.0.20`, `172.20.0.30`).
- [x] Testar subida dos contêineres e certificar que todos respondem nos respectivos protocolos.

### Fase 3: Geração de Cargas Estáticas e Scripts `tc netem`
- [x] Criar script Python `scripts/generate_payloads.py` e gerar:
  - Carga A: arquivo único de 50 MB (`data/static/50MB.bin`).
  - Carga B: 100 arquivos independentes de 10 KB (`data/static/objects/obj_001.bin` a `obj_100.bin`).
- [x] Mapear o diretório de dados estáticos como volume compartilhado de leitura nos três servidores.
- [x] Criar scripts de automação `scripts/setup_netem.sh` e `scripts/setup_netem.ps1` para:
  - Aplicar Cenário 1 (LAN): `tc qdisc add dev eth0 root netem delay 0.5ms` (RTT = 1ms, perda 0%).
  - Aplicar Cenário 2 (WAN): `tc qdisc add dev eth0 root netem delay 25ms loss 2%` (RTT = 50ms, perda 2%).
  - Limpar interface: `tc qdisc del dev eth0 root`.

### Fase 4: Desenvolvimento do Cliente de Benchmark Python
- [x] Configurar ambiente Python e instalar `httpx`, `aioquic`, `asyncio`, `pandas`, `scipy`.
- [x] Desenvolver `benchmark/client.py`:
  - Cliente assíncrono para requisições HTTP/1.1 e HTTP/2 via `httpx.AsyncClient`.
  - Cliente assíncrono para requisições HTTP/3 sobre QUIC via `aioquic`.
- [x] Implementar **Controle Rigoroso de Viés de Sessão (Client-Side Bias Control)** (`benchmark/session_control.py`):
  - Desabilitar cache HTTP local.
  - Modo Cold TTFB: fechar explicitamente a sessão do cliente (`client.close()`) antes de cada requisição individual para medir latência real do handshake.
  - Modo Warm Connection: manter conexão persistente única para download concorrente de 100 objetos (multiplexação).
- [x] Registrar métricas com precisão de microssegundos via `time.perf_counter()` (`benchmark/metrics.py`).
- [x] Implementar exportação de resultados para `data/raw/results.json` e `data/raw/results.csv`.

### Fase 5: Automação Runner 1-Click e Execução dos 12 Testes
- [x] Criar orquestrador mestre `run_experiments.sh` (Linux/WSL) e `run_experiments.ps1` (Windows):
  1. Subir contêineres (`docker compose up -d`);
  2. Aplicar Cenário 1 (LAN: delay 0.5ms, loss 0%);
  3. Executar T01, T02, T03 (Carga A - 50MB);
  4. Executar T07, T08, T09 (Carga B - 100x10KB);
  5. Aplicar Cenário 2 (WAN: delay 25ms, loss 2%);
  6. Executar T04, T05, T06 (Carga A - 50MB);
  7. Executar T10, T11, T12 (Carga B - 100x10KB);
  8. Restaurar interfaces (`tc qdisc del dev eth0 root`);
  9. Disparar pipeline de processamento e gráficos;
  10. Finalizar contêineres (`docker compose down`).
- [x] Executar bateria completa com repetições independentes ($N \ge 10$).
- [x] Validar integridade dos arquivos gerados em `data/raw/results.json` e `results.csv`.

### Fase 6: Pipeline de Análise Estatística e Visualização Gráfica
- [x] Criar `analysis/process_data.py`:
  - Calcular média, mediana, desvio padrão, percentis p50 e p99, e Intervalo de Confiança de 95% (t-Student, $t=2.262$).
  - Gerar tabelas consolidadas em CSV e LaTeX para o relatório (`summary_table.csv` e `summary_table.tex`).
- [x] Criar `analysis/plot_results.py` e gerar gráficos com **barras de erro obrigatórias** em `data/plots/`:
  - `fig1_ttfb_cold_comparison.png`: TTFB Cold por Protocolo (LAN vs WAN).
  - `fig2_throughput_carga_a.png`: Vazão Sustentada (Goodput) de 50 MB (T01 a T06).
  - `fig3_load_time_carga_b.png`: Tempo Total de Carregamento dos 100 objetos (T07 a T12).
  - `fig4_rps_carga_b_wan.png`: Requisições por Segundo (RPS) na Carga B sob Perdas (T10 vs T11 vs T12).
  - `fig5_cdf_latency_distribution.png`: Curva CDF de latência demonstrando mitigação do HoL blocking no HTTP/3.

### Fase 7: Redação do Relatório Técnico Científico (LaTeX SBC)
- [x] Configurar modelo oficial da SBC (`relatorio/sbc-template.tex`, `sbc.sty`, `relatorio.bib`).
- [x] Redigir Resumo e Abstract com palavras-chave formais.
- [x] Seção 1: Introdução, contextualização da Web moderna e objetivos pedagógicos.
- [x] Seção 2: Fundamentação Teórica (Handshakes, HoL Blocking nas camadas, RFCs 793, 7540, 9000, 9114).
- [x] Seção 3: Metodologia Experimental e Topologia (diagramas, parâmetros do `tc netem`, cliente Python).
- [x] Seção 4: Resultados Experimentais e Discussão:
  - Tabelas de consolidação com médias, medianas, desvio padrão, p50 e p99.
  - Figuras com barras de erro de alta resolução (300 DPI).
  - **Articulação obrigatória com Tanenbaum Seção 6.5.11 (TCP CUBIC)**: justificativa matemática e conceitual do colapso no T04 e T05 sob 2% de perda estocástica na WAN.
  - **Articulação obrigatória com Tanenbaum Seção 6.6.1 (QUIC) e Seção 6.6.2 (BBR)**: justificativa da resiliência e superioridade de throughput/RPS no T06 e T12.
- [x] Seção 5: Conclusões e considerações finais.
- [x] Posição do link do vídeo na 1ª página reservada e formatada no PDF (`relatorio/sbc-template.pdf`, 8 páginas compiladas).

### Fase 8: Gravação do Vídeo de 15 Minutos e Submissão SIGAA
- [x] Elaborar apresentação de slides de suporte em HTML/CSS interativo (`video/slides.html`).
- [x] Estruturar roteiro cronometrado minuto a minuto (00:00 a 15:00) em `brain/04_entregaveis/roteiro_video_15min.md`.
- [ ] Gravar vídeo demonstrativo completo com OBS Studio (15 minutos exatos).
- [ ] Fazer upload no YouTube em modo "Não listado" ou "Público".
- [ ] Substituir o link no LaTeX (`relatorio/sbc-template.tex`, linha 36) e recompilar o PDF final.
- [ ] Empacotar no formato ZIP padronizado (`TP2_Redes2_JoaoMarcosSousa.zip`).
- [ ] Submeter no SIGAA dentro do prazo.
