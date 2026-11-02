#!/usr/bin/env python3
"""
Pipeline de Geração de Gráficos Científicos de Alta Resolução (300 DPI).
Disciplina: Redes de Computadores II (UFPI - CSHNB)
Aluno: João Marcos Sousa Rufino Leal (jsousarufinoleal@ufpi.edu.br)

Garante conformidade irrestrita com o Edital:
- BARRAS DE ERRO OBRIGATÓRIAS em todos os gráficos de barras e de linhas (evita penalidade de -10 pontos).
- Resolução de 300 DPI para impressão em artigo científico.
- Paleta acessível e formatação rigorosa de eixos, limites positivos e anotações de valores.
"""

import os
import csv
import json
from collections import defaultdict
from typing import List, Dict, Any
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Configuração de estilo científico
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 10.5,
    'figure.titlesize': 14,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

PALETTE = {
    'HTTP/1.1': '#1f77b4',       # Azul
    'HTTPS/TLS1.3': '#ff7f0e',   # Laranja
    'HTTP/3-QUIC': '#2ca02c'     # Verde
}


def load_data(csv_path: str, json_path: str) -> List[Dict[str, Any]]:
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = []
            for r in reader:
                r['iteration'] = int(r['iteration'])
                r['request_id'] = int(r['request_id'])
                r['status_code'] = int(r['status_code'])
                r['ttfb_ms'] = float(r['ttfb_ms'])
                r['load_time_ms'] = float(r['load_time_ms'])
                r['bytes_downloaded'] = int(r['bytes_downloaded'])
                r['goodput_mbps'] = float(r['goodput_mbps'])
                rows.append(r)
            return rows
    else:
        raise FileNotFoundError("Nenhum arquivo de resultados brutos encontrado em data/raw/.")


def calc_ci95_margin(vals: np.ndarray) -> float:
    vals = np.asarray(vals, dtype=float)
    vals = vals[~np.isnan(vals)]
    if len(vals) < 2:
        return 0.0
    sem = float(stats.sem(vals))
    if sem == 0.0:
        return 0.0
    mean = float(np.mean(vals))
    ci_low, _ = stats.t.interval(0.95, df=len(vals) - 1, loc=mean, scale=sem)
    return float(mean - ci_low)


def plot_fig1_ttfb(data: List[Dict[str, Any]], output_dir: str):
    """Gráfico 1: Time to First Byte (Cold TTFB) por Protocolo (LAN vs WAN) com Barras de Erro (IC 95%)."""
    fig, ax = plt.subplots(figsize=(8.5, 5.2))

    cold_rows = [r for r in data if r['mode'] == 'cold']
    scenarios = ['LAN (1ms, 0% loss)', 'WAN (50ms, 2% loss)']
    protocols = ['HTTP/1.1', 'HTTPS/TLS1.3', 'HTTP/3-QUIC']

    x = np.arange(len(scenarios))
    width = 0.25
    max_top = 0.0

    for i, proto in enumerate(protocols):
        means = []
        cis = []
        for sc in scenarios:
            sub = np.array([float(r['ttfb_ms']) for r in cold_rows if r['scenario'] == sc and r['protocol'] == proto])
            if len(sub) > 0:
                mean = float(np.mean(sub))
                err = min(calc_ci95_margin(sub), mean * 0.95)
                means.append(mean)
                cis.append(err)
                max_top = max(max_top, mean + err)
            else:
                means.append(0.0)
                cis.append(0.0)

        bars = ax.bar(
            x + (i - 1) * width, means, width, yerr=cis, capsize=5,
            label=proto, color=PALETTE[proto], edgecolor='black', alpha=0.9,
            error_kw={'elinewidth': 1.5, 'ecolor': 'black'}
        )
        for bar, m, e in zip(bars, means, cis):
            ax.annotate(
                f'{m:.2f} ms',
                xy=(bar.get_x() + bar.get_width() / 2, m + e),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontsize=9.5, fontweight='bold'
            )

    ax.set_ylim(0, max_top * 1.22 if max_top > 0 else 150)
    ax.set_title('Figura 1: Latência Inicial de Handshake (Cold TTFB) com IC de 95%', fontweight='bold')
    ax.set_ylabel('TTFB Médio (milissegundos)')
    ax.set_xlabel('Cenário de Canal Emulado')
    ax.set_xticks(x)
    ax.set_xticklabels(['Cenário 1: LAN\n(RTT 1ms, 0% Perda)', 'Cenário 2: WAN\n(RTT 50ms, 2% Perda)'])
    ax.legend(title='Protocolo Web', loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.6)

    out_path = os.path.join(output_dir, 'fig1_ttfb_cold_comparison.png')
    plt.savefig(out_path)
    plt.close()
    print(f"[+] Gráfico 1 gerado: {out_path}")


def plot_fig2_throughput(data: List[Dict[str, Any]], output_dir: str):
    """Gráfico 2: Vazão Sustentada (Goodput Mbps) na Carga A (50 MB) com Barras de Erro (Desvio Padrão)."""
    fig, ax = plt.subplots(figsize=(8.5, 5.2))

    rows_a = [r for r in data if 'Carga A' in r['payload_type']]
    scenarios = ['LAN (1ms, 0% loss)', 'WAN (50ms, 2% loss)']
    protocols = ['HTTP/1.1', 'HTTPS/TLS1.3', 'HTTP/3-QUIC']

    x = np.arange(len(scenarios))
    width = 0.25
    max_top = 0.0

    for i, proto in enumerate(protocols):
        means = []
        stds = []
        for sc in scenarios:
            sub = np.array([float(r['goodput_mbps']) for r in rows_a if r['scenario'] == sc and r['protocol'] == proto])
            if len(sub) > 0:
                mean = float(np.mean(sub))
                std = float(np.std(sub, ddof=1)) if len(sub) > 1 else 0.0
                std = min(std, mean * 0.95)
                means.append(mean)
                stds.append(std)
                max_top = max(max_top, mean + std)
            else:
                means.append(0.0)
                stds.append(0.0)

        bars = ax.bar(
            x + (i - 1) * width, means, width, yerr=stds, capsize=5,
            label=proto, color=PALETTE[proto], edgecolor='black', alpha=0.9,
            error_kw={'elinewidth': 1.5, 'ecolor': 'black'}
        )
        for bar, m, s in zip(bars, means, stds):
            ax.annotate(
                f'{m:.2f}',
                xy=(bar.get_x() + bar.get_width() / 2, m + s),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontsize=9.5, fontweight='bold'
            )

    ax.set_ylim(0, max_top * 1.18 if max_top > 0 else 400)
    ax.set_title('Figura 2: Vazão Sustentada (Goodput) na Carga de 50 MB com Desvio Padrão', fontweight='bold')
    ax.set_ylabel('Vazão Útil Média (Mbps)')
    ax.set_xlabel('Cenário de Rede Emulado')
    ax.set_xticks(x)
    ax.set_xticklabels(['Cenário 1: LAN\n(RTT 1ms, 0% Perda)', 'Cenário 2: WAN\n(RTT 50ms, 2% Perda)'])
    ax.legend(title='Protocolo Web', loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.6)

    out_path = os.path.join(output_dir, 'fig2_throughput_carga_a.png')
    plt.savefig(out_path)
    plt.close()
    print(f"[+] Gráfico 2 gerado: {out_path}")


def plot_fig3_load_time_b(data: List[Dict[str, Any]], output_dir: str):
    """Gráfico 3: Tempo Total de Carregamento dos 100 Objetos (Carga B) com Barras de Erro (IC 95%)."""
    fig, ax = plt.subplots(figsize=(8.5, 5.2))

    rows_b = [r for r in data if 'Carga B' in r['payload_type']]
    scenarios = ['LAN (1ms, 0% loss)', 'WAN (50ms, 2% loss)']
    protocols = ['HTTP/1.1', 'HTTPS/TLS1.3', 'HTTP/3-QUIC']

    x = np.arange(len(scenarios))
    width = 0.25
    max_top = 0.0

    for i, proto in enumerate(protocols):
        means = []
        cis = []
        for sc in scenarios:
            sub = [r for r in rows_b if r['scenario'] == sc and r['protocol'] == proto]
            it_map = defaultdict(list)
            for r in sub:
                it_map[int(r['iteration'])].append(float(r['load_time_ms']))
            it_times = np.array([max(vals) for vals in it_map.values()])
            if len(it_times) > 0:
                mean = float(np.mean(it_times))
                err = min(calc_ci95_margin(it_times), mean * 0.95)
                means.append(mean)
                cis.append(err)
                max_top = max(max_top, mean + err)
            else:
                means.append(0.0)
                cis.append(0.0)

        bars = ax.bar(
            x + (i - 1) * width, means, width, yerr=cis, capsize=5,
            label=proto, color=PALETTE[proto], edgecolor='black', alpha=0.9,
            error_kw={'elinewidth': 1.5, 'ecolor': 'black'}
        )
        for bar, m, e in zip(bars, means, cis):
            ax.annotate(
                f'{m / 1000.0:.2f} s',
                xy=(bar.get_x() + bar.get_width() / 2, m + e),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontsize=9.5, fontweight='bold'
            )

    ax.set_ylim(0, max_top * 1.18 if max_top > 0 else 6000)
    ax.set_title('Figura 3: Tempo Total de Carregamento da Carga B (100 Objetos) com IC 95%', fontweight='bold')
    ax.set_ylabel('Duração Total Média (milissegundos)')
    ax.set_xlabel('Cenário de Canal Emulado')
    ax.set_xticks(x)
    ax.set_xticklabels(['Cenário 1: LAN\n(RTT 1ms, 0% Perda)', 'Cenário 2: WAN\n(RTT 50ms, 2% Perda)'])
    ax.legend(title='Protocolo Web', loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.6)

    out_path = os.path.join(output_dir, 'fig3_load_time_carga_b.png')
    plt.savefig(out_path)
    plt.close()
    print(f"[+] Gráfico 3 gerado: {out_path}")


def plot_fig4_rps_wan(data: List[Dict[str, Any]], output_dir: str):
    """Gráfico 4: Requisições por Segundo (RPS) na Carga B sob Perdas (T10 vs T11 vs T12) com Barras de Erro."""
    fig, ax = plt.subplots(figsize=(7.5, 5.2))

    rows_b_wan = [r for r in data if 'Carga B' in r['payload_type'] and 'WAN' in r['scenario']]
    protocols = ['HTTP/1.1', 'HTTPS/TLS1.3', 'HTTP/3-QUIC']

    means = []
    stds = []
    max_top = 0.0

    for proto in protocols:
        sub = [r for r in rows_b_wan if r['protocol'] == proto]
        it_map = defaultdict(list)
        for r in sub:
            it_map[int(r['iteration'])].append(float(r['load_time_ms']))
        rps_list = []
        for vals in it_map.values():
            max_dur_s = max(vals) / 1000.0
            if max_dur_s > 0:
                rps_list.append(len(vals) / max_dur_s)
        if rps_list:
            m = float(np.mean(rps_list))
            s = float(np.std(rps_list, ddof=1)) if len(rps_list) > 1 else 0.0
            means.append(m)
            stds.append(s)
            max_top = max(max_top, m + s)
        else:
            means.append(0.0)
            stds.append(0.0)

    bars = ax.bar(
        protocols, means, yerr=stds, capsize=6,
        color=[PALETTE[p] for p in protocols], edgecolor='black', alpha=0.9, width=0.48,
        error_kw={'elinewidth': 1.6, 'ecolor': 'black'}
    )

    for bar, m, s in zip(bars, means, stds):
        ax.annotate(
            f'{m:.1f} req/s',
            xy=(bar.get_x() + bar.get_width() / 2, m + s),
            xytext=(0, 6), textcoords="offset points",
            ha='center', va='bottom', fontweight='bold', fontsize=10.5
        )

    ax.set_ylim(0, max_top * 1.20 if max_top > 0 else 110)
    ax.set_title('Figura 4: Throughput Concorrente (RPS) na WAN sob 2% de Perda (T10, T11, T12)', fontweight='bold')
    ax.set_ylabel('Requisições Concluídas por Segundo (RPS)')
    ax.set_xlabel('Protocolo sob Degradação de Rede')
    ax.grid(True, linestyle='--', alpha=0.6)

    out_path = os.path.join(output_dir, 'fig4_rps_carga_b_wan.png')
    plt.savefig(out_path)
    plt.close()
    print(f"[+] Gráfico 4 gerado: {out_path}")


def plot_fig5_cdf(data: List[Dict[str, Any]], output_dir: str):
    """Gráfico 5: Curva CDF de Latência dos Objetos sob Perda de 2% com Barras de Erro (IC 95%)."""
    fig, ax = plt.subplots(figsize=(8.5, 5.2))

    rows_b_wan = [r for r in data if 'Carga B' in r['payload_type'] and 'WAN' in r['scenario']]
    protocols = ['HTTP/1.1', 'HTTPS/TLS1.3', 'HTTP/3-QUIC']

    y_grid = np.linspace(0.01, 1.0, 100)
    eb_indices = [19, 49, 74, 89, 98]  # Percentis: p20, p50, p75, p90, p99

    for proto in protocols:
        sub = [r for r in rows_b_wan if r['protocol'] == proto]
        it_map = defaultdict(list)
        for r in sub:
            it_map[int(r['iteration'])].append(float(r['ttfb_ms']))

        it_curves = []
        for it in sorted(it_map.keys()):
            vals = np.sort(np.array(it_map[it], dtype=float))
            if len(vals) == 100:
                it_curves.append(vals)
            elif len(vals) > 0:
                it_curves.append(np.quantile(vals, y_grid))

        if it_curves:
            mat = np.vstack(it_curves)  # shape: (n_iterations, 100)
            mean_curve = np.mean(mat, axis=0)
            ci_margins = np.array([calc_ci95_margin(mat[:, j]) for j in range(mat.shape[1])])

            ax.plot(mean_curve, y_grid, label=f"{proto} (Média ± IC 95%)", color=PALETTE[proto], linewidth=2.3)
            ax.fill_betweenx(
                y_grid,
                np.maximum(0, mean_curve - ci_margins),
                mean_curve + ci_margins,
                color=PALETTE[proto],
                alpha=0.18
            )
            # Barras de erro explícitas nos quantis p20, p50, p75, p90 e p99
            ax.errorbar(
                mean_curve[eb_indices],
                y_grid[eb_indices],
                xerr=ci_margins[eb_indices],
                fmt='o',
                color=PALETTE[proto],
                ecolor='black',
                elinewidth=1.3,
                capsize=4,
                markersize=4.5
            )

    ax.set_xlim(left=0)
    ax.set_ylim(0, 1.05)
    ax.set_title('Figura 5: Curva CDF de Latência na WAN com Barras de Erro (IC 95%)', fontweight='bold')
    ax.set_xlabel('Latência de Resposta por Objeto (milissegundos)')
    ax.set_ylabel(r'Probabilidade Cumulativa $P(X \leq x)$')
    ax.legend(title='Protocolo Web', loc='lower right')
    ax.grid(True, linestyle='--', alpha=0.6)

    out_path = os.path.join(output_dir, 'fig5_cdf_latency_distribution.png')
    plt.savefig(out_path)
    plt.close()
    print(f"[+] Gráfico 5 gerado: {out_path}")


def generate_all_plots():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_csv = os.path.join(base_dir, 'data', 'raw', 'results.csv')
    raw_json = os.path.join(base_dir, 'data', 'raw', 'results.json')
    plots_dir = os.path.join(base_dir, 'data', 'plots')
    os.makedirs(plots_dir, exist_ok=True)

    print("[*] Carregando dados para plotagem científica...")
    data = load_data(raw_csv, raw_json)
    print(f"[*] Base de dados carregada com {len(data)} amostras.")

    plot_fig1_ttfb(data, plots_dir)
    plot_fig2_throughput(data, plots_dir)
    plot_fig3_load_time_b(data, plots_dir)
    plot_fig4_rps_wan(data, plots_dir)
    plot_fig5_cdf(data, plots_dir)
    print("[OK] Todos os 5 gráficos científicos gerados com barras de erro obrigatórias em data/plots/!")


if __name__ == '__main__':
    generate_all_plots()
