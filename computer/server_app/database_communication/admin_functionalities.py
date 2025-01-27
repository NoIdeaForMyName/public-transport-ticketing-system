from database_communication.common_functions import *


##############################################################################################################################
#functionalities related to vehicles:

# fetch all vehicles data
def fetch_all_vehicles():
    with db_session() as session:
        active_courses = select(Course).where(Course.course_end_datetime == null()).subquery()
        to_return = (
            session.query(
                Vehicle,
                func.min(active_courses.c.id).label("Courses_id") # could be any function (min, max, first etc.) because it will always be only one Course entry available
            )
            .outerjoin(active_courses, Vehicle.id == active_courses.c.fk_vehicle_course) # left join
            .group_by(Vehicle)
            .all()
        )
        return {"vehicle_data": list(map(lambda v_d: vehicle_data_to_dict(*v_d), to_return))}, True

def vehicle_data_to_dict(vehicle: Vehicle, course_id: int | None):
    return {
        "id": vehicle.id,
        "plate_number": vehicle.vehicle_plate_number,
        "course_id": course_id
    }
'''
select vehicle.id, vehicle.plate_nb, first(course.id) from
vehicles left join (select course.id from courses where course.end_datetime = NULL) on vehicle.id = course.id
group by vehicle.id, vehicle.plate_nb
'''

# add vehicle
def add_vehicle(plate_nb: str):
    vehicle_db = Vehicle(
        vehicle_plate_number = plate_nb
    )
    with db_session() as session:
        try:
            session.add(vehicle_db)
            session.commit()
            return {"message": f"Vehicle with plate number: {plate_nb} added succesfully"}, True
        except IntegrityError:
            return {"error": f"Vehicle with plate number: {plate_nb} already exists or given plate number is invalid"}, False

# delete vehicle
def delete_vehicle(plate_nb: str):
    with db_session() as session:
        stmt = session.query(Vehicle).filter_by(vehicle_plate_number=plate_nb)
        if not stmt.first():
            return {"error": f"No vehicle with plate number: {plate_nb}"}, False
        try:
            stmt.delete()
            session.commit()
        except IntegrityError:
            return {"error": f"Vehicle with plate number: {plate_nb} has delete-restricted relationships"}, False
    return {"message": f"Vehicle with plate number: {plate_nb} deleted succesfully"}, True

# end course
def end_course(plate_nb: str, end_datetime: datetime):
    with db_session() as session:
        course_to_end = session.query(Course)\
            .where(Course.course_end_datetime == null())\
            .join(Vehicle, Course.fk_vehicle_course == Vehicle.id)\
            .where(Vehicle.vehicle_plate_number == plate_nb).first()
        if not course_to_end:
            return {"error": f"No active courses found for vehicle: {plate_nb}"}, False
        course_to_end.course_end_datetime = end_datetime
        session.commit()
    return {"message": f"Course of vehicle: {plate_nb} succesfully ended"}, True

# start new course
def start_course(plate_nb: str, start_datetime: datetime):
    with db_session() as session:
        vehicle = session.query(Vehicle).filter_by(vehicle_plate_number=plate_nb).first()
        if not vehicle:
            return {"error": f"No vehicle with plate number: {plate_nb} found"}, False
        vehicle_id = vehicle.id
        # check if vehicle has active courses
        active_courses = (
            session.query(Course)
                .join(Vehicle, Course.fk_vehicle_course == Vehicle.id)
                .where(Vehicle.vehicle_plate_number == plate_nb)
                .where(Course.course_end_datetime == null())
                .all()
        )
        if active_courses != []:
            return {"error": f"Vehicle with plate number: {plate_nb} already has active courses"}, False
        course_db = Course(
                fk_vehicle_course = vehicle_id,
                course_start_datetime = start_datetime
            )
        session.add(course_db)
        session.commit() 
    return {"message": f"New course for vehicle: {plate_nb} succesfully started"}, True   
##############################################################################################################################



##############################################################################################################################
# functionalities related to ticket validators:

# get all ticket validators
def get_all_ticket_validators():
    with db_session() as session:
        to_return = (
            session.query(TicketValidator)
                .options(joinedload(TicketValidator.vehicle))
                .all()
        )
        return {"ticket_validators": list(map(ticket_validator_data_to_dict, to_return))}, True

def ticket_validator_data_to_dict(validator: TicketValidator):
    return {
        "id": validator.id,
        "ipv4": validator.validator_ip_address,
        "vehicle_id": validator.vehicle.id,
        "vehicle_plate_nb": validator.vehicle.vehicle_plate_number
    }

# add ticket validator
def add_ticket_validator(ipv4: str, vehicle_plate_nb: str | None):
    with db_session() as session:
        vehicle_id = None
        if vehicle_plate_nb:
            vehicle = session.query(Vehicle).filter_by(vehicle_plate_number=vehicle_plate_nb).first()
            if not vehicle:
                return {"error": f"No vehicle with plate number: {vehicle_plate_nb} found"}, False
            vehicle_id = vehicle.id
        ticket_validator_db = TicketValidator(
            validator_ip_address = ipv4,
            fk_vehicle_validator = vehicle_id
        )
        try:
            session.add(ticket_validator_db)
            session.commit()
            return {"message": f"Ticket validator with ip address: {ipv4} succesfully added"}, True
        except IntegrityError:
            return {"error": f"Ticket validator with ip address: {ipv4} already exists or given ip address is invalid"}, False 

# delete ticket validator
def delete_ticket_validator(ipv4: str):
    with db_session() as session:
        stmt = session.query(TicketValidator).filter_by(validator_ip_address=ipv4)
        if not stmt.first():
            return {"error": f"No ticket validator with ip address: {ipv4}"}, False 
        stmt.delete()
        session.commit()
        return {"message": f"Ticket validator with ip address: {ipv4} succesfully deleted"}, True

# change validator's vehicle
def change_validators_vehicle(ipv4, new_vehicle_plate_nb: str | None):
    with db_session() as session:
        new_vehicle = session.query(Vehicle).filter_by(vehicle_plate_number=new_vehicle_plate_nb).first()
        if not new_vehicle:
            return {"error": f"No vehicle with plate number: {new_vehicle_plate_nb} found"}, False
        new_vehicle_id = new_vehicle.id
        to_update_validator = session.query(TicketValidator).filter_by(validator_ip_address=ipv4).first()
        if not to_update_validator:
            return {"error": f"No ticket validator with ip address: {ipv4}"}, False 
        to_update_validator.fk_vehicle_validator = new_vehicle_id
        session.commit()
        return {"message": f"Ticket validator with ip address: {ipv4} succesfully updated, new vehicle plate number: {new_vehicle_plate_nb}"}, True 
##############################################################################################################################



##############################################################################################################################
# functionalities related to price list:

# fetch price list
# fetch_price_list() - imported from common_functions

# add time ticket to offer
def add_time_ticket_to_offer(validity_period: int, price: float):
    time_ticket_price_db = TimeTicketPrice(
        time_ticket_validity_period = validity_period,
        time_ticket_amount = price
    )
    with db_session() as session:
        try:
            session.add(time_ticket_price_db)
            session.commit()
            return {"message": f"Time ticket type with validity period {validity_period} succesfully added"}, True
        except IntegrityError:
            return {"error": f"Time ticket type with validity period: {validity_period} already exists or given validity period is invalid"}, False

# edit time ticket in offer
def edit_time_ticket_in_offer(ticket_id: int, new_price: float):
    with db_session() as session:
        time_ticket_to_edit = session.query(TimeTicketPrice).filter_by(id=ticket_id).first()
        if not time_ticket_to_edit:
            return {"error": f"No time ticket type with id: {ticket_id}"}, False
        time_ticket_to_edit.time_ticket_amount = new_price
        session.commit()
        return {"message": f"Time ticket type with id: {ticket_id} succesfully updated, new price: {new_price}"}, True

# delete time ticket from offer
def delete_time_ticket_from_offer(ticket_id: int):
    with db_session() as session:
        stmt = session.query(TimeTicketPrice).filter_by(id=ticket_id)
        if not stmt.first():
            return {"error": f"No time ticket type with id: {ticket_id}"}, False
        stmt.delete()
        session.commit()
        return {"message": f"Time ticket type with id: {ticket_id} succesfully deleted"}, True

# edit single-use ticket in offer
def edit_course_ticket_in_offer(ticket_id: int, new_price: float):
    with db_session() as session:
        course_ticket_to_edit = session.query(CourseTicketPrice).filter_by(id=ticket_id).first()
        if not course_ticket_to_edit:
            return {"error": f"No course ticket type with id: {ticket_id}"}, False
        course_ticket_to_edit.course_ticket_amount = new_price
        session.commit()
        return {"message": f"Course ticket type with id: {ticket_id} succesfully updated, new price: {new_price}"}, True
##############################################################################################################################



##############################################################################################################################
# functionalities related to RFID cards:

# get all RFID cards
def get_all_RFID_cards():
    with db_session() as session:
        to_return = session.query(Card).all()
        return {"cards": list(map(card_to_dict, to_return))}, True

def card_to_dict(card: Card):
    return {
        "id": card.id,
        "RFID": card.card_RFID,
        "balance": card.card_balance
    }

# add new RFID card
def add_RFID_card(RFID: str):
    card_db = Card(
            card_RFID = RFID
        )
    with db_session() as session:
        try:
            session.add(card_db)
            session.commit()
            return {"message": f"Card with RFID: {RFID} added succesfully"}, True
        except IntegrityError:
            return {"error": f"Card with RFID: {RFID} already exists or given RFID is invalid"}, False

# delete RFID card
def delete_RFID_card(RFID: str):
    with db_session() as session:
        stmt = session.query(Card).filter_by(card_RFID=RFID)
        if not stmt.first():
            return {"error": f"No card with RFID: {RFID}"}, False
        try:
            stmt.delete()
            session.commit()
        except IntegrityError:
            return {"error": f"Card with RFID: {RFID} has delete-restricted relationships"}, False
        return {"message": f"Card with RFID: {RFID} deleted succesfully"}, True
