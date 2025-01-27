import datetime
from typing import Optional
from .model import Course, CourseTicket, Vehicle, session

class VehicleData:
    id: int
    registration_number: str
    in_use: bool

    def __init__(self, vehicle: Optional[Vehicle], registration_number: str = ""):
        if not vehicle:
            self.id = -1
            self.registration_number = registration_number
            self.in_use = False
            return
        else:
            self.id = vehicle.id
            self.registration_number = vehicle.vehicle_plate_number
            self.in_use = get_active_course(vehicle.id) is not None

def get_active_course(vehicle_id: int) -> Optional[Course]:
    vehicle = session.query(Vehicle).get(vehicle_id)
    if not vehicle:
        return None

    for course in vehicle.courses:
        if course.course_end_datetime is None:
            return course
    return None

def get_all_vehicles() -> list[VehicleData]:
    return [VehicleData(vehicle) for vehicle in session.query(Vehicle).all()]

def start_route(vehicle_id: int) -> bool:
    vehicle = session.query(Vehicle).get(vehicle_id)
    active_course = get_active_course(vehicle_id)
    if not vehicle or active_course is not None:
        return False

    # Create new course
    new_course = Course(fk_vehicle_course=vehicle_id, course_start_datetime=datetime.datetime.now())
    session.add(new_course)
    session.commit()
    return True

def end_route(vehicle_id: int) -> bool:
    vehicle = session.query(Vehicle).get(vehicle_id)
    active_course = get_active_course(vehicle_id)
    if not vehicle or active_course is None:
        return False

    # Create new course
    active_course.course_end_datetime = datetime.datetime.now()
    session.commit()
    return True

def add_vehicle(registration_number: str) -> bool:
    if session.query(Vehicle).filter_by(vehicle_plate_number=registration_number).first():
        return False

    new_vehicle = Vehicle(vehicle_plate_number=registration_number)
    session.add(new_vehicle)
    session.commit()
    return True

def delete_vehicle(vehicle_id: int) -> bool:
    vehicle = session.query(Vehicle).get(vehicle_id)
    if not vehicle:
        return False

    for course in vehicle.courses:
        for ticket in course.course_tickets:
            session.delete(ticket)
        
        session.delete(course)
    
    for validator in vehicle.ticket_validators:
        validator.fk_vehicle_validator = None

    session.delete(vehicle)
    session.commit()
    return True