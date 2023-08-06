import sys
import os
from os.path import dirname
import re
import json
import logging
import collections

from mrjob.job import MRJob
from mrjob.step import MRStep


try:
    # when running on EMR a geotweet package will be loaded onto PYTHON PATH
    #from geotweet.mapreduce.utils.words import WordExtractor
    from geotweet.mapreduce.utils.lookup import project, rproject
    from geotweet.mapreduce.utils.lookup import MetroLookup, SpatialLookup
    from geotweet.geomongo.mongo import MongoGeo

except ImportError:
    # running locally
    #from utils.words import WordExtractor
    from utils.lookup import project, rproject, MetroLookup, SpatialLookup
    parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent) 
    from geomongo.mongo import MongoGeo

# must log to stderr when running on EMR or job will fail
logging.basicConfig(stream=sys.stderr, level=logging.INFO)


DB = "geotweet"
COLLECTION = "metro_osm"
MIN_WORD_COUNT = 2
METERS_PER_MILE = 1609
METRO_DISTANCE = 50 * METERS_PER_MILE
POI_DISTANCE = 100
MONGO_TIMEOUT = 30 * 1000
POI_TAGS = ["amenity", "builing", "shop", "office", "tourism"]


class MROSMLookup(MRJob):
    """ """
    
    SORT_VALUES = True

    def steps(self):
        return [
            MRStep(
                mapper_init=self.mapper_init,
                mapper=self.mapper,
                reducer_init=self.reducer_init,
                reducer=self.reducer
            ),
            MRStep(
                reducer=self.reducer_tag_count
            ),
            MRStep(
                reducer_init=self.reducer_init_mongo,
                reducer=self.reducer_mongo
            )
        ]
    
    def mapper_init(self):
        """ build local spatial index of US metro areas """
        self.lookup = MetroLookup()
   
    def mapper(self, _, line):
        data = json.loads(line)
        if 'tags' in data:
            tag = 1
            # initalize data for POI
            lonlat = project(data['coordinates'])
            feature = dict(
                geometry=dict(type='Point', coordinates=lonlat),
                properties=dict(tags=data['tags'])
            )
        elif 'user_id' in data:
            tag = 2
            # ignore HR geo-tweets for job postings
            expr = "|".join(["(job)", "(hiring)", "(career)"])
            if data['description'] and re.findall(expr, data['description']):
                return
            # initialize data for getweet
            lonlat = project(data['lonlat'])
            feature = dict(
                coordinates=lonlat,
                text=data['text']
            )
        # lookup nearest metro area
        nearest = self.lookup.get_object(lonlat, buffer_size=METRO_DISTANCE)
        if not nearest:
            return
        metro = nearest['NAME10']
        yield metro, (tag, feature)
    
    def reducer_init(self):
        self.lookup = SpatialLookup()
  
    def reducer(self, metro, values):
        """
        Output tags of POI locations nearby tweet locations

        Values will be sorted coming into reducer.
        First element in each value tuple will be either 1 (osm POI) or 2 (geotweet).
        Build a spatial index with POI records.
        For each tweet lookup nearby POI, and emit tag values for predefined tags.
        
        """

        for i, value in enumerate(values):
            if value[0] == 1:
                # POI node, add to index
                self.lookup.insert(i, value[1])
            else:
                # geotweet, lookup nearest POI from index
                lonlat = value[1]['coordinates']
                text = value[1]['text']
                tags = []
                kwargs = dict(buffer_size=POI_DISTANCE, multiple=True)
                for poi in self.lookup.get_object(lonlat, **kwargs):
                    for tag in POI_TAGS:
                        if tag in poi['tags']:
                            tags.append(poi['tags'][tag])
                for tag in set(tags):
                    yield (metro, tag), 1
    
    def reducer_tag_count(self, key, values):
        total = sum(values)
        metro, tag = key
        yield metro, (total, tag)

    def reducer_init_mongo(self):
        self.mongo = MongoGeo(db=DB, collection=COLLECTION, timeout=MONGO_TIMEOUT)

    def reducer_mongo(self, metro, values):
        records = []
        for record in values:
            total, tag = record
            records.append(dict(
                metro_area=metro,
                tag=tag,
                count=total
            ))
        self.mongo.insert_many(records)


if __name__ == '__main__':
    MROSMLookup.run()
