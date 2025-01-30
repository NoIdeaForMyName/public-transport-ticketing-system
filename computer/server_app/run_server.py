# main python file for running server app
from database_communication import *
import json
import paho.mqtt.client as mqtt


specify_db_path("./../database/public_transport_ticketing_system.db")

# broker configuration
BROKER_ADDRESS = "localhost"
BROKER_PORT = 1883
USERNAME = ""
PASSWORD = ""

CA_CERT = ""
CLIENT_KEY = ""
CLIENT_CERT = ""

REQUEST_TOPIC = "server/request"
RESPONSE_TOPIC = "client/response"

# available methods configuration
METHODS = {
    "recharge_card": recharge_card,
    "buy_time_ticket": buy_time_ticket,
    "buy_course_ticket": buy_course_ticket,
    "check_active_tickets": check_active_tickets,
    "check_balance": check_balance,
    "fetch_price_list": fetch_price_list
}


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(REQUEST_TOPIC)
    else:
        print(f"Error connecting:  {rc}")

# server receives message via mqtt and publishes called methods results
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        request_id = payload.get("id")
        method_name = payload.get("method")
        params = payload.get("params", {})

        if method_name in METHODS:
            response_data, success = METHODS[method_name](**params)
        else:
            response_data, success = {"error": f"Unknown method: {method_name}"}, False

        response = {"id": request_id, "response": response_data, "success": success}
        client.publish(RESPONSE_TOPIC, json.dumps(response))

    except Exception as e:
        error_msg = {"id": request_id, "response": {"error": str(e)}, "success": False}
        client.publish(RESPONSE_TOPIC, json.dumps(error_msg))

#mqtt client configuration
client = mqtt.Client()
# client.username_pw_set(USERNAME, PASSWORD)
# client.tls_set(CA_CERT, CLIENT_CERT, CLIENT_KEY)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_ADDRESS, BROKER_PORT)
client.loop_forever()

# def main():
#     ...

# if __name__ == '__main__':
#     main()
