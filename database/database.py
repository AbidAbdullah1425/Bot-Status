from pymongo import MongoClient
from config import DB_URL, DB_NAME

class Database:
    def __init__(self):
        self.client = MongoClient(DB_URL)
        self.db = self.client[DB_NAME]

    def insert_or_update(self, collection, query, update, upsert=False):
        """Insert a new document or update an existing one."""
        result = self.db[collection].update_one(query, update, upsert=upsert)
        return result

    def delete_one(self, collection, query):
        """Delete a document."""
        result = self.db[collection].delete_one(query)
        return result

    def find_all(self, collection):
        """Find all documents in a collection."""
        return list(self.db[collection].find())
