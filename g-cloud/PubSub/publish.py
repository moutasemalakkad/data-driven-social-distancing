"""Publishes multiple messages to a Pub/Sub topic with an error handler."""
import time
import os

import datetime
from generator.verizon import SchemaFaker


from google.cloud import pubsub_v1


# TODO(developer)
project_id = "totemic-polygon-279515"
pub_sub_topic_name = "projects/totemic-polygon-279515/topics/meet"




# Json Key
path_service_account = 'totemic-polygon-279515-42a8a5c17575.json'


# authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path_service_account


def run_publisher():
    # create publisher instance
    publisher = pubsub_v1.PublisherClient()

    counter = 1
    start_time = datetime.datetime.now()
    while 1:
        event_data = SchemaFaker().stream()
        #print(f'Publishing {event_data} to {pub_sub_topic_name}')
        publisher.publish(pub_sub_topic_name, str(event_data).encode("utf-8"))   # must be a byte string
        counter += 1
        time.sleep(1)
        if counter>2000:
            break

    now = datetime.datetime.now()

    print(2000, "messages in ", now-start_time)





# publisher = pubsub_v1.PublisherClient()
# topic_path = publisher.topic_path(project_id, topic_name)
#




# futures = dict()
#
# def get_callback(f, data):
#     def callback(f):
#         try:
#             print(f.result())
#             futures.pop(data)
#         except:  # noqa
#             print("Please handle {} for {}.".format(f.exception(), data))
#
#     return callback
#
# for i in range(10):
#     data = str(i)
#     futures.update({data: None})
#     # When you publish a message, the client returns a future.
#     future = publisher.publish(
#         topic_path, data=data.encode("utf-8")  # data must be a bytestring.
#     )
#     futures[data] = future
#     # Publish failures shall be handled in the callback function.
#     future.add_done_callback(get_callback(future, data))
#
# # Wait for all the publish futures to resolve before exiting.
# while futures:
#     time.sleep(5)
#
# print("Published message with error handler.")
