import pymongo
import csv
import jieba


from pymongo import MongoClient


client: pymongo.MongoClient = MongoClient()


db: pymongo.database.Database = client['medical']


USELESS_KEYS = ['']


# 加上分词
def add_segment(name='disease'):
    collection = db.get_collection(name=name)

    pass

def delete_useless_keys(keys: list):
    if not keys: keys = USELESS_KEYS
    