from flask import Flask, redirect
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv('BASE_URL')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/authorize/?'
SPOTIFY_SCOPE = "user-read-playback-state" 
CALLBACK_URL = "{}:5000/callback".format(BASE_URL)

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
	data = "{}client_id={}&response_type=code&redirect_uri={}&scope={}".format(SPOTIFY_URL_AUTH, SPOTIFY_CLIENT_ID, CALLBACK_URL, SPOTIFY_SCOPE) 
	return redirect(data)

@app.route('/callback')
def callback():
	return redirect("{}:3000/".format(BASE_URL))

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
