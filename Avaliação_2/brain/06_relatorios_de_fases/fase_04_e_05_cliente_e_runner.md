# Relatório de Execução — Fases 4 e 5: Cliente de Benchmark em Python e Runner 1-Click

**Data:** 21 de Outubro de 2026  
**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)  
**Status das Fases:** ✅ CONCLUÍDAS COM SUCESSO

---

## 1. Escopo e Desafios de Engenharia Superados

As Fases 4 e 5 concentraram a implementação da lógica experimental central e do orquestrador de comando único (*1-Click Runner*):
1. Criação do cliente assíncrono em Python com suporte nativo a HTTP/1.1, HTTP/2 (TLS 1.3) e HTTP/3 (QUIC/UDP);
2. Implementação do **Controle Rigoroso de Viés de Sessão** (*Client-Side Bias Control*);
3. Criação do módulo de métricas com precisão de microssegundos via `time.perf_counter()`;
4. Desenvolvimento dos scripts orquestradores `run_experiments.sh` (Bash/Linux/WSL) e `run_experiments.ps1` (PowerShell/Windows).

---

## 2. Arquitetura do Cliente de Benchmark (`benchmark/client.py`)

O cliente foi desenvolvido com foco em alta precisão e separação de responsabilidades:
- **`httpx.AsyncClient`:** Gerencia as requisições HTTP/1.1 e HTTP/2 (com pacote `h2`).
- **`aioquic.asyncio.client.connect`:** Implementa a classe `H3BenchmarkProtocol(QuicConnectionProtocol)` para gerenciar os fluxos HTTP/3 sobre QUIC, emitindo quadros com ALPN `h3` e decodificando cabeçalhos QPACK e dados de streams assíncronas.
- **Resolução de SANs e SSL:** Configuração com verificação de certificados locais autoassinados.

---

## 3. Implementação Estrita do Controle de Viés de Sessão (`benchmark/session_control.py`)

Para assegurar validade científica e neutralizar a penalidade de -10 pontos prevista no edital:
1. **Desativação Total de Cache:** Todas as chamadas injetam cabeçalhos estritos:
   ```python
   {
       "Cache-Control": "no-cache, no-store, must-revalidate",
       "Pragma": "no-cache",
       "Expires": "0"
   }
   ```
2. **Modo Conexão Fria (Cold TTFB):**
   - Utilizado na Carga A e medições de latência inicial de handshake;
   - Antes de cada requisição individual, uma nova sessão é instanciada e destruída com `await client.aclose()`, desativando qualquer reuso de pools de conexões TCP ou tickets QUIC (0-RTT).
3. **Modo Conexão Aquecida (Warm Connection):**
   - Utilizado na Carga B (100 objetos de 10 KB);
   - Uma única conexão é aberta e mantida aquecida, disparando as 100 requisições simultaneamente via `asyncio.gather()`, permitindo avaliar a verdadeira multiplexação por quadros no HTTP/2 e por streams no HTTP/3.

---

## 4. O Orquestrador Mestre 1-Click (`run_experiments.ps1` e `run_experiments.sh`)

Os runners automatizam o ciclo de vida completo sem intervenção manual:
1. **Verificação Prévia:** Testa se portas e dependências estão disponíveis, assumindo fallback automático para a porta 8081 se a 8080 estiver em uso no host;
2. **Subida dos Contêineres:** `docker compose up -d` com injeção automática de `iproute2`;
3. **Cenário 1 (LAN):** Aplica `tc netem delay 0.5ms` e dispara T01 a T03 (Carga A) e T07 a T09 (Carga B);
4. **Cenário 2 (WAN):** Aplica `tc netem delay 25ms loss 2%` e dispara T04 a T06 (Carga A) e T10 a T12 (Carga B);
5. **Restauração:** Executa `tc qdisc del dev eth0 root`;
6. **Processamento e Plots:** Invoca `analysis/process_data.py` e `analysis/plot_results.py`;
7. **Teardown Limpo:** `docker compose down`.

---

## 5. Conclusão

Com a conclusão das Fases 4 e 5, a infraestrutura de medição encontra-se completamente operacional e automatizada, gerando os conjuntos de dados experimentais brutos em `data/raw/results.json` e `results.csv`.
