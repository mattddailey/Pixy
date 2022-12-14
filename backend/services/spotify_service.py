import base64
import logging
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

class SpotifyService:

  # env objects
  __callback_url = ''
  __client_id = ''
  __client_secret = ''

  # auth objects
  access_token = None
  authorization_code = None
  refresh_token = None
  token_expire_timestamp = None

  # -------------------------- LIFECYCLE -------------------------- 

  def __init__(self, authorization_code=None):
    dotenv.load_dotenv()
    self.authorization_code = authorization_code
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
        logging.debug("Already have a valid access token, no need to fetch new one")
        return self.access_token
      else:
        logging.debug("Access token expired. Refreshing now...")
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
    logging.debug("Received token response. Setting spotify class values")
    self.access_token = response["access_token"]
    self.token_expire_timestamp = time.time() + response["expires_in"]
    try:
      self.refresh_token = response["refresh_token"]
    except:
      logging.exception("No refresh_token in the token response received")
    
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