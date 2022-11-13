from enum import Enum
import logging

from project import spotify_api, tasks

class TaskType(Enum):
    CLOCK = "Clock"
    SPLASH = "Splash"
    SPOTIFY = "Spotify"

class TaskManager:

  current_task_type = None
  __current_task = None

  def __init__(self):
    # start splash task here
    return 

  def start_task(self, type=TaskType):
    self.revoke()

    if type is TaskType.SPOTIFY:
      self.__start_spotify()
    elif type is TaskType.CLOCK:
      self.__start_clock()

  def revoke(self):
    if self.__current_task is not None:
      logging.info("Revoking current task")
      if self.__current_task is TaskType.SPOTIFY:
        task = tasks.display_spotify_album_art.AsyncResult(self.__current_task.id)
      else:
        task = tasks.display_clock.AsyncResult(self.__current_task.id)
      task.abort()
      self.__current_task = None
      self.current_task_type = None

  def __start_clock(self):
    logging.info("Starting Clock Task")
    self.__current_task = tasks.display_clock()
    self.current_task_type = TaskType.CLOCK

  def __start_spotify(self):
    logging.info("Starting Spotify Task")
    self.__current_task = tasks.display_spotify_album_art.delay(spotify_api.access_token, spotify_api.refresh_token, spotify_api.token_expire_timestamp)
    self.current_task_type = TaskType.SPOTIFY

