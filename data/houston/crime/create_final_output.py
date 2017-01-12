#!/usr/bin/env python

# Ok, now we've got the whole list of crimes sorted by neighborhood. Let's
# combine them into a final CSV like we want. Sheesh.

import argparse, csv, collections
parser = argparse.ArgumentParser()
parser.add_argument('--input_file', default='all15_new_geocoded.csv')
parser.add_argument('--neighborhood_populations_file', default='../walkscores.csv')
parser.add_argument('--output_file', default='crimes.csv')
args = parser.parse_args()

nghd_pops = {}
for line in csv.DictReader(open(args.neighborhood_populations_file)):
    nghd_pops[line['Name'].upper()] = int(line['Population'])

print nghd_pops
nghd_crimes = collections.Counter()
for line in csv.reader(open(args.input_file)):
    print line
    nghd = line[13]
    nghd_crimes[nghd] += 1

writer = csv.writer(open(args.output_file, 'w'))
writer.writerow('neighborhood,population,Part I crimes,Part II crimes,part1_per_1000_ppl,part2_per_1000_ppl,total_per_1000_ppl'.split(','))
for nghd, crimes in nghd_crimes.iteritems():
    if nghd == 'None':
        continue
    ppl = nghd_pops[nghd]
    writer.writerow([nghd, ppl, crimes, '', crimes * 1000.0 / ppl, '', ''])
    
