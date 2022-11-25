from model.enums import ModeType

class Mode:
    def __init__(self, mode: str, authorization_code: str = None):
        self.mode = mode
        # Optional properties
        self.authorization_code = authorization_code

# class Spotify(Mode):
#     def __init__(self, authorization_code: str, mode: str = ModeType.SPOTIFY.value):
#         self.authorization_code = authorization_code
#         super().__init__(mode)