import pprint
import json
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import json_util as jsonb
from setting import config
from intention import intention_classifier

db = MongoClient()['medical']
app = Flask(__name__)

app.config.from_object(config)

DELETE_KEYS = ['']

collection = db.get_collection(name='disease')


class ChatResponse:
    def __init__(self, it_type, msg):
        self.it_type = it_type
        self.msg = msg
    def build(self):
        if self.it_type == 1: # 概念
            return self._build_concept_resp()
        elif self.it_type == 2: # 闲聊
            return self._build_chat_resp()
        elif self.it_type == 3: # 巡诊
            return self._build_inquiry_resp()
    
    def _build_concept_resp(self):
        result = collection.find_one(filter={'疾病名称': self.msg}, 
            projection={'_id': 1, '概述': 1, '疾病名称': 1})
        id_ = result.pop('_id')
        result['_id'] = str(id_)
        return result

    def _build_chat_resp(self):
        return None

    def _build_inquiry_resp(self):
        return None

def reconstruce_doc(disease_doc: dict):
    new_d = {}
    new_d['name'] = disease_doc.pop('疾病名称')
    disease_doc.pop('_id')
    new_d['data'] = disease_doc
    return new_d

@app.route('/api/disease_list/<int:page>', methods=['GET'])
def disease_list(page: int=0):
    collection = db.get_collection(name='disease') # Collection
    per_page: int = app.config['PER_PAGE']
    find_result = collection.find(filter={}, limit=per_page, sort={}, skip=per_page*page,
        projection={'疾病链接':0, 'pdf链接':0, '英文名':0, '别名':0, '所属科目':0, 'ICD号':0}) # Cursor
    u_result = []
    for i in find_result:
        id_ = str(i.pop('_id'))
        i['_id'] = id_
        u_result.append(i)
    return jsonify({'data': u_result}), 200 

@app.route('/api/disease/<id>', methods=['GET'])
def disease_doc(id: str):
    collection = db.get_collection(name='disease') # Collection
    d = collection.find_one(filter={'_id': jsonb.ObjectId(id)}, 
            projection={'疾病链接':0, 'pdf链接':0, '英文名':0, '别名':0, '所属科目':0, 'ICD号':0})
    result = reconstruce_doc(d)
    return jsonify(result), 200

@app.route('/api/chat', methods=['GET', 'POST'])
def chat():
    msg = request.args.get('msg')
    it_type = intention_classifier.classify(msg)
    resp = ChatResponse(it_type, msg).build()
    return jsonify({'data': resp}), 200


if __name__ == "__main__":
    app.run(debug=True)