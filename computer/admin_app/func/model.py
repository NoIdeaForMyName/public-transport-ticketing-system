from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Table, DateTime, create_engine
from sqlalchemy.orm import relationship, sessionmaker, scoped_session, declarative_base
from sqlalchemy.ext.declarative import declarative_base

from config import DB_ADRESS

# Create engine
engine = create_engine(DB_ADRESS)

# Create session factory and bind it to Base
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

class Card(Base):
    __tablename__ = "Cards"
    id = Column(Integer, primary_key=True, autoincrement=True)
    card_RFID = Column(String(12), unique=True, nullable=False)
    card_balance = Column(Numeric(precision=10, scale=2), nullable=False)
    time_tickets = relationship(
        "TimeTicket", back_populates="card"
    )
    course_tickets = relationship(
        "CourseTicket", back_populates="card"
    )

class Vehicle(Base):
    __tablename__ = "Vehicles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_plate_number = Column(String(8), unique=True, nullable=False)
    ticket_validators = relationship(
        "TicketValidator", back_populates="vehicle"
    )
    courses = relationship(
        "Course", back_populates="vehicle"
    )

class CourseTicketPrice(Base):
    __tablename__ = "CourseTicketPrices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_ticket_amount = Column(Numeric(precision=10, scale=2), nullable=False)

class TimeTicketPrice(Base):
    __tablename__ = "TimeTicketPrices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_ticket_validity_period = Column(Integer, unique=True, nullable=False)
    time_ticket_amount = Column(Numeric(precision=10, scale=2), nullable=False)

class TicketValidator(Base):
    __tablename__ = "TicketValidators"
    id = Column(Integer, primary_key=True, autoincrement=True)
    validator_ip_address = Column(String(15), unique=True, nullable=False)
    fk_vehicle_validator = Column(Integer, ForeignKey("Vehicles.id"), nullable=True)
    vehicle = relationship(
        "Vehicle", back_populates="ticket_validators"
    )

class TimeTicket(Base):
    __tablename__ = "TimeTickets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_validity_period = Column(Integer, nullable=False)
    ticket_end_datetime = Column(DateTime, nullable=False)
    fk_card_time_ticket = Column(Integer, ForeignKey("Cards.id"), nullable=False)
    card = relationship(
        "Card", back_populates="time_tickets"
    )

class Course(Base):
    __tablename__ = "Courses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fk_vehicle_course = Column(Integer, ForeignKey("Vehicles.id"), nullable=False)
    course_start_datetime = Column(DateTime, nullable=False)
    course_end_datetime = Column(DateTime, nullable=True)
    course_tickets = relationship(
        "CourseTicket", back_populates="course"
    )
    vehicle = relationship(
        "Vehicle", back_populates="courses"
    )

class CourseTicket(Base):
    __tablename__ = "CourseTicket"
    fk_course_ticket = Column(Integer, ForeignKey("Courses.id"), primary_key=True)
    fk_card_course_ticket = Column(Integer, ForeignKey("Cards.id"), primary_key=True)
    course = relationship(
        "Course", back_populates="course_tickets"
    )
    card = relationship(
        "Card", back_populates="course_tickets"
    )

def create_db():
    Base.metadata.create_all(engine)