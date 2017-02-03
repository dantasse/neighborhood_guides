#!/usr/bin/env python

# get_mapillary_photos was just getting photo keys; here we're downloading the
# actual images from Google Street View instead.

import argparse, csv, collections, ConfigParser, urllib, json, requests, random, ujson
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--pointmap_file', default='data/pgh/pointmap.csv', help=' ')
parser.add_argument('--photos_per_nghd', type=int, default=10, help=' ')
parser.add_argument('--venues_file', help='If provided, we will try to get photos near a venue. If not, just random photos.')
parser.add_argument('--output_dir', default='data/pgh/streetview/', help=' ')
args = parser.parse_args()

config = ConfigParser.ConfigParser()
config.read('aesthetic/config.txt')
GOOGLE_API_KEY = config.get('google', 'api_key')
GOOGLE_API_URL = 'https://maps.googleapis.com/maps/api/streetview?'
GOOGLE_METADATA_URL = 'https://maps.googleapis.com/maps/api/streetview/metadata?'

def get_photo(lat, lon):
    """ Given a lat lon, find the photo that is there, or return ZERO_RESULTS
    if there is no photo there (or we have some other error). """
     
    params = urllib.urlencode({
        'size': '600x300',
        'location': '%s,%s' % (lat, lon),
        'key': GOOGLE_API_KEY
        }) # heading=151.78&pitch=-0.76&
    try:
        metadata_resp = requests.get(GOOGLE_METADATA_URL + params).json()
        if metadata_resp['status'] == 'OK':
            print "image found"
            img_resp = requests.get(GOOGLE_API_URL + params)
            image = img_resp.content
            return image
        elif metadata_resp['status'] == 'ZERO_RESULTS':
            print "zero results"
            return 'ZERO_RESULTS'
        else:
            print "something else: ", metadata_resp
            return 'ZERO_RESULTS'

    except Exception as e:
        print "Request failed, ", e
        return []

if __name__=='__main__':
    pointmap = {}
    for line in csv.DictReader(open(args.pointmap_file)):
        pointmap[round(float(line['lat']), 3), round(float(line['lon']), 3)] = line['nghd']

    nghd_latlons = collections.defaultdict(list)
    if args.venues_file:
        print "Loading json: ", args.venues_file
        venues_json = ujson.load(open(args.venues_file))
        print "Done loading json."
        for venue in venues_json:
            lat = round(float(venue['location']['lat']), 3)
            lon = round(float(venue['location']['lng']), 3)
            if (lat, lon) in pointmap:
                nghd = pointmap[(lat, lon)]
                nghd_latlons[nghd].append((lat, lon))
            # if that latlon isn't in the pointmap, it's outside Pgh, so drop it.
    else:
        for latlon, nghd in pointmap.iteritems():
            if nghd != 'None':
                nghd_latlons[nghd].append(latlon)
    
    for nghd, latlons in nghd_latlons.iteritems():
        print nghd
        if '/' in nghd:
            nghd = nghd.replace('/', '-')
        tries = 0
        found = 0
        for i in range(args.photos_per_nghd * 5): # try up to 50 times
            latlon = random.choice(latlons)
            photo = get_photo(latlon[0], latlon[1])
            if photo == 'ZERO_RESULTS':
                pass
            else:
                img_file = open(args.output_dir + '%s_%s.png' % (nghd, found), 'w')
                img_file.write(photo)
                img_file.close()
                found += 1
                if found >= args.photos_per_nghd:
                    break

