import json
import paho.mqtt.client as mqtt
import uuid
import threading
import time
import ssl
import datetime

# Konfiguracja brokera MQTT
BROKER_ADDRESS = "localhost"
BROKER_PORT = 1883
USERNAME = "rasp1"
PASSWORD = "rasp1"

CA_CERT = "/tmp/ca.crt"
CLIENT_KEY = "/tmp/client.key"
CLIENT_CERT = "/tmp/client.crt"

REQUEST_TOPIC = "server/request"
RESPONSE_TOPIC = "client/response"

# metody oczekujące na odpowiedź
pending_requests = {}
connected = False

def on_connect(client, userdata, flags, rc):
    global connected
    if rc == 0:
        print("Połączono z brokerem!")
        client.subscribe(RESPONSE_TOPIC)
        connected = True
    else:
        print(f"Błąd połączenia, kod: {rc}")

#obsługa wiadomości
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    request_id = payload.get("id")
    response = payload.get("response")
    success = payload.get("success")

    if request_id in pending_requests:
        future_response = pending_requests.pop(request_id)
        future_response.append((response, success))

# konfiguracja klienta
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(USERNAME, PASSWORD)
# client.tls_set(ca_certs=CA_CERT,
#                certfile=CLIENT_CERT,
#                keyfile=CLIENT_KEY,
#                tls_version=ssl.PROTOCOL_TLSv1_2)
# client.tls_set(CA_CERT, CLIENT_CERT, CLIENT_KEY)

client.connect(BROKER_ADDRESS, BROKER_PORT)
client.loop_start()

def wait_for_connection(timeout=5):
    start_time = time.time()
    while not connected:
        if time.time() - start_time > timeout:
            raise Exception("Timeout")
        time.sleep(0.1)

# wysyłanie zapytań do serwera
def send_request(method, params):
    wait_for_connection()
    request_id = str(uuid.uuid4())
    
    future_response = []
    pending_requests[request_id] = future_response

    payload = {"id": request_id, "method": method, "params": params}
    client.publish(REQUEST_TOPIC, json.dumps(payload))

    # Oczekiwanie na odpowiedź
    while not future_response:
        time.sleep(0.1)

    return future_response[0]

# Definiowanie metod dostępnych dla zewnętrznych plików
def recharge_card(RFID: str, amount: float):
    return send_request("recharge_card", {"RFID": RFID, "amount": amount})

def buy_time_ticket(RFID: str, purchase_datetime, ticket_type_id: int):
    return send_request("buy_time_ticket", {"RFID": RFID, "purchase_datetime": purchase_datetime.strftime("%Y-%m-%d %H:%M:%S"), "ticket_type_id": ticket_type_id})

def buy_course_ticket(RFID: str, validator_ipv4: str):
    return send_request("buy_course_ticket", {"RFID": RFID, "validator_ipv4": validator_ipv4})

def check_active_tickets(RFID: str):
    return send_request("check_active_tickets", {"RFID": RFID})

def check_balance(RFID: str):
    return send_request("check_balance", {"RFID": RFID})

def fetch_price_list():
    return send_request("fetch_price_list", {})
