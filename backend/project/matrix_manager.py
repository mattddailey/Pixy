import tempfile
import time
import enum

from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions

from PIL import Image
import requests

FONTS_PATH = "../rpi-rgb-led-matrix/fonts/"

class Fonts(enum.Enum):
	seven_by_thirteen = FONTS_PATH + "7x13.bdf"
	nine_by_eighteen = FONTS_PATH + "9x18.bdf"
	nine_by_eighteen_b = FONTS_PATH + "9x18B.bdf"

class MatrixManager:
	__rows = 64
	__cols = 64
	__hardware_mapping = 'adafruit-hat-pwm'
	__gpio_slowdown = 3

	def __init__(self):
		options = RGBMatrixOptions()
		options.rows = self.__rows
		options.cols = self.__cols
		options.hardware_mapping = self.__hardware_mapping
		options.gpio_slowdown = self.__gpio_slowdown
		self.__matrix = RGBMatrix(options = options)
	
	def __clear(self):
		self.__matrix.Clear()

	def display_image(self, url):
		tmp = tempfile.TemporaryFile(mode="wb+")
		tmp.write(requests.get(url).content)
		tmp.seek(0)
		image = Image.open(tmp)
		image.thumbnail((self.__matrix.width, self.__matrix.height), Image.ANTIALIAS)

		self.__matrix.SetImage(image.convert('RGB'))

	def draw_text(self, font_value, x_pos, y_pos, text):
		self.__clear()
		offscreen_canvas = self.__matrix.CreateFrameCanvas()
		font = graphics.Font()
		font.LoadFont(font_value)
		textColor = graphics.Color(255, 255, 255)
		
		graphics.DrawText(offscreen_canvas, font, x_pos, y_pos, textColor, text)
		self.__matrix.SwapOnVSync(offscreen_canvas)

if __name__ == "__main__":
	matrix_manager = MatrixManager()
	matrix_manager.draw_text(Fonts.nine_by_eighteen_b.value, 2, 20, "test")
	time.sleep(5)
