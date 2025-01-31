#!/bin/bash
CERT_DIR="/etc/mosquitto/certs"
CA_KEY="$CERT_DIR/ca.key"
CA_CERT="$CERT_DIR/ca.crt"
CLIENT_KEY="$CERT_DIR/client.key"
CLIENT_CERT="$CERT_DIR/client.crt"
CLIENT_CSR="$CERT_DIR/client.csr"
DAYS_VALID=365

openssl genrsa -out "$CLIENT_KEY" 2048

openssl req -new -key "$CLIENT_KEY" -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=client" -out "$CLIENT_CSR"

openssl x509 -req -in "$CLIENT_CSR" -CA "$CA_CERT" -CAkey "$CA_KEY" -CAcreateserial -out "$CLIENT_CERT" -days "$DAYS_VALID" -sha256

chmod 600 "$CLIENT_KEY" "$CLIENT_CERT"

echo "Certificates generated"
