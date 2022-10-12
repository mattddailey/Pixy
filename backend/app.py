from flask import Flask, redirect
from flask_cors import CORS

CLIENT_ID = ""
CLIENT_SECRET = ""
SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/authorize/?'

REDIRECT_URI = "http://localhost:5000/callback"

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
	data = "{}client_id={}&response_type=code&redirect_uri={}&scope={}".format(SPOTIFY_URL_AUTH, CLIENT_ID, REDIRECT_URI, "user-read-playback-state") 
	return redirect(data)

@app.route('/callback')
def callback():
	return redirect('http://raspberrypi.local:3000/')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
