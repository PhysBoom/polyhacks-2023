import pymongo
import os


class Database:
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(
            os.environ.get("MONGODB_URI"), uuidRepresentation="standard"
        )
        Database.DATABASE = client["production"]

    @staticmethod
    def insert_one(collection, data):
        Database.DATABASE[collection].insert_one(data)  # type: ignore

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)  # type: ignore

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)  # type: ignore

    @staticmethod
    def update_one(collection, query, data):
        Database.DATABASE[collection].update_one(query, data, upsert=True)  # type: ignore

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)  # type: ignore

    @staticmethod
    def aggregate(collection, pipeline):
        return Database.DATABASE[collection].aggregate(pipeline)  # type: ignore
