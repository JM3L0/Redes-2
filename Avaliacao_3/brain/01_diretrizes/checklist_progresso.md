# ✅ Checklist de Progresso e Validação — 3ª Avaliação (N3)

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Projeto:** Análise Experimental de Controle de Congestionamento (TCP CUBIC vs. BBR) e Retomada de Sessão (0-RTT) em Redes Degradadas  
**Equipe:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`) & Marcos Willian de Sousa e Silva (`marcos.sousa@ufpi.edu.br`)

---

## 🧭 Quadro Geral de Fases

| Fase | Descrição da Fase | Status |
| :--- | :--- | :---: |
| **Fase 1** | Análise minuciosa do edital (`Terceira Avaliacao.pdf`) e estruturação completa do Cérebro (`brain/`) | ✅ CONCLUÍDA |
| **Fase 2** | Infraestrutura Docker (`docker-compose.yml`, `server_tcp_cc`, `server_http3_quic`, `client_bench`), Certificados TLS 1.3 e Objeto 1 KB | ✅ CONCLUÍDA |
| **Fase 3** | Scripts de Emulação `tc netem` (Cenários 1, 2 e 3 + Limpeza) e Validação de Kernel (`tcp_bbr` / `cubic`) | ✅ CONCLUÍDA |
| **Fase 4** | Desenvolvimento do Orquestrador de Automação (`run_n3.py`, `run_n3.sh`, `run_n3.ps1`) e Execução dos 6 Testes (E01 a E06, $N = 5$) | ✅ CONCLUÍDA |
| **Fase 5** | Pipeline Estatístico (`process_data.py`) e Geração dos 2 Gráficos Obrigatórios com Barras de Erro (`plot_results.py`) | ✅ CONCLUÍDA |
| **Fase 6** | Redação do Relatório Técnico Conciso no Formato SBRC (PDF — 6 páginas exatas) com Fundamentação Tanenbaum 6ª Ed. | ✅ CONCLUÍDA |
| **Fase 7** | Roteiro do Vídeo (15 a 25 minutos), Auditoria Pré-Submissão e Empacotamento `.zip` (`TP3_Redes2_...zip`) | ✅ CONCLUÍDA (Aguardando Gravação do Vídeo) |

---

## 📋 Itens Validados

- [x] `docker-compose.yml` configurado com `server_tcp_cc` (`172.20.0.10`), `server_http3_quic` (`172.20.0.30`) e `client_bench` (`172.20.0.50`) e permissão `cap_add: [NET_ADMIN]`.
- [x] Certificados TLS 1.3 (`certs/cert.pem` e `certs/key.pem`) e objeto estático de 1 KB (`site/1KB.bin`, `1024` bytes) gerados.
- [x] Três cenários `tc netem` (Cenário 1 LAN 1ms/0%, Cenário 2 WAN 50ms/2%, Cenário 3 WAN 50ms/0%) e limpeza (`tc qdisc del dev eth0 root`) validados.
- [x] Execução completa de $N = 5$ repetições independentes para os 6 testes essenciais (`E01` a `E06`), exportando `data/raw/results.csv` e `data/raw/results.json`.
- [x] **Gráfico 1 (Bloco A)** (`data/plots/fig1_bloco_a_vazao_cc.png`) e **Gráfico 2 (Bloco B)** (`data/plots/fig2_bloco_b_ttfb_handshake.png`) gerados a 300 DPI com **barras de erro representando o desvio padrão**.
- [x] **Relatório Técnico Conciso** (`relatorio/sbc-template.pdf`) compilado no formato oficial da **SBRC** com **6 páginas exatas** (dentro da faixa obrigatória de 4 a 6 páginas), contendo a Tabela Resumo, os 2 gráficos com barras de erro, o link do vídeo na 1ª página e a discussão teórica fundamentada em **Tanenbaum 6ª Edição (Seções 6.5.11, 6.6.1 e 6.6.2)**.
- [x] Pacote final `TP3_Redes2_JoaoMarcosSousaRufinoLeal_MarcosWilliandeSousaeSilva.zip` gerado.
