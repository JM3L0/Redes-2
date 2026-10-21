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
| **Fase 2** | Infraestrutura Docker (Nginx HTTP/1.1, Nginx HTTPS TLS 1.3, Caddy HTTP/3 QUIC) | ⏳ A INICIAR |
| **Fase 3** | Geração de Cargas Estáticas (50 MB e 100x10 KB) e Scripts `tc netem` | ⏳ A INICIAR |
| **Fase 4** | Desenvolvimento do Cliente de Benchmark Python Assíncrono (`httpx` + `aioquic`) | ⏳ A INICIAR |
| **Fase 5** | Automação Runner 1-Click (`run_experiments.sh` / `.ps1`) e Execução dos 12 Testes | ⏳ A INICIAR |
| **Fase 6** | Pipeline de Análise Estatística e Visualização com Barras de Erro Obrigatórias | ⏳ A INICIAR |
| **Fase 7** | Redação do Relatório Técnico com Fundamentação Tanenbaum (§6.5.11 e §6.6.1/§6.6.2) | ⏳ A INICIAR |
| **Fase 8** | Gravação do Vídeo de 15 Minutos, Auditoria Pré-Submissão e Empacotamento | ⏳ A INICIAR |

---

## 📋 Itens Detalhados por Fase

### Fase 1: Análise e Estruturação do Cérebro
- [x] Leitura completa e extração textual de `Segunda Avaliação Redes 2.pdf`.
- [x] Mapeamento dos 3 fenômenos: Overhead de Handshake (1 RTT vs 2 RTTs vs 1 RTT), HoL Blocking (aplicação vs transporte vs eliminação em fluxos UDP), e Controle de Congestionamento (CUBIC vs BBR sob 2% de perda).
- [x] Identificação de todas as penalidades (-15pts sem runner 1-click, -10pts sem controle de vício de sessão, -10pts sem barras de erro, -20pts relatório puramente descritivo).
- [x] Identificação do critério eliminatório crítico (falta de código, relatório em PDF ou link do vídeo de 15min = NOTA ZERO 0,0).
- [x] Criação do diretório `brain/` e documentação técnica modular completa.
- [x] Elaboração do guia de prompts de IA para execução acelerada das próximas etapas.

### Fase 2: Infraestrutura Docker & Servidores Web
- [ ] Validar ambiente Docker Desktop com suporte a motor WSL 2 no host Windows.
- [ ] Criar arquivo `docker/docker-compose.yml` com rede dedicada `net_bench` (172.20.0.0/16).
- [ ] Configurar serviço `server-http1`: imagem `nginx:alpine`, porta 8080:80, IP 172.20.0.10, `cap_add: [NET_ADMIN]`.
- [ ] Configurar serviço `server-http2`: imagem `nginx:alpine`, porta 8443:443, IP 172.20.0.20, `cap_add: [NET_ADMIN]`, suporte TLS 1.3 e HTTP/2.
- [ ] Configurar serviço `server-http3`: imagem `caddy:2.7-alpine`, portas 9443:443/tcp e 9443:443/udp, IP 172.20.0.30, `cap_add: [NET_ADMIN]`, suporte nativo a HTTP/3 QUIC.
- [ ] Criar script OpenSSL para gerar certificados locais com Subject Alternative Names (SANs) válidos (`localhost`, `172.20.0.20`, `172.20.0.30`).
- [ ] Testar subida dos contêineres e certificar que todos respondem nos respectivos protocolos.

### Fase 3: Geração de Cargas Estáticas e Scripts `tc netem`
- [ ] Criar script Python `scripts/generate_payloads.py` para gerar:
  - Carga A: arquivo único de 50 MB (`50MB.bin`).
  - Carga B: 100 arquivos independentes de 10 KB (`objects/obj_001.bin` a `obj_100.bin`).
- [ ] Mapear o diretório de dados estáticos como volume compartilhado de leitura nos três servidores.
- [ ] Criar script `scripts/setup_netem.sh` para:
  - Aplicar Cenário 1 (LAN): `tc qdisc add dev eth0 root netem delay 0.5ms` (RTT = 1ms, perda 0%).
  - Aplicar Cenário 2 (WAN): `tc qdisc add dev eth0 root netem delay 25ms loss 2%` (RTT = 50ms, perda 2%).
  - Limpar interface: `tc qdisc del dev eth0 root`.

### Fase 4: Desenvolvimento do Cliente de Benchmark Python
- [ ] Criar ambiente virtual Python e instalar `httpx`, `aioquic`, `asyncio`, `pandas`, `scipy`.
- [ ] Desenvolver `benchmark/client.py`:
  - Cliente assíncrono para requisições HTTP/1.1 e HTTP/2 via `httpx.AsyncClient`.
  - Cliente assíncrono para requisições HTTP/3 sobre QUIC via `aioquic`.
- [ ] Implementar **Controle Rigoroso de Vício de Sessão (Client-Side Bias Control)**:
  - Desabilitar cache HTTP local.
  - Modo Cold TTFB: fechar explicitamente a sessão do cliente (`client.close()`) antes de cada requisição individual para medir latência real do handshake.
  - Modo Warm Connection: manter conexão persistente única para download concorrente de 100 objetos (multiplexação).
- [ ] Registrar métricas com precisão de microssegundos: TTFB, Total Load Time, RPS, status code.
- [ ] Implementar exportação de resultados para `data/raw/results.json` e `data/raw/results.csv`.

### Fase 5: Automação Runner 1-Click e Execução dos 12 Testes
- [ ] Criar orquestrador mestre `run_experiments.sh` (Linux/WSL) e `run_experiments.ps1` (Windows):
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
- [ ] Executar bateria completa com no mínimo 10 repetições por teste ($N \ge 10$).
- [ ] Validar integridade dos arquivos gerados em `data/raw/`.

### Fase 6: Pipeline de Análise Estatística e Visualização Gráfica
- [ ] Criar `analysis/process_data.py`:
  - Calcular média, mediana, desvio padrão, percentis p50 e p99, e Intervalo de Confiança de 95% (t-Student).
  - Gerar tabelas consolidadas em CSV e LaTeX para o relatório.
- [ ] Criar `analysis/plot_results.py`:
  - Gráfico 1: TTFB Cold vs Warm por Protocolo (LAN vs WAN) — **com barras de erro**.
  - Gráfico 2: Vazão Sustentada (Throughput) de 50 MB (T01 a T06) — **com barras de erro**.
  - Gráfico 3: Tempo Total de Carregamento dos 100 objetos (T07 a T12) — **com barras de erro**.
  - Gráfico 4: Requisições por Segundo (RPS) na Carga B sob Perdas (T10 vs T11 vs T12) — **com barras de erro**.
  - Gráfico 5: Curva CDF de latência dos fluxos demonstrando eliminação do HoL blocking no HTTP/3.

### Fase 7: Redação do Relatório Técnico Científico (LaTeX SBC)
- [ ] Configurar modelo oficial da SBC (`relatorio/sbc-template.tex`, `sbc.sty`).
- [ ] Redigir Resumo e Abstract com palavras-chave.
- [ ] Seção 1: Introdução, contextualização da Web moderna e objetivos pedagógicos.
- [ ] Seção 2: Fundamentação Teórica (Handshakes, HoL Blocking nas camadas, RFCs 793, 7540, 9000, 9114).
- [ ] Seção 3: Metodologia Experimental e Topologia (diagramas Mermaid convertidos, parâmetros do `tc netem`, cliente Python).
- [ ] Seção 4: Resultados Experimentais e Discussão:
  - Tabelas de consolidação com médias, medianas, desvio padrão, p50 e p99.
  - Figuras com barras de erro de alta resolução (300 DPI).
  - **Articulação obrigatória com Tanenbaum §6.5.11 (TCP CUBIC)**: justificativa matemática e conceitual do colapso no T04 e T05 sob 2% de perda estocástica na WAN.
  - **Articulação obrigatória com Tanenbaum §6.6.1 (QUIC) e §6.6.2 (BBR)**: justificativa da resiliência e superioridade de throughput/RPS no T06 e T12.
- [ ] Seção 5: Conclusões e considerações finais.
- [ ] **INSERIR O LINK PÚBLICO DO VÍDEO DO YOUTUBE NA 1ª PÁGINA DO ARTIGO (CRÍTICO!)**.

### Fase 8: Gravação do Vídeo de 15 Minutos e Auditoria Final
- [ ] Elaborar apresentação de slides de suporte (`video/slide_deck/`).
- [ ] Ensaiar blocos cronometrados para atingir exatamente 15 minutos (tolerância: 14:50 a 15:10).
- [ ] Gravar vídeo demonstrativo completo com OBS Studio:
  - Apresentação da equipe e visão geral (2 min);
  - Código-fonte, Docker Compose e configurações de servidores (2.5 min);
  - Código do cliente Python assíncrono e controle de viés de sessão (3 min);
  - Execução ao vivo do `run_experiments.sh` e inspeção de logs (3 min);
  - Análise dos gráficos com barras de erro e fundamentação teórica Tanenbaum (3 min);
  - Conclusão e lições aprendidas (1.5 min).
- [ ] Fazer upload do vídeo no YouTube em modo "Não listado" ou "Público".
- [ ] Inserir o link do vídeo na 1ª página do relatório LaTeX e recompilar o PDF.
- [ ] Testar clique no link em janela anônima para garantir que o vídeo abre diretamente.
- [ ] Empacotar o diretório conforme edital: `TP2_Redes2_NomeAluno1_NomeAluno2.zip`.
- [ ] Submeter no SIGAA dentro do prazo.
