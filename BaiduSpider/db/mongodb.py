from pymongo import MongoClient
import datetime
import pprint
client = MongoClient('mongodb://39.108.153.3:27017/')
db = client.spider
collection = db.keyword_lib


class DB:
    @staticmethod
    def filter(words):
        result = collection.find({"word": {"$in": words}})
        for post in result:
            # print(post['word'])
            while post['word'] in words:
                words.remove(post['word'])
        return words

    def insert(self, words):
        words = self.filter(words)
        # print("words:"+str(words))
        if len(words) > 0:
            data_list = []
            for word in words:
                data_list.append({
                    "word": word,
                    "deal": 0,
                    "add_time": datetime.datetime.utcnow()
                })
            collection.insert_many(data_list)

