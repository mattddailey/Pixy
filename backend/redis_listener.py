import time
import logging

import redis

from shared.mode import Mode

MODE_CHANNEL = "mode"
UTILITY_CHANNEL = "utility"

class RedisListener:
    current_mode = Mode.OFF

    def __init__(self, redis: redis.Redis):
        self.redis = redis
        self.redis.set(MODE_CHANNEL, "off")
        self.listen()

    def listen(self):
        print("Listening for matrix control messages...")
        pubsub = self.redis.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe([MODE_CHANNEL, UTILITY_CHANNEL])
        while True:
            message = pubsub.get_message()
            if message is not None:
                if message["channel"] == MODE_CHANNEL:
                    self.handle_mode(message["data"])
                elif message["channel"] == UTILITY_CHANNEL:
                    self.handl_utility(message["data"])
            else:
                self.update_matrix_if_needed()
                
            time.sleep(1)

    def update_matrix_if_needed(self):
        if self.current_mode == Mode.CLOCK:
            # TODO: handle drawing clock
            print("drawing clock")
        elif self.current_mode == Mode.SPOTIFY:
            # TODO: handle drawing spotify
            print("drawing spotify")

    def handle_mode(self, received_mode):
        if received_mode not in [mode.value for mode in Mode]:
            print("received an invalid mode")
            return

        print("Received request to set mode to: {}".format(received_mode))
        self.redis.set(MODE_CHANNEL, received_mode)
        self.current_mode = Mode[received_mode.upper()]
        self.update_matrix_if_needed()

    def handl_utility(self, received_utility):
        # TODO: handle utility
        print("handle utility here")


if __name__ == "__main__":
    r = redis.Redis('redis', 6379, charset="utf-8", decode_responses=True)
    redis_listener = RedisListener(r)