from sqlalchemy import create_engine, func, select, event
from sqlalchemy.orm import sessionmaker, scoped_session, Session, joinedload
from sqlalchemy.sql import null
from sqlalchemy.exc import IntegrityError
from database_communication.models import *
from contextlib import contextmanager
from datetime import datetime, timedelta


DB_PATH = None


@contextmanager
def db_session():
    # Create the SQLite engine
    if not DB_PATH:
        raise ValueError("No DB_PATH specified. Run specify_db_path(db_path) to be able to start database session")
    engine = create_engine(f'sqlite:///{DB_PATH}')
    
    # Enable foreign key constraint checking for SQLite
    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.close()
    
    # Create a scoped session
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
    try:
        yield db_session
    finally:
        db_session.close()


def get_time_ticket_prices() -> list[dict]:
    with db_session() as session:
        return list(map(time_ticket_type_to_dict, session.query(TimeTicketPrice).all()))
    
def get_course_ticket_price() -> dict:
    with db_session() as session:
        return course_ticket_type_to_dict(session.query(CourseTicketPrice).first())

def fetch_price_list() -> tuple[dict, bool]:
    return {
        'course_ticket_price': get_course_ticket_price(),
        'time_ticket_prices': get_time_ticket_prices()
    }, True

def find_ticket_validator_active_course(ipv4: str) -> tuple[dict, bool]:
    with db_session() as session:
        certain_validator = session.query(TicketValidator).filter_by(validator_ip_address=ipv4).first()
        if not certain_validator:
            return {"error": f"Ticket validator with IP address: {ipv4} not found"}, False
        fk_vehicle_validator = certain_validator.fk_vehicle_validator
        return {
            "active_course": (
            session.query(Course)
                .join(Vehicle, Course.fk_vehicle_course == Vehicle.id)
                .where(Vehicle.id == fk_vehicle_validator)
                .where(Course.course_end_datetime == null())
                .first()
        )
        }, True

def check_active_time_tickets(RFID: str) -> tuple[dict, bool]:
    with db_session() as session:
        card = session.query(Card).filter_by(card_RFID=RFID).first()
        if not card:
            return {"error": f"Card with RFID:[{RFID}] not found"}, False
        card_id = card.id
        current_datetime = datetime.now()
        return {
            "active_time_tickets": (
            session.query(TimeTicket)
                .filter_by(fk_card_time_ticket=card_id)
                .filter(TimeTicket.ticket_end_datetime > current_datetime)
                .all()
        )
        }, True

def check_active_course_tickets(RFID: str) -> tuple[dict, bool]:
    with db_session() as session:
        card = session.query(Card).filter_by(card_RFID=RFID).first()
        if not card:
            return {"error": f"Card with RFID:[{RFID}] not found"}, False
        card_id = card.id
        return {
            "active_course_tickets": (
            session.query(CourseTicket)
                .filter_by(fk_card_course_ticket=card_id)
                .join(Course, CourseTicket.fk_course_ticket == Course.id)
                .filter(Course.course_end_datetime == null())
                .all()
        )
        }, True


# MODEL DATA TO DICTIONARY FUNCTIONS:

def time_ticket_to_dict(ticket: TimeTicket) -> dict:
    return {
        "id": ticket.id,
        "validity_period": ticket.ticket_validity_period,
        "end_datetime": ticket.ticket_end_datetime,
    }

def course_ticket_to_dict(ticket: CourseTicket) -> dict:
    with db_session() as session:
        ticket = session.merge(ticket)
        vehicle: Vehicle = ticket.course.vehicle
    return {
        "vehicle_id": vehicle.id,
        "vehicle_plate_nb": vehicle.vehicle_plate_number
    }

def time_ticket_type_to_dict(type: TimeTicketPrice) -> dict:
    return {
        "id": type.id,
        "validity_period": type.time_ticket_validity_period,
        "amount": type.time_ticket_amount
    }

def course_ticket_type_to_dict(type: CourseTicketPrice) -> dict:
    return {
        "id": type.id,
        "amount": type.course_ticket_amount
    }

def vehicle_to_dict(vehicle: Vehicle) -> dict:
    return {
        "id": vehicle.id,
        "plate_number": vehicle.vehicle_plate_number
    }

def vehicle_data_to_dict(vehicle: Vehicle, course_id: int | None) -> dict:
    return {
        "id": vehicle.id,
        "plate_number": vehicle.vehicle_plate_number,
        "course_id": course_id
    }

def ticket_validator_data_to_dict(validator: TicketValidator) -> dict:
    return {
        "id": validator.id,
        "ipv4": validator.validator_ip_address,
        "vehicle_id": validator.vehicle.id,
        "vehicle_plate_nb": validator.vehicle.vehicle_plate_number
    }

def card_to_dict(card: Card) -> dict:
    return {
        "id": card.id,
        "RFID": card.card_RFID,
        "balance": card.card_balance
    }
