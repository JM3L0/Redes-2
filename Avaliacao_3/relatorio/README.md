# Relatório Técnico Conciso — Formato de Artigo da SBRC / SBC (4 a 6 Páginas)

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Autores:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`) & Marcos Willian de Sousa e Silva (`marcos.sousa@ufpi.edu.br`)  
**Título:** *Análise Experimental de Controle de Congestionamento (TCP CUBIC vs. BBR) e Retomada de Sessão (0-RTT) em Redes Degradadas*

---

## 📄 Estrutura de Arquivos

- `sbc-template.tex`: Código-fonte LaTeX formatado no padrão oficial da Sociedade Brasileira de Computação (SBC / SBRC), respeitando o limite estrito de **mínimo 4 e máximo 6 páginas**.
- `sbc.sty` e `sbc.bst`: Pacotes de estilo e bibliografia da SBC.
- `relatorio.bib`: Referências bibliográficas com **Tanenbaum 6ª Edição (Seção 6.5.11, Seção 6.6.1, Seção 6.6.2)**, artigos seminais do CUBIC e BBR, e RFCs do IETF.
- `sbc-template.pdf`: Relatório técnico compilado em PDF pronto para submissão.

---

## 🛠 Instruções de Compilação

```bash
cd relatorio
pdflatex -interaction=nonstopmode sbc-template.tex
bibtex sbc-template
pdflatex -interaction=nonstopmode sbc-template.tex
pdflatex -interaction=nonstopmode sbc-template.tex
```

---

## 🎯 Conformidade com a Rubrica da N3 (50 Pontos)

1. **Padrão SBRC e Limite de Páginas:** Formato oficial da SBRC em PDF com extensão controlada entre **4 e 6 páginas**.
2. **Link do Vídeo na 1ª Página:** Inserido logo abaixo dos dados dos autores.
3. **Gráficos 1 e 2 com Barras de Erro (Desvio Padrão):** Incorporados em alta resolução (300 DPI), evitando a penalidade de -10 pontos.
4. **Tabela Resumo Obrigatória:** Médias, desvios-padrão e total de retransmissões (Bloco A) e médias/desvios-padrão de TTFB (Bloco B).
5. **Discussão Teórica Fundamentada (Tanenbaum, 6ª Ed.):**
   - **Seção 6.5.11 (TCP CUBIC) e Seção 6.6.2 (BBR):** Explicação da degradação severa do CUBIC com 2% de perda vs. manutenção de alta vazão pelo BBR via estimativa do BDP e RTT mínimo.
   - **Seção 6.6.1 (QUIC):** Explicação em milissegundos da diferença empírica entre HTTP/2, HTTP/3 Cold e HTTP/3 Resumed em função do número de RTTs de cada handshake.
