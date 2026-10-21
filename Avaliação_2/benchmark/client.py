#!/usr/bin/env python3
"""
Cliente Assíncrono de Benchmark para Avaliação Experimental de Protocolos Web
(HTTP/1.1 vs HTTPS/TLS 1.3/HTTP/2 vs HTTP/3-QUIC).

Disciplina: Redes de Computadores II (UFPI - CSHNB)
Aluno: João Marcos Sousa Rufino Leal (jsousarufinoleal@ufpi.edu.br)

Atende rigorosamente a todas as especificações do edital:
1. Chamadas assíncronas via httpx (HTTP/1.1 e HTTP/2) e aioquic (HTTP/3).
2. Controle Estrito de Viés de Sessão (Client-Side Bias Control):
   - Cold TTFB: client.aclose() explícito antes de cada requisição individual.
   - Warm Concurrency: canal persistente único aquecido para download simultâneo de 100 objetos.
   - Desativação absoluta de cache HTTP local.
3. Precisão temporal de microssegundos via time.perf_counter().
4. Mapeamento completo dos 12 testes (T01 a T12) com Cargas A (50 MB) e B (100x10 KB).
5. Exportação para results.json e results.csv.
"""

import os
import sys
import time
import ssl
import asyncio
import datetime
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

import httpx
from aioquic.asyncio.client import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.h3.connection import H3_ALPN, H3Connection
from aioquic.h3.events import HeadersReceived, DataReceived

# Importa módulos internos do benchmark
from session_control import get_no_cache_headers, SessionMode
from metrics import RequestMetric, MetricsCollector

# ==============================================================================
# CLIENTE HTTP/3 SOBRE QUIC (aioquic)
# ==============================================================================

class H3BenchmarkProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._http = H3Connection(self._quic)
        self.stream_futures: Dict[int, asyncio.Future] = {}
        self.stream_data: Dict[int, bytearray] = {}
        self.stream_status: Dict[int, int] = {}
        self.stream_ttfb: Dict[int, float] = {}
        self.stream_start: Dict[int, float] = {}

    def quic_event_received(self, event):
        if self._http is not None:
            for http_event in self._http.handle_event(event):
                if isinstance(http_event, HeadersReceived):
                    stream_id = http_event.stream_id
                    now = time.perf_counter()
                    if stream_id in self.stream_start and stream_id not in self.stream_ttfb:
                        self.stream_ttfb[stream_id] = now
                    for name, value in http_event.headers:
                        if name == b":status":
                            self.stream_status[stream_id] = int(value.decode("ascii"))
                elif isinstance(http_event, DataReceived):
                    stream_id = http_event.stream_id
                    now = time.perf_counter()
                    if stream_id in self.stream_start and stream_id not in self.stream_ttfb:
                        self.stream_ttfb[stream_id] = now
                    if stream_id in self.stream_data:
                        self.stream_data[stream_id].extend(http_event.data)
                    if http_event.stream_ended:
                        if stream_id in self.stream_futures and not self.stream_futures[stream_id].done():
                            self.stream_futures[stream_id].set_result(True)

    async def fetch_path(self, path: str, authority: str) -> Dict[str, Any]:
        stream_id = self._quic.get_next_available_stream_id()
        fut = asyncio.get_running_loop().create_future()
        self.stream_futures[stream_id] = fut
        self.stream_data[stream_id] = bytearray()
        
        headers = [
            (b":method", b"GET"),
            (b":scheme", b"https"),
            (b":authority", authority.encode("ascii")),
            (b":path", path.encode("ascii")),
            (b"user-agent", b"UFPI-Redes2-H3Client/1.0"),
            (b"cache-control", b"no-cache, no-store"),
        ]
        
        t_start = time.perf_counter()
        self.stream_start[stream_id] = t_start
        
        self._http.send_headers(stream_id=stream_id, headers=headers, end_stream=True)
        self.transmit()

        await asyncio.wait_for(fut, timeout=120.0)
        t_end = time.perf_counter()

        t_first = self.stream_ttfb.get(stream_id, t_end)
        status = self.stream_status.get(stream_id, 200)
        data = self.stream_data.get(stream_id, b"")

        ttfb_ms = (t_first - t_start) * 1000.0
        load_time_ms = (t_end - t_start) * 1000.0
        bytes_len = len(data)
        goodput_mbps = (bytes_len * 8) / ((t_end - t_start) * 1e6) if (t_end - t_start) > 0 else 0.0

        return {
            "status_code": status,
            "ttfb_ms": ttfb_ms,
            "load_time_ms": load_time_ms,
            "bytes_downloaded": bytes_len,
            "goodput_mbps": goodput_mbps,
        }

# ==============================================================================
# EXECUTOR DE BENCHMARK HTTP/1.1 E HTTP/2 (httpx)
# ==============================================================================

async def fetch_httpx_cold(
    url: str,
    http2: bool,
    test_id: str,
    protocol_name: str,
    scenario: str,
    payload_type: str,
    iteration: int,
    request_id: int
) -> RequestMetric:
    """Executa requisição no modo Cold TTFB: conexão isolada, fechamento forçado."""
    headers = get_no_cache_headers()
    t_start = time.perf_counter()
    t_first_byte = None
    bytes_downloaded = 0
    status_code = 0

    async with httpx.AsyncClient(http2=http2, verify=False, timeout=120.0) as client:
        try:
            async with client.stream("GET", url, headers=headers) as response:
                t_first_byte = time.perf_counter()
                status_code = response.status_code
                async for chunk in response.aiter_bytes():
                    bytes_downloaded += len(chunk)
        except Exception as e:
            print(f"[!] Erro no cold fetch {url}: {e}", file=sys.stderr)
            if t_first_byte is None:
                t_first_byte = time.perf_counter()

    t_end = time.perf_counter()
    if t_first_byte is None:
        t_first_byte = t_end

    ttfb_ms = (t_first_byte - t_start) * 1000.0
    load_time_ms = (t_end - t_start) * 1000.0
    duration_s = t_end - t_start
    goodput_mbps = (bytes_downloaded * 8) / (duration_s * 1e6) if duration_s > 0 else 0.0

    return RequestMetric(
        test_id=test_id,
        protocol=protocol_name,
        scenario=scenario,
        payload_type=payload_type,
        iteration=iteration,
        request_id=request_id,
        url=url,
        status_code=status_code,
        ttfb_ms=ttfb_ms,
        load_time_ms=load_time_ms,
        bytes_downloaded=bytes_downloaded,
        goodput_mbps=goodput_mbps,
        mode=SessionMode.COLD,
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    )

async def fetch_httpx_warm_batch(
    base_url: str,
    paths: List[str],
    http2: bool,
    test_id: str,
    protocol_name: str,
    scenario: str,
    payload_type: str,
    iteration: int
) -> List[RequestMetric]:
    """Executa lote de requisições no modo Warm Concurrency: 1 única sessão persistente aquecida."""
    metrics: List[RequestMetric] = []
    headers = get_no_cache_headers()

    limits = httpx.Limits(max_keepalive_connections=100, max_connections=100)
    async with httpx.AsyncClient(http2=http2, verify=False, limits=limits, timeout=120.0) as client:
        # Aquecimento inicial (1 handshake prévio)
        try:
            await client.get(f"{base_url}{paths[0]}", headers=headers)
        except Exception:
            pass

        async def fetch_single(path: str, req_id: int):
            url = f"{base_url}{path}"
            t_start = time.perf_counter()
            t_first = None
            bytes_dl = 0
            code = 0
            try:
                async with client.stream("GET", url, headers=headers) as resp:
                    t_first = time.perf_counter()
                    code = resp.status_code
                    async for chunk in resp.aiter_bytes():
                        bytes_dl += len(chunk)
            except Exception as e:
                if t_first is None:
                    t_first = time.perf_counter()
            t_end = time.perf_counter()
            if t_first is None:
                t_first = t_end
            
            dur = t_end - t_start
            return RequestMetric(
                test_id=test_id,
                protocol=protocol_name,
                scenario=scenario,
                payload_type=payload_type,
                iteration=iteration,
                request_id=req_id,
                url=url,
                status_code=code,
                ttfb_ms=(t_first - t_start) * 1000.0,
                load_time_ms=(dur) * 1000.0,
                bytes_downloaded=bytes_dl,
                goodput_mbps=(bytes_dl * 8) / (dur * 1e6) if dur > 0 else 0.0,
                mode=SessionMode.WARM,
                timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
            )

        tasks = [fetch_single(path, idx + 1) for idx, path in enumerate(paths)]
        results = await asyncio.gather(*tasks)
        metrics.extend(results)

    return metrics

# ==============================================================================
# EXECUTOR DE BENCHMARK HTTP/3 (aioquic)
# ==============================================================================

async def fetch_h3_cold(
    host: str,
    port: int,
    path: str,
    test_id: str,
    protocol_name: str,
    scenario: str,
    payload_type: str,
    iteration: int,
    request_id: int
) -> RequestMetric:
    """Executa requisição HTTP/3 Cold TTFB: conexão QUIC criada e fechada imediatamente."""
    config = QuicConfiguration(is_client=True, alpn_protocols=H3_ALPN)
    config.verify_mode = ssl.CERT_NONE
    authority = f"{host}:{port}"
    url = f"https://{authority}{path}"

    async with connect(host, port, configuration=config, create_protocol=H3BenchmarkProtocol) as client:
        res = await client.fetch_path(path, authority)

    return RequestMetric(
        test_id=test_id,
        protocol=protocol_name,
        scenario=scenario,
        payload_type=payload_type,
        iteration=iteration,
        request_id=request_id,
        url=url,
        status_code=res["status_code"],
        ttfb_ms=res["ttfb_ms"],
        load_time_ms=res["load_time_ms"],
        bytes_downloaded=res["bytes_downloaded"],
        goodput_mbps=res["goodput_mbps"],
        mode=SessionMode.COLD,
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    )

async def fetch_h3_warm_batch(
    host: str,
    port: int,
    paths: List[str],
    test_id: str,
    protocol_name: str,
    scenario: str,
    payload_type: str,
    iteration: int
) -> List[RequestMetric]:
    """Executa requisições HTTP/3 no modo Warm: única conexão persistente QUIC multiplexando streams."""
    metrics: List[RequestMetric] = []
    config = QuicConfiguration(is_client=True, alpn_protocols=H3_ALPN)
    config.verify_mode = ssl.CERT_NONE
    authority = f"{host}:{port}"

    async with connect(host, port, configuration=config, create_protocol=H3BenchmarkProtocol) as client:
        # Aquecimento de 1 stream prévio
        try:
            await client.fetch_path(paths[0], authority)
        except Exception:
            pass

        async def fetch_single(path: str, req_id: int):
            url = f"https://{authority}{path}"
            res = await client.fetch_path(path, authority)
            return RequestMetric(
                test_id=test_id,
                protocol=protocol_name,
                scenario=scenario,
                payload_type=payload_type,
                iteration=iteration,
                request_id=req_id,
                url=url,
                status_code=res["status_code"],
                ttfb_ms=res["ttfb_ms"],
                load_time_ms=res["load_time_ms"],
                bytes_downloaded=res["bytes_downloaded"],
                goodput_mbps=res["goodput_mbps"],
                mode=SessionMode.WARM,
                timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
            )

        tasks = [fetch_single(path, idx + 1) for idx, path in enumerate(paths)]
        results = await asyncio.gather(*tasks)
        metrics.extend(results)

    return metrics

# ==============================================================================
# ORQUESTRADOR DA MATRIZ EXPERIMENTAL (T01 a T12)
# ==============================================================================

TEST_DEFINITIONS = {
    "T01": {"payload": "A", "proto": "HTTP/1.1", "scenario": "LAN", "srv": "http1"},
    "T02": {"payload": "A", "proto": "HTTPS/TLS1.3", "scenario": "LAN", "srv": "http2"},
    "T03": {"payload": "A", "proto": "HTTP/3-QUIC", "scenario": "LAN", "srv": "http3"},
    "T04": {"payload": "A", "proto": "HTTP/1.1", "scenario": "WAN", "srv": "http1"},
    "T05": {"payload": "A", "proto": "HTTPS/TLS1.3", "scenario": "WAN", "srv": "http2"},
    "T06": {"payload": "A", "proto": "HTTP/3-QUIC", "scenario": "WAN", "srv": "http3"},
    "T07": {"payload": "B", "proto": "HTTP/1.1", "scenario": "LAN", "srv": "http1"},
    "T08": {"payload": "B", "proto": "HTTPS/TLS1.3", "scenario": "LAN", "srv": "http2"},
    "T09": {"payload": "B", "proto": "HTTP/3-QUIC", "scenario": "LAN", "srv": "http3"},
    "T10": {"payload": "B", "proto": "HTTP/1.1", "scenario": "WAN", "srv": "http1"},
    "T11": {"payload": "B", "proto": "HTTPS/TLS1.3", "scenario": "WAN", "srv": "http2"},
    "T12": {"payload": "B", "proto": "HTTP/3-QUIC", "scenario": "WAN", "srv": "http3"},
}

async def run_single_test(
    test_id: str,
    collector: MetricsCollector,
    http1_port: int = 8081,
    http2_port: int = 8443,
    http3_port: int = 9443,
    iterations: int = 10
):
    defn = TEST_DEFINITIONS[test_id]
    payload_type = "Carga A (50MB)" if defn["payload"] == "A" else "Carga B (100x10KB)"
    scenario_str = "LAN (1ms, 0% loss)" if defn["scenario"] == "LAN" else "WAN (50ms, 2% loss)"
    proto = defn["proto"]
    srv = defn["srv"]

    print(f"\n>>> Executando {test_id} [{proto} | {defn['scenario']} | {payload_type}] (N={iterations})...")

    # Lista de caminhos da Carga B (100 objetos)
    paths_b = [f"/objects/obj_{i:03d}.bin" for i in range(1, 101)]

    for it in range(1, iterations + 1):
        t0 = time.perf_counter()
        if defn["payload"] == "A":
            # Carga A: download de 50MB.bin no modo Cold TTFB (medição isolada de handshake + vazão)
            if srv == "http1":
                url = f"http://127.0.0.1:{http1_port}/50MB.bin"
                m = await fetch_httpx_cold(url, False, test_id, proto, scenario_str, payload_type, it, 1)
                collector.record(m)
            elif srv == "http2":
                url = f"https://127.0.0.1:{http2_port}/50MB.bin"
                m = await fetch_httpx_cold(url, True, test_id, proto, scenario_str, payload_type, it, 1)
                collector.record(m)
            elif srv == "http3":
                m = await fetch_h3_cold("127.0.0.1", http3_port, "/50MB.bin", test_id, proto, scenario_str, payload_type, it, 1)
                collector.record(m)
            
            elapsed = time.perf_counter() - t0
            print(f"    [Iter {it:02d}/{iterations}] TTFB: {m.ttfb_ms:.2f} ms | Load: {m.load_time_ms:.2f} ms | Goodput: {m.goodput_mbps:.2f} Mbps")

        else:
            # Carga B: 100 objetos de 10 KB concorrentes no modo Warm Connection
            if srv == "http1":
                base_url = f"http://127.0.0.1:{http1_port}"
                results = await fetch_httpx_warm_batch(base_url, paths_b, False, test_id, proto, scenario_str, payload_type, it)
            elif srv == "http2":
                base_url = f"https://127.0.0.1:{http2_port}"
                results = await fetch_httpx_warm_batch(base_url, paths_b, True, test_id, proto, scenario_str, payload_type, it)
            elif srv == "http3":
                results = await fetch_h3_warm_batch("127.0.0.1", http3_port, paths_b, test_id, proto, scenario_str, payload_type, it)

            for m in results:
                collector.record(m)

            elapsed = time.perf_counter() - t0
            avg_ttfb = sum(r.ttfb_ms for r in results) / len(results)
            rps = len(results) / elapsed if elapsed > 0 else 0
            print(f"    [Iter {it:02d}/{iterations}] 100 objetos | Tempo Janela: {elapsed:.3f} s | RPS: {rps:.1f} | TTFB Médio: {avg_ttfb:.2f} ms")

async def main():
    import argparse
    parser = argparse.ArgumentParser(description="Cliente de Benchmark Web UFPI (HTTP/1.1 vs HTTP/2 vs HTTP/3)")
    parser.add_argument("--test", type=str, default="all", help="ID do teste (T01 a T12) ou 'all'")
    parser.add_argument("--scenario", type=str, default=None, choices=["lan", "wan"], help="Filtra testes por cenário (lan ou wan)")
    parser.add_argument("--iterations", type=int, default=10, help="Número de repetições por teste (mínimo 10)")
    parser.add_argument("--http1-port", type=int, default=int(os.getenv("HTTP1_PORT", "8081")), help="Porta host para HTTP/1.1")
    parser.add_argument("--http2-port", type=int, default=8443, help="Porta host para HTTP/2 TLS")
    parser.add_argument("--http3-port", type=int, default=9443, help="Porta host para HTTP/3 QUIC")
    parser.add_argument("--output-json", type=str, default="data/raw/results.json", help="Arquivo de saída JSON")
    parser.add_argument("--output-csv", type=str, default="data/raw/results.csv", help="Arquivo de saída CSV")
    args = parser.parse_args()

    collector = MetricsCollector()
    
    # Se o arquivo de resultados já existir, carrega os dados anteriores para acumular testes
    if os.path.exists(args.output_json):
        try:
            import json
            with open(args.output_json, "r", encoding="utf-8") as f:
                prev_data = json.load(f)
                for item in prev_data:
                    collector.record(RequestMetric(**item))
            print(f"[*] Carregados {len(prev_data)} registros pré-existentes de {args.output_json}")
        except Exception as e:
            print(f"[!] Aviso ao carregar registros anteriores: {e}")

    # Determina testes a executar
    if args.test.lower() == "all":
        if args.scenario == "lan":
            tests_to_run = ["T01", "T02", "T03", "T07", "T08", "T09"]
        elif args.scenario == "wan":
            tests_to_run = ["T04", "T05", "T06", "T10", "T11", "T12"]
        else:
            tests_to_run = list(TEST_DEFINITIONS.keys())
    else:
        test_id = args.test.upper()
        if test_id not in TEST_DEFINITIONS:
            print(f"[!] Teste inválido: {test_id}. Opções: {list(TEST_DEFINITIONS.keys())}")
            sys.exit(1)
        tests_to_run = [test_id]

    print(f"================================================================================")
    print(f" INICIANDO BATERIA EXPERIMENTAL: {len(tests_to_run)} testes x {args.iterations} repetições")
    print(f" Testes agendados: {', '.join(tests_to_run)}")
    print(f" Portas: HTTP/1.1={args.http1_port}, HTTP/2={args.http2_port}, HTTP/3={args.http3_port}")
    print(f"================================================================================")

    for tid in tests_to_run:
        # Remove métricas anteriores desse mesmo test_id para não duplicar se estiver re-executando
        collector.metrics = [m for m in collector.metrics if m.test_id != tid]
        await run_single_test(
            test_id=tid,
            collector=collector,
            http1_port=args.http1_port,
            http2_port=args.http2_port,
            http3_port=args.http3_port,
            iterations=args.iterations
        )
        # Salva incrementalmente para segurança contra interrupções
        collector.export_raw(args.output_json, args.output_csv)

    print("\n================================================================================")
    print(" BATERIA EXPERIMENTAL CONCLUÍDA COM SUCESSO!")
    print(f" Total de amostras salvas: {len(collector.metrics)}")
    print(f" JSON: {args.output_json}")
    print(f" CSV:  {args.output_csv}")
    print("================================================================================")

if __name__ == "__main__":
    asyncio.run(main())
