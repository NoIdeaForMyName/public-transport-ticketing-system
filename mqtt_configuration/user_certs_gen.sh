#!/bin/bash

if [ $# -ne 3 ]; then
    echo "Użycie: $0 <IP_klienta> <Użytkownik_SSH> <Hasło_SSH>"
    exit 1
fi

CLIENT_IP=$1
SSH_USER=$2
SSH_PASS=$3

CERT_DIR="/etc/mosquitto/certs"
CA_KEY="$CERT_DIR/ca.key"
CA_CERT="$CERT_DIR/ca.crt"
CLIENT_KEY="$CERT_DIR/client.key"
CLIENT_CERT="$CERT_DIR/client.crt"
CLIENT_CSR="$CERT_DIR/client.csr"
DAYS_VALID=365

echo "Sprawdzanie, czy sshpass jest zainstalowany..."
if ! command -v sshpass &>/dev/null; then
    echo "sshpass nie jest zainstalowany. Instalowanie..."
    apt update && apt install -y sshpass
    if [ $? -ne 0 ]; then
        echo "Nie udało się zainstalować sshpass. Sprawdź połączenie z internetem lub uprawnienia."
        exit 1
    fi
else
    echo "sshpass jest już zainstalowany."
fi

openssl genrsa -out "$CLIENT_KEY" 2048

openssl req -new -key "$CLIENT_KEY" -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=client" -out "$CLIENT_CSR"

openssl x509 -req -in "$CLIENT_CSR" -CA "$CA_CERT" -CAkey "$CA_KEY" -CAcreateserial -out "$CLIENT_CERT" -days "$DAYS_VALID" -sha256

chmod 600 "$CLIENT_KEY" "$CLIENT_CERT"

sshpass -p "$SSH_PASS" scp "$CLIENT_CERT" "$CLIENT_KEY" "$CA_CERT" "$SSH_USER@$CLIENT_IP:/tmp/"

echo "Operacja zakończona pomyślnie."
