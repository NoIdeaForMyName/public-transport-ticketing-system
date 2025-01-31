#!/bin/bash

CONFIG_FILE="/etc/mosquitto/mosquitto.conf"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Plik konfiguracyjny Mosquitto nie został znaleziony w $CONFIG_FILE."
    exit 1
fi

sed -i '/^allow_anonymous/s/^allow_anonymous.*$/allow_anonymous false/' "$CONFIG_FILE"

if ! grep -q "^password_file" "$CONFIG_FILE"; then
    echo "Dodawanie pliku haseł do konfiguracji..."
    echo "password_file /etc/mosquitto/passwords.txt" >> "$CONFIG_FILE"
fi

if systemctl is-active --quiet mosquitto; then
    systemctl restart mosquitto
else
    systemctl start mosquitto
fi

echo "Mosquitto require authorization"
