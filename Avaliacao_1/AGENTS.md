# Avaliacao 1 - Ambiente Experimental HTTP/3 e QUIC

Repositório experimental para avaliação de desempenho de protocolos (TCP vs UDP vs QUIC) sob condições controladas de rede com Docker e NetEm.
Universidade Federal do Piauí (UFPI) — Redes de Computadores II (2026-2)
Aluno: João Marcos Sousa Rufino Leal

## Estrutura do Módulo

- `run_experiments.sh` / `run_experiments.ps1`: Orquestrador mestre 1-click para Host (Linux, macOS, WSL, Windows).
- `docker/`: Configurações Docker (`docker-compose.yml`, `client/Dockerfile`, `server/Dockerfile`, `nginx.conf`, `entrypoint.sh`).
- `scripts/`: Orquestradores dos ensaios experimentais (`setup_netem.sh`, `run_experiments.sh`, `test_scenario_[a|b|c].sh`, `generate_static_data.py`, `process_pcaps.sh`).
- `data/`:
  - `static/`: Cargas estáticas (`100MB.bin`, `1GB.bin`, `objects/*.bin`).
  - `raw/`: Saída bruta dos ensaios em CSV.
  - `pcaps/`: Capturas de pacotes com tshark (.pcapng com snaplen 160B).
  - `processed/`: Consolidação estatística (IC 95%, p90, p95, overhead PCAP).
  - `plots/`: Gráficos científicos de alta resolução (300 DPI).
- `analysis/`: Scripts de visualização estatística e gráficos científicos (`parse_logs.py`, `generate_plots.py`).
- `artigo/`: Documentação científica em formato SBC/SBRC (LaTeX).
- `brain/`: Diretrizes de fases, modelagem e checklists do projeto.

## Comandos Essenciais

### Execução Completa Automatizada (1-Click Run)

No Linux / macOS / WSL / Git Bash:
```bash
./run_experiments.sh
```

No Windows PowerShell:
```powershell
.\run_experiments.ps1
```

Ou dentro do contêiner de teste interativo:
```bash
docker compose -f docker/docker-compose.yml up -d
docker exec -it redes2_client /workspace/scripts/run_experiments.sh
```

## Regras Críticas de Conformidade

1. **NetEm & Permissões**: Qualquer comando `tc` exige `cap_add: NET_ADMIN` no container.
2. **Medição de QUIC**: O cURL usa o binário com suporte HTTP/3 nativo (ngtcp2 + nghttp3). Sempre passe `--http3-only` para garantir que o fallback para TCP não mascare o teste.
3. **Integridade de Dados**: Sempre valide `%{http_code}` ao usar curl nos scripts de benchmark para evitar computar requisições com falha como goodput.
4. **Capturas de Tráfego**: As capturas `tshark` usam snaplen de 160 bytes (`-s 160`) para preservar todos os cabeçalhos de transporte (Ethernet, IP, TCP, TLS, QUIC) sem gerar arquivos desnecessariamente gigantescos de payload sintético.
5. **Rigor Estatístico**: Cada ponto de teste possui 10 repetições independentes com cálculo de média, desvio padrão, percentis p90/p95 e intervalo de confiança de 95% (t-Student).
