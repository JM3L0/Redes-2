# Relatório de Execução — Fases 2 e 3: Infraestrutura Docker, Certificados TLS 1.3, Payload 1 KB e Emulação `tc netem`

**Data:** 17 de Novembro de 2026  
**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)  
**Status das Fases:** ✅ CONCLUÍDAS COM SUCESSO

---

## 1. Escopo e Objetivos Realizados

1. Implementação do arquivo declarativo `docker-compose.yml` com os três contêineres na sub-rede `net_bench` (`172.20.0.0/16`) e `cap_add: [NET_ADMIN]`:
   - `server_tcp_cc` (`networkstatic/iperf3 -s`, IP `172.20.0.10`);
   - `server_http3_quic` (`caddy:2.7-alpine`, IP `172.20.0.30`);
   - `client_bench` (`curlimages/curl:latest`, IP `172.20.0.50`, com `curl` estático 8.22 suportando HTTP/3 e `iperf3`);
2. Geração de certificados TLS 1.3 com SANs para `172.20.0.30` e `server_http3_quic` (`scripts/generate_certs.py`);
3. Geração determinística do objeto estático de 1 KB (`site/1KB.bin`, `1024` bytes) (`scripts/generate_payloads.py`);
4. Habilitação automática do módulo `tcp_bbr` no kernel Linux (`nsenter -t 1 -m -u -n -i modprobe tcp_bbr`);
5. Implementação e homologação dos scripts `scripts/setup_netem.py`, `setup_netem.sh` e `setup_netem.ps1` para os Cenários 1 (LAN 1ms/0%), 2 (WAN 50ms/2%) e 3 (WAN 50ms/0%) + limpeza (`tc qdisc del dev eth0 root`).
