from database_communication.common_functions import *

'''
pobierz_cennik(); -> json - cena biletu jednorazowego: {id ceny, cena}, cena biletu czasowego: [{id ceny, cena za 15 min}, {id ceny, cena za 30 min}, {...}] # wywolywane przed kazda proba zakupu biletu w kasowniku
doladuj_karte(RFID, kwota); -> udalo sie lub nie
kup_bilet_czasowy(RFID, czas_kupna, id_ceny_biletu_czasowego); -> udalo sie lub nie
kup_bilet_jednorazowy(RFID, IP_kasownika, id_ceny_biletu_jednorazowego); -> udalo sie lub nie
sprawdz_aktywne_bilety(RFID); -> json - dla czasowych: tylko dane z biletu; dla jednorazowych: id pojazdu
'''

# fetch price list
# fetch_price_list() - imported from common_functions

# recharge card
def recharge_card(RFID: str, amount: float):
    with db_session() as session:
        card_to_charge = session.query(Card).filter_by(card_RFID=RFID).first()
        card_to_charge.card_balance += amount
        session.commit()

# buy time ticket
def buy_time_ticket(RFID: str, purchase_datetime: datetime, ticket_type_id: int):
    with db_session() as session:
        card_id = session.query(Card).filter_by(card_RFID=RFID).first().id
        time_ticket_type = session.query(TimeTicketPrice).filter_by(id=ticket_type_id).first()
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

# buy single-use ticket
def buy_course_ticket(RFID: str, validator_ipv4: str, ticket_type_id: int):
    with db_session() as session:
        card_id = session.query(Card).filter_by(card_RFID=RFID).first().id
        course_id = find_ticket_validator_active_course(validator_ipv4).id
        course_ticket_db = CourseTicket(
            fk_course_ticket = course_id,
            fk_card_course_ticket = card_id
        )
        session.add(course_ticket_db)
        session.commit()

# check active tickets
def check_active_tickets(RFID: str):
    time_ticket_list = check_active_time_tickets(RFID)
    course_ticket_list = check_active_course_tickets(RFID)
    return time_ticket_list + course_ticket_list
