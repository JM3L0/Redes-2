#!/usr/bin/env python3
"""
generate_plots.py - Geracao dos Graficos Cientificos
=====================================================
Redes de Computadores II (UFPI - 2026-2) - Avaliacao 1
Aluno: Joao Marcos Sousa Rufino Leal

Graficos gerados (1 imagem por grafico):
  graf1a  - Goodput Efetivo vs Taxa de Injecao (Cenario A, UDP)
  graf1b  - Jitter vs Taxa de Injecao (Cenario A, UDP)
  graf2   - Overhead de Cabecalho por Protocolo (Cenario A)
  graf3a  - FCT por Protocolo e Tamanho de Arquivo (Cenario B)
  graf3b  - Goodput por Protocolo e Tamanho de Arquivo (Cenario B)
  graf4a  - Latencia de Handshake TLS/QUIC (Cenario B)
  graf4b  - TTFB por Protocolo (Cenario B)
  graf5a  - FCT Medio sob Perda de Pacotes (Cenario C)
  graf5b  - FCT p95 sob Perda de Pacotes (Cenario C)
  graf6   - CDF do FCT - Evidencia do HoL Blocking (Cenario C, 5%)
  graf7a  - Overhead de Cabecalho Empirico via PCAP
  graf7b  - Retransmissoes TCP via PCAP

Uso:
  python3 analysis/generate_plots.py [--proc-dir data/processed] [--out-dir data/plots]
"""

import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paleta e mapeamentos
# ---------------------------------------------------------------------------
PROTOCOL_COLORS = {
    "http1.1":             "#E63946",
    "http2":               "#457B9D",
    "http3":               "#2A9D8F",
    "UDP":                 "#F4A261",
    "TCP (min)":           "#457B9D",
    "TCP (max)":           "#1D3557",
    "QUIC (Short Header)": "#2A9D8F",
}
PROTOCOL_LABELS = {
    "http1.1": "HTTP/1.1 (TCP+TLS)",
    "http2":   "HTTP/2 (TCP+TLS)",
    "http3":   "HTTP/3 (QUIC)",
    "UDP":     "UDP Puro",
}

DPI        = 300
FIG_W      = 7
FIG_H      = 4.8
FONT_LABEL = 11
FONT_TICK  = 9
FONT_ANNOT = 8

# ---------------------------------------------------------------------------
# Estilo global (inspirado na figura de referencia)
# ---------------------------------------------------------------------------
plt.rcParams.update({
    "font.family":        "DejaVu Sans",
    "font.size":          FONT_TICK,
    "axes.facecolor":     "#f0f0f0",
    "figure.facecolor":   "white",
    "axes.grid":          True,
    "grid.color":         "white",
    "grid.linewidth":     0.8,
    "grid.linestyle":     "-",
    "grid.alpha":         1.0,
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.spines.left":   True,
    "axes.spines.bottom": True,
    "axes.edgecolor":     "#bbbbbb",
    "legend.framealpha":  0.9,
    "legend.edgecolor":   "#cccccc",
    "legend.fontsize":    FONT_TICK,
})


def _save(fig: plt.Figure, out_dir: Path, name: str) -> None:
    dest = out_dir / name
    fig.savefig(dest, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  [+] Salvo: {dest}")


def _new_fig():
    return plt.subplots(figsize=(FIG_W, FIG_H))


# ---------------------------------------------------------------------------
# Graf. 1a: Goodput Efetivo vs Taxa de Injecao  (Cenario A)
# ---------------------------------------------------------------------------
def plot_1a_goodput(proc_dir: Path, out_dir: Path) -> None:
    path = proc_dir / "scenario_a_goodput.csv"
    if not path.exists():
        print("[AVISO] scenario_a_goodput.csv ausente. Pulando graf1a.")
        return

    df = pd.read_csv(path)
    fig, ax = _new_fig()

    rates = df["target_rate_mbps"]
    ax.plot(rates, df["mean"], "o-",
            color=PROTOCOL_COLORS["UDP"], linewidth=2, label="Goodput medio")
    ax.fill_between(rates, df["ic95_low"], df["ic95_high"],
                    alpha=0.25, color=PROTOCOL_COLORS["UDP"], label="IC 95%")
    ax.plot(rates, rates, "k--", linewidth=1, alpha=0.5, label="Ideal")

    ax.set_xlabel("Taxa de Injecao (Mbit/s)", fontsize=FONT_LABEL)
    ax.set_ylabel("Goodput Efetivo (Mbit/s)", fontsize=FONT_LABEL)
    ax.tick_params(labelsize=FONT_TICK)
    ax.legend(loc="upper left")

    fig.tight_layout()
    _save(fig, out_dir, "graf1a_goodput_vs_taxa.png")


# ---------------------------------------------------------------------------
# Graf. 1b: Jitter vs Taxa de Injecao  (Cenario A)
# ---------------------------------------------------------------------------
def plot_1b_jitter(proc_dir: Path, out_dir: Path) -> None:
    path = proc_dir / "scenario_a_jitter.csv"
    if not path.exists():
        print("[AVISO] scenario_a_jitter.csv ausente. Pulando graf1b.")
        return

    df = pd.read_csv(path)
    fig, ax = _new_fig()

    # Usar posicoes categoricas uniformes para evitar sobreposicao de barras
    rates     = df["target_rate_mbps"]
    x_pos     = np.arange(len(rates))
    jitter_ms = df["mean"] * 1e3
    error_ms  = df["ic95_half"] * 1e3

    ax.bar(x_pos, jitter_ms,
           yerr=error_ms,
           color=PROTOCOL_COLORS["UDP"],
           alpha=0.85, capsize=4, ecolor="#555555",
           label="Jitter +/- IC 95%",
           width=0.6)

    # Rotulos do eixo X com o valor real da taxa
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f"{int(r)}" for r in rates], fontsize=FONT_TICK)
    ax.set_xlabel("Taxa de Injecao (Mbit/s)", fontsize=FONT_LABEL)
    ax.set_ylabel("Jitter (ms)", fontsize=FONT_LABEL)
    ax.tick_params(labelsize=FONT_TICK)
    ax.legend(loc="upper right")

    fig.tight_layout()
    _save(fig, out_dir, "graf1b_jitter_vs_taxa.png")


# ---------------------------------------------------------------------------
# Graf. 2: Overhead de Cabecalho por Protocolo  (Cenario A)
# ---------------------------------------------------------------------------
def plot_2_overhead(proc_dir: Path, out_dir: Path) -> None:
    path = proc_dir / "scenario_a_header_overhead.csv"
    if not path.exists():
        print("[AVISO] scenario_a_header_overhead.csv ausente. Pulando graf2.")
        return

    df = pd.read_csv(path)
    fig, ax = _new_fig()

    colors = [PROTOCOL_COLORS.get(p, "#888888") for p in df["protocol"]]
    bars   = ax.bar(df["protocol"], df["total_overhead_bytes"],
                    color=colors, alpha=0.85, width=0.5)

    for bar, val in zip(bars, df["total_overhead_bytes"]):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                f"{val} B", ha="center", va="bottom",
                fontsize=FONT_ANNOT, fontweight="bold")

    ax.set_xlabel("Protocolo de Transporte", fontsize=FONT_LABEL)
    ax.set_ylabel("Overhead por Datagrama/Segmento (bytes)", fontsize=FONT_LABEL)
    ax.tick_params(labelsize=FONT_TICK)
    ax.set_ylim(0, df["total_overhead_bytes"].max() * 1.30)

    fig.tight_layout()
    _save(fig, out_dir, "graf2_overhead_cabecalho.png")


# ---------------------------------------------------------------------------
# Graf. 3a: FCT por Protocolo e Tamanho  (Cenario B)
# ---------------------------------------------------------------------------
def plot_3a_fct(proc_dir: Path, out_dir: Path) -> None:
    path = proc_dir / "scenario_b_fct.csv"
    if not path.exists():
        print("[AVISO] scenario_b_fct.csv ausente. Pulando graf3a.")
        return

    df      = pd.read_csv(path)
    files   = sorted(df["file_size_label"].unique())
    protos  = ["http1.1", "http2", "http3"]
    x       = np.arange(len(protos))
    width   = 0.30
    n_files = len(files)

    fig, ax = _new_fig()

    # Calcular ylim antecipado para reservar espaco para anotacoes
    all_tops = []
    file_handles = []
    bar_info = []   # (x_center, top, p95_label)

    for fi, f_label in enumerate(files):
        sub    = df[df["file_size_label"] == f_label].set_index("protocol")
        offset = (fi - (n_files - 1) / 2) * width
        hatch  = "/" if fi == 1 else ""
        for pi, proto in enumerate(protos):
            if proto not in sub.index:
                continue
            row  = sub.loc[proto]
            top  = row["mean"] + row["ic95_half"]
            all_tops.append(top)
            ax.bar(pi + offset, row["mean"],
                   width=width,
                   color=PROTOCOL_COLORS.get(proto, "#888888"),
                   alpha=0.85, hatch=hatch,
                   yerr=row["ic95_half"], capsize=3, ecolor="#444444")
            bar_info.append((pi + offset, top, f"p95={row['p95']:.1f}s"))
        file_handles.append((plt.Rectangle((0, 0), 1, 1,
                              color="#aaaaaa", hatch=hatch, alpha=0.85), f_label))

    # Reservar 20% extra de altura para os rotulos p95
    y_max = max(all_tops) if all_tops else 1
    ax.set_ylim(0, y_max * 1.28)

    # Anotacoes p95 horizontais, acima da barra de erro
    for x_c, top, label in bar_info:
        ax.text(x_c, top + y_max * 0.02, label,
                ha="center", va="bottom", fontsize=7,
                color="#333333")

    ax.set_xticks(x)
    ax.set_xticklabels([PROTOCOL_LABELS.get(p, p) for p in protos],
                       fontsize=FONT_TICK)
    ax.set_ylabel("Flow Completion Time - FCT (s)", fontsize=FONT_LABEL)
    ax.tick_params(labelsize=FONT_TICK)

    # Legenda de protocolos (por cor) + legenda de tamanhos (por hatch)
    # empilhadas: Protocolo em cima, Arquivo embaixo (loc upper left)
    proto_handles = [plt.Rectangle((0, 0), 1, 1,
                     color=PROTOCOL_COLORS.get(p, "#888888"), alpha=0.85)
                     for p in protos]
    all_handles = proto_handles + [h for h, _ in file_handles]
    all_labels  = ([PROTOCOL_LABELS.get(p, p) for p in protos]
                   + [l for _, l in file_handles])

    # Separador visual entre os dois grupos via titulo de grupo nao disponivel
    # usamos ncol=1 e inserimos handle vazio como separador
    sep_handle = plt.Rectangle((0, 0), 1, 1, color="none", fill=False,
                                linewidth=0)
    final_handles = proto_handles + [sep_handle] + [h for h, _ in file_handles]
    final_labels  = ([PROTOCOL_LABELS.get(p, p) for p in protos]
                     + ["── Arquivo ──"]
                     + [l for _, l in file_handles])

    ax.legend(final_handles, final_labels,
              loc="upper left", ncol=1,
              fontsize=FONT_TICK - 1,
              handlelength=1.2, handleheight=0.9,
              borderpad=0.6)

    fig.tight_layout()
    _save(fig, out_dir, "graf3a_fct_cenario_b.png")


# ---------------------------------------------------------------------------
# Graf. 3b: Goodput por Protocolo e Tamanho  (Cenario B)
# ---------------------------------------------------------------------------
def plot_3b_goodput(proc_dir: Path, out_dir: Path) -> None:
    path = proc_dir / "scenario_b_goodput.csv"
    if not path.exists():
        print("[AVISO] scenario_b_goodput.csv ausente. Pulando graf3b.")
        return

    df      = pd.read_csv(path)
    files   = sorted(df["file_size_label"].unique())
    protos  = ["http1.1", "http2", "http3"]
    x       = np.arange(len(protos))
    width   = 0.30
    n_files = len(files)

    fig, ax = _new_fig()

    all_tops     = []
    file_handles = []
    bar_info     = []   # (x_center, top, label)

    for fi, f_label in enumerate(files):
        sub    = df[df["file_size_label"] == f_label].set_index("protocol")
        offset = (fi - (n_files - 1) / 2) * width
        hatch  = "/" if fi == 1 else ""
        for pi, proto in enumerate(protos):
            if proto not in sub.index:
                continue
            row = sub.loc[proto]
            top = row["mean"] + row["ic95_half"]
            all_tops.append(top)
            ax.bar(pi + offset, row["mean"],
                   width=width,
                   color=PROTOCOL_COLORS.get(proto, "#888888"),
                   alpha=0.85, hatch=hatch,
                   yerr=row["ic95_half"], capsize=3, ecolor="#444444")
            bar_info.append((pi + offset, top, f"{row['mean']:.1f}"))
        file_handles.append((plt.Rectangle((0, 0), 1, 1,
                              color="#aaaaaa", hatch=hatch, alpha=0.85), f_label))

    y_max = max(all_tops) if all_tops else 1
    ax.set_ylim(0, y_max * 1.35)

    for x_c, top, label in bar_info:
        ax.text(x_c, top + y_max * 0.015, label,
                ha="center", va="bottom", fontsize=7,
                color="#333333",
                bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.7))

    ax.set_xticks(x)
    ax.set_xticklabels([PROTOCOL_LABELS.get(p, p) for p in protos],
                       fontsize=FONT_TICK)
    ax.set_ylabel("Goodput (Mbit/s)", fontsize=FONT_LABEL)
    ax.tick_params(labelsize=FONT_TICK)

    proto_handles = [plt.Rectangle((0, 0), 1, 1,
                     color=PROTOCOL_COLORS.get(p, "#888888"), alpha=0.85)
                     for p in protos]
    sep_handle = plt.Rectangle((0, 0), 1, 1, color="none", fill=False, linewidth=0)
    final_handles = proto_handles + [sep_handle] + [h for h, _ in file_handles]
    final_labels  = ([PROTOCOL_LABELS.get(p, p) for p in protos]
                     + ["── Arquivo ──"]
                     + [l for _, l in file_handles])
    ax.legend(final_handles, final_labels,
              loc="upper right", ncol=1,
              fontsize=FONT_TICK - 1,
              handlelength=1.2, handleheight=0.9,
              borderpad=0.6)

    fig.tight_layout()
    _save(fig, out_dir, "graf3b_goodput_cenario_b.png")


# ---------------------------------------------------------------------------
# Graf. 4a/4b: Handshake e TTFB  (Cenario B)  — funcao auxiliar
# ---------------------------------------------------------------------------
def _plot_b_latency(proc_dir: Path, out_dir: Path,
                    csv_name: str, ylabel: str, out_name: str) -> None:
    path = proc_dir / csv_name
    if not path.exists():
        print(f"[AVISO] {csv_name} ausente. Pulando {out_name}.")
        return

    df     = pd.read_csv(path)
    protos = ["http1.1", "http2", "http3"]

    file_label = ("100MB" if "100MB" in df["file_size_label"].values
                  else df["file_size_label"].iloc[0])
    sub = df[df["file_size_label"] == file_label].set_index("protocol")

    # Converter s -> ms
    means  = [sub.loc[p, "mean"]      * 1e3 if p in sub.index else 0 for p in protos]
    errors = [sub.loc[p, "ic95_half"] * 1e3 if p in sub.index else 0 for p in protos]
    colors = [PROTOCOL_COLORS.get(p, "#888888") for p in protos]

    fig, ax = _new_fig()
    bars = ax.bar(range(len(protos)), means,
                  yerr=errors, color=colors, alpha=0.85,
                  capsize=5, ecolor="#444444", width=0.45)

    y_max = max(m + e for m, e in zip(means, errors)) if means else 1
    # Anotacao acima do topo da barra de erro, com fundo branco para legibilidade
    for val, err in zip(means, errors):
        x_c = means.index(val)  # posicao categorica
    for i, (val, err) in enumerate(zip(means, errors)):
        ax.text(i, val + err + y_max * 0.04,
                f"{val:.1f} ms",
                ha="center", va="bottom",
                fontsize=FONT_ANNOT + 1, fontweight="bold",
                color="#222222",
                bbox=dict(boxstyle="round,pad=0.2", fc="white",
                          ec="#cccccc", alpha=0.85, linewidth=0.5))

    ax.set_xticks(range(len(protos)))
    ax.set_xticklabels([PROTOCOL_LABELS.get(p, p) for p in protos],
                       fontsize=FONT_TICK)
    ax.set_ylabel(ylabel, fontsize=FONT_LABEL)
    ax.tick_params(labelsize=FONT_TICK)
    ax.set_ylim(0, y_max * 1.35)

    fig.tight_layout()
    _save(fig, out_dir, out_name)


def plot_4a_handshake(proc_dir: Path, out_dir: Path) -> None:
    _plot_b_latency(proc_dir, out_dir,
                    "scenario_b_handshake.csv",
                    "Latencia de Handshake TLS/QUIC (ms)",
                    "graf4a_handshake.png")


def plot_4b_ttfb(proc_dir: Path, out_dir: Path) -> None:
    _plot_b_latency(proc_dir, out_dir,
                    "scenario_b_ttfb.csv",
                    "Time To First Byte - TTFB (ms)",
                    "graf4b_ttfb.png")


# ---------------------------------------------------------------------------
# Graf. 5a/5b: FCT sob Perdas  (Cenario C)  — funcao auxiliar
# ---------------------------------------------------------------------------
def _plot_c_bars(proc_dir: Path, out_dir: Path,
                 metric_col: str, ylabel: str, out_name: str,
                 with_error: bool = False) -> None:
    path = proc_dir / "scenario_c_fct.csv"
    if not path.exists():
        print(f"[AVISO] scenario_c_fct.csv ausente. Pulando {out_name}.")
        return

    df     = pd.read_csv(path)
    protos = ["http1.1", "http2", "http3"]
    losses = sorted(df["loss_percent"].unique())
    x      = np.arange(len(losses))
    width  = 0.24

    fig, ax = _new_fig()

    for idx, proto in enumerate(protos):
        sub    = df[df["protocol"] == proto].set_index("loss_percent")
        vals   = [sub.loc[l, metric_col]   if l in sub.index else 0 for l in losses]
        errors = ([sub.loc[l, "ic95_half"] if l in sub.index else 0 for l in losses]
                  if with_error else None)
        offset = (idx - 1) * width
        ax.bar(x + offset, vals, width,
               yerr=errors, capsize=4, ecolor="#444444",
               color=PROTOCOL_COLORS.get(proto, "#888888"), alpha=0.85,
               label=PROTOCOL_LABELS.get(proto, proto))

    ax.set_xticks(x)
    ax.set_xticklabels([f"{l}%" for l in losses], fontsize=FONT_TICK)
    ax.set_xlabel("Taxa de Perda de Pacotes (%)", fontsize=FONT_LABEL)
    ax.set_ylabel(ylabel, fontsize=FONT_LABEL)
    ax.tick_params(labelsize=FONT_TICK)
    ax.legend(loc="upper left")

    fig.tight_layout()
    _save(fig, out_dir, out_name)


def plot_5a_fct_mean(proc_dir: Path, out_dir: Path) -> None:
    _plot_c_bars(proc_dir, out_dir,
                 "mean", "FCT Medio (s)",
                 "graf5a_fct_medio_perdas.png", with_error=True)


def plot_5b_fct_p95(proc_dir: Path, out_dir: Path) -> None:
    _plot_c_bars(proc_dir, out_dir,
                 "p95", "FCT Percentil 95 (s)",
                 "graf5b_fct_p95_perdas.png", with_error=False)


# ---------------------------------------------------------------------------
# Graf. 6: CDF do FCT  (Cenario C, 5% perda)
# ---------------------------------------------------------------------------
def plot_6_cdf(proc_dir: Path, out_dir: Path) -> None:
    path = proc_dir / "scenario_c_cdf_loss5.csv"
    if not path.exists():
        print("[AVISO] scenario_c_cdf_loss5.csv ausente. Pulando graf6.")
        return

    df  = pd.read_csv(path)
    fig, ax = _new_fig()

    for proto in df["protocol"].unique():
        sub = df[df["protocol"] == proto].sort_values("fct_sec")
        ax.plot(sub["fct_sec"], sub["cdf"],
                color=PROTOCOL_COLORS.get(proto, "#888888"),
                linewidth=2, label=PROTOCOL_LABELS.get(proto, proto))

    ax.axhline(0.95, color="#888888", linestyle=":", linewidth=1.2)
    x_min, x_max = ax.get_xlim()
    ax.text(x_min + 0.02 * (x_max - x_min), 0.96,
            "p95", fontsize=FONT_TICK, color="#666666")

    ax.set_xlabel("FCT do Lote (s)", fontsize=FONT_LABEL)
    ax.set_ylabel("Fracao Acumulada (CDF)", fontsize=FONT_LABEL)
    ax.set_ylim(0, 1.05)
    ax.tick_params(labelsize=FONT_TICK)
    ax.legend(loc="lower right")

    fig.tight_layout()
    _save(fig, out_dir, "graf6_cdf_hol_blocking.png")


# ---------------------------------------------------------------------------
# Graf. 7a/7b: Analise PCAP  — funcao auxiliar
# ---------------------------------------------------------------------------
def _plot_pcap(proc_dir: Path, out_dir: Path,
               col: str, ylabel: str, out_name: str,
               color: str, fmt_fn=None) -> None:
    path = proc_dir / "pcap_overhead_analysis.csv"
    if not path.exists():
        print(f"[INFO] pcap_overhead_analysis.csv ausente. Pulando {out_name}.")
        return

    df = pd.read_csv(path)
    if df.empty:
        return

    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    labels  = [f.replace(".pcapng", "") for f in df["pcap_file"]]
    x       = range(len(labels))
    top_val = df[col].max()

    fig, ax = _new_fig()
    ax.bar(x, df[col], color=color, alpha=0.85, width=0.5)

    margin = top_val * 0.02 if top_val > 0 else 0.01
    for i, val in enumerate(df[col]):
        txt = fmt_fn(val) if fmt_fn else f"{val:.2f}"
        ax.text(i, val + margin, txt,
                ha="center", va="bottom", fontsize=FONT_ANNOT)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20, ha="right", fontsize=FONT_TICK)
    ax.set_ylabel(ylabel, fontsize=FONT_LABEL)
    ax.tick_params(labelsize=FONT_TICK)
    ax.set_ylim(0, top_val * 1.35 if top_val > 0 else 1)

    fig.tight_layout()
    _save(fig, out_dir, out_name)


def plot_7a_pcap_overhead(proc_dir: Path, out_dir: Path) -> None:
    _plot_pcap(proc_dir, out_dir,
               "overhead_percent",
               "Overhead de Cabecalho (%)",
               "graf7a_pcap_overhead.png",
               "#457B9D",
               fmt_fn=lambda v: f"{v:.2f}%")


def plot_7b_pcap_retrans(proc_dir: Path, out_dir: Path) -> None:
    _plot_pcap(proc_dir, out_dir,
               "tcp_retransmissions",
               "Retransmissoes TCP (segmentos)",
               "graf7b_pcap_retransmissoes.png",
               "#E63946",
               fmt_fn=lambda v: str(int(v)))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera os graficos cientificos da avaliacao.")
    parser.add_argument("--proc-dir", default="data/processed",
                        help="Diretorio com dados processados")
    parser.add_argument("--out-dir",  default="data/plots",
                        help="Diretorio de saida dos graficos")
    args = parser.parse_args()

    proc_dir = Path(args.proc_dir)
    out_dir  = Path(args.out_dir)

    if not proc_dir.exists():
        print(f"[ERRO] Execute 'parse_logs.py' primeiro para gerar '{proc_dir}'.")
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"[*] Gerando graficos: '{proc_dir}' -> '{out_dir}' ({DPI} DPI)\n")

    steps = [
        ("Graf. 1a  Goodput vs Taxa de Injecao",    plot_1a_goodput),
        ("Graf. 1b  Jitter vs Taxa de Injecao",      plot_1b_jitter),
        ("Graf. 2   Overhead de Cabecalho",           plot_2_overhead),
        ("Graf. 3a  FCT Cenario B",                   plot_3a_fct),
        ("Graf. 3b  Goodput Cenario B",               plot_3b_goodput),
        ("Graf. 4a  Handshake TLS/QUIC",              plot_4a_handshake),
        ("Graf. 4b  TTFB",                            plot_4b_ttfb),
        ("Graf. 5a  FCT Medio sob Perdas",            plot_5a_fct_mean),
        ("Graf. 5b  FCT p95 sob Perdas",              plot_5b_fct_p95),
        ("Graf. 6   CDF do FCT (HoL Blocking)",       plot_6_cdf),
        ("Graf. 7a  PCAP Overhead",                   plot_7a_pcap_overhead),
        ("Graf. 7b  PCAP Retransmissoes",             plot_7b_pcap_retrans),
    ]

    for label, fn in steps:
        print(f"[{label}]")
        fn(proc_dir, out_dir)

    print(f"\n[OK] {len(steps)} graficos gerados em '{out_dir}'")


if __name__ == "__main__":
    main()
