#!/usr/bin/env python3
"""
Gera certificados TLS 1.3 locais autoassinados com Subject Alternative Names (SANs)
para o servidor Caddy HTTP/3 e HTTP/2 da 3ª Avaliação (N3).
"""

import os
import datetime
import ipaddress
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_self_signed_cert(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    key_path = os.path.join(output_dir, "key.pem")
    cert_path = os.path.join(output_dir, "cert.pem")

    print("[*] Gerando chave privada RSA de 2048 bits...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    print("[*] Construindo certificado X.509 v3 com SANs para 172.20.0.30...")
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "BR"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Piaui"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Picos"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "UFPI"),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "RedesII-N3"),
        x509.NameAttribute(NameOID.COMMON_NAME, "server_http3_quic"),
    ])

    san_extensions = [
        x509.DNSName("localhost"),
        x509.DNSName("server_http3_quic"),
        x509.DNSName("server-http3"),
        x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
        x509.IPAddress(ipaddress.ip_address("172.20.0.30")),
    ]

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName(san_extensions),
            critical=False,
        )
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=None),
            critical=True,
        )
        .sign(private_key, hashes.SHA256())
    )

    with open(key_path, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    print(f"[+] Certificados TLS 1.3 salvos com sucesso em {output_dir}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    certs_dir = os.path.join(base_dir, "certs")
    generate_self_signed_cert(certs_dir)
