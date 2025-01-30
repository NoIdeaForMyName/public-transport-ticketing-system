from enum import Enum


class Action(Enum):
    GREEN_PRESS = 1
    RED_PRESS = 2
    RED_LONG_PRESS = 3
    CARD_TAPPED = 4