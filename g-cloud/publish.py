"""Publishes multiple messages to a Pub/Sub topic with an error handler."""
import time
import os


from meet_faker import SchemaFaker


from google.cloud import pubsub_v1


# TODO(developer)
project_id = "covid-19-279120"
pub_sub_topic_name = "projects/covid-19-279120/topics/raw_data"




# Json Key
path_service_account = 'covid-19-279120-1afca8da4df0.json'


# authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path_service_account


# create publisher instance
publisher = pubsub_v1.PublisherClient()


while 1:
    event_data = SchemaFaker().stream()
    #print(f'Publishing {event_data} to {pub_sub_topic_name}')
    publisher.publish(pub_sub_topic_name, str(event_data).encode("utf-8"))   # must be a byte string







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
