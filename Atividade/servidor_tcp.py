import socket

# Configurações do Servidor TCP
HOST = "127.0.0.1"
PORT = 65432

def main():
    # Criação do socket TCP: AF_INET (IPv4) e SOCK_STREAM (TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Permite reutilizar o endereço/porta imediatamente após reinicializações
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Realiza o bind na porta 65432
        server_socket.bind((HOST, PORT))
        
        # Coloca o socket em modo de escuta (listen)
        server_socket.listen()
        print(f"[*] Servidor TCP ativo e escutando em {HOST}:{PORT}...")
        print("[*] Aguardando conexões de clientes (Pressione Ctrl+C para encerrar)...\n")
        
        try:
            while True:
                # accept() é uma chamada bloqueante síncrona: aguarda a conclusão do three-way handshake
                # Retorna um novo socket (conn) dedicado à conexão do cliente e o endereço (addr)
                conn, addr = server_socket.accept()
                
                with conn:
                    print(f"[+] Conexão estabelecida com o cliente: {addr}")
                    
                    # Loop para receber dados continuamente enquanto a conexão estiver ativa
                    while True:
                        data = conn.recv(1024)
                        
                        # Quando o cliente encerra a conexão (FIN/close), recv() retorna bytes vazios b''
                        if not data:
                            print(f"[-] Cliente {addr} encerrou a conexão.\n")
                            break
                        
                        mensagem = data.decode("utf-8")
                        print(f"[{addr}] Recebido: \"{mensagem}\"")
                        
                        # Serviço de eco: devolve exatamente a mesma mensagem recebida ao cliente
                        conn.sendall(data)
                        print(f"[{addr}] Resposta de eco enviada com sucesso.")
                        
        except KeyboardInterrupt:
            print("\n[!] Encerrando o servidor TCP por solicitação do usuário...")
        finally:
            print("[*] Servidor TCP finalizado.")

if __name__ == "__main__":
    main()
