#!/usr/bin/env python

# Take in a dump of all the tweets in a city. Split it into neighborhoods and
# spit out a JSON file that has all the text, tweet by tweet, for each nghd.
# Single-processor version, because though it is slower, I can't apparently
# do this without bugs :-/

import argparse, csv, collections, ast, json, os
from util import pointmap, tweetutil

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--city_tweets_file', default='data/pgh/tweets.csv', help=' ')
parser.add_argument('--pointmap_file', default='data/pgh/pointmap.csv', help=' ')
parser.add_argument('--output_file', default='pgh_nghd_tweets.json', help=' ')
args = parser.parse_args()

if __name__ == '__main__':
    city_pointmap = pointmap.Pointmap(args.pointmap_file)
    nghds_tweettexts = collections.defaultdict(list)

    reader = csv.reader(open(args.city_tweets_file))
    counter = 0
    skipped_rows = []
    for row in reader:
        counter += 1
        if counter % 100000 == 0:
            print "Processed %s lines" % counter
        username, lon, lat, date, time, text = row
        if tweetutil.is_spammer(username):
            continue

        try:
            nghd = city_pointmap[lat, lon]
        except ValueError as e:
            print "ValueError"
            print row
            print counter
            continue
        formatted_text = tweetutil.format(text)

        try:
            json.dumps(formatted_text)
        except UnicodeDecodeError:
            print "UnicodeDecodeError: %s" % text
            skipped_rows.append(row)
            continue

        nghds_tweettexts[nghd].append({
            'words':formatted_text,
            'fulltext': text,
            'username': username})

    print "Skipped this many: %s" % len(skipped_rows)
    for row in skipped_rows:
        print ','.join(row)

    print "Dumping to json file"
    json.dump(nghds_tweettexts, open(args.output_file, 'w'), indent=2)
