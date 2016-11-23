#!/usr/bin/env python

# Simplest version: get the average autotag for each neighborhood.

import argparse, csv, collections, ast, json, operator
from util import pointmap

parser = argparse.ArgumentParser()
parser.add_argument('--yfcc_autotags_file', default='data/yfcc100m_pgh_autotagged.csv')
parser.add_argument('--pointmap_file', default='data/pgh_pointmap.csv')
parser.add_argument('--output_file', default='pgh_nghd_autotags_urls.csv')
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

    # this is the final output dict with neighborhood: 'num_photos': x , 'autotags_90plus_minusbaseline': [{'autotag': x, 'score': x, 'examples': x}, ]
    nghd_autotags_urls = dict()
    overall_autotags_90plus = collections.Counter()
    for row in csv.reader(open(args.yfcc_autotags_file)):
        photo_id, nsid, lat, lon, url = row[0:5]
        nghd = pgh_pointmap[lat, lon]
        # autotags_90plus is the autotags for each pic with >=0.9 score
        autotags_90plus = ast.literal_eval(row[5])
        autotags = row[6].split(',')
        autotags_ctr = collections.Counter()
        if nghd not in nghd_autotags_urls: nghd_autotags_urls[nghd] = dict()
        for tag in autotags:
            if tag == '':
                continue
            else:
                tagname, value = tag.split(':')
                nghds_autotags[nghd][tagname] += round(float(value), 3) 
                if tagname in nghd_autotags_urls[nghd]: 
                    nghd_autotags_urls[nghd][tagname] += [url]
                else: 
                    nghd_autotags_urls[nghd][tagname] = [url]
        #'NUM_PHOTOS' is number of photos of that neighborhood            
        nghds_autotags[nghd]['NUM_PHOTOS'] += 1
        #put in 'NUM_PHOTOS' to nghds_autotags90plus
        nghds_autotags90plus[nghd].update(autotags_90plus + ['NUM_PHOTOS'])
        #put in 'NUM_PHOTOS', autotags_90plus to overall_autotags_90plus
        overall_autotags_90plus.update(autotags_90plus + ['NUM_PHOTOS'])
        # this looks like Counter({'NUM_PHOTOS': 15, 'outdoor': 5, 'building':
        # 2, 'gable': 2, 'nature': 2, 'indoor': 2, 'plant': 2, 'architecture':
        # 2, 'pink': 1, 'vehicle': 1, 'house': 1, 'pediment': 1, 'frieze': 1,
        # 'flower': 1, 'green': 1, 'suit': 1, 'banana tree': 1, 'car': 1})

    # Compute the overall rates of each tag, so we can subtract them off.
    tempdict = collections.Counter()
    for tag, value in overall_autotags_90plus.items():
        tempdict[tag] = (value*1.0/overall_autotags_90plus['NUM_PHOTOS'])
    del tempdict['NUM_PHOTOS']
    overall_autotags_90plus = tempdict
    sorted_output = dict()
    output = dict()
    for nghd, autotags90plus in nghds_autotags90plus.items():
    	sorted_output[nghd] = dict() #this is output with the max 10 autotags
        sorted_output[nghd]["autotags_90plus_minusbaseline"] = list()
        autotags = nghds_autotags[nghd]
        # Counter({'NUM_PHOTOS': 1, 'indoor': 0.925, 'people': 0.895, 'blue':
        # 0.695, 'sleeping': 0.674})
        num_photos = autotags90plus['NUM_PHOTOS']
        sorted_output[nghd]['NUM_PHOTOS'] = num_photos
        output[nghd] = {'num_photos': num_photos, #'autotags_90plus': {}, 'autotags_all': {}, 
        'autotags_90plus_minusbaseline':{}}
            # 'autotags_90plus': [], 'autotags_all': []}
        for autotag, count in autotags90plus.most_common():
            if autotag == 'NUM_PHOTOS':
                continue
            pct_photos = round(count * 1.0 / num_photos, 5)
            # output[nghd]['autotags_90plus'][autotag] = pct_photos
            # output[nghd]['autotags_90plus'].append((autotag, round(count*1.0/num_photos, 5)))
            # for each neighborhood, find the max 10 autotags
            output[nghd]['autotags_90plus_minusbaseline'][autotag] = round(pct_photos - overall_autotags_90plus[autotag], 5)
        #figiure out the top 10 autotags for each output[neighborhood]['autotags_90plus_minusbaseline'] which is a dict of tag:pct
        sorted_output[nghd]['autotags_90plus_minusbaseline'] = dict(sorted(output[nghd]['autotags_90plus_minusbaseline'].iteritems(), key=operator.itemgetter(1), reverse=True)[:10])
   
    ###-------now add the urls to sorted output -------------
    # this is the final output, with sorted top 10 autotags and urls
    output_autotag_url = dict()
    for nghd in sorted_output: 
        output_autotag_url[nghd] = dict()
        output_autotag_url[nghd]['autotags_90plus_minusbaseline'] = list()
        output_autotag_url[nghd]['NUM_PHOTOS'] = sorted_output[nghd]['NUM_PHOTOS']
        for tag in sorted_output[nghd]['autotags_90plus_minusbaseline']: 
            if tag == 'indoor' or tag == 'outdoor': 
                output_autotag_url[nghd][tag] = sorted_output[nghd]['autotags_90plus_minusbaseline'][tag]
                continue
            urls = nghd_autotags_urls[nghd][tag]
            score = sorted_output[nghd]['autotags_90plus_minusbaseline'][tag]
            output_autotag_url[nghd]['autotags_90plus_minusbaseline'] += [{'autotag': tag, 'score': score, 'example_url': urls}]
    json.dump(output_autotag_url, open(args.output_file, 'w'))
