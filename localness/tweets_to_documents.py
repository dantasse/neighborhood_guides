#!/usr/bin/env python

# Take in a dump of all the tweets in a city. Split it into neighborhoods and
# spit out a JSON file that has all the text, tweet by tweet, for each nghd.

import argparse, csv, collections, ast, json, os, multiprocessing, io
from util import pointmap, tweetutil

parser = argparse.ArgumentParser()
parser.add_argument('--city_tweets_file', default='data/tweet_pgh_with_text.csv')
parser.add_argument('--pointmap_file', default='data/pgh_pointmap.csv')
parser.add_argument('--output_file', default='pgh_nghd_tweets.json')
parser.add_argument('--num_processes', type=int, default=multiprocessing.cpu_count())
args = parser.parse_args()

def process_lines(start, end):
    tweets_file = open(args.city_tweets_file)
    tweets_file.seek(start)

    # Probably throw out the first line b/c you seeked to the middle of it.
    # Unless you didn't! (b/c it's the first line, or you randomly hit the
    # start of a line)
    keep_first_line = False
    if start == 0:
        keep_first_line = True
    else:
        tweets_file.seek(-1, 1) # , 1 means "relative to current location."
        if tweets_file.read(1) == '\n':
            keep_first_line = True

    lines = tweets_file.readlines(end - start)
    print "One process starting, this many lines to read: " + str(len(lines))
    reader = csv.reader(lines)
    if not keep_first_line:
        reader.next()

    nghds_tweettexts_thischunk = collections.defaultdict(list)
    counter = 0
    skipped_rows = []
    for row in reader:
        counter += 1
        if counter % 10000 == 0:
            print "This process processed %s lines" % counter
        username, lon, lat, date, time, text = row
        if tweetutil.is_spammer(username):
            continue

        nghd = pgh_pointmap[lat, lon]
        formatted_text = tweetutil.format(text)

        try:
            json.dumps(formatted_text)
        except UnicodeDecodeError:
            print "UnicodeDecodeError: %s" % text
            skipped_rows.append(row)
            continue

        nghds_tweettexts_thischunk[nghd].append(formatted_text)

    print "Skipped this many: %s" % len(skipped_rows)
    for row in skipped_rows:
        print ','.join(row)

    return nghds_tweettexts_thischunk


if __name__ == '__main__':
    pgh_pointmap = pointmap.Pointmap(args.pointmap_file)
    nghds_tweettexts = collections.defaultdict(list)

    file_size = os.path.getsize(args.city_tweets_file)
    start_indices = [i * file_size / args.num_processes for i in range(args.num_processes)]
    end_indices = start_indices[1:] + [file_size]
    worker_pool = multiprocessing.Pool(args.num_processes)

    results = []
    for i in range(args.num_processes):
        res = worker_pool.apply_async(process_lines, (start_indices[i], end_indices[i]))
        results.append(res)
    for res in results:
        nghds_tweettexts_thatchunk = res.get()
        for nghd, tweettexts in nghds_tweettexts_thatchunk.iteritems():
            nghds_tweettexts[nghd].extend(tweettexts)

    worker_pool.close()
    worker_pool.join()

    print "Dumping to json file"
    json.dump(nghds_tweettexts, open(args.output_file, 'w'))
