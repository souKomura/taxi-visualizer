import csv
import datetime
import requests
import re
import json
import math
import sys
import time

import index_list as idx
import apikeys

sin,cos, atan2 = math.sin, math.cos, math.atan2
rad = math.radians
sqrt = math.sqrt

mapboxkey = apikeys.mapboxkey
mapbox_style1 = "styles/v1/leblanc1234/cktk2toca24yk18mu3g9f25dh" #with road
mapbox_style2 = "styles/v1/leblanc1234/cktprs5bj2ih717pme8g3es7t" #without road, only label

#latitude/longitude range is stated in url.
#1 半島
img_write_path = json_write_path = "./files/1/"
mon, date = "02", "01"
readpath = "./csv/per_day/2015-{}-{}.csv".format(mon,date)
map_url_preformat = "https://api.mapbox.com/{0}/static/[-74.0619,40.6973,-73.8713,40.8417]/1080x1080@2x?access_token={1}"

# #2 2つの空港を含む範囲
# img_write_path = json_write_path = "./files/2/"
# mon,date = "05", "10"
# readpath = "./csv/per_day/2015-{}-{}.csv".format(mon, date)
# map_url_preformat = "https://api.mapbox.com/{0}/static/[-74.1624,40.5688,-73.6498,40.8601]/1280x960@2x?access_token={1}"

# #3 半島下半分くらい
# img_write_path = json_write_path = "./files/3/"
# mon,date = "05", "15"
# readpath = "./csv/per_day/2015-{}-{}.csv".format(mon, date)
# map_url_preformat = "https://api.mapbox.com/{0}/static/[-74.0321,40.6994,-73.929,40.7775]/1080x1080?access_token={1}"

map_url1 = map_url_preformat.format(mapbox_style1, mapboxkey)
map_url2 = map_url_preformat.format(mapbox_style2, mapboxkey)

jsonfilepath = json_write_path + "datas.json"

detail_timrange = [
    datetime.datetime(2015, int(mon), int(date), 11, 0, 0).timestamp() + 46800,
    datetime.datetime(2015, int(mon), int(date), 15, 0, 0).timestamp() + 46800
]

#--------------------------------------------------------
def main():
    csv_to_waypoints()
    save_image()
    return

#--------------------------------------------------------
def csv_to_waypoints():
    # map's lon/lat range can be get from request-url
    floatpattern = "([+-]{0,1}[\d.]+)"
    pattern = re.compile("{0},{0},{0},{0}".format(floatpattern))
    minlon, minlat, maxlon, maxlat = map(float, pattern.search(map_url_preformat).groups())

    print("this map is showing:")
    print("minimum : {}".format((minlon, minlat)))
    print("maximum : {}".format((maxlon, maxlat)))

    lonrange = maxlon-minlon
    latrange = maxlat-minlat

    # format original csv.
    # if a pick-up coodinate is not on the map, don't format the data.
    pre_count = 0

    write_content = []
    count = 0
    error_count = 0
    first = True
    lastslept = time.time()

    with open(readpath, "r") as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            pu_lat = float(row[idx.pickup_latitude])
            pu_lon = float(row[idx.pickup_longitude])

            pudate, putime = row[idx.tpep_pickup_datetime].split()
            py, pm, pd = map(int, pudate.split("-"))
            ph, pmin, ps = map(int, putime.split(":"))
            pu_epoch = datetime.datetime(py, pm, pd, ph, pmin, ps).timestamp() + 46800



            if detail_timrange[0] <= pu_epoch <= detail_timrange[1] \
                and minlon <= pu_lon <= maxlon \
                and minlat <= pu_lat <= maxlat:

                pre_count += 1

        print("now will format {} datas".format(pre_count))
        if input("press y to go >> ") == "y":
            pass
        else:
            return

    #create new JSON file
    with open(jsonfilepath, "w") as jsonfile:
        jsonfile.write("[\n")

    with open(readpath, "r") as csvfile:
        reader = csv.reader(csvfile)

        for rowcnt, row in enumerate(reader):
            try:
                number_of_passanger = int(row[idx.passenger_count])

                #Pickup / dropoff coordinate
                pu_lat = float(row[idx.pickup_latitude])
                pu_lon = float(row[idx.pickup_longitude])
                do_lat = float(row[idx.dropoff_latitude])
                do_lon = float(row[idx.dropoff_longitude])

                if not (minlon <= pu_lon <= maxlon and minlat <= pu_lat <= maxlat):
                    continue

                pu_lat_normalized = (pu_lat - minlat) / latrange
                pu_lon_normalized = (pu_lon - minlon) / lonrange
                do_lat_normalized = (do_lat - minlat) / latrange
                do_lon_normalized = (do_lon - minlon) / lonrange
                
                #format pickup/dropoff datetime "yyyy-mm-dd hh:mm:ss" to epoch second. 
                # ----------------------------------------
                pudate, putime = row[idx.tpep_pickup_datetime].split()
                py, pm, pd = map(int, pudate.split("-"))
                ph, pmin, ps = map(int, putime.split(":"))
                pu_epoch = datetime.datetime(py, pm, pd, ph, pmin, ps).timestamp() + 46800

                dodate, dotime = row[idx.tpep_dropoff_datetime].split()
                dy, dm, dd = map(int, dodate.split("-"))
                dh, dmin, ds = map(int, dotime.split(":")) 
                do_epoch = datetime.datetime(dy, dm, dd, dh, dmin, ds).timestamp() + 46800
                # ----------------------------------------

                if not (detail_timrange[0] <= pu_epoch <= detail_timrange[1]):
                    continue
            
                direction_url = "https://api.mapbox.com/directions/v5/mapbox/driving/{}%2C{}%3B{}%2C{}?alternatives=false&geometries=geojson&steps=false&access_token={}".format(pu_lon, pu_lat, do_lon, do_lat, mapboxkey)
                res = requests.get(direction_url)
                text = res.content
                jsondata = json.loads(text)

                waypoints = jsondata["routes"][0]["geometry"]["coordinates"]
                pickup_location = jsondata["waypoints"][0]["name"]
                dropoff_location = jsondata["waypoints"][1]["name"]

                distsum = 0
                for i in range(1, len(waypoints)):
                    distsum += measure(waypoints[i-1][0], waypoints[i-1][1], waypoints[i][0], waypoints[i][1])
                
                wp_and_weight = []
                for i in range(len(waypoints)):
                    wp_lon = (waypoints[i][0] - minlon) / lonrange
                    wp_lat = (waypoints[i][1] - minlat) / latrange
                    if i == 0:
                        dist = 0
                    else: 
                        dist = measure(waypoints[i-1][0], waypoints[i-1][1], waypoints[i][0], waypoints[i][1]) / distsum

                    wp_and_weight.append([dist, [wp_lon, wp_lat]])

                dic = {
                    "number_of_passanger": number_of_passanger,
                    "locations": [pickup_location, dropoff_location],
                    "pickup_cood": [pu_lon, pu_lat],
                    "dropoff_cood": [do_lon, do_lat],
                    "pickup_normalized": [pu_lon_normalized, pu_lat_normalized],
                    "dropoff_normalized": [do_lon_normalized, do_lat_normalized],
                    "waypoint_with_dist": wp_and_weight,
                    "time_range": [pu_epoch, do_epoch],
                    "distance": distsum
                }

                write_content.append(dic)
                
                count += 1
                sys.stdout.write("\rnow on row->{:>5},{:>5}/{:>5}, error:{} (20020 + 23023 done)".format(rowcnt, count, pre_count, error_count))
                sys.stdout.flush()

                #write to JSON for every 1000 datas
                if len(write_content) > 1000:
                    with open(jsonfilepath, "a") as jsonfile:
                        for dic in write_content:
                            if first:
                                first = False
                            else:
                                jsonfile.write(",\n")
                            jsonfile.write(json.dumps(dic, indent=4))

                    write_content.clear()

                #mapbox API's limitation of request.
                # 300 / 1min
                if count % 290 == 0:
                    elapsed = time.time() - lastslept
                    if elapsed < 60:
                        print("\n sleep {} sec".format(60-elapsed))
                        time.sleep(60 - elapsed) 

                    lastslept = time.time()

            except (IndexError, ZeroDivisionError) as e:
                error_count += 1

    with open(jsonfilepath, "a") as jsonfile:
        for dic in write_content:
            if first:
                first = False
            else:
                jsonfile.write(",\n")
            jsonfile.write(json.dumps(dic, indent=4))
    
    with open(jsonfilepath, "a") as jsonfile:
        jsonfile.write("\n]")

    return

#--------------------------------------------------------
def save_image():
    
    with open(img_write_path + "map1.png", "wb") as imgfile:
        imgfile.write(requests.get(map_url1).content)
    
    with open(img_write_path + "map2.png", "wb") as imgfile:
        imgfile.write(requests.get(map_url2).content)

    return

#--------------------------------------------------------
def measure(lon1, lat1, lon2, lat2):
    """measure distance with spherical trigonometry"""
    r = 6378.137

    dlat = rad(lat2) - rad(lat1)
    dlon = rad(lon2) - rad(lon1)

    a = sin(dlat/2)**2 + cos(rad(lat1)) * cos(rad(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = r * c

    return d*1000

#--------------------------------------------------------

if __name__ == "__main__":
    main()