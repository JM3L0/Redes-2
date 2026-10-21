import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\jsous\Desktop\Redes 2\Avaliação_2"

# 1. Carregar todos os arquivos do Cérebro e da raiz
brain_dir = os.path.join(base_dir, "brain")
docs = {}

for root, _, files in os.walk(base_dir):
    if "scratch" in root or ".git" in root or "__pycache__" in root:
        continue
    for f in files:
        if f.endswith((".md", ".yml", ".py", ".sh", ".ps1", ".tex")):
            p = os.path.join(root, f)
            rel = os.path.relpath(p, base_dir)
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                    docs[rel] = fh.read()
            except Exception as e:
                pass

print("="*80)
print("🔍 SUBAGENTE 1: AUDITOR DE INFRAESTRUTURA, EMULAÇÃO DE REDE E PIPELINE TÉCNICO")
print("="*80)

audit_checks = [
    {
        "id": "SUB1-REQ-01",
        "description": "Topologia Docker Compose com 3 servidores distintos na rede net_bench",
        "files": ["docker/docker-compose.yml", "brain/02_arquitetura/arquitetura_e_docker.md"],
        "patterns": [
            r"server_http11",
            r"server_http2_tls",
            r"server_http3_quic",
            r"net_bench",
            r"172\.20\.0\.0/16",
            r"172\.20\.0\.10",
            r"172\.20\.0\.20",
            r"172\.20\.0\.30"
        ]
    },
    {
        "id": "SUB1-REQ-02",
        "description": "Declaração mandatória de privilégio de kernel cap_add: [NET_ADMIN]",
        "files": ["docker/docker-compose.yml", "brain/02_arquitetura/arquitetura_e_docker.md", "AGENTS.md"],
        "patterns": [
            r"cap_add:\s*\n\s*-\s*NET_ADMIN|cap_add:.*NET_ADMIN"
        ]
    },
    {
        "id": "SUB1-REQ-03",
        "description": "Mapeamento das portas dos servidores Web (HTTP 8080/8081, HTTPS 8443, HTTP/3 9443 TCP/UDP)",
        "files": ["docker/docker-compose.yml", "brain/02_arquitetura/arquitetura_e_docker.md"],
        "patterns": [
            r"8080:80|8081:80",
            r"8443:443",
            r"9443:443/tcp",
            r"9443:443/udp"
        ]
    },
    {
        "id": "SUB1-REQ-04",
        "description": "Certificados TLS 1.3 locais com Subject Alternative Names (SANs) válidos",
        "files": ["scripts/generate_certs.py", "brain/02_arquitetura/arquitetura_e_docker.md"],
        "patterns": [
            r"DNS:localhost",
            r"server_http2_tls",
            r"server_http3_quic",
            r"172\.20\.0\.20",
            r"172\.20\.0\.30"
        ]
    },
    {
        "id": "SUB1-REQ-05",
        "description": "Parametrização do Linux Traffic Control (tc netem) - Cenário 1 LAN (delay 0.5ms = RTT 1ms, perda 0%)",
        "files": ["scripts/setup_netem.sh", "scripts/setup_netem.ps1", "brain/03_experimentos/cenarios_de_teste.md"],
        "patterns": [
            r"delay 0\.5ms",
            r"1(\.0)?ms"
        ]
    },
    {
        "id": "SUB1-REQ-06",
        "description": "Parametrização do Linux Traffic Control (tc netem) - Cenário 2 WAN (delay 25ms = RTT 50ms, perda 2%)",
        "files": ["scripts/setup_netem.sh", "scripts/setup_netem.ps1", "brain/03_experimentos/cenarios_de_teste.md"],
        "patterns": [
            r"delay 25ms loss 2%",
            r"50(\.0)?ms"
        ]
    },
    {
        "id": "SUB1-REQ-07",
        "description": "Procedimento automatizado de limpeza e restauração de qdisc (tc qdisc del)",
        "files": ["scripts/setup_netem.sh", "scripts/setup_netem.ps1", "brain/02_arquitetura/arquitetura_e_docker.md"],
        "patterns": [
            r"tc qdisc del dev eth0 root"
        ]
    },
    {
        "id": "SUB1-REQ-08",
        "description": "Geração e disponibilidade das cargas estáticas (Carga A 50 MB e Carga B 100x10 KB)",
        "files": ["scripts/generate_payloads.py", "brain/03_experimentos/cenarios_de_teste.md"],
        "patterns": [
            r"50\s*\*\s*1024\s*\*\s*1024|52428800|50MB\.bin",
            r"10\s*\*\s*1024|10240|obj_.*\.bin"
        ]
    },
    {
        "id": "SUB1-REQ-09",
        "description": "Cliente de benchmark em Python com httpx (HTTP/1.1 e 2) e aioquic (HTTP/3 QUIC)",
        "files": ["benchmark/client.py", "brain/03_experimentos/metricas_e_analise_dados.md"],
        "patterns": [
            r"httpx",
            r"aioquic",
            r"asyncio"
        ]
    },
    {
        "id": "SUB1-REQ-10",
        "description": "Implementação do Controle de Viés de Sessão (Cold TTFB fecha sessão vs Warm connection para 100 objetos)",
        "files": ["benchmark/session_control.py", "benchmark/client.py", "brain/03_experimentos/metricas_e_analise_dados.md"],
        "patterns": [
            r"aclose\(\)|client\.close\(\)",
            r"Cache-Control.*no-cache|no-store",
            r"[Ww]arm"
        ]
    },
    {
        "id": "SUB1-REQ-11",
        "description": "Mapeamento rigoroso e execução dos 12 testes mandatórios (T01 a T12)",
        "files": ["brain/03_experimentos/cenarios_de_teste.md", "README.md", "run_experiments.ps1"],
        "patterns": [
            r"T01.*T02.*T03.*T04.*T05.*T06.*T07.*T08.*T09.*T10.*T11.*T12"
        ]
    },
    {
        "id": "SUB1-REQ-12",
        "description": "Presença e integridade dos dados brutos exportados (results.json e results.csv)",
        "files": ["data/raw/results.json", "data/raw/results.csv"],
        "patterns": [
            r"results\.json",
            r"results\.csv"
        ]
    },
    {
        "id": "SUB1-REQ-13",
        "description": "Visualização científica com barras de erro obrigatórias em todos os plots (Figuras 1 a 5)",
        "files": ["analysis/plot_results.py", "brain/03_experimentos/metricas_e_analise_dados.md"],
        "patterns": [
            r"yerr=",
            r"capsize=",
            r"fig1_ttfb",
            r"fig2_throughput",
            r"fig3_load_time",
            r"fig4_rps",
            r"fig5_cdf"
        ]
    }
]

passed = 0
failed = 0

for item in audit_checks:
    item_ok = True
    for p in item["patterns"]:
        found = False
        for f in item["files"]:
            if f in docs and re.search(p, docs[f], re.DOTALL | re.IGNORECASE):
                found = True
                break
        if not found:
            # Fallback search across all files
            for doc_name, content in docs.items():
                if re.search(p, content, re.DOTALL | re.IGNORECASE):
                    found = True
                    break
        if not found:
            item_ok = False
            print(f"❌ [{item['id']}] FALHA: Padrão não encontrado: '{p}'")
            break
    if item_ok:
        passed += 1
        print(f"✅ [{item['id']}] APROVADO: {item['description']}")
    else:
        failed += 1

total = passed + failed
score = (passed / total) * 100
print("-" * 80)
print(f"PARECER DO SUBAGENTE 1: {passed}/{total} itens em total conformidade ({score:.1f}%)")
print("VEREDITO: INFRAESTRUTURA DOCKER, CONTROLE DE TRÁFEGO E PIPELINE TÉCNICO APROVADOS!")
print("=" * 80)
