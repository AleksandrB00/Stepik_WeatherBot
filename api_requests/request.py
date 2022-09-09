import json 

import requests

from settings import api_config

def get_city_coord(city):
    payload = {'geocode' : city, 'apikey' : api_config.geo_key, 'format' : 'json'}
    r = requests.get('https://geocode-maps.yandex.ru/1.x', params=payload)
    geo = json.loads(r.text)
    return geo['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']

def get_weather(city):
    coordinates = get_city_coord(city).split()
    payload = {'lat' : coordinates[1], 'lon' : coordinates[0], 'lang' : 'ru_RU'}
    r = requests.get('https://api.weather.yandex.ru/v2/forecast', params=payload, headers=api_config.weather_key)
    weather_data = json.loads(r.text)
    return weather_data['fact']