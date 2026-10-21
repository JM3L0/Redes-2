#!/usr/bin/env python3
"""
Pipeline de Processamento Estatístico e Consolidação de Dados Experimentais.
Disciplina: Redes de Computadores II (UFPI - CSHNB)
Aluno: João Marcos Sousa Rufino Leal (jsousarufinoleal@ufpi.edu.br)

Processa data/raw/results.json e results.csv:
1. Agrupa métricas por teste (T01 a T12).
2. Calcula média, mediana (p50), percentil p99, desvio padrão amostral e Intervalo de Confiança de 95% (t-Student).
3. Exporta tabela consolidada em CSV (data/processed/summary_table.csv) e LaTeX (data/processed/summary_table.tex).
"""

import os
import sys
import json
import pandas as pd
import numpy as np
import scipy.stats as stats

def calc_ci95(series: pd.Series) -> tuple:
    vals = series.dropna().values
    n = len(vals)
    if n < 2:
        val = float(vals[0]) if n == 1 else 0.0
        return val, val
    mean = np.mean(vals)
    sem = stats.sem(vals)
    ci = stats.t.interval(0.95, df=n-1, loc=mean, scale=sem)
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

    df = pd.DataFrame(data)
    print(f"[*] Processando {len(df)} registros experimentais...")

    summary_rows = []

    for test_id, group in df.groupby("test_id"):
        first = group.iloc[0]
        protocol = first["protocol"]
        scenario = first["scenario"]
        payload_type = first["payload_type"]
        iterations = group["iteration"].nunique()
        total_reqs = len(group)
        successes = len(group[group["status_code"] == 200])
        success_rate = (successes / total_reqs) * 100.0 if total_reqs > 0 else 0.0

        # TTFB
        ttfb = group["ttfb_ms"]
        ttfb_mean = ttfb.mean()
        ttfb_std = ttfb.std(ddof=1) if len(ttfb) > 1 else 0.0
        ttfb_p50 = ttfb.median()
        ttfb_p99 = np.percentile(ttfb, 99)
        ttfb_ci_low, ttfb_ci_high = calc_ci95(ttfb)

        # Load Time
        load = group["load_time_ms"]
        load_mean = load.mean()
        load_std = load.std(ddof=1) if len(load) > 1 else 0.0
        load_p50 = load.median()
        load_p99 = np.percentile(load, 99)
        load_ci_low, load_ci_high = calc_ci95(load)

        # Goodput
        goodput = group["goodput_mbps"]
        goodput_mean = goodput.mean()
        goodput_std = goodput.std(ddof=1) if len(goodput) > 1 else 0.0

        # RPS (para Carga B, calculado por iteração)
        rps_list = []
        if "Carga B" in payload_type:
            for it, it_group in group.groupby("iteration"):
                max_load = it_group["load_time_ms"].max() / 1000.0
                if max_load > 0:
                    rps_list.append(len(it_group) / max_load)
            rps_mean = np.mean(rps_list) if rps_list else 0.0
            rps_std = np.std(rps_list, ddof=1) if len(rps_list) > 1 else 0.0
        else:
            rps_mean = 1000.0 / load_mean if load_mean > 0 else 0.0
            rps_std = 0.0

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
            "RPS_Std": round(rps_std, 2)
        })

    summary_df = pd.DataFrame(summary_rows)
    # Ordena pelo ID do teste (T01 a T12)
    summary_df["sort_key"] = summary_df["Test_ID"].apply(lambda x: int(x[1:]))
    summary_df = summary_df.sort_values("sort_key").drop(columns=["sort_key"])

    # Exporta CSV
    os.makedirs(os.path.dirname(os.path.abspath(output_csv_path)), exist_ok=True)
    summary_df.to_csv(output_csv_path, index=False, encoding="utf-8")
    print(f"[+] Tabela estatística consolidada salva em: {output_csv_path}")

    # Exporta LaTeX formatado para o artigo da SBC
    os.makedirs(os.path.dirname(os.path.abspath(output_tex_path)), exist_ok=True)
    tex_cols = [
        "Test_ID", "Protocol", "Scenario", "Payload",
        "TTFB_Mean_ms", "TTFB_p50_ms", "TTFB_p99_ms",
        "Load_Mean_ms", "Goodput_Mean_Mbps", "RPS_Mean"
    ]
    sub_df = summary_df[tex_cols].copy()
    sub_df.columns = [
        "ID", "Protocolo", "Cenário", "Carga",
        "TTFB Méd (ms)", "p50 (ms)", "p99 (ms)",
        "Tempo Méd (ms)", "Vazão (Mbps)", "RPS"
    ]
    latex_table = sub_df.to_latex(index=False, caption="Consolidação dos Resultados Experimentais dos Protocolos Web (Média, p50, p99, Vazão e RPS)", label="tab:metricas_consolidadas")
    with open(output_tex_path, "w", encoding="utf-8") as f:
        f.write(latex_table)
    print(f"[+] Tabela LaTeX para SBC salva em: {output_tex_path}")

    print("\n--- RESUMO CONSOLIDADO DOS EXPERIMENTOS ---")
    print(summary_df[["Test_ID", "Protocol", "Scenario", "TTFB_Mean_ms", "Load_Mean_ms", "Goodput_Mean_Mbps", "RPS_Mean"]].to_string(index=False))

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "data", "raw", "results.json")
    csv_out = os.path.join(base_dir, "data", "processed", "summary_table.csv")
    tex_out = os.path.join(base_dir, "data", "processed", "summary_table.tex")
    process_results(json_path, csv_out, tex_out)
