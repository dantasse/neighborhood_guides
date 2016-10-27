#!/usr/bin/env python

# Take in the Yelp data and a city name, get out all the businesses and reviews
# and checkins and tips for that city.

import argparse, csv, collections, time, util.cities, json, ujson
parser = argparse.ArgumentParser()
parser.add_argument('--yelp_business_file', default='data/yelp_academic_dataset_business.json')
parser.add_argument('--yelp_checkin_file', default='data/yelp_academic_dataset_checkin.json')
parser.add_argument('--yelp_review_file', default='data/yelp_academic_dataset_review.json')
parser.add_argument('--yelp_tip_file', default='data/yelp_academic_dataset_tip.json')
parser.add_argument('--city', default='pgh', choices=util.cities.CITY_NAMES)
parser.add_argument('--output_file', default='data/pgh/yelp_businesses.json')
args = parser.parse_args()

if __name__ == '__main__':
    
    city_min_lon, city_min_lat, city_max_lon, city_max_lat = [float(n) for n in util.cities.CITY_LOCATIONS[args.city]['locations'].split(',')]

    print "%s\tLoading businesses" % time.asctime()
    businesses = [ujson.loads(line) for line in open(args.yelp_business_file)]
    print "%s\tLoading reviews" % time.asctime()
    reviews = [ujson.loads(line) for line in open(args.yelp_review_file)]
    print "%s\tLoading tips" % time.asctime()
    tips = [ujson.loads(line) for line in open(args.yelp_tip_file)]
    print "%s\tLoading checkins" % time.asctime()
    checkins = [ujson.loads(line) for line in open(args.yelp_checkin_file)]
    print "%s\tDone loading. Checking businesses." % time.asctime()

    print "This many businesses: ", len(businesses)
    city_businesses = {} # id -> business
    for business in businesses:
        if business['latitude'] < city_min_lat or business['latitude'] > city_max_lat or business['longitude'] < city_min_lon or business['longitude'] > city_max_lon:
            continue
        business['reviews'] = []
        business['tips'] = []
        business['checkins'] = None
        city_businesses[business['business_id']] = business

    print "This many businesses in the right city: ", len(city_businesses)

    for review in reviews:
        if review['business_id'] in city_businesses:
            city_businesses[review['business_id']]['reviews'].append(review)

    for tip in tips:
        if tip['business_id'] in city_businesses:
            city_businesses[tip['business_id']]['tips'].append(tip)
            
    for checkin in checkins:
        if checkin['business_id'] in city_businesses:
            city_businesses[checkin['business_id']]['checkins'] = checkin

    review_ctr = collections.Counter([len(biz['reviews']) for biz in city_businesses.values()])
    tip_ctr = collections.Counter(len(biz['tips']) for biz in city_businesses.values())
    num_with_checkins = sum(1 if biz['checkins'] != None else 0 for biz in city_businesses.values())
    print "%s\tDone. %s businesses, %s reviews, %s tips" % (time.asctime(),\
            len(city_businesses), sum(review_ctr), sum(tip_ctr))
    print "Distribution of reviews: %s" % review_ctr
    print "Distribution of tips: %s" % tip_ctr
    print "Pct with checkins: %s" % (num_with_checkins * 1.0 / len(city_businesses))

    print "%s\tDumping to json file." % time.asctime()
    json.dump(city_businesses, open(args.output_file, 'w'))
