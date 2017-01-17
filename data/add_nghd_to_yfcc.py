#!/usr/bin/env python

# Read in a yfcc100m.csv file, add neighborhood names to each photo.

import argparse, csv, collections
from util import pointmap
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--city', required=False, help='If provided, will auto-fill all the filenames and you can skip other arguments.')
parser.add_argument('--input_file', default='data/pgh/yfcc100m.csv', help=' ')
parser.add_argument('--pointmap_file', default='data/pgh/pointmap.csv', help=' ')
parser.add_argument('--output_file', default='data/pgh/yfcc100m_nghds.csv', help=' ')
# I guess I'm hoping, after we run this, we just run:
# "mv yfcc100m_nghds.csv yfcc100m.csv"
args = parser.parse_args()

if __name__ == '__main__':
    if args.city:
        args.input_file='data/' + args.city + '/yfcc100m.csv'
        args.pointmap_file='data/' + args.city + '/pointmap.csv'
        args.output_file='data/' + args.city + '/yfcc100m_nghds.csv'
    city_pointmap = pointmap.Pointmap(args.pointmap_file)
    writer = csv.writer(open(args.output_file, 'w'))
    for line in csv.reader(open(args.input_file)):
        nghd = city_pointmap[line[2], line[3]]
        line.append(nghd)
        writer.writerow(line)

