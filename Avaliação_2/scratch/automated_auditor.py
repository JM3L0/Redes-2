import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\jsous\Desktop\Redes 2\Avaliação_2"

checks = [
    {
        "category": "1. Infraestrutura Docker & Servidores Web",
        "tests": [
            ("server_http11 em Nginx na porta 8080", r"server_http11.*8080"),
            ("server_http2_tls em Nginx na porta 8443", r"server_http2_tls.*8443"),
            ("server_http3_quic em Caddy na porta 9443", r"server_http3_quic.*9443"),
            ("Rede net_bench 172.20.0.0/16", r"172\.20\.0\.0/16"),
            ("IPs estáticos 172.20.0.10, .20, .30", r"172\.20\.0\.10.*172\.20\.0\.20.*172\.20\.0\.30"),
            ("Permissão de kernel cap_add: NET_ADMIN", r"cap_add:.*NET_ADMIN"),
            ("Certificados TLS 1.3 locais com SANs", r"TLS.*1\.3.*SAN|Subject Alternative Name"),
        ]
    },
    {
        "category": "2. Emulação com tc netem",
        "tests": [
            ("Cenário 1 (LAN: delay 0.5ms = RTT 1ms, 0% perda)", r"0\.5ms.*1(\.0)?ms"),
            ("Cenário 2 (WAN: delay 25ms = RTT 50ms, 2% perda)", r"25ms.*50(\.0)?ms.*2%"),
            ("Justificativa matemática do atraso unidirecional RTT/2", r"RTT/2|delay.*RTT"),
            ("Comando de aplicação do netem", r"tc qdisc add dev eth0 root netem"),
            ("Comando de limpeza do netem", r"tc qdisc del dev eth0 root"),
        ]
    },
    {
        "category": "3. Cliente de Benchmark em Python",
        "tests": [
            ("Módulos httpx e aioquic", r"httpx.*aioquic"),
            ("Controle de Viés: desativação de cache", r"Cache-Control.*no-(store|cache)"),
            ("Controle de Viés: Cold TTFB com fechamento explícito", r"client\.close\(\)|aclose\(\)"),
            ("Controle de Viés: Warm Connection para multiplexação", r"[Ww]arm.*connection|[Cc]onexão.*aquecida"),
            ("Métricas: TTFB, Load Time, RPS, p50, p99", r"TTFB.*Load Time.*RPS.*p50.*p99"),
            ("Exportação para results.json e results.csv", r"results\.json.*results\.csv"),
        ]
    },
    {
        "category": "4. Perfis de Carga e Matriz Experimental (12 Testes)",
        "tests": [
            ("Carga A (50 MB)", r"50\s*MB"),
            ("Carga B (100 objetos de 10 KB)", r"100.*10\s*KB"),
            ("Testes T01 a T06 (Carga A)", r"T01.*T02.*T03.*T04.*T05.*T06"),
            ("Testes T07 a T12 (Carga B)", r"T07.*T08.*T09.*T10.*T11.*T12"),
            ("Rigor estatístico N >= 10 repetições", r"N\s*>=\s*10|10 repetições"),
            ("Intervalo de Confiança de 95% (t-Student)", r"95%|t-Student"),
        ]
    },
    {
        "category": "5. Rubricas, Penalidades e Regras Críticas",
        "tests": [
            ("Rubrica de 100 pontos detalhada (25, 25, 20, 30)", r"25.*25.*20.*30"),
            ("Penalidade -15 pts (sem runner 1-click)", r"-15.*(run_experiments|comando único)"),
            ("Penalidade -10 pts (sem controle de viés no TTFB)", r"-10.*viés|bias"),
            ("Penalidade -10 pts (sem barras de erro nos gráficos)", r"-10.*barras de erro"),
            ("Penalidade -20 pts (relatório descritivo sem Tanenbaum)", r"-20.*Tanenbaum"),
            ("Critério Eliminatório NOTA ZERO (código, relatório, vídeo)", r"NOTA ZERO|Nota [Zz]ero"),
            ("Fundamentação Tanenbaum §6.5.11 (TCP CUBIC)", r"6\.5\.11.*CUBIC"),
            ("Fundamentação Tanenbaum §6.6.1 (QUIC) e §6.6.2 (BBR)", r"6\.6\.1.*QUIC.*6\.6\.2.*BBR"),
            ("Roteiro do Vídeo de 15 minutos cronometrado", r"15 minutos.*(00:00|roteiro)"),
            ("Arquivo ZIP no padrão do edital", r"TP2_Redes2_NomeAluno"),
        ]
    }
]

# Read all brain files concatenated
all_text = ""
file_list = []
for root, dirs, files in os.walk(base_dir):
    if "scratch" in root or ".git" in root:
        continue
    for f in files:
        if f.endswith(".md"):
            p = os.path.join(root, f)
            file_list.append(os.path.relpath(p, base_dir))
            with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                all_text += f"\n--- {f} ---\n" + fh.read()

print("="*70)
print("AUDITORIA PROGRAMÁTICA DO CÉREBRO — AVALIAÇÃO 2")
print(f"Arquivos analisados ({len(file_list)}): {', '.join(file_list)}")
print("="*70)

total_tests = 0
passed_tests = 0

for group in checks:
    print(f"\n📁 {group['category']}")
    for name, pattern in group["tests"]:
        total_tests += 1
        match = re.search(pattern, all_text, re.DOTALL | re.IGNORECASE)
        if match:
            passed_tests += 1
            print(f"  [ PASS ] {name}")
        else:
            print(f"  [ FAIL ] {name} (Padrão não encontrado: {pattern})")

score = (passed_tests / total_tests) * 100
print("\n" + "="*70)
print(f"RESULTADO FINAL: {passed_tests}/{total_tests} testes aprovados ({score:.1f}% de conformidade)")
print("="*70)
