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
		except requests.exceptions.RequestException:
			print("Error using requests library to communicate with spotify api")
			pass
		except ValueError:
			print("Caught a request while decoding json")
			pass
		except: 
			print("Some other error occured")
		finally:
			if image_url != url_to_display:
				url_to_display = image_url
				matrix_manager.display_image(url_to_display)
				print("SPOTIFY task displaying new image")
			elif url_to_display != None:
				print("SPOTIFY task displaying same image")
				pass
		time.sleep(1)

		
		
