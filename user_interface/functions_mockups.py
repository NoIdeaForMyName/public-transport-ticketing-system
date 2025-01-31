from datetime import datetime
import random


# recharge card
def recharge_card(RFID: str, amount: float) -> tuple[dict, bool]:
    value = random.choices([False, True], weights=[0.2, 0.8])[0]
    dict = {}
    return dict, value


# buy time ticket
def buy_time_ticket(RFID: str, purchase_datetime: datetime, ticket_type_id: int) -> tuple[dict, bool]:
    value = random.choices([False, True], weights=[0.2, 0.8])[0]
    dict = {}
    return dict, value


# buy single-use ticket
def buy_course_ticket(RFID: str, validator_ipv4: str) -> tuple[dict, bool]:
    value = random.choices([False, True], weights=[0.2, 0.8])[0]
    dict = {}
    return dict, value

# check active tickets
def check_active_tickets(RFID: str) -> tuple[dict, bool]:
    value = random.choices([False, True], weights=[0.2, 0.8])[0]
    dict = {}
    return dict, value

# check balance
def check_balance(RFID: str) -> tuple[dict, bool]:
    value = random.choices([False, True], weights=[0.2, 0.8])[0]
    dict = {}
    return dict, value
