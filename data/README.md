# `data`

Not all data in this file might be checked in to git. (It's not usually a good practice to check in big files.)

## Neighborhood Boundaries
`sf_planning_neighborhoods.json` is from the SF Department of City Planning, [link](https://data.sfgov.org/Geographic-Locations-and-Boundaries/Neighborhood-Groups-Map/qc6m-r4ih)

`sffind_neighborhoods.json` is from the SF Mayor's Office, [link](https://data.sfgov.org/Geographic-Locations-and-Boundaries/SFFind-Neighborhoods/ejmn-jyk6). It is finer-grained than the Planning department neighborhoods.

`Pittsburgh_Neighborhoods.geojson` is from the City of Pittsburgh, [link](https://data.wprdc.org/dataset/pittsburgh-neighborhoods2de67)

`usa_cities.geojson` is from Mapzen, [link](https://mapzen.com/data/borders/)

## Safety
A few possible sources:

- `pgh_crime.csv` is from the Western Pennsylvania Open Data Portal [Tableau file we extracted CSV from](https://public.tableau.com/profile/alleghenycountydhsdare#!/vizhome/OverallTrendsinViolence_Public_8-12-16/OverallTrend), [overall crime data page](http://www.wprdc.org/crime/)
- [Police blotter archive](https://data.wprdc.org/dataset/uniform-crime-reporting-data)
- `pgh_2015_review.csv` is from [this report](http://apps.pittsburghpa.gov/pghbop/ANNUAL_REPORT_DRAFT_2015_May_31.pdf)

(for now I think `pgh_2015_review.csv` is the most straightforward to use.)

"Type 1": Homicide, rape, aggravated assault, robbery, theft, burglary, motor vehicle theft, arson. "Type 2": Simple assault, vandalism, drug violations, fraud, disorderly conduct, drunk driving, forgery, weapons violations, prostitution, public intoxication, other.

## Convenience

`pgh_nghd_walkscores` - I think I manually scraped this at one point?

## Localness

`tweet_pgh_with_text.csv` is just a dump of the `tweet_pgh` table, which is to say, all the coordinate-geotagged tweets in Pittsburgh since, I think, early 2014.
