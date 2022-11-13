import tempfile
import time

from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions

from PIL import Image
import requests

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

	def draw_text(self, font, x_pos, y_pos, text):
		self.__clear()
		offscreen_canvas = self.__matrix.CreateFrameCanvas()
		font = graphics.Font()
		font.LoadFont("../rpi-rgb-led-matrix/fonts/9x18B.bdf")
		textColor = graphics.Color(255, 255, 255)
		
		graphics.DrawText(offscreen_canvas, font, x_pos, y_pos, textColor, text))
		self.__matrix.SwapOnVSync(offscreen_canvas)

if __name__ == "__main__":
	matrix_manager = MatrixManager()
	matrix_manager.draw_text()
	time.sleep(5)
