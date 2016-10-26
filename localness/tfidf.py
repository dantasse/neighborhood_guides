#!/usr/bin/env python

# Running TF-iDF on words per neighborhood... yes, again.
# Needs: data/(city)/nghd_tweets.json

import argparse, csv, collections, json, ujson, os, time, math, util.cities
parser = argparse.ArgumentParser()
parser.add_argument('--city', default='pgh', choices=util.cities.CITY_NAMES)
parser.add_argument('--skip_single_words', action='store_false') # default true
parser.add_argument('--output_file', default='data/pgh/tweet_tfidf.json')
args = parser.parse_args()

if __name__ == '__main__':
    print "%s\tLoading json." % time.asctime()
    # data/pgh/nghd_tweets.json, for example.
    jsondata = ujson.load(open('data%s%s%s%s' %\
            (os.sep, args.city, os.sep, 'nghd_tweets.json')))

    print "%s\tDone loading json, counting words." % time.asctime()
    nghd_counts = collections.defaultdict(collections.Counter)
    for nghd, tweets in jsondata.iteritems():
        if nghd == 'None':
            continue
        for tweet in tweets:
            nghd_counts[nghd].update(list(set(tweet))) # unique words per tweet.

    print "%s\tDone counting words." % time.asctime()
    print "%s\tCounting neighborhoods each word is in." % time.asctime()

    word_in_how_many_nghds = collections.Counter()
    for nghd, counter in nghd_counts.iteritems():
        for word in counter.keys():
            word_in_how_many_nghds[word] += 1


    print "%s\tComputing TF-IDF." % time.asctime()
    for nghd, counter in nghd_counts.iteritems():
        for word in counter.keys():
            if counter[word] == 1 and args.skip_single_words:
                del counter[word]
            else:
                tfidf = math.log(counter[word]) / word_in_how_many_nghds[word]
                counter[word] = round(tfidf, 5)
            # counter[word] *= 1.0 / word_in_how_many_nghds[word]

    # print overall_counts.most_common(50)
    # print nghd_counts['Shadyside'].most_common(50)
    # print tweets['Shadyside']
    output = {}
    for nghd, counter in nghd_counts.iteritems():
        output[nghd] = counter.items()

    json.dump(output, open(args.output_file, 'w'))
