#!/usr/bin/env python

# sfpd_2015.csv is just every incident. Gotta aggregate ourselves, I guess?

import argparse, csv, collections, json
from util.pointmap import Pointmap
parser = argparse.ArgumentParser()
parser.add_argument('--crimes_data', default='data/sf/sfpd_2015.csv')
parser.add_argument('--pointmap_file', default='data/sf/pointmap.csv')
parser.add_argument('--acs_file', default='data/sf/acs_2014.csv')
parser.add_argument('--tracts_to_nghds_file', default='data/sf/tracts_analysis_nghds.geojson')
parser.add_argument('--nghd_bounds_file', default='data/sf/pointmap.csv')
parser.add_argument('--output_file', default='data/sf/crimes.csv')
args = parser.parse_args()

PART1_CATEGORIES = ['ARSON', 'BURGLARY', 'LARCENY/THEFT', 'ROBBERY',
        'SEX OFFENSES, FORCIBLE', 'VEHICLE THEFT']
# Type 1 also includes Homicide and Aggravated Assault, but we're missing
# homicide data (?!) but there are only 53 in 2015 in SF, and the data.sf.gov
# page doesn't distinguish Aggravated and Simple assault in the category, so
# we'll process ASSAULT separately.
PART2_CATEGORIES = ['BAD CHECKS', 'BRIBERY', 'DISORDERLY CONDUCT',
        'DRIVING UNDER THE INFLUENCE', 'DRUG/NARCOTIC', 'DRUNKENNESS',
        'EMBEZZLEMENT', 'EXTORTION', 'FAMILY OFFENSES', 'FORGERY/COUNTERFEITING',
        'FRAUD', 'GAMBLING', 'KIDNAPPING', 'LIQUOR LAWS', 'LOITERING',
        'OTHER OFFENSES', 'PORNOGRAPHY/OBSCENE MAT', 'PROSTITUTION',
        'SECONDARY CODES', 'SEX OFFENSES, NON FORCIBLE', 'STOLEN PROPERTY',
        'SUICIDE', 'TREA', 'TRESPASS', 'VANDALISM', 'WARRANTS', 'WEAPON LAWS']
        # Based on looking through 2014-2016, "TREA" is Trespassing also.
NOT_CRIMES = ['MISSING PERSON', 'NON-CRIMINAL', 'RECOVERED VEHICLE', 'RUNAWAY',
        'SUSPICIOUS OCC']

def get_type(line):
    """ Returns the type of a crime according to the FBI's UCR:
    http://www.ucrdatatool.gov/offenses.cfm
    Returns 1 if type 1, 2 if type 2, 3 if not a crime, and None if unknown.
    """
    category = line['Category'].upper()
    if category == 'ASSAULT':
        return 1 if 'AGGRAVATED' in line['Descript'] else 2
    elif category in PART1_CATEGORIES:
        return 1
    elif category in PART2_CATEGORIES:
        return 2
    elif category in NOT_CRIMES:
        return 3
    else:
        return None

if __name__ == '__main__':

    # First figure out all the neighborhood populations
    tracts_nghds = {t['properties']['geoid']: t['properties']['nhood'] for t in json.load(open(args.tracts_to_nghds_file))['features']}
    nghds_pops = collections.Counter()
    acs_reader = csv.DictReader(open(args.acs_file))
    acs_reader.next() # two header rows in this one :-/
    for tract in acs_reader:
        pop = int(tract['HC01_EST_VC01'])
        tract_geoid = tract['GEO.id2']
        if tract_geoid in ['06075980401', '06075990100']:
            # Farallon Islands and offshore Ocean Beach :-/
            continue
        nghd = tracts_nghds[tract_geoid]
        nghds_pops[nghd] += pop

    # Read and tally each crime by neighborhood and type.
    crimes_reader = csv.DictReader(open(args.crimes_data))
    output_writer = csv.writer(open(args.output_file, 'w'))
    output_writer.writerow(['Neighborhoods', 'Population 2010', 'Part I crimes', 'Part II crimes', 'part1_per_1000_ppl', 'part2_per_1000_ppl', 'total_per_1000_ppl'])
    pointmap = Pointmap(args.pointmap_file)
    part1_counter = collections.Counter()
    part2_counter = collections.Counter()
    for line in crimes_reader:
        type = get_type(line) # FBI UCR Part 1 or 2, or 3 (not a crime).
        neighborhood = pointmap[(line['Y'], line['X'])]
        if type == 1:
            part1_counter[neighborhood] += 1
        elif type == 2:
            part2_counter[neighborhood] += 1
        # elif type == 3, whatever, not a crime, ignore it.
 
    # Write output.
    for nghd in nghds_pops.keys():
        pop = nghds_pops[nghd]
        part1 = part1_counter[nghd]
        part2 = part2_counter[nghd]
        output_writer.writerow([nghd, pop, part1, part2,
            round(part1 * 1000.0 / pop, 2),
            round(part2 * 1000.0 / pop, 2),
            round((part1 + part2) * 1000.0 / pop, 2)])


