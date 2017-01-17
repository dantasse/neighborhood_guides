#!/usr/bin/env python

# Take in a json file of all the venues in a city, and output a CSV for each
# neighborhood telling some info about it - number of businesses per square
# km or something.

import argparse, csv, collections, ujson, util.pointmap, pprint
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# This formatter, and the "helps" below, means it shows the defaults when you call --help.
parser.add_argument('--foursquare_venue_file', default='data/pgh/4sq_venues.json', help=' ')
parser.add_argument('--foursquare_category_file', default='liveliness/4sq_categories.json', help=' ')
parser.add_argument('--nghd_bounds_file', default='data/pgh/nghd_bounds.geojson', help=' ')
parser.add_argument('--pointmap_file', default='data/pgh/pointmap.csv', help=' ')
parser.add_argument('--city_name', default='Pittsburgh', help=' ')
parser.add_argument('--output_file', default='data/pgh/nghd_4sq.csv', help=' ')
args = parser.parse_args()

def get_categories(venue):
    return list(set(foursquare_categories[category['id']] for category in venue['categories']))

def median(lst):
    even = (0 if len(lst) % 2 else 1) + 1
    half = (len(lst) - 1) / 2
    return sum(sorted(lst)[half:half + even]) / float(even)

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
    all_venues = []
    all_foods = []
    all_nightlifes = []
    all_arts = []
    all_shops = []
    all_recs = []
    for nghd, venues in nghds_venues.iteritems():
        foods = len(filter(lambda x: 'Food' in get_categories(x), venues))
        nightlifes = len(filter(lambda x: 'Nightlife Spot' in get_categories(x), venues))
        arts = len(filter(lambda x: 'Arts & Entertainment' in get_categories(x), venues))
        shops = len(filter(lambda x: 'Shop & Service' in get_categories(x), venues))
        recs = len(filter(lambda x: 'Outdoors & Recreation' in get_categories(x), venues))
        # events = len(filter(lambda x: 'Event' in get_categories(x), venues))
        # There are almost no Events in foursquare.
        area = round(nghd_areas[nghd], 5)
        venues_persqmi = round(len(venues) * 1.0 / area, 1)
        foods_persqmi = round(foods * 1.0 / area, 1)
        nightlifes_persqmi = round(arts * 1.0 / area, 1)
        arts_persqmi = round(arts * 1.0 / area, 1)
        shops_persqmi = round(shops * 1.0 / area, 1)
        recs_persqmi = round(recs * 1.0 / area, 1)
        outwriter.writerow([nghd, area, venues_persqmi, foods_persqmi,
            nightlifes_persqmi, arts_persqmi, shops_persqmi, recs_persqmi])

        all_venues.append(venues_persqmi)
        all_foods.append(foods_persqmi)
        all_nightlifes.append(nightlifes_persqmi)
        all_arts.append(arts_persqmi)
        all_shops.append(shops_persqmi)
        all_recs.append(recs_persqmi)

    # Instead of (total venues / total sq mi), we are using median(venues per sqmi)
    # This is so super-sparse neighborhoods don't skew the averages.
    median_venues = median(all_venues)
    median_foods = median(all_foods)
    median_nightlifes = median(all_nightlifes)
    median_arts = median(all_arts)
    median_shops = median(all_shops)
    median_recs = median(all_recs)
    outwriter.writerow([args.city_name, 1, median_venues, median_foods,\
            median_nightlifes, median_arts, median_shops, median_recs])

