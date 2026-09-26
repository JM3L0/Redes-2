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

# Validar em tempo de build que o NGINX possui suporte a HTTP/3 (ngx_http_v3_module).
# Se esta imagem nao possuir o modulo, o build falhara com erro explicito,
# evitando que os experimentos rodem sem QUIC real.
RUN nginx -V 2>&1 | grep -q "http_v3_module" || \
    { echo ""; \
      echo "=============================================================="; \
      echo "ERRO CRITICO: Esta imagem NGINX nao possui suporte a HTTP/3."; \
      echo "O modulo ngx_http_v3_module nao foi encontrado em nginx -V."; \
      echo "Solucao: use 'nginx:mainline-alpine' ou compile from source."; \
      echo "=============================================================="; \
      exit 1; }

# Expor portas de teste:
# 443 TCP: HTTP/1.1 e HTTP/2 com TLS 1.3
# 443 UDP: HTTP/3 (QUIC)
# 5201 TCP/UDP: iperf3
EXPOSE 443/tcp 443/udp 5201/tcp 5201/udp

ENTRYPOINT ["/entrypoint.sh"]
