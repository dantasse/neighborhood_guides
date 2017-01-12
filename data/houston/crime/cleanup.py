#!/usr/bin/env python

# Ok, so sometimes they put in an address wrong, so it gets classified as some
# nonsense. But they still have Beats listed for each row. So we say, if one
# police beat is 99% in neighborhood X, but then we have some 'None's, then
# put those 'None's in neighborhood X.

# Edit: nah, y'know what, this isn't really needed. We don't have that many
# Nones that we can easily/automatically correct.

import argparse, csv, collections
parser = argparse.ArgumentParser()
parser.add_argument('--input_file', default='all15_new_geocoded.csv')
parser.add_argument('--output_file', default='all15_new_geocoded_cleaned.csv')

args = parser.parse_args()

beats_rows = collections.defaultdict(list)
for line in csv.reader(open(args.input_file)):
    beat = line[3]
    beats_rows[beat].append(line)

for beat, crimes in beats_rows.iteritems():
    nghds = collections.Counter()
    for crime in crimes:
        nghd = crime[13]
        nghds[nghd] += 1

    majority = nghds.most_common(1)
    print beat
    print len(crimes)
    print majority[0][1]
    print majority[0][1] * 1.0/len(crimes)
    print nghds

