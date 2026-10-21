# Relatório Técnico Científico — Artigo Padrão SBC

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Autor:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)  
**Título:** *Estudo Experimental de Desempenho e Sobrecarga de Protocolos Web: Uma Análise Comparativa entre HTTP/1.1, HTTPS/TLS 1.3 e HTTP/3-QUIC sob Degradação Controlada de Canal com Docker e Python*

---

## 📄 Estrutura de Arquivos

- `sbc-template.tex`: Código-fonte LaTeX formatado rigorosamente no padrão SBC/SBRC.
- `sbc.sty`: Pacote de estilo oficial da Sociedade Brasileira de Computação (SBC).
- `relatorio.bib`: Base de referências bibliográficas com Tanenbaum (Seção 6.5.11, Seção 6.6.1, Seção 6.6.2) e todas as RFCs do IETF (RFC 793, 7540, 8446, 9000, 9001, 9114).
- `sbc-template.pdf`: Documento final compilado em alta resolução.

---

## 🛠 Instruções de Compilação

Para compilar o artigo e resolver todas as citações bibliográficas e referências cruzadas:

No terminal (Linux, macOS, WSL ou Windows com MiKTeX/TeX Live):
```bash
cd relatorio
pdflatex -interaction=nonstopmode sbc-template.tex
bibtex sbc-template
pdflatex -interaction=nonstopmode sbc-template.tex
pdflatex -interaction=nonstopmode sbc-template.tex
```

---

## 🎯 Elementos Mandatórios Atendidos

1. **Link do Vídeo no YouTube:** Posicionado logo abaixo dos dados do autor na **Página 1** (critério eliminatório contra nota zero).
2. **Fundamentação Teórica Mandatória:**
   - Citação analítica de **Tanenbaum Seção 6.5.11** para explicar a retração multiplicativa e colapso do TCP CUBIC sob 2% de perda na WAN;
   - Citação de **Tanenbaum Seções 6.6.1 e 6.6.2** para demonstrar a imunidade ao HoL blocking e o controle de pacing do QUIC/BBR.
3. **Visualização Científica:** Todas as figuras citadas contêm **barras de erro obrigatórias** (evitando a penalidade de -10 pontos).
4. **Tabela de Consolidação Numérica:** Média, desvio padrão, percentis p50 e p99, Throughput e RPS para todos os 12 testes (T01 a T12).
