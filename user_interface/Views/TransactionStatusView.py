import time

from .BaseView import BaseView
from .Actions import Action
from user_interface.image_playground import (
    prepare_draw_object,
    generate_static_icon_interface,
    generate_dynamic_icon_interface
)
from user_interface.utilities.constants import (
    HAPPY_FACE_PATH, ANGRY_FACE_PATH,
    TICK_MARK_PATH, X_MARK_PATH,
    CHARGE_CARD_SUCCESS_TITLE, NOT_BOUGHT_TITLE, BACKGROUND_IMAGE_PATH, CARD_REJECTED_TITLE, CHARGE_CARD_SUCCESS_TITLE,
    MARKS_SIZE, BOUGHT_SUCCESSFULLY_TITLE, NOT_BOUGHT_TITLE, YOUR_TICKET_TITLE, NOT_ACTIVE_TEXT
)


class TransactionStatusView(BaseView):
    def __init__(self, manager, message, success, extra_text=""):
        super().__init__()
        self.manager = manager
        self.message = message
        self.success = success
        self.extra_text = extra_text
        self.start_time = time.time()

    def render(self):
        draw, result = prepare_draw_object(BACKGROUND_IMAGE_PATH)

        if self.message in ["Doładowanie: 5zł", "Doładowanie: 10zł", "Doładowanie: 50zł"]:
            icon = TICK_MARK_PATH if self.success else X_MARK_PATH
            title = CHARGE_CARD_SUCCESS_TITLE if self.success else CARD_REJECTED_TITLE
            generate_static_icon_interface(draw, result, title, icon, MARKS_SIZE)

        elif self.message in ["Bilet 15min", "Bilet 30min", "Bilet 1h", "Bilet jednorazowy"]:
            icon = TICK_MARK_PATH if self.success else X_MARK_PATH
            title = BOUGHT_SUCCESSFULLY_TITLE if self.success else NOT_BOUGHT_TITLE
            generate_static_icon_interface(draw, result, title, icon, MARKS_SIZE)

        elif self.message == "Sprawdzenie biletu":
            icon = HAPPY_FACE_PATH if self.success else ANGRY_FACE_PATH
            if self.success:
                generate_dynamic_icon_interface(draw, result, YOUR_TICKET_TITLE, self.extra_text, icon)
            else:
                generate_dynamic_icon_interface(draw, result, YOUR_TICKET_TITLE, NOT_ACTIVE_TEXT, icon)



        return result

    def handle_input(self, action):
        elapsed = time.time() - self.start_time
        if elapsed >= 2:
            from .MainMenuView import MainMenuView
            return MainMenuView, None

        if action == Action.RED_PRESS or action == Action.RED_LONG_PRESS:
            from .MainMenuView import MainMenuView
            return MainMenuView, None

        return self.__class__, None

