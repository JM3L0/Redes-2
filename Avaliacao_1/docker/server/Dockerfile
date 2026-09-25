FROM nginx:1.27-alpine

# Instalar dependencias necessarias: iperf3, openssl, iproute2 (tc), bash
RUN apk add --no-cache \
    iperf3 \
    openssl \
    iproute2 \
    bash \
    ca-certificates

# Copiar configuracao customizada do NGINX
COPY nginx.conf /etc/nginx/nginx.conf

# Copiar script de inicializacao
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expor portas de teste:
# 443 TCP: HTTP/1.1 e HTTP/2 com TLS 1.3
# 443 UDP: HTTP/3 (QUIC)
# 5201 TCP/UDP: iperf3
EXPOSE 443/tcp 443/udp 5201/tcp 5201/udp

ENTRYPOINT ["/entrypoint.sh"]
