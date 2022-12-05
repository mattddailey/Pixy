import json
import os
import time

import dotenv
import requests

from model.weather import Weather

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

class WeatherService:

    # configured to refresh after 15 mins
    __last_refresh: int = 0
    __refresh_after: int = 54000
    __weather: Weather = None
    
    def __init__(self):
        dotenv.load_dotenv()
        self.latitude = os.getenv('WEATHER_LATITUDE')
        self.longitude = os.getenv('WEATHER_LONGITUDE')
        self.app_id = os.getenv('WEATHER_AP_ID')

    def get_weather(self, force: bool = False):
        if force:
            return self.__refresh_weather_data()
        elif self.__last_refresh + self.__refresh_after < time.time():
            print("Weather data being refreshed...")
            return self.__refresh_weather_data()

        print("Returning stored weather data")
        return self.__weather

    def __refresh_weather_data(self):
        
        url = "{}?lat={}&lon={}&units=imperial&appid={}".format(BASE_URL, self.latitude, self.longitude, self.app_id)
        print("URL: {}".format(url))

        response = requests.get(url)

        try:
            json_data = json.loads(response.text)

            weather = json_data["weather"][0]
            main = weather["main"]
            description = weather["description"]
            temp = json_data["main"]["temp"]
            wind = json_data["wind"]["speed"]

            self.__weather = Weather(main, description, temp, wind)
            self.__last_refresh = time.time()
            print("New weather data saved: {}".format(self.__weather.__dict__))
            return self.__weather
        except:
            print("Error parsing weather response data. Returning...")
            return
            
