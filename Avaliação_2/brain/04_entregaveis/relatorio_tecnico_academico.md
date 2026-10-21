# 04. Diretrizes para o Relatório Técnico Acadêmico (Padrão SBC / LaTeX)

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** Universidade Federal do Piauí (UFPI) — Campus Senador Helvídio Nunes de Barros (CSHNB)  
**Curso:** Bacharelado em Sistemas de Informação  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)

O Relatório Técnico conclusivo deve apresentar rigor formal de publicação científica, sendo elaborado preferencialmente no modelo da **Sociedade Brasileira de Computação (SBC)**, padrão consagrado no **Simpósio Brasileiro de Redes de Computadores e Sistemas Distribuídos (SBRC)**.

---

## 1. 🚨 Elemento Mandatório e Eliminatório na 1ª Página

> [!CAUTION]
> ### REGRA DE NOTA ZERO (0,0):
> **"O relatório técnico conclusivo e o vídeo de 15 minutos explicando a execução, os pontos importantes da implementação, os resultados e a conclusão dos experimentos... O link do vídeo no Youtube deve estar no Relatório Técnico... Faltando os códigos, o relatório ou o vídeo, a nota será zero."**

O link público do vídeo no YouTube deve ser obrigatoriamente inserido na **primeira página**, logo abaixo dos dados do autor ou como nota de rodapé dos autores.

### Código de Inserção no LaTeX (`sbc-template.tex`):
```latex
\author{
  João Marcos Sousa Rufino Leal\inst{1}
}

\address{Departamento de Computação -- Universidade Federal do Piauí (UFPI)\\
  Campus Senador Helvídio Nunes de Barros (CSHNB) -- Picos -- PI -- Brasil\\
  \email{jsousarufinoleal@ufpi.edu.br}
  \vspace{0.25cm}
  \newline
  \textbf{Vídeo de Apresentação e Demonstração Técnica (15 min):} \\
  \url{https://youtu.be/SEU_LINK_AQUI}
}
```

---

## 2. Estrutura Obrigatória das Seções do Relatório

O documento deve seguir a estrutura acadêmica formal composta pelas seções abaixo:

### 2.1. Resumo e Abstract
- **Resumo (Português):** Síntese estruturada (150 a 250 palavras) contendo contexto da pilha de transporte da Web, objetivos da investigação experimental (handshakes, HoL blocking e perdas), metodologia com Docker e cliente Python assíncrono, principais resultados empíricos e conclusões.
- **Abstract (Inglês):** Versão fiel e fluida em inglês acadêmico.
- **Palavras-chave / Keywords:** Protocolos Web, HTTP/1.1, HTTPS, HTTP/2, HTTP/3, QUIC, TLS 1.3, TCP CUBIC, BBR, Linux Traffic Control, Avaliação de Desempenho.

### 2.2. Seção 1: Introdução e Objetivos
- Evolução histórica dos protocolos de aplicação: das limitações de concorrência do HTTP/1.1 à multiplexação em conexão única do HTTP/2 e à transição para datagramas UDP no HTTP/3 (QUIC).
- Apresentação clara dos 3 fenômenos pedagógicos investigados:
  1. O custo cumulativo de RTTs de handshakes de transporte e criptografia (1 RTT vs 2 RTTs vs 1 RTT);
  2. O Bloqueio de Início de Linha (*Head-of-Line Blocking*) na aplicação e no transporte;
  3. O comportamento sob canais ruidosos e com perdas estocásticas.
- Definição formal das hipóteses científicas do trabalho.

### 2.3. Seção 2: Fundamentação Teórica
Apresentação detalhada da literatura técnica e normas do IETF:
- **Handshakes e Estabelecimento de Conexão:**
  - TCP 3-Way Handshake (SYN, SYN-ACK, ACK — RFC 793);
  - TLS 1.3 Handshake (negociação integrada em 1 RTT com Diffie-Hellman efêmero — RFC 8446);
  - QUIC Crypto & Transport Handshake (fusão do transporte e chaves criptográficas em 1 RTT conjunto sobre UDP — RFC 9000 e RFC 9001).
- **Mecanismos de Multiplexação e HoL Blocking:**
  - HTTP/1.1 (RFC 7230): ausência de multiplexação nativa, dependência de conexões TCP paralelas ou pipelining ineficiente;
  - HTTP/2 (RFC 7540): multiplexação por quadros binários sobre TCP e a vulnerabilidade à perda de pacotes no transporte;
  - HTTP/3 (RFC 9114): multiplexação sobre streams QUIC independentes.

### 2.4. Seção 3: Metodologia Experimental e Topologia
- Descrição da topologia de contêineres na rede Docker `net_bench` (172.20.0.0/16).
- Especificações dos 3 servidores: Nginx HTTP/1.1 (8080), Nginx HTTPS TLS 1.3 (8443) e Caddy HTTP/3 (9443).
- Modelagem de canal com Linux Traffic Control (`tc netem`) e justificativa matemática do atraso unidirecional $N/2$ para RTT de $N$ ms (Cenário 1: 0.5ms delay = 1ms RTT; Cenário 2: 25ms delay, 2% loss = 50ms RTT).
- Arquitetura do Cliente de Benchmark Python:
  - Assincronismo com `httpx` e `aioquic`;
  - Procedimentos de **Controle de Viés de Sessão (Client-Side Bias Control)**: destruição explícita de sessão (`client.close()`) para Cold TTFB vs canal persistente mantido para Carga B concorrente.
- Matriz Experimental dos 12 testes (T01 a T12) e protocolo de 10 repetições independentes ($N \ge 10$).

### 2.5. Seção 4: Resultados Experimentais e Discussão Analítica
Esta seção constitui o cerne científico da avaliação (peso de 30 pontos no Eixo 4):

#### A. Consolidação Numérica em Tabelas
Apresentação de tabelas com dados consolidados para os 12 testes:
- Média ($\bar{x}$) e Desvio Padrão ($s$);
- Mediana e Intervalo de Confiança de 95% ($CI_{95\%}$);
- Percentis p50 e p99 para:
  - TTFB (ms);
  - Tempo Total de Carregamento (ms);
  - Vazão Útil / Goodput (Mbps);
  - Requisições por Segundo (RPS).

#### B. Visualização Gráfica com Barras de Erro Obrigatórias
- Todos os gráficos devem conter **barras de erro** representando a dispersão amostral (desvio padrão ou IC 95%).
- Gráficos gerados programaticamente com eixos rotulados, unidades expressas e legendas nítidas.

#### C. Articulação Teórica Obrigatória com Tanenbaum

> [!IMPORTANT]
> ### EXIGÊNCIA EXPRESSA DO EDITAL (-20 PONTOS SE FALTAR):
> O edital prescreve que o relatório **não pode ser meramente descritivo**. A discussão dos dados deve confrontar os números observados com a literatura clássica:
>
> 1. **Tanenbaum §6.5.11 (TCP CUBIC):**  
>    Utilizar para fundamentar analiticamente o colapso de throughput e elevação de latência observado nos testes **T04** (HTTP/1.1 WAN) e **T05** (HTTP/2 WAN).  
>    - Demonstrar matematicamente a função de janela cúbica do CUBIC:  
>      $$W_{\text{cubic}}(t) = C (t - K)^3 + W_{\text{max}}$$  
>      onde $C$ é a constante de escala, $t$ é o tempo transcorrido desde a última redução de janela, $W_{\text{max}}$ é o tamanho da janela no instante da perda e $K = \sqrt[3]{(W_{\text{max}} \beta) / C}$.
>    - Explicar por que a injeção contínua de 2% de perda estocástica impede o CUBIC de alcançar a fase côncava/convexa de saturação de banda, forçando sucessivas retrações multiplicativas ($\beta = 0.7$) e mantendo a janela *cwnd* permanentemente estrangulada em canais com RTT de 50ms.
>
> 2. **Tanenbaum §6.6.1 (QUIC) e §6.6.2 (BBR):**  
>    Utilizar para justificar por que os testes **T06** (Carga A QUIC WAN) e **T12** (Carga B QUIC WAN) sustentam alto desempenho e RPS superior sob as mesmíssimas condições adversas.  
>    - Explicar como o QUIC elimina o HoL blocking na camada de transporte ao encapsular fluxos independentes em datagramas UDP separados, garantindo que o descarte de um pacote atrase apenas a entrega do stream correspondente, sem congelar os buffers dos 99 streams restantes.  
>    - Descrever como os algoritmos modernos de controle de congestionamento associados ao QUIC (como o BBR — *Bottleneck Bandwidth and RTT*) dissociam a perda de pacotes da estimativa de capacidade do enlace, regulando a injeção de pacotes pelo modelo de ritmo (*pacing*) fundamentado na largura de banda de gargalo real e no RTT mínimo de propagação física.

### 2.6. Seção 5: Considerações Finais e Conclusões
- Síntese dos achados empíricos e confirmação das hipóteses teóricas.
- Implicações práticas para arquitetos de software e engenheiros de infraestrutura de redes: quando adotar HTTP/2 vs HTTP/3 na produção.

### 2.7. Referências Bibliográficas
- Citação completa do livro texto:
  - TANENBAUM, Andrew S.; WETHERALL, David J. *Redes de Computadores*. 5ª ou 6ª Edição. Pearson.
- Citação formal das RFCs mandatórias do IETF:
  - RFC 793 (TCP)
  - RFC 768 (UDP)
  - RFC 7540 (HTTP/2)
  - RFC 8446 (TLS 1.3)
  - RFC 9000 (QUIC Transport)
  - RFC 9001 (QUIC TLS)
  - RFC 9114 (HTTP/3)
