#!/usr/bin/env python

# Given a file with a bunch of twimg and instagram photos, get each photo.

import argparse, csv, collections, requests, re, time
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--input_file', default='tweet_pgh_images.csv', help=' ')
parser.add_argument('--output_file', default='tweet_pgh_goodimages.csv', help=' ')
parser.add_argument('--pointmap_file', default='pgh/pointmap.csv', help=' ')
args = parser.parse_args()

pointmap = {}
for line in csv.DictReader(open(args.pointmap_file)):
    pointmap[(float(line['lat']), float(line['lon']))] = line['nghd']

writer = csv.writer(open(args.output_file, 'w'))
counter = 0
for line in csv.reader(open(args.input_file)):
    counter += 1
    if counter % 10000 == 0:
        print counter
    url = line[1]
    lat = round(float(line[3]), 3)
    lon = round(float(line[2]), 3)
    if (lat, lon) in pointmap:
        nghd = pointmap[(lat, lon)]
    else:
        nghd = 'None'
    if url.startswith('http://pbs.twimg.com/'):
        good_url = url
    elif 'instagram' in url:
        page = requests.get(url)
        for page_line in page.content.split('\n'):
            matches = re.match('.*meta property="og:image" content="(.*)"', page_line)
            if matches:
                good_url = matches.group(1)
                break
    else:
        print url
    line.append(nghd)
    line.append(good_url)
    writer.writerow(line)

