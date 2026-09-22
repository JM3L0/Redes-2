import socket

# Configurações de destino para o Servidor UDP
UDP_IP = "127.0.0.1"
UDP_PORT = 6789

def main():
    # Criação do socket UDP: AF_INET (IPv4) e SOCK_DGRAM (UDP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print(f"[*] Cliente UDP configurado para destino: {UDP_IP}:{UDP_PORT}")
    
    try:
        # Solicita a mensagem de texto ao usuário no terminal
        mensagem = input("Digite a mensagem para enviar ao servidor UDP: ")
        
        # Envia a mensagem codificada em bytes para o endereço/porta do servidor
        # Em UDP não há handshake prévio (não orientado à conexão)
        client_socket.sendto(mensagem.encode("utf-8"), (UDP_IP, UDP_PORT))
        print(f"[+] Mensagem enviada com sucesso para {UDP_IP}:{UDP_PORT}!")
        
    except Exception as e:
        print(f"[-] Erro ao enviar mensagem: {e}")
    finally:
        # Fechamento do socket do cliente
        client_socket.close()
        print("[*] Socket do cliente UDP finalizado.")

if __name__ == "__main__":
    main()
