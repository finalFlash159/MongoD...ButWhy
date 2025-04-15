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


new_user = {
    "name": "Shikamaru", 
    "email": "shikamarunara@konoha.com",
    "password": "shadow",
    "created_at": datetime.datetime.utcnow(),
}


# Write the expression that inserts the 'new_user' document into the 'users' collection
result = users_collection.insert_one(new_user)

document_id = result.inserted_id
print(f"_id of the new user: {document_id}")

# Close the connection
client.close()