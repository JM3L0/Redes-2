# Atividade Prática: Comunicação em Rede com Sockets (Python)

## 📌 Objetivo
Implementar e testar aplicações cliente-servidor básicas em Python utilizando os protocolos de transporte **UDP** (não orientado à conexão) e **TCP** (orientado à conexão), analisando as diferenças de comportamento entre eles.

---

## 🔹 Questão 1: Comunicação Não Orientada à Conexão (UDP)

### 1.1 Servidor UDP
- **Protocolo:** UDP (`socket.SOCK_DGRAM`)
- **Endereço de Bind:** `127.0.0.1` (localhost)
- **Porta:** `6789`
- **Comportamento esperado:**
  - Permanecer em loop contínuo aguardando o recebimento de datagramas;
  - Ao receber uma mensagem, imprimir no terminal:
    - O endereço de origem (IP e porta do cliente);
    - O conteúdo decodificado da mensagem recebida.

### 1.2 Cliente UDP
- **Comportamento esperado:**
  - Solicitar uma mensagem de texto ao usuário através do terminal (`input`);
  - Enviar o datagrama com a mensagem digitada para o servidor configurado (`127.0.0.1:6789`).

---

## 🔹 Questão 2: Comunicação Orientada à Conexão (TCP)

### 2.1 Servidor TCP
- **Protocolo:** TCP (`socket.SOCK_STREAM`)
- **Porta:** `65432`
- **Comportamento esperado:**
  - Realizar o *bind* na porta especificada e colocar o socket em modo de escuta (*listen*);
  - Aceitar (*accept*) a conexão de um cliente;
  - Receber dados continuamente enquanto a conexão estiver ativa;
  - Exibir o conteúdo recebido no terminal;
  - Devolver exatamente a mesma mensagem recebida ao cliente (**serviço de eco**) antes de fechar a conexão.

### 2.2 Cliente TCP
- **Comportamento esperado:**
  - Estabelecer conexão com o servidor TCP na porta `65432`;
  - Permitir o envio de mensagens digitadas pelo usuário;
  - Exibir no terminal a resposta de eco recebida do servidor;
  - Encerrar a conexão e a sessão caso a mensagem digitada seja a palavra `"sair"`.

---

## 🔹 Questão 3: Testes Práticos e Análise Conceitual

### 3.1 Ordem de Inicialização
- **Procedimento:**
  - Executar primeiro o script cliente sem que o respectivo servidor esteja em execução (testar para UDP e para TCP).
- **Questões a responder:**
  - O que acontece no caso do **UDP** versus no caso do **TCP**?
  - Explique a diferença de comportamento com base nas características de cada protocolo (conceito de conexão e processo de *handshake* de três vias).

### 3.2 Concorrência Básica
- **Procedimento:**
  - Com o servidor TCP em execução, tentar conectar dois clientes simultaneamente a partir de terminais distintos.
- **Questões a responder:**
  - O segundo cliente consegue ter suas mensagens processadas de imediato?
  - Justifique o motivo considerando a estrutura padrão síncrona (bloqueante) do socket e como o servidor lida com o fluxo de execução.

---

## 📂 Arquivos da Solução Implementada

| Arquivo | Descrição |
| :--- | :--- |
| [`servidor_udp.py`](file:///c:/Users/jsous/Desktop/Redes%202/Atividade/servidor_udp.py) | Implementação do servidor UDP na porta `6789` |
| [`cliente_udp.py`](file:///c:/Users/jsous/Desktop/Redes%202/Atividade/cliente_udp.py) | Implementação do cliente UDP com entrada de texto |
| [`servidor_tcp.py`](file:///c:/Users/jsous/Desktop/Redes%202/Atividade/servidor_tcp.py) | Implementação do servidor TCP de eco na porta `65432` |
| [`cliente_tcp.py`](file:///c:/Users/jsous/Desktop/Redes%202/Atividade/cliente_tcp.py) | Implementação do cliente TCP com encerramento por `"sair"` |
| [`respostas_questao3.md`](file:///c:/Users/jsous/Desktop/Redes%202/Atividade/respostas_questao3.md) | Relatório com respostas teóricas e práticas da Questão 3 |

### Como Executar os Testes

#### 1. Testando UDP (Questão 1)
- **Terminal 1:** `python servidor_udp.py`
- **Terminal 2:** `python cliente_udp.py`

#### 2. Testando TCP (Questão 2 e Questão 3.2)
- **Terminal 1:** `python servidor_tcp.py`
- **Terminal 2:** `python cliente_tcp.py`
- **Terminal 3 (Teste de Concorrência):** `python cliente_tcp.py`

