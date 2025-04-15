import os
import pprint

from dotenv import load_dotenv
from pymongo import MongoClient

# Load config from .env file
load_dotenv()
MONGO_URI = os.environ["MONGODB_URI"]

# Connect to MongoDB cluster 
client = MongoClient(MONGO_URI)

db = client.bank

# Get the reference to the collection
accounts_collection = db.accounts

# Calculate the average balance of checking and savings accounts with balances of less than $1000

# Select accounts with balances of less than $1000
select_by_balance ={"$match": {"balance": {"$lt": 1000}}}

# Separate documents by account type and calculate the average balance for each account type
separate_by_account_calculate_avg_balance = {
    "$group": {"_id": "$account_type", "avg_balance": {"$avg": "$balances"}}
}

# Create an aggregation pipeline using 'stage_match_balance' and 'stage_group_account_type'

pipeline = [
    select_by_balance,
    separate_by_account_calculate_avg_balance
]

# Perform the aggregation on 'pipeline'
results = accounts_collection.agggregate(pipeline)

print()
print("Average balance of checking and savings accounts with balances of less than $1000:")

for item in results:
    pprint.pprint(item)

# Close the connection
client.close()