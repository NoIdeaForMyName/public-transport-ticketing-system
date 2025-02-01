#!/bin/bash

USER=$1
PASSWORD=$2
PASSWORD_FILE="/etc/mosquitto/passwords.txt"

mosquitto_passwd -b "$PASSWORD_FILE" "$USER" "$PASSWORD"

if systemctl is-active --quiet mosquitto; then
    systemctl restart mosquitto
else
    systemctl start mosquitto
fi

echo "User $USER has been added and can subscribe now"

