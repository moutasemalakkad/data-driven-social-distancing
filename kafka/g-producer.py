import os
import time
from google.cloud import pubsub_v1


from meet_faker import SchemaFaker



if __name__== "__main__":

	# add project id "from console"
	project = "beam-276623"


	#add pubsub topic
	pubsub_topic = "projects/beam-276623/topics/Topic1"

	#permission JsonFile
	path_service_Account = "beam-276623-290ddf0eab0b.json"


	#set permissions
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_service_Account


	# create Publisher
	publisher = pubsub_v1.PublisherClient()


	# csv
	# input_file = "counts.csv"



	while True:
		event_data = SchemaFaker().stream()
		print(f"Publishing {event_data} to {pubsub_topic}")
		publisher.publish(pubsub_topic, event_data)
