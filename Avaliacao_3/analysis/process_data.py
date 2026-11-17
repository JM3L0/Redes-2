#!/usr/bin/env python3
"""
Processamento Estatístico da 3ª Avaliação (N3) — Redes de Computadores II (UFPI).
Calcula médias, desvios-padrão amostrais (s), intervalos de confiança (95%) e total de
retransmissões para os 6 testes essenciais (E01 a E06, N >= 5 repetições).
Exporta data/processed/summary_table.csv, summary_table.json e summary_table.tex.
"""

import os
import csv
import json
import numpy as np
import scipy.stats as stats


def compute_stats(values: list[float]) -> dict[str, float]:
    arr = np.asarray(values, dtype=float)
    n = len(arr)
    if n == 0:
        return {"n": 0, "mean": 0.0, "std": 0.0, "ci95": 0.0, "min": 0.0, "max": 0.0, "sum": 0.0}
    mean = float(np.mean(arr))
    std = float(np.std(arr, ddof=1)) if n > 1 else 0.0
    sem = float(stats.sem(arr)) if n > 1 else 0.0
    if n > 1 and sem > 0:
        ci_low, _ = stats.t.interval(0.95, df=n - 1, loc=mean, scale=sem)
        ci95 = float(mean - ci_low)
    else:
        ci95 = 0.0
    return {
        "n": int(n),
        "mean": mean,
        "std": std,
        "ci95": ci95,
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "sum": float(np.sum(arr)),
    }


def process_results(base_dir: str):
    raw_json_path = os.path.join(base_dir, "data", "raw", "results.json")
    processed_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    if not os.path.exists(raw_json_path):
        raise FileNotFoundError(f"Arquivo bruto não encontrado: {raw_json_path}")

    with open(raw_json_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    test_order = ["E01", "E02", "E03", "E04", "E05", "E06"]
    grouped = {tid: [] for tid in test_order}
    for r in records:
        tid = r["test_id"]
        if tid in grouped:
            grouped[tid].append(r)

    summary_rows = []
    for tid in test_order:
        rows = grouped[tid]
        if not rows:
            continue
        first = rows[0]
        block = first["block"]
        protocol_mode = first["protocol_mode"]
        scenario = first["scenario"]
        rtt_ms = first["rtt_ms"]
        loss_pct = first["loss_pct"]

        if block == "A":
            tput_vals = [float(r["throughput_mbps"]) for r in rows]
            retr_vals = [float(r["retransmits"]) for r in rows]
            tput_st = compute_stats(tput_vals)
            retr_st = compute_stats(retr_vals)
            summary_rows.append({
                "test_id": tid,
                "block": "Bloco A",
                "protocol_mode": protocol_mode,
                "scenario": scenario,
                "rtt_ms": rtt_ms,
                "loss_pct": loss_pct,
                "n": tput_st["n"],
                "throughput_mean_mbps": round(tput_st["mean"], 2),
                "throughput_std_mbps": round(tput_st["std"], 2),
                "throughput_ci95_mbps": round(tput_st["ci95"], 2),
                "retrans_mean": round(retr_st["mean"], 1),
                "retrans_std": round(retr_st["std"], 1),
                "retrans_total": int(round(retr_st["sum"])),
                "ttfb_mean_ms": None,
                "ttfb_std_ms": None,
                "ttfb_ci95_ms": None,
            })
        else:
            ttfb_vals = [float(r["ttfb_ms"]) for r in rows]
            ttfb_st = compute_stats(ttfb_vals)
            summary_rows.append({
                "test_id": tid,
                "block": "Bloco B",
                "protocol_mode": protocol_mode,
                "scenario": scenario,
                "rtt_ms": rtt_ms,
                "loss_pct": loss_pct,
                "n": ttfb_st["n"],
                "throughput_mean_mbps": None,
                "throughput_std_mbps": None,
                "throughput_ci95_mbps": None,
                "retrans_mean": None,
                "retrans_std": None,
                "retrans_total": None,
                "ttfb_mean_ms": round(ttfb_st["mean"], 2),
                "ttfb_std_ms": round(ttfb_st["std"], 2),
                "ttfb_ci95_ms": round(ttfb_st["ci95"], 2),
            })

    # Salvar CSV consolidado
    csv_out = os.path.join(processed_dir, "summary_table.csv")
    fieldnames = [
        "test_id", "block", "protocol_mode", "scenario", "rtt_ms", "loss_pct", "n",
        "throughput_mean_mbps", "throughput_std_mbps", "throughput_ci95_mbps",
        "retrans_mean", "retrans_std", "retrans_total",
        "ttfb_mean_ms", "ttfb_std_ms", "ttfb_ci95_ms"
    ]
    with open(csv_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    # Salvar JSON consolidado
    json_out = os.path.join(processed_dir, "summary_table.json")
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(summary_rows, f, indent=2, ensure_ascii=False)

    # Salvar Tabela LaTeX pronta para inclusão no relatório SBRC
    tex_out = os.path.join(processed_dir, "summary_table.tex")
    with open(tex_out, "w", encoding="utf-8") as f:
        f.write("% Tabela Resumo Gerada Automaticamente por analysis/process_data.py\n")
        f.write("\\begin{table}[htbp]\n\\centering\n")
        f.write("\\caption{Tabela Resumo dos Resultados Experimentais (Blocos A e B --- $N=5$ repetições por teste).}\n")
        f.write("\\label{tab:resumo_n3}\n")
        f.write("\\resizebox{\\textwidth}{!}{%\n")
        f.write("\\begin{tabular}{@{}clllcccc@{}}\n\\toprule\n")
        f.write("\\textbf{ID} & \\textbf{Algoritmo / Modo} & \\textbf{Cenário (\\texttt{tc netem})} & \\textbf{Métrica} & \\textbf{Média ($\\bar{x}$)} & \\textbf{Desv. Padrão ($s$)} & \\textbf{Retr./Fluxo} & \\textbf{Total Retr.} \\\\\n\\midrule\n")
        for r in summary_rows:
            if r["block"] == "Bloco A":
                f.write(
                    f"\\textbf{{{r['test_id']}}} & {r['protocol_mode']} & {r['scenario']} & Vazão (Mbps) & "
                    f"${r['throughput_mean_mbps']:.2f}$ & $\\pm {r['throughput_std_mbps']:.2f}$ & "
                    f"${r['retrans_mean']:.1f} \\pm {r['retrans_std']:.1f}$ & ${r['retrans_total']}$ \\\\\n"
                )
            else:
                f.write(
                    f"\\textbf{{{r['test_id']}}} & {r['protocol_mode']} & {r['scenario']} & TTFB (ms) & "
                    f"${r['ttfb_mean_ms']:.2f}$ & $\\pm {r['ttfb_std_ms']:.2f}$ & --- & --- \\\\\n"
                )
        f.write("\\bottomrule\n\\end{tabular}%\n}\n\\end{table}\n")

    print("\n" + "=" * 88)
    print(" RESUMO ESTATÍSTICO CONSOLIDADO — 3ª AVALIAÇÃO (N3)")
    print("=" * 88)
    for r in summary_rows:
        if r["block"] == "Bloco A":
            print(
                f" [{r['test_id']}] {r['protocol_mode']:<12} | {r['scenario']:<20} | "
                f"Vazão: {r['throughput_mean_mbps']:>8.2f} ± {r['throughput_std_mbps']:<6.2f} Mbps | "
                f"Retrans (Total): {r['retrans_total']} (média {r['retrans_mean']:.1f}/fluxo)"
            )
        else:
            print(
                f" [{r['test_id']}] {r['protocol_mode']:<26} | {r['scenario']:<20} | "
                f"TTFB : {r['ttfb_mean_ms']:>8.2f} ± {r['ttfb_std_ms']:<6.2f} ms"
            )
    print("=" * 88 + "\n")
    print(f"[+] Tabelas salvas em {csv_out} e {tex_out}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    process_results(base_dir)
