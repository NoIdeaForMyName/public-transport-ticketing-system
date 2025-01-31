#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Użycie: $0 <nazwa_użytkownika> <hasło>"
    exit 1
fi

USER=$1
PASSWORD=$2
PASSWORD_FILE="/etc/mosquitto/passwords.txt"

mosquitto_passwd -b "$PASSWORD_FILE" "$USER" "$PASSWORD"

if systemctl is-active --quiet mosquitto; then
    systemctl restart mosquitto
else
    systemctl start mosquitto
fi

echo "Użytkownik $USER został dodany i może subskrybować tematy."
