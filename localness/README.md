Input: tweets in a city.
Output: a "representative" feature vector of twitter words for that nghd?

Before running, get: (e.g. for Pittsburgh)

- `data/tweet_pgh_with_text.csv`
- `data/pgh_pointmap.csv` (from [pointmap on github](https://github.com/dantasse/pointmap) if necessary)

Usage: (e.g. for Pittsburgh)

    cd .. # start at the top-level neighborhood_guides directory
    source env/bin/activate
    python -m localness.tweet_to_documents --city_tweets_file=data/tweet_pgh_with_text.csv --pointmap_file=data/pgh_pointmap.csv --output_file=pgh_nghd_tweets.json
    
