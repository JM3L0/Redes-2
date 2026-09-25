#!/usr/bin/env python3
"""
Gera os ficheiros estaticos necessarios para os ensaios experimentais:
1. index.html - Pagina basica de teste
2. 100MB.bin  - Carga media para Cenario B
3. 1GB.bin    - Carga massiva para Cenario B
4. objects/   - 100 arquivos independentes (~50 KB cada) para simulacao de lote web no Cenario C
"""
import os
import sys

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "static"))
    os.makedirs(base_dir, exist_ok=True)
    objects_dir = os.path.join(base_dir, "objects")
    os.makedirs(objects_dir, exist_ok=True)

    print(f"[*] Gerando dados estaticos em: {base_dir}")

    # 1. index.html
    index_path = os.path.join(base_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html><html><head><title>UFPI Redes 2 - HTTP/3 QUIC Server</title></head>"
                "<body><h1>Servidor NGINX HTTP/1.1, HTTP/2 e HTTP/3 (QUIC)</h1>"
                "<p>Ambiente experimental de Redes de Computadores II (2026-2) - UFPI</p></body></html>\n")
    print("  [+] index.html criado.")

    # 2. 100MB.bin (104,857,600 bytes)
    mb100_path = os.path.join(base_dir, "100MB.bin")
    if not os.path.exists(mb100_path) or os.path.getsize(mb100_path) != 100 * 1024 * 1024:
        print("  [+] Gerando 100MB.bin...")
        chunk = b"X" * (1024 * 1024) # 1 MB chunk
        with open(mb100_path, "wb") as f:
            for _ in range(100):
                f.write(chunk)
        print("  [+] 100MB.bin gerado com sucesso (100 MB).")
    else:
        print("  [=] 100MB.bin ja existe.")

    # 3. 1GB.bin (1,073,741,824 bytes)
    gb1_path = os.path.join(base_dir, "1GB.bin")
    if not os.path.exists(gb1_path) or os.path.getsize(gb1_path) != 1024 * 1024 * 1024:
        print("  [+] Gerando 1GB.bin...")
        chunk = b"Y" * (4 * 1024 * 1024) # 4 MB chunk
        with open(gb1_path, "wb") as f:
            for _ in range(256):
                f.write(chunk)
        print("  [+] 1GB.bin gerado com sucesso (1 GB).")
    else:
        print("  [=] 1GB.bin ja existe.")

    # 4. 100 pequenos objetos web de 50 KB cada
    print("  [+] Verificando/Gerando 100 objetos web em objects/...")
    obj_chunk = b"Z" * (50 * 1024) # 50 KB cada
    for i in range(1, 101):
        obj_name = f"obj_{i:03d}.bin"
        obj_path = os.path.join(objects_dir, obj_name)
        if not os.path.exists(obj_path) or os.path.getsize(obj_path) != 50 * 1024:
            with open(obj_path, "wb") as f:
                f.write(obj_chunk)
    print("  [+] 100 objetos (obj_001.bin a obj_100.bin) prontos.")

    print("[*] Concluido com sucesso!")

if __name__ == "__main__":
    main()
