import datetime
import os

from dotenv import load_dotenv
from pymongo import MongoClient

# Load config from .env file
load_dotenv()
MONGODB_URI = os.environ["MONGODB_URI"]

# Connect to MongoDb cluster with MongoClient
client = MongoClient(MONGODB_URI)

# Get the reference to the database
db = client.sample_mflix

# Get the reference to the collection
users_collection = db.users

# Create a new user array
new_users = [
    {
        "name": "Naruto",
        "email": "12342asd34@sf",
        "password": "123AQ4234",
        "created_at": datetime.datetime.utcnow(),
    },
    {
        "name": "Sakura",
        "email": "123asfac234@sf",
        "password": "1234aa234",
        "created_at": datetime.datetime.utcnow(),
    }
]

# Write the expression that inserts the 'new_user' document into the 'users' collection
result = users_collection.insert_many(new_users)

document_ids = result.inserted_ids
print("# of documents inserted: " + str(len(document_ids)))
print(f"_ids of inserted documents: {document_ids}")

# Close the connection
client.close()