#!/usr/bin/env python3

# import lib.oled.SSD1331 as SSD1331


def init_oled():
    # disp = SSD1331.SSD1331()
    # disp.Init()
    # return disp
    return None

def oled_manager(disp, image_to_show):
    disp.clear()
    disp.ShowImage(image_to_show, 0, 0)



