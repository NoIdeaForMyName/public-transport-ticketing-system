from database_communication.common_functions import *

'''
pobierz_dane_wszystkich_pojazdow(); -> json - id, rejestracja, id obecnego kursu(opcjonalnie)
dodaj_pojazd(rejestracja); -> udalo sie lub nie (np. taki pojazd juz istnieje)
usun_pojazd(rejestracja); -> udalo sie lub nie
zakoncz_kurs(rejestracja, czas_zakonczenia); -> udalo sie lub nie (np. pojazd nie ma aktywnych kursow)
rozpocznij_kurs(rejestracja, czas_rozpoczecia); -> udalo sie lub nie

pobierz_dane_wszystkich_kasownikow(); -> json - id, ipv4, {dane_pojazdu: id, rejestracja}
dodaj_kasownik(ipv4, rejestracja_pojazdu(opcjonalnie)); -> udalo sie lub nie (np. taki kasownik juz istnieje)
usun_kasownik(ipv4); -> udalo sie lub nie
zmien_pojazd_kasownika(ipv4, rejestracja_pojazdu(opcjonalnie)); -> udalo sie lub nie

pobierz_cennik(); -> struktura jak wyzej
dodaj_bilet_czasowy(czas_waznosci, cena); -> udalo sie lub nie (np. istnieje juz bilet o danym czasie waznosci)
edytuj_bilet_czasowy(id_biletu, cena); -> udalo sie lub nie # mozna edytowac tylko cene, bo jego czas waznosci jest kluczem kandydujacym
usun_bilet_czasowy(id_biletu); -> udalo sie lub nie
edytuj_bilet_jednorazowy(id_biletu, cena); -> udalo sie lub nie
'''

##############################################################################################################################
#functionalities related to vehicles:

# fetch all vehicles data
def fetch_all_vehicles():
    with db_session() as session:
        active_courses = select(Course).where(Course.course_end_datetime == null()).subquery()
        return (
            session.query(
                Vehicle,
                func.min(active_courses.c.id).label("Courses_id") # could be any function (min, max, first etc.) because it will always be only one Course entry available
            )
            .outerjoin(active_courses, Vehicle.id == active_courses.c.fk_vehicle_course) # left join
            .group_by(Vehicle)
            .all()
        )
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
        session.add(vehicle_db)
        session.commit()

# delete vehicle
def delete_vehicle(plate_nb: str):
    with db_session() as session:
        session.query(Vehicle).filter_by(vehicle_plate_number=plate_nb).delete()
        session.commit()

# end course
def end_course(plate_nb: str, end_datetime: datetime):
    with db_session() as session:
        course_to_end = session.query(Course)\
            .where(Course.course_end_datetime == null())\
            .join(Vehicle, Course.fk_vehicle_course == Vehicle.id)\
            .where(Vehicle.vehicle_plate_number == plate_nb).first()
        course_to_end.course_end_datetime = end_datetime
        session.commit()

# start new course
def start_course(plate_nb: str, start_datetime: datetime):
    with db_session() as session:
        course_db = Course(
                fk_vehicle_course = session.query(Vehicle).filter_by(vehicle_plate_number=plate_nb).first().id,
                course_start_datetime = start_datetime
            )
        session.add(course_db)
        session.commit()     
##############################################################################################################################



##############################################################################################################################
# functionalities related to ticket validators:

# get all ticket validators
def get_all_ticket_validators():
    with db_session() as session:
        return (
            session.query(TicketValidator)
                .options(joinedload(TicketValidator.vehicle))
                .all()
        )

# add ticket validator
def add_ticket_validator(ipv4: str, vehicle_plate_nb: str | None):
    with db_session() as session:
        vehicle_id = None
        if vehicle_plate_nb:
            vehicle_id = session.query(Vehicle).filter_by(vehicle_plate_number=vehicle_plate_nb).first().id
        ticket_validator_db = TicketValidator(
            validator_ip_address = ipv4,
            fk_vehicle_validator = vehicle_id
        )
        session.add(ticket_validator_db)
        session.commit()

# delete ticket validator
def delete_ticket_validator(ipv4: str):
    with db_session() as session:
        session.query(TicketValidator).filter_by(validator_ip_address=ipv4).delete()
        session.commit()

# change validator's vehicle
def change_validators_vehicle(ipv4, new_vehicle_plate_nb: str | None):
    with db_session() as session:
        new_vehicle_id = session.query(Vehicle).filter_by(vehicle_plate_number=new_vehicle_plate_nb).first().id
        to_update_validator = session.query(TicketValidator).filter_by(validator_ip_address=ipv4).first()
        to_update_validator.fk_vehicle_validator = new_vehicle_id
        session.commit()
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
        session.add(time_ticket_price_db)
        session.commit()

# edit time ticket in offer
def edit_time_ticket_in_offer(ticket_id: int, new_price: float):
    with db_session() as session:
        session.query(TimeTicketPrice).filter_by(id=ticket_id).first().time_ticket_amount = new_price
        session.commit()

# delete time ticket from offer
def delete_time_ticket_from_offer(ticket_id: int):
    with db_session() as session:
        session.query(TimeTicketPrice).filter_by(id=ticket_id).delete()
        session.commit()

# edit single-use ticket in offer
def edit_course_ticket_in_offer(ticket_id: int, new_price: float):
    with db_session() as session:
        session.query(CourseTicketPrice).filter_by(id=ticket_id).first().course_ticket_amount = new_price
        session.commit()

##############################################################################################################################



##############################################################################################################################
# functionalities related to RFID cards:

# get all RFID cards
def get_all_RFID_cards():
    with db_session() as session:
        return session.query(Card).all()

# add new RFID card
def add_RFID_card(RFID: str):
    card_db = Card(
            card_RFID = RFID
        )
    with db_session() as session:
        session.add(card_db)
        session.commit()

# delete RFID card
def delete_RFID_card(RFID: str):
    with db_session() as session:
        session.query(Card).filter_by(card_RFID=RFID).delete()
        session.commit()
