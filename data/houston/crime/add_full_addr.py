#!/usr/bin/env python

# Geocode a CSV of Houston crimes

import argparse, csv, collections
parser = argparse.ArgumentParser()
parser.add_argument('--input_file', default='all15.csv')
parser.add_argument('--output_file', default='all15_new.csv')
args = parser.parse_args()

writer = csv.writer(open(args.output_file, 'w'))
for line in csv.reader(open(args.input_file)):
    line = line[0:10]
    if line[9].endswith('ate'): # ehh long story, comes from joining files together
        line[9] = 1

    street_num = line[5].split('-')[0] # so "4000-4099" becomes just "4000"
    if street_num == 'UNK':
        street_num = ''
    street = line[6]
    if line[7] != '-':
        street += ' ' + line[7]
    if line[8] != '-':
        street += ' ' + line[8]

    line.append(street_num + ' ' + street + ", Houston, TX")
    writer.writerow(line)


