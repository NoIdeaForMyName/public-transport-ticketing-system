# tap_card_view.py
from datetime import datetime

from .BaseView import BaseView
from .Actions import Action
from user_interface.image_playground import (
    generate_static_icon_interface,
    generate_dynamic_icon_interface,
    prepare_draw_object
)

from user_interface.utilities.constants import (
    TAP_CARD_TITLE, CARD_ICON_PATH, CARDS_ICON_SIZE,
    CHARGE_CARD_SUCCESS_TITLE, TICK_MARK_PATH,
    X_MARK_PATH, BOUGHT_SUCCESSFULLY_TITLE, NOT_BOUGHT_TITLE,
    YOUR_TICKET_TITLE, HAPPY_FACE_PATH, ANGRY_FACE_PATH, MARKS_SIZE, CARD_REJECTED_TITLE
)

from user_interface.functions_mockups import (
    buy_course_ticket, recharge_card, buy_time_ticket, check_active_tickets
)


class TapCardView(BaseView):
    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        self.display_communicate = False
        self.transaction_succeeded = False
        self.message_dict = {}

    def render(self):
        draw, result = prepare_draw_object('utilities/background.png')

        if self.display_communicate:
            if self.mode in ['5zl', '10zl', '50zl']:
                if self.transaction_succeeded:
                    generate_static_icon_interface(
                        draw, result, CHARGE_CARD_SUCCESS_TITLE,
                        TICK_MARK_PATH, MARKS_SIZE
                    )
                else:
                    generate_static_icon_interface(
                        draw, result, CARD_REJECTED_TITLE,
                        X_MARK_PATH, MARKS_SIZE
                    )

            elif self.mode in ['15min', '30min', '1h', 'course_ticket']:
                if self.transaction_succeeded:
                    generate_static_icon_interface(
                        draw, result, BOUGHT_SUCCESSFULLY_TITLE,
                        TICK_MARK_PATH, MARKS_SIZE
                    )
                else:
                    generate_static_icon_interface(
                        draw, result, NOT_BOUGHT_TITLE,
                        X_MARK_PATH, MARKS_SIZE
                    )

            elif self.mode == 'check_ticket':
                text = ''
                if self.transaction_succeeded:
                    if len(self.message_dict.get("active_time_tickets", [])) > 0:
                        text = self.message_dict["active_time_tickets"][0]
                    elif len(self.message_dict.get("active_course_tickets", [])) > 0:
                        text = self.message_dict["active_course_tickets"][0]

                    generate_dynamic_icon_interface(
                        draw, result, YOUR_TICKET_TITLE,
                        text, HAPPY_FACE_PATH
                    )
                else:
                    generate_dynamic_icon_interface(
                        draw, result, YOUR_TICKET_TITLE,
                        text, ANGRY_FACE_PATH
                    )

        else:
            generate_static_icon_interface(draw, result, TAP_CARD_TITLE, CARD_ICON_PATH, CARDS_ICON_SIZE)

        return result

    def handle_input(self, action):
        if action == Action.CARD_TAPPED:
            rfid = '123'
            ip = '192.168.0.100'

            if self.mode == 'course_ticket':
                _, success = buy_course_ticket(rfid, ip)
                self.transaction_succeeded = success

            elif self.mode == '5zl':
                _, success = recharge_card(rfid, 5.0)
                self.transaction_succeeded = success

            elif self.mode == '10zl':
                _, success = recharge_card(rfid, 10.0)
                self.transaction_succeeded = success

            elif self.mode == '50zl':
                _, success = recharge_card(rfid, 50.0)
                self.transaction_succeeded = success

            elif self.mode == '15min':
                _, success = buy_time_ticket(rfid, datetime.now(), 1)
                self.transaction_succeeded = success

            elif self.mode == '30min':
                _, success = buy_time_ticket(rfid, datetime.now(), 2)
                self.transaction_succeeded = success

            elif self.mode == '1h':
                _, success = buy_time_ticket(rfid, datetime.now(), 3)
                self.transaction_succeeded = success

            elif self.mode == 'check_ticket':
                self.message_dict, success = check_active_tickets(rfid)
                self.transaction_succeeded = success

            self.display_communicate = True

        return self.__class__, None