import os

from flask import redirect, url_for, request

from project import create_app, ext_celery, spotify_api, tasks
from project.task_manager import TaskManager, TaskType
from project.spotify import Spotify

app = create_app()
celery = ext_celery.celery
task_manager = TaskManager()
spotify_api = Spotify()

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

@app.route('/spotify')
def spotify():
	task_manager.start_task(type=TaskType.SPOTIFY)
	return "", 204