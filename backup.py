#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import urllib
import requests
import math
from flask import Flask, request
app = Flask(__name__)
API_KEY = 'ebc2ccbd44d15f282010c6f3514c5c02'
API_URL = 'http://api.openweathermap.org/data/2.5/weather?'
API_QUERY = 'lat={lat}&lon={lon}&appid={api}'

# SAMPLE REQUEST
# http://
# api.openweathermap.org/data/2.5/weather?q=London,uk&appid=ebc2ccbd44d15f282010c6f3514c5c02

# API_KEY='E8D05ADD-DF71-3D14-3794-93FAF8ED8F5'
# API_URL='https://api.airmap.io/data/v1/status'

"""
curl -v -L -G \
    --header "X-API-Key: 'E8D05ADD-DF71-3D14-3794-93FAF8ED8F5'" \
    -d "latitude=33.9425&longitude=-118.4081&unique_id=laxexample" \
    https://api.airmap.io/data/v1/status
"""

"""
curl -v -L -G \
    --header "X-API-Key: fd94daed750a375ef87d87445090cc8fab3bf3f62796ac37698b6f7b3add3146" \
    -d "latitude=8.985955&longitude=-79.529316&radius=100000&unique_id=colexample&weather=true" \
    https://api.airmap.io/data/v1/status
"""

"""
curl -v -L -G \
    --header "'X-api-key: fd94daed750a375ef87d87445090cc8fab3bf3f62796ac37698b6f7b3add3146" \
    -d "latitude=8.983258&longitude=-79.557281&radius=100000&unique_id=colexample&weather=true" \
    https://api.airmap.io/data/v1/status

Airport Tocumen: 
latitude=9.088791&longitude=-79.384632

AirPort  Gelabert:
8.983258, -79.557281

curl -G \
    --header "X-API-Key: fd94daed750a375ef87d87445090cc8fab3bf3f62796ac37698b6f7b3add3146" \
    -d "latitude=8.985955&longitude=-79.529316&radius=100000&unique_id=colexample&weather=true" \
    https://api.airmap.io/data/v1/status
"""


@app.route('/')
def hello_world():
    return 'Flask Dockerized'

@app.route('/get_data')
def get_data():
    R = 6378.1 #Radius of the Earth
    brng = 1.57 #Bearing is 90 degrees converted to radians.
    d = 15 #Distance in km
    lat1 = math.radians(52.20472) #Current lat point converted to radians
    lon1 = math.radians(0.14056) #Current long point converted to radians

    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
         math.cos(lat1)*math.sin(d/R)*math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
                 math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    print(lat2)
    print(lon2)
    return 'Get data route %s %s' % (lat2, lon2)

@app.route('/get_something_else')
def get_something_else():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    if latitude is None:
        latitude = 8.985955
    if longitude is None:
        longitude = -79.529316
    url = API_URL + API_QUERY.format(lat=latitude, lon=longitude, api=API_KEY) 
    values = urllib2.urlopen(url).read()
    return values

@app.route('/get_flight_zones')
def get_flight_zones():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    if latitude is None:
        latitude = 8.985955
    if longitude is None:
        longitude = -79.529316

    url = 'https://api.airmap.io/data/v1/status?radius=360&latitude=%s&longitude=%s&unique_id=sample&weather=true' % (latitude, longitude)
    headers = { 'X-API-Key': 'fd94daed750a375ef87d87445090cc8fab3bf3f62796ac37698b6f7b3add3146' }
    req = requests.get(url,headers=headers)
    no_flight_near_me = map(lambda x: x['name'], req.json()['nearest_advisories'])

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



#!/usr/bin/env python

# Haversine formula example in Python
# Author: Wayne Dyck

import math

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')