import dotenv
import os

from flask import redirect, url_for, request
from flask_cors import CORS

from project import create_app, ext_celery, spotify_api, tasks
from project.task_manager import TaskManager, TaskType

app = create_app()
CORS(app)

celery = ext_celery.celery
task_manager = TaskManager()

dotenv.load_dotenv()
REDIRECT_URL = os.getenv("BASE_URL") + ":3000"

@app.route('/')
def index():
	if spotify_api.authorization_code:
		print("Already have an auth code")
		return redirect(url_for('callback'))
	else:
		print("Fetching a auth code")
		auth_url = spotify_api.authorize_url()
		return redirect(auth_url)

@app.route('/callback')
def callback():
	code = request.args.get('code')
	if code is not None:
		spotify_api.authorization_code = code
	spotify_api.get_access_token()
	return redirect(REDIRECT_URL)

@app.route('/currentMode')
def getCurrentMode():
	if task_manager.current_task_type is not None:
		return { 'currentMode' :  task_manager.current_task_type.value }
	else:
		return { 'currentMode' : 'Off' }

@app.route('/isLoggedIn')
def isLoggedIn():
	isLoggedIn = (spotify_api.authorization_code is not None) and (spotify_api.access_token is not None) and (spotify_api.refresh_token is not None)
	return { 'isLoggedIn': str(isLoggedIn) }

@app.route('/spotify')
def spotify():
	task_manager.start_task(type=TaskType.SPOTIFY)
	return "", 204

@app.route('/clock')
def clock():
	task_manager.start_task(type=TaskType.CLOCK)
	return "", 204

@app.route('/revoke')
def revoke():
	task_manager.revoke()
	return "", 204
