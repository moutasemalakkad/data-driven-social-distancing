import os
import time
from google.cloud import pubsub_v1



if __name__== "__main__":

	#permission JsonFile
	path_service_Account = "beam-276623-290ddf0eab0b.json"

	#set permissions
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_service_Account

	#subscription
	subscription_path = "projects/beam-276623/subscriptions/subscribe2"



	subscriber = pubsub_v1.SubscriberClient()


	def callback(message):
		print(f"Recieved message: {message}")
		message.ack()


	subscriber.subscribe(subscription_path, callback=callback)



	while True:
		time.sleep(60)
