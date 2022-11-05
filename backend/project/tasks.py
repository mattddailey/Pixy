import time
import logging
import requests

from celery import shared_task

from project.spotify import Spotify
from project.matrix_manager import MatrixManager

logger = logging.getLogger(__name__)

@shared_task
def display_spotify_album_art(access_token, refresh_token, token_expire_timestamp):
	spotify_api = Spotify(access_token=access_token, refresh_token=refresh_token, token_expire_timestamp=token_expire_timestamp)
	matrix_manager = MatrixManager() 
	
	url_to_display = None
	image_url = None
	while True:
		try:
			current_playing = spotify_api.get_current_playing()
			image_url = current_playing['item']['album']['images'][0]['url']
		except requests.exceptions.RequestException:
			logger.exception("Error during request to spotify api")
		except ValueError:
			logger.exception("Error decoding json response from spotify api")
		except TypeError:
			logger.exception("Error finding 'url' component in response from spotify api")
		except:
			logger.exception("Some other error occured while trying to use spotify api")
		finally:
			if image_url != url_to_display:
				url_to_display = image_url
				matrix_manager.display_image(url_to_display)
				logger.info("SPOTIFY task displaying new image")
			elif url_to_display != None:
				logger.info("SPOTIFY task displaying same image")
			time.sleep(1)

		
		
