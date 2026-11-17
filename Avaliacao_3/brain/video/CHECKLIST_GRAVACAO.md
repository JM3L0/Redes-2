# ✅ Checklist Rápido de Gravação do Vídeo (15 a 25 Minutos) — 3ª Avaliação (N3)

**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)  
**Duração Obrigatória no Edital:** **Entre 15 e 25 minutos** (Meta do roteiro: **~18 minutos**)  
**Valor na Rubrica:** **30 Pontos** (Ausência = **Nota 0,0**)

---

## 1. Antes de Iniciar a Gravação no OBS Studio
- [ ] Docker Desktop aberto e rodando (`docker compose up -d` executado na pasta `Avaliacao_3`).
- [ ] Backup da pasta `data/` criado (`data_backup_n3`).
- [ ] Abas do VS Code abertas com:
  - [ ] [`relatorio/sbc-template.pdf`](../../relatorio/sbc-template.pdf)
  - [ ] [`docker-compose.yml`](../../docker-compose.yml) e [`docker/Caddyfile`](../../docker/Caddyfile)
  - [ ] [`scripts/setup_netem.py`](../../scripts/setup_netem.py)
  - [ ] [`run_n3.py`](../../run_n3.py) e [`run_n3.sh`](../../run_n3.sh)
  - [ ] [`data/plots/fig1_bloco_a_vazao_cc.png`](../../data/plots/fig1_bloco_a_vazao_cc.png)
  - [ ] [`data/plots/fig2_bloco_b_ttfb_handshake.png`](../../data/plots/fig2_bloco_b_ttfb_handshake.png)
- [ ] Microfone testado no OBS Studio.

---

## 2. Tópicos Obrigatórios Durante a Gravação
- [ ] **Bloco 1 (00:00 - 03:00):** Apresentação individual e explicação dos 2 mecanismos investigados (Bloco A: CUBIC vs. BBR; Bloco B: HTTP/2 vs. HTTP/3 Cold 1-RTT vs. HTTP/3 Warm/Resumption 0-RTT).
- [ ] **Bloco 2 (03:00 - 06:00):** Explicação do `docker-compose.yml` (`server_tcp_cc`, `server_http3_quic`, `client_bench`, `cap_add: NET_ADMIN`) e dos 3 cenários `tc netem` (LAN 1ms/0%, WAN 50ms/2%, WAN 50ms/0% + limpeza).
- [ ] **Bloco 3 (06:00 - 09:00):** Explicação do script de automação (`run_n3.py` / `run_n3.sh`), 5 repetições por teste e extração dos dados brutos (CSV/JSON).
- [ ] **Bloco 4 (09:00 - 12:30):** Demonstração prática ao vivo no terminal (`iperf3 -C cubic` vs. `-C bbr` na WAN com 2% de perda; `curl` HTTP/2 vs. HTTP/3 Cold e Warm na WAN sem perda).
- [ ] **Bloco 5 (12:30 - 16:00):** Apresentação do **Gráfico 1 (Bloco A)** e do **Gráfico 2 (Bloco B)** com **barras de erro (desvio padrão)** e da **Tabela Resumo**.
- [ ] **Bloco 6 (16:00 - 18:00):** Articulação teórica com **Tanenbaum 6ª Ed. (Seções 6.5.11, 6.6.1 e 6.6.2)**, conclusão e verificação de que o cronômetro do OBS está **entre 15:00 e 25:00** antes de encerrar!

---

## 3. Após a Gravação (Submissão SIGAA)
- [ ] Verificar se o vídeo final tem duração **entre 15 e 25 minutos**.
- [ ] Fazer upload no YouTube (**Público** ou **Não listado**) e testar o link em janela anônima.
- [ ] Colar o link definitivo do YouTube na **1ª página** do `relatorio/sbc-template.tex` e recompilar o `relatorio/sbc-template.pdf` (garantindo entre **4 e 6 páginas**).
- [ ] Gerar o arquivo compactado `TP3_Redes2_JoaoMarcosSousaRufinoLeal.zip` contendo o código-fonte + relatório PDF com link do vídeo.
