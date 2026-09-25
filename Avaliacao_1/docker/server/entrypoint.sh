#!/bin/sh
set -e

# Criar diretorio para certificados se nao existir
mkdir -p /etc/nginx/certs

# Gerar certificado autoassinado TLS 1.3 com SAN se nao existir
if [ ! -f /etc/nginx/certs/server.crt ]; then
    echo "[SERVER ENTRYPOINT] Gerando certificados autoassinados TLS 1.3..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/nginx/certs/server.key \
        -out /etc/nginx/certs/server.crt \
        -subj "/C=BR/ST=PI/L=Teresina/O=UFPI/OU=Redes2/CN=server" \
        -addext "subjectAltName=DNS:server,DNS:localhost,IP:172.28.0.10"
    chmod 644 /etc/nginx/certs/server.crt
    chmod 600 /etc/nginx/certs/server.key
    echo "[SERVER ENTRYPOINT] Certificados gerados com sucesso."
fi

# Iniciar servidor iperf3 em segundo plano na porta 5201
echo "[SERVER ENTRYPOINT] Iniciando servidor iperf3 na porta 5201..."
iperf3 -s -p 5201 -D

# Iniciar o NGINX
echo "[SERVER ENTRYPOINT] Iniciando NGINX (HTTP/1.1, HTTP/2 e HTTP/3 QUIC)..."
exec nginx -g "daemon off;"
