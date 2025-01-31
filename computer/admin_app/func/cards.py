from .model import Card, CourseTickets, TimeTicket, session

class CardData:
    id: int
    rfid: str
    balance: float

    def __init__(self, card: Card):
        self.id = card.id
        self.rfid = card.card_RFID
        self.balance = card.card_balance

def get_all_cards() -> list[CardData]:
    return [CardData(card) for card in session.query(Card).all()]

def get_card_by_id(card_id: int) -> CardData:
    return CardData(session.query(Card).get(card_id))

def add_card(rfid: str) -> bool:
    if session.query(Card).filter_by(card_RFID=rfid).first():
        return False
    
    new_card = Card(card_RFID=rfid, card_balance=0)
    session.add(new_card)
    session.commit()
    return True

# def update_ticket_validator(validator_id: int, vehicle_id: int) -> bool:
#     validator = session.query(TicketValidator).get(validator_id)
#     if not validator:
#         return False

#     validator.fk_vehicle_validator = vehicle_id
#     session.commit()
#     return True

def delete_card(card_id: int) -> bool:
    card = session.query(Card).get(card_id)
    if not card:
        return False

    session.query(CourseTickets).filter(
        CourseTickets.fk_card_course_ticket == card_id
    ).delete(synchronize_session=False)
    
    # Then delete TimeTickets
    session.query(TimeTicket).filter(
        TimeTicket.fk_card_time_ticket == card_id
    ).delete(synchronize_session=False)
    
    # Finally delete the card
    card = session.query(Card).get(card_id)
    if not card:
        return False
        
    session.delete(card)
    session.flush()
    session.commit()
    return True