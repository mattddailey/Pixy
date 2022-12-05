from datetime import datetime
from enum import Enum

import pytz

from rgbmatrix import graphics
from model.weather import Weather

FONTS_PATH = "../../rpi-rgb-led-matrix/fonts/"

class Fonts(Enum):
	seven_by_thirteen = FONTS_PATH + "7x13.bdf"
	nine_by_eighteen = FONTS_PATH + "9x18.bdf"
	nine_by_eighteen_b = FONTS_PATH + "9x18B.bdf"

def draw_time(canvas, primary_color: graphics.Color):
    # create string for current time
    timezone = pytz.timezone('America/New_York')
    now = datetime.now(timezone)
    readable_time = now.strftime("%-I:%M%p")

    # configure x_pos (different when hours number is two digits)
    if (now.hour == 10) or (now.hour == 11) or (now.hour == 12):
        x_pos = 1
    else:
        x_pos = 5

    font = graphics.Font()
    font.LoadFont(Fonts.nine_by_eighteen_b.value)
    graphics.DrawText(canvas, font, x_pos, 37, primary_color, readable_time)
    
    return canvas


def draw_weather(canvas, weather: Weather):

    return canvas
