# Methods to format text from tweets.

from ark_twokenize_py import twokenize

# We want to ignore links, people's usernames, ... anything else?
def is_stopword(word):
    return word.startswith('http') or word.startswith('@')

# Obviously this is super heuristic-based, but it's the best we've got for now.
def is_spammer(username):
    username_lower = username.lower()
    for jobword in ['job', 'career', 'tmj', 'join', 'workat', 'recruit', 'soliant']:
        if jobword in username_lower:
            return True
    return False

def format(text):
    text = text.replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<")
    words = twokenize.tokenize(text.lower())
    return_words = [w for w in words if not is_stopword(w)]
    return return_words
