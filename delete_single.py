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
document_to_delete = {"_id": ObjectId("67fe0bd2d56bd449a4997610")}

# Search for the document before deleting
print("Searching for the document to delete: ")
pprint.pprint(users_collection.find_one(document_to_delete))


# Write the expression that deletes the document with the specified ObjectId
result = users_collection.delete_one(document_to_delete)
print(f"Number of documents deleted: {result.deleted_count}")

client.close()