import json
import time

from redis import Redis

from matrix.matrix import Matrix
from shared.constants import AUTHORIZATION_CODE_KEY, MODE_KEY, UTILITY_KEY
from shared.mode import Mode
from shared.spotify import Spotify

MODE_KEY = "mode"
UTILITY_KEY = "utility"

class RedisListener:
    counter = 0
    current_mode = Mode.OFF

    def __init__(self, matrix: Matrix, redis: Redis, spotify: Spotify):
        self.matrix = matrix
        self.redis = redis
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
                    self.handl_utility(message["data"])
            else:
                self.update_matrix_if_needed()
                
            time.sleep(1)

            # Clock is the only mode where we need to keep track of counter (for now)
            if self.current_mode == Mode.CLOCK:
                self.counter += 1


    def update_matrix_if_needed(self):
        if self.current_mode == Mode.CLOCK:
            if self.counter % 60 == 0:
                print("Updating clock...")
                self.matrix.draw_clock()
                self.counter == 0
        
        elif self.current_mode == Mode.OFF:
            print("Turning matrix off...")
            self.matrix.off()

        elif self.current_mode == Mode.SPOTIFY:
            self.matrix.draw_spotify()
            return


    def handle_mode(self, data):
        data = json.loads(data)
        mode = data[MODE_KEY]
        if AUTHORIZATION_CODE_KEY in data:
            spotify.authorization_code = data[AUTHORIZATION_CODE_KEY]

        if mode not in [mode.value for mode in Mode]:
            print("Received an unsupported mode")
            return

        print("Received request to set mode to: {}".format(mode))
        self.redis.set(MODE_KEY, mode)
        self.current_mode = Mode[mode.upper()]
        self.update_matrix_if_needed()


    def handl_utility(self, received_utility):
        # TODO: handle utility
        return


if __name__ == "__main__":
    redis = Redis('redis', 6379, charset="utf-8", decode_responses=True)
    spotify = Spotify()
    matrix = Matrix(spotify)
    redis_listener = RedisListener(matrix, redis, spotify)