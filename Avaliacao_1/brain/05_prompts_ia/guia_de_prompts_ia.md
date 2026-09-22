# 06. Guia de Prompts Prontos para IAs

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** UFPI — Bacharelado em Sistemas de Informação

Utilize os prompts estruturados abaixo nas próximas sessões de desenvolvimento ou com outras IAs para gerar os artefatos de código, scripts e texto científico com máxima precisão e contexto.

---

## 🚀 Prompt 1: Criação da Infraestrutura Docker e NGINX HTTP/3

```text
Você é um especialista em redes de computadores, Linux e Docker. Estamos desenvolvendo a 1ª Avaliação Prática de Redes II da UFPI (2026-2) sobre avaliação comparativa de transporte (TCP, UDP Puro e QUIC HTTP/3).

Consulte os arquivos de contexto em:
- Avaliacao_1/brain/00_VISAO_GERAL_E_REGRAS.md
- Avaliacao_1/brain/01_ARQUITETURA_E_DOCKER.md

Sua tarefa é criar a infraestrutura completa de contêineres:
1. `docker/docker-compose.yml`: Topologia com contêiner 'server' (172.28.0.10) e 'client' (172.28.0.20), rede bridge isolada 'redes2_net', e 'cap_add: [NET_ADMIN]' no cliente.
2. `docker/server/Dockerfile`: NGINX oficial com suporte a ngx_http_v3_module, iperf3 daemon instalado, script entrypoint que inicia iperf3 -s em background e NGINX em foreground, e script de geração de certificados TLS 1.3 autoassinados via OpenSSL.
3. `docker/server/nginx.conf`: Configuração com listen 443 ssl (http2 on), listen 443 quic reuseport, TLSv1.3, ssl_early_data on, cabeçalho Alt-Svc 'h3=":443"; ma=86400'.
4. `docker/server/generate_assets.sh`: Script para gerar os arquivos estáticos de teste (100MB.bin, 1GB.bin e 100 imagens/objetos obj_001 a obj_100 na pasta web).
5. `docker/client/Dockerfile`: Base Ubuntu, com curl compilado com suporte a HTTP/3, iperf3, tshark, iproute2 (tc), python3, pandas, matplotlib, numpy, scipy.

Gere os arquivos com código limpo, comentado e pronto para execução.
```

---

## 🧪 Prompt 2: Criação dos Scripts de Automação dos Testes (Shell)

```text
Você é um especialista em automação e testes empíricos de redes no Linux. Estamos implementando os ensaios da 1ª Avaliação Prática de Redes II da UFPI.

Consulte os arquivos de contexto:
- Avaliacao_1/brain/02_CENARIOS_DE_TESTE.md
- Avaliacao_1/brain/03_METRICAS_E_ANALISE_DADOS.md

Sua tarefa é criar os scripts de automação em `scripts/`:
1. `setup_netem.sh`: Função que recebe como parâmetro o cenário (A, B ou C) e configura o `tc netem` na interface eth0:
   - Cenário A: delay 1.5ms, loss 0% (RTT < 5ms).
   - Cenário B: delay 10ms, loss 0% (RTT ~ 20ms).
   - Cenário C: delay 50ms (RTT 100ms) com perdas configuráveis (2%, 3%, 5%).
2. `test_scenario_a.sh`: Dispara 10 repetições de UDP Puro via iperf3 em 10, 50, 100, 250 e 500 Mbps com datagramas pequenos (128 bytes), salvando logs JSON e capturas tshark .pcapng.
3. `test_scenario_b.sh`: Dispara 10 repetições de download de 100MB e 1GB comparando HTTP/1.1, HTTP/2 e HTTP/3 (cURL com %{time_total}, %{speed_download}), com capturas tshark .pcapng.
4. `test_scenario_c.sh`: Dispara 10 repetições de download concorrente de 100 objetos simulando página web e reconexão TLS (HTTP/1.1 multi-conn, HTTP/2 e HTTP/3) sob perdas de 2%, 3% e 5%, salvando métricas de FCT por objeto e captura tshark.
5. `run_experiments.sh`: Script mestre 1-click que executa a bateria completa sequencialmente, sem intervenção humana, organizando saídas em `data/raw_logs/` e `data/pcaps/`.
```

---

## 📊 Prompt 3: Pipeline de Análise Estatística e Gráficos (Python)

```text
Você é um cientista de dados especializado em redes e medições experimentais.
Consulte:
- Avaliacao_1/brain/02_CENARIOS_DE_TESTE.md
- Avaliacao_1/brain/03_METRICAS_E_ANALISE_DADOS.md

Sua tarefa é criar o pipeline Python em `analysis/`:
1. `parse_logs.py`:
   - Processa os logs CSV e JSON gerados pelos scripts dos Cenários A, B e C.
   - Utiliza tshark em linha de comando ou via subprocess/pyshark para extrair o volume de bytes brutos dos arquivos .pcapng e calcular o Protocol Overhead.
   - Computa métricas estatísticas para cada condição (N=10 repetições): Média, Desvio Padrão, Intervalo de Confiança de 95% (t-Student, 9 graus de liberdade) e percentis p50, p90, p95 para o FCT.
   - Exporta tabelas consolidadas em CSV e formato LaTeX (tabular).
2. `generate_plots.py`:
   - Utiliza matplotlib e seaborn com estilo visual moderno e acadêmico (alta resolução 300 DPI).
   - Gera Gráfico 1: Injeção vs Goodput e Jitter (UDP Cenário A).
   - Gera Gráfico 2: Sobrecarga de cabeçalho comparativa (UDP vs TCP vs QUIC).
   - Gera Gráfico 3: Goodput e FCT para 100MB e 1GB com barras de erro (Cenário B).
   - Gera Gráfico 4: FCT Médio e percentil p95 sob perdas de 0%, 2%, 5% (Cenário C).
   - Gera Gráfico 5: CDF (Cumulative Distribution Function) do FCT na transferência dos objetos sob perda no Cenário C, demonstrando a eliminação do Head-of-Line Blocking no QUIC.
   - Salva os gráficos em `paper/figures/`.
```

---

## 📝 Prompt 4: Redação Completa do Artigo SBC/SBRC em LaTeX

```text
Você é um pesquisador experiente em redes de computadores com diversas publicações no SBRC e simpósios da SBC.
Consulte:
- Avaliacao_1/brain/00_VISAO_GERAL_E_REGRAS.md
- Avaliacao_1/brain/04_ARTIGO_SBC_SBRC.md
- As tabelas e gráficos gerados em `analysis/output/`

Sua tarefa é redigir o artigo científico completo em formato LaTeX padrão SBC (`sbc-template.tex` e `referencias.bib`):
1. Inclua obrigatoriamente na primeira página o link público para o vídeo gravado de 15 minutos (requisito crítico eliminatório).
2. Estruture rigorosamente as seções:
   - Resumo e Abstract
   - 1. Introdução e Objetivos
   - 2. Fundamentação Teórica (TCP RFC 793, UDP RFC 768, QUIC RFC 9000, RFC 9001 e TLS 1.3 RFC 8446)
   - 3. Metodologia Experimental e Topologia (Docker, NetEm, NGINX, curl HTTP/3, rigor estatístico com N=10 repetições)
   - 4. Resultados Experimentais e Discussão (Seções 4.1 Cenário A, 4.2 Cenário B, 4.3 Cenário C, com tabelas e gráficos detalhados)
   - 5. Considerações Finais e Conclusão
   - Referências Bibliográficas (incluindo as 5 RFCs mandatórias e literatura correlata)
3. Garanta escrita formal, técnica, em terceira pessoa, aprofundando os conceitos de Head-of-Line Blocking, TSO/GRO no Linux kernel e impacto do handshake TLS 1.3 1-RTT/0-RTT.
```
