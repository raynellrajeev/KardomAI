"""
OpenWeather
@author: Raynell Rajeev

"""

class Weather:
    def __init__(self):
        pass

    def weather(self, city:str):

        import json
        import requests

        self.city=city

        api_key='3c4098d69bd50bc59bbe181350a9a094'
        url=f'https://api.openweathermap.org/data/2.5/forecast?q={self.city}&appid={api_key}&units=metric'

        response= requests.get(url)
        if response.status_code == 200:
            data=response.json()
            print(json.dumps(data, indent=2, sort_keys=True)) #this is temporary, change it when implementing.

        else:
            print(f"Error with status code: {response.status_code}")  
