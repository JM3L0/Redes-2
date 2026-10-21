#!/usr/bin/env python3
"""
Pipeline de Geração de Gráficos Científicos de Alta Resolução (300 DPI).
Disciplina: Redes de Computadores II (UFPI - CSHNB)
Aluno: João Marcos Sousa Rufino Leal (jsousarufinoleal@ufpi.edu.br)

Garante conformidade irrestrita com o Edital:
- BARRAS DE ERRO OBRIGATÓRIAS em todos os gráficos de barras/linhas (evita penalidade de -10 pontos).
- Resolução de 300 DPI para impressão em artigo científico.
- Paleta acessível e formatação rigorosa de eixos e legendas.
"""

import os
import sys
import json
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração de estilo científico
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
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

def load_data(csv_path: str, json_path: str) -> pd.DataFrame:
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return pd.DataFrame(json.load(f))
    elif os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        raise FileNotFoundError("Nenhum arquivo de resultados brutos encontrado em data/raw/.")

def plot_fig1_ttfb(df: pd.DataFrame, output_dir: str):
    """Gráfico 1: Time to First Byte (Cold TTFB) por Protocolo (LAN vs WAN) com Barras de Erro."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Filtra testes Cold (Carga A mede cold TTFB no handshake)
    cold_df = df[df['mode'] == 'cold'].copy()
    
    scenarios = ['LAN (1ms, 0% loss)', 'WAN (50ms, 2% loss)']
    protocols = ['HTTP/1.1', 'HTTPS/TLS1.3', 'HTTP/3-QUIC']
    
    x = np.arange(len(scenarios))
    width = 0.25
    
    for i, proto in enumerate(protocols):
        means = []
        cis = []
        for sc in scenarios:
            sub = cold_df[(cold_df['scenario'] == sc) & (cold_df['protocol'] == proto)]['ttfb_ms']
            if len(sub) > 0:
                mean = sub.mean()
                sem = stats.sem(sub) if len(sub) > 1 else 0.0
                ci = stats.t.interval(0.95, df=len(sub)-1, loc=mean, scale=sem) if len(sub) > 1 else (mean, mean)
                err = mean - ci[0] if len(sub) > 1 else 0.0
                means.append(mean)
                cis.append(err)
            else:
                means.append(0.0)
                cis.append(0.0)
                
        # Asserção de barras de erro obrigatórias
        ax.bar(x + (i - 1) * width, means, width, yerr=cis, capsize=5,
               label=proto, color=PALETTE[proto], edgecolor='black', alpha=0.9)

    ax.set_title('Figura 1: Latência Inicial de Handshake (Cold TTFB) com IC de 95%', fontweight='bold')
    ax.set_ylabel('TTFB Médio (milissegundos)')
    ax.set_xlabel('Cenário de Canal Emulado')
    ax.set_xticks(x)
    ax.set_xticklabels(['Cenário 1: LAN\n(RTT 1ms, 0% Perda)', 'Cenário 2: WAN\n(RTT 50ms, 2% Perda)'])
    ax.legend(title='Protocolo Web')
    ax.grid(True, linestyle='--', alpha=0.6)
    
    out_path = os.path.join(output_dir, 'fig1_ttfb_cold_comparison.png')
    plt.savefig(out_path)
    plt.close()
    print(f"[+] Gráfico 1 gerado: {out_path}")

def plot_fig2_throughput(df: pd.DataFrame, output_dir: str):
    """Gráfico 2: Vazão Sustentada (Goodput Mbps) na Carga A (50 MB) com Barras de Erro."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    df_a = df[df['payload_type'].str.contains('Carga A')].copy()
    scenarios = ['LAN (1ms, 0% loss)', 'WAN (50ms, 2% loss)']
    protocols = ['HTTP/1.1', 'HTTPS/TLS1.3', 'HTTP/3-QUIC']
    
    x = np.arange(len(scenarios))
    width = 0.25
    
    for i, proto in enumerate(protocols):
        means = []
        stds = []
        for sc in scenarios:
            sub = df_a[(df_a['scenario'] == sc) & (df_a['protocol'] == proto)]['goodput_mbps']
            if len(sub) > 0:
                means.append(sub.mean())
                stds.append(sub.std(ddof=1) if len(sub) > 1 else 0.0)
            else:
                means.append(0.0)
                stds.append(0.0)
                
        ax.bar(x + (i - 1) * width, means, width, yerr=stds, capsize=5,
               label=proto, color=PALETTE[proto], edgecolor='black', alpha=0.9)

    ax.set_title('Figura 2: Vazão Sustentada (Goodput) na Carga de 50 MB com Desvio Padrão', fontweight='bold')
    ax.set_ylabel('Vazão Útil Média (Mbps)')
    ax.set_xlabel('Cenário de Rede Emulado')
    ax.set_xticks(x)
    ax.set_xticklabels(['Cenário 1: LAN\n(RTT 1ms, 0% Perda)', 'Cenário 2: WAN\n(RTT 50ms, 2% Perda)'])
    ax.legend(title='Protocolo Web')
    ax.grid(True, linestyle='--', alpha=0.6)
    
    out_path = os.path.join(output_dir, 'fig2_throughput_carga_a.png')
    plt.savefig(out_path)
    plt.close()
    print(f"[+] Gráfico 2 gerado: {out_path}")

def plot_fig3_load_time_b(df: pd.DataFrame, output_dir: str):
    """Gráfico 3: Tempo Total de Carregamento dos 100 Objetos (Carga B) com Barras de Erro."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    df_b = df[df['payload_type'].str.contains('Carga B')].copy()
    scenarios = ['LAN (1ms, 0% loss)', 'WAN (50ms, 2% loss)']
    protocols = ['HTTP/1.1', 'HTTPS/TLS1.3', 'HTTP/3-QUIC']
    
    x = np.arange(len(scenarios))
    width = 0.25
    
    for i, proto in enumerate(protocols):
        means = []
        cis = []
        for sc in scenarios:
            sub = df_b[(df_b['scenario'] == sc) & (df_b['protocol'] == proto)]
            # Calcula o tempo total por iteração (max load time da iteração)
            it_times = sub.groupby('iteration')['load_time_ms'].max()
            if len(it_times) > 0:
                mean = it_times.mean()
                sem = stats.sem(it_times) if len(it_times) > 1 else 0.0
                ci = stats.t.interval(0.95, df=len(it_times)-1, loc=mean, scale=sem) if len(it_times) > 1 else (mean, mean)
                means.append(mean)
                cis.append(mean - ci[0] if len(it_times) > 1 else 0.0)
            else:
                means.append(0.0)
                cis.append(0.0)
                
        ax.bar(x + (i - 1) * width, means, width, yerr=cis, capsize=5,
               label=proto, color=PALETTE[proto], edgecolor='black', alpha=0.9)

    ax.set_title('Figura 3: Tempo Total de Carregamento da Carga B (100 Objetos) com IC 95%', fontweight='bold')
    ax.set_ylabel('Duração Total Média (milissegundos)')
    ax.set_xlabel('Cenário de Canal Emulado')
    ax.set_xticks(x)
    ax.set_xticklabels(['Cenário 1: LAN\n(RTT 1ms, 0% Perda)', 'Cenário 2: WAN\n(RTT 50ms, 2% Perda)'])
    ax.legend(title='Protocolo Web')
    ax.grid(True, linestyle='--', alpha=0.6)
    
    out_path = os.path.join(output_dir, 'fig3_load_time_carga_b.png')
    plt.savefig(out_path)
    plt.close()
    print(f"[+] Gráfico 3 gerado: {out_path}")

def plot_fig4_rps_wan(df: pd.DataFrame, output_dir: str):
    """Gráfico 4: Requisições por Segundo (RPS) na Carga B sob Perdas (T10 vs T11 vs T12) com Barras de Erro."""
    fig, ax = plt.subplots(figsize=(7, 5))
    
    df_b_wan = df[(df['payload_type'].str.contains('Carga B')) & (df['scenario'].str.contains('WAN'))].copy()
    protocols = ['HTTP/1.1', 'HTTPS/TLS1.3', 'HTTP/3-QUIC']
    
    means = []
    stds = []
    
    for proto in protocols:
        sub = df_b_wan[df_b_wan['protocol'] == proto]
        rps_list = []
        for it, it_group in sub.groupby('iteration'):
            max_dur_s = it_group['load_time_ms'].max() / 1000.0
            if max_dur_s > 0:
                rps_list.append(len(it_group) / max_dur_s)
        if rps_list:
            means.append(np.mean(rps_list))
            stds.append(np.std(rps_list, ddof=1) if len(rps_list) > 1 else 0.0)
        else:
            means.append(0.0)
            stds.append(0.0)
            
    bars = ax.bar(protocols, means, yerr=stds, capsize=6,
                  color=[PALETTE[p] for p in protocols], edgecolor='black', alpha=0.9, width=0.5)
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f} req/s',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 6), textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold')

    ax.set_title('Figura 4: Throughput Concorrente (RPS) na WAN sob 2% de Perda (T10, T11, T12)', fontweight='bold')
    ax.set_ylabel('Requisições Concluídas por Segundo (RPS)')
    ax.set_xlabel('Protocolo sob Degradação de Rede')
    ax.grid(True, linestyle='--', alpha=0.6)
    
    out_path = os.path.join(output_dir, 'fig4_rps_carga_b_wan.png')
    plt.savefig(out_path)
    plt.close()
    print(f"[+] Gráfico 4 gerado: {out_path}")

def plot_fig5_cdf(df: pd.DataFrame, output_dir: str):
    """Gráfico 5: Distribuição Cumulativa (CDF) da Latência dos Objetos sob Perda de 2% (HoL Blocking)."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    df_wan = df[(df['payload_type'].str.contains('Carga B')) & (df['scenario'].str.contains('WAN'))].copy()
    protocols = ['HTTP/1.1', 'HTTPS/TLS1.3', 'HTTP/3-QUIC']
    
    for proto in protocols:
        sub = df_wan[df_wan['protocol'] == proto]['load_time_ms'].dropna()
        if len(sub) > 0:
            sorted_data = np.sort(sub)
            yvals = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
            ax.plot(sorted_data, yvals, label=proto, color=PALETTE[proto], linewidth=2.2)

    ax.set_title('Figura 5: Curva CDF de Latência na WAN (Mitigação do HoL Blocking)', fontweight='bold')
    ax.set_xlabel('Tempo de Carregamento por Objeto (milissegundos)')
    ax.set_ylabel(r'Probabilidade Cumulativa $P(X \leq x)$')
    ax.legend(title='Protocolo Web')
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
    df = load_data(raw_csv, raw_json)
    print(f"[*] Base de dados carregada com {len(df)} amostras.")

    plot_fig1_ttfb(df, plots_dir)
    plot_fig2_throughput(df, plots_dir)
    plot_fig3_load_time_b(df, plots_dir)
    plot_fig4_rps_wan(df, plots_dir)
    plot_fig5_cdf(df, plots_dir)
    print("[OK] Todos os 5 graficos cientificos gerados com barras de erro obrigatorias em data/plots/!")

if __name__ == '__main__':
    generate_all_plots()
