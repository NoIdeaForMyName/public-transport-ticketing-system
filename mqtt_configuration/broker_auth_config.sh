#!/bin/bash

CONFIG_FILE="/etc/mosquitto/mosquitto.conf"

sed -i '/^allow_anonymous/s/^allow_anonymous.*$/allow_anonymous false/' "$CONFIG_FILE"

if ! grep -q "^password_file" "$CONFIG_FILE"; then
    echo "password_file /etc/mosquitto/passwords.txt" >> "$CONFIG_FILE"
fi

sudo touch /etc/mosquitto/passwords.txt

if systemctl is-active --quiet mosquitto; then
    systemctl restart mosquitto
else
    systemctl start mosquitto
fi

echo "Mosquitto require authorization"
