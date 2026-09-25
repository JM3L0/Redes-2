FROM ubuntu:24.04

# Evitar prompts interativos durante a instalacao
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias essenciais, tshark, iperf3, tc (iproute2) e Python para ciencia de dados
RUN apt-get update && apt-get install -y --no-install-recommends \
    iproute2 \
    iperf3 \
    tshark \
    python3 \
    python3-pip \
    python3-pandas \
    python3-matplotlib \
    python3-numpy \
    python3-scipy \
    ca-certificates \
    wget \
    tar \
    xz-utils \
    jq \
    dnsutils \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Instalar cURL moderno compilado nativamente com suporte a HTTP/3 (ngtcp2 + nghttp3 + TLS 1.3)
RUN wget -q https://github.com/stunnel/static-curl/releases/download/8.22.0/curl-linux-x86_64-glibc-8.22.0.tar.xz -O /tmp/curl.tar.xz \
    && wget -q https://github.com/stunnel/static-curl/releases/download/8.22.0/SHA256SUMS -O /tmp/SHA256SUMS \
    && grep "curl-linux-x86_64-glibc-8.22.0.tar.xz" /tmp/SHA256SUMS | sha256sum -c - \
    && tar -xf /tmp/curl.tar.xz -C /tmp \
    && mv /tmp/curl /usr/local/bin/curl \
    && chmod +x /usr/local/bin/curl \
    && rm -f /tmp/curl.tar.xz /tmp/SHA256SUMS

# Validar que o cURL possui suporte nativo a HTTP3
RUN /usr/local/bin/curl --version | grep -q "HTTP3"

# Criar diretorios de trabalho
WORKDIR /workspace

CMD ["/bin/bash"]
