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
users_collection = db.users

# Query by ObjectId
document_to_find = ObjectId("67fe0bd2d56bd449a4997610")

# Write the expression that finds the document with the specified ObjectId
result = users_collection.find_one({"_id": document_to_find})
pprint.pprint(result)

client.close()