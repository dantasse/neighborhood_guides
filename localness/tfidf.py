#!/usr/bin/env python

# Running TF-iDF on words per neighborhood... yes, again.
# Needs: data/(city)/nghd_tweets.json

import argparse, csv, collections, json, ujson, os, time, math, util.cities
parser = argparse.ArgumentParser()
parser.add_argument('--nghd_tweets_file', default='data/pgh/nghd_tweets.json')
parser.add_argument('--top10_output_file', default='data/pgh/tweet_tfidf_top10.json')
args = parser.parse_args()

def get_context_tweets(all_tweets, nghd, word):
    """ Given a word and a neighborhood, find up to 10 full texts of tweets in
    that neighborhood that have that word. """
    context_tweets = []
    for tweet in all_tweets[nghd]:
        if word in tweet['words']:
            context_tweets.append(tweet['fulltext'])
            if len(context_tweets) >= 10:
                break
    return context_tweets

if __name__ == '__main__':
    print "%s\tLoading json." % time.asctime()
    # data/pgh/nghd_tweets.json, for example.
    jsondata = ujson.load(open(args.nghd_tweets_file))

    print "%s\tDone loading json, counting words." % time.asctime()
    # nghd -> (word -> set of ppl using it)
    # lambda function: trick to do nested defaultdicts
    nghd_word_users = collections.defaultdict(lambda: collections.defaultdict(set))
    for nghd, tweets in jsondata.iteritems():
        if nghd == 'None':
            continue
        for tweet in tweets:
            words = tweet['words']
            for word in words:
                nghd_word_users[nghd][word].add(tweet['username'])

    nghd_counts = collections.defaultdict(collections.Counter)
    # nghd -> (word -> count)
    for nghd, word_users in nghd_word_users.iteritems():
        for word, users in word_users.iteritems():
            nghd_counts[nghd][word] = len(users)

    print "%s\tDone counting words." % time.asctime()
    print "%s\tCounting neighborhoods each word is in." % time.asctime()

    word_in_how_many_nghds = collections.Counter()
    for nghd, counter in nghd_counts.iteritems():
        for word in counter.keys():
            word_in_how_many_nghds[word] += 1

    print "%s\tComputing TF-IDF." % time.asctime()
    for nghd, counter in nghd_counts.iteritems():
        for word in counter.keys():
            tfidf = math.log(counter[word]) / word_in_how_many_nghds[word]
            counter[word] = round(tfidf, 5)

    top10_output = {}
    for nghd, counter in nghd_counts.iteritems():
        top10_words = counter.most_common(10)
        top10_output[nghd] = []
        for word, score in counter.most_common(10):
            context_tweets = get_context_tweets(jsondata, nghd, word)
            top10_output[nghd].append({'word': word, 'context': context_tweets, 'score': score})

    json.dump(top10_output, open(args.top10_output_file, 'w'))
