# Relatório de Execução — Fases 6 e 7: Pipeline Estatístico, Visualização Gráfica e Artigo Científico SBC

**Data:** 21 de Outubro de 2026  
**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)  
**Status das Fases:** ✅ CONCLUÍDAS COM SUCESSO

---

## 1. Escopo e Objetivos Realizados

As Fases 6 e 7 integraram o tratamento dos dados brutos gerados pela matriz de 12 testes ($N=10$) e a redação formal do artigo científico conclusivo:
1. Processamento e consolidação matemática dos dados brutos de `data/raw/results.json` e `results.csv`;
2. Cálculo de métricas descritivas: média, mediana, desvio padrão ($s$), percentis p50 e p99, e Intervalo de Confiança de 95% ($CI_{95\%}$) via distribuição t-Student;
3. Geração programática de 5 gráficos de alta resolução (300 DPI) em `data/plots/` com **barras de erro obrigatórias** em todas as figuras;
4. Redação formal do artigo científico em LaTeX no modelo da Sociedade Brasileira de Computação (SBC/SBRC);
5. Deduções e articulações teóricas detalhadas com Tanenbaum §6.5.11 (TCP CUBIC) e §6.6.1/§6.6.2 (QUIC e BBR);
6. Compilação do PDF oficial (`relatorio/sbc-template.pdf`, 8 páginas) com o link do vídeo posicionado na primeira página.

---

## 2. Pipeline Estatístico e Visualização Gráfica (`analysis/`)

### 2.1. Processamento de Dados (`analysis/process_data.py`)
- Agrega as amostras independentes de cada teste ($N = 10$).
- Aplica o multiplicador crítico de Student para 9 graus de liberdade ($t_{0.025, 9} \approx 2.262$).
- Gera `data/processed/summary_table.csv` e o código da tabela formatada em LaTeX (`data/processed/summary_table.tex`).

### 2.2. Figuras Científicas com Barras de Erro (`analysis/plot_results.py`)
Conforme exigido pelo edital (mitigando a penalidade de -10 pontos), todas as figuras incorporam barras de erro visíveis:
- **`fig1_ttfb_cold_comparison.png`:** Cold TTFB evidenciando o custo dos handshakes: 1 RTT (TCP), 2 RTTs (TCP + TLS 1.3) e 1 RTT integrado (QUIC).
- **`fig2_throughput_carga_a.png`:** Vazão sustentada da Carga A de 50 MB demonstrando o colapso de throughput no TCP CUBIC sob 2% de perda estocástica na WAN (>98% de redução) contra a sustentação de vazão do QUIC/BBR.
- **`fig3_load_time_carga_b.png`:** Tempo total de carregamento dos 100 objetos pequenos de 10 KB.
- **`fig4_rps_carga_b_wan.png`:** Taxa de requisições por segundo (RPS) sob o Cenário WAN, comprovando a superioridade de concorrência do HTTP/3.
- **`fig5_cdf_latency_distribution.png`:** Curva de distribuição acumulada (CDF) dos tempos por objeto, evidenciando a cauda longa no HTTP/2 provocada pelo HoL blocking no TCP e a curva uniforme e rápida do HTTP/3.

---

## 3. Redação do Artigo Científico em LaTeX (`relatorio/sbc-template.tex`)

### 3.1. Estrutura Acadêmica Formal
- **Template:** Modelo oficial SBC (`sbc.sty` e `sbc-template.tex`).
- **Resumo e Abstract:** Contextualização, objetivos empíricos, metodologia e conclusões em português e inglês.
- **Seções Desenvolvidas:**
  1. Introdução e Objetivos Pedagógicos;
  2. Fundamentação Teórica (Handshakes, TLS 1.3, HoL Blocking e multiplexação);
  3. Metodologia Experimental e Topologia (Docker Compose, rede `net_bench`, `tc netem` e cliente assíncrono Python);
  4. Resultados Experimentais e Discussão Analítica (tabelas e figuras com barras de erro);
  5. Considerações Finais e Conclusões;
  6. Referências Bibliográficas (Tanenbaum, RFC 793, RFC 768, RFC 7540, RFC 8446, RFC 9000, RFC 9001, RFC 9114).

### 3.2. Articulação Teórica com Tanenbaum (Evitando penalidade de -20 pontos)
- **Tanenbaum §6.5.11 (TCP CUBIC):** Explicação analítica da função cúbica $W_{\text{cubic}}(t) = C (t - K)^3 + W_{\text{max}}$ e da penalidade multiplicativa ($\beta = 0.7$). Sob 2% de descarte contínuo e 50ms de RTT, a janela *cwnd* colapsa antes de alcançar o ponto de inflexão $W_{\text{max}}$, estrangulando o goodput.
- **Tanenbaum §6.6.1 (QUIC) e §6.6.2 (BBR):** Justificativa de resiliência baseada no desacoplamento entre streams UDP e no controle de ritmo (*pacing*) fundamentado em taxa real de entrega e RTT mínimo físico, imune à interpretação ingênua de perdas estocásticas.

### 3.3. Critério Eliminatório (Nota Zero)
- O link do vídeo técnico foi inserido na **primeira página**, logo abaixo do e-mail do autor, conforme preconiza o edital:
  `\textbf{Vídeo de Apresentação e Demonstração Técnica (15 Minutos):} \url{https://youtu.be/...}`
- O arquivo compilado gerou `relatorio/sbc-template.pdf` com 8 páginas de alta qualidade editorial.
