import urllib2
from flask import Flask, request
app = Flask(__name__)
API_KEY = 'ebc2ccbd44d15f282010c6f3514c5c02'
API_URL = 'http://api.openweathermap.org/data/2.5/weather?'
API_QUERY = 'lat={lat}&lon={lon}&appid={api}'
# SAMPLE REQUEST
# http://api.openweathermap.org/data/2.5/weather?q=London,uk&appid=ebc2ccbd44d15f282010c6f3514c5c02

API_KEY='E8D05ADD-DF71-3D14-3794-93FAF8ED8F5'
API_URL='https://api.airmap.io/data/v1/status'

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
    --header "X-API-Key: fd94daed750a375ef87d87445090cc8fab3bf3f62796ac37698b6f7b3add3146" \
    -d "latitude=8.983258&longitude=-79.557281&radius=100000&unique_id=colexample&weather=true" \
    https://api.airmap.io/data/v1/status

Airport Tocumen: 
latitude=9.088791&longitude=-79.384632

AirPort  Gelabert:
8.983258, -79.557281


"""


@app.route('/')
def hello_world():
    return 'Flask Dockerized'

@app.route('/get_data')
def get_data():
    return 'Get data route'

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

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')