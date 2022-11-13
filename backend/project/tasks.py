from datetime import datetime
import time
import logging
import requests
import pytz

from celery import shared_task
from celery.contrib.abortable import AbortableTask
from celery.utils.log import get_task_logger

from project.spotify import Spotify
from project.matrix_manager import Fonts, MatrixManager

logger = get_task_logger(__name__)

@shared_task(bind=True, base=AbortableTask)
def display_clock(self):
	matrix_manager = MatrixManager()
	while True:
		if self.is_aborted():
			return
		timezone = pytz.timezone('America/New_York')
		now = datetime.now(timezone)
		readable_time = now.strftime("%I:%M%p")
		
		if readable_time[0] == "0":
			readable_time = readable_time[1:]
		
		if (now.hour == 10) or (now.hour == 11) or (now.hour == 12):
			x_pos = 1
		else:
			x_pos = 5
			
		logging.info("drawing time: {}".format(readable_time))
		matrix_manager.draw_text(Fonts.nine_by_eighteen_b.value, x_pos, 37, readable_time)
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
