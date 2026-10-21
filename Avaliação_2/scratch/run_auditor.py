import os
import subprocess
import glob

base_dir = r"c:\Users\jsous\Desktop\Redes 2\Avaliação_2"

# 1. Read PDF extracted text
pdf_text_path = os.path.join(base_dir, "pdf_extracted_text.txt")
with open(pdf_text_path, "r", encoding="utf-8") as f:
    pdf_text = f.read()

# 2. Collect all created files
files_to_check = [
    "AGENTS.md",
    "README.md",
    os.path.join("brain", "README.md"),
    os.path.join("brain", "01_diretrizes", "visao_geral_e_regras.md"),
    os.path.join("brain", "01_diretrizes", "checklist_progresso.md"),
    os.path.join("brain", "02_arquitetura", "arquitetura_e_docker.md"),
    os.path.join("brain", "03_experimentos", "cenarios_de_teste.md"),
    os.path.join("brain", "03_experimentos", "metricas_e_analise_dados.md"),
    os.path.join("brain", "04_entregaveis", "relatorio_tecnico_academico.md"),
    os.path.join("brain", "04_entregaveis", "roteiro_video_15min.md"),
    os.path.join("brain", "05_prompts_ia", "guia_de_prompts_ia.md"),
    os.path.join("brain", "06_relatorios_de_fases", "README.md"),
    os.path.join("brain", "06_relatorios_de_fases", "fase_01_analise_e_estruturacao.md"),
]

files_content = {}
for rel_path in files_to_check:
    full_path = os.path.join(base_dir, rel_path)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            files_content[rel_path] = f.read()
    else:
        files_content[rel_path] = "ARQUIVO NÃO ENCONTRADO!"

# 3. Construct the Auditor Agent Prompt
prompt = f"""# PAPEL: Agente Auditor Independente de Qualidade e Conformidade Técnica e Acadêmica

Você foi convocado como um SEGUNDO AGENTE INDEPENDENTE para auditar e verificar minuciosamente o "Cérebro do Projeto" montado para a:
**2ª Avaliação Prática de Redes de Computadores II (UFPI - 2026-2)**
**Estudo Experimental de Desempenho de Protocolos Web (HTTP/1.1 vs HTTPS/TLS vs HTTP/3-QUIC) em Ambiente Emulado com Docker e Python**

Aluno: João Marcos Sousa Rufino Leal
Repositório: c:\\Users\\jsous\\Desktop\\Redes 2\\Avaliação_2

---
## EDITAL OFICIAL DA AVALIAÇÃO (TEXTO EXTRAÍDO DO PDF):
{pdf_text}

---
## ARQUIVOS CRIADOS NO CÉREBRO DO PROJETO:
"""

for rel_path, content in files_content.items():
    prompt += f"\n\n==================== ARQUIVO: {rel_path} ====================\n{content}\n"

prompt += """

---
## INSTRUÇÕES PARA A AUDITORIA:
Como Agente Auditor, analise criteriosamente se TUDO o que foi exigido no edital foi coberto com exatidão e sem omissões nos arquivos do Cérebro. Verifique especificamente:

1. **Requisitos de Infraestrutura e Docker:**
   - 3 servidores declarados (server_http11 em Nginx 8080 HTTP/1.1, server_http2_tls em Nginx 8443 HTTPS/TLS 1.3, server_http3_quic em Caddy 9443 HTTP/3 QUIC)?
   - Rede bridge `net_bench` (172.20.0.0/16) e IPs estáticos (172.20.0.10, 172.20.0.20, 172.20.0.30)?
   - Diretiva obrigatória de permissão de kernel `cap_add: [NET_ADMIN]`?

2. **Emulação de Rede com `tc netem`:**
   - Cenário 1 (LAN: delay 0.5ms = RTT 1.0ms, perda 0%) e Cenário 2 (WAN: delay 25ms = RTT 50.0ms, perda 2%)?
   - Justificativa matemática do atraso unidirecional RTT/2?
   - Comandos sintáticos exatos para aplicar e limpar (`tc qdisc del dev eth0 root`)?

3. **Cliente de Benchmark em Python:**
   - Uso de `httpx` (HTTP/1.1 e HTTP/2) e `aioquic` com `asyncio` (HTTP/3)?
   - **Controle de Viés de Sessão (Client-Side Bias Control)**: desativação de cache, fechamento explícito de sessão (`client.close()`) para Cold TTFB, e canal persistente mantido para multiplexação (Carga B)?
   - Métricas com precisão de microssegundos: TTFB, Total Load Time, RPS, percentis p50 e p99?
   - Exportação para `results.json` e `results.csv`?

4. **Perfis de Carga e Matriz Experimental:**
   - Carga A (1 objeto grande de 50 MB) e Carga B (100 objetos pequenos de 10 KB)?
   - Matriz completa de 12 testes (T01 a T12) com protocolo alvo, servidor, cenário e foco analítico?
   - Rigor estatístico ($N \\ge 10$ repetições independentes com média, desvio padrão, p50, p99 e IC 95%)?

5. **Entregáveis, Rubrica e Penalidades:**
   - Rubrica de 100 pontos detalhada (Eixo 1 Infra 25pts, Eixo 2 Client 25pts, Eixo 3 Coleta/Gráficos 20pts, Eixo 4 Relatório 30pts)?
   - Tabela de penalidades: -15pts sem runner 1-click, -10pts sem controle de viés no TTFB, -10pts sem barras de erro nos gráficos, -20pts relatório meramente descritivo sem Tanenbaum?
   - **Critério Eliminatório (NOTA ZERO)**: ausência de código, relatório ou vídeo de 15 minutos com link na página 1?
   - **Fundamentação teórica obrigatória com Tanenbaum**:
     - Tanenbaum §6.5.11 (TCP CUBIC): colapso de throughput no T04/T05 em canal WAN (função cúbica de janela e recuo multiplicativo sob 2% de perda estocástica)?
     - Tanenbaum §6.6.1 (QUIC) e §6.6.2 (BBR): isolamento de perdas por stream UDP e pacing de entrega imune a perdas pontuais no T06/T12?
   - **Exigência mandatória de BARRAS DE ERRO** em todos os gráficos?
   - Roteiro estruturado minuto a minuto (00:00 a 15:00) para o vídeo de apresentação?
   - Submissão via SIGAA no formato `TP2_Redes2_NomeAluno1_NomeAluno2.zip`?

---
## FORMATO DO SEU RELATÓRIO DE AUDITORIA:
Estruture sua resposta como um Relatório Oficial de Auditoria Técnica:
1. **Cabeçalho:** Identificação do Auditor, Data, Projeto Auditado e Escopo.
2. **Veredito Geral:** (APROVADO / APROVADO COM RESSALVAS / REPROVADO) com Pontuação de Conformidade (0 a 100%).
3. **Matriz de Conformidade por Requisito:** Tabela detalhada comparando cada exigência do edital com o que foi entregue nos arquivos do cérebro.
4. **Análise dos Pontos Fortes e Diferenciais de Engenharia:** O que foi além do básico.
5. **Checagem de Mitigação de Riscos de Penalidade:** Verificação específica das 4 penalidades (-15, -10, -10, -20) e do critério de Nota Zero.
6. **Recomendações e Diretrizes para as Próximas Fases.**
7. **Conclusão Formal do Auditor.**
"""

prompt_file = os.path.join(base_dir, "scratch", "compiled_audit_prompt.txt")
with open(prompt_file, "w", encoding="utf-8") as f:
    f.write(prompt)

print(f"Prompt compilado com sucesso ({len(prompt)} caracteres). Disparando o segundo agente auditor via agy...")

# Executa o agy CLI passando o prompt compilado via STDIN com auto-aprovação de permissões headless
result = subprocess.run(
    ["agy", "--dangerously-skip-permissions", "-p", "-"],
    input=prompt,
    capture_output=True,
    text=True,
    encoding="utf-8"
)

audit_report_path = os.path.join(base_dir, "brain", "01_diretrizes", "auditoria_cerebro.md")
with open(audit_report_path, "w", encoding="utf-8") as f:
    f.write(result.stdout)

print(f"Auditoria concluída com código de retorno: {result.returncode}")
print(f"Relatório de auditoria salvo em: {audit_report_path}")
if result.stderr:
    print(f"Avisos/Stderr: {result.stderr[:500]}")
