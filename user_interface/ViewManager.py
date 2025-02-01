import time
from Views.Actions import Action
from Views.TapCardView import TapCardView as TapCardView
from Views.MainMenuView import MainMenuView
from rasberryPI.oled_functionalities import oled_manager, init_oled

try:
    import RPi.GPIO as GPIO
    from mfrc522 import MFRC522
except ImportError:
    GPIO = None
    MFRC522 = None


class ViewManager:
    def __init__(self, initial_view, device_mode="mock"):
        self.current_view = initial_view
        self.device_mode = device_mode
        self.display = None
        self.oled_manager_fun = None

        self.red_is_pressed = False
        self.red_press_start = 0.0

        self.green_is_pressed = False

        self.reader = None
        self.card_already_detected = False
        self.last_card_id = None

        if self.device_mode == "real":
            self.setup_real_hardware()

    def setup_real_hardware(self):
        from config import buttonRed, buttonGreen
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(buttonRed, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(buttonGreen, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.reader = MFRC522()

        self.display = init_oled()
        self.oled_manager_fun = oled_manager

        print("[ViewManager] Real hardware setup complete.")

    def start(self):
        image = self.current_view.render()    
        if self.oled_manager_fun:
            self.oled_manager_fun(self.display, image)
        else:
            image.show()
        while True:
        
            if self.device_mode == "real":
                action = self._poll_real_hardware()
            else:
                action = self._poll_mock_input()

            if action is not None:
                next_view_class, param = self.current_view.handle_input(action)
                print(param) 
                if next_view_class != self.current_view.__class__:
                    self._switch_view(next_view_class, param)
                    image = self.current_view.render()    
                    if self.oled_manager_fun:
                        self.oled_manager_fun(self.display, image)
                    else:
                        image.show()
                       
                elif param:
                    image = self.current_view.render()    
                    if self.oled_manager_fun:
                        self.oled_manager_fun(self.display, image)
                    else:
                        image.show()

            
            time.sleep(0.01)

    def _switch_view(self, next_view_class, param):
        if isinstance(param, dict):
            self.current_view = next_view_class(self, **param)
        elif param is not None:
            self.current_view = next_view_class(self, param)
        else:
            self.current_view = next_view_class(self)

        # image = self.current_view.render()    
        # if self.oled_manager_fun:
        #     self.oled_manager_fun(self.display, image)
        # else:
        #     image.show()

    # ----------------- MOCK -------------------
    def _poll_mock_input(self):
        user_input = input("(G)reen, (R)ed, (RR)ed-long, (C)ard, (Q)uit? ").strip().lower()
        if user_input == 'g':
            return Action.GREEN_PRESS
        elif user_input == 'r':
            return Action.RED_PRESS
        elif user_input == 'rr':
            return Action.RED_LONG_PRESS
        elif user_input == 'c':
            self.last_card_id = "MOCK_123"
            return Action.CARD_TAPPED

        return None

    # ----------------- REAL -------------------
    def _poll_real_hardware(self):
        action = self._check_buttons()
        if action:
            return action
        action = self._check_rfid()
        return action

    def _check_buttons(self):
        from config import buttonRed, buttonGreen
        now = time.time()
        action = None

        red_state = (GPIO.input(buttonRed) == GPIO.LOW)
        if red_state and not self.red_is_pressed:
            self.red_is_pressed = True
            self.red_press_start = now
        elif not red_state and self.red_is_pressed:
            press_duration = now - self.red_press_start
            self.red_is_pressed = False
            if press_duration > 2.0:
                action = Action.RED_LONG_PRESS
            else:
                action = Action.RED_PRESS

        green_state = (GPIO.input(buttonGreen) == GPIO.LOW)
        if green_state and not self.green_is_pressed:
            self.green_is_pressed = True
            action = Action.GREEN_PRESS
        elif not green_state and self.green_is_pressed:
            self.green_is_pressed = False


        return action

    def _check_rfid(self):
        if not self.reader:
            return None

        status, tag_type = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
        if status == self.reader.MI_OK:
            status, uid = self.reader.MFRC522_Anticoll()
            if status == self.reader.MI_OK:
                card_id = "".join(str(x) for x in uid)
                if not self.card_already_detected:
                    self.card_already_detected = True
                    self.last_card_id = card_id
                    return Action.CARD_TAPPED
        else:
            if self.card_already_detected:
                self.card_already_detected = False

        return None