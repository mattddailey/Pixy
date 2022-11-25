from model.enums import ModeType

class Mode:
    def __init__(self, mode: str, authorization_code: str = None):
        self.mode = mode
        # Optional properties
        self.authorization_code = authorization_code