# 🎬 Checklist de Gravação do Vídeo Técnico (15 Minutos — Com Links Clicáveis)
## Estudo Experimental de Desempenho de Protocolos Web (HTTP/1.1 vs HTTPS/TLS 1.3 vs HTTP/3-QUIC)
**Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)**  
**Equipe:** João Marcos Sousa Rufino Leal & Marcos Willian de Sousa e Silva  
**Disciplina:** Redes de Computadores II (2026-2)  

> **Instrução de Uso:** Todos os arquivos abaixo são **links clicáveis** (`Ctrl + Clique` no editor ou clique simples no Preview do Markdown). Basta clicar em cada arquivo na ordem da lista para abri-lo imediatamente na tela durante a gravação!

---

### ⏱ Visão de Tempo e Cronograma
- **Tempo Total Obrigatório:** **15 minutos** (janela ideal: **14:45 a 15:05**).
- **Divisão da Dupla:** ~7m30s de fala para João Marcos e ~7m30s para Marcos Willian.
- **Resolução de Gravação:** 1080p (1920x1080), 30 ou 60 FPS no OBS Studio.

---

### 📋 Checklist de Itens Obrigatórios por Bloco

#### 🟢 Bloco 1: Abertura e Objetivos [00:00 - 02:00] (~2 min)
- [ ] **Clicar para abrir:** 📄 [sbc-template.pdf](../../relatorio/sbc-template.pdf) *(Páginas 1 e 2)* ou [README.md](../../README.md).
- [ ] **Apresentação verbal da equipe:** João Marcos e Marcos Willian se apresentam com nome completo.
- [ ] **Objetivo 1 (apontar na Seção 1 / Tabela 1 do PDF):** Overhead de handshakes e latência inicial no Time to First Byte (1 RTT TCP vs 2 RTTs HTTPS/TLS 1.3 vs 1 RTT integrado QUIC/UDP).
- [ ] **Objetivo 2 (apontar na Tabela 1 do PDF):** Bloqueio de Início de Linha (*Head-of-Line Blocking*) na aplicação (HTTP/1.1), transferido para o transporte TCP (HTTP/2) e eliminado completamente no HTTP/3 via streams UDP independentes.
- [ ] **Objetivo 3:** Efeito das condições de canal móvel/WAN (50ms de RTT e 2% de perda estocástica) comparando TCP CUBIC vs QUIC.

---

#### 🟢 Bloco 2: Arquitetura Docker e Emulação `tc netem` [02:00 - 04:30] (~2m30s)
- [ ] **Clicar para abrir:** 🐳 [docker-compose.yml](../../docker/docker-compose.yml)
  - [ ] Apontar a rede bridge isolada `net_bench` (sub-rede `172.20.0.0/16`).
  - [ ] Apontar o Servidor 1 (`server_http11`, IP `172.20.0.10`, porta `8080`) e clicar em [server-http1/nginx.conf](../../docker/server-http1/nginx.conf).
  - [ ] Apontar o Servidor 2 (`server_http2_tls`, IP `172.20.0.20`, porta `8443`) e clicar em [server-http2/nginx.conf](../../docker/server-http2/nginx.conf) (`listen 443 ssl http2; ssl_protocols TLSv1.3`).
  - [ ] Apontar o Servidor 3 (`server_http3_quic`, IP `172.20.0.30`, porta `9443` TCP e UDP) e clicar em [server-http3/Caddyfile](../../docker/server-http3/Caddyfile).
- [ ] **Enfatizar o privilégio de kernel obrigatório:**
  - [ ] Clicar em [docker-compose.yml (linha 7)](../../docker/docker-compose.yml#L7-L8) para destacar `cap_add: - NET_ADMIN` e explicar que sem isso o `tc` falha por falta de permissão.
- [ ] **Clicar para abrir:** 🌐 [setup_netem.ps1](../../scripts/setup_netem.ps1) *(ou [setup_netem.sh](../../scripts/setup_netem.sh))*
  - [ ] Apontar o Cenário 1 (LAN): atraso de `0.5ms` (RTT = `1.0ms`, perda 0%).
  - [ ] Apontar o Cenário 2 (WAN): atraso de `25ms` e `loss 2%` (RTT = `50ms` e 2% de perda).
  - [ ] Apontar a função de limpeza: `tc qdisc del dev eth0 root`.

---

#### 🟢 Bloco 3: Cliente Python e Controle de Viés [04:30 - 07:30] (~3 min)
- [ ] **Clicar para abrir:** 🔒 [session_control.py](../../benchmark/session_control.py)
  - [ ] Mostrar `get_no_cache_headers()` desativando qualquer cache (`Cache-Control: no-cache, no-store, must-revalidate`).
  - [ ] Explicar `SessionMode.COLD` vs `SessionMode.WARM` (controle de viés que evita a penalidade de -10 pontos).
- [ ] **Clicar para abrir:** 🐍 [client.py](../../benchmark/client.py)
  - [ ] Mostrar os imports assíncronos (`asyncio`, `httpx`, `aioquic`) e a classe [H3BenchmarkProtocol (linha 44)](../../benchmark/client.py#L44).
  - [ ] Clicar no **Modo Cold TTFB** ([fetch_httpx_cold (linha 128)](../../benchmark/client.py#L128) e [fetch_h3_cold (linha 173)](../../benchmark/client.py#L173)): destacar o fechamento explícito da sessão (`client.aclose()`) antes de CADA requisição individual.
  - [ ] Clicar no **Modo Warm Concurrency** ([fetch_httpx_warm_batch (linha 225)](../../benchmark/client.py#L225) e [fetch_h3_warm_batch (linha 285)](../../benchmark/client.py#L285)): destacar que abre **uma única conexão persistente** e dispara os **100 objetos de 10 KB simultaneamente** com `asyncio.gather`.
  - [ ] Clicar na matriz dos 12 testes ([TEST_DEFINITIONS (linha 350)](../../benchmark/client.py#L350)): Carga A (50 MB) e Carga B (100x10 KB).
- [ ] **Clicar para abrir:** 📊 [metrics.py](../../benchmark/metrics.py)
  - [ ] Mostrar `RequestMetric` e a exportação para [results.json](../../data/raw/results.json) e [results.csv](../../data/raw/results.csv).

---

#### 🟢 Bloco 4: Demonstração Experimental ao Vivo (1-Click Run) [07:30 - 10:30] (~3 min)
- [ ] **Clicar para abrir:** ⚡ [run_experiments.ps1](../../run_experiments.ps1) e [run_experiments.sh](../../run_experiments.sh) (mostrando que o projeto inteiro roda com 1 único comando, evitando a penalidade de -15 pontos).
- [ ] **Na Tela (Terminal PowerShell):** Seguir os comandos de 📋 [GUIA_EXECUCAO_AO_VIVO.md](GUIA_EXECUCAO_AO_VIVO.md):
  - [ ] Aplicar `.\scripts\setup_netem.ps1 lan` e rodar testes rápidos na LAN (`T01`, `T02`, `T09`).
  - [ ] Aplicar `.\scripts\setup_netem.ps1 wan` e rodar ao vivo `T10` (HTTP/1.1), `T11` (HTTP/2) e `T12` (HTTP/3) na WAN, mostrando o HTTP/3 terminando os 100 objetos em ~1 segundo enquanto o HTTP/2 e o HTTP/1.1 demoram de 3 a 5 segundos.
  - [ ] Limpar a interface com `.\scripts\setup_netem.ps1 clean` e rodar [process_data.py](../../analysis/process_data.py) e [plot_results.py](../../analysis/plot_results.py).
- [ ] **Clicar para abrir:** 📁 [results.csv](../../data/raw/results.csv) e [summary_table.csv](../../data/processed/summary_table.csv) para mostrar os dados exportados.

---

#### 🟢 Bloco 5: Resultados e Fundamentação em Tanenbaum [10:30 - 13:30] (~3 min)
- [ ] **Clicar para abrir:** 📄 [sbc-template.pdf](../../relatorio/sbc-template.pdf) *(Páginas 4 a 8)* ou clicar direto nas imagens abaixo:
- [ ] **Mostrar a Tabela 2 do [sbc-template.pdf](../../relatorio/sbc-template.pdf) (Página 4):** Consolidação dos 12 testes.
- [ ] **Clicar na Figura 1:** 📈 [fig1_ttfb_cold_comparison.png](../../data/plots/fig1_ttfb_cold_comparison.png) *(ou Página 5 do PDF)*:
  - [ ] Apontar as **barras de erro obrigatórias** (IC 95%).
  - [ ] Explicar que na WAN o HTTPS/HTTP/2 leva quase o dobro do tempo de TTFB (2 viagens de ida e volta: TCP + TLS) comparado ao HTTP/3 (1 viagem unificada no QUIC).
- [ ] **Clicar na Figura 2:** 📈 [fig2_throughput_carga_a.png](../../data/plots/fig2_throughput_carga_a.png) *(ou Páginas 5 e 6 do PDF)*:
  - [ ] Explicar por que na LAN o TCP é mais rápido (roda direto no kernel do Linux, enquanto `aioquic` roda em Python no espaço de usuário), mas na WAN com perdas a velocidade do TCP despenca.
  - [ ] **Apontar na Página 6 do [sbc-template.pdf](../../relatorio/sbc-template.pdf) a Citação Teórica — Tanenbaum Seção 6.5.11 (TCP CUBIC):**
    - [ ] Explicar de forma conceitual: o TCP CUBIC trata qualquer pacote perdido como congestionamento e corta drasticamente sua janela de transmissão; como na WAN há perdas o tempo todo, a janela é cortada repetidas vezes antes de conseguir crescer de novo.
- [ ] **Clicar nas Figuras 3, 4 e 5:**
  - 📈 [fig3_load_time_carga_b.png](../../data/plots/fig3_load_time_carga_b.png) *(Tempo de carga dos 100 objetos)*
  - 📈 [fig4_rps_carga_b_wan.png](../../data/plots/fig4_rps_carga_b_wan.png) *(RPS na WAN: HTTP/3 faz quase o triplo do HTTP/2)*
  - 📈 [fig5_cdf_latency_distribution.png](../../data/plots/fig5_cdf_latency_distribution.png) *(Curva CDF de latência com barras de erro)*
  - [ ] **Apontar na Página 7 do [sbc-template.pdf](../../relatorio/sbc-template.pdf) a Citação Teórica — Tanenbaum Seções 6.6.1 (QUIC) e 6.6.2 (BBR):**
    - [ ] Explicar de forma conceitual o fim do *Head-of-Line Blocking*: no HTTP/2 um pacote perdido trava todos os 100 arquivos na mesma fila do TCP, enquanto no HTTP/3 sobre QUIC cada arquivo tem seu próprio fluxo UDP (só o arquivo que sofreu perda espera retransmissão, e os outros 99 passam direto).
    - [ ] Mencionar que o controle de congestionamento moderno do QUIC/BBR (Seção 6.6.2) controla o ritmo de envio medindo a banda e a latência real sem entrar em pânico a cada perda isolada.
    - [ ] Mostrar na [Figura 5 (CDF)](../../data/plots/fig5_cdf_latency_distribution.png) que a linha verde do HTTP/3 sobe reta logo no início, enquanto as linhas do HTTP/2 e HTTP/1.1 se esticam para a direita por causa das travadas de fila do TCP.

---

#### 🟢 Bloco 6: Conclusões e Encerramento [13:30 - 15:00] (~1m30s)
- [ ] **Clicar para abrir:** 📄 [sbc-template.pdf](../../relatorio/sbc-template.pdf) *(Páginas 8 e 9 — Seção 5 e Referências)* e [relatorio.bib](../../relatorio/relatorio.bib).
- [ ] **Síntese dos achados:** TCP em kernel é ótimo em redes locais perfeitas (LAN), mas o HTTP/3 sobre QUIC é indispensável em redes reais e móveis (WAN) sujeitas a atraso e perda de pacotes.
- [ ] **Voltar à Página 1 do [sbc-template.pdf](../../relatorio/sbc-template.pdf):** Mostrar onde ficará o link público do vídeo no cabeçalho do artigo SBC antes da submissão no SIGAA.
- [ ] **Agradecimento final:** Agradecer ao professor e encerrar a gravação.
