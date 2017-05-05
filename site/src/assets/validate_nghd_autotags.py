#!/usr/bin/env python

# For each Flickr URL, see if it's actually there or been changed to "no longer
# available." Spit out a copy of the input file with the "no longer availables"
# removed.

import argparse, csv, collections, requests, json
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--input_file', default='pgh/nghd_autotags.json', help=' ')
parser.add_argument('--output_file', default='pgh/nghd_autotags_validated.json', help=' ')
args = parser.parse_args()

all_urls = json.load(open(args.input_file))

for nghd in all_urls:
    print nghd
    for autotag in all_urls[nghd]['autotags_90plus_minusbaseline']:
        examples = autotag['example_url']
        good_urls = []
        for url in examples:
            a = requests.get(url)
            if a.url == 'https://s.yimg.com/pw/images/en-us/photo_unavailable.png':
                print "bad one"
            else:
                good_urls.append(url)
        autotag['example_url'] = good_urls
json.dump(all_urls, open(args.output_file, 'w'), indent=2)
