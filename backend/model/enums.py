from enum import Enum, EnumMeta

class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True  

class ModeType(Enum, metaclass=MetaEnum):
    CLOCK = "clock"
    OFF = "off"
    SPOTIFY = "spotify"

class UtilityType(Enum, metaclass=MetaEnum):
    BRIGHTNESS = "brightness"
    PRIMARY_COLOR = "primary_color"
