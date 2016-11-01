#!/usr/bin/env python

# "Clean up" a geojson file so it's just what we need. Probably this means
# a neighborhood name, geometry, and area. And round the area coordinates to
# take less space. Nobody needs 11 decimal digits :P

import argparse, csv, collections, ujson, geojson
parser = argparse.ArgumentParser()
parser.add_argument('--input_file', default='pgh/Pittsburgh_Neighborhoods.geojson')
parser.add_argument('--output_file', default='pgh/nghd_bounds.geojson')
args = parser.parse_args()

def get_nghd_name(props):
    if 'hood' in props:
        return props['hood']
    # TODO add other ways that people store neighborhood names here.
    return None

def get_nghd_area(props):
    if 'sqmiles' in props:
        return props['sqmiles']
    # TODO add other ways that people store neighborhood areas here.
    return None

if __name__ == '__main__':
    old_geojson = geojson.load(open(args.input_file))
    for feature in old_geojson['features']:
        old_props = feature['properties']
        new_props = {'name': get_nghd_name(old_props),
                'area_sqmi': get_nghd_area(old_props)}
        feature['properties'] = new_props

        feature['geometry'] = geojson.utils.map_coords(lambda x: round(x, 5), feature['geometry'])
    geojson.dump(old_geojson, open(args.output_file, 'w'))

