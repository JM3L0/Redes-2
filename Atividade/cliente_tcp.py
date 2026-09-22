import socket

# Configurações de conexão com o Servidor TCP
HOST = "127.0.0.1"
PORT = 65432

def main():
    print(f"[*] Tentando conectar ao servidor TCP em {HOST}:{PORT}...")
    
    try:
        # Criação do socket TCP: AF_INET (IPv4) e SOCK_STREAM (TCP)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Estabelece a conexão (realiza o Three-Way Handshake SYN -> SYN-ACK -> ACK)
            client_socket.connect((HOST, PORT))
            print(f"[+] Conectado com sucesso ao servidor {HOST}:{PORT}!")
            print("[*] Digite suas mensagens abaixo. Digite 'sair' para encerrar a sessão.\n")
            
            while True:
                mensagem = input("Cliente (mensagem) > ").strip()
                
                if not mensagem:
                    continue
                
                # Critério de parada: palavra 'sair' encerra a sessão
                if mensagem.lower() == "sair":
                    print("[*] Encerrando sessão com o servidor...")
                    break
                
                # Envia mensagem codificada ao servidor
                client_socket.sendall(mensagem.encode("utf-8"))
                
                # Aguarda a resposta (serviço de eco) do servidor
                data = client_socket.recv(1024)
                if not data:
                    print("[-] O servidor fechou a conexão inesperadamente.")
                    break
                
                print(f"[+] Servidor (Eco) > {data.decode('utf-8')}\n")
                
    except ConnectionRefusedError:
        print(f"[-] Erro: Conexão recusada em {HOST}:{PORT}. O servidor TCP não está em execução ou rejeitou a conexão.")
    except Exception as e:
        print(f"[-] Erro durante a comunicação: {e}")
    finally:
        print("[*] Conexão encerrada e socket do cliente TCP fechado.")

if __name__ == "__main__":
    main()
