import requests
from shapely.geometry import Point, shape, mapping, Polygon
import json
import difflib
from geopy.distance import great_circle

"""
curl -v -L -G \
    -d "latitude=8.537981&longitude=-80.782127" \
    http://localhost:5000/get_flight_data

curl -v -L -G \
    -d "latitude=9.011125&longitude=-79.474583" \
    http://localhost:5000/get_flight_data

curl -v -L -G \
    -d "latitude=8.968821&longitude=-79.558096" \
    http://localhost:5000/get_flight_data
"""


def find_flight_data(latitude, longitude):
    weather, advisories = _get_weather_data(latitude, longitude)
    res = dict()
    res['weather'] = weather
    res['alerts'] = advisories
    return json.dumps(res, default=jdefault)

def find_life_expectancy(latitude, longitude, elevation):
    current_position = (-79.559984, 8.970602)
    d = great_circle(current_position, (longitude, latitude)).kilometers
    return {'distance': d, 'latitude': current_position[1], 'longitude': current_position[0]}

def jdefault(o):
    if isinstance(o, Polygon):
        return mapping(o)
    return o.__dict__


def _get_weather_data(latitude, longitude):
    url = 'https://api.airmap.io/data/v1/status?radius=360&latitude=%s&longitude=%s&unique_id=sample&weather=true' % (latitude, longitude)
    headers = { 'X-API-Key': 'fd94daed750a375ef87d87445090cc8fab3bf3f62796ac37698b6f7b3add3146' }
    req = requests.get(url,headers=headers)
    response = req.json()
    weather = response['weather']
    advisories = response['nearest_advisories']
    advisories = _find_advisories(advisories, latitude, longitude)
    advisories = _process_advisories(advisories, latitude, longitude)
    return weather, advisories


def _process_advisories(advisories, latitude, longitude):
    # current_position = (latitude, longitude)
    current_position = (longitude, latitude)
    result = []
    for o in advisories:
        distance = _find_shortest_with_coordinates(current_position, o['polygon'].exterior.coords)
        if distance:
            o['close_distace'] = distance
            o['inside'] = o['polygon'].contains(Point(float(longitude), float(latitude)))
            result.append(o)
    return result


def _find_shortest_with_coordinates(current_position, coordinate_list):
    all_distances = map(lambda x: great_circle(current_position, x).kilometers ,coordinate_list)
    return min(float(s) for s in filter(lambda x: x <= 2.00, all_distances))


def _find_distance_with_coordinates(current_position, coordinate_list):
    all_distances = map(lambda x: great_circle(current_position, x).kilometers ,coordinate_list)
    return len(filter(lambda x: x <= 2.00, all_distances)) > 0 # 900 meters away form boders


def _find_advisories(advisories, latitude, longitude):
    advisories_names = map(lambda x: x['name'], advisories)
    location_advisories = _find_panama_advisory_data()
    local = map(lambda x: x['name'], location_advisories)
    return filter(lambda x: difflib.get_close_matches(x['name'],advisories_names), location_advisories)


def _find_panama_advisory_data():
    # # load GeoJSON file containing sectors
    with open('drone-feedback/sources/geojson/panama.json') as data_file:    
        js = json.load(data_file)
    advisories = []
    for feature in js['features']:
        polygon = shape(feature['geometry'])
        data = dict()
        data['name'] = feature['properties']['name']
        data['polygon'] = polygon
        advisories.append(data)
    return advisories
