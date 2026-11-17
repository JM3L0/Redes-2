# Roteiro Mestre de Apresentação Individual (15 a 25 Minutos — Meta: 18 Minutos) — 3ª Avaliação (N3)

**Disciplina:** Redes de Computadores II (2026-2) — UFPI / CSHNB  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)  
**Pontuação na Rubrica (Eixo 4):** **30 Pontos** (Duração obrigatória: **entre 15 e 25 minutos**; ausência implica **Nota 0,0**).

> **Como usar este documento:** Este é o **único arquivo** que você precisa abrir para gravar o vídeo da 3ª Avaliação (N3). Ele foi planejado para **18 minutos** (com folga segura dentro do intervalo obrigatório de **15 a 25 minutos**), estruturado em 1ª pessoa do singular para apresentação individual e contém:
> 1. A preparação rápida do terminal antes de abrir o OBS;
> 2. O roteiro de falas conceitual e fluido dividido em 6 blocos;
> 3. Os blocos de comandos prontos para copiar e colar na hora exata da fala;
> 4. Todos os arquivos citados como **links clicáveis**;
> 5. O passo final de restauração e limpeza pós-gravação.

---

## 🛠️ PASSO 0: Preparação Rápida ANTES de Gravar (2 min antes no OBS)

Abra o **PowerShell** na pasta raiz do projeto (`c:\Users\jsous\Desktop\Redes 2\Avaliacao_3`) e rode este bloco **antes** de começar a gravar:

```powershell
# 1. Sobe os contêineres Docker da N3 em segundo plano
docker compose up -d

# 2. Cria backup dos dados oficiais (N=5) para proteger o dataset do relatório
if (Test-Path "data") { Copy-Item -Path "data" -Destination "data_backup_n3" -Recurse -Force }

# 3. Limpa o terminal para começar a gravação com a tela limpa
Clear-Host
```

---

## ⏱ Divisão do Tempo e Atalhos Rápidos (00:00 a 18:00 — Faixa Obrigatória: 15 a 25 min)

| Bloco | Tempo | Duração | Tópico da Apresentação | Arquivos Clicáveis para Mostrar na Tela |
| :---: | :---: | :---: | :--- | :--- |
| **Bloco 1** | 00:00 - 03:00 | 3m 00s | **Abertura e Fundamentação Teórica** | 📄 [sbc-template.pdf](../../relatorio/sbc-template.pdf) *(Págs. 1 e 2)* · [README.md](../../README.md) |
| **Bloco 2** | 03:00 - 06:00 | 3m 00s | **Arquitetura Docker e 3 Cenários `tc netem`** | 🐳 [docker-compose.yml](../../docker-compose.yml) · [Caddyfile](../../docker/Caddyfile) · [setup_netem.py](../../scripts/setup_netem.py) |
| **Bloco 3** | 06:00 - 09:00 | 3m 00s | **Automação (`run_n3.py`) e Matriz E01–E06** | 🐍 [run_n3.py](../../run_n3.py) · [run_n3.sh](../../run_n3.sh) · [process_data.py](../../analysis/process_data.py) · [plot_results.py](../../analysis/plot_results.py) |
| **Bloco 4** | 09:00 - 12:30 | 3m 30s | **Demonstração ao Vivo no Terminal** | ⚡ **Comandos de Terminal abaixo** (`iperf3` CUBIC vs BBR e `curl` HTTP/2 vs HTTP/3 1-RTT e 0-RTT) · [results.csv](../../data/raw/results.csv) |
| **Bloco 5** | 12:30 - 16:00 | 3m 30s | **Gráficos com Barras de Erro e Tabela Resumo** | 📊 [Gráfico 1 (Bloco A)](../../data/plots/fig1_bloco_a_vazao_cc.png) · [Gráfico 2 (Bloco B)](../../data/plots/fig2_bloco_b_ttfb_handshake.png) · [sbc-template.pdf](../../relatorio/sbc-template.pdf) *(Págs. 4 e 5)* |
| **Bloco 6** | 16:00 - 18:00 | 2m 00s | **Discussão Tanenbaum 6ª Ed. e Conclusão** | 🎯 [sbc-template.pdf](../../relatorio/sbc-template.pdf) *(Págs. 5, 6 e 1)* |

---

## 🎬 Roteiro Falado Minuto a Minuto com Comandos Integrados

---

### 📌 Bloco 1: Abertura e Objetivos Pedagógicos da N3 [00:00 - 03:00]
* **Clique para abrir na tela:** 📄 [sbc-template.pdf](../../relatorio/sbc-template.pdf) *(Página 1 e depois rolar até a Seção 2 na Página 2)* e [README.md](../../README.md).

* **Fala (00:00 - 01:30):**
  > *"Olá, professor! Tudo bem? Eu sou o **João Marcos Sousa Rufino Leal**, e esta é a apresentação do meu Trabalho Prático referente à Terceira Avaliação (N3) da disciplina de Redes de Computadores II, da UFPI — Campus de Picos.  
  > Nesta terceira avaliação, eu dei continuidade direta à bancada experimental com contêineres Docker e emulação de canal via Linux Traffic Control (`tc netem`), agora focando na análise empírica de dois mecanismos avançados da camada de transporte moderna:  
  > No **Bloco A**, eu confronto dois paradigmas opostos de controle de congestionamento no TCP usando fluxos contínuos de 15 segundos no `iperf3`: o **TCP CUBIC**, que é baseado em perda de pacotes, contra o **TCP BBR**, desenvolvido pelo Google, que é baseado em modelo do Produto Largura de Banda-Atraso (BDP).  
  > E no **Bloco B**, eu isolo a latência pura de estabelecimento de conexão e retomada de sessão usando o `curl` para transferir um objeto pequeno de 1 KB, comparando o **HTTPS com HTTP/2 sobre TCP+TLS 1.3**, o **HTTP/3 em conexão fria (Cold 1-RTT)** e o **HTTP/3 com retomada de sessão (Warm / 0-RTT)**."*

* **Fala (01:30 - 03:00):**
  > *(Ação: Rolar o [sbc-template.pdf](../../relatorio/sbc-template.pdf) até a Seção 2 de Fundamentação Teórica nas páginas 2 e 3).*  
  > *"Como eu destaco na fundamentação teórica do relatório baseada na 6ª edição do livro do Tanenbaum, esses dois blocos respondem a duas grandes questões práticas da engenharia de redes:  
  > A primeira questão — tratada nas **Seções 6.5.11 e 6.6.2 do Tanenbaum** — é: por que conexões TCP tradicionais perdem quase toda a sua velocidade em enlaces de longa distância quando existe uma pequena taxa de perda aleatória, como 2%? Isso acontece porque o **TCP CUBIC** interpreta qualquer pacote descartado como fila cheia no roteador e reduz sua janela de congestionamento (`cwnd`) multiplicativamente em 30% a cada perda. Já o **BBR** estima continuamente a banda real do gargalo ($BtlBw$) e o RTT mínimo ($RTprop$), mantendo o envio no ponto ótimo do BDP sem colapsar diante de perdas estocásticas.  
  > E a segunda questão — tratada na **Seção 6.6.1 do Tanenbaum** — é o custo dos RTTs de handshake: enquanto o HTTP/2 precisa primeiro abrir o TCP em 1 RTT e depois negociar o TLS 1.3 em mais 1 RTT antes de pedir o arquivo (totalizando 3 RTTs até o primeiro byte), o protocolo QUIC integra transporte e criptografia em apenas 1 RTT na primeira conexão (2 RTTs até o primeiro byte) e permite enviar a requisição já no primeiro pacote (0-RTT) nas conexões seguintes (apenas 1 RTT até o primeiro byte)."*

---

### 🏗 Bloco 2: Arquitetura Simplificada no Docker e os 3 Cenários `tc netem` [03:00 - 06:00]
* **Clique para abrir na tela:** 🐳 [docker-compose.yml](../../docker-compose.yml) · [Caddyfile](../../docker/Caddyfile) · [setup_netem.py](../../scripts/setup_netem.py).

* **Fala (03:00 - 04:30):**
  > *(Ação: Mostrar [docker-compose.yml](../../docker-compose.yml) e [Caddyfile](../../docker/Caddyfile)).*  
  > *"Seguindo a especificação da Seção 2 do edital, eu estruturei o [docker-compose.yml](../../docker-compose.yml) sobre a rede bridge isolada `net_bench` na sub-rede `172.20.0.0/16` com três contêineres:  
  > O primeiro é o `server_tcp_cc`, no IP `172.20.0.10`, rodando a imagem `networkstatic/iperf3` em modo servidor (`-s`), dedicado aos testes de vazão e retransmissões do Bloco A.  
  > O segundo é o `server_http3_quic`, no IP `172.20.0.30`, rodando o `caddy:2.7-alpine` com os certificados TLS 1.3 montados em `/etc/caddy/certs` e o diretório `/usr/share/caddy` servindo o arquivo estático de 1 KB (`1KB.bin`). Aqui no [Caddyfile](../../docker/Caddyfile), eu habilitei tanto o HTTP/2 sobre TCP quanto o HTTP/3 sobre QUIC/UDP na porta 443.  
  > E o terceiro é o contêiner cliente `client_bench`, no IP `172.20.0.50`, de onde são disparadas as chamadas padronizadas do `iperf3` e do `curl` com suporte nativo a `--http3`.  
  > Todos os contêineres possuem a permissão obrigatória `cap_add: NET_ADMIN`, permitindo que o Linux Traffic Control injete regras nas interfaces virtuais `eth0`."*

* **Fala (04:30 - 06:00):**
  > *(Ação: Mostrar [setup_netem.py](../../scripts/setup_netem.py) / [setup_netem.sh](../../scripts/setup_netem.sh)).*  
  > *"Aqui no módulo de emulação de rede ([setup_netem.py](../../scripts/setup_netem.py)), eu implementei os três cenários definidos na Seção 3 do edital, lembrando que o atraso unidirecional aplicado na interface corresponde à metade do RTT total desejado:  
  > O **Cenário 1 (LAN — Canal Ideal)** aplica `netem delay 0.5ms` sem perda, produzindo um RTT total de **1 milissegundo e 0% de perda**, usado no teste E01 para medir a capacidade máxima do TCP CUBIC.  
  > O **Cenário 2 (WAN — Canal Degradado)** aplica `netem delay 25ms loss 2%`, resultando em um RTT total de **50 milissegundos com 2% de perda estocástica de pacotes**, usado nos testes E02 e E03 para confrontar o TCP CUBIC contra o TCP BBR.  
  > E o **Cenário 3 (WAN sem Perda)** aplica `netem delay 25ms` com **0% de perda**, gerando um RTT puro de **50 milissegundos**, usado no Bloco B (testes E04, E05 e E06) para isolar perfeitamente o custo dos RTTs de handshake sem interferência de descartes aleatórios. Ao final de cada etapa, o script executa `tc qdisc del dev eth0 root` para limpar as interfaces."*

---

### 💻 Bloco 3: O Script de Automação (`run_n3`) e a Matriz de 6 Testes [06:00 - 09:00]
* **Clique para abrir na tela:** 🐍 [run_n3.py](../../run_n3.py) · [run_n3.sh](../../run_n3.sh) · [process_data.py](../../analysis/process_data.py) · [plot_results.py](../../analysis/plot_results.py).

* **Fala (06:00 - 07:30):**
  > *(Ação: Percorrer o código de [run_n3.py](../../run_n3.py)).*  
  > *"Para atender ao requisito de automação completa, eu desenvolvi o orquestrador [run_n3.py](../../run_n3.py) (e os wrappers [run_n3.sh](../../run_n3.sh) e [run_n3.ps1](../../run_n3.ps1)).  
  > Quando executado, ele gera os certificados TLS 1.3 com SANs válidos ([generate_certs.py](../../scripts/generate_certs.py)) e o objeto determinístico de 1 KB ([generate_payloads.py](../../scripts/generate_payloads.py)), sobe os contêineres, garante que os módulos `tcp_cubic` e `tcp_bbr` estão carregados no kernel Linux e executa a matriz de **6 testes essenciais (E01 a E06)** com as **5 repetições independentes por teste**.  
  > No **Bloco A**, antes de cada repetição de 15 segundos de E01, E02 e E03, o script limpa o cache de rota TCP (`ip route flush cache`) para evitar vício de `ssthresh` entre rodadas, executa `iperf3 -c 172.20.0.10 -t 15 -C cubic -J` (ou `-C bbr -J`), faz o parse do JSON e extrai a **vazão média em Mbps** e o **contador de retransmissões**."*

* **Fala (07:30 - 09:00):**
  > *(Ação: Mostrar a função `run_curl_block_b` em [run_n3.py](../../run_n3.py#L126) e depois [process_data.py](../../analysis/process_data.py) e [plot_results.py](../../analysis/plot_results.py)).*  
  > *"Na segunda metade do [run_n3.py](../../run_n3.py#L126), eu executo o **Bloco B** sob o Cenário 3 (WAN de 50 ms sem perda), medindo o `%{time_starttransfer}` (TTFB) no `curl` para o arquivo de 1 KB:  
  > No **E04**, o script mede o HTTPS com HTTP/2 sobre TCP+TLS 1.3.  
  > E nos testes **E05 (HTTP/3 Cold 1-RTT)** e **E06 (HTTP/3 Warm / Resumption)**, seguindo exatamente a dica da página 7 do edital, o script realiza requisições sequenciais na mesma chamada do `curl --http3-only`: a primeira requisição parte do zero e mede o handshake 1-RTT do QUIC (E05), enquanto a segunda requisição reaproveita a sessão estabelecida (0-RTT de espera de handshake), medindo o E06.  
  > Terminadas as 30 amostras, o script exporta `data/raw/results.csv` e `results.json`, limpa o `tc netem` e aciona [process_data.py](../../analysis/process_data.py) e [plot_results.py](../../analysis/plot_results.py) para gerar a Tabela Resumo e os 2 gráficos com barras de erro."*

---

### ⚡ Bloco 4: Demonstração Ao Vivo no Terminal [09:00 - 12:30]
* **Na tela:** Terminal PowerShell aberto ao lado do VS Code.

* **Fala (09:00 - 10:45):**
  > *"Vou demonstrar agora ao vivo no terminal o comportamento real dos dois blocos! Primeiro, vou aplicar o Cenário 2 (WAN: 50 ms de RTT e 2% de perda) e comparar o **TCP CUBIC (E02)** contra o **TCP BBR (E03)**:"*
  ```powershell
  # Aplicando Cenário 2 (WAN: 50ms RTT, 2% perda)
  python scripts/setup_netem.py wan_loss

  # Demonstração E02: TCP CUBIC sob 50ms RTT e 2% perda
  docker exec client_bench iperf3 -c 172.20.0.10 -t 5 -C cubic

  # Demonstração E03: TCP BBR sob os mesmos 50ms RTT e 2% perda
  docker exec client_bench iperf3 -c 172.20.0.10 -t 5 -C bbr
  ```
  > *"Vejam no terminal a diferença dramática: sob exatamente o mesmo canal com 50 ms de RTT e 2% de perda estocástica, o **TCP CUBIC** fica preso em torno de 2 a 3 Mbps porque sua janela `cwnd` colapsa a cada pacote descartado. Mudando apenas para `-C bbr`, o **TCP BBR** sustenta cerca de 300 Mbps — mais de 100 vezes a vazão do CUBIC — porque mantém a janela dimensionada pelo BDP estimado!"*

* **Fala (10:45 - 12:30):**
  > *"Agora vou demonstrar ao vivo o **Bloco B**: aplico o Cenário 3 (WAN: 50 ms de RTT e 0% de perda) e comparo o TTFB (`time_starttransfer`) para o objeto de 1 KB entre o HTTP/2 (E04), o HTTP/3 Cold 1-RTT (E05) e o HTTP/3 Warm/Resumed 0-RTT (E06):"*
  ```powershell
  # Aplicando Cenário 3 (WAN sem perda: 50ms RTT, 0% perda)
  python scripts/setup_netem.py wan_noloss

  # E04: HTTPS (HTTP/2 sobre TCP + TLS 1.3) -> ~3 RTTs (~163 ms)
  docker exec client_bench curl -k --http2 -o /dev/null -s -w "E04 HTTP/2 TTFB: %{time_starttransfer}s`n" https://172.20.0.30/1KB.bin

  # E05 (1ª req HTTP/3 Cold -> ~2 RTTs ~112 ms) vs E06 (2ª req HTTP/3 Warm/Resumption -> ~1 RTT ~61 ms)
  docker exec client_bench curl -k --http3-only -s -w "Req HTTP/3 TTFB: %{time_starttransfer}s`n" -o /dev/null https://172.20.0.30/1KB.bin -o /dev/null https://172.20.0.30/1KB.bin

  # Limpando as interfaces tc netem
  python scripts/setup_netem.py clean
  ```
  > *"Olhem que resultado preciso no terminal:  
  > No **E04 (HTTP/2)**, o TTFB deu cerca de **0.163s (~163 ms)**, correspondente a 3 RTTs de 50 ms mais o processamento.  
  > Na primeira requisição **HTTP/3 Cold (E05)**, o TTFB caiu para **0.112s (~112 ms)** — economizando exatos 50 ms (1 RTT) graças ao handshake integrado do QUIC.  
  > E na segunda requisição sequencial **HTTP/3 Warm/Resumption (E06)**, o TTFB caiu para **0.061s (~61 ms)** — apenas 1 RTT, eliminando totalmente a espera do handshake!  
  > E aqui em [data/raw/results.csv](../../data/raw/results.csv) e [data/raw/results.json](../../data/raw/results.json) estão todas as 30 amostras oficiais coletadas."*

---

### 📊 Bloco 5: Gráficos com Barras de Erro e Tabela Resumo [12:30 - 16:00]
* **Clique para abrir na tela:** 📊 [fig1_bloco_a_vazao_cc.png](../../data/plots/fig1_bloco_a_vazao_cc.png) · [fig2_bloco_b_ttfb_handshake.png](../../data/plots/fig2_bloco_b_ttfb_handshake.png) · [sbc-template.pdf](../../relatorio/sbc-template.pdf) *(Páginas 4 e 5)*.

* **Fala (12:30 - 14:15):**
  > *(Ação: Abrir o **Gráfico 1** [fig1_bloco_a_vazao_cc.png](../../data/plots/fig1_bloco_a_vazao_cc.png) e a Tabela 1 na página 4 do PDF).*  
  > *"Passando para os gráficos e para a Tabela Resumo do relatório, vemos aqui no **Gráfico 1 (Bloco A)** a vazão média em Mbps com as **barras de erro representando o desvio padrão ($s$)** das 5 repetições:  
  > No painel (a), o teste **E01 (TCP CUBIC na LAN de 1 ms e 0% de perda)** atingiu **21945,80 ± 2486,81 Mbps** (~21,95 Gbps na bridge virtual), estabelecendo o nosso baseline de capacidade máxima.  
  > Já no painel (b), que destaca o cenário WAN degradado (50 ms de RTT e 2% de perda), vemos o contraste direto entre o **E02 (TCP CUBIC)**, que colapsou para **2,63 ± 0,56 Mbps**, e o **E03 (TCP BBR)**, que alcançou **303,13 ± 18,87 Mbps** — um ganho de **115,3 vezes** na vazão média!  
  > Além disso, na Tabela 1 do relatório, eu explico o **Total de Retransmissões**: o CUBIC teve apenas **390 retransmissões totais** porque ficou paralisado transmitindo apenas ~24,7 MB nas 5 rodadas; já o BBR registrou **39095 retransmissões** justamente porque transferiu cerca de **2,84 GB** sob um canal que descarta fisicamente 2% dos pacotes, retransmitindo os segmentos perdidos sem deixar o enlace ocioso."*

* **Fala (14:15 - 16:00):**
  > *(Ação: Abrir o **Gráfico 2** [fig2_bloco_b_ttfb_handshake.png](../../data/plots/fig2_bloco_b_ttfb_handshake.png)).*  
  > *"E aqui no **Gráfico 2 (Bloco B)** — também com as barras de erro de desvio padrão amostral —, temos a comparação do TTFB médio para o objeto de 1 KB na WAN de 50 ms sem perda:  
  > No **E04 (HTTPS / HTTP/2 sobre TCP+TLS 1.3)**, o TTFB médio foi de **163,57 ± 2,73 ms** (3 RTTs = 150 ms de propagação + 13,57 ms de processamento).  
  > No **E05 (HTTP/3 Cold 1-RTT)**, o TTFB médio caiu para **112,36 ± 0,99 ms** (2 RTTs = 100 ms de propagação + 12,36 ms de processamento), uma redução exata de **51,21 ms (1 RTT)**.  
  > E no **E06 (HTTP/3 Warm / Session Resumption 0-RTT)**, o TTFB médio caiu para **61,46 ± 0,95 ms** (1 RTT = 50 ms de propagação + 11,46 ms de processamento), reduzindo mais **50,90 ms (1 RTT)** e totalizando **102,11 ms (2 RTTs ou 62,4%)** de economia em relação ao HTTP/2."*

---

### 🎯 Bloco 6: Articulação Teórica (Tanenbaum 6ª Ed.) e Conclusão [16:00 - 18:00]
* **Clique para abrir na tela:** 📄 [sbc-template.pdf](../../relatorio/sbc-template.pdf) *(Páginas 5, 6 e retorno à Página 1)*.

* **Fala (16:00 - 18:00):**
  > *(Ação: Mostrar as páginas 5, 6 e 1 do [sbc-template.pdf](../../relatorio/sbc-template.pdf)).*  
  > *"Concluindo a apresentação, todos esses resultados estão rigorosamente fundamentados no relatório técnico de **6 páginas** no formato oficial da **SBRC**, articulando a **Seção 6.5.11 (TCP CUBIC)**, a **Seção 6.6.2 (BBR)** e a **Seção 6.6.1 (QUIC)** da 6ª edição de Redes de Computadores do Tanenbaum.  
  > Na primeira página do PDF está inserido o link deste vídeo no YouTube, e todo o repositório de código, scripts de automação e dados brutos está empacotado no arquivo `.zip` padronizado para submissão no SIGAA.  
  > Muito obrigado pela atenção, professor, e até mais!"*

---

## 🧹 PASSO FINAL (APÓS PARAR A GRAVAÇÃO NO OBS)

```powershell
# Restaura o backup oficial dos dados e desliga os contêineres Docker
if (Test-Path "data_backup_n3") {
    Copy-Item -Path "data_backup_n3\*" -Destination "data" -Recurse -Force
    Remove-Item -Path "data_backup_n3" -Recurse -Force
}
python scripts/setup_netem.py clean
docker compose down
```
