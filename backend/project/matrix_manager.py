from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import time
import requests
import tempfile

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
		self.__clear()
		
		tmp = tempfile.TemporaryFile(mode="wb+")
		tmp.write(requests.get(url).content)
		tmp.seek(0)
		image = Image.open(tmp)
		image.thumbnail((self.__matrix.width, self.__matrix.height), Image.ANTIALIAS)

		self.__matrix.SetImage(image.convert('RGB'))


def matrix_image(image_url):
	matrix_manager = MatrixManager()

	matrix_manager.display_image(image_url)
	
	time.sleep(5)

if __name__ == "__main__":
    matrix_image('https://i.scdn.co/image/ab67616d0000b27336adb8a0c812b3f6df627b58')
