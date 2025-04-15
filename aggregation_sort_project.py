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


# Return the account type, original balance, and balance converted to Great Bristish Pounds (GBP)
# of all checking accounts with an original balance of greater then $1,500 US dollars, in order from highest original balance to lowest.

# To calculate the balance in GBP, divide the original balance by the conversion rate
conversion_rate_us_to_gbp = 1.3

# Select checking accounts with balances of mare than $1.500
select_accounts = {"$match": {"account_type": "checking", "balance": {"$gt": 1500}}}

# Organize the documents by balance in descending order
organize_by_original_balance = {"$sort": {"balance": -1}}

# Return the account type & balance fields, plus a new field containing balance in Great bristish Pounds (GBP)
return_specified_fields = {
    "$project": {
        "account_type:": 1, 
        "balance": 1, 
        "gbp_balance": {"$divide": ["$balance", conversion_rate_us_to_gbp]},
        "_id": 0
    }
}


# Create an aggregation pipeline containing the four stages created above
pipeline = [
    select_accounts,
    organize_by_original_balance,
    return_specified_fields
]

# Perform the aggregation on 'pipeline'
results = accounts_collection.aggregate(pipeline)
print()
print("Checking accounts with an original balance of greater than $1,500 US dollars:")
for item in results:
    pprint.pprint(item)
    print("")
# Close the connection
client.close()