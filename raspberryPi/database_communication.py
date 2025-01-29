import json
import paho.mqtt.client as mqtt
import uuid

#broker configuration
BROKER_ADDRESS = ""
BROKER_PORT = 8883
USERNAME = ""
PASSWORD = ""

CA_CERT = ""
CLIENT_KEY = ""
CLIENT_CERT = ""

REQUEST_TOPIC = "server/request"
RESPONSE_TOPIC = "client/response"

pending_requests = {}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Połączono z brokerem!")
        client.subscribe(RESPONSE_TOPIC)
    else:
        print(f"Błąd połączenia, kod: {rc}")

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    request_id = payload.get("id")
    response = payload.get("response")
    success = payload.get("success")

    if request_id in pending_requests:
        callback = pending_requests.pop(request_id)
        callback(response, success)

#sending method and parameters to server
def send_request(method, params):
    request_id = str(uuid.uuid4())
    
    future_response = []
    pending_requests[request_id] = lambda response, success: future_response.append((response, success))
    
    payload = {"id": request_id, "method": method, "params": params}
    client.publish(REQUEST_TOPIC, json.dumps(payload))

    while not future_response:
        client.loop()

    return future_response[0]

#client configuration
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(CA_CERT, CLIENT_CERT, CLIENT_KEY)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_ADDRESS, BROKER_PORT)
client.loop_start()

#available methods
def recharge_card(RFID: str, amount: float):
    return send_request("recharge_card", {"RFID": RFID, "amount": amount})

def buy_time_ticket(RFID: str, purchase_datetime: str, ticket_type_id: int):
    return send_request("buy_time_ticket", {"RFID": RFID, "purchase_datetime": purchase_datetime, "ticket_type_id": ticket_type_id})

def buy_course_ticket(RFID: str, validator_ipv4: str):
    return send_request("buy_course_ticket", {"RFID": RFID, "validator_ipv4": validator_ipv4})

def check_active_tickets(RFID: str):
    return send_request("check_active_tickets", {"RFID": RFID})

def check_balance(RFID: str):
    return send_request("check_balance", {"RFID": RFID})

def fetch_price_list():
    return send_request("fetch_price_list", {})
