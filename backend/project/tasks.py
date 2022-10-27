from celery import shared_task

from project.spotify import Spotify

@shared_task
def display_spotify_album_art(url, access_token, refresh_token, token_expire_timestamp):
	spotify_api = Spotify(access_token=access_token, refresh_token=refresh_token, token_expire_timestamp=token_expire_timestamp)

	return "displaying spotify album art for url: {}".format(url)