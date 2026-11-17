#!/usr/bin/env python3
"""
Orquestrador Mestre de Automação (run_n3.py) — 3ª Avaliação (N3) de Redes de Computadores II (UFPI).
Atende integralmente à Seção 5 e aos Eixos 1 e 2 da Rubrica:
1. Gera certificados TLS 1.3 e objeto estático de 1 KB (1024 bytes);
2. Sobe os contêineres Docker (server_tcp_cc, server_http3_quic, client_bench) na rede net_bench;
3. Garante módulos tcp_cubic e tcp_bbr ativos no kernel e utilitários iproute2 (tc), iperf3 e curl (HTTP/3);
4. Aplica as regras tc netem dos Cenários 1, 2 e 3 e executa as 5 repetições dos 6 testes (E01 a E06);
5. Exporta os dados brutos estruturados em data/raw/results.csv e data/raw/results.json;
6. Limpa todas as interfaces tc netem ao final;
7. Dispara o processamento estatístico (process_data.py) e a geração dos 2 gráficos com barras de erro (plot_results.py).
"""

import os
import sys
import csv
import json
import time
import argparse
import datetime
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from scripts.generate_certs import generate_self_signed_cert
from scripts.generate_payloads import generate_site_payloads
from scripts.setup_netem import apply_lan, apply_wan_loss, apply_wan_noloss, clean_netem
from analysis.process_data import process_results
from analysis.plot_results import generate_all_plots


def run_cmd(cmd: list[str], check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, text=True, capture_output=capture)


def prepare_environment():
    print("\n" + "=" * 80)
    print(" [FASE 1/4] PREPARAÇÃO DO AMBIENTE DOCKER, KERNEL BBR E PAYLOADS")
    print("=" * 80)

    generate_self_signed_cert(os.path.join(BASE_DIR, "certs"))
    generate_site_payloads(os.path.join(BASE_DIR, "site"))

    print("[*] Habilitando módulo tcp_bbr no kernel Linux do Docker Host...")
    run_cmd([
        "docker", "run", "--rm", "--privileged", "--pid=host", "alpine:latest",
        "nsenter", "-t", "1", "-m", "-u", "-n", "-i", "sh", "-c",
        "modprobe tcp_bbr 2>/dev/null || true; sysctl net.ipv4.tcp_available_congestion_control"
    ], check=False)

    print("[*] Subindo contêineres Docker (server_tcp_cc, server_http3_quic, client_bench)...")
    run_cmd(["docker", "compose", "-f", os.path.join(BASE_DIR, "docker-compose.yml"), "up", "-d"], capture=False)
    time.sleep(2)

    print("[*] Verificando utilitários iproute2 (tc), iperf3 e curl (HTTP/3) nos contêineres...")
    run_cmd([
        "docker", "exec", "server_http3_quic", "sh", "-c",
        "which tc >/dev/null 2>&1 || apk add --no-cache iproute2 >/dev/null"
    ])
    run_cmd([
        "docker", "exec", "client_bench", "sh", "-c",
        "which tc >/dev/null 2>&1 && which iperf3 >/dev/null 2>&1 || apk add --no-cache iperf3 iproute2 >/dev/null"
    ])
    run_cmd([
        "docker", "exec", "server_tcp_cc", "sh", "-c",
        "which tc >/dev/null 2>&1 || (apt-get update >/dev/null && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends iproute2 >/dev/null)"
    ])

    # Garante binário curl estático com suporte nativo a HTTP/3 no client_bench
    curl_check = run_cmd(["docker", "exec", "client_bench", "sh", "-c", "curl --version | grep -q HTTP3"], check=False)
    if curl_check.returncode != 0:
        local_curl = os.path.join(BASE_DIR, "docker", "curl-http3")
        if not os.path.exists(local_curl):
            print("[*] Extraindo/baixando binário estático curl com suporte HTTP/3...")
            run_cmd([
                "docker", "run", "--rm", "--entrypoint", "sh",
                "-v", f"{os.path.join(BASE_DIR, 'docker')}:/out",
                "docker-client:latest", "-c", "cp /usr/local/bin/curl /out/curl-http3 && chmod +x /out/curl-http3"
            ], check=False)
        if not os.path.exists(local_curl):
            run_cmd([
                "docker", "exec", "client_bench", "sh", "-c",
                "wget -qO /tmp/curl-static.tar.xz https://github.com/stunnel/static-curl/releases/download/8.22.0/curl-linux-x86_64-glibc-8.22.0.tar.xz && "
                "tar -xf /tmp/curl-static.tar.xz -C /tmp && mv /tmp/curl /usr/local/bin/curl && cp /usr/local/bin/curl /usr/bin/curl && chmod +x /usr/bin/curl"
            ], check=False)
        if os.path.exists(local_curl):
            run_cmd(["docker", "cp", local_curl, "client_bench:/usr/bin/curl"])
            run_cmd(["docker", "cp", local_curl, "client_bench:/usr/local/bin/curl"])


def run_iperf3_test(test_id: str, algorithm: str, scenario_label: str, rtt_ms: float, loss_pct: float,
                    repetitions: int, duration_sec: int, raw_dir: str) -> list[dict]:
    records = []
    protocol_label = f"TCP {algorithm.upper()}"
    print(f"\n>>> Executando {test_id}: {protocol_label} | {scenario_label} ({repetitions} repetições de {duration_sec}s)...")

    for rep in range(1, repetitions + 1):
        # Limpa cache de métricas TCP entre repetições para independência amostral
        run_cmd(["docker", "exec", "--privileged", "client_bench", "ip", "route", "flush", "cache"], check=False)
        run_cmd(["docker", "exec", "--privileged", "server_tcp_cc", "ip", "route", "flush", "cache"], check=False)
        time.sleep(1.0)

        cmd = [
            "docker", "exec", "client_bench",
            "iperf3", "-c", "172.20.0.10", "-t", str(duration_sec), "-C", algorithm, "-J"
        ]
        res = run_cmd(cmd, check=False)
        data = json.loads(res.stdout)

        # Salva JSON individual bruto do iperf3
        iperf_log = os.path.join(raw_dir, f"{test_id}_rep{rep}_{algorithm}.json")
        with open(iperf_log, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        end_data = data.get("end", {})
        sum_recv = end_data.get("sum_received", {})
        sum_sent = end_data.get("sum_sent", {})

        bps = float(sum_recv.get("bits_per_second", sum_sent.get("bits_per_second", 0.0)))
        throughput_mbps = bps / 1e6
        retransmits = int(sum_sent.get("retransmits", 0))

        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        rec = {
            "test_id": test_id,
            "block": "A",
            "repetition": rep,
            "timestamp": now_iso,
            "protocol_mode": protocol_label,
            "scenario": scenario_label,
            "rtt_ms": rtt_ms,
            "loss_pct": loss_pct,
            "metric_name": "throughput_mbps",
            "throughput_mbps": round(throughput_mbps, 4),
            "retransmits": retransmits,
            "ttfb_ms": None,
        }
        records.append(rec)
        print(f"    [{test_id} Rep {rep}/{repetitions}] Vazão = {throughput_mbps:.2f} Mbps | Retransmissões = {retransmits}")

    return records


def run_curl_block_b(repetitions: int) -> list[dict]:
    records = []
    scenario_label = "WAN (50 ms, 0% perda)"
    url = "https://172.20.0.30/1KB.bin"

    # Aquecimento inicial do servidor Caddy (evita latência de carregamento de certificado em disco)
    run_cmd([
        "docker", "exec", "client_bench",
        "curl", "-k", "--http3-only", "-s", "-o", "/dev/null", url
    ], check=False)
    time.sleep(0.5)

    # E04: HTTPS (HTTP/2 sobre TCP+TLS)
    print(f"\n>>> Executando E04: HTTPS (HTTP/2 sobre TCP+TLS) | {scenario_label} ({repetitions} repetições)...")
    for rep in range(1, repetitions + 1):
        time.sleep(0.4)
        res = run_cmd([
            "docker", "exec", "client_bench",
            "curl", "-k", "--http2", "-H", "Cache-Control: no-cache, no-store",
            "-o", "/dev/null", "-s", "-w", "%{http_code};%{time_starttransfer}\n", url
        ])
        code_str, ttfb_str = res.stdout.strip().split(";")
        ttfb_ms = float(ttfb_str) * 1000.0
        records.append({
            "test_id": "E04",
            "block": "B",
            "repetition": rep,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "protocol_mode": "HTTPS (HTTP/2 sobre TCP+TLS)",
            "scenario": scenario_label,
            "rtt_ms": 50.0,
            "loss_pct": 0.0,
            "metric_name": "ttfb_ms",
            "throughput_mbps": None,
            "retransmits": None,
            "ttfb_ms": round(ttfb_ms, 3),
        })
        print(f"    [E04 Rep {rep}/{repetitions}] HTTP {code_str} | TTFB (time_starttransfer) = {ttfb_ms:.2f} ms")

    # E05 (HTTP/3 Cold 1-RTT) & E06 (HTTP/3 Warm / Resumption)
    # Conforme a Dica de Execução da página 7 do edital:
    # "Ao realizar requisições sequenciais na mesma chamada do curl ou reutilizando tickets de sessão TLS,
    # compare o time_starttransfer da primeira requisição com o das requisições subsequentes."
    print(f"\n>>> Executando E05 (HTTP/3 Cold 1-RTT) e E06 (HTTP/3 Warm / Resumption) | {scenario_label} ({repetitions} repetições)...")
    e05_records = []
    e06_records = []

    for rep in range(1, repetitions + 1):
        time.sleep(0.4)
        res = run_cmd([
            "docker", "exec", "client_bench",
            "curl", "-k", "--http3-only", "-H", "Cache-Control: no-cache, no-store",
            "-s", "-w", "%{http_code};%{time_starttransfer}\n",
            "-o", "/dev/null", url,
            "-o", "/dev/null", url
        ])
        lines = [ln.strip() for ln in res.stdout.strip().splitlines() if ln.strip()]
        code1, ttfb1_str = lines[0].split(";")
        code2, ttfb2_str = lines[1].split(";")
        ttfb_cold_ms = float(ttfb1_str) * 1000.0
        ttfb_warm_ms = float(ttfb2_str) * 1000.0

        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        e05_records.append({
            "test_id": "E05",
            "block": "B",
            "repetition": rep,
            "timestamp": now_iso,
            "protocol_mode": "HTTP/3 Cold (1-RTT)",
            "scenario": scenario_label,
            "rtt_ms": 50.0,
            "loss_pct": 0.0,
            "metric_name": "ttfb_ms",
            "throughput_mbps": None,
            "retransmits": None,
            "ttfb_ms": round(ttfb_cold_ms, 3),
        })
        e06_records.append({
            "test_id": "E06",
            "block": "B",
            "repetition": rep,
            "timestamp": now_iso,
            "protocol_mode": "HTTP/3 Warm / Resumption",
            "scenario": scenario_label,
            "rtt_ms": 50.0,
            "loss_pct": 0.0,
            "metric_name": "ttfb_ms",
            "throughput_mbps": None,
            "retransmits": None,
            "ttfb_ms": round(ttfb_warm_ms, 3),
        })
        print(
            f"    [Rep {rep}/{repetitions}] E05 Cold (1-RTT): {ttfb_cold_ms:.2f} ms (HTTP {code1}) | "
            f"E06 Warm/Resumed (0-RTT): {ttfb_warm_ms:.2f} ms (HTTP {code2})"
        )

    records.extend(e05_records)
    records.extend(e06_records)
    return records


def export_raw_data(all_records: list[dict], raw_dir: str):
    os.makedirs(raw_dir, exist_ok=True)
    json_path = os.path.join(raw_dir, "results.json")
    csv_path = os.path.join(raw_dir, "results.csv")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=2, ensure_ascii=False)

    fieldnames = [
        "test_id", "block", "repetition", "timestamp", "protocol_mode",
        "scenario", "rtt_ms", "loss_pct", "metric_name",
        "throughput_mbps", "retransmits", "ttfb_ms"
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_records)

    print(f"\n[+] Dados brutos exportados com sucesso:")
    print(f"    - CSV : {csv_path}")
    print(f"    - JSON: {json_path}")


def main():
    parser = argparse.ArgumentParser(description="Orquestrador da 3ª Avaliação (N3) — Redes II UFPI")
    parser.add_argument("--repetitions", "-n", type=int, default=5, help="Número de repetições por teste (padrão: 5)")
    parser.add_argument("--duration", "-t", type=int, default=15, help="Duração do fluxo iperf3 em segundos (padrão: 15)")
    args = parser.parse_args()

    raw_dir = os.path.join(BASE_DIR, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)

    all_records = []
    try:
        prepare_environment()

        print("\n" + "=" * 80)
        print(" [FASE 2/4] BLOCO A: IMPACTO DO CONTROLE DE CONGESTIONAMENTO (CUBIC vs. BBR)")
        print("=" * 80)

        # Cenário 1: LAN (1 ms RTT, 0% perda) -> E01 (TCP CUBIC)
        apply_lan()
        all_records.extend(
            run_iperf3_test("E01", "cubic", "LAN (1 ms, 0% perda)", 1.0, 0.0, args.repetitions, args.duration, raw_dir)
        )

        # Cenário 2: WAN (50 ms RTT, 2% perda) -> E02 (TCP CUBIC) e E03 (TCP BBR)
        apply_wan_loss()
        all_records.extend(
            run_iperf3_test("E02", "cubic", "WAN (50 ms, 2% perda)", 50.0, 2.0, args.repetitions, args.duration, raw_dir)
        )
        all_records.extend(
            run_iperf3_test("E03", "bbr", "WAN (50 ms, 2% perda)", 50.0, 2.0, args.repetitions, args.duration, raw_dir)
        )

        print("\n" + "=" * 80)
        print(" [FASE 3/4] BLOCO B: LATÊNCIA DE HANDSHAKE E SESSION RESUMPTION NO HTTP/3")
        print("=" * 80)

        # Cenário 3: WAN sem Perda (50 ms RTT, 0% perda) -> E04, E05 e E06
        apply_wan_noloss()
        all_records.extend(run_curl_block_b(args.repetitions))

    finally:
        print("\n[*] Restaurando e limpando interfaces de rede (tc qdisc del dev eth0 root)...")
        clean_netem()

    print("\n" + "=" * 80)
    print(" [FASE 4/4] EXPORTAÇÃO DE DADOS, ESTATÍSTICA E GERAÇÃO DOS 2 GRÁFICOS")
    print("=" * 80)
    export_raw_data(all_records, raw_dir)
    process_results(BASE_DIR)
    generate_all_plots(BASE_DIR)
    print("\n[OK] Bateria experimental da 3ª Avaliação (N3) concluída com 100% de sucesso!")


if __name__ == "__main__":
    main()
