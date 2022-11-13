from datetime import datetime
import time
import logging
import requests

from celery import shared_task
from celery.contrib.abortable import AbortableTask
from celery.utils.log import get_task_logger

from project.spotify import Spotify
from project.matrix_manager import MatrixManager

logger = get_task_logger(__name__)

@shared_task(bind=True, base=AbortableTask)
def display_clock(self):
	matrix_manager = MatrixManager()
	while True:
		if self.is_aborted():
			return
		now = datetime.now()
		readable_time = now.strftime("%I:%M %p")
		if readable_time[0] == "0":
			readable_time = readable_time[1:]
		matrix_manager.display_text()
		time.sleep(60)


@shared_task(bind=True, base=AbortableTask)
def display_spotify_album_art(self, access_token, refresh_token, token_expire_timestamp, base=AbortableTask):
	spotify_api = Spotify(access_token=access_token, refresh_token=refresh_token, token_expire_timestamp=token_expire_timestamp)
	matrix_manager = MatrixManager() 
	
	url_to_display = None
	image_url = None
	while True:
		if self.is_aborted():
			return
		try:
			current_playing = spotify_api.get_current_playing()
			image_url = current_playing['item']['album']['images'][0]['url']
		except: 
			logging.exception("An error occured attempting to get spotify album cover")
		finally:
			if image_url != url_to_display:
				logging.info("Displaying new album cover")
				url_to_display = image_url
				matrix_manager.display_image(url_to_display)
		time.sleep(1)