# -*- coding: UTF-8 -*-
#
# Methods to format text from tweets.

import re, string
from ark_twokenize_py import twokenize

stopwords = [u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your', u'yours', u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her', u'hers', u'herself', u'it', u'its', u'itself', u'they', u'them', u'their', u'theirs', u'themselves', u'what', u'which', u'who', u'whom', u'this', u'that', u'these', u'those', u'am', u'is', u'are', u'was', u'were', u'be', u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does', u'did', u'doing', u'a', u'an', u'the', u'and', u'but', u'if', u'or', u'because', u'as', u'until', u'while', u'of', u'at', u'by', u'for', u'with', u'about', u'against', u'between', u'into', u'through', u'during', u'before', u'after', u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on', u'off', u'over', u'under', u'again', u'further', u'then', u'once', u'here', u'there', u'when', u'where', u'why', u'how', u'all', u'any', u'both', u'each', u'few', u'more', u'most', u'other', u'some', u'such', u'no', u'nor', u'not', u'only', u'own', u'same', u'so', u'than', u'too', u'very', u's', u't', u'can', u'will', u'just', u'don', u'should', u'now', u'd', u'll', u'm', u'o', u're', u've', u'y', u'ain', u'aren', u'couldn', u'didn', u'doesn', u'hadn', u'hasn', u'haven', u'isn', u'ma', u'mightn', u'mustn', u'needn', u'shan', u'shouldn', u'wasn', u'weren', u'won', u'wouldn'] # from NLTK

spammers = ['rachelmeemken', 'rg_ep', 'teensteem', 'ladacciillumina', 'sydwalsh_', 'jackbranan',]

def is_all_punctuation(word):
    for char in word:
        if char not in string.punctuation:
            return False
    return True

# We want to ignore links, people's usernames, ... anything else?
def is_stopword(word):
    return word in stopwords or word.startswith('http') or word.startswith('@')

# Obviously this is super heuristic-based, but it's the best we've got for now.
def is_spammer(username):
    username_lower = username.lower()
    for jobword in ['job', 'career', 'tmj', 'join', 'workat', 'recruit', 'soliant']:
        if jobword in username_lower:
            return True
    if username_lower in spammers:
        return True
    return False

tcoUrls = re.compile('https?://t.co/[a-zA-Z0-9]+')
def format(text):

    # Replace random stuff that was causing problems with the tokenizer.
    # You might futz with the tokenizer a bit too (as I did) but be careful, it
    # is an unending rabbit hole. As a result, I think I'm skipping about 43
    # tweets out of 4 million from Pittsburgh and I'm just going to skip them.
    text = text.replace("à", "a") # Sorry, French people saying "jusqu'à."
    text = text.replace("•", "*")
    text = text.replace("£", "GBP")
    text = tcoUrls.sub(' ', text) # We don't want URLs anyway.
    text = text.replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<")

    words = twokenize.tokenize(text.lower())
    return_words = [w for w in words if not is_stopword(w) and not is_all_punctuation(w)]
    return return_words
