from faker import Faker
from faker.providers import internet
from faker.providers import geo

import pygeohash as gh

import time, json, pprint
from math import pi, sin, cos

class SchemaFaker:

    ff = Faker()

    def randKdig(self, k1, k2):
        return self.ff.random.randint(10**k1, 10**(k2+1))


    def takeWord(self, lst):
        return self.ff.word(ext_word_list=lst)

    def randTime(self):
        return self.ff.random.randint(1378888200000, round(1000*time.time()))

    def getUrlName(self, s):
        words = s.split(' ')
        if (len(words)>=2):
            return words[0] + "-" + words[1]
        else:
            return words[0]

    def getUrlKey(self, s):
        ch = self.ff.word(ext_word_list=['-',''])
        return s.lower().replace(' ', ch)



    def nearbyPoint(self, long, lat):
        rad = self.ff.random.uniform(500, 2000) / 111000
        ang = 2*pi*self.ff.random.random()
        long1 = round(long + rad * cos(ang), 5)
        lat1 = round(lat + rad * sin(ang), 5)
        return long1, lat1



    def genRandomSchema(self):

        sch = {}


        place = self.ff.local_latlng(country_code='US')
        venue = {}
        venue["mode"] = self.takeWord(["online", "offline"])
        venue["venue_name"] = place[2]
        venue["lon"] = float(place[0])
        venue["lat"] = float(place[1])
        venue["geohash"] = gh.encode(venue["lat"], venue["lon"], precision=5)
        venue["venue_id"] = self.randKdig(7, 9)

        sch["venue"] = venue

        sch["visibility"] = self.takeWord(["private", "public"])
        sch["response"] = self.takeWord(["yes", "no"])
        sch["guests"] = self.ff.random.randint(0, 1000)

        member = {}
        member["member_id"] = self.randKdig(8, 13)
        member["photo"] = self.ff.image_url() + f'/{member["member_id"]}'
        member["member_name"] = self.ff.name()

        sch["member"] = member

        sch["rsvp_id"] = self.randKdig(8, 10)
        sch["mtime"] = self.randTime()

        event = {}
        event["event_id"] = self.randKdig(8, 10)
        event["time"] = sch["mtime"] + self.ff.random.randint(5*60*1000, 3600*24*1000)
        event["event_url"] = f'{self.ff.url()}events/{event["event_id"]}'
        event["event_name"] = self.ff.text(40)[:-1]

        sch["event"] = event

        group = {}

        cont, city = place[4].split('/')[:2]

        group_topics = []

        # List we can modify
        topics_list = ["social", "adventure", "diningout", "fun-times", "tech", "volunteering", "town", "covid", "dinner", "drinks", "charity", "local", "business", "cultural", "hiking", "home", "cards", "drinks", "house party"]

        nTopics = self.ff.random.randint(5,15)
        for i in range(nTopics):
            topic = {}
            # If we delete ext_word_list = topics_list, it will use its own list of words
            # nb_words is the (maximal) number of words used for the topic name
            #should be 1 for combos we can do 3 to comb three words
            topic_name = self.ff.sentence(nb_words=1, ext_word_list = topics_list)[:-1]
            topic["urlkey"] = self.getUrlKey(topic_name)
            topic["topic_name"] = topic_name

            group_topics.append(topic)

        group["group_topics"] = group_topics

        group["group_city"] = city
        group["group_country"] = place[3]
        group["group_id"] =  self.randKdig(8, 10)
        group["group_name"] = self.ff.text(40)[:-1]
        group["group_urlname"] = self.getUrlName(group["group_name"])
        group["group_lon"], group["group_lat"] = self.nearbyPoint(venue["lon"], venue["lat"])

        sch["group"] = group

        return sch

    def stream(self):
        return json.dumps(self.genRandomSchema()) # , indent=4

if __name__ == "__main__":
    instance = SchemaFaker()

    while True:
        print(instance.stream())
