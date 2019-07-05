# coding: utf8

# 意图识别
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

        return 1

    def train(self, ):
        return None

    def load_model(self, path: str):
        return None
        

    def save_model(self, path: str):
        return None

intention_classifier = IntentionClassifier(train=False)