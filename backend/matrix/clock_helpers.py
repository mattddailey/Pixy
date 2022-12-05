from datetime import datetime
from enum import Enum
import time

import pytz

from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
# from model.weather import Weather

FONTS_PATH = "../../rpi-rgb-led-matrix/fonts/"

class Fonts(Enum):
	four_by_six = FONTS_PATH + "4x6.bdf"
	five_by_eight = FONTS_PATH + "5x8.bdf"
	six_by_ten = FONTS_PATH + "6x10.bdf"
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


def draw_weather(canvas, primary_color: graphics.Color, weather=None):
    current_temp_font = graphics.Font()
    current_temp_font.LoadFont(Fonts.six_by_ten.value)
    graphics.DrawText(canvas, current_temp_font, 30, 54, primary_color, "65°")

	return canvas


if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.hardware_mapping = 'adafruit-hat-pwm'
    options.gpio_slowdown = 2
    matrix = RGBMatrix(options = options)
    canvas = matrix.CreateFrameCanvas()
    canvas = draw_time(canvas, graphics.Color(255, 255, 255))
    canvas = draw_weather(canvas, graphics.Color(255, 255, 255))
    matrix.SwapOnVSync(canvas)
    time.sleep(5)


