from enums import UtilityType

class Utility:
    def __init__(self, utility: UtilityType):
        self.utility = utility.value

class Brightness(Utility):
    def __init__(self, brightness: int):
        self.brightness = brightness
        super().__init__(UtilityType.BRIGHTNESS)

class Color(Utility):
    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue
        super().__init__(UtilityType.PRIMARY_COLOR)