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

	def draw_text(self):
		offscreen_canvas = self.__matrix.CreateFrameCanvas()
		font = graphics.Font()
		font.LoadFont("../rpi-rgb-led-matrix/fonts/7x13.bdf")
		textColor = graphics.Color(255, 255, 255)
		test = graphics.DrawText(offscreen_canvas, font, 10, 10, textColor, "test")
		print(test)	
	
	def scroll_test(self):
		offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../rpi-rgb-led-matrix/fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width
        my_text = "test"

        while True:
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

if __name__ == "__main__":
	matrix_manager = MatrixManager()
	matrix_manager.draw_text()
	time.sleep(5)
