import requests
from shapely.geometry import Point, shape, mapping, Polygon
import json
import difflib
from geopy.distance import great_circle

def find_flight_data(latitude, longitude):
    weather, advisories = _get_weather_data(latitude, longitude)
    res = dict()
    res['weather'] = weather
    res['alerts'] = advisories
    return json.dumps(res, default=jdefault)


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
    advisories = _distance_to_advisories(advisories, latitude, longitude)
    return weather, advisories


def _distance_to_advisories(advisories, latitude, longitude):
    # current_position = (latitude, longitude)
    current_position = (longitude, latitude)
    destination = (41.499498, -81.695391)
    thing = filter(lambda x: _find_distance_with_coordinates(current_position, x['polygon'].exterior.coords)==True , advisories)
    return thing


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
