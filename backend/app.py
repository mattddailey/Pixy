import os

from flask import redirect, url_for, request

from project import create_app, ext_celery, spotify_api, tasks

app = create_app()
celery = ext_celery.celery

current_task = None

@app.route('/')
def index():
	if spotify_api.authorization_code:
		print("ALREADY HAVE AUTH CODE")
		return redirect(url_for('callback'))
	else:
		print("FETCHING AUTH CODE")
		auth_url = spotify_api.authorize_url()
		return redirect(auth_url)

@app.route('/callback')
def callback():
	code = request.args.get('code')
	if code is not None:
		spotify_api.authorization_code = code
	spotify_api.get_access_token()
	return "test"

@app.route('/current_playing')
def current_playing():
	result = spotify_api.get_current_playing()
	url = result['item']['album']['images'][0]['url']
	# matrix_tests.matrix_image(url)
	return url

@app.route('/spotify_album')
def spotify_album():
	global current_task
	current_task = tasks.display_spotify_album_art.delay(spotify_api.access_token, spotify_api.refresh_token, spotify_api.token_expire_timestamp)
	return str(current_task)

@app.route('/revoke')
def revoke():
	global current_task
	if current_task is not None:
		current_task.revoke(terminate=True)
		current_task = None
		return "task revoked"
	else:
		return "No current task"