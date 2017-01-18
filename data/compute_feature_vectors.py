#!/usr/bin/env python

# For each neighborhood in a city, computes all the feature vectors used to make
# similarity calculations.

import argparse, csv, collections, os, numpy as np, pandas as pd, ujson, ast, re, json
from numpy import linalg as LA
from scipy.spatial import distance
from gensim import corpora, similarities
parser = argparse.ArgumentParser()
parser.add_argument('--city1', choices=['pgh', 'sf'], default='pgh')
parser.add_argument('--city2', choices=['pgh', 'sf'], default='sf')
parser.add_argument('--skip_twitter', action='store_true', help='If true, do not \
        compute twitter summaries, in order to save time while debugging.')
# parser.add_argument('--output_file', help='json output', default='nghd_recommendations.json')
# output will go to, e.g. pgh_sf_recommendations.json
args = parser.parse_args()

filenames = {'4sq': 'nghd_4sq.csv', 'autotags': 'yfcc100m.csv',
        'walkscores': 'nghd_walkscores.csv', 'tweets': 'nghd_tweets.json',
        'crimes': 'crimes.csv'}
files1 = {}
filenames1 = {}
files2 = {}
filenames2 = {}
# Argh. This is useful because all of these files have the city listed as one
# of the neighborhoods.
CITY_FULL_NAMES = ['San Francisco', 'Pittsburgh', 'Austin', 'Houston', 'Chicago']

for type, filename in filenames.items():
    files1[type] = open(args.city1 + os.sep + filename)
    filenames1[type] = args.city1 + os.sep + filename
    files2[type] = open(args.city2 + os.sep + filename)
    filenames2[type] = args.city2 + os.sep + filename
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

def read_flickr_file(file):
    """ Returns a dict of nghd -> {tag -> pct of photos in nghd with tag}"""
    nghd_taglists = collections.defaultdict(list)
    # nghd_taglists: nghd -> [[tags for photo 1], [tags for photo 2], ...]
    nghd_tagpcts = collections.defaultdict(dict) # nghd -> {tag -> pct of photos}
    for line in csv.reader(file):
        tags = ast.literal_eval(line[5]) # Slowest part of the thing.
        # Tried to use regexes to speed it up but it didn't get quicker :-/
        nghd = line[7]
        nghd_taglists[nghd].append(tags)
    for nghd, taglists in nghd_taglists.iteritems():
        alltags = set(tag for photo in taglists for tag in photo)
        for tag in alltags:
            photos_with_tag = len([photo for photo in taglists if tag in photo])
            nghd_tagpcts[nghd][tag] = photos_with_tag * 1.0 / len(taglists)
    return nghd_tagpcts
    
flickr_nghds = collections.defaultdict(dict) # nghd -> {tag: value}
def generate_flickr_nghds(file1, file2):
    global flickr_nghds
    print "loading flickr file 1"
    json_nghds_tagvectors_filename = filenames1['autotags'] + '_nghds.json'
    if os.path.isfile(json_nghds_tagvectors_filename):
        print "Already made this, opening: " + json_nghds_tagvectors_filename
        nghd_tags1 = ujson.load(open(json_nghds_tagvectors_filename))
    else:
        nghd_tags1 = read_flickr_file(file1)
        ujson.dump(nghd_tags1, open(json_nghds_tagvectors_filename, 'w'))
    print "loading flickr file 2"
    json_nghds_tagvectors_filename = filenames2['autotags'] + '_nghds.json'
    if os.path.isfile(json_nghds_tagvectors_filename):
        print "Already made this, opening: " + json_nghds_tagvectors_filename
        nghd_tags2 = ujson.load(open(json_nghds_tagvectors_filename))
    else:
        nghd_tags2 = read_flickr_file(file2)
        ujson.dump(nghd_tags2, open(json_nghds_tagvectors_filename, 'w'))
        
    return dict(nghd_tags1.items() + nghd_tags2.items())

def flickr_dissimilarity(nghd1, nghd2):
    global flickr_nghds
    if len(flickr_nghds) == 0:
        flickr_nghds = generate_flickr_nghds(files1['autotags'], files2['autotags'])
    if nghd1 in flickr_nghds:
        nghd1_tags = flickr_nghds[nghd1]
    else:
        nghd1_tags = {}
    if nghd2 in flickr_nghds:
        nghd2_tags = flickr_nghds[nghd2]
    else:
        nghd2_tags = {}

    # So here I'm going with sum of absolute differences, divided by sum of
    # both vectors.
    sum_diffs = 0
    for tag, val1 in nghd1_tags.items():
        val2 = nghd2_tags[tag] if tag in nghd2_tags else 0
        sum_diffs += abs(val1 - val2)
    for tag, val2 in nghd2_tags.items():
        if tag not in nghd1_tags:
            sum_diffs += val2
        # if tag in nghd2_tags:
        #     sum += value * nghd2_tags[tag]
    return sum_diffs/(sum(nghd1_tags.values()) + sum(nghd2_tags.values()))

foursq_lines1 = {line['Neighborhood']: line for line in csv.DictReader(files1['4sq'])}
walkscore_lines1 = {line['Name']: line for line in csv.DictReader(files1['walkscores'])}
crime_lines1 = {line['neighborhood']: line for line in csv.DictReader(files1['crimes'])}
foursq_lines2 = {line['Neighborhood']: line for line in csv.DictReader(files2['4sq'])}
walkscore_lines2 = {line['Name']: line for line in csv.DictReader(files2['walkscores'])}
crime_lines2 = {line['neighborhood']: line for line in csv.DictReader(files2['crimes'])}

dissimilarities = [] # list to later make into a Data Frame
for nghd1 in crime_lines1.keys():
    for nghd2 in crime_lines2.keys():
        if nghd1 in CITY_FULL_NAMES or nghd2 in CITY_FULL_NAMES:
            continue
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
        # print all_dissims
        avg_dissim = sum(all_dissims)/len(all_dissims)
        dissimilarities.append({'nghd1': nghd1, 'nghd2': nghd2, 'type': 'average', 'dissimilarity': avg_dissim})
 
dissimilarities = pd.DataFrame(dissimilarities)

# TODO pick up here
# output a better dissimilarity json I guess, that shows the query we want
# but in the meantime use the data frame to do some nice sorting
print dissimilarities
dissimilarities.to_csv('dissimilarities.csv')

output = {}
df = dissimilarities
for nghd in set(df.ix[:, 'nghd1']):
    this_nghd_output = {}
    nghd1_comparisons = df[df.nghd1 == nghd]
    nghd1_avg_comps = nghd1_comparisons[nghd1_comparisons.type == 'average']
    nghd1_avg_comps = nghd1_avg_comps.sort_values(by='dissimilarity')
    top5 = nghd1_avg_comps[0:5]['nghd2']
    for compare_nghd in top5:
        reasons = nghd1_comparisons[nghd1_comparisons.nghd2 == compare_nghd]
        reasons = reasons[['type', 'dissimilarity']]
        reasons_output = {}
        for row in reasons.itertuples():
            reasons_output[row[1]] = round(row[2], 3)
        this_nghd_output[compare_nghd] = reasons_output
    output[nghd] = this_nghd_output
json.dump(output, open(args.city1 + '_' + args.city2 + '_recommendations.json', 'w'))

output = {}
# Argh now back the other way. For each nghd2, find the closest nghd1.
for nghd in set(df.ix[:, 'nghd2']):
    this_nghd_output = {}
    nghd2_comparisons = df[df.nghd2 == nghd]
    nghd2_avg_comps = nghd2_comparisons[nghd2_comparisons.type == 'average']
    nghd2_avg_comps = nghd2_avg_comps.sort_values(by='dissimilarity')
    top5 = nghd2_avg_comps[0:5]['nghd1']
    for compare_nghd in top5:
        reasons = nghd2_comparisons[nghd2_comparisons.nghd1 == compare_nghd]
        reasons = reasons[['type', 'dissimilarity']]
        reasons_output = {}
        for row in reasons.itertuples():
            reasons_output[row[1]] = row[2]
        this_nghd_output[compare_nghd] = reasons_output
    output[nghd] = this_nghd_output
json.dump(output, open(args.city2 + '_' + args.city1 + '_recommendations.json', 'w'))

    


