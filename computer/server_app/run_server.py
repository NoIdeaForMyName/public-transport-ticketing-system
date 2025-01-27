# main python file for running server app
from database_communication import *


#initialize_session("./../database/public_transport_ticketing_system.db")
specify_db_path("./../database/public_transport_ticketing_system.db")

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)





# ADMINISTRATOR TESTING...

# TICKET PRICES TESTS

#print(add_time_ticket_to_offer(30, 2.))
#print(edit_time_ticket_in_offer(1, 5.))
#print(delete_time_ticket_from_offer(1))
#print(edit_course_ticket_in_offer(1, 4.5))

# time_ticket_price_list_db = fetch_price_list()[0]['time_ticket_prices']
# for time_ticket_price_db in time_ticket_price_list_db:
#     print(time_ticket_price_db)

# single_ticket_price_db = fetch_price_list()[0]['course_ticket_price']
# print(single_ticket_price_db)


# VEHICLES MANAGEMENT TEST

#print(add_vehicle("JP20000"))
#print(delete_vehicle("JP10000"))
#print(end_course("JP10000", datetime.now()))
#print(start_course("JP10000", datetime.now()))

# all_vehicles, _ = fetch_all_vehicles()
# print(all_vehicles)
# for vehicle in all_vehicles['vehicle_data']:
#     print(vehicle)



# TICKET VALIDATORS MANAGEMENT TEST

#print(add_ticket_validator("192.168.0.2", "JP10000"))
#print(delete_ticket_validator("192.168.0.2"))
#print(change_validators_vehicle("192.168.0.2", "JP10000"))

# all_validators, _ = get_all_ticket_validators()
# print(all_validators)
# for validator in all_validators['ticket_validators']:
#     print(validator)



# RFID CARD MANAGEMENT TEST

#print(add_RFID_card("123456789012"))
#print(delete_RFID_card("123456789012"))

# all_cards, _ = get_all_RFID_cards()
# print(all_cards)
# for card in all_cards['cards']:
#     print(card)



# CLIENT TESTING...

# you can buy only one course ticket but you can buy multiple time tickets

#print(buy_course_ticket("123456789012", "192.168.0.2"))
#print(recharge_card("123456789012", 25))
#print(buy_time_ticket("123456789012", datetime.now(), 1))
#print(buy_course_ticket("123456789012", "192.168.0.2"))

# active_tickets, _ = check_active_tickets("123456789012")
# print(active_tickets)
# print("Active time tickets:")
# for ticket in active_tickets['active_time_tickets']:
#     print(ticket)
# print("Active course tickets:")
# for ticket in active_tickets['active_course_tickets']:
#     print(ticket)

#print(check_balance("123456789012"))
