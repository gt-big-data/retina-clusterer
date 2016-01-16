from pymongo import MongoClient, errors

client = MongoClient('mongodb://143.215.138.132:27017/') # Old GCE instance: mongodb://146.148.59.202:27017/
db = client['big_data']