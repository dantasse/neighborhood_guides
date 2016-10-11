#!/usr/bin/env python

# Simplest version: get the average autotag for each neighborhood.

import argparse, csv, collections, ast, json
from util import pointmap

parser = argparse.ArgumentParser()
parser.add_argument('--yfcc_autotags_file', default='data/yfcc100m_pgh_autotagged.csv')
parser.add_argument('--pointmap_file', default='data/pgh_pointmap.csv')
parser.add_argument('--output_file', default='pgh_nghd_autotags.csv')
args = parser.parse_args()

if __name__ == '__main__':
    pgh_pointmap = pointmap.Pointmap(args.pointmap_file)

    # Neighborhood -> counter of # of times an autotag shows up.
    # e.g. 'Upper Lawrenceville': Counter({'indoor': 197', 'text': 125, ...})
    nghds_autotags90plus = collections.defaultdict(collections.Counter)

    # Neighborhood -> sum of all probabilities. 
    # (even though this doesn't make a ton of sense.)
    # e.g. 'Upper Lawrenceville': Counter({'indoor': 28.342, 'text': 20.451, ...})
    nghds_autotags = collections.defaultdict(collections.Counter)

    overall_autotags_90plus = collections.Counter()
    for row in csv.reader(open(args.yfcc_autotags_file)):
        photo_id, nsid, lat, lon = row[0:4]
        nghd = pgh_pointmap[lat, lon]

        autotags_90plus = ast.literal_eval(row[4])
        autotags = row[5].split(',')
        autotags_ctr = collections.Counter()
        for tag in autotags:
            if tag == '':
                continue
            else:
                tagname, value = tag.split(':')
                nghds_autotags[nghd][tagname] += round(float(value), 3)
        nghds_autotags[nghd]['NUM_PHOTOS'] += 1
        nghds_autotags90plus[nghd].update(autotags_90plus + ['NUM_PHOTOS'])
        overall_autotags_90plus.update(autotags_90plus + ['NUM_PHOTOS'])
 
    
    # Compute the overall rates of each tag, so we can subtract them off.
    tempdict = collections.Counter()
    for tag, value in overall_autotags_90plus.items():
        tempdict[tag] = (value*1.0/overall_autotags_90plus['NUM_PHOTOS'])
    del tempdict['NUM_PHOTOS']
    overall_autotags_90plus = tempdict

    output = {}
    for nghd, autotags90plus in nghds_autotags90plus.items():
        autotags = nghds_autotags[nghd]
        num_photos = autotags90plus['NUM_PHOTOS']
        output[nghd] = {'num_photos': num_photos, 'autotags_90plus': {},
                'autotags_all': {}, 'autotags_90plus_minusbaseline':{}}
            # 'autotags_90plus': [], 'autotags_all': []}
        for autotag, count in autotags90plus.most_common():
            if autotag == 'NUM_PHOTOS':
                continue
            pct_photos = round(count * 1.0 / num_photos, 5)
            output[nghd]['autotags_90plus'][autotag] = pct_photos
            # output[nghd]['autotags_90plus'].append((autotag, round(count*1.0/num_photos, 5)))
            output[nghd]['autotags_90plus_minusbaseline'][autotag] = round(pct_photos - overall_autotags_90plus[autotag], 5)

        for autotag, count in autotags.most_common():
            if autotag == 'NUM_PHOTOS':
                continue
            output[nghd]['autotags_all'][autotag] = round(count*1.0/num_photos, 5)
            # output[nghd]['autotags_all'].append((autotag, round(count*1.0/num_photos, 5)))
 
    json.dump(output, open(args.output_file, 'w'))
