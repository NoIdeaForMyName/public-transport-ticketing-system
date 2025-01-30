# tap_card_view.py
from datetime import datetime

from .BaseView import BaseView
from .Actions import Action
from .TransactionStatusView import TransactionStatusView
from user_interface.image_playground import (
    generate_static_icon_interface,
    generate_dynamic_icon_interface,
    prepare_draw_object
)

from user_interface.utilities.constants import (
    TAP_CARD_TITLE, CARD_ICON_PATH, CARDS_ICON_SIZE,
    CHARGE_CARD_SUCCESS_TITLE, TICK_MARK_PATH,
    X_MARK_PATH, BOUGHT_SUCCESSFULLY_TITLE, NOT_BOUGHT_TITLE,
    YOUR_TICKET_TITLE, HAPPY_FACE_PATH, ANGRY_FACE_PATH, MARKS_SIZE, CARD_REJECTED_TITLE, BACKGROUND_IMAGE_PATH
)

from user_interface.functions_mockups import (
    buy_course_ticket, recharge_card, buy_time_ticket, check_active_tickets
)


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
            ip = "192.168.0.100" ## HOW TO GET THIS??????????

            success = False
            extra_text = ""
            message = ""

            if self.mode == 'course_ticket':
                message = "Bilet jednorazowy"
                _, success = buy_course_ticket(rfid, ip)
            elif self.mode == '5zl':
                message = "Doładowanie: 5zł"
                _, success = recharge_card(rfid, 5.0)
            elif self.mode == '10zl':
                message = "Doładowanie: 10zł"
                _, success = recharge_card(rfid, 10.0)
            elif self.mode == '50zl':
                message = "Doładowanie: 50zł"
                _, success = recharge_card(rfid, 50.0)
            elif self.mode == '15min':
                message = "Bilet 15min"
                _, success = buy_time_ticket(rfid, datetime.now(), 1)
            elif self.mode == '30min':
                message = "Bilet 30min"
                _, success = buy_time_ticket(rfid, datetime.now(), 2)
            elif self.mode == '1h':
                message = "Bilet 1h"
                _, success = buy_time_ticket(rfid, datetime.now(), 3)
            elif self.mode == 'check_ticket':
                message = "Sprawdzenie biletu"
                data_dict, success = check_active_tickets(rfid)
                if success: ## will be changed
                    if data_dict.get("active_time_tickets"):
                        extra_text = "Aktywny bilet czasowy pozostalo: " + data_dict["active_time_tickets"][0]
                    elif data_dict.get("active_course_tickets"):
                        extra_text = "Aktywny bilet jednorazowy "

            param = {
                "message": message,
                "success": success,
                "extra_text": extra_text
            }
            return TransactionStatusView, param

        return self.__class__, None