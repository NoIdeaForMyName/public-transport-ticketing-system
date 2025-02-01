from .BaseView import BaseView
from .Actions import Action
from image_playground import generate_radio_button_interface, prepare_draw_object
from utilities.constants import VALIDITY_TIME_OPTIONS, VALIDITY_TIME_TITLE, BACKGROUND_IMAGE_PATH
from .TapCardView import TapCardView


class ValidityTimeView(BaseView):
    def __init__(self, manager, selected_option=1):
        super().__init__()
        self.manager = manager
        self.selected_option = selected_option
        self.title = VALIDITY_TIME_TITLE
        self.options = VALIDITY_TIME_OPTIONS

    def render(self):
        draw, result = prepare_draw_object(BACKGROUND_IMAGE_PATH)
        generate_radio_button_interface(draw, result, self.title, self.options, self.selected_option)
        return result

    def handle_input(self, action):
        reload = False
        if action == Action.GREEN_PRESS:
            if self.selected_option == 1:
                return TapCardView, {"mode": "15min"}
            elif self.selected_option == 2:
                return TapCardView, {"mode": "30min"}
            elif self.selected_option == 3:
                return TapCardView, {"mode": "1h"}

        elif action == Action.RED_PRESS:
            reload = True
            if self.selected_option < 3:
                self.selected_option += 1
            else:
                self.selected_option = 1

        elif action == Action.RED_LONG_PRESS:
            from .TicketChoiceView import TicketChoiceView
            return TicketChoiceView, None

        return self.__class__, reload
