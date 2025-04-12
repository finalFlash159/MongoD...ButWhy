import os

from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()
MONGODB_URI = os.environ["MONGODB_URI"]

client = MongoClient(MONGODB_URI)

# test connection
for db in client.list_database_names():
    print(db)

client.close()