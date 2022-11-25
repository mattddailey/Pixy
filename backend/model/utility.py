from model.enums import UtilityType

class Utility:
    def __init__(self, utility: str, brightness: int = None, red: int = None, green: int = None, blue: int = None,):
        self.utility = utility
        # Optional Properties
        self.brightness = brightness
        self.red = red
        self.green = green
        self.blue = blue