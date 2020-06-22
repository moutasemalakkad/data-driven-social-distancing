![stop coivd](images/Stop.png)


## Background

With sensors devices being affordable and accurate, It is almost inevitable for any business to leverage fresh data, which aids in the automation of many sectors and gives us the capability to respond to live events. In 2019 there were 26.66 billion active IoT devices in the world. That number is expected to reach 75 billion by 2025.

I wanted to leverage IoT to fight the pandemic that had taken 435 thousand lives away from their loved ones. Consequently, I wanted to build an application that promotes social distancing and improves public health during the COVID-19 pandemic using cell-phone signals. 


## Tech Stack

![tech](images/pipe1.png)


## Running Instruction

- Clone the repo
- Change GCP's account info
	- Project ID
	- PubSub subscriptions
	- GCP's JSON key for authorization
- CD to g-cloud
- Publish Messages using:
	python run_publish.py --total_message_to_send 10000
- Consume:
	python -m \
    Beam-flink \
    --project \
    <PROJECT ID> \
    --runner rundataflow \
    --temp_location \
    gs://<GCP BUCKET>/temp \
    --output \
    gs://<GCP BUCKET>/results/output \
    --job_name dataflow-meet \
    --region <YOUR REGION EX:us-central1>
