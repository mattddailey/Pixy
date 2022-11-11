import time
import logging
import requests

from celery import shared_task
from celery.contrib.abortable import AbortableTask

from project.spotify import Spotify
from project.matrix_manager import MatrixManager

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
			print("An error occured attempting to get spotify album cover")
		finally:
			if image_url != url_to_display:
				url_to_display = image_url
				matrix_manager.display_image(url_to_display)
		time.sleep(1)

		
		
