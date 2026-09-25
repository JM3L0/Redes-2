# 📘 Fase 2: Infraestrutura Docker & NGINX HTTP/3

**Status:**  CONCLUÍDA  
**Data:** 25/09/2026  
**Responsável:** João Marcos Sousa Rufino Leal  

---

## 1. Objetivos da Fase
Construir uma infraestrutura reproduzível, isolada e baseada em contêineres Docker capaz de prover:
1. Servidor web NGINX moderno com suporte concorrente a **HTTP/1.1**, **HTTP/2** e **HTTP/3 (QUIC)** sob criptografia **TLS 1.3**;
2. Servidor `iperf3` para geração de fluxos UDP puros;
3. Contêiner cliente equipado com utilitário `curl` moderno com suporte a HTTP/3 nativo, `tshark` para captura de tráfego e ferramentas de controle de tráfego (`tc/netem`);
4. Topologia de rede em ponte (bridge) com endereçamento estático e privilégios `NET_ADMIN`.

---

## 2. O que foi Feito

### 2.1. Normalização de Ambiente e Quebras de Linha (`.gitattributes`)
* Como o host é Windows com WSL 2, configuramos o [`.gitattributes`](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/.gitattributes) para forçar quebras de linha `LF` em todos os arquivos de script (`.sh`), configurações (`.conf`), Dockerfiles e código Python, prevenindo erros de execução (`\r: command not found`).

### 2.2. Contêiner Servidor (`redes2_server`)
* **Base:** `nginx:1.27-alpine` com módulo `ngx_http_v3_module` integrado.
* **Arquivo NGINX:** [docker/server/nginx.conf](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/docker/server/nginx.conf)
  * Configurado para escutar na porta 443 TCP (`ssl http2`) e porta 443 UDP (`quic reuseport`).
  * TLS 1.3 ativado com cifra moderna e suporte a 0-RTT (`ssl_early_data on`).
  * Injeção obrigatória do cabeçalho de anúncio de protocolo alternativo: `Alt-Svc: h3=":443"; ma=86400`.
* **Inicialização Automatizada:** [docker/server/entrypoint.sh](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/docker/server/entrypoint.sh)
  * Geração dinâmica via OpenSSL de certificados TLS 1.3 com Subject Alternative Names (SAN: `server`, `localhost`, `172.28.0.10`).
  * Inicialização do daemon `iperf3 -s -p 5201 -D`.
  * Execução do NGINX em primeiro plano.

### 2.3. Contêiner Cliente (`redes2_client`)
* **Base:** `ubuntu:24.04` com pacotes essenciais de rede e análise: `iproute2`, `iperf3`, `tshark`, `jq`, `python3`, `pandas`, `matplotlib`, `numpy` e `scipy`.
* **Binário Nativo cURL HTTP/3:** Instalação e verificação do cURL com backend `ngtcp2 + nghttp3 + TLS 1.3`, habilitando flags `--http3` e `--http3-only`.

### 2.4. Orquestração Declarativa (`docker-compose.yml`)
* [docker/docker-compose.yml](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/docker/docker-compose.yml):
  * Rede isolada `redes2_net` (`172.28.0.0/16`).
  * Servidor fixado em `172.28.0.10`.
  * Cliente fixado em `172.28.0.20`.
  * Privilégio `cap_add: [NET_ADMIN]` concedido a ambos os nós para permitir injeção de atraso e perdas com `tc`.

### 2.5. Geração das Cargas Estáticas de Teste
* Criação e execução do gerador [scripts/generate_static_data.py](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/scripts/generate_static_data.py):
  * `data/static/index.html` (página de teste);
  * `data/static/100MB.bin` (arquivo de 100 MB);
  * `data/static/1GB.bin` (arquivo de 1 GB);
  * `data/static/objects/obj_001.bin` a `obj_100.bin` (100 arquivos de 50 KB cada).

### 2.6. Testes Práticos de Validação de Conectividade e Protocolos
Executamos no contêiner `redes2_client` os comandos de validação real:
1. **UDP com iperf3 (`50 Mbps`):**
   * Comando: `iperf3 -c 172.28.0.10 -u -b 50M -t 2`
   * Resultado: 50.0 Mbits/sec entregues com 0% de perda e jitter de 0.036 ms.
2. **HTTP/1.1 via cURL:**
   * Comando: `curl -k --http1.1 https://server/index.html -I`
   * Resultado: `HTTP/1.1 200 OK`, `X-Protocol: HTTP/1.1`, cabeçalho `Alt-Svc: h3=":443"` presente.
3. **HTTP/2 via cURL:**
   * Comando: `curl -k --http2 https://server/index.html -I`
   * Resultado: `HTTP/2 200`, `x-protocol: HTTP/2.0`.
4. **HTTP/3 (QUIC sobre UDP) via cURL:**
   * Comando: `curl -k --http3-only https://server/index.html -I`
   * Resultado: `HTTP/3 200`, `x-protocol: HTTP/3.0`, confirmando handshake 1-RTT com TLS 1.3 nativo em UDP!
5. **Traffic Control (`tc/netem`):**
   * Comando: `./scripts/setup_netem.sh scenario_b`
   * Resultado: Injeção de 10ms de atraso validada via `ping 172.28.0.10` com RTT estável em 10.3 ms e limpeza posterior com `clear`.

---

## 3. Artefatos Produzidos
* [**`docker/server/Dockerfile`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/docker/server/Dockerfile)
* [**`docker/server/nginx.conf`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/docker/server/nginx.conf)
* [**`docker/server/entrypoint.sh`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/docker/server/entrypoint.sh)
* [**`docker/client/Dockerfile`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/docker/client/Dockerfile)
* [**`docker/docker-compose.yml`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/docker/docker-compose.yml)
* [**`scripts/generate_static_data.py`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/scripts/generate_static_data.py)
* [**`data/static/`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/data/static/)
