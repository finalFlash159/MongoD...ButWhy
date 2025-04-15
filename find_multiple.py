import datetime
import os
import pprint

from dotenv import load_dotenv
from pymongo import MongoClient

# Import ObjectId from bson
from bson import ObjectId

# Load config from .env file
load_dotenv()
MONGODB_URI = os.environ["MONGODB_URI"]

# Connect to MongoDb cluster with MongoClient
client = MongoClient(MONGODB_URI)

# Get the reference to the database
db = client.sample_mflix

# Get the reference to the collection
movies_collection = db.movies

# Query
documents_to_find = {"released": {"$gte": datetime.datetime(1935, 1, 1)}}

# Write the expression that finds the documents with the specified ObjectId
cursor = movies_collection.find(documents_to_find)

num_docs = 0
for doc in cursor:
    num_docs += 1
    pprint.pprint(doc)
    print("")
print(f"Number of documents found: {num_docs}")

client.close()