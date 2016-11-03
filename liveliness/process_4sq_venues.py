#!/usr/bin/env python

# Take in a json file of all the venues in a city, and output a CSV for each
# neighborhood telling some info about it - number of businesses per square
# km or something.

import argparse, csv, collections, ujson, util.pointmap, pprint
parser = argparse.ArgumentParser()
parser.add_argument('--foursquare_venue_file', default='data/pgh/4sq_venues.json')
parser.add_argument('--foursquare_category_file', default='liveliness/4sq_categories.json')
parser.add_argument('--nghd_bounds_file', default='data/pgh/nghd_bounds.geojson')
parser.add_argument('--pointmap_file', default='data/pgh/pointmap.csv')
parser.add_argument('--output_file', default='data/pgh/nghd_4sq.csv')
args = parser.parse_args()

def get_categories(venue):
    return list(set(foursquare_categories[category['id']] for category in venue['categories']))

if __name__ == '__main__':
    nghds_venues = collections.defaultdict(list)
    foursquare_data = ujson.load(open(args.foursquare_venue_file))
    foursquare_categories = ujson.load(open(args.foursquare_category_file))
    pointmap = util.pointmap.Pointmap(args.pointmap_file)
    nghd_bounds = ujson.load(open(args.nghd_bounds_file))
    nghd_areas = {n['properties']['name']: float(n['properties']['area_sqmi']) for n in nghd_bounds['features']}
    for venue in foursquare_data:
        if 'lat' not in venue['location'] or 'lng' not in venue['location']:
            pprint.pprint(venue['location'])
            continue
        lat = float(venue['location']['lat'])
        lon = float(venue['location']['lng'])
        nghd = pointmap[(lat, lon)]
        if nghd != 'None':
            nghds_venues[nghd].append(venue)

    outwriter = csv.writer(open(args.output_file, 'w'))
    outwriter.writerow(['Neighborhood', 'Area in Sq Mi', 'All Venues', 'Food', 'Nightlife Spot', 'Arts and Entertainment', 'Shop & Service', 'Outdoors & Recreation'])
    # Possible top-level types: [u'Travel & Transport', u'Food', u'Residence', u'College & University', u'Nightlife Spot', u'Arts & Entertainment', u'Shop & Service', u'Outdoors & Recreation', u'Professional & Other Places', u'Event'])
    # Also track the total # of venues to get averages.
    all_venues = all_foods = all_nightlifes = all_arts = all_shops = all_recs = 0
    for nghd, venues in nghds_venues.iteritems():
        print nghd
        print 'all venues: ', len(venues)
        foods = len(filter(lambda x: 'Food' in get_categories(x), venues))
        nightlifes = len(filter(lambda x: 'Nightlife Spot' in get_categories(x), venues))
        arts = len(filter(lambda x: 'Arts & Entertainment' in get_categories(x), venues))
        shops = len(filter(lambda x: 'Shop & Service' in get_categories(x), venues))
        recs = len(filter(lambda x: 'Outdoors & Recreation' in get_categories(x), venues))
        all_venues += len(venues)
        all_foods += foods
        all_nightlifes += nightlifes
        all_arts += arts
        all_shops += shops
        all_recs += recs
        # events = len(filter(lambda x: 'Event' in get_categories(x), venues))
        # There are almost no Events in foursquare.
        area = round(nghd_areas[nghd], 5)
        outwriter.writerow([nghd, area, len(venues), foods, nightlifes, arts, shops, recs])
    all_venues *= 1.0 / len(nghds_venues)
    all_foods *= 1.0 / len(nghds_venues)
    all_nightlifes *= 1.0 / len(nghds_venues)
    all_arts *= 1.0 / len(nghds_venues)
    all_shops *= 1.0 / len(nghds_venues)
    all_recs *= 1.0 / len(nghds_venues)
    outwriter.writerow(['Pittsburgh', 1, all_venues, all_foods, all_nightlifes,\
            all_arts, all_shops, all_recs])

