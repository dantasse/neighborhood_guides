#!/usr/bin/env python

# For each neighborhood in a city, computes all the feature vectors used to make
# similarity calculations.

import argparse, csv, collections, os, numpy as np, pandas as pd, ujson
from numpy import linalg as LA
from scipy.spatial import distance
from gensim import corpora, similarities
parser = argparse.ArgumentParser()
parser.add_argument('--city1', choices=['pgh', 'sf'], default='pgh')
parser.add_argument('--city2', choices=['pgh', 'sf'], default='sf')
parser.add_argument('--skip_twitter', action='store_true', help='If true, do not \
        compute twitter summaries, in order to save time while debugging.')
parser.add_argument('--output_file', help='json output', default='city_vectors.json')
args = parser.parse_args()

filenames = {'4sq': 'nghd_4sq.csv', 'autotags': 'nghd_autotags.json',
        'walkscores': 'nghd_walkscores.csv', 'tweets': 'nghd_tweets.json',
        'crimes': 'crimes.csv'}
files1 = {}
files2 = {}
for type, filename in filenames.items():
    files1[type] = open(args.city1 + os.sep + filename)
    files2[type] = open(args.city2 + os.sep + filename)
    # quit fast if any of those files are missing.

def normalize(vector):
    vector = np.array(vector)
    return vector / LA.norm(vector)

twitter_docs = collections.defaultdict(list) # nghd -> list of tokens
twitter_dictionary = None
twitter_index = None
twitter_nghd_to_index = {}

def generate_twitter_docs(file1, file2):
    global twitter_docs, twitter_dictionary, twitter_index
    print "loading twitter file 1"
    tweets1 = ujson.load(file1)
    print "loading twitter file 2"
    tweets2 = ujson.load(file2)
    # counter = 0
    for nghd, tweets in tweets1.items() + tweets2.items():
        nghd_words = [word for t in tweets for word in t['words']]
        twitter_docs[nghd] = nghd_words
        # twitter_nghd_to_index[nghd] = counter # this seems hacky but I can't
        # figure out how else to get the index back. Like you'll get
        # twitter_index[twitter_docs['Shadyside']] but 
        # counter += 1

    twitter_dictionary = corpora.Dictionary(twitter_docs.values())
    twitter_dictionary.save('cities_twitter.dict')
    for nghd, tweets in twitter_docs.items():
        twitter_docs[nghd] = twitter_dictionary.doc2bow(tweets)
    twitter_index = similarities.docsim.Similarity('foo', twitter_docs.values(), num_features = len(twitter_dictionary))

def twitter_dissimilarity(nghd1, nghd2):
    """ """
    if nghd1 == 'San Francisco' or nghd2 == 'San Francisco':
        return 0 # TODO
    global twitter_docs, twitter_dictionary, twitter_index
    if len(twitter_docs) == 0:
        generate_twitter_docs(files1['tweets'], files2['tweets'])
    similarity = twitter_index[twitter_docs[nghd1]][twitter_docs.keys().index(nghd2)]
    return 1 - similarity

def foursquare_dissimilarity(nghd1, nghd2):
    """ each |nghd| is a 6-element dict w area, all, food, nightlife, arts,
    shop, outdoors """
    vec1 = []
    vec2 = []
    for item in ['Food', 'Nightlife Spot', 'Arts and Entertainment',
            'Shop & Service', 'Outdoors & Recreation']:
        vec1.append(float(nghd1[item]) / float(nghd1['Area in Sq Mi']))
        vec2.append(float(nghd2[item]) / float(nghd2['Area in Sq Mi']))
    vec1 = normalize(vec1)
    vec2 = normalize(vec2)

    return distance.euclidean(vec1, vec2)

def walkscore_dissimilarity(nghd1, nghd2):
    """ Here each nghd has 3 numbers: walkscore, transitscore, bikescore. """
    vec1 = []
    vec2 = []
    for item in ['Walk Score', 'Transit Score', 'Bike Score']:
        vec1.append(float(nghd1[item]) / 100)
        vec2.append(float(nghd2[item]) / 100)
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return distance.euclidean(vec1, vec2)

def crime_dissimilarity(nghd1, nghd2):
    """ Value here is just the ratio of crimes between the 2 neighborhoods,
    subtracted from 1. So if one place has 100 crimes per 1000 ppl and the
    other has 300 crimes, 100/300 = 0.33, 1-0.33 = 0.67.
    This provides a nice number between 0 and 1. Similar crime rates: closer to
    0; very different crime rates: closer to 1. """
    if nghd1['total_per_1000_ppl'] == '' or nghd2['total_per_1000_ppl'] == '':
        # I guess some cities don't report part 1 and part 2 crimes.
        # In that case, just use the part 1 crimes.
        total1 = float(nghd1['part1_per_1000_ppl'])
        total2 = float(nghd2['part1_per_1000_ppl'])
    else:
        total1 = float(nghd1['total_per_1000_ppl'])
        total2 = float(nghd2['total_per_1000_ppl'])
    return 1 - min(total1 / total2, total2 / total1)


flickr_nghds = collections.defaultdict(dict) # nghd -> {tag: value}
def generate_flickr_nghds(file1, file2):
    global flickr_nghds
    print "loading flickr file 1"
    autotags1 = ujson.load(file1)
    print "loading flickr file 2"
    autotags2 = ujson.load(file2)
    for nghd, nghd_info in autotags1.items() + autotags2.items():
        # nghd_info, e.g. {'autotags_90plus_minusbaseline': [
        #   {'autotag': 'people', 'score': 0.085}
        #   {'autotag': 'road', 'score': 0.042}, ...]}}
        tags = {t['autotag']: float(t['score']) for t in nghd_info['autotags_90plus_minusbaseline']}
        flickr_nghds[nghd] = tags 
 
def flickr_dissimilarity(nghd1, nghd2):
    global flickr_nghds
    if len(flickr_nghds) == 0:
        generate_flickr_nghds(files1['autotags'], files2['autotags'])
    # just dot-product the two neighborhoods.
    sum = 0
    for tag, value in flickr_nghds[nghd1].items():
        if tag in flickr_nghds[nghd2]:
            sum += value * flickr_nghds[nghd2][tag]
    return 1 - sum

foursq_lines1 = {line['Neighborhood']: line for line in csv.DictReader(files1['4sq'])}
walkscore_lines1 = {line['Name']: line for line in csv.DictReader(files1['walkscores'])}
crime_lines1 = {line['neighborhood']: line for line in csv.DictReader(files1['crimes'])}
foursq_lines2 = {line['Neighborhood']: line for line in csv.DictReader(files2['4sq'])}
walkscore_lines2 = {line['Name']: line for line in csv.DictReader(files2['walkscores'])}
crime_lines2 = {line['neighborhood']: line for line in csv.DictReader(files2['crimes'])}

dissimilarities = [] # list to later make into a Data Frame
for nghd1 in crime_lines1.keys():
    foursq_dissimilarities = {}
    walkscore_dissimilarities = {}
    for nghd2 in crime_lines2.keys():
        
        foursq_dissim= foursquare_dissimilarity(foursq_lines1[nghd1], foursq_lines2[nghd2])
        dissimilarities.append({'nghd1': nghd1, 'nghd2': nghd2, 'type': '4sq', 'dissimilarity': foursq_dissim})

        walkscore_dissim = walkscore_dissimilarity(walkscore_lines1[nghd1], walkscore_lines2[nghd2])
        dissimilarities.append({'nghd1': nghd1, 'nghd2': nghd2, 'type': 'walkscore', 'dissimilarity': walkscore_dissim})

        crime_dissim = crime_dissimilarity(crime_lines1[nghd1], crime_lines2[nghd2])
        dissimilarities.append({'nghd1': nghd1, 'nghd2': nghd2, 'type': 'crime', 'dissimilarity': crime_dissim})
        
        if args.skip_twitter:
            twitter_dissim = 0
        else:
            twitter_dissim = twitter_dissimilarity(nghd1, nghd2)
        dissimilarities.append({'nghd1': nghd1, 'nghd2': nghd2, 'type': 'twitter', 'dissimilarity': twitter_dissim})

        flickr_dissim = flickr_dissimilarity(nghd1, nghd2)
        dissimilarities.append({'nghd1': nghd1, 'nghd2': nghd2, 'type': 'flickr', 'dissimilarity': flickr_dissim})

        all_dissims = [foursq_dissim, walkscore_dissim, crime_dissim, twitter_dissim, flickr_dissim]
        print all_dissims
        avg_dissim = sum(all_dissims)/len(all_dissims)
        dissimilarities.append({'nghd1': nghd1, 'nghd2': nghd2, 'type': 'average', 'dissimilarity': avg_dissim})
 
    # print twitter_index[twitter_docs[nghd1]]
    # print sorted(dissimilarities.items(), key=lambda x: x['average'])
dissimilarities = pd.DataFrame(dissimilarities)

# TODO pick up here
# output a better dissimilarity json I guess, that shows the query we want
# but in the meantime use the data frame to do some nice sorting
print dissimilarities
dissimilarities.to_csv('dissimilarities.csv')
