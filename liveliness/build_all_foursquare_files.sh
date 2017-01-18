#!/bin/bash

cd ..

source env/bin/activate

echo "Processing Pittsburgh"
python -m liveliness.process_4sq_venues --foursquare_venue_file=data/pgh/4sq_venues.json --nghd_bounds_file=data/pgh/nghd_bounds.geojson --pointmap_file=data/pgh/pointmap.csv --city_name="Pittsburgh" --output_file=data/pgh/nghd_4sq.csv
echo "Done with Pittsburgh, copying to site/"
cp data/pgh/nghd_4sq.csv site/src/assets/pgh/

echo "Processing SF"
python -m liveliness.process_4sq_venues --foursquare_venue_file=data/sf/4sq_venues.json --nghd_bounds_file=data/sf/nghd_bounds.geojson --pointmap_file=data/sf/pointmap.csv --city_name="San Francisco" --output_file=data/sf/nghd_4sq.csv
cp data/sf/nghd_4sq.csv site/src/assets/sf/
echo "Done with SF, copying to site/"

echo "Processing Houston"
python -m liveliness.process_4sq_venues --foursquare_venue_file=data/houston/4sq_venues.json --nghd_bounds_file=data/houston/nghd_bounds.geojson --pointmap_file=data/houston/pointmap.csv --city_name="Houston" --output_file=data/houston/nghd_4sq.csv
cp data/houston/nghd_4sq.csv site/src/assets/houston/
echo "Done with Houston, copying to site/"

echo "Processing Chicago"
python -m liveliness.process_4sq_venues --foursquare_venue_file=data/chicago/4sq_venues.json --nghd_bounds_file=data/chicago/nghd_bounds.geojson --pointmap_file=data/chicago/pointmap.csv --city_name="Chicago" --output_file=data/chicago/nghd_4sq.csv
cp data/chicago/nghd_4sq.csv site/src/assets/chicago/
echo "Done with Chicago, copying to site/"

echo "Processing Austin"
python -m liveliness.process_4sq_venues --foursquare_venue_file=data/austin/4sq_venues.json --nghd_bounds_file=data/austin/nghd_bounds.geojson --pointmap_file=data/austin/pointmap.csv --city_name="Austin" --output_file=data/austin/nghd_4sq.csv
cp data/austin/nghd_4sq.csv site/src/assets/austin/
echo "Done with Austin, copying to site/"
