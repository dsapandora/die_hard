#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import urllib
import requests
import math
from flask import Flask, request, jsonify
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

def register_controller():
    pass

@app.route('/am_gonna_die')
def am_i_away():
    from logic import find_life_expectancy
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    return jsonify(find_life_expectancy(latitude, longitude, None))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')