import apache_beam as beam



# Transform our Json object to Python Dict
def to_python_dict(element):
    return json.loads(element)


# get venue
def get_venue(elements):
  return elements['venue']

# get mode
def get_mode(elements):
   return elements['mode']

# build tuple
def build_tuple(elements):
  mode = elements['mode']
  geo_hash = elements['geohash']
  return (geo_hash, mode)





# Building a Beam Pipline
p1 = beam.Pipeline()

attendance_count = (

   p1
    |'read file' >> beam.io.external.ReadFromKafka(
                    consumer_config={
                      'bootstrap.servers': 'notvalid1:7777, notvalid2:3531'
                  },
                  topics=['topic1', 'topic2'],
                  key_deserializer='org.apache.kafka.'
                  'common.serialization.'
                  'ByteArrayDeserializer',
                  value_deserializer='org.apache.kafka.'
                  'common.serialization.'
                  'LongDeserializer'
))   #ReadAllFromText.    # beam.io.external.kafka





    | 'to python dict' >> beam.Map(to_python_dict)

    | 'Filter offline events' >> beam.Filter(lambda element: element['venue']['mode'] == 'online') # change to offline


    | 'get venue' >> beam.Map(get_venue)
    | 'build_tuple' >> beam.Map(build_tuple)



    |'write out' >> beam.io.WriteToText('output_python_dic')

)


# running pipline
p1.run()











# pipeline
#    .apply(KafkaIO.read()
#          .withBootstrapServers("broker_1:9092,broker_2:9092")
#          .withTopics(ImmutableList.of("topic_1", "topic_2"))
#
#          .withKeyCoder(BigEndianLongCoder.of())
#          .withValueCoder(StringUtf8Coder.of())
#          .updateConsumerProperties(
#                ImmutableMap.of("receive.buffer.bytes", 1024 * 1024))
#
#        .withTimestampFn(new CustomTypestampFunction())
#        .withWatermarkFn...
