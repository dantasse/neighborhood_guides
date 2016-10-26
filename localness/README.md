Input: tweets in a city.
Output: a "representative" feature vector of twitter words for that nghd?

Before running, get: (e.g. for Pittsburgh)

- `data/pgh/tweets.csv` (can be created with [`dump_tweets` on github](https://github.com/dantasse/dump_tweets))
- `data/pgh/pointmap.csv` (from [`pointmap` on github](https://github.com/dantasse/pointmap) if necessary)

Usage: (e.g. for Pittsburgh)

    cd .. # start at the top-level neighborhood_guides directory
    source env/bin/activate # or virtualenv env && pip install -r requirements.txt
    python -m localness.tweets_to_documents --city_tweets_file=data/pgh/tweets.csv --pointmap_file=data/pgh/pointmap.csv --output_file=data/pgh/nghd_tweets.json
    python -m localness.tfidf --city=pgh --output_file=data/pgh/tweet_tfidf.json

To train doc2vec:

    python -m localness.train_doc2vec --city pgh sf --model_output_file=localness/doc2vec.model

To do a tSNE plot of these vectors (don't expect miracles, it's kind of a hairball), run `jupyter notebook` and open `plot_tsne_pca.ipynb`.
