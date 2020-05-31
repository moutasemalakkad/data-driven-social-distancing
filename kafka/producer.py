from time import sleep
from json import dumps
from kafka import KafkaProducer




producer = KafkaProducer(bootstrap_servers='localhost:9092'   
                         value_serializer=lambda x:
                         #searlize object to send to kafkas
                         dumps(x).encode('utf-8'))




while True:
	data = SchemaFaker().stream()


# for data in SchemaFaker().stream():
#     producer.send('meetup', value=data)   # add topic name
#     sleep(1)
