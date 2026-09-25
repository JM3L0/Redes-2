# 📘 Fase 1: Análise do Edital e Estruturação do Cérebro

**Status:**  CONCLUÍDA  
**Data:** 25/09/2026  
**Responsável:** João Marcos Sousa Rufino Leal  

---

## 1. Objetivos da Fase
Compreender exaustivamente todos os requisitos técnicos, científicos e regras do edital da **1ª Avaliação Prática de Redes de Computadores II (UFPI - 2026-2)** e construir uma base de conhecimento persistente (**Cérebro / Brain**) para guiar o desenvolvimento do projeto.

---

## 2. O que foi Feito

### 2.1. Análise Crítica do Edital (`1_Avaliacao - Redes 2.pdf`)
* Identificação do objetivo central: comparação empírica de desempenho e sobrecarga entre **TCP** (HTTP/1.1 e HTTP/2), **UDP Puro** e **QUIC** (HTTP/3 sobre UDP) utilizando NGINX e Linux.
* Levantamento de todas as métricas obrigatórias: *Flow Completion Time* (FCT), *Goodput* efetivo, *Overhead* de cabeçalho e resiliência a perdas.
* Mapeamento da regra eliminatória severa (**Nota 0,0**):
  1. Ausência do artigo no formato SBC/SBRC;
  2. Ausência ou inoperância do link público para o vídeo de 15 minutos na **1ª página do artigo**.

### 2.2. Criação da Arquitetura do Cérebro (`brain/`)
Foi construída uma estrutura modular de documentação técnica dividida em 5 pilares originais:
1. `01_diretrizes/`: Escopo, regras críticas e checklist de acompanhamento kanban.
2. `02_arquitetura/`: Topologia em Docker, requisitos de contêineres e configurações de rede.
3. `03_experimentos/`: Especificação detalhada dos Cenários A, B e C, métricas e rigor estatístico ($N=10$).
4. `04_entregaveis/`: Estrutura do artigo SBC, RFCs mandatórias (793, 768, 9000, 9001, 8446) e roteiro cronometrado para o vídeo de 15 minutos.
5. `05_prompts_ia/`: Biblioteca de prompts especializados para automação com inteligências artificiais.

---

## 3. Artefatos Produzidos
* [**`brain/README.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/README.md)
* [**`brain/01_diretrizes/visao_geral_e_regras.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/01_diretrizes/visao_geral_e_regras.md)
* [**`brain/01_diretrizes/checklist_progresso.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/01_diretrizes/checklist_progresso.md)
* [**`brain/02_arquitetura/arquitetura_e_docker.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/02_arquitetura/arquitetura_e_docker.md)
* [**`brain/03_experimentos/cenarios_de_teste.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/03_experimentos/cenarios_de_teste.md)
* [**`brain/03_experimentos/metricas_e_analise_dados.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/03_experimentos/metricas_e_analise_dados.md)
* [**`brain/04_entregaveis/artigo_sbc_sbrc.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/04_entregaveis/artigo_sbc_sbrc.md)
* [**`brain/04_entregaveis/roteiro_video_15min.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/04_entregaveis/roteiro_video_15min.md)
* [**`brain/05_prompts_ia/guia_de_prompts_ia.md`**](file:///c:/Users/jsous/Desktop/Redes%202/Avaliacao_1/brain/05_prompts_ia/guia_de_prompts_ia.md)
