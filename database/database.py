from pymongo import MongoClient
from config import DB_URL, DB_NAME

class Database:
    def __init__(self):
        self.client = MongoClient(DB_URL)
        self.db = self.client[DB_NAME]

    def get_collection(self, name):
        return self.db[name]
      
