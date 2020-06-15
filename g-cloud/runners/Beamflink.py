import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions, SetupOptions
from apache_beam import window

from google.cloud import pubsub_v1


import json
import os
import time

import sys


project_id = "totemic-polygon-279515"


# Json Key
path_service_account = 'totemic-polygon-279515-42a8a5c17575.json'


#### json file (authirzation)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_service_account


#### topics#####
input_subscription = 'projects/totemic-polygon-279515/subscriptions/meet'





import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--project')
parser.add_argument('--runner')
parser.add_argument('--temp_location')
parser.add_argument('--output')
parser.add_argument('--job_name')
parser.add_argument('--region')
parser.add_argument('--streaming')

known_args, pipeline_args = parser.parse_known_args()

pipeline_options = PipelineOptions(pipeline_args)
pipeline_options.view_as(SetupOptions).save_main_session = True
pipeline_options.view_as(StandardOptions).streaming = True



#######Transformation Functions#######

# Json to Python Dic
def to_python_dict(element):
    element = json.loads(element) # had to change this to encode
    #print(type(element))
    return element      #str(event_data).encode("utf-8")


# get venue value
def get_venue(elements):
  return elements['venue']


# get mode value
def get_mode(elements):
   return elements['mode']

# build tuple
def build_tuple(elements):
  mode = elements['mode']
  geo_hash = elements['geohash']
  lon = elements['lon']
  lat = elements['lat']
  return {"geohash":geo_hash, "lat":lat, "lon":lon, "mode":mode} #






###### Pipline Beam (Transforms) ############


print(0000000000000000)
# Building a Beam Pipline
p1 = beam.Pipeline(options=pipeline_options)

attendance_count = (
    p1
    |'read pub_sub' >> beam.io.ReadFromPubSub(subscription=input_subscription) #beam.io.ReadFromPubSub(subscription=input_subscription) #, timestamp_attribute


    # timestamp_attribute –
    # Message value to use as element timestamp. If None, uses message publishing time as the timestamp.


    | 'to python dict' >> beam.Map(to_python_dict)



    | 'Filter offline events' >> beam.Filter(lambda element: element['venue']['mode'] == 'offline') # change to offline


    | 'get venue' >> beam.Map(get_venue)


    | 'build_tuple' >> beam.Map(build_tuple)


#    | 'ecode' >> beam.Map(lambda x : str(x).encode("utf-8"))


    | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
                        "totemic-polygon-279515:dataset.meetup",
                        schema="geohash:string, mode:string, lat:Float, lon:float")
#beam.io.WriteToText('ou.txt')
)

print(111111111111111)
# running pipline
result = p1.run() #
result.wait_until_finish()
