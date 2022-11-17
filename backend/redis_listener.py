import json
import time

from redis import Redis

from matrix.renderer import Renderer
from shared.constants import AUTHORIZATION_CODE_KEY, MODE_KEY, UTILITY_KEY
from shared.enums import Mode, Utility
from shared.spotify import Spotify

MODE_KEY = "mode"
UTILITY_KEY = "utility"

class RedisListener:
    counter = 0
    current_mode = Mode.OFF

    def __init__(self, redis: Redis, renderer: Renderer, spotify: Spotify):
        self.redis = redis
        self.renderer = renderer
        self.spotify = spotify
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
            if self.current_mode == Mode.CLOCK:
                self.counter += 1


    def update_matrix_if_needed(self, force=False):
        if self.current_mode == Mode.CLOCK:
            if self.counter % 60 == 0:
                self.renderer.update_clock()
                self.counter = 0

        elif self.current_mode == Mode.SPOTIFY:
            self.renderer.update_spotify_album_if_needed(force)
            return


    def handle_mode(self, data):
        data = json.loads(data)
        mode = data[MODE_KEY]
        if AUTHORIZATION_CODE_KEY in data:
            spotify.authorization_code = data[AUTHORIZATION_CODE_KEY]

        if mode not in Mode:
            print("Received an unsupported mode")
            return

        print("Received request to set mode to: {}".format(mode))
        self.redis.set(MODE_KEY, mode)
        self.current_mode = Mode[mode.upper()]
        
        if self.current_mode == Mode.OFF:
            print("Turning matrix off...")
            self.renderer.off() 
        else:
            self.__rerender()


    def handle_utility(self, data):
        data = json.loads(data)
        utility = data[UTILITY_KEY]
        
        if not utility in Utility:
            print("Received an unsupported mode")
            return

        print("Received request to set {} utility".format(utility))
        
        if utility == Utility.BRIGHTNESS.value:
            brightness = data[Utility.BRIGHTNESS.value]
            renderer.set_brightness(brightness)
            self.redis.set(Utility.BRIGHTNESS.value, brightness)
        elif utility == Utility.PRIMARY_COLOR.value:
            primary_color = {
                "red" : data["red"],
                "green" : data["green"],
                "blue" : data["blue"]
            }
            renderer.set_primary_color(primary_color["red"], primary_color["green"], primary_color["blue"])
            self.redis.set(Utility.PRIMARY_COLOR.value, json.dumps(primary_color))
            self.__rerender()


    def __rerender(self):
        self.counter = 0
        self.update_matrix_if_needed(True)

if __name__ == "__main__":
    redis = Redis('redis', 6379, charset="utf-8", decode_responses=True)
    spotify = Spotify()
    renderer = Renderer(spotify)
    redis_listener = RedisListener(redis, renderer, spotify)