#!/usr/bin/env python

# For each Flickr URL, see if it's actually there or been changed to "no longer
# available." Spit out a copy of the input file with the "no longer availables"
# removed.

import argparse, csv, collections, requests, json
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--input_file', default='photo_urls.json', help=' ')
parser.add_argument('--output_file', default='photo_urls_validated.json', help=' ')
args = parser.parse_args()

all_urls = json.load(open(args.input_file))

for city in all_urls:
    for nghd in all_urls[city]:
        print nghd
        for type in all_urls[city][nghd]:
            if 'flickr' not in type:
                continue
            urls_to_check = all_urls[city][nghd][type]
            good_urls = []
            for url in urls_to_check:
                a = requests.get(url)
                if a.url == 'https://s.yimg.com/pw/images/en-us/photo_unavailable.png':
                    print "bad one"
                else:
                    good_urls.append(url)
            all_urls[city][nghd][type] = good_urls
json.dump(all_urls, open(args.output_file, 'w'), indent=2)
