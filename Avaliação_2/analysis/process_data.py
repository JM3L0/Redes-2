#!/usr/bin/env python3
"""
Pipeline de Processamento Estatístico e Consolidação de Dados Experimentais.
Disciplina: Redes de Computadores II (UFPI - CSHNB)
Aluno: João Marcos Sousa Rufino Leal (jsousarufinoleal@ufpi.edu.br)

Processa data/raw/results.json e results.csv:
1. Agrupa métricas por teste (T01 a T12) com N=10 repetições independentes.
2. Calcula média, mediana (p50), percentil p99, desvio padrão amostral e Intervalo de Confiança de 95% (t-Student).
3. Exporta tabela consolidada em CSV (data/processed/summary_table.csv) e LaTeX (data/processed/summary_table.tex).
"""

import os
import csv
import json
from collections import defaultdict
import numpy as np
import scipy.stats as stats


def calc_ci95(vals: np.ndarray) -> tuple:
    vals = np.asarray(vals, dtype=float)
    vals = vals[~np.isnan(vals)]
    n = len(vals)
    if n < 2:
        val = float(vals[0]) if n == 1 else 0.0
        return val, val
    mean = float(np.mean(vals))
    sem = float(stats.sem(vals))
    if sem == 0.0:
        return mean, mean
    ci = stats.t.interval(0.95, df=n - 1, loc=mean, scale=sem)
    return float(ci[0]), float(ci[1])


def process_results(raw_json_path: str, output_csv_path: str, output_tex_path: str):
    if not os.path.exists(raw_json_path):
        print(f"[!] Arquivo não encontrado: {raw_json_path}")
        return

    with open(raw_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        print("[!] Arquivo de dados brutos está vazio.")
        return

    print(f"[*] Processando {len(data)} registros experimentais...")

    groups = defaultdict(list)
    for row in data:
        groups[row["test_id"]].append(row)

    summary_rows = []

    for test_id in sorted(groups.keys(), key=lambda x: int(x[1:])):
        group = groups[test_id]
        first = group[0]
        protocol = first["protocol"]
        scenario = first["scenario"]
        payload_type = first["payload_type"]
        iterations = len(set(r["iteration"] for r in group))
        total_reqs = len(group)
        successes = sum(1 for r in group if int(r["status_code"]) == 200)
        success_rate = (successes / total_reqs) * 100.0 if total_reqs > 0 else 0.0

        # 1. TTFB (ms)
        ttfb = np.array([float(r["ttfb_ms"]) for r in group], dtype=float)
        ttfb_mean = float(np.mean(ttfb))
        ttfb_std = float(np.std(ttfb, ddof=1)) if len(ttfb) > 1 else 0.0
        ttfb_p50 = float(np.percentile(ttfb, 50))
        ttfb_p99 = float(np.percentile(ttfb, 99))
        ttfb_ci_low, _ = calc_ci95(ttfb)

        # 2. Tempo Total, Vazão (Goodput) e RPS por Iteração
        if "Carga B" in payload_type:
            it_groups = defaultdict(list)
            for r in group:
                it_groups[int(r["iteration"])].append(r)

            it_stats = []
            for it in sorted(it_groups.keys()):
                it_rows = it_groups[it]
                batch_load_ms = max(float(r["load_time_ms"]) for r in it_rows)
                batch_bytes = sum(int(r["bytes_downloaded"]) for r in it_rows)
                batch_dur_s = batch_load_ms / 1000.0
                batch_goodput = (batch_bytes * 8.0) / (batch_dur_s * 1e6) if batch_dur_s > 0 else 0.0
                batch_rps = len(it_rows) / batch_dur_s if batch_dur_s > 0 else 0.0
                it_stats.append((batch_load_ms, batch_goodput, batch_rps))

            load_arr = np.array([x[0] for x in it_stats], dtype=float)
            goodput_arr = np.array([x[1] for x in it_stats], dtype=float)
            rps_arr = np.array([x[2] for x in it_stats], dtype=float)
        else:
            load_arr = np.array([float(r["load_time_ms"]) for r in group], dtype=float)
            goodput_arr = np.array([float(r["goodput_mbps"]) for r in group], dtype=float)
            rps_arr = np.array([1000.0 / x if x > 0 else 0.0 for x in load_arr], dtype=float)

        load_mean = float(np.mean(load_arr))
        load_std = float(np.std(load_arr, ddof=1)) if len(load_arr) > 1 else 0.0
        load_p50 = float(np.percentile(load_arr, 50))
        load_p99 = float(np.percentile(load_arr, 99))
        load_ci_low, _ = calc_ci95(load_arr)

        goodput_mean = float(np.mean(goodput_arr))
        goodput_std = float(np.std(goodput_arr, ddof=1)) if len(goodput_arr) > 1 else 0.0

        rps_mean = float(np.mean(rps_arr))
        rps_std = float(np.std(rps_arr, ddof=1)) if len(rps_arr) > 1 else 0.0
        rps_p50 = float(np.percentile(rps_arr, 50))
        rps_p99 = float(np.percentile(rps_arr, 99))

        summary_rows.append({
            "Test_ID": test_id,
            "Protocol": protocol,
            "Scenario": scenario,
            "Payload": payload_type,
            "Iterations": iterations,
            "Total_Requests": total_reqs,
            "Success_Rate_%": round(success_rate, 1),
            "TTFB_Mean_ms": round(ttfb_mean, 2),
            "TTFB_Std_ms": round(ttfb_std, 2),
            "TTFB_p50_ms": round(ttfb_p50, 2),
            "TTFB_p99_ms": round(ttfb_p99, 2),
            "TTFB_CI95_Margin": round(ttfb_mean - ttfb_ci_low, 2),
            "Load_Mean_ms": round(load_mean, 2),
            "Load_Std_ms": round(load_std, 2),
            "Load_p50_ms": round(load_p50, 2),
            "Load_p99_ms": round(load_p99, 2),
            "Load_CI95_Margin": round(load_mean - load_ci_low, 2),
            "Goodput_Mean_Mbps": round(goodput_mean, 2),
            "Goodput_Std_Mbps": round(goodput_std, 2),
            "RPS_Mean": round(rps_mean, 2),
            "RPS_Std": round(rps_std, 2),
            "RPS_p50": round(rps_p50, 2),
            "RPS_p99": round(rps_p99, 2),
        })

    # Exporta CSV
    os.makedirs(os.path.dirname(os.path.abspath(output_csv_path)), exist_ok=True)
    fieldnames = list(summary_rows[0].keys())
    with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)
    print(f"[+] Tabela estatística consolidada salva em: {output_csv_path}")

    # Exporta LaTeX formatado para o artigo da SBC
    os.makedirs(os.path.dirname(os.path.abspath(output_tex_path)), exist_ok=True)
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Consolidação Estatística dos Resultados Experimentais dos Protocolos Web (T01 a T12, $N=10$)}",
        r"\label{tab:metricas_consolidadas}",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{@{}llllrrrrrr@{}}",
        r"\toprule",
        r"\textbf{ID} & \textbf{Protocolo} & \textbf{Cenário} & \textbf{Carga} & \textbf{TTFB $\bar{x} \pm s$ (ms)} & \textbf{TTFB p50 / p99 (ms)} & \textbf{Tempo Total $\bar{x} \pm s$ (s)} & \textbf{Tempo p50 / p99 (s)} & \textbf{Vazão $\bar{x} \pm s$ (Mbps)} & \textbf{RPS $\bar{x} \pm s$ (p50/p99)} \\ \midrule",
    ]
    for row in summary_rows:
        sc_short = "LAN (1ms, 0\\%)" if "LAN" in row["Scenario"] else "WAN (50ms, 2\\%)"
        pl_short = "Carga A (50MB)" if "Carga A" in row["Payload"] else "Carga B (100x10K)"
        ttfb_ms_str = f"{row['TTFB_Mean_ms']:.2f} $\\pm$ {row['TTFB_Std_ms']:.1f}"
        ttfb_p_str = f"{row['TTFB_p50_ms']:.1f} / {row['TTFB_p99_ms']:.1f}"
        load_s_mean = row["Load_Mean_ms"] / 1000.0
        load_s_std = row["Load_Std_ms"] / 1000.0
        load_s_p50 = row["Load_p50_ms"] / 1000.0
        load_s_p99 = row["Load_p99_ms"] / 1000.0
        load_s_str = f"{load_s_mean:.2f} $\\pm$ {load_s_std:.2f}"
        load_p_str = f"{load_s_p50:.2f} / {load_s_p99:.2f}"
        gp_str = f"{row['Goodput_Mean_Mbps']:.2f} $\\pm$ {row['Goodput_Std_Mbps']:.2f}"
        rps_str = f"{row['RPS_Mean']:.2f} $\\pm$ {row['RPS_Std']:.2f} ({row['RPS_p50']:.2f}/{row['RPS_p99']:.2f})"
        line = f"{row['Test_ID']} & {row['Protocol']} & {sc_short} & {pl_short} & {ttfb_ms_str} & {ttfb_p_str} & {load_s_str} & {load_p_str} & {gp_str} & {rps_str} \\\\"
        if row["Test_ID"] == "T06":
            line += r" \midrule"
        lines.append(line)
    lines.extend([
        r"\bottomrule",
        r"\end{tabular}%",
        r"}",
        r"\end{table}",
    ])
    with open(output_tex_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[+] Tabela LaTeX para SBC salva em: {output_tex_path}")

    print("\n--- RESUMO CONSOLIDADO DOS EXPERIMENTOS (N=10) ---")
    header = f"{'ID':<4} {'Protocol':<13} {'Scenario':<20} {'N':<3} {'TTFB_Mean':<10} {'TTFB_Std':<9} {'p50':<8} {'p99':<8} {'Load_ms':<10} {'Goodput':<9} {'RPS':<8}"
    print(header)
    print("-" * len(header))
    for r in summary_rows:
        print(f"{r['Test_ID']:<4} {r['Protocol']:<13} {r['Scenario']:<20} {r['Iterations']:<3} {r['TTFB_Mean_ms']:<10.2f} {r['TTFB_Std_ms']:<9.2f} {r['TTFB_p50_ms']:<8.2f} {r['TTFB_p99_ms']:<8.2f} {r['Load_Mean_ms']:<10.2f} {r['Goodput_Mean_Mbps']:<9.2f} {r['RPS_Mean']:<8.2f}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "data", "raw", "results.json")
    csv_out = os.path.join(base_dir, "data", "processed", "summary_table.csv")
    tex_out = os.path.join(base_dir, "data", "processed", "summary_table.tex")
    process_results(json_path, csv_out, tex_out)
