# 05. Roteiro de Gravação do Vídeo Técnico (15 Minutos Exatos)

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** UFPI — Bacharelado em Sistemas de Informação

---

## ⏱️ Distribuição de Tempo Minuto a Minuto

O edital exige uma apresentação técnica de **exatamente 15 minutos**. Abaixo está o cronômetro planejado para cobrir todos os itens obrigatórios sem estourar nem deixar tempo ocioso.

```text
00:00 ───┬── 01:30 : Bloco 1 - Apresentação da Equipe & Contexto
01:30 ───┼── 05:00 : Bloco 2 - Demonstração Guiada do Código-Fonte (Docker, NGINX, tc/netem)
05:00 ───┼── 10:00 : Bloco 3 - Execução ao Vivo & Demonstração de Capturas (Wireshark / tshark)
10:00 ───┼── 14:00 : Bloco 4 - Apresentação dos Gráficos Gerados & Discussão Científica
14:00 ───┴── 15:00 : Bloco 5 - Conclusões Finais & Encerramento
```

---

## 🎙️ Roteiro Detalhado por Bloco

### Bloco 1: Apresentação da Equipe e Contexto (00:00 – 01:30) [1 min 30s]
- **Tela:** Slide de abertura com título formal, universidade (UFPI), curso, disciplina (Redes II) e nome dos integrantes.
- **Falas Chave:**
  - Saudação formal ao professor e avaliadores.
  - Identificação de cada membro da equipe.
  - Declaração do objetivo da prática: investigação experimental comparativa de desempenho e sobrecarga entre TCP (HTTP/1.1 e 2), UDP Puro (iperf3) e QUIC (HTTP/3) sob condições controladas de emulação com `tc/netem` em ambiente Linux Docker.

### Bloco 2: Demonstração Guiada do Código-Fonte (01:30 – 05:00) [3 min 30s]
- **Tela:** VS Code / Terminal exibindo os arquivos de infraestrutura.
- **Passo a Passo da Demonstração:**
  1. **`docker-compose.yml` (01:30 - 02:30):**
     - Mostrar a definição dos serviços `server` e `client`.
     - Destacar a rede bridge isolada com IP fixo (`172.28.0.0/16`).
     - Enfatizar a flag `cap_add: [NET_ADMIN]` no contêiner cliente, explicando que ela é mandatória para permitir manipulação da pilha de tráfego do kernel Linux via `tc`.
  2. **`nginx.conf` e Certificados TLS (02:30 - 03:45):**
     - Mostrar as diretivas `listen 443 ssl` e `listen 443 quic reuseport`.
     - Mostrar a ativação estrita do `ssl_protocols TLSv1.3` e `ssl_early_data on` (0-RTT).
     - Mostrar o cabeçalho crítico `Alt-Svc: 'h3=":443"; ma=86400'`, explicando sua função em avisar ao cliente sobre a presença do HTTP/3.
     - Mostrar a geração dos certificados autoassinados via OpenSSL.
  3. **Scripts de Emulação com `tc/netem` (03:45 - 05:00):**
     - Abrir o script `setup_netem.sh`.
     - Explicar como o comando `tc qdisc add dev eth0 root netem delay ... loss ...` altera deterministicamente as características do enlace virtual para cada um dos 3 cenários (A, B e C).

### Bloco 3: Execução dos Contêineres ao Vivo e Capturas (05:00 – 10:00) [5 min 00s]
- **Tela:** Terminal dividido (split terminal) ou terminal + Wireshark em tela cheia.
- **Passo a Passo da Demonstração:**
  1. **Inicialização do Ambiente (05:00 - 05:45):**
     - Executar `./run_experiments.sh` ou `docker compose up -d`.
     - Mostrar os dois contêineres saudáveis no `docker ps`.
     - Teste rápido de curl HTTP/3 (`curl -k --http3-only https://server/index.html -I`).
  2. **Disparo do Cenário A (UDP Puro) (05:45 - 06:45):**
     - Disparar o `iperf3` cliente UDP enviando pequenos datagramas a 100/500 Mbps.
     - Mostrar no terminal a ausência de controle de congestionamento e a recepção contínua na taxa nominal.
  3. **Disparo do Cenário B (TCP Massivo) (06:45 - 08:00):**
     - Disparar o download de 100MB via HTTP/2 vs HTTP/3.
     - Mostrar a vazão saturando a banda com alta eficiência no TCP.
  4. **Disparo do Cenário C e Demonstração no Wireshark (08:00 - 10:00):**
     - Aplicar no terminal: `tc qdisc change dev eth0 root netem delay 50ms loss 3%`.
     - Abrir o arquivo de captura `.pcapng` no Wireshark.
     - **Demonstração visual do TCP:** Filtrar por `tcp.analysis.retransmission` e mostrar os pacotes retransmitidos e os congelamentos de janela (Head-of-Line Blocking).
     - **Demonstração visual do QUIC:** Mostrar pacotes `Initial`, `Handshake` e frames `STREAM` com novos números de pacotes monotônicos, comprovando que fluxos independentes não são bloqueados mutuamente pela perda de um único datagrama.

### Bloco 4: Apresentação dos Gráficos Gerados e Discussão (10:00 – 14:00) [4 min 00s]
- **Tela:** Apresentação de slides em alta resolução exibindo os gráficos gerados pelo Python com barras de erro e intervalos de confiança.
- **Discussão dos Resultados:**
  1. **Gráfico do Cenário A (10:00 - 11:00):**
     - Analisar o Goodput do UDP Puro vs sobrecarga de cabeçalho fixa de 8 bytes.
     - Discutir por que o UDP é insubstituível em telemetria em tempo real onde perda eventual é preferível a atraso de retransmissão.
  2. **Gráficos do Cenário B (11:00 - 12:15):**
     - Comparativo de FCT e Goodput para 100MB e 1GB.
     - Explicar tecnicamente a vitória do TCP em canal estável: os mecanismos de offload de hardware/kernel (TSO/GRO) do Linux tornam o TCP extremamente eficiente em CPU frente ao QUIC em user-space.
  3. **Gráficos do Cenário C (12:15 - 14:00):**
     - Comparativo de FCT médio e cauda de latência (p90 e p95) no carregamento dos 100 objetos sob perda de 3% e 5%.
     - Explicar a curva CDF: demonstrar como a curva do HTTP/3 atinge 100% de conclusão muito antes do HTTP/2, provando a mitigação empírica do Head-of-Line Blocking.
     - Comentar a vantagem do handshake TLS 1.3 de 1-RTT e reconexões 0-RTT em conexões com RTT de 100ms.

### Bloco 5: Conclusões Finais e Encerramento (14:00 – 15:00) [1 min 00s]
- **Tela:** Slide de conclusões síntese com câmera dos apresentadores.
- **Mensagens Finais:**
  - Síntese dos trade-offs: Não existe protocolo universalmente superior; a escolha depende dos requisitos da aplicação e das condições do enlace.
  - UDP para tempo real estrito; TCP para transferências massivas em redes estáveis; QUIC para a Web moderna interativa sob redes móveis e instáveis.
  - Agradecimentos e encerramento exatamente na marca dos 15 minutos (14:55 a 15:05).

---

## 🛠️ Checklist e Recomendações de Gravação

- **Software Recomendado:** OBS Studio (configurado para gravação em 1080p a 30 ou 60 FPS).
- **Áudio:** Microfone testado previamente, sem eco e com volume equalizado entre todos os membros da equipe.
- **Fonte do Terminal:** Aumentar a fonte do terminal (mínimo 16pt a 18pt) para garantir legibilidade nítida no vídeo.
- **Hospedagem:**
  - Se YouTube: Configurar como **"Não listado" (Unlisted)** ou **"Público"**. Nunca como privado!
  - Se Google Drive: Configurar o compartilhamento geral como **"Qualquer pessoa com o link pode visualizar"**.
- **Validação Cruzada:** Testar a abertura do link em uma aba anônima (sem login do Google) antes de submeter o relatório.
