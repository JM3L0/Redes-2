# ✅ Checklist de Progresso e Validação do Projeto

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** UFPI — Bacharelado em Sistemas de Informação  
**Projeto:** Avaliação de Desempenho e Sobrecarga de Transporte — TCP, UDP e QUIC

---

## 🧭 Quadro Geral de Fases

| Fase | Descrição | Status |
| :--- | :--- | :---: |
| **Fase 1** | Análise minuciosa do edital e criação do Cérebro do Projeto |  CONCLUÍDA |
| **Fase 2** | Infraestrutura Docker (NGINX HTTP/3 + iperf3 + curl HTTP/3 + tc) |  CONCLUÍDA |
| **Fase 3** | Scripts de Automação, Emulação de Canal (`tc/netem`) e Capturas |  CONCLUÍDA |
| **Fase 4** | Execução das Baterias Experimentais (Cenários A, B e C com $N=10$) | ⏳ A INICIAR |
| **Fase 5** | Pipeline Python: Processamento de Dados, Estatística e Gráficos |  CONCLUÍDA |
| **Fase 6** | Redação do Artigo Científico no Padrão SBC/SBRC (LaTeX) | ⏳ A INICIAR |
| **Fase 7** | Gravação e Hospedagem do Vídeo Técnico (15 minutos exatos) | ⏳ A INICIAR |
| **Fase 8** | Verificação Crítica Pré-Submissão (Critérios Eliminatórios) | ⏳ A INICIAR |

---

## 📋 Itens Detalhados por Fase

### Fase 1: Análise e Estruturação do Cérebro
- [x] Leitura completa do arquivo `1_Avaliacao - Redes 2.pdf`.
- [x] Identificação das regras críticas eliminatórias (PDF SBC + Link do vídeo funcional = Nota 0 se faltar).
- [x] Criação do diretório `brain/` com documentação técnica modular.
- [x] Elaboração do guia de prompts para delegação a IAs.

### Fase 2: Infraestrutura Docker & NGINX
- [x] Validar ambiente no host: Docker Desktop com motor WSL 2 ativo.
- [x] Garantir que scripts `.sh` e arquivos de config usem quebra de linha `LF` (e não `CRLF`).
- [x] Criar pasta `docker/` e subpastas `server/` e `client/`.
- [x] Configurar `docker/server/Dockerfile` (NGINX com suporte a HTTP/3 + `iperf3 -s`).
- [x] Configurar `docker/server/nginx.conf` com TLS 1.3, QUIC e cabeçalho `Alt-Svc`.
- [x] Criar script para gerar certificados autoassinados via OpenSSL (`entrypoint.sh`).
- [x] Gerar dados de teste estáticos (arquivos de 100MB, 1GB e 100 objetos web via `generate_static_data.py`).
- [x] Configurar `docker/client/Dockerfile` (Ubuntu com cURL HTTP/3 nativo, iperf3, tshark, Python).
- [x] Criar `docker/docker-compose.yml` com rede bridge 172.28.0.0/16 e `cap_add: [NET_ADMIN]`.
- [x] Testar se `docker compose up -d` sobe limpo e ambos contêineres se comunicam.

### Fase 3: Scripts de Automação e Emulação
- [x] Criar `scripts/setup_netem.sh` para alternar entre as condições dos Cenários A, B e C.
- [x] Criar `scripts/test_scenario_a.sh` (10 repetições de UDP em taxas de 10 a 500 Mbps).
- [x] Criar `scripts/test_scenario_b.sh` (10 repetições de download massivo HTTP/1.1 vs HTTP/2 vs HTTP/3).
- [x] Criar `scripts/test_scenario_c.sh` (10 repetições de 100 objetos simultâneos sob perda de 2% a 5%).
- [x] Criar orquestrador mestre `scripts/run_experiments.sh` que dispara tudo de ponta a ponta sem intervenção manual.
- [x] Validar a sincronização de gravação dos `.pcapng` com `tshark` (substituído `sleep 1` por polling de PID).

### Fase 4: Execução Experimental e Coleta
- [ ] Executar bateria completa do Cenário A ($10 \times 5 = 50$ execuções).
- [ ] Executar bateria completa do Cenário B ($10 \times 3 \times 2 = 60$ execuções).
- [ ] Executar bateria completa do Cenário C ($10 \times 3 \times 3 = 90$ execuções).
- [ ] Conferir integridade de todos os arquivos de logs CSV/JSON e `.pcapng` em `data/`.

### Fase 5: Análise Estatística e Gráficos (Python)
- [x] Criar `analysis/parse_logs.py` para processar métricas de Goodput, FCT e Overhead (via tshark).
- [x] Calcular média, desvio padrão e intervalo de confiança de 95% para cada ponto (t-Student, t_crit=2.262, N=10).
- [x] Criar `analysis/generate_plots.py` e gerar:
  - [x] Gráfico 1: UDP Taxa de Injeção vs Goodput/Jitter (Cenário A).
  - [x] Gráfico 2: Sobrecarga de cabeçalho comparativa (UDP 8B vs TCP vs QUIC).
  - [x] Gráfico 3: FCT e Goodput de 100MB/1GB com barras de erro (Cenário B).
  - [x] Gráfico 4: Handshake TLS/QUIC e TTFB por protocolo (Cenário B).
  - [x] Gráfico 5: FCT Médio e p95 sob perdas contínuas (Cenário C).
  - [x] Gráfico 6: Curva CDF demonstrando mitigação do HoL Blocking no QUIC (Cenário C).

### Fase 6: Redação do Artigo Científico (LaTeX SBC)
- [ ] Baixar/configurar template oficial da SBC (`sbc-template.tex` e `sbc.sty`).
- [ ] Redigir Resumo e Abstract.
- [ ] Redigir Seção 1: Introdução e Objetivos.
- [ ] Redigir Seção 2: Fundamentação Teórica (detalhando TCP RFC 793, UDP RFC 768, QUIC RFC 9000/9001 e TLS 1.3 RFC 8446).
- [ ] Redigir Seção 3: Metodologia e Topologia (diagramas e parâmetros `tc/netem`).
- [ ] Redigir Seção 4: Resultados Experimentais e Discussão (incorporando tabelas consolidadas e figuras de alta resolução).
- [ ] Redigir Seção 5: Conclusões.
- [ ] Compilar bibliografia com todas as RFCs mandatórias.
- [ ] **INSERIR O LINK DO VÍDEO NA 1ª PÁGINA DO ARTIGO (CRÍTICO!)**.

### Fase 7: Gravação do Vídeo Técnico (15 Minutos)
- [ ] Elaborar slides de suporte (`video/slide_deck/`).
- [ ] Ensaiar a transição entre blocos cronometrados (00:00 a 15:00).
- [ ] Gravar apresentação com OBS Studio (código, terminal ao vivo, tshark/Wireshark e gráficos).
- [ ] Validar tempo exato de 15 minutos (tolerância recomendada: 14:50 a 15:10).
- [ ] Fazer upload no YouTube ("Não listado" ou "Público") ou Google Drive (permissão aberta a todos).
- [ ] Testar o link em janela anônima em dispositivo diferente.

### Fase 8: Validação Final e Submissão
- [ ] Compilar versão final do PDF do artigo no modelo SBC.
- [ ] Clicar no link do vídeo contido na 1ª página do PDF e confirmar se abre diretamente o vídeo.
- [ ] Conferir se todos os 3 cenários foram documentados e fundamentados.
- [ ] Compactar ou submeter conforme instruções do professor.
