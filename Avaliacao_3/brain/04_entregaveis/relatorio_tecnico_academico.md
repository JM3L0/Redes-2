# 04. Diretrizes para o Relatório Técnico Conciso (Padrão SBRC — 4 a 6 Páginas) — 3ª Avaliação (N3)

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Curso:** Bacharelado em Sistemas de Informação  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)

Este documento especifica todos os requisitos formais, estruturais e teóricos do **Relatório Técnico Conciso (valendo 50 pontos na rubrica)** da 3ª Avaliação (N3).

---

## 1. 🚨 Regras Formais Estritas do Relatório na N3

1. **Formato Obrigatório:** Artigo científico no padrão da **SBRC / SBC** (`sbc.sty`, compilado em **PDF**).
2. **Limite Estrito de Extensão:** **Mínimo de 4 páginas e máximo de 6 páginas** (Seção 5, item 2 do edital: *"Relatório Técnico Conciso (PDF — mínimo 4, máximo 6 páginas)"*).
3. **Link do Vídeo na 1ª Página (Critério Eliminatório — Nota 0,0 se ausente):**
   O link público/não-listado do vídeo no YouTube (**15 a 25 minutos**, valendo 30 pontos) deve constar de forma destacada logo no bloco de endereço/identificação da **primeira página**:
   ```latex
   \author{João Marcos Sousa Rufino Leal\inst{1}}

   \address{Departamento de Computação -- Universidade Federal do Piauí (UFPI)\\
     Campus Senador Helvídio Nunes de Barros (CSHNB) -- Picos -- PI -- Brasil\\
     \texttt{jsousarufinoleal@ufpi.edu.br}
     \par\vspace{0.2cm}
     \textbf{Repositório do Projeto:} \url{https://github.com/JM3L0/Redes-2}\\
     \textbf{Vídeo Explicativo no YouTube (15--25 min):} \url{https://youtu.be/LINK_DO_VIDEO_N3}
   }
   ```

---

## 2. Estrutura de Seções Planejada (Alvo: 5 a 6 Páginas Exatas)

Para cumprir rigorosamente a faixa de **4 a 6 páginas** no template SBRC sem cortes abruptos nem excesso de páginas:

### Página 1: Título, Autores, Link do Vídeo, Resumo, Abstract e Seção 1 (Introdução)
- **Título:** *Análise Experimental de Controle de Congestionamento (TCP CUBIC vs. BBR) e Retomada de Sessão no QUIC (1-RTT vs. 0-RTT) em Redes Degradadas*
- **Resumo & Abstract:** Contexto, objetivos dos Blocos A e B, metodologia em Docker + `tc netem` (`iperf3` e `curl`), síntese numérica dos resultados (E01 a E06) e conclusões.
- **Seção 1 — Introdução:** Contextualização da evolução da camada de transporte moderna: a transição do controle de congestionamento reativo baseado em perda (CUBIC) para o controle proativo baseado em modelo (BBR), e a unificação transporte-criptografia do QUIC (1-RTT e 0-RTT) frente à pilha clássica TCP+TLS 1.3 (HTTP/2).

### Página 2: Seção 2 (Fundamentação Teórica — Tanenbaum 6ª Ed.)
- **2.1. Controle de Congestionamento TCP CUBIC (Tanenbaum 6ª Ed., Seção 6.5.11):**
  - Equação de crescimento cúbico da janela:
    $$W_{\text{cubic}}(t) = C(t - K)^3 + W_{\max}, \quad K = \sqrt[3]{\frac{W_{\max}\beta}{C}}$$
  - Explicação do fator de decréscimo multiplicativo ($\beta = 0.7$) e da incapacidade de distinguir perdas por congestionamento de descartes estocásticos em enlaces WAN de alto BDP.
- **2.2. Controle de Congestionamento Baseado em Modelo — BBR (Tanenbaum 6ª Ed., Seção 6.6.2):**
  - Estimativa contínua do *Bottleneck Bandwidth* ($BtlBw = \max(\text{delivery\_rate})$) e do *Round-trip propagation time* ($RTprop = \min(\text{RTT})$).
  - Operação no ponto ótimo do Produto Largura de Banda-Atraso ($BDP = BtlBw \times RTprop$) via controle de ritmo (*pacing*), evitando *bufferbloat* e mantendo a vazão estável sob perdas aleatórias de 2%.
- **2.3. Estabelecimento Rápido de Conexão e 0-RTT no QUIC (Tanenbaum 6ª Ed., Seção 6.6.1):**
  - Comparação do custo em RTTs entre TCP+TLS 1.3 (2 RTTs de handshake + 1 RTT de dados = 3 RTTs), QUIC Cold 1-RTT (1 RTT de handshake integrado + 1 RTT de dados = 2 RTTs) e QUIC Warm / Session Resumption 0-RTT (envio imediato de dados sem RTT de handshake = 1 RTT).

### Página 3: Seção 3 (Arquitetura Experimental e Metodologia)
- Topologia Docker na sub-rede `net_bench` (`172.20.0.0/16`): `server_tcp_cc` (`172.20.0.10`, `networkstatic/iperf3`), `server_http3_quic` (`172.20.0.30`, `caddy:2.7-alpine`) e `client_bench` (`172.20.0.50`), todos com `cap_add: NET_ADMIN`.
- Configuração dos **3 Cenários `tc netem`** (Cenário 1 LAN 1ms/0%, Cenário 2 WAN 50ms/2%, Cenário 3 WAN 50ms/0%) e justificativa da simetria do atraso unidirecional ($\text{delay} = \text{RTT}/2$).
- Quadro da **Matriz Experimental Reduzida (E01 a E06)** com $N \ge 5$ repetições por teste e automação via `run_n3.py` / `run_n3.sh`.

### Páginas 4 e 5: Seção 4 (Resultados Experimentais e Discussão Fundamentada)
- **Tabela Resumo Obrigatória:**
  - Bloco A (E01, E02, E03): Vazão Média (Mbps), Desvio Padrão (Mbps), Média de Retransmissões e **Total de Retransmissões**.
  - Bloco B (E04, E05, E06): TTFB Médio (ms) e Desvio Padrão (ms).
- **Gráfico 1 (Bloco A):** Figura de alta resolução (300 DPI) com **barras de erro (desvio padrão)** comparando TCP CUBIC (LAN/WAN) e TCP BBR (WAN).
- **Gráfico 2 (Bloco B):** Figura de alta resolução (300 DPI) com **barras de erro (desvio padrão)** comparando HTTP/2 vs. HTTP/3 Cold vs. HTTP/3 Warm/Resumed.
- **Discussão Analítica Rigorosa (Tanenbaum 6ª Ed.):**
  - Confronto direto dos números obtidos em E01, E02 e E03 com as **Seções 6.5.11 e 6.6.2 de Tanenbaum (6ª Ed.)**.
  - Confronto direto dos tempos em milissegundos obtidos em E04 (~150 ms), E05 (~100 ms) e E06 (~50 ms) com a **Seção 6.6.1 de Tanenbaum (6ª Ed.)** em função do número de RTTs de 50 ms.

### Página 6: Seção 5 (Conclusões) e Referências Bibliográficas
- Síntese dos resultados empíricos dos Blocos A e B.
- Referências bibliográficas formais no padrão SBC (`sbc.bst`), encabeçadas por **TANENBAUM, A. S.; FEAMSTER, N.; WETHERALL, D. J. *Redes de Computadores*. 6ª Edição. Bookman/Pearson, 2021**, seguidas de Cardwell et al. (BBR, *ACM Queue*, 2016), Ha et al. (CUBIC, 2008), RFC 8446 (TLS 1.3), RFC 9000 (QUIC) e RFC 9114 (HTTP/3).

---

## 3. Checklist de Blindagem do Relatório (50 Pontos + Prevenção de Penalidades)

- [ ] Formato oficial de artigo da **SBRC / SBC** compilado em PDF?
- [ ] Número total de páginas entre **4 e 6 páginas**?
- [ ] **Link do vídeo no YouTube (15 a 25 min)** presente e clicável na **1ª página**?
- [ ] **Gráfico 1 (Bloco A)** presente e com **barras de erro (desvio padrão)** visíveis (evita -10 pts)?
- [ ] **Gráfico 2 (Bloco B)** presente e com **barras de erro (desvio padrão)** visíveis (evita -10 pts)?
- [ ] **Tabela Resumo** contendo médias, desvios-padrão e total de retransmissões (Bloco A) + médias e desvios-padrão de TTFB (Bloco B)?
- [ ] **Discussão teórica explícita** citando **Tanenbaum 6ª Ed., Seção 6.5.11 (TCP CUBIC), Seção 6.6.2 (BBR) e Seção 6.6.1 (QUIC)** (evita -20 pts)?
