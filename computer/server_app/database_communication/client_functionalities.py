from database_communication.common_functions import *


# fetch price list
# fetch_price_list() - imported from common_functions

# recharge card
def recharge_card(RFID: str, amount: float):
    with db_session() as session:
        card_to_charge = session.query(Card).filter_by(card_RFID=RFID).first()
        if not card_to_charge:
            return {"error": f"Card with RFID:[{RFID}] not found"}, False
        card_to_charge.card_balance += amount
        session.commit()
    return {"message": "Card recharged succesfully"}, True

# buy time ticket
def buy_time_ticket(RFID: str, purchase_datetime: datetime, ticket_type_id: int):
    with db_session() as session:
        card = session.query(Card).filter_by(card_RFID=RFID).first()
        if not card:
            return {"error": f"Card with RFID:[{RFID}] not found"}, False
        card_id = card.id
        time_ticket_type = session.query(TimeTicketPrice).filter_by(id=ticket_type_id).first()
        if not time_ticket_type:
            return {"error": f"Time ticket type with id: {ticket_type_id} not found"}, False
        validity_period = time_ticket_type.time_ticket_validity_period
        price = time_ticket_type.time_ticket_amount
        end_datetime = purchase_datetime + timedelta(minutes=validity_period)
        ticket_db = TimeTicket(
            ticket_validity_period = validity_period,
            ticket_end_datetime = end_datetime,
            fk_card_time_ticket = card_id
        )
        session.add(ticket_db)
        session.commit()
    return {"message": "Time ticket bought succesfully"}, True

# buy single-use ticket
def buy_course_ticket(RFID: str, validator_ipv4: str):
    with db_session() as session:
        card = session.query(Card).filter_by(card_RFID=RFID).first()
        if not card:
            return {"error": f"Card with RFID:[{RFID}] not found"}, False
        card_id = card.id
        msg, course_found = find_ticket_validator_active_course(validator_ipv4)
        if not course_found:
            return msg, course_found
        course = msg['active_course']
        if not course:
            return {"error": f"Ticket validator is not active"}, False # no active courses found for given validator's ip address
        course_id = course.id
        course_ticket_db = CourseTicket(
            fk_course_ticket = course_id,
            fk_card_course_ticket = card_id
        )
        session.add(course_ticket_db)
        session.commit()
    return {"message": "Course ticket bought succesfully"}, True

# check active tickets
def check_active_tickets(RFID: str):
    time_ticket_msg, t_ticket_found = check_active_time_tickets(RFID)
    if not t_ticket_found:
        return time_ticket_msg, t_ticket_found
    course_ticket_msg, c_ticket_found = check_active_course_tickets(RFID)
    if not c_ticket_found:
        return course_ticket_msg, c_ticket_found
    return {"active_tickets": list(map(time_ticket_to_dict, time_ticket_msg["active_time_tickets"])) + list(map(course_ticket_to_dict, course_ticket_msg["active_course_tickets"]))}, True
