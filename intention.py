# coding: utf8

# 意图识别
import re
from model import db

class IT_TYPE:
    CONCEPT = 1
    CHAT = 2
    INQUIRY = 3
    TREATMENT = 4


class IntentionClassifier:
    def __init__(self, train=False):
        if train:
            self.model = self.train()
        else:
            self.model = self.load_model()
        

    def classify(self, msg: str):
        collection = db.get_collection(name='disease') # Collection
        if collection.find_one(filter={'疾病名称': msg}):
            return IT_TYPE.CONCEPT
        status, entity = self._match_treat(msg)
        if status:
            return IT_TYPE.TREATMENT, entity
        status, entity = self._match_inquiry(msg)
        if status:
            return IT_TYPE.INQUIRY, entity
        return IT_TYPE.CHAT

    def train(self, ):
        return None

    def load_model(self, path: str):
        return None
        

    def save_model(self, path: str):
        return None

    def _build_model(self):
        pass

    def _match_treat(self, msg):
        patt1 = re.compile(r'.*?得了(.*?)[该]*怎么办[\?]*')
        patt2 = re.compile(r'(.*?)怎么治[\?]')
        
        all_patts = [patt1, patt2]
        for patt in all_patts:
            mat_obj = patt.match(msg)
            if mat_obj:
                entity = mat_obj.group(1)
                return True, entity
        else: return False, None

    def _match_inquiry(self, msg):
         
        return False, None


intention_classifier = IntentionClassifier(train=False)