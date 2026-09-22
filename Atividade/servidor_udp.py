import socket

# Configurações do Servidor UDP
UDP_IP = "127.0.0.1"
UDP_PORT = 6789

def main():
    # Criação do socket UDP: AF_INET (IPv4) e SOCK_DGRAM (UDP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Vinculando o socket ao endereço IP e porta especificados
    server_socket.bind((UDP_IP, UDP_PORT))
    
    print(f"[*] Servidor UDP ativo e aguardando datagramas em {UDP_IP}:{UDP_PORT}...")
    print("[*] Pressione Ctrl+C para encerrar o servidor.\n")
    
    try:
        while True:
            # recvfrom é uma chamada bloqueante que aguarda a chegada de um datagrama
            # Retorna os dados recebidos (máx 1024 bytes) e a tupla com (IP, porta) do cliente
            data, client_address = server_socket.recvfrom(1024)
            
            mensagem = data.decode("utf-8")
            print(f"[+] Datagrama recebido de {client_address}:")
            print(f"    Conteúdo: \"{mensagem}\"\n")
            
    except KeyboardInterrupt:
        print("\n[!] Encerrando servidor UDP por solicitação do usuário...")
    finally:
        server_socket.close()
        print("[*] Socket UDP fechado.")

if __name__ == "__main__":
    main()
