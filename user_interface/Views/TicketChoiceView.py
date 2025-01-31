from .BaseView import BaseView
from .Actions import Action
from user_interface.image_playground import generate_radio_button_interface, prepare_draw_object
from user_interface.utilities.constants import TICKET_CHOICE_OPTIONS, TICKET_CHOICE_TITLE, BACKGROUND_IMAGE_PATH
from .TapCardView import TapCardView
from .ValidityTimeView import ValidityTimeView


class TicketChoiceView(BaseView):
    def __init__(self, manager, selected_option=1):
        super().__init__()
        self.manager = manager
        self.selected_option = selected_option
        self.title = TICKET_CHOICE_TITLE
        self.options = TICKET_CHOICE_OPTIONS

    def render(self):
        draw, result = prepare_draw_object(BACKGROUND_IMAGE_PATH)
        generate_radio_button_interface(draw, result, self.title, self.options, self.selected_option)
        return result

    def handle_input(self, action):
        if action == Action.GREEN_PRESS:
            if self.selected_option == 1:
                return TapCardView, {"mode": "course_ticket"}
            elif self.selected_option == 2:
                return ValidityTimeView, None

        elif action == Action.RED_PRESS:
            if self.selected_option < 2:
                self.selected_option += 1
            else:
                self.selected_option = 1

        elif action == Action.RED_LONG_PRESS:
            from .MainMenuView import MainMenuView
            return MainMenuView, None

        return self.__class__, None
