#!/usr/bin/env python

# Generate a CSV file with one row per neighborhood.

import argparse, csv, collections, ConfigParser, urllib, urllib2, json
parser = argparse.ArgumentParser()
parser.add_argument('--pointmap_file', default='data/pgh/pointmap.csv')
parser.add_argument('--output_file', default='nghd_mapillary_keys.csv')
args = parser.parse_args()

config = ConfigParser.ConfigParser()
config.read('aesthetic/config.txt')
MAPILLARY_CLIENT_ID = config.get('mapillary', 'client_id')
MAPILLARY_API_URL = 'https://a.mapillary.com/v2/search/im/close?'
def get_photo_keys(min_lat, max_lat, min_lon, max_lon):
    """ Given a neighborhood's bounds, finds some photo keys in there. """
    lat = (min_lat + max_lat) / 2.0
    lon = (min_lon + max_lon) / 2.0
 
    params = urllib.urlencode(zip(['lat', 'lon', 'distance', 'max-results', 'client_id'],
        [lat, lon, 500, 10, MAPILLARY_CLIENT_ID]))
    try:
        query = urllib2.urlopen(MAPILLARY_API_URL + params).read()
        query = json.loads(query)
        return [photo['key'] for photo in query['ims']]
    except e:
        print "Request failed"
        print e
        return []

if __name__=='__main__':
    writer = csv.writer(open(args.output_file, 'w'))
    writer.writerow(['neighborhood', 'photo_keys'])

    nghd_latlons = collections.defaultdict(list)
    for line in csv.DictReader(open(args.pointmap_file)):
        if line['nghd'] != 'None':
            latlon = (float(line['lat']), float(line['lon']))
            nghd_latlons[line['nghd']].append(latlon)
    
    for nghd, latlons in nghd_latlons.iteritems():
        min_lat = min([ll[0] for ll in latlons])
        max_lat = max([ll[0] for ll in latlons])
        min_lon = min([ll[1] for ll in latlons])
        max_lon = max([ll[1] for ll in latlons])
        photo_keys = get_photo_keys(min_lat, max_lat, min_lon, max_lon)
        writer.writerow([nghd,json.dumps(photo_keys)])

