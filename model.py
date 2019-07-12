import pymongo
import csv
import jieba


from pymongo import MongoClient


client: pymongo.MongoClient = MongoClient()


db: pymongo.database.Database = client['medical']

all_title_seg = set()
all_desc = []

USELESS_KEYS = ['疾病链接', 'pdf链接', '英文名', 'ICD号', '_id']


def delete_keys(d: dict):
    for k in USELESS_KEYS:
        d.pop(k)
    return d

# 加上分词
def add_segment(name='disease'):
    collection = db.get_collection(name=name)
    new_collection = db.create_collection(name='new_medical')
    documents = []
    for d in collection.find():
        d = delete_keys(d)
        title = d['疾病名称']
        seg_title = jieba.cut_for_search(title)
        d['segmented'] = {k: 0 for k in seg_title}
        documents.append(d)
        if len(documents) == 500:
            new_collection.insert_many(documents)




def delete_useless_keys(keys: list):
    if not keys: keys = USELESS_KEYS
    