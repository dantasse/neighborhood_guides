#!/usr/bin/env python

# Geocode each row! Using the Mapbox geocoder.

import argparse, csv, collections, ConfigParser, requests, json, urllib, time
# import xmltodict
parser = argparse.ArgumentParser()
parser.add_argument('--input_file', default='crimes_2015.csv')
parser.add_argument('--config_file', default='config.txt')
parser.add_argument('--partial_file')
parser.add_argument('--pointmap_file', default='../pointmap.csv')
parser.add_argument('--output_file', default='crimes_2015_geocoded.csv')
args = parser.parse_args()

config = ConfigParser.ConfigParser()
config.read(args.config_file)

pointmap = {}
for line in csv.DictReader(open(args.pointmap_file)):
    pointmap[(float(line['lat']), float(line['lon']))] = line['nghd']

cache = {} # addr -> (lat, lon)
if args.partial_file:
    partial = open(args.partial_file)
    for line in csv.reader(partial):
        cache[line[10]] = (float(line[11]), float(line[12]))
    partial.close()
print "Loaded this many cache entries: " + str(len(cache))
print cache

geocode_url = "https://api.mapbox.com/geocoding/v5/mapbox.places/"

def geocode(addr):
    global cache
    try:
        print "Searching for " + addr
        if addr in cache:
            print "cached: " + str(cache[addr])
            return cache[addr]
        else:
            url = geocode_url + urllib.quote(addr) + ".json"
            params = {"country": "US",
                    "types":"address", "limit": 1,
                    "access_token": config.get("mapbox", "access_token"),
                    "bbox": [-98.0, 30.0, -97.4, 30.6]}
            res = requests.get(url, params=params)
            if res.status_code == 200:
                lonlat = res.json()['features'][0]['center']
                print (lonlat[1], lonlat[0])
                cache[addr] = (lonlat[1], lonlat[0])
                time.sleep(0.1)
                return (lonlat[1], lonlat[0])
            else:
                print "No response"
                return None
    except Exception as e:
        print e

writer = csv.writer(open(args.output_file, 'a'))
input_reader = csv.reader(open(args.input_file))
input_reader.next()
for line in input_reader:
    addr = line[5].strip() + ", Austin, TX"

    latlon = geocode(addr)
    if latlon == None:
        continue
    rounded_latlon = (round(latlon[0], 3), round(latlon[1], 3))

    if rounded_latlon in pointmap:
        nghd = pointmap[rounded_latlon]
    else:
        nghd = "None"
    line.append(latlon[0])
    line.append(latlon[1])
    line.append(nghd)
    writer.writerow(line)

