import json
import time

from redis import Redis

from constants import AUTHORIZATION_CODE_KEY, MODE_KEY, UTILITY_KEY
from matrix.renderer import Renderer
from model.enums import ModeType, UtilityType
from model.mode import Mode, Spotify
from model.utility import Brightness, PrimaryColor
from services.spotify_service import SpotifyService

MODE_KEY = "mode"
UTILITY_KEY = "utility"

class RedisListener:
    counter = 0
    current_mode = ModeType.OFF

    def __init__(self, redis: Redis, renderer: Renderer, spotify_service: SpotifyService):
        self.redis = redis
        self.renderer = renderer
        self.spotify_service = spotify_service
        self.redis.set(MODE_KEY, "off")
        self.listen()


    def listen(self):
        print("Listening for matrix control messages...")
        pubsub = self.redis.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe([MODE_KEY, UTILITY_KEY])
        while True:
            message = pubsub.get_message()
            if message is not None:
                if message["channel"] == MODE_KEY:
                    self.handle_mode(message["data"])
                elif message["channel"] == UTILITY_KEY:
                    self.handle_utility(message["data"])
            else:
                self.update_matrix_if_needed()
                
            time.sleep(1)

            # Clock is the only mode where we need to keep track of counter (for now)
            if self.current_mode == ModeType.CLOCK:
                self.counter += 1


    def update_matrix_if_needed(self, force=False):
        if self.current_mode == ModeType.CLOCK:
            if self.counter % 60 == 0:
                self.renderer.update_clock()
                self.counter = 0

        elif self.current_mode == ModeType.SPOTIFY:
            self.renderer.update_spotify_album_if_needed(force)
            return


    def handle_mode(self, data):
        mode = self.__unpack_mode(json.loads(data))

        if isinstance(mode, Spotify):
            spotify_service.authorization_code = data[AUTHORIZATION_CODE_KEY]

        print("Received request to set mode to: {}".format(mode.mode))
        self.redis.set(MODE_KEY, mode.mode)
        self.current_mode = ModeType[mode.mode.upper()]
        
        if self.current_mode == ModeType.OFF:
            print("Turning matrix off...")
            self.renderer.off() 
        else:
            self.__rerender()


    def handle_utility(self, data):
        utility = self.__unpack_utility(json.loads(data))
        
        if utility is None:
            print("Received an unsupported mode")
            return

        print("Received request to set {} utility".format(utility.utility))
        
        if isinstance(utility, Brightness):
            renderer.set_brightness(utility.brightness)
            self.redis.set(UtilityType.BRIGHTNESS.value, utility.brightness)
        elif isinstance(utility, PrimaryColor):
            renderer.set_primary_color(utility.red, utility.green, utility.blue)
            self.redis.set(UtilityType.PRIMARY_COLOR.value, utility)
            
        self.__rerender()


    def __rerender(self):
        self.counter = 0
        self.update_matrix_if_needed(True)

    def __unpack_mode(self, data):
        if data[MODE_KEY] == ModeType.SPOTIFY.value:
            mode = Spotify(**data)
        elif data[MODE_KEY] == ModeType.CLOCK.value:
            mode = Mode(**data)
        else:
            mode = Mode("off")
        return mode

    def __unpack_utility(self, data):
        utility = None
        if data[UTILITY_KEY] == UtilityType.BRIGHTNESS.value:
            utility = Brightness(**data)
        elif data[UTILITY_KEY] == UtilityType.PRIMARY_COLOR.value:
            utility = PrimaryColor(**data)
        return utility



if __name__ == "__main__":
    redis = Redis('redis', 6379, charset="utf-8", decode_responses=True)
    spotify_service = SpotifyService()
    renderer = Renderer(spotify_service)
    redis_listener = RedisListener(redis, renderer, spotify_service)