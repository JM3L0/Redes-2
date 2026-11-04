# Roteiro de Apresentação em Dupla (15 Minutos — Fluido, Natural e Conceitual)

**Disciplina:** Redes de Computadores II (2026-2) — UFPI / CSHNB  
**Equipe:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`) & Marcos Willian de Sousa e Silva (`marcos.sousa@ufpi.edu.br`)  

> **Dica de Apresentação:** Todos os arquivos citados neste roteiro são **links clicáveis** (`Ctrl + Clique` no editor ou clique direto no Preview do Markdown) para você abrir cada arquivo na hora exata durante a gravação.

---

## ⏱ Divisão do Tempo e Atalhos Rápidos (00:00 a 15:00)

| Bloco | Tempo | Duração | Quem fala | Arquivos Clicáveis para Mostrar na Tela |
| :---: | :---: | :---: | :---: | :--- |
| **Bloco 1** | 00:00 - 02:00 | 2m 00s | **João Marcos & Marcos Willian** | 📄 [sbc-template.pdf](../../relatorio/sbc-template.pdf) *(Págs. 1 e 2)* · [README.md](../../README.md) |
| **Bloco 2** | 02:00 - 04:30 | 2m 30s | **Marcos Willian & João Marcos** | 🐳 [docker-compose.yml](../../docker/docker-compose.yml) · [nginx.conf (H1)](../../docker/server-http1/nginx.conf) · [nginx.conf (H2)](../../docker/server-http2/nginx.conf) · [Caddyfile (H3)](../../docker/server-http3/Caddyfile) · [setup_netem.ps1](../../scripts/setup_netem.ps1) |
| **Bloco 3** | 04:30 - 07:30 | 3m 00s | **João Marcos & Marcos Willian** | 🐍 [client.py](../../benchmark/client.py) · [session_control.py](../../benchmark/session_control.py) · [metrics.py](../../benchmark/metrics.py) |
| **Bloco 4** | 07:30 - 10:30 | 3m 00s | **João Marcos & Marcos Willian** | ⚡ [run_experiments.ps1](../../run_experiments.ps1) · [run_experiments.sh](../../run_experiments.sh) · [GUIA_EXECUCAO_AO_VIVO.md](GUIA_EXECUCAO_AO_VIVO.md) · [results.csv](../../data/raw/results.csv) · [summary_table.csv](../../data/processed/summary_table.csv) |
| **Bloco 5** | 10:30 - 13:30 | 3m 00s | **Marcos Willian & João Marcos** | 📊 [sbc-template.pdf](../../relatorio/sbc-template.pdf) *(Págs. 4 a 8)* · [Fig 1 (TTFB)](../../data/plots/fig1_ttfb_cold_comparison.png) · [Fig 2 (Throughput)](../../data/plots/fig2_throughput_carga_a.png) · [Fig 3 (Load B)](../../data/plots/fig3_load_time_carga_b.png) · [Fig 4 (RPS WAN)](../../data/plots/fig4_rps_carga_b_wan.png) · [Fig 5 (CDF)](../../data/plots/fig5_cdf_latency_distribution.png) |
| **Bloco 6** | 13:30 - 15:00 | 1m 30s | **Marcos Willian & João Marcos** | 🎯 [sbc-template.pdf](../../relatorio/sbc-template.pdf) *(Págs. 8, 9 e 1)* · [relatorio.bib](../../relatorio/relatorio.bib) |

---

## 🎬 Roteiro Falado Minuto a Minuto

---

### 📌 Bloco 1: Abertura e Ideia Geral do Trabalho [00:00 - 02:00]
* **Clique para abrir na tela:** 📄 [sbc-template.pdf](../../relatorio/sbc-template.pdf) *(abrir na Página 1 e depois rolar até a Tabela 1 na Página 2)* ou [README.md](../../README.md).

* **Fala — João Marcos (00:00 - 00:50):**
  > *"Olá, pessoal! Tudo bem? Essa é a apresentação do nosso Trabalho Prático da segunda avaliação de Redes de Computadores II, da UFPI de Picos.  
  > Eu sou o **João Marcos**, e estou fazendo esse trabalho em dupla com o **Marcos Willian**.  
  > A proposta do nosso projeto foi colocar frente a frente as três gerações de protocolos da Web — o HTTP/1.1 puro sobre TCP, o HTTP/2 com segurança TLS 1.3 e o HTTP/3 que roda sobre o protocolo QUIC em cima de UDP — usando um ambiente controlado no Docker e um cliente de testes que nós mesmos construímos em Python."*

* **Fala — Marcos Willian (00:50 - 02:00):**
  > *(Ação: Rolar o [sbc-template.pdf](../../relatorio/sbc-template.pdf) para a **Tabela 1** na página 2).*  
  > *"Olhando aqui para a Tabela 1 do nosso relatório, a gente resume bem as três grandes perguntas que queríamos responder na prática:  
  > A primeira é sobre **o tempo para abrir a conexão (o handshake)**: no TCP puro a gente gasta uma viagem de ida e volta (1 RTT); quando coloca o TLS 1.3 em cima do TCP, como no HTTP/2, são duas viagens antes de começar a baixar o arquivo; já o HTTP/3 com QUIC junta o transporte e a criptografia em uma viagem só sobre o UDP.  
  > A segunda pergunta é sobre o famoso **Bloqueio de Início de Linha (o Head-of-Line Blocking)**: no HTTP/1.1, uma requisição trava a fila na camada de aplicação. O HTTP/2 resolveu isso na aplicação multiplexando vários arquivos na mesma conexão, mas continuou preso ao TCP: se um único pacote se perde na rede, o TCP trava a entrega de todos os arquivos ao mesmo tempo esperando a retransmissão. Já o HTTP/3 resolve isso de vez criando fluxos independentes no UDP.  
  > E a terceira pergunta é ver **como cada protocolo reage quando a rede fica ruim**, comparando uma rede local perfeita com uma rede de longa distância que tem atraso e perda de pacotes."*

---

### 🏗 Bloco 2: Infraestrutura no Docker e Emulação de Rede [02:00 - 04:30]
* **Clique para abrir na tela:**
  1. 🐳 [docker-compose.yml](../../docker/docker-compose.yml)
  2. ⚙️ [server-http1/nginx.conf](../../docker/server-http1/nginx.conf) · [server-http2/nginx.conf](../../docker/server-http2/nginx.conf) · [server-http3/Caddyfile](../../docker/server-http3/Caddyfile)
  3. 🌐 [setup_netem.ps1](../../scripts/setup_netem.ps1) *(ou [setup_netem.sh](../../scripts/setup_netem.sh))*

* **Fala — Marcos Willian (02:00 - 03:15):**
  > *(Ação: Clicar em [docker-compose.yml](../../docker/docker-compose.yml) e passar rapidamente por [server-http1/nginx.conf](../../docker/server-http1/nginx.conf), [server-http2/nginx.conf](../../docker/server-http2/nginx.conf) e [server-http3/Caddyfile](../../docker/server-http3/Caddyfile)).*  
  > *"Para que o nosso teste não sofresse interferência da nossa internet de casa ou de variações do computador, nós isolamos os três servidores dentro de uma rede virtual do Docker.  
  > Aqui no [docker-compose.yml](../../docker/docker-compose.yml), nós subimos três contêineres separados:  
  > O primeiro usa o NGINX ([server-http1/nginx.conf](../../docker/server-http1/nginx.conf)) servindo HTTP/1.1 em texto claro, sem criptografia, para servir como nossa base de comparação do TCP.  
  > O segundo também usa NGINX ([server-http2/nginx.conf](../../docker/server-http2/nginx.conf)), mas configurado com HTTP/2 e criptografia TLS 1.3 usando certificados digitais gerados localmente para o nosso ambiente ([generate_certs.py](../../scripts/generate_certs.py)).  
  > E o terceiro servidor usa o Caddy ([server-http3/Caddyfile](../../docker/server-http3/Caddyfile)), que já tem suporte nativo e maduro ao HTTP/3 sobre QUIC, escutando na porta UDP para receber os datagramas do cliente."*

* **Fala — João Marcos (03:15 - 04:30):**
  > *(Ação: Apontar `cap_add: - NET_ADMIN` no [docker-compose.yml](../../docker/docker-compose.yml#L7-L8) e depois clicar em [setup_netem.ps1](../../scripts/setup_netem.ps1)).*  
  > *"Aqui no [docker-compose.yml](../../docker/docker-compose.yml#L7-L8) tem um detalhe muito importante exigido na especificação, que é essa permissão `cap_add: NET_ADMIN` em todos os contêineres. Como os contêineres são isolados por padrão, sem essa permissão o Linux bloqueia qualquer comando que tente alterar o atraso ou a perda da placa de rede virtual.  
  > Com essa permissão ativa, nós usamos esse script [setup_netem.ps1](../../scripts/setup_netem.ps1) (e a versão Linux [setup_netem.sh](../../scripts/setup_netem.sh)) para simular dois cenários direto na interface de rede dos servidores usando o utilitário `tc netem`:  
  > Primeiro, o **Cenário LAN**, que simula uma rede local ideal, com tempo de ida e volta de apenas 1 milissegundo e nenhuma perda de pacotes.  
  > Segundo, o **Cenário WAN**, que simula uma conexão longa ou rede móvel degradada, aplicando 50 milissegundos de tempo de ida e volta e uma taxa de perda aleatória de pacotes. Além disso, o script tem o comando `clean`, que limpa todas as regras ao final da bateria para deixar a rede restaurada."*

---

### 💻 Bloco 3: O Cliente em Python e o Controle de Sessão [04:30 - 07:30]
* **Clique para abrir na tela:**
  1. 🐍 [client.py](../../benchmark/client.py)
  2. 📊 [metrics.py](../../benchmark/metrics.py)
  3. 🔒 [session_control.py](../../benchmark/session_control.py)
  4. ❄️ [client.py — Funções Cold TTFB (linha 128)](../../benchmark/client.py#L128)
  5. 🔥 [client.py — Funções Warm Concurrency (linha 225)](../../benchmark/client.py#L225)

* **Fala — João Marcos (04:30 - 06:00):**
  > *(Ação: Clicar em [client.py](../../benchmark/client.py#L29) e depois em [metrics.py](../../benchmark/metrics.py)).*  
  > *"Passando para o código do cliente em [benchmark/client.py](../../benchmark/client.py), nós não poderíamos usar um navegador comum porque o navegador faz cache e reaproveita conexões por conta própria, o que estragaria a medição.  
  > Por isso, escrevemos o cliente inteiro em Python assíncrono: usamos a biblioteca `httpx` para conversar com os servidores HTTP/1.1 e HTTP/2, e a biblioteca `aioquic` para implementar a comunicação HTTP/3 sobre QUIC.  
  > Nós testamos dois tipos de carga gerados pelo script [generate_payloads.py](../../scripts/generate_payloads.py): a **Carga A**, que é o download de um arquivo único grande de 50 Mega para ver a velocidade sustentada de transferência; e a **Carga B**, que dispara o download de 100 arquivos pequenos de 10 KB ao mesmo tempo para testar a multiplexação. Tudo isso é cronometrado com alta precisão em [benchmark/metrics.py](../../benchmark/metrics.py) e salvo automaticamente nos arquivos [results.json](../../data/raw/results.json) e [results.csv](../../data/raw/results.csv)."*

* **Fala — Marcos Willian (06:00 - 07:30):**
  > *(Ação: Clicar em [session_control.py](../../benchmark/session_control.py) e depois clicar em [client.py (Cold TTFB — linha 128)](../../benchmark/client.py#L128) e [client.py (Warm — linha 225)](../../benchmark/client.py#L225)).*  
  > *"E aqui em [session_control.py](../../benchmark/session_control.py) e nas funções de coleta do [client.py](../../benchmark/client.py#L128) está o cuidado mais importante do código, que é o **controle de viés de sessão**:  
  > Primeiro, nós mandamos cabeçalhos em todas as requisições proibindo qualquer tipo de cache.  
  > Segundo, quando queremos medir o **Cold TTFB** — que é o tempo até chegar o primeiro byte partindo do zero —, o nosso código ([fetch_httpx_cold](../../benchmark/client.py#L128) e [fetch_h3_cold](../../benchmark/client.py#L173)) fecha explicitamente o cliente com `client.aclose()` antes de cada requisição. Assim a gente obriga o protocolo a fazer todo o handshake de novo, sem trapacear reaproveitando uma conexão que já estava aberta.  
  > Já no teste da **Carga B com os 100 arquivos pequenos**, nós fazemos o oposto de propósito: usamos o modo **Warm Connection** ([fetch_httpx_warm_batch](../../benchmark/client.py#L225) e [fetch_h3_warm_batch](../../benchmark/client.py#L285)), onde abrimos uma única conexão, aquecemos o canal e disparamos os 100 pedidos simultâneos dentro dessa mesma sessão. É isso que permite ver na prática como o HTTP/2 e o HTTP/3 multiplexam vários arquivos num único canal."*

---

### 🧪 Bloco 4: Demonstração Executando Ao Vivo no Terminal [07:30 - 10:30]
* **Clique para abrir na tela:**
  1. ⚡ [run_experiments.ps1](../../run_experiments.ps1) e [run_experiments.sh](../../run_experiments.sh)
  2. 📋 [GUIA_EXECUCAO_AO_VIVO.md](GUIA_EXECUCAO_AO_VIVO.md) *(com os comandos prontos para colar no Terminal PowerShell)*
  3. 📁 Ao terminar, clicar em [results.csv](../../data/raw/results.csv) e [summary_table.csv](../../data/processed/summary_table.csv)

* **Fala — João Marcos (07:30 - 08:45):**
  > *(Ação: Clicar em [run_experiments.ps1](../../run_experiments.ps1) / [run_experiments.sh](../../run_experiments.sh) e depois ir para o Terminal PowerShell).*  
  > *"Aqui na raiz temos o script [run_experiments.ps1](../../run_experiments.ps1) (e [run_experiments.sh](../../run_experiments.sh)), que automatiza todo o experimento com um único comando: ele sobe os contêineres, aplica os cenários de rede, roda os 12 testes da matriz, processa as estatísticas, plota os gráficos e desliga o ambiente.  
  > Aqui no terminal, nossos três contêineres já estão rodando. Vamos aplicar agora ao vivo o **Cenário 1 (LAN)** com o `setup_netem` e rodar os testes de rede local."*  
  > *(Ação no Terminal: Rodar `.\scripts\setup_netem.ps1 lan` e em seguida os testes de LAN do [GUIA_EXECUCAO_AO_VIVO.md](GUIA_EXECUCAO_AO_VIVO.md)).*  
  > *"Vejam que a regra de rede local já foi injetada nos três servidores e os testes rodam super rápido: na rede local sem perdas, tanto o arquivo de 50 Mega quanto o lote de 100 arquivos terminam quase instantaneamente."*

* **Fala — Marcos Willian (08:45 - 10:30):**
  > *(Ação no Terminal: Rodar `.\scripts\setup_netem.ps1 wan` e depois `T10`, `T11` e `T12` na WAN, seguidos de `clean`, [process_data.py](../../analysis/process_data.py) e [plot_results.py](../../analysis/plot_results.py)).*  
  > *"Agora vamos mudar ao vivo para o **Cenário 2 (WAN)**, injetando o atraso de 50 milissegundos e a perda de pacotes nos servidores, e vamos pedir para os três protocolos baixarem os 100 arquivos simultâneos:  
  > Olhem a diferença acontecendo na tela: o HTTP/1.1 (`T10`) demora quase 5 segundos para terminar; o HTTP/2 (`T11`), mesmo sendo multiplexado, fica preso nas perdas do TCP e leva mais de 3 segundos; e agora olhem o HTTP/3 sobre QUIC (`T12`): mesmo na rede ruim, ele entrega os 100 arquivos em pouco mais de 1 segundo!  
  > Por fim, limpamos as regras da placa de rede com o comando `clean` e rodamos os scripts [process_data.py](../../analysis/process_data.py) e [plot_results.py](../../analysis/plot_results.py), que leem o nosso dataset completo das 10 repetições em [results.csv](../../data/raw/results.csv), geram a tabela resumo em [summary_table.csv](../../data/processed/summary_table.csv) e salvam todos os gráficos com barras de erro."*

---

### 📊 Bloco 5: Análise dos Gráficos e Explicação Teórica (Tanenbaum) [10:30 - 13:30]
* **Clique para abrir na tela (direto nas imagens ou no PDF):**
  - 📄 [sbc-template.pdf](../../relatorio/sbc-template.pdf) *(Páginas 4 a 8)*
  - 📈 **Gráficos individuais em alta resolução:**
    1. [fig1_ttfb_cold_comparison.png](../../data/plots/fig1_ttfb_cold_comparison.png) *(Cold TTFB — Handshake)*
    2. [fig2_throughput_carga_a.png](../../data/plots/fig2_throughput_carga_a.png) *(Vazão 50 MB — Colapso TCP CUBIC)*
    3. [fig3_load_time_carga_b.png](../../data/plots/fig3_load_time_carga_b.png) *(Tempo Total — 100 Objetos)*
    4. [fig4_rps_carga_b_wan.png](../../data/plots/fig4_rps_carga_b_wan.png) *(RPS na WAN — Carga B)*
    5. [fig5_cdf_latency_distribution.png](../../data/plots/fig5_cdf_latency_distribution.png) *(Curva CDF de Latência)*

* **Fala — Marcos Willian (10:30 - 12:00):**
  > *(Ação: Mostrar a Tabela 2 no [sbc-template.pdf](../../relatorio/sbc-template.pdf) na página 4, e depois abrir [fig1_ttfb_cold_comparison.png](../../data/plots/fig1_ttfb_cold_comparison.png) e [fig2_throughput_carga_a.png](../../data/plots/fig2_throughput_carga_a.png) — ou mostrá-las nas páginas 5 e 6 do PDF).*  
  > *"Agora vamos olhar os gráficos que geramos no nosso relatório. Vale destacar que todos os gráficos trazem as **barras de erro** mostrando a variação e o intervalo de confiança das medições.  
  > Aqui na **Figura 1** ([fig1_ttfb_cold_comparison.png](../../data/plots/fig1_ttfb_cold_comparison.png)), que mede o tempo até o primeiro byte com conexão fria (o Cold TTFB), o gráfico mostra exatamente a teoria dos handshakes na prática: quando a rede tem latência alta na WAN, a barra do HTTPS/HTTP/2 fica bem mais alta porque ele precisa esperar duas viagens de ida e volta (a do TCP mais a do TLS), enquanto o HTTP/3 leva praticamente a metade do tempo por resolver tudo em uma viagem só no QUIC.  
  > Já na **Figura 2** ([fig2_throughput_carga_a.png](../../data/plots/fig2_throughput_carga_a.png)), que mostra a velocidade de download do arquivo grande de 50 Mega, acontece uma coisa muito interessante:  
  > Na rede local perfeita (LAN), o TCP tradicional tem uma velocidade bruta maior que o HTTP/3. Isso acontece porque o TCP roda direto dentro do kernel do Linux com otimizações nativas do sistema operacional, enquanto a biblioteca `aioquic` do cliente HTTP/3 processa cada pacote UDP em Python no espaço de usuário.  
  > Só que, quando passamos para a rede WAN com perda de pacotes (nos testes T04 e T05), a velocidade do TCP simplesmente despenca!  
  > Como nós fundamentamos aqui na Seção 4.2 do [sbc-template.pdf](../../relatorio/sbc-template.pdf) citando o livro do **Tanenbaum na Seção 6.5.11 sobre o TCP CUBIC**, o algoritmo CUBIC interpreta qualquer pacote perdido como sinal de que a rede está congestionada e reduz drasticamente a sua janela de transmissão. Como na nossa WAN existem perdas acontecendo o tempo todo durante os 50 Mega, a janela do TCP é cortada repetidas vezes antes de conseguir crescer de novo, derrubando a vazão lá para baixo."*

* **Fala — João Marcos (12:00 - 13:30):**
  > *(Ação: Clicar em [fig3_load_time_carga_b.png](../../data/plots/fig3_load_time_carga_b.png), [fig4_rps_carga_b_wan.png](../../data/plots/fig4_rps_carga_b_wan.png) e [fig5_cdf_latency_distribution.png](../../data/plots/fig5_cdf_latency_distribution.png) — ou mostrá-las nas páginas 7 e 8 do [sbc-template.pdf](../../relatorio/sbc-template.pdf)).*  
  > *"Em compensação, quando olhamos os testes T06 e principalmente o T12 nas **Figuras 3 e 4** ([fig3_load_time_carga_b.png](../../data/plots/fig3_load_time_carga_b.png) e [fig4_rps_carga_b_wan.png](../../data/plots/fig4_rps_carga_b_wan.png)), vemos que o HTTP/3 manteve um desempenho excelente na WAN, entregando quase o triplo de requisições por segundo em relação ao HTTP/2.  
  > A explicação teórica para isso também está no **Tanenbaum, nas Seções 6.6.1 (sobre o QUIC) e 6.6.2 (sobre o BBR)**:  
  > O primeiro motivo é o fim do **Bloqueio de Início de Linha no transporte**. No HTTP/2, como todos os 100 arquivos passam pelo mesmo cano TCP, quando um pacote se perde na rede, o sistema operacional segura a entrega de todos os outros 99 arquivos até que aquele pacote perdido seja retransmitido. Já no HTTP/3 sobre QUIC, cada arquivo viaja em um fluxo UDP separado: se um pacote se perde, apenas aquele único arquivo espera a retransmissão, e os outros 99 passam direto sem nenhum bloqueio.  
  > O segundo motivo é que o controle de congestionamento moderno usado com o QUIC (inspirado no BBR da Seção 6.6.2) controla o ritmo de envio medindo a capacidade real do link e a latência, sem entrar em pânico a cada perda isolada.  
  > A **Figura 5** ([fig5_cdf_latency_distribution.png](../../data/plots/fig5_cdf_latency_distribution.png)) fecha essa análise mostrando a curva de distribuição de atraso (CDF): reparem como a linha verde do HTTP/3 sobe quase reta logo no começo — mostrando que até os piores casos (o percentil p99) responderam rápido —, enquanto as curvas do HTTP/2 e do HTTP/1.1 se arrastam para a direita por causa das travadas de fila do TCP."*

---

### 🎯 Bloco 6: Conclusão e Encerramento [13:30 - 15:00]
* **Clique para abrir na tela:** 📄 [sbc-template.pdf](../../relatorio/sbc-template.pdf) *(Páginas 8 e 9 — Seção 5 e Referências, e depois voltar à Página 1)*.

* **Fala — Marcos Willian (13:30 - 14:15):**
  > *"Para concluir, aqui na Seção 5 do [sbc-template.pdf](../../relatorio/sbc-template.pdf): esse experimento deixou muito claro pra gente que não existe protocolo perfeito para tudo, mas sim o protocolo certo para cada cenário. Em uma rede interna fechada e sem perdas, o TCP no kernel do sistema operacional ainda entrega uma vazão bruta altíssima com baixo uso de CPU. Porém, na Internet do mundo real — principalmente no Wi-Fi e nas redes móveis 4G e 5G, onde atraso e perda de pacotes são normais —, o HTTP/3 sobre QUIC faz uma diferença enorme na experiência do usuário."*

* **Fala — João Marcos (14:15 - 15:00):**
  > *(Ação: Voltar para a Página 1 do [sbc-template.pdf](../../relatorio/sbc-template.pdf)).*  
  > *"Todo o nosso código, os contêineres Docker, os scripts de automação, os dados coletados e esse relatório em formato da SBC já estão organizados no pacote final do trabalho, com o link deste vídeo aqui na primeira página do PDF.  
  > A gente agradece ao professor e a todos que assistiram. Muito obrigado e até mais!"*
