# `data`

Not all data in this file might be checked in to git. (It's not usually a good practice to check in big files.)

## Organization
One directory per city. Then hopefully we'll have the same data in each directory.

## Neighborhood Boundaries
`sf/analysis_neighborhoods.json` is from the SF Department of City Planning, [link](https://data.sfgov.org/Geographic-Locations-and-Boundaries/Analysis-Neighborhoods/p5b7-5n3h#). There are other neighborhood divisions available through data.sfgov.org, but this looks the most like what I'm used to.

`pgh/Pittsburgh_Neighborhoods.geojson` is from the City of Pittsburgh, [link](https://data.wprdc.org/dataset/pittsburgh-neighborhoods2de67)

`usa_cities.geojson` is from Mapzen, [link](https://mapzen.com/data/borders/)

## Safety

`pgh/crimes.csv` is from [this report](http://apps.pittsburghpa.gov/pghbop/ANNUAL_REPORT_DRAFT_2015_May_31.pdf). (for now I think this is the most straightforward to use. Other sources are in `other_crime`. Population stats are from 2010.

"Type 1": Homicide, rape, aggravated assault, robbery, theft, burglary, motor vehicle theft, arson. "Type 2": Simple assault, vandalism, drug violations, fraud, disorderly conduct, drunk driving, forgery, weapons violations, prostitution, public intoxication, other.

`sf/sfpd_2015.csv` is a list of all the police incidents in 2015. Unfortunately, they don't seem to be categorized all that well. Population stats are from 2014.

## Convenience

`nghd_walkscores` - These are just copy/pasted from Walkscore, [here](https://www.walkscore.com/CA/San_Francisco)

## Localness

`tweets.csv` is just a dump of the tweet tables, which is to say, all the coordinate-geotagged tweets in each city since sometime in 2014/15 depending on city. [More details](talesnideas.blogspot.com/2016/02/welcome-to-domo.html)

## Liveliness

Foursquare venue data in `4sq_venues.json`. Yelp data (which is way more limited - has Pgh but not any of our other cities, and has 4k businesses instead of the 46k I found in Foursquare - so we're probably not using it) from the [Yelp academic dataset](https://www.yelp.com/dataset_challenge/dataset).

`nghd_4sq.csv` has these venues counted per square mile per neighborhood. There's also one line at the end that represents the city as a whole - which is a little different. It's an average of each neighborhood. So like "Food venues" there is not the total number of food venues in the city divided by the area of the city, because this would underestimate because some neighborhoods are really sparse. Instead, it's the average number of food venues per neighborhood.

## Aesthetics
`yfcc100m.csv` is all the yfcc100m photos in Pittsburgh. `nghd_autotags.json` is the top 10 autotags for each neighborhood.

The directory `yfcc100m_autotagged` is to store YFCC100M dumps from other cities, just so I don't have to compute them again.
