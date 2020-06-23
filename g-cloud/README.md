![stop coivd](images/Stop.png)


## Background

With sensors devices being affordable and accurate, It is almost inevitable for any business to leverage fresh data, which aids in the automation of many sectors and gives us the capability to respond to live events. In 2019 there were 26.66 billion active IoT devices in the world. That number is expected to reach 75 billion by 2025.

I wanted to leverage IoT to fight the pandemic that had taken 435 thousand lives away from their loved ones. Consequently, I wanted to build an application that promotes social distancing and improves public health during the COVID-19 pandemic using cell-phone signals. 

## Rnunning Insturctions
- Clone the repo
- Change GCP's account info
    - Project ID
    - PubSub subscriptions
    - GCP's JSON key for authorization

- CD to g-cloud
```bash 
cd g-cloud
``` 

- Publish Messages using:
```python 
python run_publish.py <--total_message_to_send (int)> (optional)
``` 

- Consume:
```python 
python -m \
    Beam-flink \
    --project \
    <Project Name> \
    --runner DataflowRunner \
    --temp_location \
    <GC BUCKET>/temp \
    --output \
    <GC BUCKET>/results/output \
    --job_name <namme> \
    -- <Region> ex: region us-central1
``` 


## App Demo (Please click the video below)
[![Watch the video](images/youtube.png)](https://www.youtube.com/watch?v=_C6mzchTkE8&feature=emb_title)


## License
[MIT](https://choosealicense.com/licenses/mit/)




Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)