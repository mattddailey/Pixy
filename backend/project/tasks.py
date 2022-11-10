import time
import logging
import requests

from celery import shared_task
from celery.utils.log import get_task_logger

from project.spotify import Spotify
# from project.matrix_manager import MatrixManager

# logger = get_task_logger(__name__)

@shared_task
def display_spotify_album_art(access_token, refresh_token, token_expire_timestamp):
	spotify_api = Spotify(access_token=access_token, refresh_token=refresh_token, token_expire_timestamp=token_expire_timestamp)
	# matrix_manager = MatrixManager() 
	
	url_to_display = None
	image_url = None
	while True:
		try:
			current_playing = spotify_api.get_current_playing()
			image_url = current_playing['item']['album']['images'][0]['url']
		except requests.exceptions.RequestException:
			# logger.exception("Some other error occured while trying to use spotify api")
			print("Caught a request exception")
			pass
		except ValueError:
			print("Caught a request while decoding json")
		finally:
			if image_url != url_to_display:
				url_to_display = image_url
				# matrix_manager.display_image(url_to_display)
				print("SPOTIFY task displaying new image")
			elif url_to_display != None:
				print("SPOTIFY task displaying same image")
				pass
		time.sleep(1)

		
		
