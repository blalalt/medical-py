import pprint
import json
from flask import Flask, jsonify
from pymongo import MongoClient
from bson import json_util as jsonb
from setting import config

db = MongoClient()['medical']
app = Flask(__name__)

app.config.from_object(config)


@app.route('/api/disease_list/<int:page>', methods=['GET'])
def disease_list(page: int=0):
    collection = db.get_collection(name='disease') # Collection
    per_page: int = app.config['PER_PAGE']
    find_result = collection.find(filter={}, limit=per_page, sort={}, skip=per_page*page) # Cursor
    # pprint.pprint(jsonb.dumps(list(find_result)))
    u_result = jsonb.dumps(list(find_result))
    # print('type: ', type(jsonb.dumps(list(find_result))), jsonb.dumps(list(find_result)))
    return jsonify(json.loads(u_result))



if __name__ == "__main__":
    app.run(debug=True)