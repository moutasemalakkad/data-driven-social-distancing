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
