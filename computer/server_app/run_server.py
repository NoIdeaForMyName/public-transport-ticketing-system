# main python file for running server app
from database_communication import *

import json

#initialize_session("./../database/public_transport_ticketing_system.db")
specify_db_path("./../database/public_transport_ticketing_system.db")

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)





# ADMINISTRATOR TESTING...

# TICKET PRICES TESTS

#add_time_ticket_to_offer(30, 2.)
#edit_time_ticket_in_offer(1, 5.)
#delete_time_ticket_from_offer(1)
#edit_course_ticket_in_offer(1, 4.5)

# time_ticket_price_list_db = fetch_price_list()['time_ticket_prices']
# for time_ticket_price_db in time_ticket_price_list_db:
#     print(json.dumps(time_ticket_price_db, cls=AlchemyEncoder))

# single_ticket_price_db = fetch_price_list()['course_ticket_price']
# print(json.dumps(single_ticket_price_db, cls=AlchemyEncoder))


# VEHICLES MANAGEMENT TEST

#add_vehicle("JP20000")
#delete_vehicle("JP10000")
#end_course("JP10000", datetime.now())
#start_course("JP10000", datetime.now())

# all_vehicles = fetch_all_vehicles()
# print(all_vehicles)
# for vehicle in all_vehicles:
#     print(vehicle[0].id, vehicle[0].vehicle_plate_number, vehicle[1])



# TICKET VALIDATORS MANAGEMENT TEST

#add_ticket_validator("192.168.0.2", "JP10000")
#delete_ticket_validator("192.168.0.2")
#change_validators_vehicle("192.168.0.2", "JP10000")

# all_validators = get_all_ticket_validators()
# print(all_validators)
# for validator in all_validators:
#     print(validator.id, validator.validator_ip_address, *(validator.vehicle.id, validator.vehicle.vehicle_plate_number) if validator.vehicle else None)



# RFID CARD MANAGEMENT TEST

#add_RFID_card("123456789012")
#delete_RFID_card("123456789012")

# all_cards = get_all_RFID_cards()
# print(all_cards)
# for card in all_cards:
#     print(card.id, card.card_RFID, card.card_balance)



# CLIENT TESTING...
# TODO

