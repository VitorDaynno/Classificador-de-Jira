from pymongo import MongoClient

class Mongo_DAO:

    def __init__(self,host, port, db):
        self._client = MongoClient(host,port)
        self._db = self._client[db]

    def insert(self, collection, item):
        cursor = self._db[collection]
        cursor.insert(item)
    
    def update(self, collection, filters, fields):
        cursor = self._db[collection]
        cursor.update(filters, fields)