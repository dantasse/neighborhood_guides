#!/usr/bin/env python

# Train a doc2vec model on tweets.

import argparse, csv, collections, ujson, json, time, gensim, util.cities
from gensim.models import doc2vec
parser = argparse.ArgumentParser()
parser.add_argument('--city', nargs='+', default=['pgh'], choices=util.cities.CITY_LOCATIONS)
parser.add_argument('--model_output_file', default='localness/doc2vec_model')
args = parser.parse_args()

NGHD_TWEETS_FILE='nghd_tweets.json' # so, sf's file is in data/sf/nghd_tweets.json.

def flatten(lol):
    output = []
    for list in lol:
        output.extend(list)
    return output

if __name__ == '__main__':
    assert doc2vec.FAST_VERSION > -1 # Apparently it is unusably slow otherwise.
    sentences = []
    for city in args.city:
        print "%s\tLoading tweets from city: %s" % (time.asctime(), city)
        nghd_tweets = ujson.load(open('data/%s/%s' % (city, NGHD_TWEETS_FILE)))
        print "%s\tDone loading tweets for city: %s" % (time.asctime(), city)
        for nghd, tweet_words in nghd_tweets.iteritems():
            words_flattened = flatten(tweet_words)
            sentences.append(doc2vec.LabeledSentence(words=words_flattened,
                tags=['CITY_' + city, 'NGHD_' + nghd]))
        

    # This below is all from https://rare-technologies.com/doc2vec-tutorial/
    print "%s\tbuilding vocab" % time.asctime()
    model = doc2vec.Doc2Vec(size=100, min_count=2, alpha=0.025, min_alpha=0.025, max_vocab_size=30000, workers=4)
    model.build_vocab(sentences)

    # print "%s\tdone building vocab, this many words: %s" % (time.asctime(), model.
    for epoch in range(10):
        print "%s\ttraining epoch %s" % (time.asctime(), epoch)
        model.train(sentences)
        model.alpha -= 0.002
        model.min_alpha = model.alpha
    model.save(args.model_output_file)

    docvecs_outfile = csv.writer(open(args.model_output_file + '_docvecs', 'w'))
    for i in range(len(model.docvecs.doctags)):
        tagname = model.docvecs.index_to_doctag(i)
        vec = model.docvecs[i]
        docvecs_outfile.writerow([tagname] + list(vec))

