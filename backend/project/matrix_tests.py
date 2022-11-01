from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import time
import requests

def matrix_image(image_url):
    # image = Image.open('/root/smiley.jpeg')
    
    with open('/root/test.jpg', 'wb') as image:
        image.write(requests.get(image_url).content)
        image.close()

    image = Image.open('/root/test.jpg')

    # Configure the matrix
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.hardware_mapping = 'adafruit-hat-pwm'
    options.gpio_slowdown = 3

    matrix = RGBMatrix(options = options)

    image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

    matrix.SetImage(image.convert('RGB'))
    
    time.sleep(5)

    image.close()

if __name__ == "__main__":
    matrix_image('https://i.scdn.co/image/ab67616d0000b27336adb8a0c812b3f6df627b58')
