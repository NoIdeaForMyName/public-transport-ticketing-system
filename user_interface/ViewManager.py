# view_manager.py

import time
from Views.Actions import Action
from Views.TapCardView import TapCardView as TapCardView
from user_interface.Views.MainMenuView import MainMenuView


class ViewManager:
    def __init__(self, initial_view, display=None, oled_manager_fun=None):
        self.current_view = initial_view
        self.display = display
        self.oled_manager_fun = oled_manager_fun

    def start(self):
        while True:
            image = self.current_view.render()

            if self.oled_manager_fun:
                self.oled_manager_fun(self.display, image)
            else:
                image.show()

            print(isinstance(self.current_view, TapCardView))


            print(type(self.current_view))
            if isinstance(self.current_view, TapCardView) and self.current_view.display_communicate:
                print("[ViewManager] Transakcja zakończona. Czekam 2 sek i wracam do menu głównego.")
                time.sleep(2)

                self.current_view.display_communicate = False

                self.current_view = MainMenuView()

                continue

            action = self.read_action_mock()
            if action == Action.EXIT:
                print("Exiting application...")
                break

            if action:
                next_view_class, param = self.current_view.handle_input(action)

                if next_view_class != self.current_view.__class__:
                    if param:
                        self.current_view = next_view_class(param)
                    else:
                        self.current_view = next_view_class()

    def read_action_mock(self):
        """
        Funkcja mockująca odczyt akcji z klawiatury:
        (G)reen, (R)ed, (RR)ed-long, (C)ard, (Q)uit
        """
        user_input = input("(G)reen, (R)ed, (RR)ed-long, (C)ard, (Q)uit? ").strip().lower()

        if user_input == 'g':
            return Action.GREEN_PRESS
        elif user_input == 'r':
            return Action.RED_PRESS
        elif user_input == 'rr':
            return Action.RED_LONG_PRESS
        elif user_input == 'c':
            return Action.CARD_TAPPED
        elif user_input == 'q':
            return Action.EXIT
        else:
            return None
