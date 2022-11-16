from datetime import datetime
from enum import Enum

import pytz

from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions

FONTS_PATH = "../../rpi-rgb-led-matrix/fonts/"

class Fonts(Enum):
	seven_by_thirteen = FONTS_PATH + "7x13.bdf"
	nine_by_eighteen = FONTS_PATH + "9x18.bdf"
	nine_by_eighteen_b = FONTS_PATH + "9x18B.bdf"


class Renderer:
    primary_color = graphics.Color(255, 255, 255)

    def __init__(self, spotify):
        self.spotify = spotify
        # Configured Matrix
        #TODO: move to env?
        options = RGBMatrixOptions()
        options.rows = 64
        options.cols = 64
        options.hardware_mapping = 'adafruit-hat-pwm'
        options.gpio_slowdown = 3
        self.matrix = RGBMatrix(options = options)

    def off(self):
        self.matrix.Clear()
        return

    def update_clock(self):
        # create string for current time
        timezone = pytz.timezone('America/New_York')
        now = datetime.now(timezone)
        readable_time = now.strftime("%I:%M%p")
        if readable_time[0] == "0":
            readable_time = readable_time[1:]

        # configure x_pos (different when hours number is two digits)
        if (now.hour == 10) or (now.hour == 11) or (now.hour == 12):
            x_pos = 1
        else:
            x_pos = 5

        # create canvas and draw
        canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont(Fonts.nine_by_eighteen_b.value)
        graphics.DrawText(canvas, font, x_pos, 37, self.primary_color, readable_time)
        self.matrix.SwapOnVSync(canvas)


    def update_spotify_album_if_needed(self):
        return

