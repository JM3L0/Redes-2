#!/usr/bin/env python3
"""
parse_logs.py - Pipeline de Consolidacao e Analise Estatistica dos Dados Brutos
================================================================================
Redes de Computadores II (UFPI - 2026-2) — Avaliacao 1
Aluno: Joao Marcos Sousa Rufino Leal

Funcao:
  Consolida os CSVs gerados pelas baterias de ensaios (Cenarios A, B e C),
  computa media, desvio padrao, percentis (p50, p90, p95) e intervalo de
  confianca de 95% (t-Student, N=10, t_critico=2.262) para cada grupo
  de medicoes. Salva os resultados em `data/processed/`.

Uso:
  python3 analysis/parse_logs.py [--raw-dir data/raw] [--out-dir data/processed]
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

def confidence_interval_95(series: pd.Series) -> float:
    """Calcula a semi-amplitude do intervalo de confianca de 95% via distribuicao t-Student."""
    n = len(series)
    if n < 2:
        return float("nan")
    sem = series.std(ddof=1) / np.sqrt(n)
    t_crit = stats.t.ppf(0.975, df=n - 1)
    return float(t_crit * sem)


def aggregate(df: pd.DataFrame, group_cols: list[str], metric_col: str) -> pd.DataFrame:
    """Agrega uma metrica por grupo, computando estatisticas descritivas e IC 95%."""
    grouped = df.groupby(group_cols)[metric_col]
    result = grouped.agg(
        count="count",
        mean="mean",
        std=lambda x: x.std(ddof=1) if len(x) > 1 else 0.0,
        median="median",
        p90=lambda x: x.quantile(0.90),
        p95=lambda x: x.quantile(0.95),
        min="min",
        max="max",
        ic95_half=confidence_interval_95,
    ).reset_index()

    result["ic95_low"] = result["mean"] - result["ic95_half"]
    result["ic95_high"] = result["mean"] + result["ic95_half"]
    result["metric"] = metric_col
    return result


# ---------------------------------------------------------------------------
# Cenario A: UDP Puro (iperf3)
# ---------------------------------------------------------------------------
def process_scenario_a(raw_dir: Path, out_dir: Path) -> None:
    csv_path = raw_dir / "scenario_a_results.csv"
    if not csv_path.exists():
        print(f"[AVISO] {csv_path} nao encontrado. Pulando Cenario A.")
        return

    df = pd.read_csv(csv_path)
    print(f"[A] Carregados {len(df)} registros de {csv_path}")

    # Filtrar registros com goodput valido
    df = df[df["goodput_mbps"] > 0].copy()

    # Goodput por taxa de injecao
    goodput = aggregate(df, ["target_rate_mbps"], "goodput_mbps")
    goodput.to_csv(out_dir / "scenario_a_goodput.csv", index=False)

    # Jitter por taxa de injecao
    jitter = aggregate(df, ["target_rate_mbps"], "jitter_ms")
    jitter.to_csv(out_dir / "scenario_a_jitter.csv", index=False)

    # Taxa de perda por taxa de injecao
    loss = aggregate(df, ["target_rate_mbps"], "loss_percent")
    loss.to_csv(out_dir / "scenario_a_loss.csv", index=False)

    # Overhead de cabecalho UDP vs TCP (calculado teoricamente)
    overhead = pd.DataFrame({
        "protocol": ["UDP", "TCP (min)", "TCP (max)", "QUIC (Short Header)"],
        "transport_header_bytes": [8, 20, 60, 4],   # Short Header QUIC ~4B
        "crypto_overhead_bytes":  [0,  0,   0, 16],  # AEAD tag
        "total_overhead_bytes":   [8, 20,  60, 20],
    })
    overhead.to_csv(out_dir / "scenario_a_header_overhead.csv", index=False)

    print(f"[A] Resultados salvos em {out_dir}")


# ---------------------------------------------------------------------------
# Cenario B: TCP Massivo vs QUIC (curl HTTP/1.1 vs HTTP/2 vs HTTP/3)
# ---------------------------------------------------------------------------
def process_scenario_b(raw_dir: Path, out_dir: Path) -> None:
    csv_path = raw_dir / "scenario_b_results.csv"
    if not csv_path.exists():
        print(f"[AVISO] {csv_path} nao encontrado. Pulando Cenario B.")
        return

    df = pd.read_csv(csv_path)
    print(f"[B] Carregados {len(df)} registros de {csv_path}")
    df = df[df["goodput_mbps"] > 0].copy()

    # FCT por protocolo e tamanho do arquivo
    fct = aggregate(df, ["file_size_label", "protocol"], "total_time_sec")
    fct.to_csv(out_dir / "scenario_b_fct.csv", index=False)

    # Goodput por protocolo e tamanho
    goodput = aggregate(df, ["file_size_label", "protocol"], "goodput_mbps")
    goodput.to_csv(out_dir / "scenario_b_goodput.csv", index=False)

    # Tempo de handshake (TLS/QUIC) por protocolo
    handshake = aggregate(df, ["file_size_label", "protocol"], "tls_time_sec")
    handshake.to_csv(out_dir / "scenario_b_handshake.csv", index=False)

    # TTFB por protocolo
    ttfb = aggregate(df, ["file_size_label", "protocol"], "ttfb_sec")
    ttfb.to_csv(out_dir / "scenario_b_ttfb.csv", index=False)

    print(f"[B] Resultados salvos em {out_dir}")


# ---------------------------------------------------------------------------
# Cenario C: QUIC & HoL Blocking (100 objetos sob perda)
# ---------------------------------------------------------------------------
def process_scenario_c(raw_dir: Path, out_dir: Path) -> None:
    csv_path = raw_dir / "scenario_c_results.csv"
    if not csv_path.exists():
        print(f"[AVISO] {csv_path} nao encontrado. Pulando Cenario C.")
        return

    df = pd.read_csv(csv_path)
    print(f"[C] Carregados {len(df)} registros de {csv_path}")
    df = df[df["goodput_mbps"] > 0].copy()
    df["loss_percent"] = pd.to_numeric(df["loss_percent"], errors="coerce")

    # FCT do lote por protocolo e nivel de perda
    fct = aggregate(df, ["loss_percent", "protocol"], "total_batch_fct_sec")
    fct.to_csv(out_dir / "scenario_c_fct.csv", index=False)

    # Goodput do lote por protocolo e nivel de perda
    goodput = aggregate(df, ["loss_percent", "protocol"], "goodput_mbps")
    goodput.to_csv(out_dir / "scenario_c_goodput.csv", index=False)

    # CDF por protocolo para nivel de perda de 5% (pior caso = mais relevante)
    loss5_df = df[df["loss_percent"] == 5].copy()
    if not loss5_df.empty:
        cdf_records = []
        for proto in loss5_df["protocol"].unique():
            values = np.sort(loss5_df[loss5_df["protocol"] == proto]["total_batch_fct_sec"].values)
            cdf = np.arange(1, len(values) + 1) / len(values)
            for v, c in zip(values, cdf):
                cdf_records.append({"protocol": proto, "fct_sec": v, "cdf": c})
        pd.DataFrame(cdf_records).to_csv(out_dir / "scenario_c_cdf_loss5.csv", index=False)

    print(f"[C] Resultados salvos em {out_dir}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Consolida e processa dados brutos dos experimentos.")
    parser.add_argument("--raw-dir",  default="data/raw",       help="Diretorio com CSVs brutos")
    parser.add_argument("--out-dir",  default="data/processed", help="Diretorio de saida dos dados processados")
    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    out_dir = Path(args.out_dir)

    if not raw_dir.exists():
        print(f"[ERRO] Diretorio de dados brutos '{raw_dir}' nao existe. Execute os experimentos primeiro.")
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"[*] Processando dados de '{raw_dir}' -> '{out_dir}'")

    process_scenario_a(raw_dir, out_dir)
    process_scenario_b(raw_dir, out_dir)
    process_scenario_c(raw_dir, out_dir)

    print("\n[OK] Pipeline de analise concluido com sucesso!")


if __name__ == "__main__":
    main()
