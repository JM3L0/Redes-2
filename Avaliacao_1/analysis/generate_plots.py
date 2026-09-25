#!/usr/bin/env python3
"""
generate_plots.py - Geracao dos 6 Graficos Cientificos Obrigatorios
====================================================================
Redes de Computadores II (UFPI - 2026-2) — Avaliacao 1
Aluno: Joao Marcos Sousa Rufino Leal

Graficos gerados (conforme especificacao em metricas_e_analise_dados.md):
  Graf. 1: Taxa de Injecao vs Goodput/Jitter — UDP Puro (Cenario A)
  Graf. 2: Overhead de Cabecalho Comparativo — UDP vs TCP vs QUIC (Cenario A)
  Graf. 3: Goodput e FCT — 100MB e 1GB com barras de erro (Cenario B)
  Graf. 4: Tempo de Handshake e TTFB por Protocolo (Cenario B)
  Graf. 5: FCT Medio e p95 sob Perdas — 0%, 2%, 5% (Cenario C)
  Graf. 6: CDF do FCT — Evidencia do HoL Blocking (Cenario C, perda 5%)

Uso:
  python3 analysis/generate_plots.py [--proc-dir data/processed] [--out-dir data/plots]
"""

import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")   # Backend sem display (ideal para execucao em conteineres)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Estetica global da publicacao
# ---------------------------------------------------------------------------
PROTOCOL_COLORS = {
    "http1.1":   "#E63946",   # Vermelho
    "http2":     "#457B9D",   # Azul medio
    "http3":     "#2A9D8F",   # Verde-azulado (QUIC)
    "UDP":       "#F4A261",   # Laranja
    "TCP (min)": "#457B9D",
    "TCP (max)": "#1D3557",
    "QUIC (Short Header)": "#2A9D8F",
}
PROTOCOL_LABELS = {
    "http1.1": "HTTP/1.1 (TCP+TLS)",
    "http2":   "HTTP/2 (TCP+TLS)",
    "http3":   "HTTP/3 (QUIC)",
    "UDP":     "UDP Puro",
}

DPI = 300
FONT_TITLE = 13
FONT_LABEL = 11
FONT_TICK  = 9

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.35,
    "grid.linestyle": "--",
})


def savefig(fig: plt.Figure, path: Path, name: str) -> None:
    dest = path / name
    fig.savefig(dest, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  [+] Salvo: {dest}")


# ---------------------------------------------------------------------------
# Grafico 1: Taxa de Injecao vs Goodput e Jitter (Cenario A - UDP Puro)
# ---------------------------------------------------------------------------
def plot_scenario_a_goodput_jitter(proc_dir: Path, out_dir: Path) -> None:
    g_path = proc_dir / "scenario_a_goodput.csv"
    j_path = proc_dir / "scenario_a_jitter.csv"
    if not g_path.exists() or not j_path.exists():
        print("[AVISO] Dados do Cenario A ausentes. Pulando Grafico 1.")
        return

    gdf = pd.read_csv(g_path)
    jdf = pd.read_csv(j_path)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Cenário A — UDP Puro: Taxa de Injeção vs Goodput e Jitter", fontsize=FONT_TITLE, fontweight="bold")

    rates = gdf["target_rate_mbps"]

    # Painel esquerdo: Goodput
    ax1.plot(rates, gdf["mean"], "o-", color=PROTOCOL_COLORS["UDP"], linewidth=2, label="Goodput médio")
    ax1.fill_between(rates, gdf["ic95_low"], gdf["ic95_high"], alpha=0.25, color=PROTOCOL_COLORS["UDP"], label="IC 95%")
    ax1.plot(rates, rates, "k--", linewidth=1, alpha=0.5, label="Ideal (injeção = goodput)")
    ax1.set_xlabel("Taxa de Injeção (Mbps)", fontsize=FONT_LABEL)
    ax1.set_ylabel("Goodput Efetivo (Mbps)", fontsize=FONT_LABEL)
    ax1.set_title("Vazão Efetiva vs Taxa Injetada", fontsize=FONT_LABEL)
    ax1.legend(fontsize=FONT_TICK)
    ax1.tick_params(labelsize=FONT_TICK)

    # Painel direito: Jitter
    ax2.bar(rates, jdf["mean"], yerr=jdf["ic95_half"], color=PROTOCOL_COLORS["UDP"],
            alpha=0.8, capsize=4, ecolor="gray", label="Jitter ± IC 95%")
    ax2.set_xlabel("Taxa de Injeção (Mbps)", fontsize=FONT_LABEL)
    ax2.set_ylabel("Jitter (ms)", fontsize=FONT_LABEL)
    ax2.set_title("Jitter por Taxa de Injeção", fontsize=FONT_LABEL)
    ax2.legend(fontsize=FONT_TICK)
    ax2.tick_params(labelsize=FONT_TICK)

    savefig(fig, out_dir, "graf1_scenario_a_goodput_jitter.png")


# ---------------------------------------------------------------------------
# Grafico 2: Overhead de Cabecalho (Cenario A - comparativo de protocolos)
# ---------------------------------------------------------------------------
def plot_scenario_a_overhead(proc_dir: Path, out_dir: Path) -> None:
    path = proc_dir / "scenario_a_header_overhead.csv"
    if not path.exists():
        print("[AVISO] Dados de overhead ausentes. Pulando Grafico 2.")
        return

    df = pd.read_csv(path)
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.suptitle("Cenário A — Overhead de Cabeçalho por Protocolo de Transporte",
                 fontsize=FONT_TITLE, fontweight="bold")

    colors = [PROTOCOL_COLORS.get(p, "#888") for p in df["protocol"]]
    bars = ax.bar(df["protocol"], df["total_overhead_bytes"], color=colors, alpha=0.85, width=0.55)

    # Anotacoes de valor nas barras
    for bar, val in zip(bars, df["total_overhead_bytes"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{val} B", ha="center", va="bottom", fontsize=FONT_TICK, fontweight="bold")

    ax.set_ylabel("Overhead Total por Datagrama/Segmento (bytes)", fontsize=FONT_LABEL)
    ax.set_xlabel("Protocolo", fontsize=FONT_LABEL)
    ax.tick_params(labelsize=FONT_TICK)
    ax.set_ylim(0, df["total_overhead_bytes"].max() * 1.25)

    savefig(fig, out_dir, "graf2_scenario_a_header_overhead.png")


# ---------------------------------------------------------------------------
# Grafico 3: FCT e Goodput por protocolo e tamanho de arquivo (Cenario B)
# ---------------------------------------------------------------------------
def plot_scenario_b_fct_goodput(proc_dir: Path, out_dir: Path) -> None:
    fct_path = proc_dir / "scenario_b_fct.csv"
    gpt_path = proc_dir / "scenario_b_goodput.csv"
    if not fct_path.exists() or not gpt_path.exists():
        print("[AVISO] Dados do Cenario B ausentes. Pulando Grafico 3.")
        return

    fct_df = pd.read_csv(fct_path)
    gpt_df = pd.read_csv(gpt_path)
    files  = sorted(fct_df["file_size_label"].unique())
    protos = ["http1.1", "http2", "http3"]

    fig, axes = plt.subplots(2, len(files), figsize=(6 * len(files), 10))
    fig.suptitle("Cenário B — FCT e Goodput: HTTP/1.1 vs HTTP/2 vs HTTP/3 (TCP vs QUIC)",
                 fontsize=FONT_TITLE, fontweight="bold")

    bar_width = 0.25

    for col, f_label in enumerate(files):
        fct_sub = fct_df[fct_df["file_size_label"] == f_label].set_index("protocol")
        gpt_sub = gpt_df[gpt_df["file_size_label"] == f_label].set_index("protocol")

        # FCT
        ax_fct = axes[0][col]
        for i, proto in enumerate(protos):
            if proto not in fct_sub.index:
                continue
            row = fct_sub.loc[proto]
            ax_fct.bar(i, row["mean"], width=bar_width * 2.5,
                       color=PROTOCOL_COLORS.get(proto, "#888"), alpha=0.85,
                       yerr=row["ic95_half"], capsize=5, ecolor="gray",
                       label=PROTOCOL_LABELS.get(proto, proto))
            ax_fct.text(i, row["mean"] + row["ic95_half"] + 0.1,
                        f"p95={row['p95']:.1f}s", ha="center", fontsize=7)

        ax_fct.set_title(f"FCT — {f_label}", fontsize=FONT_LABEL)
        ax_fct.set_ylabel("Tempo de Conclusão (s)", fontsize=FONT_LABEL)
        ax_fct.set_xticks(range(len(protos)))
        ax_fct.set_xticklabels([PROTOCOL_LABELS.get(p, p) for p in protos], fontsize=FONT_TICK, rotation=10)
        ax_fct.tick_params(labelsize=FONT_TICK)

        # Goodput
        ax_gpt = axes[1][col]
        for i, proto in enumerate(protos):
            if proto not in gpt_sub.index:
                continue
            row = gpt_sub.loc[proto]
            ax_gpt.bar(i, row["mean"], width=bar_width * 2.5,
                       color=PROTOCOL_COLORS.get(proto, "#888"), alpha=0.85,
                       yerr=row["ic95_half"], capsize=5, ecolor="gray")
            ax_gpt.text(i, row["mean"] + row["ic95_half"] + 0.2,
                        f"{row['mean']:.1f}", ha="center", fontsize=7)

        ax_gpt.set_title(f"Goodput — {f_label}", fontsize=FONT_LABEL)
        ax_gpt.set_ylabel("Goodput (Mbps)", fontsize=FONT_LABEL)
        ax_gpt.set_xticks(range(len(protos)))
        ax_gpt.set_xticklabels([PROTOCOL_LABELS.get(p, p) for p in protos], fontsize=FONT_TICK, rotation=10)
        ax_gpt.tick_params(labelsize=FONT_TICK)

    handles = [plt.Rectangle((0, 0), 1, 1, color=PROTOCOL_COLORS.get(p, "#888"), alpha=0.85) for p in protos]
    labels  = [PROTOCOL_LABELS.get(p, p) for p in protos]
    fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=FONT_TICK, bbox_to_anchor=(0.5, 0.01))
    fig.tight_layout(rect=[0, 0.05, 1, 0.97])

    savefig(fig, out_dir, "graf3_scenario_b_fct_goodput.png")


# ---------------------------------------------------------------------------
# Grafico 4: Handshake (TLS/QUIC) e TTFB por Protocolo (Cenario B)
# ---------------------------------------------------------------------------
def plot_scenario_b_handshake(proc_dir: Path, out_dir: Path) -> None:
    hs_path   = proc_dir / "scenario_b_handshake.csv"
    ttfb_path = proc_dir / "scenario_b_ttfb.csv"
    if not hs_path.exists() or not ttfb_path.exists():
        print("[AVISO] Dados de handshake ausentes. Pulando Grafico 4.")
        return

    hs_df   = pd.read_csv(hs_path)
    ttfb_df = pd.read_csv(ttfb_path)
    protos  = ["http1.1", "http2", "http3"]

    # Handshake independe do tamanho do payload transferido
    file_label = "100MB" if "100MB" in hs_df["file_size_label"].values else hs_df["file_size_label"].iloc[0]
    hs_sub   = hs_df[hs_df["file_size_label"] == file_label].set_index("protocol")
    ttfb_sub = ttfb_df[ttfb_df["file_size_label"] == file_label].set_index("protocol")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
    fig.suptitle("Cenário B — Latência de Handshake e TTFB por Protocolo",
                 fontsize=FONT_TITLE, fontweight="bold")

    for ax, sub_df, ylabel, title in [
        (ax1, hs_sub,   "Tempo de Handshake TLS/QUIC (s)", "Overhead de Estabelecimento de Sessão"),
        (ax2, ttfb_sub, "Time To First Byte — TTFB (s)",   "TTFB (Latência do Primeiro Byte Útil)"),
    ]:
        means  = [sub_df.loc[p, "mean"]      if p in sub_df.index else 0 for p in protos]
        errors = [sub_df.loc[p, "ic95_half"] if p in sub_df.index else 0 for p in protos]
        colors = [PROTOCOL_COLORS.get(p, "#888") for p in protos]
        bars   = ax.bar(range(len(protos)), means, yerr=errors, color=colors, alpha=0.85,
                        capsize=5, ecolor="gray", width=0.5)
        for bar, val in zip(bars, means):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.001,
                    f"{val*1000:.1f} ms", ha="center", va="bottom", fontsize=FONT_TICK)
        ax.set_xticks(range(len(protos)))
        ax.set_xticklabels([PROTOCOL_LABELS.get(p, p) for p in protos], fontsize=FONT_TICK)
        ax.set_ylabel(ylabel, fontsize=FONT_LABEL)
        ax.set_title(title, fontsize=FONT_LABEL)
        ax.tick_params(labelsize=FONT_TICK)

    fig.tight_layout()
    savefig(fig, out_dir, "graf4_scenario_b_handshake_ttfb.png")


# ---------------------------------------------------------------------------
# Grafico 5: FCT Medio e p95 sob Perdas — Cenario C
# ---------------------------------------------------------------------------
def plot_scenario_c_fct_loss(proc_dir: Path, out_dir: Path) -> None:
    path = proc_dir / "scenario_c_fct.csv"
    if not path.exists():
        print("[AVISO] Dados do Cenario C ausentes. Pulando Grafico 5.")
        return

    df     = pd.read_csv(path)
    protos = ["http1.1", "http2", "http3"]
    losses = sorted(df["loss_percent"].unique())

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
    fig.suptitle("Cenário C — FCT do Lote de 100 Objetos sob Perda de Pacotes",
                 fontsize=FONT_TITLE, fontweight="bold")

    x     = np.arange(len(losses))
    width = 0.25

    for idx, proto in enumerate(protos):
        sub    = df[df["protocol"] == proto].set_index("loss_percent")
        means  = [sub.loc[l, "mean"]      if l in sub.index else 0 for l in losses]
        errors = [sub.loc[l, "ic95_half"] if l in sub.index else 0 for l in losses]
        p95s   = [sub.loc[l, "p95"]       if l in sub.index else 0 for l in losses]

        offset = (idx - 1) * width
        ax1.bar(x + offset, means, width, yerr=errors,
                color=PROTOCOL_COLORS.get(proto, "#888"), alpha=0.85, capsize=4, ecolor="gray",
                label=PROTOCOL_LABELS.get(proto, proto))
        ax2.bar(x + offset, p95s, width,
                color=PROTOCOL_COLORS.get(proto, "#888"), alpha=0.85,
                label=PROTOCOL_LABELS.get(proto, proto))

    for ax, title, ylabel in [
        (ax1, "FCT Médio ± IC 95%",           "FCT Médio (s)"),
        (ax2, "Percentil p95 do FCT do Lote",  "FCT p95 (s)"),
    ]:
        ax.set_xticks(x)
        ax.set_xticklabels([f"{l}% perda" for l in losses], fontsize=FONT_TICK)
        ax.set_ylabel(ylabel, fontsize=FONT_LABEL)
        ax.set_title(title, fontsize=FONT_LABEL)
        ax.legend(fontsize=FONT_TICK)
        ax.tick_params(labelsize=FONT_TICK)

    fig.tight_layout()
    savefig(fig, out_dir, "graf5_scenario_c_fct_loss.png")


# ---------------------------------------------------------------------------
# Grafico 6: CDF do FCT — Evidencia do HoL Blocking (Cenario C, 5% perda)
# ---------------------------------------------------------------------------
def plot_scenario_c_cdf(proc_dir: Path, out_dir: Path) -> None:
    path = proc_dir / "scenario_c_cdf_loss5.csv"
    if not path.exists():
        print("[AVISO] Dados de CDF ausentes. Pulando Grafico 6.")
        return

    df = pd.read_csv(path)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.suptitle("Cenário C — CDF do FCT (100 Objetos, 5% Perda)\nEvidência do Head-of-Line Blocking",
                 fontsize=FONT_TITLE, fontweight="bold")

    for proto in df["protocol"].unique():
        sub = df[df["protocol"] == proto].sort_values("fct_sec")
        ax.plot(sub["fct_sec"], sub["cdf"],
                color=PROTOCOL_COLORS.get(proto, "#888"),
                linewidth=2, label=PROTOCOL_LABELS.get(proto, proto))

    # Linha de referencia p95
    ax.axhline(0.95, color="gray", linestyle=":", linewidth=1, alpha=0.7)
    x_min, x_max = ax.get_xlim()
    ax.text(x_min + 0.02 * (x_max - x_min), 0.96, "p95", fontsize=FONT_TICK, color="gray")

    ax.set_xlabel("FCT do Lote (s)", fontsize=FONT_LABEL)
    ax.set_ylabel("CDF — Fração Acumulada das Medições", fontsize=FONT_LABEL)
    ax.legend(fontsize=FONT_TICK)
    ax.tick_params(labelsize=FONT_TICK)
    ax.set_ylim(0, 1.05)

    savefig(fig, out_dir, "graf6_scenario_c_cdf_hol_blocking.png")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Gera os 6 graficos cientificos da avaliacao.")
    parser.add_argument("--proc-dir", default="data/processed", help="Diretorio com dados processados")
    parser.add_argument("--out-dir",  default="data/plots",     help="Diretorio de saida dos graficos")
    args = parser.parse_args()

    proc_dir = Path(args.proc_dir)
    out_dir  = Path(args.out_dir)

    if not proc_dir.exists():
        print(f"[ERRO] Execute 'parse_logs.py' primeiro para gerar os dados processados em '{proc_dir}'.")
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"[*] Gerando graficos de '{proc_dir}' -> '{out_dir}' ({DPI} DPI)\n")

    print("[Graf. 1] Taxa de Injecao vs Goodput e Jitter (Cenario A)")
    plot_scenario_a_goodput_jitter(proc_dir, out_dir)

    print("[Graf. 2] Overhead de Cabecalho por Protocolo (Cenario A)")
    plot_scenario_a_overhead(proc_dir, out_dir)

    print("[Graf. 3] FCT e Goodput — 100MB e 1GB (Cenario B)")
    plot_scenario_b_fct_goodput(proc_dir, out_dir)

    print("[Graf. 4] Handshake TLS/QUIC e TTFB (Cenario B)")
    plot_scenario_b_handshake(proc_dir, out_dir)

    print("[Graf. 5] FCT Medio e p95 sob Perdas 0/2/5% (Cenario C)")
    plot_scenario_c_fct_loss(proc_dir, out_dir)

    print("[Graf. 6] CDF do FCT — Evidencia do HoL Blocking (Cenario C, 5%)")
    plot_scenario_c_cdf(proc_dir, out_dir)

    print(f"\n[OK] {6} graficos gerados em '{out_dir}'")


if __name__ == "__main__":
    main()
