from make_celery import make_celery
from flask import Flask, redirect, request
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

AUTHORIZATION_CODE = ""

app = Flask(__name__)
app.config.update(CELERY_CONFIG={
	'broker_url': 'redis://localhost:6379'
})
CORS(app)
celery = make_celery(app)


@app.route('/image')
def image():
	return

@app.route('/spotify-auth')
def spotify_auth():
	# Redirect Spotify Authorization URL
	authURL = "{}client_id={}&response_type=code&redirect_uri={}&scope={}".format(SPOTIFY_URL_AUTH, SPOTIFY_CLIENT_ID, CALLBACK_URL, SPOTIFY_SCOPE) 
	return redirect(authURL)

@app.route('/callback')
def spotify_callback():
	# Upon successful callback from Sptofify Authorization, redirect to the React App Homepage
	return redirect("{}:3000/".format(BASE_URL))
	# return "Hello from dietpi"






@app.route('/hello/<name>')
def test(name):
	hello.delay(name)
	return "Request sent"


@celery.task(name='celery_test_task')
def hello(name):
	return "hello " + name

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
