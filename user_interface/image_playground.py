from PIL import Image, ImageDraw, ImageFont
from utilities.constants import (BACKGROUND_SIZE, MAX_TEXT_WIDTH, TEXT_LINES_SPACING, RADIO_BUTTON_START_Y,
                                 RADIO_BUTTON_SPACING, CIRCLE_X, RADIO_BUTTON_TEXT_X, TITLE_START_COORDS,
                                 FACES_SIZE, MARKS_SIZE, DYNAMIC_TEXT_COORDS, DYNAMIC_INTERFACE_ICON_COORDS, STATIC_INTERFACE_ICON_COORDS)


def paste_scaled_icon(result, icon_path, position, new_size):
    icon = Image.open(icon_path).convert("RGBA")
    icon = icon.resize(new_size, Image.LANCZOS)
    result.paste(icon, position, mask=icon)


def draw_radio_button(draw, center, is_selected=False, radius=4):
    x, y = center
    draw.ellipse(
        (x - radius, y - radius, x + radius, y + radius),
        outline="black",
        fill="white"
    )
    if is_selected:
        inner_radius = radius - 2
        draw.ellipse(
            (x - inner_radius, y - inner_radius, x + inner_radius, y + inner_radius),
            fill="black"
        )


def prepare_draw_object(background_path):
    original_bg = Image.open(background_path).convert('RGBA')
    background = original_bg.resize(BACKGROUND_SIZE, Image.LANCZOS)
    width, height = background.size

    result = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    result.paste(background, (0, 0))

    draw = ImageDraw.Draw(result)
    return draw, result


def draw_text(draw, text, start_coords, font=ImageFont.load_default()):
    x, y = start_coords
    words = text.split()
    current_line = ""
    wrapped_lines = []

    for word in words:
        test_line = current_line + " " + word if current_line else word
        line_width = draw.textbbox((0, 0), test_line, font=font)[2]

        if line_width <= MAX_TEXT_WIDTH:
            current_line = test_line
        else:
            if current_line:
                wrapped_lines.append(current_line)
            current_line = word

    if current_line:
        wrapped_lines.append(current_line)

    for line in wrapped_lines:
        draw.text((x, y), line, font=font, fill="white")
        y += font.getbbox("A")[3] + TEXT_LINES_SPACING


def generate_radio_button_interface(draw, result, title, options, selected_option, font=ImageFont.load_default()):
    draw_text(draw, title, TITLE_START_COORDS)

    # change start y so that it is dependent on titles length

    for i, option_text in enumerate(options, start=1):
        cy = RADIO_BUTTON_START_Y + (i - 1) * RADIO_BUTTON_SPACING
        draw_radio_button(draw, (CIRCLE_X, cy + 4), is_selected=(selected_option == i))
        draw.text((RADIO_BUTTON_TEXT_X, cy), option_text, font=font, fill="white")

    return result


def generate_static_icon_interface(draw, result, title, icon, icon_size):
    draw_text(draw, title, TITLE_START_COORDS)
    paste_scaled_icon(result, icon, STATIC_INTERFACE_ICON_COORDS, icon_size)
    return result


def generate_dynamic_icon_interface(draw, result, title, dynamic_text, icon):
    draw_text(draw, title, TITLE_START_COORDS)
    font = ImageFont.truetype("arial.ttf", 7)
    draw_text(draw, dynamic_text, DYNAMIC_TEXT_COORDS, font)
    paste_scaled_icon(result, icon, DYNAMIC_INTERFACE_ICON_COORDS, FACES_SIZE)
    return result



if __name__ == "__main__":
    draw, result = prepare_draw_object('utilities/background.png')
    # generate_static_icon_interface(draw, result, "Zakup wykonany pomyslnie", 'icons/x_mark.png', (24, 24))
    generate_dynamic_icon_interface(draw, result, "Twoj bilet", "Aktywny bilet czasowy, pozostalo: 7min 20 s", 'icons/angry_face.png')



    # title_main = "Wybierz opcje:"
    # options_main = ["Kup bilet", "Sprawdz bilet", "Doladowanie"]
    #
    # generate_radio_button_interface(
    #     draw,
    #     result,
    #     title=title_main,
    #     options=options_main,
    #     selected_option=1
    # )
    #
    # generate_radio_button_interface(
    #     title=title_main,
    #     options=options_main,
    #     selected_option=2,
    #     background_path="images/background.png",
    #     output_path="images/main_menu_2.png"
    # )
    #
    # generate_radio_button_interface(
    #     title=title_main,
    #     options=options_main,
    #     selected_option=3,
    #     background_path="images/background.png",
    #     output_path="images/main_menu_3.png"
    # )
    #
    # generate_radio_button_interface(
    #     title="Wybierz bilet:",
    #     options=["Jednorazowy", "Czasowy"],
    #     selected_option=1,
    #     background_path="images/background.png",
    #     output_path="images/ticket_choice_1.png"
    # )
    # generate_radio_button_interface(
    #     title="Wybierz bilet:",
    #     options=["Jednorazowy", "Czasowy"],
    #     selected_option=2,
    #     background_path="images/background.png",
    #     output_path="images/ticket_choice_2.png"
    # )
    #
    # time_title = "Czas waznosci:"
    #
    # generate_radio_button_interface(
    #     title=time_title,
    #     options=["15min", "30min", "1h"],
    #     selected_option=1,
    #     background_path="images/background.png",
    #     output_path="images/time_choice_1.png"
    # )
    # generate_radio_button_interface(
    #     title=time_title,
    #     options=["15min", "30min", "1h"],
    #     selected_option=2,
    #     background_path="images/background.png",
    #     output_path="images/time_choice_2.png"
    # )
    #
    # generate_radio_button_interface(
    #     title=time_title,
    #     options=["15min", "30min", "1h"],
    #     selected_option=3,
    #     background_path="images/background.png",
    #     output_path="images/time_choice_3.png"
    # )
    #
    # amount_title = "Kwota doladowania:"
    # amount_options = ["5zl", "10zl", "50zl"]
    # generate_radio_button_interface(
    #     title=amount_title,
    #     options=amount_options,
    #     selected_option=1,
    #     background_path="images/background.png",
    #     output_path="images/amount_choice_1.png"
    # )
    #
    # generate_radio_button_interface(
    #     title=amount_title,
    #     options=amount_options,
    #     selected_option=2,
    #     background_path="images/background.png",
    #     output_path="images/amount_choice_2.png"
    # )
    #
    # generate_radio_button_interface(
    #     title=amount_title,
    #     options=amount_options,
    #     selected_option=3,
    #     background_path="images/background.png",
    #     output_path="images/amount_choice_3.png"
    # )
