# What I did here

- Download each month Excel file from data.ohouston.org (site down now so I don't remember the exact URL)
- Save them all as CSVs, one at a time
- Smash them together with `cat *.csv > all15.csv`
- Change \r to \n with `tr '\r' '\n' < all15.csv > all15_new.csv`
- There were still only a couple goofs - the last line of each file didn't have a newline so it just ended with a `<feff>` character and then started the next line. `add_full_addr.py` fixed that, along with concatenating a couple columns so there were legit addresses.
- ignore `make_batches.py`; that was for trying to use the here.com geocoder
- Run `geocode.py` - input is `all15_new.csv`, output is `all15_new_geocoded.csv` - this uses Mapbox's geocoder
- run `create_final_output.py` (using `../walkscores.csv` for populations) to make a csv with one row per neighborhood - call that `crimes.csv`
- go into crimes.csv in excel and add one more line for Houston as a whole.

There are going to be errors in this - often the street addresses entered are not very good. In fact, I tried to clean them up (see `cleanup.py`) using police "beat"s - if 90% of a beat is in neighborhood X, then a "none" in that same neighborhood should probably be classified as neighborhood X too. But a lot of the beats cross neighborhoods, and there aren't that many "none"s or mistakes anyway. Limitation of data entry, etc.

Old versions of all15.csv and `all15_new_geotagged.csv` are in `sources.tar.gz` - it took a while to put them together so I want to save them in case I need them again.
