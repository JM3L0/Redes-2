#!/usr/bin/env python3
"""
Gerenciador de Emulação de Rede com Linux Traffic Control (tc netem) — 3ª Avaliação (N3).
Implementa rigorosamente os 3 cenários especificados na Seção 3 do edital:
- Cenário 1 (lan): Atraso unidirecional de 0.5 ms (RTT total = 1 ms) e 0% de perda.
- Cenário 2 (wan_loss): Atraso unidirecional de 25 ms (RTT total = 50 ms) e 2% de perda estocástica.
- Cenário 3 (wan_noloss): Atraso unidirecional de 25 ms (RTT total = 50 ms) e 0% de perda.
- Limpeza (clean): Remove as regras tc qdisc das interfaces eth0.
"""

import subprocess
import sys

CONTAINERS_ALL = ["server_tcp_cc", "server_http3_quic", "client_bench"]


def run_cmd(cmd: list[str], ignore_errors: bool = False):
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0 and not ignore_errors:
        print(f"[!] Aviso ao executar {' '.join(cmd)}: {res.stderr.strip()}")
    return res


def clean_netem():
    print("[*] Limpando interfaces de rede (tc qdisc del dev eth0 root)...")
    for c in CONTAINERS_ALL:
        run_cmd(["docker", "exec", "--privileged", c, "tc", "qdisc", "del", "dev", "eth0", "root"], ignore_errors=True)


def apply_lan():
    clean_netem()
    print("[*] Aplicando Cenário 1 (LAN - Canal Ideal: delay 0.5ms -> RTT = 1 ms, 0% perda)...")
    for c in ["server_tcp_cc", "server_http3_quic", "client_bench"]:
        run_cmd([
            "docker", "exec", "--privileged", c,
            "tc", "qdisc", "add", "dev", "eth0", "root", "netem", "delay", "0.5ms"
        ])


def apply_wan_loss():
    clean_netem()
    print("[*] Aplicando Cenário 2 (WAN - Canal Degradado: delay 25ms loss 2% -> RTT = 50 ms, 2% perda)...")
    for c in ["server_tcp_cc", "server_http3_quic", "client_bench"]:
        run_cmd([
            "docker", "exec", "--privileged", c,
            "tc", "qdisc", "add", "dev", "eth0", "root", "netem", "delay", "25ms", "loss", "2%"
        ])


def apply_wan_noloss():
    clean_netem()
    print("[*] Aplicando Cenário 3 (WAN sem Perda - Isolamento Handshake: delay 25ms -> RTT = 50 ms, 0% perda)...")
    for c in ["server_http3_quic", "client_bench"]:
        run_cmd([
            "docker", "exec", "--privileged", c,
            "tc", "qdisc", "add", "dev", "eth0", "root", "netem", "delay", "25ms"
        ])


if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "clean"
    if mode in ("lan", "cenario1", "1"):
        apply_lan()
    elif mode in ("wan_loss", "wan", "cenario2", "2"):
        apply_wan_loss()
    elif mode in ("wan_noloss", "handshake", "cenario3", "3"):
        apply_wan_noloss()
    elif mode in ("clean", "clear", "del", "reset"):
        clean_netem()
    else:
        print(f"Uso: python {sys.argv[0]} [lan | wan_loss | wan_noloss | clean]")
        sys.exit(1)
