import pymongo
from pymongo import ASCENDING, DESCENDING
from config.config import Config


class Mongo:

    def __init__(self):
        config = Config()
        self.client = config.set_mongo()
        self.db = self.client["upbit"]
        self.col = None
        self.inserted_id = None
        self.doc = None

    def get_col_list(self):

        return self.db.collection_names()

    def set_col(self, col):

        self.col = self.db[col]
        return self.col

    def is_col(self):

        if self.col:
            if self.col.name in self.get_col_list():
                return True

        return False

    def insert_doc(self, post):

        self.inserted_id = None
        if self.is_col():
            self.inserted_id = self.col.insert_one(post).inserted_id

        return self.inserted_id

    def get_doc_one(self):

        self.doc = None
        if self.is_col():
            self.doc = self.col.find_one(sort=[("_id", -1)])

        return self.doc

    def get_doc(self, limit):

        results = self.col.find().sort("_id", DESCENDING).limit(limit)

        data_list = []
        for result in results:
            data_list.append(result)

        return data_list
