#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import urllib
import requests
import math
from flask import Flask, request
app = Flask(__name__)
# SAMPLE REQUEST
# http://
# api.openweathermap.org/data/2.5/weather?q=London,uk&appid=ebc2ccbd44d15f282010c6f3514c5c02

# API_KEY='E8D05ADD-DF71-3D14-3794-93FAF8ED8F5'
# API_URL='https://api.airmap.io/data/v1/status'

@app.route('/get_flight_zones')
def get_flight_zones():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    if latitude is None:
        latitude = 8.970602
    if longitude is None:
        longitude = -79.559984

    url = 'https://api.airmap.io/data/v1/status?radius=360&latitude=%s&longitude=%s&unique_id=sample&weather=true' % (latitude, longitude)
    headers = { 'X-API-Key': 'fd94daed750a375ef87d87445090cc8fab3bf3f62796ac37698b6f7b3add3146' }
    req = requests.get(url,headers=headers)
    no_flight_near_me = map(lambda x: x['name'], req.json()['nearest_advisories'])
    from geopy.distance import great_circle
    import json
    with open('gelabert.json') as data_file:    
        data = json.load(data_file)
    im_close  = map(lambda x: distance((latitude,longitude), (x[1], x[0])), data['geometry']['coordinates'][0])
    return str(filter(lambda x: x <= 0.100, im_close))

def distance(origin, destination):
    lat1, lon1 = origin
    print destination
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d

@app.route('/get_weather_data')
def get_weather_data():
    """
    Weather parameters of wind speed and direction, gust speed potential, dew point, temperature and visibility.
    """
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    if latitude is None:
        latitude = 8.985955
    if longitude is None:
        longitude = -79.529316

    url = 'https://api.airmap.io/data/v1/status?radius=360&latitude=%s&longitude=%s&unique_id=sample&weather=true' % (latitude, longitude)
    headers = { 'X-API-Key': 'fd94daed750a375ef87d87445090cc8fab3bf3f62796ac37698b6f7b3add3146' }
    req = requests.get(url,headers=headers)
    return str(req.json()['weather'])



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')