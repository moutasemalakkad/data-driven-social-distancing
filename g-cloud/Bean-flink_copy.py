import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions, SetupOptions
from apache_beam import window
from geopy.geocoders import Nominatim
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
output_topic = 'projects/covid-19-279120/topics/cleaned_data'


argv = [
        '--project=totemic-polygon-279515'
        , '--job_name=dataflow-meet-new'
      #  , '--save_main_session'
        , '--staging_location=gs://totemic-polygon-279515/staging/'
        , '--temp_location=gs://totemic-polygon-279515/tmp/'
        , '--runner=DataflowRunner'
        , '--streaming'
        , '--region=us-central1'
]
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
  global Nominatim
  locator = Nominatim(user_agent='google')
  mode = elements['mode']
  geo_hash = elements['geohash']
  lon = elements['lon']
  lat = elements['lat']
  return {"geohash":geo_hash, "lat":lat, "lon":lon, "mode":mode} #



def get_address(elements):
    locator = Nominatim(user_agent='google', domain='localhost:8080/nominatim', scheme='http')    #user_agent='google'
    coordinates = elements['lat'], elements['lon']
    location = locator.reverse(coordinates)
    dict = location.raw
    address = dict['display_name']
    elements['address'] = address
    return elements
    #change pipeline
###### Pipline Beam (Transforms) ############
# Building a Beam Pipline
p1 = beam.Pipeline(argv=argv)
attendance_count = (
    p1
    |'read pub_sub' >> beam.io.ReadFromPubSub(subscription=input_subscription) #beam.io.ReadFromPubSub(subscription=input_subscription) #, timestamp_attribute
    # timestamp_attribute –
    # Message value to use as element timestamp. If None, uses message publishing time as the timestamp.
    | 'to python dict' >> beam.Map(to_python_dict)
    | 'Filter offline events' >> beam.Filter(lambda element: element['venue']['mode'] == 'offline') # change to offline
    | 'get venue' >> beam.Map(get_venue)
    | 'Build initital dic' >> beam.Map(build_tuple)
    | 'build_tuple' >> beam.Map(get_address)
#   | 'encode' >> beam.Map(lambda x : str(x).encode("utf-8"))
   | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
                       "totemic-polygon-279515:dataset.meetup_address",
                       schema="geohash:string, mode:string, lat:Float, lon:Float, address:string")
#beam.io.WriteToText('ou.txt')
)
# running pipline
result = p1.run() #
result.wait_until_finish()
