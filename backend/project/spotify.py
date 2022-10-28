import base64
import json
import os
import time

import dotenv
import requests

ACCOUNTS_BASE_URL = 'https://accounts.spotify.com'
API_BASE_URL = 'https://api.spotify.com'

AUTHORIZE_ENDPOINT = '/authorize'
TOKEN_ENDPOINT = '/api/token'
CURRENT_PLAYING_ENDPOINT = '/v1/me/player/currently-playing'

class Spotify:

  # env objects
  __callback_url = ''
  __client_id = ''
  __client_secret = ''

  # auth objects
  access_token = None
  authorization_code = ''
  refresh_token = ''
  token_expire_timestamp = None

  # -------------------------- LIFECYCLE -------------------------- 

  def __init__(self, access_token=None, refresh_token=None, token_expire_timestamp=None):
    dotenv.load_dotenv()
    self.access_token = access_token
    self.refresh_token = refresh_token
    self.token_expire_timestamp = token_expire_timestamp
    self.__callback_url = os.getenv('BASE_URL') + ':5000/callback'
    self.__client_id = os.getenv('SPOTIFY_CLIENT_ID')
    self.__client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

  # ------------------------ AUTHORIZATION ------------------------

  def authorize_url(self):
    url = "{}/?client_id={}&response_type={}&redirect_uri={}&scope={}".format(ACCOUNTS_BASE_URL + AUTHORIZE_ENDPOINT, self.__client_id, 'code', self.__callback_url, 'user-read-playback-state')
    return url

  def get_access_token(self):
    if (self.access_token is not None) and (self.token_expire_timestamp is not None):
      if time.time() < self.token_expire_timestamp:
        # access token already fetched, and not yet expired
        return self.access_token
      else:
        # access token fetched, but expired
        return self.__refresh_access_token()
    
    # fetching access token for the first time

    data = {
		  'grant_type': 'authorization_code',
		  'code': self.authorization_code,
		  'redirect_uri': self.__callback_url,
	  }

    post = requests.post(ACCOUNTS_BASE_URL + TOKEN_ENDPOINT, data=data, headers=self.__authorization_headers)
    return self.__handle_token_response(json.loads(post.text))

  def __handle_token_response(self, response):
    self.access_token = response["access_token"]
    self.token_expire_timestamp = time.time() + response["expires_in"]
    self.refresh_token = response["refresh_token"] 
    return self.access_token
  
  def __refresh_access_token(self):
    data = {
		  'grant_type': 'refresh_token',
		  'refresh_token': self.refresh_token
	  }

    post = requests.post(ACCOUNTS_BASE_URL + TOKEN_ENDPOINT, data=data, headers=self.__authorization_headers)
    return self.__handle_token_response(json.loads(post.text))

  @property
  def __authorization_headers(self):
    authorization = base64.b64encode(("{}:{}".format(self.__client_id, self.__client_secret)).encode())
    headers = {
      "Authorization": "Basic {}".format(authorization.decode())
    }
    return headers
    

  # -------------------------- API CALLS --------------------------

  def get_current_playing(self):
    get = requests.get(API_BASE_URL + CURRENT_PLAYING_ENDPOINT, headers=self.__api_headers)
    return json.loads(get.text)

  @property
  def __api_headers(self):
    token = self.get_access_token()
    headers = {
      'Authorization': f'Bearer {token}',
    }
    return headers