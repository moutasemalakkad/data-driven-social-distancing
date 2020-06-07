import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam import window

from google.cloud import pubsub_v1


import json
import os
import time



#### json file (authirzation)
path_service_account = "covid-19-279120-1afca8da4df0.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_service_account


#### topics#####
input_subscription = 'projects/covid-19-279120/subscriptions/beam-raw-data-sub'
output_topic = 'projects/covid-19-279120/topics/cleaned_data'




#######Beam Configs#######
# set options
options = PipelineOptions()
options.view_as(StandardOptions).streaming = True



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
  return (geo_hash, 1) #





###### Pipline Beam (Transforms) ############



# Building a Beam Pipline
p1 = beam.Pipeline(options=options)

attendance_count = (
    p1
    |'read pub_sub' >> beam.io.ReadFromPubSub(subscription=input_subscription) #, timestamp_attribute


    # timestamp_attribute –
    # Message value to use as element timestamp. If None, uses message publishing time as the timestamp.


    | 'to python dict' >> beam.Map(to_python_dict)



    | 'Filter offline events' >> beam.Filter(lambda element: element['venue']['mode'] == 'offline') # change to offline


    | 'get venue' >> beam.Map(get_venue)


    | 'build_tuple' >> beam.Map(build_tuple)


    | 'ecode' >> beam.Map(lambda x : str(x).encode("utf-8"))

    | 'Window' >> beam.WindowInto(window.FixedWindows(20))


    | 'Write to PubSUb' >> beam.io.WriteToPubSub(output_topic)

)


# running pipline
result = p1.run()
result.wait_until_finish()
