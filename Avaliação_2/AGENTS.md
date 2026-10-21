# Avaliacao 2 - Estudo Experimental de Desempenho de Protocolos Web
## (HTTP/1.1 vs HTTPS/TLS vs HTTP/3-QUIC) em Ambiente Emulado com Docker e Python

Repositório experimental para avaliação empírica de desempenho e sobrecarga dos protocolos da Web sob condições controladas de canal de rede (LAN vs WAN com perda) utilizando Docker, Linux Traffic Control (`tc netem`) e cliente assíncrono em Python (`httpx` + `aioquic`).

Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
Disciplina: Redes de Computadores II (2026-2)  
Aluno: João Marcos Sousa Rufino Leal  
E-mail: `jsousarufinoleal@ufpi.edu.br`

---

## Estrutura do Repositório

- `run_experiments.sh` / `run_experiments.ps1`: Orquestrador mestre 1-click para Host (Linux, macOS, WSL 2, Windows).
- `docker/`: Configurações de infraestrutura Docker:
  - `docker-compose.yml`: Topologia com os 3 servidores Web isolados na rede `net_bench` (172.20.0.0/16).
  - `server-http1/`: NGINX Alpine servindo HTTP/1.1 em texto claro (Porta 80 / Host 8080).
  - `server-http2/`: NGINX Alpine servindo HTTPS/HTTP/2 com TLS 1.3 (Porta 443 / Host 8443).
  - `server-http3/`: Caddy 2.7 Alpine servindo HTTP/3 sobre QUIC nativo (Porta 443 TCP/UDP / Host 9443).
  - `certs/`: Certificados criptográficos TLS 1.3 locais com SANs válidos gerados via OpenSSL.
- `benchmark/`: Código-fonte do cliente de benchmark em Python:
  - `client.py`: Cliente assíncrono utilizando `httpx` (HTTP/1.1 e HTTP/2) e `aioquic` (HTTP/3).
  - `session_control.py`: Módulo estrito de controle de viés de sessão (Cold TTFB com fechamento explícito vs Warm multiplexado).
  - `metrics.py`: Coleta e cálculo de precisão (TTFB, Load Time, RPS, p50, p99).
- `scripts/`: Scripts de emulação e controle:
  - `setup_netem.sh`: Aplicação e remoção de regras `tc netem` (Cenário 1 LAN vs Cenário 2 WAN).
  - `generate_payloads.py`: Geração determinística de cargas sintéticas (Carga A de 50 MB e Carga B de 100x10 KB).
- `data/`:
  - `static/`: Cargas estáticas (`50MB.bin` e pasta `objects/` com 100 arquivos de 10 KB).
  - `raw/`: Dados brutos exportados pelos ensaios (`results.json` e `results.csv`).
  - `processed/`: Consolidação estatística (médias, medianas, desvio padrão, IC 95%, percentis).
  - `plots/`: Gráficos científicos de alta resolução com **barras de erro obrigatórias**.
- `analysis/`: Scripts Python de processamento estatístico e geração de figuras (`process_data.py`, `plot_results.py`).
- `relatorio/`: Artigo técnico científico em padrão formal SBC/LaTeX com citações teóricas ao Tanenbaum (Seção 6.5.11 e Seções 6.6.1 e 6.6.2).
- `video/`: Roteiro cronometrado e slides para o vídeo de apresentação de 15 minutos.
- `brain/`: Diretrizes de fases, modelagem arquitetural, matriz de testes e checklists do projeto.

---

## Comandos Essenciais

### 1. Execução Completa Automatizada (1-Click Run)

No Linux / macOS / WSL 2 / Git Bash:
```bash
./run_experiments.sh
```

No Windows PowerShell:
```powershell
.\run_experiments.ps1
```

O script mestre realiza automaticamente:
1. Subida dos contêineres dos 3 servidores Web (`docker compose up -d`);
2. Aplicação e verificação das regras do `tc netem` para o Cenário 1 (LAN: delay 0.5ms, loss 0%);
3. Execução dos testes T01 a T03 (Carga A) e T07 a T09 (Carga B);
4. Aplicação das regras do `tc netem` para o Cenário 2 (WAN: delay 25ms, loss 2%);
5. Execução dos testes T04 a T06 (Carga A) e T10 a T12 (Carga B);
6. Limpeza e restauração das interfaces (`tc qdisc del dev eth0 root`);
7. Exportação e consolidação dos dados brutos em `data/raw/results.json` e `results.csv`;
8. Execução do pipeline de visualização gráfica (`python analysis/plot_results.py`);
9. Encerramento limpo do ambiente Docker (`docker compose down`).

---

## Regras Críticas de Conformidade

1. **Permissões de Kernel (`tc netem`)**: Todos os serviços do Docker Compose que sofrem emulação de rede possuem obrigatoriamente a diretiva `cap_add: [NET_ADMIN]`. O atraso unidirecional injetado na interface é $N/2$ para obter um RTT de $N$ ms (ex.: 0.5ms para RTT 1ms; 25ms para RTT 50ms).
2. **Controle Estrito de Vício de Sessão (Client-Side Bias Control)**:
   - **Cold TTFB (Handshake)**: A sessão do cliente deve ser explicitamente encerrada (`client.close()`) antes de cada requisição individual para medir o custo real do handshake (TCP 1 RTT, TLS 1.3 2 RTTs, QUIC 1 RTT).
   - **Warm Connection (Multiplexação)**: Os testes de concorrência com 100 objetos mantêm explicitamente uma única conexão persistente aquecida para avaliar a multiplexação real sem sucessivos handshakes.
3. **Matriz Experimental Obrigatória**: Todos os 12 testes previstos (T01 a T12) devem ser executados com no mínimo 10 repetições independentes ($N \ge 10$).
4. **Visualização Gráfica Científica**: É terminantemente proibido plotar gráficos planos. Todos os gráficos de barras ou de linhas devem exibir **barras de erro** representando o desvio padrão ou o intervalo de confiança de 95% (penalidade de 10 pontos na nota se ausentes).
5. **Fundamentação Teórica Mandatória no Relatório**: A análise dos resultados nos testes sob perdas (Cenário WAN) deve citar e articular expressamente:
   - **Tanenbaum Seção 6.5.11 (TCP CUBIC)**: para o colapso de vazão do TCP sob 2% de perda estocástica;
   - **Tanenbaum Seção 6.6.1 (QUIC) e Seção 6.6.2 (BBR)**: para a resiliência e manutenção de alto desempenho no QUIC.
6. **Critério Eliminatório (Nota Zero)**: A submissão exige impreterivelmente o código, o relatório técnico em PDF e o link público funcional para o vídeo de 15 minutos contido na 1ª página do relatório. A falta de qualquer um destes três itens resulta em **NOTA ZERO (0,0)** automática.
