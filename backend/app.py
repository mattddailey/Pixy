import os
import logging

from flask import redirect, url_for, request
from flask_cors import CORS

from project import create_app, ext_celery, spotify_api, tasks
from project.task_manager import TaskManager, TaskType

logging.basicConfig(filename='pixy-flask.log', 
					level=logging.INFO, 
					format='[%(asctime)s] %(levelname)s  : %(message)s')

app = create_app()
CORS(app)
celery = ext_celery.celery
task_manager = TaskManager()

@app.route('/')
def index():
	if spotify_api.authorization_code:
		app.logger.info("Already have an auth code")
		return redirect(url_for('callback'))
	else:
		app.logger.info("Fetching a auth code")
		auth_url = spotify_api.authorize_url()
		return redirect(auth_url)

@app.route('/callback')
def callback():
	code = request.args.get('code')
	if code is not None:
		spotify_api.authorization_code = code
	spotify_api.get_access_token()
	return redirect('localhost:3000')

@app.route('/currentMode')
def getCurrentMode():
	if task_manager.current_task is not None:
		return { 'currentMode' :  task_manager.current_task }
	else:
		return { 'currentMode' : 'off' }

@app.route('/isLoggedIn')
def isLoggedIn():
	return { 'isLoggedIn': 'true' }

@app.route('/spotify')
def spotify():
	task_manager.start_task(type=TaskType.SPOTIFY)
	return "", 204

@app.route('/revoke')
def revoke():
	task_manager.revoke()
	return "", 204