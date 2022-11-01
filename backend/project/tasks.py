import time

from celery import shared_task

from project.spotify import Spotify

@shared_task
def display_spotify_album_art(access_token, refresh_token, token_expire_timestamp):
	spotify_api = Spotify(access_token=access_token, refresh_token=refresh_token, token_expire_timestamp=token_expire_timestamp)
	
	url_to_display = None
	while True:
		current_playing = spotify_api.get_current_playing()
		image_url = current_playing['item']['album']['images'][0]['url']
		if image_url != url_to_display:
			url_to_display = image_url
			# CALL DISPLAY IMAGE HERE
			print("Displaying new image now")
		else:
			print("Image has not changed")
		time.sleep(5)
