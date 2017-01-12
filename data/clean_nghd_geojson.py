#!/usr/bin/env python

# "Clean up" a geojson file so it's just what we need. Probably this means
# a neighborhood name, geometry, and area. And round the area coordinates to
# take less space. Nobody needs 11 decimal digits :P

import argparse, csv, collections, ujson, geojson, area
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--input_file', default='pgh/Pittsburgh_Neighborhoods.geojson', help=' ')
parser.add_argument('--name_field', help='what variable in the geojson file means "neighborhood name."')
parser.add_argument('--output_file', default='pgh/nghd_bounds.geojson', help=' ')
args = parser.parse_args()

def get_nghd_name(props):
    if args.name_field:
        return props[args.name_field]
    if 'hood' in props:
        return props['hood']
    elif 'nhood' in props:
        return props['nhood']
    # TODO add other ways that people store neighborhood names here.
    return None

def get_nghd_area(obj):
    """ Returns the area of the neighborhood in square miles. """
    if 'sqmiles' in obj['properties']:
        return obj['properties']['sqmiles']
    # TODO add other ways that people store neighborhood areas here.
    else:
        nghd_area_sqm = area.area(obj['geometry'])
        print obj
        print nghd_area_sqm
        return nghd_area_sqm / 2589988.11 # 1 sq mile = this many sq meters.
    return None

if __name__ == '__main__':
    old_geojson = geojson.load(open(args.input_file))
    for feature in old_geojson['features']:
        old_props = feature['properties']
        new_props = {'name': get_nghd_name(old_props),
                'area_sqmi': get_nghd_area(feature)}
        feature['properties'] = new_props

        feature['geometry'] = geojson.utils.map_coords(lambda x: round(x, 5), feature['geometry'])
    geojson.dump(old_geojson, open(args.output_file, 'w'))

