# Avaliacao 1 - Ambiente Experimental HTTP/3 e QUIC

Repositório experimental para avaliação de desempenho de protocolos (TCP vs UDP vs QUIC) sob condições controladas de rede com Docker e NetEm.

## Estrutura do Módulo

- `docker/`: Configurações Docker (`docker-compose.yml`, `client/Dockerfile`, `server/Dockerfile`, `nginx.conf`, `entrypoint.sh`).
- `scripts/`: Orquestradores dos ensaios experimentais (`setup_netem.sh`, `run_experiments.sh`, `test_scenario_[a|b|c].sh`, `generate_static_data.py`).
- `data/`:
  - `static/`: Cargas estáticas (`100MB.bin`, `1GB.bin`, `objects/*.bin`).
  - `raw/`: Saída bruta dos ensaios em CSV.
  - `pcaps/`: Capturas de pacotes com tshark.
- `analysis/`: Scripts de visualização estatística e gráficos científicos.
- `artigo/`: Documentação científica em formato SBC/SBRC (LaTeX).
- `brain/`: Diretrizes de fases, modelagem e checklists do projeto.

## Comandos Essenciais

```bash
# Subir infraestrutura
cd docker && docker compose up -d --build

# Acessar contêiner de teste
docker exec -it redes2_client /bin/bash

# Executar bateria completa dentro do contêiner
/workspace/scripts/run_experiments.sh
```

## Regras Críticas para Modificações

1. **NetEm & Permissões**: Qualquer comando `tc` exige `cap_add: NET_ADMIN` no container.
2. **Medição de QUIC**: O cURL usa o binário estático com suporte HTTP/3 em `/usr/local/bin/curl`. Sempre passe a flag `--http3-only` para garantir que o fallback para TCP não mascare o teste.
3. **Integridade de Dados**: Sempre valide `%{http_code}` ao usar curl nos scripts de benchmark para evitar computar requisições com falha como goodput.
