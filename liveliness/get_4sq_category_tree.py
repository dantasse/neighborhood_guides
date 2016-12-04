#!/usr/bin/env python

# Foursquare publishes a category tree. Just download it and spit it out to a
# file describing how to map them into high-level categories.

import argparse, csv, collections, requests, json, ConfigParser
parser = argparse.ArgumentParser()
parser.add_argument('--output_file', default='liveliness/4sq_categories.json')
parser.add_argument('--config_file', default='liveliness/config.txt')
args = parser.parse_args()

def get_subcats_list(cat):
    cats_list = [cat['id']]
    for subcat in cat['categories']:
        cats_list.extend(get_subcats_list(subcat))
    return cats_list

if __name__=='__main__':
    config = ConfigParser.ConfigParser()
    config.read(args.config_file)
    PARAMS = {'client_id': config.get('foursquare', 'client_id'),
             'client_secret': config.get('foursquare', 'client_secret'),
             'v': '20161028'}

    CATEGORY_URL = 'https://api.foursquare.com/v2/venues/categories'
    res = requests.get(CATEGORY_URL, params = PARAMS)

    output = {}
    for category in res.json()['response']['categories']:
        # this just hits the top level
        for subcat in get_subcats_list(category):
            output[subcat] = category['name']

    json.dump(output, open(args.output_file, 'w'))
