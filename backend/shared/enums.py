from enum import Enum, EnumMeta

class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True  

class Mode(Enum, metaclass=MetaEnum):
    CLOCK = "clock"
    OFF = "off"
    SPOTIFY = "spotify"

class Utility(Enum, metaclass=MetaEnum):
    BRIGHTNESS = "brightness"
    PRIMARY_COLOR = "primary_color"
