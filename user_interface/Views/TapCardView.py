# tap_card_view.py
from datetime import *

# from functions_mockups import (
#     buy_course_ticket, recharge_card, buy_time_ticket, check_active_tickets
# )
from image_playground import (
    generate_static_icon_interface,
    prepare_draw_object
)
from utilities.constants import (
    TAP_CARD_TITLE, CARD_ICON_PATH, CARDS_ICON_SIZE,
    BACKGROUND_IMAGE_PATH
)
from .Actions import Action
from .BaseView import BaseView
from .TransactionStatusView import TransactionStatusView

import socket
import Views.database_communication as database_communication

class TapCardView(BaseView):
    def __init__(self, manager, mode):
        super().__init__()
        self.manager = manager
        self.mode = mode

    def render(self):
        draw, result = prepare_draw_object(BACKGROUND_IMAGE_PATH)
        generate_static_icon_interface(draw, result, TAP_CARD_TITLE, CARD_ICON_PATH, CARDS_ICON_SIZE)
        return result

    def handle_input(self, action):
        if action == Action.RED_PRESS or action == Action.RED_LONG_PRESS:
            from .MainMenuView import MainMenuView
            return MainMenuView, None

        if action == Action.CARD_TAPPED:
            rfid = self.manager.last_card_id or "UNKNOWN"
            ip = "10.108.33.121"  ## HOW TO GET THIS??????????

            # ip = socket.gethostbyname(socket.gethostname())
            success = False
            extra_text = ""
            message = ""

            if self.mode == 'course_ticket':
                message = "Bilet jednorazowy"
                _, success = database_communication.buy_course_ticket(rfid, ip)
            elif self.mode == '5zl':
                message = "Doładowanie: 5zł"
                _, success = database_communication.recharge_card(rfid, 5.0)
            elif self.mode == '10zl':
                message = "Doładowanie: 10zł"
                _, success = database_communication.recharge_card(rfid, 10.0)
            elif self.mode == '50zl':
                message = "Doładowanie: 50zł"
                _, success = database_communication.recharge_card(rfid, 50.0)
            elif self.mode == '15min':
                message = "Bilet 15min"
                price_dict = database_communication.fetch_price_list()
                print(price_dict)

                id_ticket = 1
                for dict_tmp in price_dict[0]['time_ticket_prices']:
                    if dict_tmp["validity_period"] == 15:
                        id_ticket = dict_tmp["id"]

                # id_ticket = price_dict['time_ticket_prices'][1]['id']
                _, success = database_communication.buy_time_ticket(rfid, datetime.now(), id_ticket)
            elif self.mode == '30min':
                message = "Bilet 30min"
                price_dict = database_communication.fetch_price_list()

                id_ticket = 1
                for dict_tmp in price_dict[0]['time_ticket_prices']:
                    if dict_tmp["validity_period"] == 30:
                        id_ticket = dict_tmp["id"]

                # id_ticket = price_dict['time_ticket_prices'][0]['id']
                _, success = database_communication.buy_time_ticket(rfid, datetime.now(), id_ticket)
            elif self.mode == '1h':
                message = "Bilet 1h"
                price_dict = database_communication.fetch_price_list()
                # id_ticket = price_dict['time_ticket_prices'][2]['id']

                id_ticket = 1
                for dict_tmp in price_dict[0]['time_ticket_prices']:
                    if dict_tmp["validity_period"] == 60:
                        id_ticket = dict_tmp["id"]
                
                _, success = database_communication.buy_time_ticket(rfid, datetime.now(), id_ticket)
            elif self.mode == 'check_ticket':
                message = "Sprawdzenie biletu"
                data_dict, success = database_communication.check_active_tickets(rfid)
                if success:  ## will be changed
                    if data_dict.get("active_time_tickets"):
                        time_left = (datetime.now() - data_dict["active_time_tickets"]['validity_period']).total_seconds()
                        minutes, seconds = divmod(time_left, 60)
                        extra_text = f"Aktywny bilet czasowy pozostalo: {minutes} minut {seconds} sekund"
                    elif data_dict.get("active_course_tickets"):
                        extra_text = "Aktywny bilet jednorazowy "

            param = {
                "message": message,
                "success": success,
                "extra_text": extra_text
            }
            return TransactionStatusView, param

        return self.__class__, None
