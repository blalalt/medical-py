import pymongo
import csv


from pymongo import MongoClient


client: pymongo.MongoClient = MongoClient()


db: pymongo.database.Database = client['medical']


# 检查
def check_import(check_file_path: str):
    collection = db.get_collection(name='check')
    pass