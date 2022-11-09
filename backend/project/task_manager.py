from enum import Enum
import logging

from project import spotify_api, tasks

class TaskType(Enum):
    SPLASH = "splash"
    SPOTIFY = "spotify"

class TaskManager:

  current_task = None

  def __init__(self):
    # start splash task here
    return 

  def start_task(self, type=TaskType):
    self.revoke()

    if type is TaskType.SPOTIFY:
      self.__start_spotify()

  def revoke(self):
    if self.current_task is not None:
      logging.info("Revoking current task")
      self.current_task.revoke(terminate=True)
      self.current_task = None

  def __start_spotify(self):
    logging.info("Starting Spotify Task")
    self.current_task = tasks.display_spotify_album_art.delay(spotify_api.access_token, spotify_api.refresh_token, spotify_api.token_expire_timestamp)

