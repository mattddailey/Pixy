from celery import Celery
from rgbmatrix import RGBMatrix

def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

def matrix_text():
    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = 64
    options.columns = 64
    options.hardware_mapping = 'adafruit-hat'

    matrix = RGBMatrix(options = options)