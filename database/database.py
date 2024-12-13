from pymongo import MongoClient
from config import DB_URL, DB_NAME

class Database:
    def __init__(self):
        self.client = MongoClient(DB_URL)
        self.db = self.client[DB_NAME]

    def get_collection(self, name):
        return self.db[name]

    def insert_or_update(self, collection, query, update, upsert=False):
        """Insert a new document or update an existing one."""
        collection = self.get_collection(collection)
        result = collection.update_one(query, update, upsert=upsert)
        return result
