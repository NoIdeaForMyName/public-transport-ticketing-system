from sqlalchemy import create_engine, func, select, event
from sqlalchemy.orm import sessionmaker, scoped_session, Session, joinedload
from sqlalchemy.sql import null
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
        return session.query(TimeTicketPrice).all()

def get_course_ticket_price():
    with db_session() as session:
        return session.query(CourseTicketPrice).first()

def fetch_price_list():
    return {
        'course_ticket_price': get_course_ticket_price(),
        'time_ticket_prices': get_time_ticket_prices()
    }

def find_ticket_validator_active_course(ipv4: str):
    with db_session() as session:
        certain_validator = select(TicketValidator).where(TicketValidator.validator_ip_address == ipv4).subquery()
        return (
            session.query(Course)
                .join(Vehicle, Course.fk_vehicle_course == Vehicle.id)
                .join(certain_validator, Vehicle.id == certain_validator.fk_vehicle_validator)
                .first()
        )

def check_active_time_tickets(RFID: str):
    with db_session() as session:
        card_id = session.query(Card).filter_by(card_RFID=RFID).first().id
        current_datetime = datetime.now()
        return (
            session.query(TimeTicket)
                .filter_by(fk_card_time_ticket=card_id)
                .filter(TimeTicket.ticket_end_datetime > current_datetime)
                .all()
        )

def check_active_course_tickets(RFID: str):
    with db_session() as session:
        card_id = session.query(Card).filter_by(card_RFID=RFID).first().id
        return (
            session.query(CourseTicket)
                .filter_by(fk_card_course_ticket=card_id)
                .join(Course, CourseTicket.fk_course_ticket == Course.id)
                .filter(Course.course_end_datetime == null())
                .all()
        )
