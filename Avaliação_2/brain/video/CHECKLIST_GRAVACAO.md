# 🎬 Checklist de Gravação do Vídeo Técnico (15 Minutos — Direto no Código e no Relatório PDF)
## Estudo Experimental de Desempenho de Protocolos Web (HTTP/1.1 vs HTTPS/TLS 1.3 vs HTTP/3-QUIC)
**Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)**  
**Equipe:** João Marcos Sousa Rufino Leal & Marcos Willian de Sousa e Silva  
**Disciplina:** Redes de Computadores II (2026-2)  

> **Instrução de Uso:** Deixe abertos no computador apenas o **VS Code** (com a pasta do projeto), o **Terminal PowerShell** e o **Relatório PDF (`relatorio/sbc-template.pdf`)**. Mantenha este checklist em um segundo monitor ou celular para ir marcando cada item mostrado na tela.

---

### ⏱ Visão de Tempo e Cronograma
- **Tempo Total Obrigatório:** **15 minutos** (janela ideal: **14:45 a 15:05**).
- **Divisão da Dupla:** ~7m30s de fala para João Marcos e ~7m30s para Marcos Willian.
- **Resolução de Gravação:** 1080p (1920x1080), 30 ou 60 FPS no OBS Studio.

---

### 📋 Checklist de Itens Obrigatórios por Bloco

#### 🟢 Bloco 1: Abertura e Objetivos [00:00 - 02:00] (~2 min)
- [ ] **Na Tela:** Abrir o **Relatório PDF (`relatorio/sbc-template.pdf`) na Página 1 e Página 2** (ou o `README.md` na raiz), mostrando o título oficial, UFPI/CSHNB, nomes e e-mails da dupla, Resumo/Abstract e a **Seção 1 (Introdução)** + **Tabela 1 (Síntese Arquitetural dos Protocolos)**.
- [ ] **Apresentação verbal da equipe:** João Marcos e Marcos Willian se apresentam com nome completo.
- [ ] **Objetivo 1 (apontar na Seção 1 / Tabela 1 do PDF):** Overhead de handshakes e latência inicial no Time to First Byte (1 RTT TCP vs 2 RTTs HTTPS/TLS 1.3 vs 1 RTT integrado QUIC/UDP).
- [ ] **Objetivo 2 (apontar na Tabela 1 do PDF):** Bloqueio de Início de Linha (*Head-of-Line Blocking*) na aplicação (HTTP/1.1), transferido para o transporte TCP (HTTP/2) e eliminado completamente no HTTP/3 via streams UDP independentes.
- [ ] **Objetivo 3:** Efeito das condições de canal móvel/WAN (50ms de RTT e 2% de perda estocástica) comparando TCP CUBIC vs QUIC.

---

#### 🟢 Bloco 2: Arquitetura Docker e Emulação `tc netem` [02:00 - 04:30] (~2m30s)
- [ ] **Na Tela (VS Code):** Abrir `docker/docker-compose.yml`:
  - [ ] Apontar a rede bridge isolada `net_bench` (sub-rede `172.20.0.0/16`).
  - [ ] Apontar o Servidor 1: `server_http11` (IP `172.20.0.10`, porta `8080`, NGINX Alpine, HTTP/1.1 texto claro) e mostrar rapidamente `docker/server-http1/nginx.conf`.
  - [ ] Apontar o Servidor 2: `server_http2_tls` (IP `172.20.0.20`, porta `8443`, NGINX Alpine, HTTP/2 + TLS 1.3) e mostrar `docker/server-http2/nginx.conf` (`listen 443 ssl http2; ssl_protocols TLSv1.3`).
  - [ ] Apontar o Servidor 3: `server_http3_quic` (IP `172.20.0.30`, porta `9443` TCP e UDP, Caddy 2.7 Alpine, HTTP/3 QUIC) e mostrar `docker/server-http3/Caddyfile`.
- [ ] **Enfatizar o privilégio de kernel obrigatório no `docker-compose.yml`:**
  - [ ] Selecionar com o mouse a linha `cap_add: - NET_ADMIN` em cada serviço e explicar que sem isso o `tc` falha com erro `RTNETLINK answers: Operation not permitted`.
- [ ] **Na Tela (VS Code):** Abrir `scripts/setup_netem.ps1` (ou `scripts/setup_netem.sh`):
  - [ ] Apontar o Cenário 1 (LAN): atraso unidirecional de `0.5ms` (`delay 0.5ms`, RTT final = `1.0ms`, perda 0%).
  - [ ] Apontar o Cenário 2 (WAN): atraso unidirecional de `25ms` (`delay 25ms loss 2%`, RTT final = `50ms` e 2% de perda).
  - [ ] Apontar a função `clean_qdisc`: restauração limpa com `tc qdisc del dev eth0 root`.

---

#### 🟢 Bloco 3: Cliente Python e Controle de Viés [04:30 - 07:30] (~3 min)
- [ ] **Na Tela (VS Code):** Abrir `benchmark/session_control.py`:
  - [ ] Mostrar `get_no_cache_headers()` desativando qualquer cache (`Cache-Control: no-cache, no-store, must-revalidate`).
  - [ ] Explicar `SessionMode.COLD` vs `SessionMode.WARM` (controle de viés que evita a penalidade de -10 pontos).
- [ ] **Na Tela (VS Code):** Abrir `benchmark/client.py`:
  - [ ] Mostrar os imports assíncronos (`asyncio`, `httpx`, `aioquic`) e a classe `H3BenchmarkProtocol` (linhas 25–115).
  - [ ] Mostrar o **Modo Cold TTFB** (`fetch_httpx_cold` e `fetch_h3_cold`, linhas 128–215): destacar o fechamento explícito da sessão (`async with httpx.AsyncClient(...)` / `await client.aclose()`) antes de CADA requisição individual para medir o handshake real sem reuso de conexão.
  - [ ] Mostrar o **Modo Warm Concurrency** (`fetch_httpx_warm_batch` e `fetch_h3_warm_batch`, linhas 220–345): destacar que abre **uma única conexão persistente**, faz 1 requisição de aquecimento do handshake e depois dispara os **100 objetos de 10 KB simultaneamente** com `asyncio.gather(*tasks)`.
  - [ ] Mostrar a matriz dos 12 testes `TEST_DEFINITIONS` (`T01` a `T12`, linhas 350–380): Carga A (`50MB.bin`) e Carga B (`100x10KB`).
- [ ] **Na Tela (VS Code):** Abrir rapidamente `benchmark/metrics.py`:
  - [ ] Mostrar `RequestMetric` e a exportação para `results.json` e `results.csv` com `time.perf_counter()`.

---

#### 🟢 Bloco 4: Demonstração Experimental ao Vivo (1-Click Run) [07:30 - 10:30] (~3 min)
- [ ] **Na Tela (VS Code):** Mostrar rapidamente `run_experiments.ps1` e `run_experiments.sh` (mostrando que o projeto inteiro roda com 1 único comando, evitando a penalidade de -15 pontos).
- [ ] **Na Tela (Terminal PowerShell):** Seguir os comandos de [`GUIA_EXECUCAO_AO_VIVO.md`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliação_2/brain/video/GUIA_EXECUCAO_AO_VIVO.md):
  - [ ] Mostrar os 3 contêineres rodando (`docker ps`).
  - [ ] Aplicar `.\scripts\setup_netem.ps1 lan` e mostrar o status `delay 500.0us` nos 3 servidores.
  - [ ] Rodar testes rápidos na LAN (`T01`, `T02`, `T09`) mostrando a saída em tempo real.
  - [ ] Aplicar `.\scripts\setup_netem.ps1 wan` (`delay 25.0ms loss 2%`).
  - [ ] Rodar ao vivo `T10` (HTTP/1.1), `T11` (HTTP/2) e `T12` (HTTP/3) na WAN, destacando no terminal o HTTP/3 terminando os 100 objetos em **~1,1s (~87 RPS)** contra **~3,2s (~31 RPS)** do HTTP/2 e **~4,8s (~20 RPS)** do HTTP/1.1.
  - [ ] Limpar a interface com `.\scripts\setup_netem.ps1 clean` e rodar `python analysis\process_data.py` e `python analysis\plot_results.py`.
- [ ] **Na Tela (VS Code):** Abrir rapidamente `data/raw/results.csv` e `data/processed/summary_table.csv` para provar os dados exportados.

---

#### 🟢 Bloco 5: Resultados e Fundamentação em Tanenbaum no Relatório PDF [10:30 - 13:30] (~3 min)
- [ ] **Na Tela:** Abrir o **Relatório PDF (`relatorio/sbc-template.pdf`) na Seção 4 (Páginas 4 a 8)** (ou abrir as imagens de `data/plots/` junto com o PDF):
- [ ] **Mostrar a Tabela 2 do PDF (Página 4 — Consolidação Estatística T01 a T12):**
  - [ ] Destacar que todos os 12 testes têm Média, Desvio Padrão, Mediana (p50), Cauda Longa (p99), Goodput e RPS para $N=10$ repetições.
- [ ] **Mostrar a Figura 1 do PDF (Página 5 — Cold TTFB, `fig1_ttfb_cold_comparison.png`):**
  - [ ] Apontar as **barras de erro obrigatórias** (IC 95%).
  - [ ] Comparar LAN: HTTP/1.1 (28.7ms) vs HTTPS (50.2ms) vs HTTP/3 (7.7ms).
  - [ ] Comparar WAN (50ms RTT): HTTPS leva 118.4ms (~2 RTTs + TLS) vs HTTP/3 com 54.2ms (1 RTT unificado QUIC).
- [ ] **Mostrar a Figura 2 e Equações (1) e (2) do PDF (Páginas 5 e 6 — Carga A 50 MB e Seção 4.2):**
  - [ ] Apontar o colapso do TCP CUBIC sob 2% de perda: de 330.09 Mbps (T01) e 151.53 Mbps (T02) na LAN para **4.95 Mbps (T04)** e **4.70 Mbps (T05)** na WAN (queda de 98.5%).
  - [ ] Explicar por que na LAN o TCP (330 Mbps) é maior que o HTTP/3 (22.59 Mbps): TCP roda no kernel Linux com *zero-copy*/TSO, enquanto `aioquic` roda em espaço de usuário em Python; mas na WAN com perdas, o HTTP/3 mantém **17.38 Mbps** (3,7× maior que o HTTPS/2).
  - [ ] **Apontar no PDF a Citação Teórica Obrigatória — Tanenbaum Seção 6.5.11 (TCP CUBIC):**
    - [ ] Mostrar a Seção 4.2 na página 6 do PDF e explicar de forma conceitual: o TCP CUBIC trata qualquer pacote perdido como congestionamento e corta drasticamente sua janela de transmissão; como na WAN há perdas o tempo todo, a janela é cortada repetidas vezes antes de conseguir crescer de novo, derrubando a velocidade.
- [ ] **Mostrar as Figuras 3, 4 e 5 do PDF (Páginas 7 e 8 — Carga B 100 Objetos e Seção 4.3):**
  - [ ] Apontar na Figura 3 e Figura 4: na WAN, o HTTP/3 entrega quase o triplo de requisições por segundo em comparação ao HTTP/2.
  - [ ] **Apontar no PDF a Citação Teórica Obrigatória — Tanenbaum Seções 6.6.1 (QUIC) e 6.6.2 (BBR):**
    - [ ] Explicar de forma conceitual o fim do *Head-of-Line Blocking*: no HTTP/2 um pacote perdido trava todos os 100 arquivos na mesma fila do TCP, enquanto no HTTP/3 sobre QUIC cada arquivo tem seu próprio fluxo UDP (só o arquivo que sofreu perda espera retransmissão, e os outros 99 passam direto).
    - [ ] Mencionar que o controle de congestionamento moderno do QUIC/BBR (Seção 6.6.2) controla o ritmo de envio medindo a banda e a latência real sem entrar em pânico a cada perda isolada.
  - [ ] Apontar a **Figura 5 (Página 8 — Curva CDF de Latência com Barras de Erro)**: mostrar visualmente que a linha verde do HTTP/3 sobe reta logo no início (baixa latência mesmo nos piores casos, p99), enquanto as linhas do HTTP/2 e HTTP/1.1 se esticam para a direita por causa das travadas de fila do TCP.

---

#### 🟢 Bloco 6: Conclusões e Encerramento no Relatório PDF [13:30 - 15:00] (~1m30s)
- [ ] **Na Tela:** Mostrar a **Seção 5 (Considerações Finais) e as Referências Bibliográficas (Páginas 8 e 9)** do `relatorio/sbc-template.pdf`.
- [ ] **Síntese dos achados:** TCP em kernel é excelente em redes locais sem perdas (LAN), mas o HTTP/3 sobre QUIC é indispensável em redes geograficamente distribuídas ou móveis (WAN) sujeitas a latência e perda de pacotes.
- [ ] **Voltar à Página 1 do PDF:** Mostrar onde ficará o link público do vídeo no cabeçalho do artigo SBC antes da submissão do `.zip` no SIGAA.
- [ ] **Agradecimento final:** Agradecer ao professor e encerrar a gravação.

---

### ⚠️ Armadilhas Fatais para Evitar no Vídeo
1. **NÃO esqueça de falar em voz alta os números das seções do Tanenbaum (6.5.11, 6.6.1 e 6.6.2):** Mostre as equações na página 6 do PDF e fale os números das seções (vale até 20 pontos na rubrica).
2. **NÃO passe pelos gráficos sem apontar as barras de erro:** Destaque com o cursor do mouse as barras de erro ($IC_{95\%}$ e desvio padrão) nas Figuras 1 a 5 do PDF (vale 10 pontos).
3. **NÃO deixe de mostrar o `client.aclose()` no código (`benchmark/client.py`):** Mostre a linha exata onde a sessão é fechada no Cold TTFB e mantida aberta na Carga B (vale 10 pontos).
4. **NÃO passe de 15 minutos nem grave menos de 14 minutos:** Mantenha o cronômetro visível.
