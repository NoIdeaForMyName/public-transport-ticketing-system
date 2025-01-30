from .BaseView import BaseView
from .Actions import Action
from user_interface.image_playground import generate_radio_button_interface, prepare_draw_object
from user_interface.utilities.constants import MAIN_MENU_OPTIONS, MAIN_MENU_TITLE, BACKGROUND_IMAGE_PATH
from .TicketChoiceView import TicketChoiceView
from .ChargeCardView import ChargeCardView
from .TapCardView import TapCardView


class MainMenuView(BaseView):
    def __init__(self, manager, selected_option=1):
        super().__init__()
        self.manager = manager
        self.selected_option = selected_option
        self.title = MAIN_MENU_TITLE
        self.options = MAIN_MENU_OPTIONS

    def render(self):
        draw, result = prepare_draw_object(BACKGROUND_IMAGE_PATH)
        generate_radio_button_interface(draw, result, self.title, self.options, self.selected_option)
        return result

    def handle_input(self, action):
        if action == Action.GREEN_PRESS:
            if self.selected_option == 1:
                return TicketChoiceView, None
            elif self.selected_option == 2:
                return TapCardView, {"mode": "check_ticket"}
            elif self.selected_option == 3:
                return ChargeCardView, None

        elif action == Action.RED_PRESS:
            if self.selected_option < 3:
                self.selected_option += 1
            else:
                self.selected_option = 1

        return self.__class__, None
