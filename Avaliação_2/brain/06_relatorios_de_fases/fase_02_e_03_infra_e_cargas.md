# Relatório de Execução — Fases 2 e 3: Infraestrutura Docker, Certificados TLS e Emulação `tc netem`

**Data:** 21 de Outubro de 2026  
**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)  
**Status das Fases:** ✅ CONCLUÍDAS COM SUCESSO

---

## 1. Escopo e Objetivos Realizados

As Fases 2 e 3 englobaram a materialização de toda a infraestrutura física virtualizada e dos scripts de controle de tráfego exigidos no edital da 2ª Avaliação:
1. Modelagem do `docker-compose.yml` com os três servidores Web alocados na rede bridge dedicada `net_bench` (172.20.0.0/16);
2. Resolução do privilégio de kernel obrigatório `cap_add: [NET_ADMIN]`;
3. Geração programática de certificados TLS 1.3 locais autoassinados com Subject Alternative Names (SANs);
4. Geração determinística dos payloads sintéticos: Carga A (50 MB) e Carga B (100 objetos de 10 KB);
5. Validação sintática e operacional dos scripts de controle de tráfego `tc netem` (Cenário 1 LAN vs Cenário 2 WAN).

---

## 2. Detalhes de Implementação dos Servidores

### 2.1. Servidor 1: HTTP/1.1 (`server_http11`)
- **Imagem:** `nginx:alpine`
- **Endereço IPv4 na rede Docker:** `172.20.0.10:80`
- **Porta Host:** Mapeada para `${HTTP1_PORT:-8080}:80`. Na máquina de avaliação/host, se a porta 8080 estiver em uso por serviços de sistema, o orquestrador assume dinamicamente 8081 sem falha de bind.
- **Configuração:** `docker/server-http1/nginx.conf` servindo `/usr/share/nginx/html` com cabeçalho `Cache-Control: no-store, no-cache, must-revalidate`.

### 2.2. Servidor 2: HTTPS / HTTP/2 com TLS 1.3 (`server_http2_tls`)
- **Imagem:** `nginx:alpine`
- **Endereço IPv4 na rede Docker:** `172.20.0.20:443`
- **Porta Host:** `8443:443`
- **Configuração:** `docker/server-http2/nginx.conf` com `ssl_protocols TLSv1.3 TLSv1.2;`, montando `/etc/nginx/certs`.

### 2.3. Servidor 3: HTTP/3 Nativo sobre QUIC (`server_http3_quic`)
- **Imagem:** `caddy:2.7-alpine`
- **Endereço IPv4 na rede Docker:** `172.20.0.30:443`
- **Portas Host:** `9443:443/tcp` e `9443:443/udp`
- **Configuração:** `docker/server-http3/Caddyfile` com HTTPS ativo, montando `/etc/caddy/certs` e expondo o cabeçalho `Alt-Svc: h3=":9443"; ma=86400`.

---

## 3. Geração dos Certificados TLS 1.3 (`scripts/generate_certs.py`)

Para evitar dependência de binários externos de OpenSSL no Windows Host, implementou-se um gerador puro em Python utilizando a biblioteca `cryptography`. O certificado gerado inclui:
- **Chave Privada:** RSA de 2048 bits em PEM (`docker/certs/key.pem`).
- **Certificado:** X.509 v3 autoassinado com validade de 365 dias (`docker/certs/cert.pem`).
- **Subject Alternative Names (SANs):**
  - DNS: `localhost`, `server_http2_tls`, `server_http3_quic`
  - IP: `127.0.0.1`, `172.20.0.20`, `172.20.0.30`

---

## 4. Geração dos Payloads Sintéticos (`scripts/generate_payloads.py`)

- **Carga A:** Arquivo binário estático de exatamente 52.428.800 bytes (`data/static/50MB.bin`), montado como volume de leitura compartilhada nos três contêineres.
- **Carga B:** Diretório `data/static/objects/` contendo 100 arquivos independentes de 10.240 bytes cada (`obj_001.bin` a `obj_100.bin`).

---

## 5. Emulação de Rede e Validação `tc netem` (`scripts/setup_netem.sh` / `.ps1`)

Os testes confirmaram a aplicação precisa das disciplinas de fila:
- **Cenário 1 (LAN):** `tc qdisc add dev eth0 root netem delay 0.5ms` $\implies$ RTT final de 1.0 ms com 0% de perda.
- **Cenário 2 (WAN):** `tc qdisc add dev eth0 root netem delay 25ms loss 2%` $\implies$ RTT final de 50.0 ms com 2% de descarte estocástico de pacotes.
- **Limpeza:** `tc qdisc del dev eth0 root` restaurando a interface limpa (`qdisc noqueue`).

---

## 6. Conclusão

Todas as metas das Fases 2 e 3 foram homologadas e integradas ao repositório, deixando o ecossistema pronto para a coleta maciça de dados das fases subsequentes.
