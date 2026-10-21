"""
Módulo de Coleta e Modelagem de Métricas de Rede e Benchmark.
Registra métricas temporais com precisão de microssegundos via time.perf_counter().
Calcula estimadores estatísticos: média, mediana (p50), percentil p99, desvio padrão e IC 95%.
Exporta resultados em JSON e CSV conforme exigido na especificação da 2ª Avaliação.
"""

import os
import json
import csv
import time
import math
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import numpy as np
import scipy.stats as stats

@dataclass
class RequestMetric:
    test_id: str             # Ex: "T01", "T02", ..., "T12"
    protocol: str            # "HTTP/1.1", "HTTPS/TLS1.3", "HTTP/3-QUIC"
    scenario: str            # "LAN (1ms, 0% loss)" ou "WAN (50ms, 2% loss)"
    payload_type: str        # "Carga A (50MB)" ou "Carga B (100x10KB)"
    iteration: int           # 1 a 10
    request_id: int          # ID do objeto ou requisição
    url: str                 # URL requisitada
    status_code: int         # 200, etc.
    ttfb_ms: float           # Time to First Byte em milissegundos
    load_time_ms: float      # Tempo Total de Carregamento em milissegundos
    bytes_downloaded: int    # Tamanho transferido em bytes
    goodput_mbps: float      # Vazão útil em Megabits por segundo (Mbps)
    mode: str                # "cold" ou "warm"
    timestamp: str           # ISO 8601

@dataclass
class TestSummary:
    test_id: str
    protocol: str
    scenario: str
    payload_type: str
    total_iterations: int
    total_requests: int
    success_rate: float
    # TTFB (ms)
    ttfb_mean_ms: float
    ttfb_std_ms: float
    ttfb_p50_ms: float
    ttfb_p99_ms: float
    ttfb_ci95_low_ms: float
    ttfb_ci95_high_ms: float
    # Total Load Time (ms)
    load_time_mean_ms: float
    load_time_std_ms: float
    load_time_p50_ms: float
    load_time_p99_ms: float
    load_time_ci95_low_ms: float
    load_time_ci95_high_ms: float
    # Throughput / Goodput (Mbps)
    goodput_mean_mbps: float
    goodput_std_mbps: float
    # Requests Per Second (RPS)
    rps: float

class MetricsCollector:
    def __init__(self):
        self.metrics: List[RequestMetric] = []

    def record(self, metric: RequestMetric):
        self.metrics.append(metric)

    def to_dataframe(self):
        import pandas as pd
        return pd.DataFrame([asdict(m) for m in self.metrics])

    def export_raw(self, json_path: str, csv_path: str):
        os.makedirs(os.path.dirname(os.path.abspath(json_path)), exist_ok=True)
        os.makedirs(os.path.dirname(os.path.abspath(csv_path)), exist_ok=True)

        data_dicts = [asdict(m) for m in self.metrics]

        # Salva JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data_dicts, f, indent=2, ensure_ascii=False)
        print(f"[+] Dados brutos exportados em JSON: {json_path} ({len(self.metrics)} registros)")

        # Salva CSV
        if self.metrics:
            fieldnames = list(data_dicts[0].keys())
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data_dicts)
            print(f"[+] Dados brutos exportados em CSV: {csv_path}")

    @staticmethod
    def compute_summary(metrics_list: List[RequestMetric], test_window_sec: float) -> Optional[TestSummary]:
        if not metrics_list:
            return None

        first = metrics_list[0]
        n = len(metrics_list)
        successes = sum(1 for m in metrics_list if m.status_code == 200)
        success_rate = (successes / n) * 100.0

        ttfbs = np.array([m.ttfb_ms for m in metrics_list])
        load_times = np.array([m.load_time_ms for m in metrics_list])
        goodputs = np.array([m.goodput_mbps for m in metrics_list])

        def calc_ci95(arr):
            if len(arr) < 2:
                return float(np.mean(arr)), float(np.mean(arr))
            mean = np.mean(arr)
            sem = stats.sem(arr)
            ci = stats.t.interval(0.95, df=len(arr)-1, loc=mean, scale=sem)
            return float(ci[0]), float(ci[1])

        ttfb_ci = calc_ci95(ttfbs)
        load_ci = calc_ci95(load_times)

        # RPS calculado sobre a janela de teste
        rps = (successes / test_window_sec) if test_window_sec > 0 else 0.0

        return TestSummary(
            test_id=first.test_id,
            protocol=first.protocol,
            scenario=first.scenario,
            payload_type=first.payload_type,
            total_iterations=max(m.iteration for m in metrics_list),
            total_requests=n,
            success_rate=success_rate,
            ttfb_mean_ms=float(np.mean(ttfbs)),
            ttfb_std_ms=float(np.std(ttfbs, ddof=1)) if n > 1 else 0.0,
            ttfb_p50_ms=float(np.percentile(ttfbs, 50)),
            ttfb_p99_ms=float(np.percentile(ttfbs, 99)),
            ttfb_ci95_low_ms=ttfb_ci[0],
            ttfb_ci95_high_ms=ttfb_ci[1],
            load_time_mean_ms=float(np.mean(load_times)),
            load_time_std_ms=float(np.std(load_times, ddof=1)) if n > 1 else 0.0,
            load_time_p50_ms=float(np.percentile(load_times, 50)),
            load_time_p99_ms=float(np.percentile(load_times, 99)),
            load_time_ci95_low_ms=load_ci[0],
            load_time_ci95_high_ms=load_ci[1],
            goodput_mean_mbps=float(np.mean(goodputs)),
            goodput_std_mbps=float(np.std(goodputs, ddof=1)) if n > 1 else 0.0,
            rps=rps
        )
