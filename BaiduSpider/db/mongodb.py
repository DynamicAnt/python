from pymongo import MongoClient
import datetime
import pprint
import time
client = MongoClient('mongodb://39.108.153.3:27017/')
db = client.spider
collection = db.test
link_col = db.links


class DB:
    @staticmethod
    def filter(words):
        filter_start_time = time.clock()
        result = collection.find({"word": {"$in": words}})
        for post in result:
            # print(post['word'])
            while post['word'] in words:
                words.remove(post['word'])
        filter_end_time = time.clock()
        print("filter耗时：%f s" % (filter_end_time - filter_start_time))
        return words

    def insert(self, words):
        insert_start_time = time.clock()
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
            try:
                collection.insert_many(data_list)
            except Exception as e:
                pprint(e.message)
                words = self.filter(words)
                self.insert(words)
        insert_end_time = time.clock()
        print("filter耗时：%f s" % (insert_end_time - insert_start_time))

    @staticmethod
    def find(word):
        result = collection.find({"word": word})
        for rst in result:
            pprint(rst['word'])

    @staticmethod
    def find_words(start=0, offset=0):
        result = collection.find({"w_id": {"$gte": start}}).limit(offset)
        words = []
        for rst in result:
            words.append(rst["word"])
            # print(str(rst))
        return words

    @staticmethod
    def update(condition):
        result = collection.find(condition)
        for rst in result:
            rst.deal = "1"
            collection.save(rst)

    @staticmethod
    def get_total_num():
        return collection.count()

    @staticmethod
    def write_to_link(data):
        link_col.insert_many(data)
# DB.find("剪叉式液压升降机")
# DB.find_words(0, 3)

