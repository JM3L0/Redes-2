# Relatório de Execução — Fases 5 e 6: Coleta Estatística, Gráficos com Barras de Erro e Artigo SBRC (4 a 6 Páginas)

**Data:** 17 de Novembro de 2026  
**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)  
**Status das Fases:** ✅ CONCLUÍDAS COM SUCESSO

---

## 1. Artefatos Estatísticos e Visuais Gerados

1. **Consolidação Estatística (`analysis/process_data.py`):**
   - `data/processed/summary_table.csv`, `summary_table.json` e `summary_table.tex`.
2. **Gráficos Comparativos com Barras de Erro (`analysis/plot_results.py`):**
   - **Gráfico 1 (`data/plots/fig1_bloco_a_vazao_cc.png`):** Vazão média (Mbps) comparando TCP CUBIC (LAN/WAN) e TCP BBR (WAN) com barras de erro de desvio padrão ($s$), evidenciando o ganho de **115,3x** do BBR sobre o CUBIC sob 2% de perda na WAN.
   - **Gráfico 2 (`data/plots/fig2_bloco_b_ttfb_handshake.png`):** TTFB médio (ms) comparando HTTP/2 ($163{,}57\text{ ms}$), HTTP/3 Cold 1-RTT ($112{,}36\text{ ms}$) e HTTP/3 Warm/Resumed 0-RTT ($61{,}46\text{ ms}$) com barras de erro de desvio padrão ($s$).
3. **Relatório Técnico Conciso no Formato SBRC (`relatorio/sbc-template.pdf`):**
   - Compilado dentro do limite rigoroso de **4 a 6 páginas** exigido pelo edital, contendo a Tabela Resumo, os 2 gráficos com barras de erro e a discussão teórica fundamentada em **Tanenbaum 6ª Edição (Seções 6.5.11, 6.6.1 e 6.6.2)**.
