from .model import TicketValidator, session

class TicketValidatorData:
    id: int
    ip_adress: str
    vehicle_id: int
    vehicle_plate_number: str

    def __init__(self, ticket_validator: TicketValidator):
        self.id = ticket_validator.id
        self.ip_adress = ticket_validator.validator_ip_address
        self.vehicle_id = ticket_validator.fk_vehicle_validator if ticket_validator.fk_vehicle_validator else -1
        self.vehicle_plate_number = TicketValidator.vehicle.vehicle_plate_number if ticket_validator.fk_vehicle_validator else ""

def get_all_ticket_validators() -> list[TicketValidatorData]:
    return [TicketValidatorData(validator) for validator in session.query(TicketValidator).all()]

def get_ticket_validator_by_id(validator_id: int) -> TicketValidatorData:
    return TicketValidatorData(session.query(TicketValidator).get(validator_id))

def add_ticket_validator(ip_adress: str) -> bool:
    if session.query(TicketValidator).filter_by(validator_ip_address=ip_adress).first():
        return False
    
    new_validator = TicketValidator(validator_ip_address=ip_adress)
    session.add(new_validator)
    session.commit()
    return True

def update_ticket_validator(validator_id: int, vehicle_id: int) -> bool:
    validator = session.query(TicketValidator).get(validator_id)
    if not validator:
        return False

    validator.fk_vehicle_validator = vehicle_id
    session.commit()
    return True

def delete_ticket_validator(validator_id: int) -> bool:
    validator = session.query(TicketValidator).get(validator_id)
    if not validator:
        return False

    TicketValidator.delete(validator)
    session.commit()
    return True