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

    @classmethod
    def has_value(cls, value):
        values = [item.value for item in Mode]
        return value in values
