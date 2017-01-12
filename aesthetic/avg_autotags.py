#!/usr/bin/env python

# Simplest version: get the average autotag for each neighborhood.

import argparse, csv, collections, ast, json, operator, random, requests
from util import pointmap

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--yfcc_autotags_file', default='data/pgh/yfcc100m.csv', help=' ')
parser.add_argument('--pointmap_file', default='data/pgh/pointmap.csv', help=' ')
parser.add_argument('--output_file', default='data/pgh/nghd_autotags.json', help=' ')
args = parser.parse_args()

# Tags that are meaningless so let's not include them at all.
STOPTAGS = ['photo border', 'blackandwhite', 'depth of field', 'monochrome', 'head']

def is_good_url(url_to_test):
    """ Check a URL to see if there's actually a photo there (and it's not a
    video) """
    resp = requests.get(url_to_test)
    if 'photo_unavailable' in resp.url or 'video' in resp.url:
        return False
    else:
        return True

if __name__ == '__main__':
    pgh_pointmap = pointmap.Pointmap(args.pointmap_file)
    # Neighborhood -> counter of # of times an autotag shows up.
    # e.g. 'Upper Lawrenceville': Counter({'indoor': 197', 'text': 125, ...})
    nghds_autotags90plus = collections.defaultdict(collections.Counter)

    # this is the final output dict with neighborhood: 'num_photos': x , 'autotags_90plus_minusbaseline': [{'autotag': x, 'score': x, 'examples': x}, ]
    nghd_autotags_urls = collections.defaultdict(dict)

    overall_autotags_90plus = collections.Counter()
    for row in csv.reader(open(args.yfcc_autotags_file)):
        photo_id, nsid, lat, lon, url = row[0:5]
        nghd = pgh_pointmap[lat, lon]

        # autotags_90plus is the autotags for each pic with >=0.9 score
        autotags_90plus = ast.literal_eval(row[5])
        autotags_90plus = filter(lambda x: x not in STOPTAGS, autotags_90plus)

        #'NUM_PHOTOS' is number of photos of that neighborhood            
        nghds_autotags90plus[nghd].update(autotags_90plus + ['NUM_PHOTOS'])
        #put in 'NUM_PHOTOS', autotags_90plus to overall_autotags_90plus
        overall_autotags_90plus.update(autotags_90plus + ['NUM_PHOTOS'])
        # this looks like Counter({'NUM_PHOTOS': 15, 'outdoor': 5, 'building':
        # 2, 'gable': 2, 'nature': 2, 'indoor': 2, 'plant': 2, etc.})

        for tag in autotags_90plus:
            if tag in nghd_autotags_urls[nghd]: 
                nghd_autotags_urls[nghd][tag].append(url)
            else: 
                nghd_autotags_urls[nghd][tag] = [url]


    # Compute the overall rates of each tag, so we can subtract them off.
    tempdict = collections.Counter()
    for tag, value in overall_autotags_90plus.items():
        tempdict[tag] = (value*1.0/overall_autotags_90plus['NUM_PHOTOS'])
    del tempdict['NUM_PHOTOS']
    overall_autotags_90plus = tempdict
    sorted_output = dict()
    output = dict()
    for nghd, autotags90plus in nghds_autotags90plus.items():
        num_photos = autotags90plus['NUM_PHOTOS']

        # This is output with the max 10 autotags.
        sorted_output[nghd] = {'autotags_90plus_minusbaseline': {},
                'NUM_PHOTOS': num_photos, 'num_indoor': 0, 'num_outdoor': 0}

        for autotag, count in autotags90plus.most_common():
            if autotag == 'NUM_PHOTOS':
                continue
            elif autotag == 'outdoor':
                sorted_output[nghd]['num_outdoor'] += count
            elif autotag == 'indoor':
                sorted_output[nghd]['num_indoor'] += count
            pct_photos = round(count * 1.0 / num_photos, 5)

            # for each neighborhood, find the max 10 autotags
            sorted_output[nghd]['autotags_90plus_minusbaseline'][autotag] = round(pct_photos - overall_autotags_90plus[autotag], 5)
        # figure out the top 10 autotags for each output[neighborhood]['autotags_90plus_minusbaseline'] which is a dict of tag:pct
        sorted_output[nghd]['autotags_90plus_minusbaseline'] = \
                dict(sorted(sorted_output[nghd]['autotags_90plus_minusbaseline'].iteritems(), 
                    key=operator.itemgetter(1), reverse=True)[:10])
   
    ###-------now add the urls to sorted output -------------
    # this is the final output, with sorted top 10 autotags and urls
    output_autotag_url = dict()
    for nghd in sorted_output: 
        print "Getting URLs for %s" % nghd
        output_autotag_url[nghd] = {'autotags_90plus_minusbaseline': [],
                'NUM_PHOTOS': sorted_output[nghd]['NUM_PHOTOS'],
                'num_indoor': sorted_output[nghd]['num_indoor'],
                'num_outdoor': sorted_output[nghd]['num_outdoor']}

        for tag in sorted_output[nghd]['autotags_90plus_minusbaseline']: 
            urls = nghd_autotags_urls[nghd][tag]
            # Add only 10 random URLs; that will be enough sample photos.
            if len(urls) > 10:
                urls = random.sample(urls, 10)
            # Actually GET each photo to make sure it's still there and isn't
            # "This photo has been removed."
            urls = filter(lambda u: is_good_url(u), urls)

            score = sorted_output[nghd]['autotags_90plus_minusbaseline'][tag]
            output_autotag_url[nghd]['autotags_90plus_minusbaseline'] += [{'autotag': tag, 'score': score, 'example_url': urls}]

    json.dump(output_autotag_url, open(args.output_file, 'w'))
