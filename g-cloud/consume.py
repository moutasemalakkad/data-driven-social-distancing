from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

import time


import os






if __name__ == "__main__":


    # Json Key
    path_service_account = 'covid-19-279120-1afca8da4df0.json'

    # authentication
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path_service_account



    # subscription path
    subscription_name = "projects/covid-19-279120/subscriptions/beam_cleaned"


    # subscriber instance
    Subscriber = pubsub_v1.SubscriberClient()



    def callback(message):
        print(f'Received messages: {message}')
        message.ack()




    while True:
        Subscriber.subscribe(subscription_name, callback=callback)
        time.sleep(6)



######################################################################## #################################### #################################### ####################################


# # TODO(developer)
# project_id = "covid-19-279120"
# subscription_name = "projects/covid-19-279120/subscriptions/beam-raw-data-sub"
# # Number of seconds the subscriber should listen for messages
# # timeout = 5.0
#
# subscriber = pubsub_v1.SubscriberClient()
# # The `subscription_path` method creates a fully qualified identifier
# # in the form `projects/{project_id}/subscriptions/{subscription_name}`
# subscription_path = subscriber.subscription_path(project_id, subscription_name)
#
#
# # authentication
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path_service_account
#
# def callback(message):
#     print("Received message: {}".format(message))
#     message.ack()
#
# streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
# print("Listening for messages on {}..\n".format(subscription_path))
#
# # Wrap subscriber in a 'with' block to automatically call close() when done.
# with subscriber:
#     try:
#         # When `timeout` is not set, result() will block indefinitely,
#         # unless an exception is encountered first.
#         streaming_pull_future.result(timeout=timeout)
#     except TimeoutError:
#         streaming_pull_future.cancel()
