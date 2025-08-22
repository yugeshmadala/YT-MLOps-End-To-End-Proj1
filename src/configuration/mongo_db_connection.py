import os
import sys
import pymongo
import certifi

from dotenv import load_dotenv
from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGODB_URL_KEY

# Load .env file
load_dotenv()

# Fetch Mongo URI and strip any accidental quotes
mongo_uri = os.getenv(MONGODB_URL_KEY)
if mongo_uri:
    mongo_uri = mongo_uri.strip().strip('"').strip("'")  # Remove quotes and whitespace

# Debug print
print("DEBUG Mongo URI:", repr(mongo_uri))

if not mongo_uri or not mongo_uri.startswith(("mongodb://", "mongodb+srv://")):
    raise ValueError("Invalid URI scheme: URI must begin with 'mongodb://' or 'mongodb+srv://'")

ca = certifi.where()

class MongoDBClient:
    client = None

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                if mongo_uri is None:
                    raise Exception(f"Environment variable '{MONGODB_URL_KEY}' is not set.")
                MongoDBClient.client = pymongo.MongoClient(mongo_uri, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection successful.")
        except Exception as e:
            raise MyException(e, sys)
