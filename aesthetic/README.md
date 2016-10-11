Input: flickr photos and autotags.
Output: a "representative" feature vector of autotags for that neighborhood.

Before running, get: (e.g. for Pittsburgh)

- `data/yfcc100m_dataset`
- `data/yfcc100m_autotags`
- `data/pgh_pointmap.csv` (from [pointmap on github](https://github.com/dantasse/pointmap) if necessary)

Usage: (e.g. for Pittsburgh)

    cd .. # start at the top-level neighborhood_guides directory
    source env/bin/activate
    python -m aesthetic.flickr_in_city --yfcc_file=data/yfcc100m_dataset --city=pgh --output_file=yfcc100m_in_pgh.csv
    python -m aesthetic.add_autotags --city_csv_file=yfcc100m_in_pgh.csv --autotags_file=data/yfcc100m_autotags --output_file=yfcc100m_pgh_autotagged.csv
    python -m aesthetic.avg_autotags --yfcc_autotags_file=yfcc100m_pgh_autotagged.csv --pointmap_file=data/pgh_pointmap.csv --output_file=pgh_nghd_autotags.csv
    
