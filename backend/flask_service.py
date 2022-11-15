import dotenv
import os

from flask import redirect, url_for, request, Flask
from flask_cors import CORS
import redis

from shared.spotify import Spotify
from shared.mode import Mode

app = Flask(__name__)
spotify_api = Spotify()
r = redis.Redis('redis', 6379, charset="utf-8", decode_responses=True)
CORS(app)

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
	current_mode = r.get("mode")
	return { 'currentMode' : current_mode }

@app.route('/isLoggedIn')
def isLoggedIn():
	isLoggedIn = spotify_api.authorization_code is not None
	return { 'isLoggedIn': str(isLoggedIn) }

@app.route('/spotify')
def spotify():
	r.publish('mode', Mode.SPOTIFY.value)
	return "", 204

@app.route('/clock')
def clock():
	r.publish('mode', Mode.CLOCK.value)
	return "", 204

@app.route('/revoke')
def revoke():
	r.publish('mode', Mode.OFF.value)
	return "", 204
