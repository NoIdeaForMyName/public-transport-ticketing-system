from .BaseView import BaseView
from .Actions import Action
from user_interface.image_playground import generate_radio_button_interface, prepare_draw_object
from user_interface.utilities.constants import VALIDITY_TIME_OPTIONS, VALIDITY_TIME_TITLE
from .TapCardView import TapCardView


class ValidityTimeView(BaseView):
    def __init__(self, title=VALIDITY_TIME_TITLE, options=VALIDITY_TIME_OPTIONS, selected_option=1):
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
                return TapCardView, '15min'
            elif self.selected_option == 2:
                return TapCardView, '30min'
            elif self.selected_option == 3:
                return TapCardView, '1h'

        elif action == Action.RED_PRESS:
            if self.selected_option < 3:
                self.selected_option += 1
            else:
                self.selected_option = 1

        elif action == Action.RED_LONG_PRESS:
            from .TicketChoiceView import TicketChoiceView
            return TicketChoiceView, ''

        return self.__class__, None
