#!/usr/bin/env python3
"""
generate_plots.py - Pipeline de Analise Estatistica e Geracao de Figuras Cientificas
Gera graficos com padrao de publicacao (SBC/IEEE) e tabelas consolidadas em LaTeX.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Configuracao global de estetica cientifica para publicacao SBC
plt.rcParams.update({
    'font.size': 11,
    'font.family': 'serif',
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 14,
    'grid.linestyle': '--',
    'grid.alpha': 0.6,
})

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_RAW = os.path.join(BASE_DIR, "data", "raw")
PLOTS_DIR = os.path.join(BASE_DIR, "artigo", "figuras")
TABLES_DIR = os.path.join(BASE_DIR, "artigo")
os.makedirs(PLOTS_DIR, exist_ok=True)

def calc_ci95(series):
    """Calcula margem de erro do Intervalo de Confianca de 95%"""
    n = len(series)
    if n <= 1:
        return 0.0
    se = stats.sem(series)
    h = se * stats.t.ppf((1 + 0.95) / 2., n - 1)
    return h

def plot_scenario_a():
    csv_path = os.path.join(DATA_RAW, "scenario_a_results.csv")
    if not os.path.exists(csv_path):
        print(f"[!] Arquivo nao encontrado: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    # Agrupar por taxa
    grouped = df.groupby('target_rate_mbps').agg(
        goodput_mean=('goodput_mbps', 'mean'),
        goodput_std=('goodput_mbps', 'std'),
        jitter_mean=('jitter_ms', 'mean'),
        jitter_std=('jitter_ms', 'std'),
        loss_mean=('loss_percent', 'mean')
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(7, 4.5))

    rates = grouped['target_rate_mbps']
    ax1.plot(rates, grouped['goodput_mean'], marker='o', color='#1f77b4', linewidth=2, label='Goodput Efetivo (Mbps)')
    ax1.plot(rates, rates, '--', color='#7f7f7f', alpha=0.7, label='Taxa Alvo Ideal (Sem Perda)')
    ax1.set_xlabel('Taxa Alvo Injetada (Mbps)')
    ax1.set_ylabel('Goodput Efetivo (Mbps)', color='#1f77b4')
    ax1.tick_params(axis='y', labelcolor='#1f77b4')
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.plot(rates, grouped['jitter_mean'], marker='s', color='#d62728', linestyle=':', linewidth=2, label='Jitter (ms)')
    ax2.set_ylabel('Jitter Médio (ms)', color='#d62728')
    ax2.tick_params(axis='y', labelcolor='#d62728')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.title('Cenário A: Desempenho do UDP Puro sob Taxas Crescentes')
    plt.tight_layout()
    out_file = os.path.join(PLOTS_DIR, "cenario_a_udp_performance.pdf")
    plt.savefig(out_file)
    plt.savefig(out_file.replace('.pdf', '.png'), dpi=300)
    plt.close()
    print(f"[+] Gráfico Cenário A gerado: {out_file}")

def plot_scenario_b():
    csv_path = os.path.join(DATA_RAW, "scenario_b_results.csv")
    if not os.path.exists(csv_path):
        print(f"[!] Arquivo nao encontrado: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    grouped = df.groupby(['file_size_label', 'protocol']).agg(
        fct_mean=('total_time_sec', 'mean'),
        fct_std=('total_time_sec', 'std'),
        goodput_mean=('goodput_mbps', 'mean'),
        goodput_std=('goodput_mbps', 'std')
    ).reset_index()

    # Mapear rotulos amigaveis
    proto_map = {'http1.1': 'HTTP/1.1 (TCP)', 'http2': 'HTTP/2 (TCP)', 'http3': 'HTTP/3 (QUIC)'}
    grouped['proto_label'] = grouped['protocol'].map(proto_map)

    # Grafico de FCT
    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(grouped['file_size_label'].unique()))
    width = 0.25

    protos = ['http1.1', 'http2', 'http3']
    colors = ['#2ca02c', '#1f77b4', '#ff7f0e']

    for i, proto in enumerate(protos):
        sub = grouped[grouped['protocol'] == proto]
        pos = x + (i - 1) * width
        ax.bar(pos, sub['fct_mean'], width, yerr=sub['fct_std'], capsize=5, label=proto_map[proto], color=colors[i], alpha=0.9)

    ax.set_ylabel('Flow Completion Time Médio (segundos)')
    ax.set_title('Cenário B: FCT para Ficheiros Massivos (100 MB e 1 GB)')
    ax.set_xticks(x)
    ax.set_xticklabels(grouped['file_size_label'].unique())
    ax.legend()
    ax.grid(True, axis='y')

    plt.tight_layout()
    out_file = os.path.join(PLOTS_DIR, "cenario_b_fct_comparison.pdf")
    plt.savefig(out_file)
    plt.savefig(out_file.replace('.pdf', '.png'), dpi=300)
    plt.close()
    print(f"[+] Gráfico Cenário B gerado: {out_file}")

def plot_scenario_c():
    csv_path = os.path.join(DATA_RAW, "scenario_c_results.csv")
    if not os.path.exists(csv_path):
        print(f"[!] Arquivo nao encontrado: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    grouped = df.groupby(['loss_percent', 'protocol']).agg(
        fct_mean=('total_batch_fct_sec', 'mean'),
        fct_std=('total_batch_fct_sec', 'std'),
        goodput_mean=('goodput_mbps', 'mean'),
        goodput_std=('goodput_mbps', 'std')
    ).reset_index()

    proto_map = {'http1.1': 'HTTP/1.1 (TCP)', 'http2': 'HTTP/2 (TCP)', 'http3': 'HTTP/3 (QUIC)'}

    fig, ax = plt.subplots(figsize=(8, 4.5))
    losses = [0, 2, 5]
    colors = {'http1.1': '#2ca02c', 'http2': '#1f77b4', 'http3': '#d62728'}
    markers = {'http1.1': '^', 'http2': 's', 'http3': 'o'}

    for proto in ['http1.1', 'http2', 'http3']:
        sub = grouped[grouped['protocol'] == proto]
        ax.errorbar(sub['loss_percent'], sub['fct_mean'], yerr=sub['fct_std'],
                    marker=markers[proto], color=colors[proto], linewidth=2, capsize=5,
                    label=proto_map[proto])

    ax.set_xlabel('Taxa de Perda Aleatória de Pacotes (%)')
    ax.set_ylabel('FCT Total do Lote (100 Objetos) [s]')
    ax.set_title('Cenário C: Impacto do Head-of-Line Blocking sob Perdas no Canal')
    ax.set_xticks(losses)
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    out_file = os.path.join(PLOTS_DIR, "cenario_c_hol_blocking.pdf")
    plt.savefig(out_file)
    plt.savefig(out_file.replace('.pdf', '.png'), dpi=300)
    plt.close()
    print(f"[+] Gráfico Cenário C gerado: {out_file}")

def generate_latex_tables():
    """Gera tabelas consolidadas em formato LaTeX para inclusao no sbc-template.tex"""
    tex_path = os.path.join(TABLES_DIR, "tabelas_consolidadas.tex")
    
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write("% Tabelas consolidadas geradas automaticamente pelo pipeline de dados\n\n")
        f.write("% ==========================================\n")
        f.write("% Tabela 1: Sobrecarga Teórica e Prática de Cabeçalhos\n")
        f.write("% ==========================================\n")
        f.write("\\begin{table}[ht]\n\\centering\n\\small\n")
        f.write("\\caption{Comparativo Estrutural de Sobrecarga (Overhead) dos Protocolos de Transporte}\n")
        f.write("\\label{tab:overhead_comparativo}\n")
        f.write("\\begin{tabular}{lcccc}\n\\hline\n")
        f.write("\\textbf{Protocolo} & \\textbf{Camada} & \\textbf{Tamanho Cabeçalho} & \\textbf{Handshake Inicial} & \\textbf{Criptografia} \\\\ \\hline\n")
        f.write("UDP Puro & Transporte & 8 bytes & 0 RTT (Sem estado) & Ausente \\\\\n")
        f.write("TCP Tradicional & Transporte & 20 a 60 bytes & 1 RTT (3-way) & Opcional (TLS externo) \\\\\n")
        f.write("TCP + TLS 1.3 & Transporte + Seg. & 20B + Record TLS & 2 RTT (1 TCP + 1 TLS) & Obrigatório \\\\\n")
        f.write("QUIC (HTTP/3) & Aplicação/Transp. & Variável (10 a 25B) & 1 RTT (Unificado TLS 1.3) & Nativa (TLS 1.3) \\\\ \\hline\n")
        f.write("\\end{tabular}\n\\end{table}\n\n")

    print(f"[+] Tabelas LaTeX consolidadas geradas em: {tex_path}")

def main():
    print("[*] Iniciando geração de figuras científicas e tabelas...")
    plot_scenario_a()
    plot_scenario_b()
    plot_scenario_c()
    generate_latex_tables()
    print("[*] Pipeline concluído com sucesso!")

if __name__ == "__main__":
    main()
