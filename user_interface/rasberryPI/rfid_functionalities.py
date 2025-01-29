import RPi.GPIO as GPIO
from mfrc522 import MFRC522
import datetime
from buzzer import test as buzz


def init_reader():
    reader = MFRC522()
    return reader

def card_reader(reader):
    while True:
        status, TagType = reader.MFRC522_Request(reader.PICC_REQIDL)
        if status == reader.MI_OK:
            status, uid = reader.MFRC522_Anticoll()
            if status == reader.MI_OK:
                card_id = "".join([str(x) for x in uid])
                buzz()
                print(f'Card id: {card_id}')
                while status == reader.MI_OK:
                    status, _ = reader.MFRC522_Anticoll()


finally:
    GPIO.cleanup()