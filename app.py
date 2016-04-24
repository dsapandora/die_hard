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

# FINAL RESPONSE
"""
{-
    weather: {'temperature': 25, 
              'visibility': 16.1, 
              'humidity': 0.91, 
              'condition': 'Scattered Thunderstorms', 
              'precipitation': 0.44, 
              'wind': {'gusting': 0, 'speed': 10, 'heading': 329}
             }, 
    alerts: [
            {"name": "Marcos A. Gelabert International Airport",
             "polygon": { "type": "Polygon", "coordinates": [ [ [ -79.555603027300023, 9.04609419376319 ], [ -79.54132457183502, 9.044695969128565 ], [ -79.527595148613713, 9.040555059239212 ], [ -79.514942641953368, 9.033830685246977 ], [ -79.503853460580757, 9.024781393091414 ], [ -79.494753817782055, 9.013755097463457 ], [ -79.487993342948187, 9.001175687826541 ], [ -79.483831655678358, 8.987526714891992 ], [ -79.482428416741698, 8.973332788100791 ], [ -79.483837233855454, 8.959139402025562 ], [ -79.48800365007736, 8.945491968920104 ], [ -79.494767284698952, 8.932914863801059 ], [ -79.503868037071243, 8.921891286538481 ], [ -79.514956108878906, 8.9128447127496 ], [ -79.527605455755094, 8.906122643278378 ], [ -79.541330150020755, 8.90198327322126 ], [ -79.555603027300023, 8.90058558930391 ], [ -79.569875904579277, 8.90198327322126 ], [ -79.583600598844953, 8.906122643278378 ], [ -79.596249945721127, 8.9128447127496 ], [ -79.607338017528789, 8.921891286538481 ], [ -79.61643876990108, 8.932914863801059 ], [ -79.623202404522672, 8.945491968920104 ], [ -79.627368820744579, 8.959139402025562 ], [ -79.628777637858335, 8.973332788100791 ], [ -79.627374398921674, 8.987526714891992 ], [ -79.623212711651846, 9.001175687826541 ], [ -79.616452236817977, 9.013755097463456 ], [ -79.607352594019275, 9.024781393091414 ], [ -79.596263412646664, 9.033830685246977 ], [ -79.583610905986319, 9.040555059239212 ], [ -79.569881482765012, 9.044695969128565 ], [ -79.555603027300023, 9.04609419376319 ] ] ] },
             "close_distace":25,
             "inside": true 
            }
        ]    
    ]
}
"""

@app.route('/get_flight_data')
def get_flight_data():
    from logic import find_flight_data
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    ## Default Area Por cardenas
    if latitude is None:
        latitude = 8.970602
    if longitude is None:
        longitude = -79.559984
    return find_flight_data(latitude,longitude)

@app.route('/get_flight_zones')
def get_flight_zones():
    ## Default Area Por cardenas
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
    return str(req.json())

@app.route('/shape')
def shape():
    from shapely.geometry import Point, shape
    import json
    # # load GeoJSON file containing sectors
    with open('drone-feedback/sources/geojson/panama.json') as data_file:    
        js = json.load(data_file)

    # construct point based on long/lat returned by geocoder
    point = Point(-79.560928, 8.969681)

    # check each polygon to see if it contains the point
    for feature in js['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            print 'Found containing polygon:', feature
    return "Shaping Life"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')