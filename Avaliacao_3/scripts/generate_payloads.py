#!/usr/bin/env python3
"""
Gera deterministicamente o objeto estático de 1 KB (1024 bytes) no diretório ./site
para os testes de latência de Handshake e Session Resumption do Bloco B (E04, E05 e E06).
"""

import os
import hashlib


def generate_site_payloads(site_dir: str):
    os.makedirs(site_dir, exist_ok=True)

    # Objeto de exatos 1024 bytes (1 KB) conforme exigido na Seção 4 (Bloco B) do edital
    payload_1kb_path = os.path.join(site_dir, "1KB.bin")
    index_path = os.path.join(site_dir, "index.html")

    seed_block = hashlib.sha256(b"UFPI-CSHNB-REDES2-N3-1KB-PAYLOAD").digest()
    data_1kb = (seed_block * 32)[:1024]

    with open(payload_1kb_path, "wb") as f:
        f.write(data_1kb)

    # Também disponibiliza index.html com exatos 1024 bytes para chamadas na raiz /
    header = (
        b"<!DOCTYPE html><html><head><title>UFPI Redes II N3</title></head>"
        b"<body><!-- "
    )
    footer = b" --></body></html>\n"
    pad_len = 1024 - len(header) - len(footer)
    html_1kb = header + (b"X" * pad_len) + footer

    with open(index_path, "wb") as f:
        f.write(html_1kb)

    print(f"[+] Payload de 1 KB gerado em {payload_1kb_path} ({os.path.getsize(payload_1kb_path)} bytes)")
    print(f"[+] Index de 1 KB gerado em {index_path} ({os.path.getsize(index_path)} bytes)")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    site_dir = os.path.join(base_dir, "site")
    generate_site_payloads(site_dir)
