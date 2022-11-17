from enums import UtilityType

class Utility:
    def __init__(self, utility: str):
        self.utility = utility

class Brightness(Utility):
    def __init__(self, brightness: int, utility: str = UtilityType.BRIGHTNESS.value):
        self.brightness = brightness
        super().__init__(utility)

class PrimaryColor(Utility):
    def __init__(self, red: int, green: int, blue: int, utility: str = UtilityType.PRIMARY_COLOR.value):
        self.red = red
        self.green = green
        self.blue = blue
        super().__init__(utility)