# `data`

Not all data in this file might be checked in to git. (It's not usually a good practice to check in big files.)

## Organization
One directory per city. Then hopefully we'll have the same data in each directory.

## Neighborhood Boundaries
`sf/sf_planning_neighborhoods.json` is from the SF Department of City Planning, [link](https://data.sfgov.org/Geographic-Locations-and-Boundaries/Neighborhood-Groups-Map/qc6m-r4ih)

`sf/sffind_neighborhoods.json` is from the SF Mayor's Office, [link](https://data.sfgov.org/Geographic-Locations-and-Boundaries/SFFind-Neighborhoods/ejmn-jyk6). It is finer-grained than the Planning department neighborhoods.

`pgh/Pittsburgh_Neighborhoods.geojson` is from the City of Pittsburgh, [link](https://data.wprdc.org/dataset/pittsburgh-neighborhoods2de67)

`usa_cities.geojson` is from Mapzen, [link](https://mapzen.com/data/borders/)

## Safety

`pgh/crimes.csv` is from [this report](http://apps.pittsburghpa.gov/pghbop/ANNUAL_REPORT_DRAFT_2015_May_31.pdf). (for now I think this is the most straightforward to use. Other sources are in `other_crime`.

"Type 1": Homicide, rape, aggravated assault, robbery, theft, burglary, motor vehicle theft, arson. "Type 2": Simple assault, vandalism, drug violations, fraud, disorderly conduct, drunk driving, forgery, weapons violations, prostitution, public intoxication, other.

## Convenience

`nghd_walkscores` - I think I manually scraped this at one point?

## Localness

`tweets.csv` is just a dump of the tweet tables, which is to say, all the coordinate-geotagged tweets in each city since sometime in 2014/15 depending on city. [More details](talesnideas.blogspot.com/2016/02/welcome-to-domo.html)

## Liveliness

Foursquare venue data in `4sq_venues.json`. Yelp data (which is way more limited - has Pgh but not any of our other cities, and has 4k businesses instead of the 46k I found in Foursquare - so we're probably not using it) from the [Yelp academic dataset](https://www.yelp.com/dataset_challenge/dataset).

## Aesthetics
`yfcc100m.csv` is all the yfcc100m photos in Pittsburgh. `nghd_autotags.json` is the top 10 autotags for each neighborhood.

The directory `yfcc100m_autotagged` is to store YFCC100M dumps from other cities, just so I don't have to compute them again.
