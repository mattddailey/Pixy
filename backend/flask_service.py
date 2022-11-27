import dotenv
import json
import os

from flask import redirect, url_for, request, Flask
from flask_cors import CORS
import redis

from constants import AUTHORIZATION_CODE_KEY, MODE_KEY, UTILITY_KEY
from model.enums import ModeType
from model.mode import Mode
from model.utility import Utility
from services.spotify_service import SpotifyService

app = Flask(__name__)
spotify_api = SpotifyService()
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
	if not mode in ModeType:
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

@app.route('/utility', methods=['POST'])
def set_utility():
	utility = request.json
	is_published = r.publish(UTILITY_KEY, json.dumps(utility))
	if is_published:
		return "", 204
	else:
		return "", 501

def build_data_for_mode(mode):
	data = Mode(mode)

	if mode == ModeType.SPOTIFY.value:
		data.authorization_code = spotify_api.authorization_code

	return json.dumps(data.__dict__)
