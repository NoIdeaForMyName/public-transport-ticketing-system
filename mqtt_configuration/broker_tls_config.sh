#!/bin/bash

CERT_DIR="/etc/mosquitto/certs"
CONFIG_FILE="/etc/mosquitto/mosquitto.conf"
CA_KEY="$CERT_DIR/ca.key"
CA_CERT="$CERT_DIR/ca.crt"
SERVER_KEY="$CERT_DIR/server.key"
SERVER_CERT="$CERT_DIR/server.crt"
SERVER_CSR="$CERT_DIR/server.csr"
DAYS_VALID=365


if ! command -v openssl &>/dev/null; then
    apt update && apt install -y openssl
    if [ $? -ne 0 ]; then
        exit 1
    fi
fi

if [ ! -d "$CERT_DIR" ]; then
    echo "Tworzenie katalogu na certyfikaty w $CERT_DIR..."
    mkdir -p "$CERT_DIR"
fi

openssl genrsa -out "$CA_KEY" 2048

openssl req -x509 -new -nodes -key "$CA_KEY" -sha256 -days "$DAYS_VALID" -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=mosquitto-ca" -out "$CA_CERT"

openssl genrsa -out "$SERVER_KEY" 2048

openssl req -new -key "$SERVER_KEY" -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=$(hostname)" -out "$SERVER_CSR"

openssl x509 -req -in "$SERVER_CSR" -CA "$CA_CERT" -CAkey "$CA_KEY" -CAcreateserial -out "$SERVER_CERT" -days "$DAYS_VALID" -sha256

chmod 600 "$CERT_DIR"/*

if ! grep -q "cafile" "$CONFIG_FILE"; then
    echo "cafile $CA_CERT" >> "$CONFIG_FILE"
fi

if ! grep -q "certfile" "$CONFIG_FILE"; then
    echo "certfile $SERVER_CERT" >> "$CONFIG_FILE"
fi

if ! grep -q "keyfile" "$CONFIG_FILE"; then
    echo "keyfile $SERVER_KEY" >> "$CONFIG_FILE"
fi

if ! grep -q "listener 8883" "$CONFIG_FILE"; then
    echo "listener 8883" >> "$CONFIG_FILE"
    echo "protocol mqtt" >> "$CONFIG_FILE"
fi

systemctl restart mosquitto

echo "TLS został skonfigurowany dla Mosquit
