# 🧪 Guia Prático: Como Rodar o Projeto Ao Vivo no Vídeo (Bloco 4 — 3 Minutos)

**Disciplina:** Redes de Computadores II (UFPI — CSHNB)  
**Equipe:** João Marcos Sousa Rufino Leal & Marcos Willian de Sousa e Silva  

> [!IMPORTANT]
> **Por que este guia é essencial?**
> 1. **Tempo de vídeo:** Os testes `T04` e `T05` (download de 50 MB sob 2% de perda na WAN) levam **~85 segundos cada repetição** porque o TCP CUBIC colapsa para ~4,8 Mbps. Se você rodar 10 repetições ao vivo, só esses dois testes levariam **30 minutos**!
> 2. **Proteção dos dados oficiais ($N=10$):** O script `client.py` salva os resultados em `data/raw/results.csv` e `results.json`. Se você rodar com 1 ou 2 repetições no vídeo sem fazer backup antes, ele sobrescreverá os dados completos de 10 repetições do relatório.

Abaixo está o passo a passo exato (copiar e colar) do que fazer **antes**, **durante** e **depois** de gravar.

---

## 🛠️ PASSO 1: Preparação ANTES de Apertar "Gravar" no OBS (2 minutos antes)

Abra um terminal **PowerShell** na pasta `c:\Users\jsous\Desktop\Redes 2\Avaliação_2` e rode este bloco **antes de começar a gravação**:

```powershell
# 1. Garante que o Docker Desktop está aberto e faz pré-pull das imagens (para não baixar imagem ao vivo)
docker compose -f docker\docker-compose.yml up -d

# 2. Já deixa o pacote iproute2 (comando tc) instalado nos 3 contêineres Alpine
docker exec server_http11 apk add --no-cache iproute2
docker exec server_http2_tls apk add --no-cache iproute2
docker exec server_http3_quic apk add --no-cache iproute2

# 3. Faz BACKUP dos dados oficiais de N=10 repetições (para restaurar depois do vídeo)
Copy-Item -Path "data" -Destination "data_backup_n10" -Recurse -Force

# 4. Limpa a tela para começar o vídeo com o terminal limpo e bonito
Clear-Host
```

---

## 🎥 PASSO 2: O Que Executar AO VIVO no Vídeo (Bloco 4: 07:30 até 10:30)

Você tem **duas formas excelentes** de mostrar a execução ao vivo em **exatos 3 minutos**. Escolha a que preferirem (ou usem a **Opção A**, que mostra tanto o comando único quanto a comparação instantânea na WAN):

### ⭐ Opção Recomendada (Cabe em 2m30s e mostra TUDO ao vivo sem travar o vídeo)

Durante o **Bloco 4 [07:30 - 10:30]**, com o terminal aberto na tela, execute os **4 comandos abaixo em sequência**:

#### 1️⃣ Comando 1 (07:30 - 08:15) — Mostrar o Orquestrador Mestre 1-Click iniciando tudo e aplicando LAN (`1ms, 0%`)
Mostre o arquivo `run_experiments.ps1` / `run_experiments.sh` e rode o orquestrador ou o setup do cenário LAN:
```powershell
.\scripts\setup_netem.ps1 lan
```
* **O que aparece na tela:** Os 3 contêineres (`server_http11`, `server_http2_tls`, `server_http3_quic`) recebendo `tc qdisc add dev eth0 root netem delay 0.5ms` e o status `qdisc netem 8001: root refcnt 2 limit 1000 delay 500.0us`.

#### 2️⃣ Comando 2 (08:15 - 09:00) — Rodar ao vivo os testes de LAN (Carga A de 50 MB + Carga B de 100 objetos)
```powershell
python benchmark\client.py --test T01 --iterations 1 --http1-port 8080
python benchmark\client.py --test T02 --iterations 1 --http1-port 8080
python benchmark\client.py --test T09 --iterations 1 --http1-port 8080
```
* **Tempo na tela:** Leva apenas **~15 segundos no total**!
* **O que comentar:** *"Vejam ao vivo na LAN sem perdas: o HTTP/1.1 e o HTTP/2 baixam 50 MB em 1 a 2 segundos, e o HTTP/3 baixa os 100 objetos concorrentes em 0,6 segundo!"*

#### 3️⃣ Comando 3 (09:00 - 10:00) — Mudar ao vivo para o Cenário WAN (`50ms RTT, 2% loss`) e provar a vitória do HTTP/3
```powershell
.\scripts\setup_netem.ps1 wan
python benchmark\client.py --test T10 --iterations 1 --http1-port 8080
python benchmark\client.py --test T11 --iterations 1 --http1-port 8080
python benchmark\client.py --test T12 --iterations 1 --http1-port 8080
```
* **Tempo na tela:** Leva apenas **~12 segundos no total**!
* **Impacto visual imediato para o professor:**
  - `T10 (HTTP/1.1 na WAN)`: demora **~4,8 segundos** (~20 RPS)
  - `T11 (HTTP/2 na WAN)`: demora **~3,2 segundos** (~31 RPS) — travado pelo HoL Blocking do TCP!
  - `T12 (HTTP/3-QUIC na WAN)`: termina em **~1,1 segundo** (~87 RPS) na frente da câmera!

#### 4️⃣ Comando 4 (10:00 - 10:30) — Limpar o `tc netem` e rodar a consolidação estatística e geração dos gráficos
```powershell
.\scripts\setup_netem.ps1 clean
Copy-Item -Path "data_backup_n10\raw\*" -Destination "data\raw\" -Force
python analysis\process_data.py
python analysis\plot_results.py
```
* **O que aparece na tela:**
  - As interfaces `eth0` dos 3 servidores limpas (`qdisc noqueue`);
  - A tabela completa dos **12 testes (T01 a T12)** sendo impressa ao vivo no terminal com TTFB, Load Time, Goodput e RPS;
  - As **5 figuras científicas (300 DPI) com barras de erro** sendo geradas e salvas em `data/plots/`!

---

### 🔄 Alternativa: Rodar diretamente o `.\run_experiments.ps1 -Iterations 1`
Se vocês quiserem digitar literalmente `.\run_experiments.ps1 -Iterations 1` no vídeo:
1. Digite no terminal:
   ```powershell
   .\run_experiments.ps1 -Iterations 1
   ```
2. Ele vai subir os contêineres, configurar o `tc netem` LAN e rodar `T01, T02, T03, T07, T08, T09` em cerca de **25 segundos**.
3. Quando ele entrar na Etapa 2 (WAN) e começar o `T04` (que leva 85 segundos por causa dos 50 MB com 2% de perda no TCP CUBIC), comentem: *"Notem como na WAN com 2% de perda o teste T04 de 50 MB no TCP CUBIC leva cerca de 85 segundos por repetição devido ao colapso da janela de congestionamento, exatamente como registrado nas 10 repetições completas do nosso dataset"*.

---

## 🧹 PASSO 3: Depois de Encerrar a Gravação (Restaurar Estado Limpo)

Assim que parar a gravação no OBS, rode no PowerShell para garantir que a pasta `data/` fique com os arquivos oficiais de $N=10$ repetições e sem a pasta temporária de backup:

```powershell
Copy-Item -Path "data_backup_n10\*" -Destination "data\" -Recurse -Force
Remove-Item -Path "data_backup_n10" -Recurse -Force
docker compose -f docker\docker-compose.yml down
```

