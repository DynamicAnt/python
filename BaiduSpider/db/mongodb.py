from pymongo import MongoClient
import datetime
import pprint
client = MongoClient('mongodb://39.108.153.3:27017/')
db = client.spider
collection = db.keyword_lib


class DB:
    @staticmethod
    def filter(words):
        word_list = []
        for element in words:
            if element not in word_list:
                word_list.append(element)
        result = collection.find({"word": {"$in": word_list}})
        for post in result:
            # print(post['word'])
            while post['word'] in word_list:
                word_list.remove(post['word'])
        return word_list

    def insert(self, words):
        # print("before filter words:"+str(words))
        words = self.filter(words)
        # print("after filter words:"+str(words))
        if len(words) > 0:
            data_list = []
            for word in words:
                data_list.append({
                    "word": word,
                    "deal": 0,
                    "add_time": datetime.datetime.utcnow()
                })
            collection.insert_many(data_list)

    @staticmethod
    def find(word):
        result = collection.find({"word": word})
        for rst in result:
            pprint(rst)


# DB.find("剪叉式液压升降机")

