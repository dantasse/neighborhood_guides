import csv

class Pointmap:
    """ A mapping from lat, lon to neighborhood names. Used for speeding up
    'which neighborhood is this point in' calculations."""

    pointmap = {}
    min_lat = min_lon = max_lat = max_lon = 0

    def __init__(self, filename):
        self.load(filename)

    def load(self, pointmap_filename):
        """ Loads a pointmap from a csv file. """

        for row in csv.DictReader(open(pointmap_filename)):
            loc = (float(row['lat']), float(row['lon']))
            self.pointmap[loc] = row['nghd']
        self.min_lat = min([k[0] for k in self.pointmap.keys()])
        self.max_lat = max([k[0] for k in self.pointmap.keys()])
        self.min_lon = min([k[1] for k in self.pointmap.keys()])
        self.max_lon = max([k[1] for k in self.pointmap.keys()])

    def __getitem__(self, key):
        lat = round(float(key[0]), 3)
        lon = round(float(key[1]), 3)
        if lat < self.min_lat or lat > self.max_lat or \
                lon < self.min_lon or lon > self.max_lon:
            return 'None'
        else:
            return self.pointmap[(lat, lon)]

