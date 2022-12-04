import json
import requests
import time

# from model.weather import Weather
class Weather:
    def __init__(self, main: str, description: str, temp: str, wind: str):
        self.main = main
        self.description = description
        self.temp = temp
        self.wind = wind

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

class WeatherService:

    __last_refresh: int = 0
    __refresh_after: int = 108000
    __weather: Weather = None
    
    def __init__(self):
        #TODO: get from environment
        # dotenv.load_dotenv()
        self.latitude = "40.27"
        self.longitude = "-76.89"
        self.app_id = "1b1c6cdd783ca4d91adb23091383808e"

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
        
        # make request
        response = requests.get(url)

        # parse response 
        try:
            json_data = json.loads(response.text)

            weather = json_data["weather"][0]
            main = weather["main"]
            description = weather["description"]
            temp = json_data["main"]["temp"]
            wind = json_data["wind"]["speed"]
        except:
            print("Error parsing weather response data. Returning...")
            return
        finally:
            self.__weather = Weather(main, description, temp, wind)
            self.__last_refresh = time.time()
            print("New weather data saved: {}".format(self.__weather.__dict__))
            return self.__weather
