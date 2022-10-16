from celery import Celery
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import time

def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

def matrix_image():
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
