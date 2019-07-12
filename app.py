import pprint
import json
import jieba
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import json_util as jsonb
from setting import config
from intention import intention_classifier, IT_TYPE
from model import db


app = Flask(__name__)

app.config.from_object(config)

DELETE_KEYS = ['']

collection = db.get_collection(name='disease')


class ChatResponse:
    def __init__(self, it_type, msg, *args, **kwargs):
        self.it_type = it_type
        self.msg = msg

    def build(self):
        if self.it_type == IT_TYPE.CONCEPT: # 概念
            return self._build_concept_resp()
        elif self.it_type == IT_TYPE.CHAT: # 闲聊
            return self._build_chat_resp()
        elif self.it_type == IT_TYPE.INQUIRY: # 巡诊
            return self._build_inquiry_resp()
        elif self.it_type == IT_TYPE.TREATMENT: # 治疗
            return self._build_treatment_resp()

    def _build_concept_resp(self):
        result = collection.find_one(filter={'疾病名称': self.msg}, 
            projection={'_id': 1, '概述': 1, '疾病名称': 1})
        id_ = result.pop('_id')
        result['id'] = str(id_)
        result['desc'] = result.pop('概述')
        result['title'] = result.pop('疾病名称')
        result['type'] = '1'
        return result

    def _build_chat_resp(self):
        return None

    def _build_inquiry_resp(self):
        return None

    def _build_treatment_resp(self):
        return None

def reconstruce_doc(disease_doc: dict):
    new_d = {}
    new_d['name'] = disease_doc.pop('疾病名称')
    disease_doc.pop('_id')
    new_d['data'] = disease_doc
    return new_d

# 搜索
def query_similarity_calculation(seg_query, title_query):
    counter = 0
    for s in seg_query:
        for t in title_query:
            if s == t:
                counter += 1
    return float(counter) / (len(seg_query) + len(title_query) + 1)


def similarity_sort(l: list, page, per_page):
    sorted_result = sorted(l, key=lambda x:x[1], reverse=True)
    return sorted_result[(page-1)*per_page:page*per_page]


def search_result(query: str, page, per_page):
    result = []
    similarities = []
    seg_query = jieba.cut_for_search(query)
    collection = db.get_collection(name='new_disease')  # Collection
    for doc in collection.find(filter={}):
        seg_title = doc['seg_title']
        id_ = str(doc['_id'])
        similarity = query_similarity_calculation(seg_query, seg_title)
        similarities.append((id_, similarity))
    sim_top_ids = similarity_sort(similarities, page, per_page)
    for id_, _ in sim_top_ids:
        doc = collection.find_one(filter={'_id': jsonb.ObjectId(id_)})
        result.append(doc)
    return result


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
            # projection={'疾病链接':0, 'pdf链接':0, '英文名':0, '别名':0, '所属科目':0, 'ICD号':0,})
        projection={'疾病名称':1, '概述':1, '临床表现':1, '治疗':1, '预防': 1})
    result = reconstruce_doc(d)
    return jsonify(result), 200


@app.route ('/api/chat', methods=['GET', 'POST'])
def chat():
    msg = request.args.get('msg')
    print(msg)
    it_type = intention_classifier.classify(msg)
    resp = ChatResponse(it_type, msg).build()
    return jsonify({'data': resp}), 200


@app.route('/api/search', methods=['GET', 'POST'])
def search_disease():
    query = request.args.get('query')
    page = request.args.get('page')
    per_page: int = app.config['PER_PAGE']
    result = search_result(query, page, per_page)
    return jsonify({'data': result}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5050, host='0.0.0.0')  