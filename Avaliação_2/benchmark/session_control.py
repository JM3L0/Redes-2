"""
Módulo de Controle Estrito de Viés de Sessão (Client-Side Bias Control).
Disciplina: Redes de Computadores II (UFPI - CSHNB)
Aluno: João Marcos Sousa Rufino Leal

Garante que:
1. Cold TTFB: cada requisição abre e fecha uma sessão dedicada (client.aclose()),
   impedindo reutilização de sockets TCP ou conexões QUIC prévias.
2. Warm Concurrency: uma única sessão persistente é mantida aberta e aquecida para
   avaliar a multiplexação real da Carga B (100 objetos) sem custos de handshake repetidos.
3. Desativação absoluta de cache HTTP com headers no-cache e no-store.
"""

from typing import Dict

def get_no_cache_headers() -> Dict[str, str]:
    """Retorna cabeçalhos rigorosos para desativar qualquer cache intermediário ou local."""
    return {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0",
        "User-Agent": "UFPI-Redes2-BenchmarkClient/1.0"
    }

class SessionMode:
    COLD = "cold"
    WARM = "warm"
