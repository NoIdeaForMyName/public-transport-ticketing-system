from sqlalchemy import create_engine, func, select, event
from sqlalchemy.orm import sessionmaker, scoped_session, Session, joinedload
from sqlalchemy.sql import null
from sqlalchemy.exc import IntegrityError
from database_communication.models import *
from contextlib import contextmanager
from datetime import datetime, timedelta

# session: scoped_session[Session] | None = None
DB_PATH = None


@contextmanager
def db_session():
    # Create the SQLite engine
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


def get_time_ticket_prices():
    with db_session() as session:
        return list(map(time_ticket_type_to_dict, session.query(TimeTicketPrice).all()))
    
def time_ticket_type_to_dict(type: TimeTicketPrice):
    return {
        "id": type.id,
        "validity_period": type.time_ticket_validity_period,
        "amount": type.time_ticket_amount
    }

def get_course_ticket_price():
    with db_session() as session:
        return course_ticket_type_to_dict(session.query(CourseTicketPrice).first())
    
def course_ticket_type_to_dict(type: CourseTicketPrice):
    return {
        "id": type.id,
        "amount": type.course_ticket_amount
    }

def fetch_price_list():
    return {
        'course_ticket_price': get_course_ticket_price(),
        'time_ticket_prices': get_time_ticket_prices()
    }

# OLD:

# def find_ticket_validator_active_course(ipv4: str):
#     with db_session() as session:
#         certain_validator = select(TicketValidator).where(TicketValidator.validator_ip_address == ipv4).subquery()
#         return (
#             session.query(Course)
#                 .join(Vehicle, Course.fk_vehicle_course == Vehicle.id)
#                 .join(certain_validator, Vehicle.id == certain_validator.fk_vehicle_validator)
#                 .first()
#         )

def find_ticket_validator_active_course(ipv4: str):
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

def check_active_time_tickets(RFID: str):
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

def check_active_course_tickets(RFID: str):
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

def time_ticket_to_dict(ticket: TimeTicket):
    return {
        "id": ticket.id,
        "validity_period": ticket.ticket_validity_period,
        "end_datetime": ticket.ticket_end_datetime,
    }

def course_ticket_to_dict(ticket: CourseTicket):
    vehicle: Vehicle = ticket.course.vehicle
    return {
        "vehicle_id": vehicle.id,
        "vehicle_plate_nb": vehicle.vehicle_plate_number
    }
