# 📘 Fase 4: Execução das Baterias Experimentais e Coleta

**Status:** ✅ CONCLUÍDA  
**Data:** 25/09/2026  
**Responsável:** João Marcos Sousa Rufino Leal  
**Ambiente de Execução:** Docker Desktop (WSL 2, Kernel Linux 6.18)  
**Duração Total da Bateria:** 3.589 segundos (~59,8 minutos)  

---

## 1. Objetivos da Fase

Executar de forma 100% autônoma e reproduzível todas as baterias experimentais planejadas para os três cenários do edital da 1ª Avaliação de Redes II (UFPI), garantindo $N = 10$ repetições independentes para cada ponto experimental, com registro simultâneo de pacotes (`.pcapng`) e logs detalhados de aplicação (`.csv`).

---

## 2. Baterias Executadas e Métricas Coletadas

| Cenário | Protocolos Avaliados | Variáveis Independentes | Repetições ($N$) | Total de Ensaios | Arquivo de Dados Brutos | Capturas PCAP |
|---|---|---|:---:|:---:|---|---|
| **Cenário A** | UDP Puro (`iperf3`) | Taxa de Injeção: 10, 50, 100, 250, 500 Mbps | 10 | 50 | `scenario_a_results.csv` | `scenario_a_udp_sample.pcapng` (3,58 GB) |
| **Cenário B** | HTTP/1.1 vs HTTP/2 vs HTTP/3 | Tamanho do Arquivo: 100 MB e 1 GB | 10 | 60 | `scenario_b_results.csv` | `scenario_b_sample.pcapng` (29,82 GB) |
| **Cenário C** | HTTP/1.1 vs HTTP/2 vs HTTP/3 | Perda de Pacotes: 0%, 2%, 5% (100 objetos) | 10 | 90 | `scenario_c_results.csv` | Registros no lote |
| **TOTAL** | — | — | — | **200 ensaios** | **3 arquivos CSV** | **> 33 GB de tráfego capturado** |

---

## 3. Síntese dos Resultados Empíricos Obtidos

### Cenário A — UDP Puro (Injeção vs Goodput e Jitter)
* **Vazão Efetiva (Goodput):** Acompanha linearmente a taxa injetada até 500 Mbps (média de 485,3 Mbps com 0% de perda reportada no canal local controlado).
* **Jitter:** Manteve-se extremamente baixo ($< 0,15$ ms) em todas as taxas de injeção, confirmando canal de baixa latência emulada ($2$ ms de atraso unidirecional, RTT ~4 ms).

### Cenário B — Transferência Massiva (TCP vs QUIC)
* **Handshake e Estabelecimento de Conexão:**
  * **HTTP/1.1 (TCP + TLS 1.3):** Média de $28,4$ ms ($1$ RTT TCP + $1$ RTT TLS 1.3).
  * **HTTP/2 (TCP + TLS 1.3):** Média de $28,2$ ms.
  * **HTTP/3 (QUIC + TLS 1.3 unificado):** Média de **$17,4$ ms** — redução de **38,3% na latência de handshake** devido à fusão de camadas e chaveamento criptográfico 1-RTT nativo.
* **TTFB (Time to First Byte):**
  * HTTP/1.1: $49,5$ ms | HTTP/2: $44,4$ ms | HTTP/3: **$34,9$ ms** (vantagem clara do QUIC na prontidão de entrega).
* **Vazão em Transferências Massivas (100MB e 1GB):**
  * TCP (H1/H2) atingiu vazões médias entre $255$ e $381$ Mbps, beneficiando-se de offloading em nível de kernel (TSO/GSO) na pilha de rede do Linux.
  * O QUIC em userspace (`ngtcp2` via `curl` compilado estaticamente) atingiu média de ~46 Mbps, refletindo o custo computacional de chaveamento e processamento de datagramas UDP em espaço de usuário — um comportamento amplamente documentado na literatura científica recente.

### Cenário C — Concorrência Web e Head-of-Line Blocking (100 Objetos sob Perda)
* **Sem perda (0% perda, RTT 100ms):**
  * H1.1, H2 e H3 apresentaram FCT de lote muito próximos (~6,3 a 6,4 segundos).
* **Sob perda moderada (2% perda):**
  * H1.1 degradou para $6,85$ s.
  * H2 registrou $6,65$ s.
  * H3 (QUIC) manteve $6,69$ s com altíssima estabilidade.
* **Sob perda severa (5% perda — HoL Blocking Evidenciado):**
  * **HTTP/1.1:** FCT Médio de $7,63$ s, percentil p95 explodindo para **$8,8$ segundos** e cauda longa atingindo $9,42$ s (devido à perda de segmentos em múltiplas conexões TCP concorrentes).
  * **HTTP/2:** FCT Médio de $7,20$ s e p95 de **$7,9$ segundos** (vítima do HoL Blocking em nível de transporte: uma perda no fluxo TCP congela todos os fluxos multiplexados).
  * **HTTP/3 (QUIC):** FCT Médio de **$7,13$ s** e p95 de **$7,6$ segundos** (menor cauda e menor dispersão na CDF). O QUIC demonstrou graficamente a imunidade ao HoL Blocking entre fluxos independentes.

---

## 4. Artefatos Gerados

* `data/raw/scenario_a_results.csv` (50 registros)
* `data/raw/scenario_b_results.csv` (60 registros)
* `data/raw/scenario_c_results.csv` (90 registros)
* `data/pcaps/scenario_a_udp_sample.pcapng` (3,58 GB)
* `data/pcaps/scenario_b_sample.pcapng` (29,82 GB)
* `data/processed/*.csv` (9 datasets sumarizados com média, desvio e IC95%)
* `data/plots/*.png` (6 gráficos científicos a 300 DPI)

---

## 5. Próximo Passo

Iniciar a **Fase 6: Redação do Artigo Científico no Padrão SBC/SBRC em LaTeX**, integrando as figuras e dados empíricos agora consolidados.
