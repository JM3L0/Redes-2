# 04. Diretrizes para o Artigo Científico (Padrão SBC / SBRC)

**Disciplina:** Redes de Computadores II (2026-2)  
**Instituição:** UFPI — Bacharelado em Sistemas de Informação  
**Aluno:** João Marcos Sousa Rufino Leal (`jsousarufinoleal@ufpi.edu.br`)

O relatório técnico deve ser redigido estritamente no modelo oficial de artigos da **Sociedade Brasileira de Computação (SBC)**, amplamente utilizado no **Simpósio Brasileiro de Redes de Computadores e Sistemas Distribuídos (SBRC)**.

---

## 🚨 Elemento Obrigatório e Eliminatório na 1ª Página

> [!CAUTION]
> O edital exige:
> **"O relatório deve incluir, logo na primeira página (abaixo do resumo ou na nota de rodapé dos autores), a ligação pública ao vídeo explicativo."**
> A ausência deste link ou link quebrado/inacessível resulta em **NOTA ZERO (0,0)** automática.

### Como Inserir no LaTeX:
```latex
\author{
  João Marcos Sousa Rufino Leal\inst{1}
}

\address{Departamento de Computação -- Universidade Federal do Piauí (UFPI)\\
  Bacharelado em Sistemas de Informação\\
  \email{jsousarufinoleal@ufpi.edu.br}
  \vspace{0.2cm}
  \newline
  \textbf{Vídeo de Demonstração e Apresentação (15 min):} \\
  \url{https://youtu.be/SEU_LINK_AQUI} % Ou link aberto do Google Drive
}
```

---

## 2. Estrutura Obrigatória de Seções

O artigo não possui limite máximo de páginas e deve conter obrigatoriamente as seguintes seções:

### 1. Resumo e Abstract
- **Resumo (Português):** Contextualização concisa (150 a 250 palavras) do problema de transporte na Internet, objetivo do artigo, metodologia experimental baseada em Docker e Linux NetEm, principais achados (onde cada protocolo venceu) e conclusão.
- **Abstract (Inglês):** Tradução fiel e fluida em inglês técnico.
- **Palavras-chave / Keywords:** TCP, UDP, QUIC, HTTP/3, TLS 1.3, Avaliação de Desempenho, NetEm.

### 2. Introdução e Objetivos
- Evolução da Web: da navegação estática (HTTP/1.0 e 1.1) às aplicações ricas e móveis (HTTP/2 e HTTP/3).
- O gargalo do TCP em redes modernas: latência de handshake duplo (TCP + TLS) e Bloqueio de Cabeça de Linha (*Head-of-Line Blocking*).
- O surgimento do QUIC padronizado pelo IETF (RFC 9000).
- Definição clara dos objetivos gerais e específicos da investigação experimental comparativa.

### 3. Fundamentação Teórica
Apresentação detalhada e rigorosa dos protocolos:
- **TCP (Transmission Control Protocol - RFC 793):**
  - Handshake de 3 vias (SYN, SYN-ACK, ACK);
  - Garantia de entrega ordenada, confirmação cumulativa (Cumulative ACK) e controle de fluxo por janela deslizante;
  - Mecanismos de controle de congestionamento (Slow Start, Congestion Avoidance, Fast Retransmit / Fast Recovery);
  - Fenômeno do Head-of-Line (HoL) Blocking na camada de transporte.
- **UDP Puro (User Datagram Protocol - RFC 768):**
  - Sem conexão, sem confirmação e sem controle de fluxo/congestionamento;
  - Estrutura mínima de cabeçalho: 8 bytes fixos (Porta Origem, Porta Destino, Tamanho, Checksum);
  - Aplicações típicas: telemetria, streaming em tempo real, DNS e VoIP.
- **QUIC (RFC 9000) e Criptografia Integrada (RFC 9001 com TLS 1.3 - RFC 8446):**
  - Arquitetura de transporte implementada sobre UDP no espaço do usuário;
  - Multiplexação de streams independentes: eliminação real do HoL blocking no nível de transporte;
  - Números de pacotes estritamente monotônicos e identificador de conexão (*Connection ID* para migração de rede);
  - Handshake unificado: troca de chaves Diffie-Hellman combinada com parâmetros de transporte em 1-RTT (e suporte a 0-RTT via Pre-Shared Keys).

### 4. Metodologia Experimental e Topologia
- Diagrama arquitetural dos contêineres Docker (Server e Client).
- Configuração detalhada do NGINX (`ngx_http_v3_module`, ALPN `h3`, cabeçalho `Alt-Svc`).
- Ferramentas utilizadas: `curl` com suporte a HTTP/3, `iperf3`, `tshark` e ambiente Python.
- Modelagem dos canais de rede via `tc` / `netem` para cada cenário.
- Protocolo de repetibilidade estatística: 10 execuções por ponto de medição, cálculo de média, desvio padrão e intervalos de confiança de 95%.

### 5. Resultados Experimentais e Discussão
Esta é a seção central do trabalho, dividida obrigatoriamente pelos 3 cenários:
- **5.1. Cenário A — Desempenho do UDP Puro em Baixa Latência:**
  - Análise de injeção de taxas (10 a 500 Mbps);
  - Tabela comparativa de sobrecarga de cabeçalho (Overhead);
  - Comportamento de latência e consumo de CPU.
- **5.2. Cenário B — Eficiência do TCP em Transferências Massivas:**
  - Download de arquivos de 100 MB e 1 GB (HTTP/1.1 vs HTTP/2 vs HTTP/3);
  - Goodput médio e tempo total de conclusão de fluxo (FCT);
  - Discussão sobre otimizações de kernel Linux (TSO, GRO) do TCP versus o custo de CPU do QUIC em user-space.
- **5.3. Cenário C — Resiliência do QUIC em Redes Instáveis e Alta Latência:**
  - Carregamento de múltiplos objetos (50 a 100 imagens);
  - Impacto das perdas de pacotes (0%, 2%, 5%) e RTT de 100 ms;
  - Evidência gráfica da eliminação do HoL Blocking no QUIC (gráfico de CDF e percentis p90/p95);
  - Eficiência do handshake 1-RTT e reconexões 0-RTT;
  - Inspeção visual de perdas e retransmissões no Wireshark.

### 6. Considerações Finais e Conclusão
- Síntese das conclusões obtidas: para qual perfil de aplicação cada protocolo é a melhor escolha técnica.
- Trade-offs identificados (complexidade de implementação e uso de CPU vs resiliência e baixa latência).
- Trabalhos futuros (avaliação de algoritmos de congestionamento como BBRv3 vs CUBIC no QUIC).

### 7. Referências Bibliográficas (MANDATÓRIAS)
Devem constar no formato BibTeX oficial:
- **RFC 793:** Transmission Control Protocol (Postel, 1981).
- **RFC 768:** User Datagram Protocol (Postel, 1980).
- **RFC 9000:** QUIC: A UDP-Based Multiplexed and Secure Transport (Iyengar & Thomson, 2021).
- **RFC 9001:** Using TLS to Secure QUIC (Thomson & Turner, 2021).
- **RFC 8446:** The Transport Layer Security (TLS) Protocol Version 1.3 (Rescorla, 2018).
- Artigos clássicos de SBRC, ACM SIGCOMM e IEEE/ACM Transactions on Networking correlatos.

---

## 3. Modelo BibTeX de Referências Obrigatórias

```bibtex
@misc{rfc793,
    series = {Request for Comments},
    number = 793,
    howpublished = {RFC 793},
    publisher = {IETF},
    organization = {Internet Engineering Task Force},
    year = 1981,
    author = {Jon Postel},
    title = {{Transmission Control Protocol}},
    url = {https://www.rfc-editor.org/info/rfc793}
}

@misc{rfc768,
    series = {Request for Comments},
    number = 768,
    howpublished = {RFC 768},
    publisher = {IETF},
    organization = {Internet Engineering Task Force},
    year = 1980,
    author = {Jon Postel},
    title = {{User Datagram Protocol}},
    url = {https://www.rfc-editor.org/info/rfc768}
}

@misc{rfc9000,
    series = {Request for Comments},
    number = 9000,
    howpublished = {RFC 9000},
    publisher = {IETF},
    organization = {Internet Engineering Task Force},
    year = 2021,
    author = {Jana Iyengar and Martin Thomson},
    title = {{QUIC: A UDP-Based Multiplexed and Secure Transport}},
    url = {https://www.rfc-editor.org/info/rfc9000}
}

@misc{rfc9001,
    series = {Request for Comments},
    number = 9001,
    howpublished = {RFC 9001},
    publisher = {IETF},
    organization = {Internet Engineering Task Force},
    year = 2021,
    author = {Martin Thomson and Sean Turner},
    title = {{Using TLS to Secure QUIC}},
    url = {https://www.rfc-editor.org/info/rfc9001}
}

@misc{rfc8446,
    series = {Request for Comments},
    number = 8446,
    howpublished = {RFC 8446},
    publisher = {IETF},
    organization = {Internet Engineering Task Force},
    year = 2018,
    author = {Eric Rescorla},
    title = {{The Transport Layer Security (TLS) Protocol Version 1.3}},
    url = {https://www.rfc-editor.org/info/rfc8446}
}
```
