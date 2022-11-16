import dotenv
import json
import os

from flask import redirect, url_for, request, Flask
from flask_cors import CORS
import redis

from shared.constants import AUTHORIZATION_CODE_KEY, MODE_KEY
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
	return redirect(REDIRECT_URL)

@app.route('/mode/<mode>', methods=['POST'])
def set_mode(mode):
	if not mode in Mode:
		return "", 400
	
	data = build_data_for_mode(mode)
	is_published = r.publish(MODE_KEY, data)
	if is_published:
		return "", 204
	else:
		return "", 501

@app.route('/mode', methods=['GET'])
def get_mode():
	current_mode = r.get(MODE_KEY)
	return { 'currentMode' : current_mode }
	
@app.route('/isLoggedIn')
def is_logged_in():
	isLoggedIn = spotify_api.authorization_code is not None
	return { 'isLoggedIn': str(isLoggedIn) }

def build_data_for_mode(mode):
	data = { MODE_KEY : mode }
	if mode == Mode.SPOTIFY.value and spotify_api.authorization_code is not None:
		data[AUTHORIZATION_CODE_KEY] = spotify_api.authorization_code
	return json.dumps(data)
