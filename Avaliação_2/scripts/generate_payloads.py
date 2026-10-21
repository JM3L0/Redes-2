#!/usr/bin/env python3
"""
Gera os payloads sinteticos padronizados para o estudo experimental:
1. Carga A (Regime Permanente / Throughput): 1 arquivo de 50 MB (50MB.bin).
2. Carga B (Multiplexacao / Latencia): 100 arquivos independentes de 10 KB cada (objects/obj_001.bin a obj_100.bin).
"""

import os
import sys

def generate_payloads(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    objects_dir = os.path.join(output_dir, "objects")
    os.makedirs(objects_dir, exist_ok=True)

    # 1. Carga A: 50 MB (50 * 1024 * 1024 bytes)
    file_50mb = os.path.join(output_dir, "50MB.bin")
    size_50mb = 50 * 1024 * 1024  # 52,428,800 bytes
    
    print(f"[*] Gerando Carga A: {file_50mb} (50 MB)...")
    if os.path.exists(file_50mb) and os.path.getsize(file_50mb) == size_50mb:
        print("    [!] Arquivo 50MB.bin ja existe e possui tamanho correto. Pulando recriacao.")
    else:
        chunk_size = 1024 * 1024  # 1 MB chunk
        pattern = os.urandom(chunk_size)
        with open(file_50mb, "wb") as f:
            for _ in range(50):
                f.write(pattern)
        print("    [+] 50MB.bin gerado com sucesso!")

    # 2. Carga B: 100 arquivos de 10 KB cada
    size_10kb = 10 * 1024  # 10,240 bytes
    print(f"[*] Gerando Carga B: 100 arquivos de 10 KB em {objects_dir}...")
    existing_count = 0
    for i in range(1, 101):
        filename = f"obj_{i:03d}.bin"
        filepath = os.path.join(objects_dir, filename)
        if os.path.exists(filepath) and os.path.getsize(filepath) == size_10kb:
            existing_count += 1
            continue
        header = f"OBJECT_ID_{i:03d}\n".encode("utf-8")
        body = b"X" * (size_10kb - len(header))
        with open(filepath, "wb") as f:
            f.write(header + body)

    if existing_count == 100:
        print("    [!] Todos os 100 objetos de 10 KB ja existem. Pulando recriacao.")
    else:
        print("    [+] 100 objetos de 10 KB gerados com sucesso!")

    print("[OK] Todos os payloads sinteticos prontos para os experimentos.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(base_dir, "data", "static")
    generate_payloads(static_dir)
