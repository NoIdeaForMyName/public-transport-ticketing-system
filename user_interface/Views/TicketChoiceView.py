# ticket_choice_view.py
from .BaseView import BaseView
from .Actions import Action
from user_interface.image_playground import generate_radio_button_interface, prepare_draw_object
from user_interface.utilities.constants import TICKET_CHOICE_OPTIONS, TICKET_CHOICE_TITLE
from .TapCardView import TapCardView
from .ValidityTimeView import ValidityTimeView


class TicketChoiceView(BaseView):
    def __init__(self, title=TICKET_CHOICE_TITLE, options=TICKET_CHOICE_OPTIONS, selected_option=1):
        super().__init__()
        self.selected_option = selected_option
        self.title = title
        self.options = options

    def render(self):
        draw, result = prepare_draw_object('utilities/background.png')
        generate_radio_button_interface(draw, result, self.title, self.options, self.selected_option)
        return result

    def handle_input(self, action):
        if action == Action.GREEN_PRESS:
            if self.selected_option == 1:
                return TapCardView, 'course_ticket'
            elif self.selected_option == 2:
                return ValidityTimeView, ''

        elif action == Action.RED_PRESS:
            if self.selected_option < 2:
                self.selected_option += 1
            else:
                self.selected_option = 1

        elif action == Action.RED_LONG_PRESS:
            from .MainMenuView import MainMenuView
            return MainMenuView, ''

        return self.__class__, None
