# 00. Visão Geral, Objetivos e Regras Críticas

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** UFPI — Bacharelado em Sistemas de Informação  
**Trabalho:** Avaliação Prática: Avaliação de Desempenho e Sobrecarga de Transporte — TCP, UDP e QUIC com NGINX e Linux

---

## 1. Visão Geral do Problema

A evolução da pilha de protocolos de transporte na Internet busca resolver gargalos históricos associados ao TCP tradicional (bloqueio de cabeça de linha — Head-of-Line Blocking, latência elevada no handshake TLS/TCP) e limitações do UDP sem confiabilidade. 

O trabalho propõe uma **investigação experimental comparativa e empírica** entre três paradigmas de transporte:
1. **TCP (com TLS 1.3):** Avaliado por meio de HTTP/1.1 e HTTP/2 servidos pelo NGINX.
2. **UDP Puro:** Avaliado via fluxos sintéticos de datagramas sem confirmação via `iperf3`.
3. **QUIC (HTTP/3 sobre UDP):** Avaliado por meio de HTTP/3 servido pelo NGINX com suporte ao módulo `ngx_http_v3_module`.

Os ensaios devem evidenciar onde e por que cada protocolo se sobressai em termos de:
- **Vazão útil (Goodput)**;
- **Latência de conexão e tempo de conclusão de fluxo (FCT)**;
- **Sobrecarga de protocolo (Header & Crypto Overhead)**;
- **Resiliência a perdas e descarte de pacotes**.

---

## 2. Requisitos Mandatórios do Ambiente

1. **Plataforma:** Linux (distribuição Ubuntu como base dos contêineres).
   > [!NOTE]
   > **Execução em Host Windows:** É 100% suportado e válido desenvolver em máquina host Windows utilizando o **Docker Desktop com motor WSL 2 (Windows Subsystem for Linux)**. Como os contêineres Docker executam imagens Linux (Ubuntu) sob um kernel Linux real do WSL 2, o ambiente de testes atende integralmente ao requisito do edital.
2. **Orquestração Obrigatória:** Exclusivamente via `docker-compose.yml`.
3. **Pilha de Software Servidor (`server`):**
   - NGINX compilado/configurado com suporte a HTTP/3 e QUIC (`ngx_http_v3_module`).
   - Certificados TLS 1.3 válidos (gerados localmente via OpenSSL).
   - Serviço `iperf3 -s` ativo em segundo plano.
4. **Pilha de Software Cliente (`client`):**
   - Utilitário `curl` compilado com suporte nativo a HTTP/3 (utilizando Quiche ou ngtcp2).
   - Cliente `iperf3`.
   - Utilitário `tshark` (Wireshark CLI) para captura de tráfego em rede.
   - Ambiente Python 3 com bibliotecas `pandas`, `matplotlib`, `numpy` e `scipy` para tratamento estatístico e plots.
5. **Emulação de Canal de Rede Obrigatória:**
   - Realizada com o subsistema de Traffic Control do Linux (`tc` com `netem`).
   - Os contêineres devem possuir capacidade de rede no Compose: `cap_add: [NET_ADMIN]`.
6. **Automação Completa (Zero intervenção manual):**
   - Script automatizado (`run_experiments.sh` ou orquestrador em Python) capaz de subir o ambiente (`docker compose up -d`), configurar as regras de emulação, executar baterias de testes, salvar capturas `.pcapng` e arquivos de log, e gerar todos os gráficos finais.

---

## 3. Resumo dos 3 Cenários Experimentais

| Cenário | Protocolo Favorecido | Condições do Canal (`tc/netem`) | Padrão de Carga | Objetivo Central / Hipótese |
| :--- | :--- | :--- | :--- | :--- |
| **Cenário A** | **UDP Puro** | Latência ultrabaixa (RTT < 5 ms), Perda 0%, Alta capacidade | Datagramas pequenos a taxas crescentes (10 Mbps a 500 Mbps) | Mínimo overhead de cabeçalho (8 bytes), sem atraso de controle de congestionamento, menor uso de CPU. |
| **Cenário B** | **TCP** | RTT ~ 20 ms, Perda 0%, Alta largura de banda | Ficheiros de grande porte (100 MB a 1 GB) em HTTP/1.1 e HTTP/2 vs HTTP/3 | Vantagem das otimizações consolidadas de kernel (TSO, GRO), saturação eficiente de banda e menor CPU vs QUIC em user space. |
| **Cenário C** | **QUIC (HTTP/3)** | Alta latência (RTT ≥ 100 ms), Perda aleatória (2% a 5%) | 50 a 100 objetos independentes concorrentes + reconexão de clientes | Eliminação do HoL blocking no nível de transporte, handshake 1-RTT/0-RTT e goodput superior sob perda contínua. |

---

## 4. Métricas e Rigor Estatístico Obrigatório

1. **Flow Completion Time (FCT):** Média, percentis (p90, p95) e dispersão temporal.
2. **Goodput (Vazão Efetiva):** Bytes úteis de aplicação entregues por segundo.
3. **Sobrecarga de Protocolo (Overhead):** Proporção entre bytes brutos trafegados na interface (captura tshark) e bytes úteis consumidos pela aplicação.
4. **Comportamento de Perda e Retransmissão:** Identificação e análise no Wireshark da recuperação de perdas de cada protocolo.
5. **Rigor Estatístico:**
   - **Mínimo de 10 repetições independentes** para cada ponto de medição.
   - Apresentação obrigatória de **média e desvio padrão** (ou intervalo de confiança de 95%) em gráficos e tabelas.

---

## 5. Entregáveis Obrigatórios

### Entregável 1: Relatório Técnico no Padrão SBC/SBRC (PDF)
- Modelo oficial da Sociedade Brasileira de Computação (SBC/SBRC).
- Sem limite de páginas.
- Estrutura mínima obrigatória:
  - Resumo e Abstract
  - Introdução e Objetivos
  - Fundamentação Teórica (TCP, UDP, QUIC e aperto de mão TLS 1.3)
  - Metodologia Experimental e Topologia (diagramas e parâmetros)
  - Resultados Experimentais e Discussão (tabelas consolidadas, gráficos e análise comparativa)
  - Considerações Finais e Conclusão
  - Referências Bibliográficas (incluindo RFC 793, RFC 768, RFC 9000, RFC 9001 e RFC 8446).
- **Obrigatório:** Link público ao vídeo explicativo na **primeira página** (abaixo do resumo ou na nota de rodapé).

### Entregável 2: Vídeo Explicativo e de Demonstração (Exatamente 15 minutos)
- Duração exata: **15 minutos**.
- Conteúdo obrigatório:
  1. Apresentação da equipe.
  2. Demonstração guiada do código-fonte: estrutura do `docker-compose.yml`, configuração do NGINX (QUIC, certificados) e regras de emulação com `tc/netem`.
  3. Execução dos contêineres ao vivo, disparo dos testes e demonstração das capturas no Wireshark ou tshark.
  4. Apresentação dos gráficos gerados e discussão detalhada dos resultados obtidos.
- Plataforma: YouTube ("Não listado" ou "Público") ou Google Drive (com permissão pública de acesso aberta a qualquer pessoa com o link).

---

## 6. 🚨 REGRA ELIMINATÓRIA CRÍTICA (NOTA ZERO)

> [!CAUTION]
> **AVISO IMPORTANTE — CRITÉRIO EXCLUDENTE:**  
> A submissão regular desta avaliação exige, impreterivelmente:  
> 1. O arquivo PDF do relatório técnico no padrão SBC/SBRC;  
> 2. O link funcional para o vídeo gravado (15 minutos) contido dentro do relatório.  
>  
> **A ausência do arquivo PDF ou a ausência/inoperância do link de vídeo implicará a atribuição automática de NOTA ZERO (0,0) à equipe, sem possibilidade de entrega posterior ou de recurso.**
