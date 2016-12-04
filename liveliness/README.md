The goal here is to generate `nghd_4sq.csv`, a list of each neighborhood and how many foursquare venues of each type are there. To do this, you need to download a file of all the foursquare venues in your city, using [`scrape_social_media_in_area`](https://github.com/CMUChimpsLab/scrape_social_media_in_area)`/scrape_foursquare_in_area.py`. Then run `process_4sq_venues.py` with `--foursquare_venue_file=this file you just scraped` (along with a bunch of other files).

`get_4sq_category_tree.py` and `4sq_categories.json` are just a mapping from subcategories (identified by ID) to top-level categories (identified by string name) in the Foursquare categorization scheme.

`split_yelp_by_city.py` is for taking the couple of JSON files from the Yelp dataset and turning them into one file per city. (a mostly failed experiment, we're not using Yelp anymore.)

