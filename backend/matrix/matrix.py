from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions

class Matrix:

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

    def draw_clock(self):
        return

    def draw_spotify(self):
        return

    def off(self):
        self.matrix.Clear()
        return