#!/usr/bin/env python

# 2015_crimes.csv is every crime, I guess.

import argparse, csv, collections, json
from util.pointmap import Pointmap
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--crimes_data', default='data/chicago/2015_crimes.csv', help=' ')
parser.add_argument('--pointmap_file', default='data/chicago/pointmap.csv', help=' ')
parser.add_argument('--nghd_populations_file', default='data/chicago/walkscores.csv', help=' ')
parser.add_argument('--output_file', default='data/chicago/crimes.csv', help=' ')
args = parser.parse_args()

PART1_CATEGORIES = ['ARSON', 'BURGLARY', 'HOMICIDE', 'THEFT', 'ROBBERY',
        'MOTOR VEHICLE THEFT']

PART2_CATEGORIES = ['CONCEALED CARRY LICENSE VIOLATION', 'CRIMINAL DAMAGE', 
        'CRIMINAL TRESPASS', 'DECEPTIVE PRACTICE', 'GAMBLING', 'HUMAN TRAFFICKING',
        'INTERFERENCE WITH PUBLIC OFFICER', 'INTIMIDATION', 'KIDNAPPING', 
        'LIQUOR LAW VIOLATION', 'NARCOTICS', 'OBSCENITY',
        'OFFENSE INVOLVING CHILDREN', 'OTHER NARCOTIC VIOLATION',
        'OTHER OFFENSE', 'PROSTITUTION', 'PUBLIC INDECENCY',
        'PUBLIC PEACE VIOLATION', 'STALKING', 'WEAPONS VIOLATION']


NOT_CRIMES = ['NON - CRIMINAL', 'NON-CRIMINAL']

def get_type(line):
    """ Returns the type of a crime according to the FBI's UCR:
    http://www.ucrdatatool.gov/offenses.cfm
    Returns 1 if type 1, 2 if type 2, 3 if not a crime, and None if unknown.
    """
    primary_type = line['Primary Type'].upper()
    # Not sure about all these, so just going with the same rules as Assault:
    # Aggravated is type 1, non-aggravated is type 2.
    if primary_type in ['ASSAULT', 'BATTERY', 'SEX OFFENSE', 'CRIM SEXUAL ASSAULT', 'OFFENSE INVOLVING CHILDREN']:
        if 'NON-AGGRAVATED' in line['Description']:
            return 2
        elif 'AGG' in line['Description']: # Sometimes "AGGRAVATED", sometimes "AGG"
            return 1
        else:
            return 2
    elif primary_type in PART1_CATEGORIES:
        return 1
    elif primary_type in PART2_CATEGORIES:
        return 2
    elif primary_type in NOT_CRIMES:
        return 3
    else:
        print 'Uncategorized', str(line)
        return None

if __name__ == '__main__':

    # First figure out all the neighborhood populations
    # tracts_nghds = {t['properties']['geoid']: t['properties']['nhood'] for t in json.load(open(args.tracts_to_nghds_file))['features']}
    nghds_pops = collections.Counter()
    for line in csv.DictReader(open(args.nghd_populations_file)):
        nghds_pops[line['Name']] += int(line['Population'])

    # Read and tally each crime by neighborhood and type.
    crimes_reader = csv.DictReader(open(args.crimes_data))
    output_writer = csv.writer(open(args.output_file, 'w'))
    output_writer.writerow(['neighborhood', 'population', 'Part I crimes', 'Part II crimes', 'part1_per_1000_ppl', 'part2_per_1000_ppl', 'total_per_1000_ppl'])
    pointmap = Pointmap(args.pointmap_file)
    part1_counter = collections.Counter()
    part2_counter = collections.Counter()
    for line in crimes_reader:
        type = get_type(line) # FBI UCR Part 1 or 2, or 3 (not a crime).
        if line['Latitude'] == '':
            missed_ctr += 1
            neighborhood = None
        else:
            neighborhood = pointmap[(float(line['Latitude']), float(line['Longitude']))]
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
        if pop == 0:
            # for parks, for example, which have no population.
            p1_per_1k = p2_per_1k = total_per_1k = 0
        else:
            p1_per_1k = round(part1 * 1000.0 / pop, 2)
            p2_per_1k = round(part2 * 1000.0 / pop, 2)
            total_per_1k = round((part1 + part2) * 1000.0 / pop, 2)
        part1 = part1_counter[nghd]
        part2 = part2_counter[nghd]
        
        output_writer.writerow([nghd, pop, part1, part2, p1_per_1k, p2_per_1k,
            total_per_1k])
    # Write one more for SF as a whole.
    total_pop = sum(nghds_pops.values())
    total_part1 = sum(part1_counter.values())
    total_part2 = sum(part2_counter.values())
    output_writer.writerow(['Chicago', total_pop, total_part1, total_part2,
            round(total_part1 * 1000.0 / total_pop, 2),
            round(total_part2 * 1000.0 / total_pop, 2),
            round((total_part1 + total_part2) * 1000.0 / total_pop, 2)])
    print 'Done. Missed this many crimes b/c they are missing a lat/lon point: ', missed_ctr
 
