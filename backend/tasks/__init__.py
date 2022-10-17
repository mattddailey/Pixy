import celery
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import time

@celery.task(name='display_image')
def display_image():
	image = Image.open('/root/smiley.jpeg')

  # Configure the matrix
  options = RGBMatrixOptions()
  options.rows = 64
  options.cols = 64
  options.hardware_mapping = 'adafruit-hat-pwm'

  matrix = RGBMatrix(options = options)

  image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

  matrix.SetImage(image.convert('RGB'))
  
  time.sleep(5)

  image.close()
