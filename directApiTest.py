import requests
import re
import json
import math

import apikeys

sin = math.sin
cos = math.cos
rad = math.radians
atan2 = math.atan2
sqrt = math.sqrt

key = apikeys.mapboxkey
map_url = "https://api.mapbox.com/styles/v1/mapbox/light-v10/static/[-74.0333,40.6815,-73.8341,40.8324]/900x900@2x?access_token={}".format(key)

def main():
    pulon = -73.96870422363281
    pulat = 40.75462341308594
    dolon = -73.98757934570312
    dolat = 40.75204086303711

    # url = "https://api.mapbox.com/directions/v5/mapbox/driving/{}%2C{}%3B{}%2C{}?alternatives=false&geometries=geojson&steps=false&access_token={}".format(pulon, pulat, dolon, dolat, key)
    # res = requests.get(url)
    # text = res.content
    # with open("./python/jsonSample.json", "wb") as jsonfile:
    #     jsonfile.write(text)

    floatpattern = "([+-]{0,1}[\d.]+)"
    pattern = re.compile("{0},{0},{0},{0}".format(floatpattern))
    minlon, minlat, maxlon, maxlat = map(float, pattern.search(map_url).groups())

    lonrange = maxlon-minlon
    latrange = maxlat-minlat

    with open("./python/jsonSample.json", "r") as jsonfile:
        text = jsonfile.read()
    
    jsondata = json.loads(text)
    waypoints = jsondata["routes"][0]["geometry"]["coordinates"]
    pickup_location = jsondata["waypoints"][0]["name"]
    dropoff_location = jsondata["waypoints"][1]["name"]
    print(pickup_location, dropoff_location)

    distsum = 0
    for i in range(1, len(waypoints)):
        distsum += measure(waypoints[i-1][0], waypoints[i-1][1], waypoints[i][0], waypoints[i][1])
    
    wp_and_weight = []
    a = 0
    for i in range(len(waypoints)):
        wp_lon = (waypoints[i][0] - minlon) / lonrange
        wp_lat = (waypoints[i][1] - minlat) / latrange
        if i == 0:
            dist = 0
        else:
            dist = measure(waypoints[i-1][0], waypoints[i-1][1], waypoints[i][0], waypoints[i][1]) / distsum
        print([dist, [wp_lon, wp_lat]])
        a += dist
        wp_and_weight.append([dist, [wp_lon, wp_lat]])
    #print(wp_and_weight)


    return

def measure(lon1, lat1, lon2, lat2):
    r = 6378.137

    dlat = rad(lat2) - rad(lat1)
    dlon = rad(lon2) - rad(lon1)

    a = sin(dlat/2)**2 + cos(rad(lat1)) * cos(rad(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = r * c

    return d*1000

if __name__ == "__main__":
    main()