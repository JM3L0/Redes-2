#!/usr/bin/env python3
"""
Geração Programática dos 2 Gráficos Comparativos Obrigatórios — 3ª Avaliação (N3).
Atende rigorosamente à Seção 5 e ao Eixo 2 da Rubrica (evitando a penalidade de -10 pontos):
- Gráfico 1 (Bloco A): Vazão média (Mbps) comparando TCP CUBIC (LAN/WAN) e TCP BBR (WAN),
  com BARRAS DE ERRO (desvio padrão).
- Gráfico 2 (Bloco B): TTFB médio (ms) comparando HTTP/2 vs. HTTP/3 Cold vs. HTTP/3 Warm/Resumed,
  com BARRAS DE ERRO (desvio padrão).
"""

import os
import json
import shutil
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 11.5,
    "axes.titlesize": 12.2,
    "xtick.labelsize": 10.2,
    "ytick.labelsize": 10.5,
    "legend.fontsize": 10,
    "figure.titlesize": 13.2,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})


def plot_bloco_a(summary_rows: list[dict], plots_dir: str, relatorio_dir: str):
    """
    Gráfico 1 (Bloco A): Vazão média (Mbps) comparando TCP CUBIC (LAN/WAN) e TCP BBR (WAN),
    com barras de erro representando o desvio padrão (s).
    """
    rows_a = {r["test_id"]: r for r in summary_rows if r["block"] == "Bloco A"}
    e01, e02, e03 = rows_a["E01"], rows_a["E02"], rows_a["E03"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.4, 5.2), gridspec_kw={"width_ratios": [1.15, 1.0]})

    # --- Painel (a): Comparação Global E01 vs E02 vs E03 ---
    labels_all = [
        "E01: TCP CUBIC\nLAN (1 ms, 0% perda)",
        "E02: TCP CUBIC\nWAN (50 ms, 2% perda)",
        "E03: TCP BBR\nWAN (50 ms, 2% perda)",
    ]
    means_all = [e01["throughput_mean_mbps"], e02["throughput_mean_mbps"], e03["throughput_mean_mbps"]]
    stds_all = [e01["throughput_std_mbps"], e02["throughput_std_mbps"], e03["throughput_std_mbps"]]
    colors_all = ["#1f77b4", "#d62728", "#2ca02c"]

    x1 = np.arange(len(labels_all))
    bars1 = ax1.bar(
        x1, means_all, width=0.54, yerr=stds_all, capsize=6,
        color=colors_all, edgecolor="black", linewidth=1.1, alpha=0.9, zorder=3,
        error_kw={"elinewidth": 1.6, "ecolor": "black", "capthick": 1.6, "zorder": 4},
        label="Vazão Média ± Desvio Padrão (s)"
    )

    max_y1 = max(m + s for m, s in zip(means_all, stds_all))
    ax1.set_ylim(0, max_y1 * 1.24)
    ax1.set_xticks(x1)
    ax1.set_xticklabels(labels_all, fontweight="bold")
    ax1.set_ylabel("Vazão Média (Mbps)", fontweight="bold")
    ax1.set_title("(a) Capacidade Baseline LAN vs. Cenário WAN (E01–E03)", fontweight="bold")

    for bar, m, s in zip(bars1, means_all, stds_all):
        ax1.annotate(
            f"{m:.1f} ± {s:.1f}\nMbps",
            xy=(bar.get_x() + bar.get_width() / 2, m + s),
            xytext=(0, 6), textcoords="offset points",
            ha="center", va="bottom", fontsize=9.5, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#dddddd", alpha=0.9)
        )

    # --- Painel (b): Zoom Direto no Cenário WAN Degradado (50 ms RTT, 2% Perda) ---
    labels_wan = [
        "E02: TCP CUBIC\n(Baseado em Perda)",
        "E03: TCP BBR\n(Baseado em Modelo BDP)",
    ]
    means_wan = [e02["throughput_mean_mbps"], e03["throughput_mean_mbps"]]
    stds_wan = [e02["throughput_std_mbps"], e03["throughput_std_mbps"]]
    retrans_wan = [e02["retrans_total"], e03["retrans_total"]]
    colors_wan = ["#d62728", "#2ca02c"]

    x2 = np.arange(len(labels_wan))
    bars2 = ax2.bar(
        x2, means_wan, width=0.46, yerr=stds_wan, capsize=7,
        color=colors_wan, edgecolor="black", linewidth=1.1, alpha=0.9, zorder=3,
        error_kw={"elinewidth": 1.8, "ecolor": "black", "capthick": 1.8, "zorder": 4}
    )

    max_y2 = max(m + s for m, s in zip(means_wan, stds_wan))
    ax2.set_ylim(0, max_y2 * 1.32)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(labels_wan, fontweight="bold")
    ax2.set_ylabel("Vazão Média na WAN (Mbps)", fontweight="bold")
    ax2.set_title("(b) Destaque WAN Degradada (50 ms RTT, 2% Perda: E02 vs. E03)", fontweight="bold")

    for bar, m, s, retr in zip(bars2, means_wan, stds_wan, retrans_wan):
        ax2.annotate(
            f"{m:.2f} ± {s:.2f} Mbps\n(Total Retr: {retr})",
            xy=(bar.get_x() + bar.get_width() / 2, m + s),
            xytext=(0, 7), textcoords="offset points",
            ha="center", va="bottom", fontsize=9.5, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#cccccc", alpha=0.95)
        )

    if e02["throughput_mean_mbps"] > 0:
        ratio = e03["throughput_mean_mbps"] / e02["throughput_mean_mbps"]
        ax2.text(
            0.04, 0.88,
            f"Ganho BBR vs. CUBIC na WAN:\n{ratio:.1f}x maior vazão sustentada",
            transform=ax2.transAxes, ha="left", va="top",
            fontsize=9.8, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#e8f8e8", edgecolor="#2ca02c", alpha=0.96)
        )

    fig.suptitle(
        "Gráfico 1 (Bloco A): Vazão Média TCP CUBIC (LAN/WAN) vs. TCP BBR (WAN) — Barras de Erro: Desvio Padrão (N=5)",
        fontweight="bold", y=1.02
    )
    plt.tight_layout()

    out_path = os.path.join(plots_dir, "fig1_bloco_a_vazao_cc.png")
    plt.savefig(out_path, dpi=300)
    plt.close(fig)
    if os.path.exists(relatorio_dir):
        shutil.copy2(out_path, os.path.join(relatorio_dir, "fig1_bloco_a_vazao_cc.png"))
    print(f"[+] Gráfico 1 (Bloco A) salvo em {out_path}")


def plot_bloco_b(summary_rows: list[dict], plots_dir: str, relatorio_dir: str):
    """
    Gráfico 2 (Bloco B): TTFB médio (ms) comparando HTTP/2 vs. HTTP/3 Cold vs. HTTP/3 Warm/Resumed,
    com barras de erro representando o desvio padrão (s).
    """
    rows_b = {r["test_id"]: r for r in summary_rows if r["block"] == "Bloco B"}
    e04, e05, e06 = rows_b["E04"], rows_b["E05"], rows_b["E06"]

    fig, ax = plt.subplots(figsize=(9.2, 5.3))

    labels = [
        "E04: HTTPS (HTTP/2)\nsobre TCP + TLS 1.3\n[2 RTTs Handshake + 1 RTT Req]",
        "E05: HTTP/3 Cold (1-RTT)\nHandshake QUIC Integrado\n[1 RTT Handshake + 1 RTT Req]",
        "E06: HTTP/3 Warm / Resumed\nSession Resumption / 0-RTT\n[0 RTT Handshake + 1 RTT Req]",
    ]
    means = [e04["ttfb_mean_ms"], e05["ttfb_mean_ms"], e06["ttfb_mean_ms"]]
    stds = [e04["ttfb_std_ms"], e05["ttfb_std_ms"], e06["ttfb_std_ms"]]
    colors = ["#ff7f0e", "#1f77b4", "#2ca02c"]

    x = np.arange(len(labels))
    bars = ax.bar(
        x, means, width=0.46, yerr=stds, capsize=7,
        color=colors, edgecolor="black", linewidth=1.1, alpha=0.92, zorder=3,
        error_kw={"elinewidth": 1.8, "ecolor": "black", "capthick": 1.8, "zorder": 4},
        label="TTFB Médio (ms) ± Desvio Padrão (s)"
    )

    # Linhas horizontais teóricas de múltiplos de RTT (RTT = 50 ms) atrás das barras
    ax.axhline(150, color="#b85c00", linestyle="--", linewidth=1.1, alpha=0.65, zorder=2,
               label="Patamares Teóricos de RTT (50 ms, 100 ms, 150 ms)")
    ax.axhline(100, color="#15527c", linestyle="--", linewidth=1.1, alpha=0.65, zorder=2)
    ax.axhline(50, color="#1e701e", linestyle="--", linewidth=1.1, alpha=0.65, zorder=2)

    # Rótulos limpos nas lacunas entre as barras para zero sobreposição
    ax.text(0.50, 152.0, "3 RTTs = 150 ms (TCP + TLS + Req)", ha="center", va="bottom",
            fontsize=8.8, color="#7a3d00", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.18", facecolor="#fff8f0", edgecolor="none", alpha=0.88))
    ax.text(1.50, 102.0, "2 RTTs = 100 ms (QUIC 1-RTT + Req)", ha="center", va="bottom",
            fontsize=8.8, color="#0f3c5c", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.18", facecolor="#f0f7ff", edgecolor="none", alpha=0.88))
    ax.text(1.42, 52.0, "1 RTT = 50 ms (0-RTT / Sem Handshake)", ha="center", va="bottom",
            fontsize=8.8, color="#145214", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.18", facecolor="#f0fff0", edgecolor="none", alpha=0.88))

    max_y = max(m + s for m, s in zip(means, stds))
    ax.set_ylim(0, max(max_y * 1.25, 205))
    ax.set_xlim(-0.5, 2.5)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontweight="bold")
    ax.set_ylabel("Time to First Byte — TTFB / time_starttransfer (ms)", fontweight="bold")
    ax.set_xlabel("Modo de Estabelecimento de Conexão (Cenário 3 WAN: RTT = 50 ms, 0% Perda, Objeto 1 KB)", fontweight="bold")
    ax.set_title(
        "Gráfico 2 (Bloco B): TTFB Médio — HTTP/2 vs. HTTP/3 Cold (1-RTT) vs. HTTP/3 Warm/Resumed (0-RTT)\n"
        "Barras de Erro: Desvio Padrão Amostral (N=5)",
        fontweight="bold"
    )

    for bar, m, s in zip(bars, means, stds):
        ax.annotate(
            f"{m:.2f} ± {s:.2f} ms",
            xy=(bar.get_x() + bar.get_width() / 2, m + s),
            xytext=(0, 7), textcoords="offset points",
            ha="center", va="bottom", fontsize=10, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#cccccc", alpha=0.95)
        )

    ax.legend(loc="upper right", frameon=True)
    plt.tight_layout()

    out_path = os.path.join(plots_dir, "fig2_bloco_b_ttfb_handshake.png")
    plt.savefig(out_path, dpi=300)
    plt.close(fig)
    if os.path.exists(relatorio_dir):
        shutil.copy2(out_path, os.path.join(relatorio_dir, "fig2_bloco_b_ttfb_handshake.png"))
    print(f"[+] Gráfico 2 (Bloco B) salvo em {out_path}")


def generate_all_plots(base_dir: str):
    summary_json = os.path.join(base_dir, "data", "processed", "summary_table.json")
    plots_dir = os.path.join(base_dir, "data", "plots")
    relatorio_dir = os.path.join(base_dir, "relatorio")
    os.makedirs(plots_dir, exist_ok=True)
    os.makedirs(relatorio_dir, exist_ok=True)

    with open(summary_json, "r", encoding="utf-8") as f:
        summary_rows = json.load(f)

    plot_bloco_a(summary_rows, plots_dir, relatorio_dir)
    plot_bloco_b(summary_rows, plots_dir, relatorio_dir)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    generate_all_plots(base_dir)
