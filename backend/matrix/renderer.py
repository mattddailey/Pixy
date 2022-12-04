from datetime import datetime
from enum import Enum
import requests
import tempfile

import pytz
from PIL import Image

from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from services.spotify_service import SpotifyService


FONTS_PATH = "../../rpi-rgb-led-matrix/fonts/"

class Fonts(Enum):
	seven_by_thirteen = FONTS_PATH + "7x13.bdf"
	nine_by_eighteen = FONTS_PATH + "9x18.bdf"
	nine_by_eighteen_b = FONTS_PATH + "9x18B.bdf"


class Renderer:
    primary_color = graphics.Color(255, 255, 255)
    spotify_current_image_url = None

    def __init__(self, spotify_service: SpotifyService):
        self.spotify_service = spotify_service
        # Configured Matrix
        options = RGBMatrixOptions()
        options.rows = 64
        options.cols = 64
        options.hardware_mapping = 'adafruit-hat-pwm'
        options.gpio_slowdown = 2
        self.matrix = RGBMatrix(options = options)

    def off(self):
        self.spotify_current_image_url = None
        self.matrix.Clear()

    def set_brightness(self, brightness):
        self.matrix.brightness = brightness

    def set_primary_color(self, red, green, blue):
        print("Setting new primary color...")
        self.primary_color = graphics.Color(red, green, blue)

    def update_clock(self):
        print("Updating clock...")
        
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


    def update_spotify_album_if_needed(self, force=False):
        # fetch current playing info
        try:
            current_playing = self.spotify_service.get_current_playing()
            image_url = current_playing['item']['album']['images'][0]['url']
        except Exception as e: 
            print("An error occured attempting to get spotify album cover")
            print(e)
            return
        
        # check if current playing image url matches what is currently being displayed
        if image_url != self.spotify_current_image_url or force == True:
            print("Updating spotify album cover...")
            self.spotify_current_image_url = image_url
            self.__display_image_from_url(image_url)


    def __display_image_from_url(self, url):
        # download image to tempfile
        tmp = tempfile.TemporaryFile(mode="wb+")
        tmp.write(requests.get(url).content)
        tmp.seek(0)

        # create image and set to matrix
        image = Image.open(tmp)
        image.thumbnail((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
        self.matrix.SetImage(image.convert('RGB'))


